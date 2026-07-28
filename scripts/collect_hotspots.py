"""
热点数据采集脚本
从微博、百度、知乎、36氪、政府网站等数据源采集热点信息
"""

import json
import os
import re
import hashlib
import logging
from datetime import datetime, date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/collect.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 项目根目录
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'hotspots'
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 关键词过滤
KEYWORDS = ['AI', '人工智能', '科技', '营销', '广西', '东盟', '数字化', '智能化',
            '大模型', 'ChatGPT', '自动化', '机器学习', '深度学习', '数据', '互联网',
            '创业', '电商', '东南亚', '南宁', '政策']

# HTTP请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def compute_hash(text: str) -> str:
    """计算文本的MD5哈希值用于去重"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def is_relevant(title: str) -> bool:
    """判断标题是否与关键词相关"""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in KEYWORDS)


def collect_weibo() -> list:
    """采集微博热搜"""
    logger.info("开始采集微博热搜...")
    items = []
    try:
        url = 'https://weibo.com/ajax/side/hotSearch'
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get('data', {}).get('realtime', [])[:50]:
            word = item.get('word', '')
            if is_relevant(word):
                items.append({
                    'source': 'weibo',
                    'title': word,
                    'heat': item.get('num', 0),
                    'url': f'https://s.weibo.com/weibo?q=%23{word}%23',
                    'category': item.get('category', ''),
                    'timestamp': datetime.now().isoformat(),
                    'hash': compute_hash(word)
                })
        logger.info(f"微博热搜采集完成，相关条目: {len(items)}")
    except Exception as e:
        logger.error(f"微博热搜采集失败: {e}")
    return items


def collect_baidu() -> list:
    """采集百度热搜"""
    logger.info("开始采集百度热搜...")
    items = []
    try:
        url = 'https://top.baidu.com/board?tab=realtime'
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 尝试从页面JSON数据提取
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'hotList' in script.string:
                match = re.search(r'"hotList"\s*:\s*(\[.*?\])\s*,\s*"', script.string, re.DOTALL)
                if match:
                    hot_list = json.loads(match.group(1))
                    for item in hot_list[:50]:
                        title = item.get('content', {}).get('query', '')
                        if is_relevant(title):
                            items.append({
                                'source': 'baidu',
                                'title': title,
                                'heat': int(item.get('content', {}).get('hotScore', 0)),
                                'url': item.get('content', {}).get('url', ''),
                                'timestamp': datetime.now().isoformat(),
                                'hash': compute_hash(title)
                            })
                    break

        # 如果JSON解析失败，尝试HTML解析
        if not items:
            cards = soup.select('.category-wrap_iQLoo .content_1Ywbm')
            for card in cards[:50]:
                title_el = card.select_one('.c-single-text-ellipsis')
                if title_el:
                    title = title_el.get_text(strip=True)
                    if is_relevant(title):
                        desc_el = card.select_one('.small_Uvkd3')
                        heat_el = card.select_one('.hot-index_1Bl1a')
                        items.append({
                            'source': 'baidu',
                            'title': title,
                            'heat': int(heat_el.get_text(strip=True)) if heat_el else 0,
                            'url': 'https://www.baidu.com/s?wd=' + title,
                            'description': desc_el.get_text(strip=True) if desc_el else '',
                            'timestamp': datetime.now().isoformat(),
                            'hash': compute_hash(title)
                        })
        logger.info(f"百度热搜采集完成，相关条目: {len(items)}")
    except Exception as e:
        logger.error(f"百度热搜采集失败: {e}")
    return items


def collect_zhihu() -> list:
    """采集知乎热榜"""
    logger.info("开始采集知乎热榜...")
    items = []
    try:
        url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total'
        headers = {**HEADERS, 'Referer': 'https://www.zhihu.com/hot'}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get('data', [])[:50]:
            target = item.get('target', {})
            title = target.get('title', '')
            if is_relevant(title):
                items.append({
                    'source': 'zhihu',
                    'title': title,
                    'heat': int(item.get('detail_text', '0').replace('万热度', '0000').replace(' 万热度', '0000') or 0),
                    'url': f'https://www.zhihu.com/question/{target.get("id", "")}',
                    'answer_count': target.get('answer_count', 0),
                    'timestamp': datetime.now().isoformat(),
                    'hash': compute_hash(title)
                })
        logger.info(f"知乎热榜采集完成，相关条目: {len(items)}")
    except Exception as e:
        logger.error(f"知乎热榜采集失败: {e}")
    return items


def collect_36kr() -> list:
    """采集36氪热门文章"""
    logger.info("开始采集36氪...")
    items = []
    try:
        url = 'https://36kr.com/hot-list/catalog'
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        articles = soup.select('.article-item-title, .hotlist-item-tool-c a')
        for article in articles[:30]:
            title = article.get_text(strip=True)
            if is_relevant(title):
                link = article.get('href', '')
                if link and not link.startswith('http'):
                    link = 'https://36kr.com' + link
                items.append({
                    'source': '36kr',
                    'title': title,
                    'heat': 0,
                    'url': link,
                    'timestamp': datetime.now().isoformat(),
                    'hash': compute_hash(title)
                })
        logger.info(f"36氪采集完成，相关条目: {len(items)}")
    except Exception as e:
        logger.error(f"36氪采集失败: {e}")
    return items


def deduplicate(items: list) -> list:
    """去重：基于标题哈希"""
    seen = set()
    unique = []
    for item in items:
        h = item.get('hash', '')
        if h not in seen:
            seen.add(h)
            unique.append(item)
    return unique


def save_hotspots(items: list):
    """保存热点数据到JSON文件"""
    today = date.today().isoformat()
    filepath = DATA_DIR / f'{today}.json'

    # 如果文件已存在，合并数据
    existing = []
    if filepath.exists():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except Exception:
            existing = []

    all_items = existing + items
    all_items = deduplicate(all_items)

    # 按热度排序
    all_items.sort(key=lambda x: x.get('heat', 0), reverse=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    logger.info(f"热点数据已保存到 {filepath}，共 {len(all_items)} 条")
    return len(all_items)


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始热点数据采集")
    logger.info("=" * 50)

    all_items = []

    # 依次采集各数据源
    collectors = [
        ('微博热搜', collect_weibo),
        ('百度热搜', collect_baidu),
        ('知乎热榜', collect_zhihu),
        ('36氪', collect_36kr),
    ]

    for name, collector in collectors:
        try:
            items = collector()
            all_items.extend(items)
            logger.info(f"{name}: 采集到 {len(items)} 条相关内容")
        except Exception as e:
            logger.error(f"{name}采集异常: {e}")

    # 去重并保存
    total = save_hotspots(all_items)
    logger.info(f"采集完成，共 {total} 条不重复热点")

    return total


if __name__ == '__main__':
    main()
