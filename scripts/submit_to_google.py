"""
Google链接提交脚本
使用Google Indexing API提交新文章
"""

import os
import json
import base64
import logging
from datetime import date
from pathlib import Path

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


def get_credentials_file(config: dict) -> str | None:
    """获取Google服务账号凭证文件路径"""
    # 优先使用环境变量
    creds_b64 = os.environ.get('GOOGLE_CREDENTIALS')
    if creds_b64:
        creds_file = BASE_DIR / 'data' / 'google_credentials.json'
        try:
            decoded = base64.b64decode(creds_b64).decode('utf-8')
            json.loads(decoded)  # 验证JSON格式
            with open(creds_file, 'w', encoding='utf-8') as f:
                f.write(decoded)
            return str(creds_file)
        except Exception as e:
            logger.error(f"解析GOOGLE_CREDENTIALS失败: {e}")

    # 使用配置文件中的路径
    creds_path = config.get('google_credentials_path', '')
    if creds_path:
        full_path = BASE_DIR / creds_path
        if full_path.exists():
            return str(full_path)

    return None


def get_new_urls(days: int = 1) -> list:
    """获取最近发布的文章完整URL"""
    urls = []
    today = date.today()
    site_url = load_config().get('site_url', 'https://aimarketing.site').rstrip('/')

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


def submit_to_google(urls: list, credentials_file: str) -> bool:
    """使用Google Indexing API提交URL"""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        logger.error("请安装: pip install google-api-python-client google-auth-httplib2 google-auth")
        return False

    SCOPES = ['https://www.googleapis.com/auth/indexing']

    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )

        service = build('indexing', 'v3', credentials=credentials)

        success_count = 0
        for url in urls:
            try:
                body = {
                    'url': url,
                    'type': 'URL_UPDATED'
                }
                response = service.urlNotifications().publish(body=body).execute()
                logger.info(f"Google提交成功: {url}")
                success_count += 1
            except Exception as e:
                logger.error(f"Google提交失败 {url}: {e}")

        logger.info(f"Google提交完成: {success_count}/{len(urls)} 成功")
        return success_count > 0

    except Exception as e:
        logger.error(f"Google API初始化失败: {e}")
        return False


def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("开始Google链接提交")
    logger.info("=" * 50)

    config = load_config()
    if not config.get('submit_enabled', True):
        logger.info("SEO提交已禁用")
        return True

    creds_file = get_credentials_file(config)
    if not creds_file:
        logger.warning("Google凭证未配置，跳过Google提交")
        return True

    urls = get_new_urls(days=1)
    if not urls:
        logger.info("没有新文章需要提交")
        return True

    success = submit_to_google(urls, creds_file)

    if success:
        logger.info("Google链接提交完成")
    else:
        logger.error("Google链接提交失败")

    return success


if __name__ == '__main__':
    main()
