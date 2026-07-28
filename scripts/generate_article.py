"""
AI内容生成脚本
使用Claude API基于热点数据自动生成文章
"""

import json
import os
import re
import logging
from datetime import datetime, date
from pathlib import Path

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None

import frontmatter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/generate.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 项目路径
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
CONTENT_DIR = BASE_DIR / 'content' / 'posts'
TEMPLATES_DIR = BASE_DIR / 'templates' / 'prompts'
HISTORY_FILE = DATA_DIR / 'articles_history.json'

CONTENT_DIR.mkdir(parents=True, exist_ok=True)

# 质量控制参数
MIN_WORDS = 1000
MAX_WORDS = 3000
MAX_RETRIES = 3

# System Prompt
SYSTEM_PROMPT = """你是专业的科技媒体编辑，擅长将热点事件转化为深度分析文章。
要求：
1. 客观准确，引用数据需注明来源
2. 有独特视角和深度分析
3. 结合行业背景和政策环境
4. 语言通俗易懂，适合技术和管理层阅读
5. 文章结构清晰，逻辑连贯"""

# 热点文章模板
HOTSPOT_USER_PROMPT = """基于以下热点信息撰写一篇深度分析文章：

热点信息：
{hotspot_info}

背景资料：
{background_info}

要求：
1. 标题：吸引眼球但不夸张，20字以内
2. 摘要：150字左右，突出核心价值
3. 正文：1500-2500字，分3-5个小节
4. 结构：引言-背景分析-核心观点-影响评估-总结
5. 风格：专业但不生硬，有数据支撑
6. 标签：提取5-8个关键词作为tags

输出格式：完整的Markdown文本，包含YAML front-matter（title, date, tags, categories, summary, ai_generated字段）。
注意：直接输出Markdown内容，不要包含```markdown```代码块标记。"""

# 政策解读模板
POLICY_USER_PROMPT = """解读以下政策文件：

政策原文：
{policy_content}

要求：
1. 政策要点提炼（3-5条）
2. 对AI/科技行业的影响分析
3. 广西/南宁相关企业能获得的机遇
4. 实操建议（如何申请、注意事项）
5. 1500-2000字

输出：Markdown格式，含front-matter（title, date, tags: ["政策解读", ...], categories: ["政策解读"], summary, ai_generated: true）"""


def get_provider() -> str:
    """获取AI提供商（环境变量控制，默认claude）"""
    return os.environ.get('AI_PROVIDER', 'claude').lower()


def get_client():
    """获取AI客户端（支持 Claude / DeepSeek）"""
    provider = get_provider()

    if provider == 'deepseek':
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")
        if openai is None:
            raise ValueError("请安装openai: pip install openai")
        return openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )

    else:  # default: claude
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("请设置环境变量 ANTHROPIC_API_KEY")
        if anthropic is None:
            raise ValueError("请安装anthropic: pip install anthropic")
        return anthropic.Anthropic(api_key=api_key)


def load_hotspots() -> list:
    """加载今日热点数据"""
    today = date.today().isoformat()
    filepath = DATA_DIR / 'hotspots' / f'{today}.json'

    if not filepath.exists():
        logger.warning(f"今日热点数据不存在: {filepath}")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_history() -> list:
    """加载已发布文章历史"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_history(history: list):
    """保存文章历史"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def is_duplicate(title: str, history: list) -> bool:
    """检查文章是否重复"""
    for article in history:
        if article.get('title') == title:
            return True
    return False


def generate_with_claude(client, user_prompt: str, system: str = SYSTEM_PROMPT) -> str:
    """调用Claude API生成内容"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        temperature=0.7,
        system=system,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    return message.content[0].text


def generate_with_deepseek(client, user_prompt: str, system: str = SYSTEM_PROMPT) -> str:
    """调用DeepSeek API生成内容（OpenAI兼容格式）"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        max_tokens=4000,
        temperature=0.7,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


def generate_content(client, user_prompt: str, system: str = SYSTEM_PROMPT) -> str:
    """根据provider选择生成方式"""
    provider = get_provider()
    if provider == 'deepseek':
        return generate_with_deepseek(client, user_prompt, system)
    else:
        return generate_with_claude(client, user_prompt, system)


def quality_check(content: str) -> dict:
    """质量检查"""
    result = {
        'passed': True,
        'issues': [],
        'word_count': 0
    }

    # 去掉front-matter计算正文字数
    body = content
    fm_match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
    if fm_match:
        body = content[fm_match.end():]

    # 中文字数统计（粗略）
    chinese_chars = len(re.findall(r'[一-鿿]', body))
    result['word_count'] = chinese_chars

    if chinese_chars < MIN_WORDS:
        result['passed'] = False
        result['issues'].append(f'字数不足: {chinese_chars} < {MIN_WORDS}')

    if chinese_chars > MAX_WORDS:
        result['passed'] = False
        result['issues'].append(f'字数超限: {chinese_chars} > {MAX_WORDS}')

    # 检查front-matter
    if not content.startswith('---'):
        result['passed'] = False
        result['issues'].append('缺少front-matter')

    # 敏感词检测（示例）
    sensitive_words = ['赌博', '色情', '暴力', '反动']
    for word in sensitive_words:
        if word in content.lower():
            result['passed'] = False
            result['issues'].append(f'包含敏感词: {word}')

    return result


def generate_article(hotspot: dict, client) -> str | None:
    """基于热点生成文章"""
    title = hotspot.get('title', '')
    source = hotspot.get('source', '')
    url = hotspot.get('url', '')

    logger.info(f"正在生成文章: {title}")

    hotspot_info = f"""
标题: {title}
来源: {source}
链接: {url}
热度: {hotspot.get('heat', 'N/A')}
"""

    user_prompt = HOTSPOT_USER_PROMPT.format(
        hotspot_info=hotspot_info,
        background_info="广西正在推进'北上广研发＋广西集成＋东盟应用'战略，AI产业是重点发展方向。"
    )

    for attempt in range(MAX_RETRIES):
        try:
            content = generate_content(client, user_prompt)

            # 质量检查
            check = quality_check(content)
            if check['passed']:
                logger.info(f"文章生成成功，字数: {check['word_count']}")
                return content
            else:
                logger.warning(f"质量检查未通过 (尝试 {attempt + 1}/{MAX_RETRIES}): {check['issues']}")
        except Exception as e:
            logger.error(f"生成失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")

    logger.error(f"文章生成最终失败: {title}")
    return None


def save_article(content: str, title: str) -> str:
    """保存文章到content目录"""
    # 生成文件名
    today = date.today().isoformat()
    slug = re.sub(r'[^\w一-鿿]+', '-', title)[:50].strip('-')
    filename = f"{today}-{slug}.md"
    filepath = CONTENT_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    logger.info(f"文章已保存: {filepath}")
    return str(filepath)


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始AI内容生成")
    logger.info("=" * 50)

    # 加载热点数据
    hotspots = load_hotspots()
    if not hotspots:
        logger.error("没有可用的热点数据，请先运行采集脚本")
        return []

    # 加载历史
    history = load_history()

    # 初始化客户端
    try:
        client = get_client()
    except ValueError as e:
        logger.error(str(e))
        return []

    # 选择未生成过的热点（按热度排序取前3）
    generated_titles = {h.get('title') for h in history}
    candidates = [h for h in hotspots if h.get('title') not in generated_titles]

    if not candidates:
        logger.info("没有新的热点需要生成文章")
        return []

    # 每次最多生成3篇
    to_generate = candidates[:3]
    generated_files = []

    for hotspot in to_generate:
        content = generate_article(hotspot, client)
        if content:
            filepath = save_article(content, hotspot['title'])
            generated_files.append(filepath)

            # 更新历史
            history.append({
                'title': hotspot['title'],
                'source': hotspot.get('source', ''),
                'file': filepath,
                'publish_date': date.today().isoformat(),
                'tags': []
            })

    save_history(history)
    logger.info(f"生成完成，共 {len(generated_files)} 篇文章")
    return generated_files


if __name__ == '__main__':
    main()
