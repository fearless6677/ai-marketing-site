"""
百度链接提交脚本
将新发布的文章链接主动推送到百度搜索开放平台
"""

import os
import re
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
        logger.error(f"SEO配置文件不存在: {CONFIG_FILE}")
        return {}

    import yaml
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_site_url(config: dict) -> str:
    """获取站点URL"""
    return config.get('site_url', 'https://aimarketing.site').rstrip('/')


def get_baidu_token(config: dict) -> str:
    """获取百度推送token"""
    token = os.environ.get('BAIDU_TOKEN') or config.get('baidu_token', '')
    return token


def get_new_urls(days: int = 1) -> list:
    """获取最近发布的文章URL"""
    urls = []
    today = date.today()

    for md_file in CONTENT_DIR.rglob('*.md'):
        try:
            post = frontmatter.load(str(md_file))
            if hasattr(post, 'date') and post.date:
                post_date = post.date.date() if hasattr(post.date, 'date') else post.date
                if (today - post_date).days <= days:
                    # 构造URL路径
                    rel_path = md_file.relative_to(CONTENT_DIR)
                    slug = rel_path.stem
                    if slug.startswith('_'):
                        continue

                    # 按日期路径格式
                    url_path = f"/{post_date.year}/{post_date.month:02d}/{slug}/"
                    urls.append(url_path)
        except Exception as e:
            logger.warning(f"解析文件失败 {md_file}: {e}")

    return urls


def submit_to_baidu(urls: list, site_url: str, token: str) -> bool:
    """提交URL到百度"""
    if not token:
        logger.warning("百度推送token未配置，跳过")
        return False

    if not urls:
        logger.info("没有新URL需要提交")
        return True

    full_urls = [f"{site_url}{url}" for url in urls]
    api_url = f"http://data.zz.baidu.com/urls?site={site_url}&token={token}"

    logger.info(f"准备提交 {len(full_urls)} 个URL到百度")

    try:
        resp = requests.post(
            api_url,
            data='\n'.join(full_urls),
            headers={'Content-Type': 'text/plain'},
            timeout=30
        )

        result = resp.json()
        if result.get('success'):
            logger.info(f"百度推送成功: 成功{result.get('success')}条, 剩余{result.get('remain')}条配额")
            return True
        else:
            logger.error(f"百度推送失败: {result}")
            return False

    except Exception as e:
        logger.error(f"百度推送异常: {e}")
        return False


def update_sitemap() -> bool:
    """更新sitemap（Hugo会自动生成，这里做备份）"""
    sitemap_path = BASE_DIR / 'public' / 'sitemap.xml'
    if sitemap_path.exists():
        logger.info("Sitemap已由Hugo生成")
        return True
    return False


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始百度链接提交")
    logger.info("=" * 50)

    config = load_config()
    if not config:
        logger.error("无法加载SEO配置")
        return False

    site_url = get_site_url(config)
    token = get_baidu_token(config)

    if not token:
        logger.warning("百度token未配置")
        return False

    urls = get_new_urls(days=1)
    if not urls:
        logger.info("没有新文章需要提交")
        return True

    success = submit_to_baidu(urls, site_url, token)

    if success:
        logger.info("百度链接提交完成")
    else:
        logger.error("百度链接提交失败")

    return success


if __name__ == '__main__':
    main()
