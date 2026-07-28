"""
每日运营报告生成脚本
"""

import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)


def count_today_articles() -> int:
    """统计今日发布文章数"""
    today = date.today()
    content_dir = BASE_DIR / 'content' / 'posts'
    count = 0
    if content_dir.exists():
        for f in content_dir.glob(f'{today.isoformat()}-*.md'):
            count += 1
    return count


def count_hotspots() -> int:
    """统计今日采集热点数"""
    today = date.today()
    filepath = BASE_DIR / 'data' / 'hotspots' / f'{today.isoformat()}.json'
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data)
    return 0


def get_article_history() -> list:
    """获取文章发布历史"""
    history_file = BASE_DIR / 'data' / 'articles_history.json'
    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def generate_report() -> str:
    """生成每日报告"""
    today = date.today()
    yesterday = today - timedelta(days=1)

    articles_today = count_today_articles()
    hotspots_today = count_hotspots()
    history = get_article_history()
    total_articles = len(history)

    report = f"""# 每日运营报告 - {today.isoformat()}

## 📊 今日数据

| 指标 | 数值 |
|------|------|
| 采集热点数 | {hotspots_today} |
| 新增文章数 | {articles_today} |
| 累计文章数 | {total_articles} |

## 📝 最近文章

"""
    recent = history[-5:] if history else []
    if recent:
        for article in reversed(recent):
            report += f"- **{article.get('title', '无标题')}** ({article.get('publish_date', '')})\n"
    else:
        report += "_暂无文章_\n"

    report += f"""
## 🔧 系统状态

- 报告生成时间: {datetime.now().isoformat()}
- 数据目录: `data/hotspots/`
- 文章目录: `content/posts/`

## 📌 备注

- 工作日目标: 每天3篇文章
- 周末目标: 每天1篇文章
- API成本: 约 ¥0.5-2/篇

---
*报告由自动化系统生成*
"""
    return report


def main():
    today = date.today()
    report = generate_report()

    filepath = REPORTS_DIR / f'{today.isoformat()}.md'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)

    logger.info(f"每日报告已生成: {filepath}")
    return str(filepath)


if __name__ == '__main__':
    main()
