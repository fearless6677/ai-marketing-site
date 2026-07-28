"""
SEO验证脚本 - 检查站点SEO配置完整性
生成SEO检查清单和验证报告
"""

import os
import re
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
PUBLIC_DIR = BASE_DIR / 'public'
LAYOUTS_DIR = BASE_DIR / 'layouts'
CONFIG_FILE = BASE_DIR / 'config.yaml'


class SEOChecker:
    """SEO检查器"""

    def __init__(self):
        self.results = []
        self.warnings = []
        self.errors = []
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def check(self, name: str, passed: bool, message: str = "", warning: bool = False):
        """记录检查结果"""
        if passed:
            self.results.append(('✅ PASS', name, message))
            self.passed += 1
        elif warning:
            self.results.append(('⚠️ WARN', name, message))
            self.warnings.append(name)
        else:
            self.results.append(('❌ FAIL', name, message))
            self.errors.append(name)
            self.failed += 1

    def skip(self, name: str, reason: str):
        """记录跳过的检查"""
        self.results.append(('⏭️ SKIP', name, reason))
        self.skipped += 1

    def check_sitemap(self):
        """检查 sitemap.xml"""
        sitemap = PUBLIC_DIR / 'sitemap.xml'
        if not sitemap.exists():
            self.check("Sitemap.xml 存在", False, "Hugo未生成sitemap.xml")
            return

        self.check("Sitemap.xml 存在", True)

        content = sitemap.read_text(encoding='utf-8')

        # 检查格式
        is_xml = '<?xml' in content and '<urlset' in content
        self.check("Sitemap.xml 格式正确", is_xml, "缺少XML声明或urlset标签")

        # 检查URL数量
        url_count = len(re.findall(r'<loc>', content))
        self.check("Sitemap.xml 包含URL", url_count > 0, f"共 {url_count} 个URL")

        # 检查priority标签
        has_priority = '<priority>' in content
        self.check("Sitemap.xml 有priority", has_priority, "缺少priority标签", warning=True)

        # 检查changefreq
        has_changefreq = '<changefreq>' in content
        self.check("Sitemap.xml 有changefreq", has_changefreq, "缺少changefreq标签", warning=True)

        # 检查首页priority=1.0
        if '1.0</priority>' in content:
            self.check("Sitemap.xml 首页高优先级", True)
        else:
            self.check("Sitemap.xml 首页高优先级", False, "首页priority应设为1.0", warning=True)

    def check_robots_txt(self):
        """检查 robots.txt"""
        robots = PUBLIC_DIR / 'robots.txt'
        if not robots.exists():
            self.check("robots.txt 存在", False, "Hugo未生成robots.txt")
            return

        self.check("robots.txt 存在", True)

        content = robots.read_text(encoding='utf-8')

        # 检查User-agent
        has_user_agent = 'User-agent' in content
        self.check("robots.txt 有User-agent", has_user_agent, "缺少User-agent指令")

        # 检查Sitemap声明
        has_sitemap = 'Sitemap:' in content
        self.check("robots.txt 声明Sitemap", has_sitemap, "缺少Sitemap: 声明", warning=True)

        # 检查sitemap URL
        if has_sitemap:
            sitemap_line = [l for l in content.split('\n') if 'Sitemap:' in l][0]
            has_correct_url = 'https://aimarketing.site/sitemap.xml' in sitemap_line
            self.check("robots.txt Sitemap URL正确", has_correct_url,
                      f"当前: {sitemap_line.strip()}")

        # 检查百度蜘蛛规则
        has_baidu = 'Baiduspider' in content
        self.check("robots.txt 百度蜘蛛规则", has_baidu, "缺少Baiduspider规则", warning=True)

    def check_meta_tags(self):
        """检查HTML中的meta标签"""
        # 检查首页
        index_html = PUBLIC_DIR / 'index.html'
        if not index_html.exists():
            self.skip("Meta标签检查", "首页HTML不存在")
            return

        content = index_html.read_text(encoding='utf-8')

        # Title
        has_title = '<title>' in content
        self.check("首页有Title标签", has_title)

        # Meta description
        has_description = 'name="description"' in content
        self.check("首页有meta description", has_description, "缺少description标签")

        # Meta keywords
        has_keywords = 'name="keywords"' in content
        self.check("首页有meta keywords", has_keywords, "缺少keywords标签", warning=True)

        # Canonical
        has_canonical = 'rel="canonical"' in content
        self.check("首页有canonical URL", has_canonical, "缺少canonical标签")

        # Open Graph
        has_og = 'og:title' in content
        self.check("首页有Open Graph标签", has_og, "缺少OG标签")

        # Twitter Card
        has_twitter = 'twitter:card' in content
        self.check("首页有Twitter Card标签", has_twitter, "缺少Twitter Card标签")

    def check_schema_json(self):
        """检查Schema.org JSON-LD"""
        index_html = PUBLIC_DIR / 'index.html'
        if not index_html.exists():
            self.skip("Schema.org检查", "首页HTML不存在")
            return

        content = index_html.read_text(encoding='utf-8')

        # 查找所有JSON-LD
        jsonld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        jsonld_blocks = re.findall(jsonld_pattern, content, re.DOTALL)

        self.check("首页有JSON-LD", len(jsonld_blocks) > 0,
                  f"找到 {len(jsonld_blocks)} 个JSON-LD块")

        # 检查各类型
        all_jsonld = '\n'.join(jsonld_blocks)
        has_org = '"Organization"' in all_jsonld or '"@type": "Organization"' in all_jsonld
        has_website = '"WebSite"' in all_jsonld
        has_search = '"SearchAction"' in all_jsonld

        self.check("Schema.org Organization", has_org, "缺少Organization schema")
        self.check("Schema.org WebSite", has_website, "缺少WebSite schema", warning=True)
        self.check("Schema.org SearchAction", has_search, "缺少SearchAction", warning=True)

    def check_article_schema(self):
        """检查文章页Schema.org"""
        # 查找第一篇文章
        article_found = False
        for article_dir in (PUBLIC_DIR / '2026').glob('*/*/') if (PUBLIC_DIR / '2026').exists() else []:
            for sub in article_dir.iterdir():
                if sub.is_dir() and (sub / 'index.html').exists():
                    content = (sub / 'index.html').read_text(encoding='utf-8')
                    has_blog_posting = '"BlogPosting"' in content
                    has_breadcrumb = '"BreadcrumbList"' in content
                    self.check("文章页有BlogPosting Schema", has_blog_posting, "缺少BlogPosting schema")
                    self.check("文章页有BreadcrumbList Schema", has_breadcrumb, "缺少BreadcrumbList schema")
                    article_found = True
                    break
            if article_found:
                break

        if not article_found:
            self.skip("文章Schema检查", "未找到已发布的文章")

    def check_performance(self):
        """检查性能优化"""
        # CSS压缩
        css_files = list(PUBLIC_DIR.glob('assets/css/*.css'))
        if css_files:
            minified = any('.min.' in f.name or '.min.' in f.read_text(encoding='utf-8', errors='ignore')[:200]
                          for f in css_files[:3])
            self.check("CSS文件存在", True, f"共 {len(css_files)} 个CSS文件")
        else:
            self.skip("CSS检查", "未找到CSS文件")

        # 图片懒加载
        index_html = PUBLIC_DIR / 'index.html'
        if index_html.exists():
            content = index_html.read_text(encoding='utf-8')
            has_lazy = 'loading="lazy"' in content or 'loading=lazy' in content
            self.check("图片懒加载属性", has_lazy, "图片缺少loading=lazy", warning=True)

        # Hugo minify
        config_text = CONFIG_FILE.read_text(encoding='utf-8') if CONFIG_FILE.exists() else ""
        has_minify = 'minifyOutput' in config_text or 'minify:' in config_text
        self.check("Hugo Minify配置", has_minify, "未启用minify", warning=True)

    def check_cache_headers(self):
        """检查缓存配置"""
        config_text = CONFIG_FILE.read_text(encoding='utf-8') if CONFIG_FILE.exists() else ""
        has_server = 'server:' in config_text
        has_cache = 'Cache-Control' in config_text

        self.check("服务器缓存头配置", has_server and has_cache,
                  "未配置服务器缓存头", warning=True)

    def check_dns_prefetch(self):
        """检查DNS预取"""
        index_html = PUBLIC_DIR / 'index.html'
        if not index_html.exists():
            self.skip("DNS预取检查", "首页不存在")
            return

        content = index_html.read_text(encoding='utf-8')
        has_prefetch = 'dns-prefetch' in content
        has_preconnect = 'preconnect' in content

        self.check("DNS Prefetch", has_prefetch, "缺少dns-prefetch", warning=True)
        self.check("Preconnect", has_preconnect, "缺少preconnect", warning=True)

    def check_social_meta(self):
        """检查社交元数据"""
        config_text = CONFIG_FILE.read_text(encoding='utf-8') if CONFIG_FILE.exists() else ""

        # OG配置
        has_social = 'social:' in config_text
        self.check("社交元数据配置", has_social, "缺少social配置", warning=True)

        # Schema sameAs
        has_sameas = 'sameAs' in config_text or 'socialIcons' in config_text
        self.check("Schema.org sameAs配置", has_sameas, "缺少sameAs配置")

    def run_all_checks(self):
        """运行所有检查"""
        logger.info("=" * 60)
        logger.info("开始SEO检查")
        logger.info(f"站点: https://aimarketing.site")
        logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)

        # 基础文件
        self.check_sitemap()
        self.check_robots_txt()

        # Meta标签
        self.check_meta_tags()

        # 结构化数据
        self.check_schema_json()
        self.check_article_schema()

        # 性能优化
        self.check_performance()
        self.check_cache_headers()
        self.check_dns_prefetch()

        # 社交元数据
        self.check_social_meta()

    def print_report(self):
        """打印报告"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("SEO检查报告")
        logger.info("=" * 60)
        logger.info(f"总检查项: {self.passed + self.failed + self.skipped}")
        logger.info(f"  ✅ 通过: {self.passed}")
        logger.info(f"  ❌ 失败: {self.failed}")
        logger.info(f"  ⚠️ 警告: {len(self.warnings)}")
        logger.info(f"  ⏭️ 跳过: {self.skipped}")
        logger.info("")

        if self.results:
            logger.info("--- 详细结果 ---")
            for status, name, message in self.results:
                if message:
                    logger.info(f"  {status} {name}: {message}")
                else:
                    logger.info(f"  {status} {name}")

        if self.errors:
            logger.info("")
            logger.info("--- 需要修复 ---")
            for err in self.errors:
                logger.info(f"  ❌ {err}")

        score = self.passed / max(1, self.passed + self.failed) * 100
        logger.info("")
        logger.info(f"SEO评分: {score:.0f}%")

        if score >= 90:
            logger.info("🌟 优秀 - SEO配置完善")
        elif score >= 75:
            logger.info("👍 良好 - 少量优化空间")
        elif score >= 60:
            logger.info("⚡ 合格 - 建议继续优化")
        else:
            logger.info("🔧 需要改进 - 建议完善SEO配置")

        return score

    def generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        lines = [
            f"# SEO检查报告",
            f"",
            f"**站点**: https://aimarketing.site",
            f"**检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## 检查结果汇总",
            f"",
            f"| 指标 | 数量 |",
            f"|------|------|",
            f"| ✅ 通过 | {self.passed} |",
            f"| ❌ 失败 | {self.failed} |",
            f"| ⚠️ 警告 | {len(self.warnings)} |",
            f"| ⏭️ 跳过 | {self.skipped} |",
            f"| **总检查项** | {self.passed + self.failed + self.skipped} |",
            f"",
            f"**SEO评分: {self.passed / max(1, self.passed + self.failed) * 100:.0f}%**",
            f"",
            f"## 详细结果",
            f"",
            f"| 状态 | 检查项 | 说明 |",
            f"|------|--------|------|",
        ]

        for status, name, message in self.results:
            lines.append(f"| {status} | {name} | {message} |")

        if self.errors:
            lines.extend([
                "",
                "## 需要修复的项目",
                "",
            ])
            for err in self.errors:
                lines.append(f"- ❌ {err}")

        return '\n'.join(lines)


def main():
    """主函数"""
    checker = SEOChecker()
    checker.run_all_checks()
    score = checker.print_report()

    # 生成报告文件
    report_path = BASE_DIR / 'reports' / 'seo-check-report.md'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(checker.generate_markdown_report(), encoding='utf-8')
    logger.info(f"\n报告已生成: {report_path}")

    return score >= 75


if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
