#!/bin/bash
# SEO检查脚本（Bash版本）
# 检查已构建的Hugo站点的SEO配置

PUBLIC_DIR="F:/marketing/ai-marketing-site/public"
LAYOUTS_DIR="F:/marketing/ai-marketing-site/layouts"
CONFIG_FILE="F:/marketing/ai-marketing-site/config.yaml"

PASSED=0
FAILED=0
WARNINGS=0

check() {
    local name="$1"
    local result="$2"  # "pass" or "fail"
    local msg="$3"
    local is_warn="${4:-false}"

    if [ "$result" = "pass" ]; then
        echo "✅ PASS: $name ${msg:+- $msg}"
        PASSED=$((PASSED + 1))
    elif [ "$is_warn" = "true" ]; then
        echo "⚠️ WARN: $name ${msg:+- $msg}"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "❌ FAIL: $name ${msg:+- $msg}"
        FAILED=$((FAILED + 1))
    fi
}

echo "============================================================"
echo "SEO检查报告"
echo "站点: https://aimarketing.site"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

# 1. 检查配置文件
echo "--- 配置文件检查 ---"

# config.yaml
if [ -f "$CONFIG_FILE" ]; then
    check "config.yaml 存在" "pass"

    # 基础字段
    grep -q "baseURL:" "$CONFIG_FILE" && \
        check "baseURL 配置" "pass" || \
        check "baseURL 配置" "fail" "缺少baseURL"

    grep -q "description:" "$CONFIG_FILE" && \
        check "站点描述" "pass" || \
        check "站点描述" "fail" "缺少description"

    grep -q "keywords:" "$CONFIG_FILE" && \
        check "站点关键词" "pass" || \
        check "站点关键词" "warn" "缺少keywords" "true"

    # 分析标签
    grep -q "EnableRobotsTXT:" "$CONFIG_FILE" && \
        check "EnableRobotsTXT" "pass" || \
        check "EnableRobotsTXT" "fail" "未启用robots.txt"

    grep -q "minifyOutput:" "$CONFIG_FILE" && \
        check "HTML压缩" "pass" || \
        check "HTML压缩" "fail" "未启用minifyOutput" "true"

    grep -q "sitemap:" "$CONFIG_FILE" && \
        check "Sitemap配置" "pass" || \
        check "Sitemap配置" "fail" "缺少sitemap配置"

    grep -q "schema:" "$CONFIG_FILE" && \
        check "Schema.org配置" "pass" || \
        check "Schema.org配置" "fail" "缺少schema配置" "true"

    grep -q "sameAs:" "$CONFIG_FILE" && \
        check "sameAs社交链接" "pass" || \
        check "sameAs社交链接" "fail" "缺少sameAs" "true"

    grep -q "server:" "$CONFIG_FILE" && \
        check "服务器缓存头" "pass" || \
        check "服务器缓存头" "fail" "缺少server缓存配置" "true"

    grep -q "analytics:" "$CONFIG_FILE" && \
        check "搜索引擎验证配置" "pass" || \
        check "搜索引擎验证配置" "fail" "缺少analytics验证" "true"

else
    check "config.yaml 存在" "fail" "文件不存在"
fi

echo ""

# 2. 检查 Layouts 覆盖
echo "--- Layouts 覆盖检查 ---"

[ -f "$LAYOUTS_DIR/robots.txt" ] && \
    check "自定义robots.txt" "pass" || \
    check "自定义robots.txt" "fail" "缺少自定义robots.txt"

[ -f "$LAYOUTS_DIR/_default/sitemap.xml" ] && \
    check "自定义sitemap模板" "pass" || \
    check "自定义sitemap模板" "fail" "缺少sitemap.xml模板"

[ -f "$LAYOUTS_DIR/_partials/extend_head.html" ] && \
    check "SEO头部增强" "pass" || \
    [ -f "$LAYOUTS_DIR/partials/extend_head.html" ] && \
    check "SEO头部增强" "pass" "(legacy路径)" || \
    check "SEO头部增强" "fail" "缺少extend_head.html"

[ -f "$LAYOUTS_DIR/_partials/templates/schema_json.html" ] && \
    check "Schema.org模板覆盖" "pass" || \
    [ -f "$LAYOUTS_DIR/partials/templates/schema_json.html" ] && \
    check "Schema.org模板覆盖" "pass" "(legacy路径)" || \
    check "Schema.org模板覆盖" "fail" "缺少schema_json.html覆盖"

[ -f "$LAYOUTS_DIR/_markup/render-image.html" ] && \
    check "图片懒加载Hook" "pass" || \
    check "图片懒加载Hook" "fail" "缺少render-image.html" "true"

echo ""

# 3. 检查已构建输出
echo "--- 构建输出检查 ---"

if [ -f "$PUBLIC_DIR/index.html" ]; then
    check "index.html 存在" "pass"

    # Meta标签
    grep -q "<title>" "$PUBLIC_DIR/index.html" && \
        check "Title标签" "pass" || \
        check "Title标签" "fail" "缺少title"

    grep -q "name=\"description\"" "$PUBLIC_DIR/index.html" && \
        check "Meta description" "pass" || \
        grep -q "name=description" "$PUBLIC_DIR/index.html" && \
        check "Meta description" "pass" || \
        check "Meta description" "fail" "缺少description"

    grep -q "name=\"keywords\"" "$PUBLIC_DIR/index.html" && \
        check "Meta keywords" "pass" || \
        grep -q "name=keywords" "$PUBLIC_DIR/index.html" && \
        check "Meta keywords" "pass" || \
        check "Meta keywords" "fail" "缺少keywords" "true"

    grep -q "rel=\"canonical\"" "$PUBLIC_DIR/index.html" && \
        check "Canonical URL" "pass" || \
        grep -q "rel=canonical" "$PUBLIC_DIR/index.html" && \
        check "Canonical URL" "pass" || \
        check "Canonical URL" "fail" "缺少canonical"

    # Open Graph
    grep -q "og:title" "$PUBLIC_DIR/index.html" && \
        check "Open Graph标签" "pass" || \
        check "Open Graph标签" "fail" "缺少OG标签"

    grep -q "og:description" "$PUBLIC_DIR/index.html" && \
        check "OG Description" "pass" || \
        check "OG Description" "fail" "缺少OG description" "true"

    # Twitter Card
    grep -q "twitter:card" "$PUBLIC_DIR/index.html" && \
        check "Twitter Card标签" "pass" || \
        check "Twitter Card标签" "fail" "缺少Twitter Card"

    # Schema.org
    grep -q "application/ld+json" "$PUBLIC_DIR/index.html" && \
        check "JSON-LD Schema" "pass" || \
        check "JSON-LD Schema" "fail" "缺少JSON-LD"

    grep -q "Organization" "$PUBLIC_DIR/index.html" && \
        check "Organization Schema" "pass" || \
        check "Organization Schema" "fail" "缺少Organization schema"

    # DNS Prefetch
    grep -q "dns-prefetch" "$PUBLIC_DIR/index.html" && \
        check "DNS Prefetch" "pass" || \
        check "DNS Prefetch" "fail" "缺少dns-prefetch" "true"

    # Robots meta
    grep -q "robots" "$PUBLIC_DIR/index.html" && \
        check "Robots meta标签" "pass" || \
        check "Robots meta标签" "fail" "缺少robots meta" "true"

else
    check "index.html 存在" "fail" "站点未构建"
fi

# 检查 sitemap.xml
if [ -f "$PUBLIC_DIR/sitemap.xml" ]; then
    check "sitemap.xml 存在" "pass"

    URL_COUNT=$(grep -o "<loc>" "$PUBLIC_DIR/sitemap.xml" 2>/dev/null | wc -l || echo "0")
    check "Sitemap包含URL" "pass" "共 $URL_COUNT 个URL"

    grep -q "<priority>" "$PUBLIC_DIR/sitemap.xml" && \
        check "Sitemap priority" "pass" || \
        check "Sitemap priority" "fail" "缺少priority" "true"

    grep -q "<changefreq>" "$PUBLIC_DIR/sitemap.xml" && \
        check "Sitemap changefreq" "pass" || \
        check "Sitemap changefreq" "fail" "缺少changefreq" "true"
else
    check "sitemap.xml 存在" "fail" "Hugo未生成sitemap"
fi

# 检查 robots.txt
if [ -f "$PUBLIC_DIR/robots.txt" ]; then
    check "robots.txt 存在" "pass"

    grep -q "User-agent" "$PUBLIC_DIR/robots.txt" && \
        check "robots User-agent" "pass" || \
        check "robots User-agent" "fail" "缺少User-agent"

    grep -q "Sitemap:" "$PUBLIC_DIR/robots.txt" && \
        check "robots Sitemap声明" "pass" || \
        check "robots Sitemap声明" "fail" "缺少Sitemap声明" "true"

    grep -q "Baiduspider" "$PUBLIC_DIR/robots.txt" && \
        check "百度蜘蛛规则" "pass" || \
        check "百度蜘蛛规则" "fail" "缺少Baiduspider规则" "true"
else
    check "robots.txt 存在" "fail" "Hugo未生成robots.txt"
fi

echo ""

# 4. 检查提交脚本
echo "--- 提交脚本检查 ---"

SCRIPTS_DIR="F:/marketing/ai-marketing-site/scripts"

[ -f "$SCRIPTS_DIR/submit_to_baidu.py" ] && \
    check "百度提交脚本" "pass" || \
    check "百度提交脚本" "fail" "缺少submit_to_baidu.py"

[ -f "$SCRIPTS_DIR/submit_to_google.py" ] && \
    check "Google提交脚本" "pass" || \
    check "Google提交脚本" "fail" "缺少submit_to_google.py"

[ -f "$SCRIPTS_DIR/submit_to_bing.py" ] && \
    check "Bing提交脚本" "pass" || \
    check "Bing提交脚本" "fail" "缺少submit_to_bing.py"

[ -f "$SCRIPTS_DIR/submit_all.py" ] && \
    check "统一提交脚本" "pass" || \
    check "统一提交脚本" "fail" "缺少submit_all.py"

[ -f "$SCRIPTS_DIR/seo_check.py" ] && \
    check "SEO检查脚本" "pass" || \
    check "SEO检查脚本" "fail" "缺少seo_check.py"

echo ""
echo "============================================================"
echo "检查结果汇总"
echo "============================================================"
TOTAL=$((PASSED + FAILED))
echo "总检查项: $TOTAL"
echo "✅ 通过: $PASSED"
echo "❌ 失败: $FAILED"
echo "⚠️ 警告: $WARNINGS"

if [ $TOTAL -gt 0 ]; then
    SCORE=$((PASSED * 100 / TOTAL))
    echo ""
    echo "SEO评分: ${SCORE}%"

    if [ $SCORE -ge 90 ]; then
        echo "🌟 优秀 - SEO配置完善"
    elif [ $SCORE -ge 75 ]; then
        echo "👍 良好 - 少量优化空间"
    elif [ $SCORE -ge 60 ]; then
        echo "⚡ 合格 - 建议继续优化"
    else
        echo "🔧 需要改进 - 建议完善SEO配置"
    fi
fi

exit 0
