"""
Bing Webmaster Tools 链接提交脚本
通过 Bing Webmaster API 提交新文章URL
"""

import os
import json
import logging
from datetime import date
from pathlib import Path

import requests
import frontmatter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/seo.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / 'data' / 'seo_config.yaml'
CONTENT_DIR = BASE_DIR / 'content'


def load_config() -> dict:
    """加载SEO配置"""
    if not CONFIG_FILE.exists():
        return {}
    import yaml
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_bing_api_key(config: dict) -> str:
    """获取Bing API Key"""
    return os.environ.get('BING_API_KEY') or config.get('bing_api_key', '')


def get_site_url(config: dict) -> str:
    """获取站点URL"""
    return config.get('site_url', 'https://aimarketing.site').rstrip('/')


def get_new_urls(days: int = 1) -> list:
    """获取最近发布的文章完整URL"""
    urls = []
    today = date.today()
    site_url = get_site_url(load_config())

    for md_file in CONTENT_DIR.rglob('*.md'):
        try:
            post = frontmatter.load(str(md_file))
            if hasattr(post, 'date') and post.date:
                post_date = post.date.date() if hasattr(post.date, 'date') else post.date
                if (today - post_date).days <= days:
                    rel_path = md_file.relative_to(CONTENT_DIR)
                    slug = rel_path.stem
                    if slug.startswith('_'):
                        continue
                    url = f"{site_url}/{post_date.year}/{post_date.month:02d}/{slug}/"
                    urls.append(url)
        except Exception as e:
            logger.warning(f"解析文件失败 {md_file}: {e}")

    return urls


def get_all_urls() -> list:
    """获取所有已发布文章的完整URL（用于首次批量提交）"""
    urls = []
    site_url = get_site_url(load_config())

    # 从 sitemap.xml 解析（如果存在）
    sitemap_path = BASE_DIR / 'public' / 'sitemap.xml'
    if sitemap_path.exists():
        import re
        content = sitemap_path.read_text(encoding='utf-8')
        urls_from_sitemap = re.findall(r'<loc>(.*?)</loc>', content)
        for url in urls_from_sitemap:
            if '/posts/' in url or ('/2026/' in url and '/tags/' not in url and '/categories/' not in url):
                urls.append(url)
        if urls:
            logger.info(f"从 sitemap.xml 提取了 {len(urls)} 个URL")
            return urls

    # 从 content 目录解析
    for md_file in CONTENT_DIR.rglob('*.md'):
        try:
            post = frontmatter.load(str(md_file))
            if hasattr(post, 'date') and post.date:
                post_date = post.date.date() if hasattr(post.date, 'date') else post.date
                rel_path = md_file.relative_to(CONTENT_DIR)
                slug = rel_path.stem
                if slug.startswith('_'):
                    continue
                if str(rel_path).startswith('posts/') or str(rel_path.parent) != '.':
                    url = f"{site_url}/{post_date.year}/{post_date.month:02d}/{slug}/"
                    urls.append(url)
        except Exception as e:
            logger.warning(f"解析文件失败 {md_file}: {e}")

    return urls


def submit_url_to_bing(url: str, api_key: str) -> bool:
    """提交单个URL到Bing"""
    api_url = "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey=" + api_key

    data = {
        "siteUrl": get_site_url(load_config()),
        "urlList": [url]
    }

    try:
        resp = requests.post(
            api_url,
            json=data,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            timeout=30
        )
        if resp.status_code == 200:
            logger.info(f"Bing提交成功: {url}")
            return True
        else:
            logger.warning(f"Bing提交失败 {url}: HTTP {resp.status_code} - {resp.text[:200]}")
            return False
    except Exception as e:
        logger.error(f"Bing提交异常 {url}: {e}")
        return False


def submit_sitemap_to_bing(api_key: str) -> bool:
    """通知Bing更新sitemap"""
    site_url = get_site_url(load_config())
    sitemap_url = f"{site_url}/sitemap.xml"

    # 通过ping方式通知
    ping_url = f"https://www.bing.com/ping?sitemap={sitemap_url}"

    try:
        resp = requests.get(ping_url, timeout=30)
        if resp.status_code == 200:
            logger.info(f"Bing sitemap ping 成功: {sitemap_url}")
            return True
        else:
            logger.warning(f"Bing sitemap ping 失败: HTTP {resp.status_code}")
            return False
    except Exception as e:
        logger.error(f"Bing sitemap ping 异常: {e}")
        return False


def submit_to_bing(urls: list, api_key: str) -> bool:
    """批量提交URL到Bing"""
    if not api_key:
        logger.warning("Bing API Key未配置，尝试sitemap ping方式")
        return submit_sitemap_to_bing(api_key="")

    success_count = 0
    for url in urls:
        if submit_url_to_bing(url, api_key):
            success_count += 1

    logger.info(f"Bing批量提交完成: {success_count}/{len(urls)} 成功")
    return success_count > 0


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始Bing链接提交")
    logger.info("=" * 50)

    config = load_config()
    if not config.get('submit_enabled', True):
        logger.info("SEO提交已禁用")
        return True

    api_key = get_bing_api_key(config)

    # 获取所有URL（首次可批量提交）
    urls = get_all_urls()
    if not urls:
        logger.info("没有URL需要提交")
        return True

    logger.info(f"共 {len(urls)} 个URL待提交")

    if api_key:
        success = submit_to_bing(urls, api_key)
    else:
        # 无API key时使用sitemap ping
        logger.info("未配置Bing API Key，使用Sitemap ping方式")
        success = submit_sitemap_to_bing("")

    if success:
        logger.info("Bing链接提交完成")
    else:
        logger.warning("Bing链接提交部分失败（可能未配置API Key）")

    return success


if __name__ == '__main__':
    main()
