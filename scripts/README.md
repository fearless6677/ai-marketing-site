# AI营销自动化系统 - 使用说明

## 📁 脚本清单

```
scripts/
├── collect_hotspots.py    # 热点数据采集（微博/百度/知乎/36氪）
├── generate_article.py    # AI内容生成（Claude / DeepSeek）
├── publish.py             # Git自动发布
├── main.py                # 主流程编排（采集→生成→构建→发布→SEO→通知）
├── submit_to_baidu.py     # 百度链接主动推送
├── submit_to_google.py    # Google Indexing API 提交
├── notify.py              # 企业微信机器人通知
└── daily_report.py        # 每日运营报告生成
```

```
.github/workflows/
├── auto-publish.yml       # 自动发布工作流（每日08:00 北京时间）
└── daily-report.yml       # 每日报告工作流（每日00:00 北京时间）
```

---

## 🔧 环境变量配置

### GitHub Secrets 设置

在 GitHub 仓库的 `Settings → Secrets and variables → Actions` 中配置：

| Secret 名称 | 必需 | 说明 |
|-------------|------|------|
| `ANTHROPIC_API_KEY` | ✅ (默认) | Claude API 密钥 |
| `AI_PROVIDER` | ❌ | AI提供商，默认 `claude`，可设为 `deepseek` |
| `DEEPSEEK_API_KEY` | 条件 | 使用DeepSeek时必填 |
| `BAIDU_TOKEN` | 可选 | 百度站长平台推送Token |
| `GOOGLE_CREDENTIALS` | 可选 | Google服务账号JSON（base64编码）|
| `WECOM_WEBHOOK_URL` | 可选 | 企业微信机器人Webhook |

### 本地运行环境变量

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-..."
$env:BAIDU_TOKEN="your_baidu_token"
$env:WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..."

# Linux / macOS
export ANTHROPIC_API_KEY="sk-ant-..."
export BAIDU_TOKEN="your_baidu_token"
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..."
```

---

## 🚀 本地运行

### 前置条件

```bash
# 安装依赖
cd F:\marketing\ai-marketing-site
pip install -r requirements.txt

# 确保安装 Hugo（构建用）
# Windows: winget install Hugo.Hugo.Extended
# 或下载: https://github.com/gohugoio/hugo/releases
```

### 完整流程运行

```bash
# 一键执行完整流程：采集 → 生成 → 构建 → 发布 → SEO → 通知
python scripts/main.py
```

### 分步运行

```bash
# Step 1: 热点采集
python scripts/collect_hotspots.py

# Step 2: AI内容生成
python scripts/generate_article.py

# Step 3: 手动发布（git操作）
python scripts/publish.py

# Step 4: 百度提交
python scripts/submit_to_baidu.py

# Step 5: Google提交
python scripts/submit_to_google.py

# Step 6: 生成日报
python scripts/daily_report.py
```

### 切换AI提供商

```bash
# 使用 Claude（默认）
$env:AI_PROVIDER="claude"
$env:ANTHROPIC_API_KEY="sk-ant-..."
python scripts/generate_article.py

# 使用 DeepSeek（更便宜）
$env:AI_PROVIDER="deepseek"
$env:DEEPSEEK_API_KEY="sk-..."
python scripts/generate_article.py
```

---

## 📬 通知系统

### 企业微信机器人配置

1. 在企业微信群聊中，点击右上角 `...` → `群机器人` → `添加机器人`
2. 复制 Webhook URL，格式如：
   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```
3. 将此URL添加到 GitHub Secrets 的 `WECOM_WEBHOOK_URL`

### 手动发送测试通知

```bash
$env:WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..."
python scripts/notify.py --test
```

### 通知类型

```bash
# 发送成功通知
python scripts/notify.py --type success --results '{"采集": true, "发布": true}'

# 发送失败告警
python scripts/notify.py --type failure --results '{"采集": false}' --message "错误详情"

# 发送每日汇总
python scripts/notify.py --type daily --results '{"hotspots": 15, "articles": 3}'
```

---

## 🔍 搜索引擎提交

### 百度推送

1. 登录 [百度站长平台](https://ziyuan.baidu.com/)
2. 添加站点并验证
3. 进入「链接提交」→「主动推送」，获取推送接口和Token
4. 将Token配置到 `BAIDU_TOKEN` Secret

### Google Indexing API

1. 在 [Google Cloud Console](https://console.cloud.google.com/) 创建项目
2. 启用 "Indexing API"
3. 创建服务账号，下载JSON密钥
4. 在 [Search Console](https://search.google.com/search-console/) 添加服务账号为「所有者」
5. 将JSON文件base64编码后配置到 `GOOGLE_CREDENTIALS` Secret：
   ```bash
   # 本地编码
   base64 google_credentials.json | tr -d '\n' > creds_b64.txt
   ```

---

## ⏰ 定时任务

### GitHub Actions 调度

| 工作流 | Cron表达式 | 北京时间 | 功能 |
|--------|-----------|---------|------|
| `auto-publish.yml` | `0 0 * * *` | 每日 08:00 | 采集+生成+发布+SEO+通知 |
| `daily-report.yml` | `0 16 * * *` | 每日 00:00 | 运营日报+通知 |

### 手动触发

在 GitHub 仓库 → `Actions` → 选择工作流 → `Run workflow`

`auto-publish.yml` 支持参数：
- `skip_generate`: 跳过AI生成（仅构建发布已有内容）

### Windows 计划任务（本地定时）

```powershell
# 使用 schtasks 创建每日 08:00 执行的任务
schtasks /create /tn "AI-Marketing-AutoPublish" `
  /tr "python F:\marketing\ai-marketing-site\scripts\main.py" `
  /sc daily /st 08:00 `
  /rl highest
```

---

## 📊 目录结构

```
ai-marketing-site/
├── scripts/                  # 自动化脚本
├── content/posts/            # 文章（Hugo content）
├── data/
│   ├── hotspots/             # 每日热点数据（JSON）
│   ├── articles_history.json # 已发布文章历史（去重用）
│   └── seo_config.yaml       # SEO配置
├── templates/
│   ├── article_template.md   # 文章模板
│   └── prompts/              # AI提示词模板
├── reports/                  # 每日运营报告
├── logs/                     # 运行日志
├── public/                   # Hugo构建输出
├── .github/workflows/        # CI/CD 工作流
├── config.yaml               # Hugo站点配置
└── requirements.txt          # Python依赖
```

---

## 🛠 故障排查

### 热点采集失败

- **微博/知乎403**：这些网站有反爬限制，在GitHub Actions中可能受限。可改用API或代理。
- **百度解析失败**：页面结构变更时需更新 `collect_hotspots.py` 中的CSS选择器。

### AI生成失败

- **API配额**：检查 `ANTHROPIC_API_KEY` 或 `DEEPSEEK_API_KEY` 余额
- **质量检查未通过**：文章字数不足1000字或超过3000字会重试（最多3次）
- **网络超时**：设置环境变量 `HTTP_TIMEOUT=60`

### Hugo构建失败

```bash
# 本地测试
hugo --minify --verbose

# 常见错误：
# - front-matter格式错误
# - Markdown语法问题
# - 模板引用错误
```

### Git推送失败

```bash
# 检查Git配置
git config user.name
git config user.email
git remote -v

# 在GitHub Actions中自动使用 GITHUB_TOKEN，无需手动配置
```

---

## 💰 成本估算

| 服务 | 费用 | 频率 | 月成本 |
|------|------|------|--------|
| Claude Sonnet | ~¥0.5-2/篇 | 3篇/天 | ~¥135 |
| DeepSeek | ~¥0.05/篇 | 3篇/天 | ~¥5 |
| GitHub Actions | 免费额度 | - | ¥0 |
| GitHub Pages | 免费 | - | ¥0 |

**推荐**：日常使用 DeepSeek，重要文章手动用 Claude。

---

## 📝 自定义

### 添加数据源

在 `collect_hotspots.py` 中新增采集函数：

```python
def collect_custom_source() -> list:
    items = []
    # 你的采集逻辑
    return items

# 添加到 collectors 列表
collectors = [
    ('微博热搜', collect_weibo),
    ('百度热搜', collect_baidu),
    ('知乎热榜', collect_zhihu),
    ('36氪', collect_36kr),
    ('自定义源', collect_custom_source),  # ← 添加
]
```

### 修改关键词过滤

在 `collect_hotspots.py` 中修改：

```python
KEYWORDS = ['AI', '人工智能', '营销', '广西', '东盟', ...]  # 添加你的关键词
```

### 自定义AI提示词

编辑 `scripts/generate_article.py` 中的 `SYSTEM_PROMPT` 和 `HOTSPOT_USER_PROMPT`。
