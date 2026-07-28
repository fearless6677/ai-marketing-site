# 使用指南

> AI营销集成服务网站 — 日常操作手册

---

## 📑 目录

1. [日常运维](#日常运维)
2. [手动发布文章](#手动发布文章)
3. [自动化流程操作](#自动化流程操作)
4. [SEO管理](#seo管理)
5. [内容审核](#内容审核)
6. [监控与排障](#监控与排障)
7. [配置修改](#配置修改)

---

## 🔄 日常运维

### 每日工作（约1小时）

| 时间 | 操作 | 说明 |
|------|------|------|
| 09:00 | 检查自动发布 | 查看是否成功生成文章 |
| 10:00 | 审核内容 | 阅读自动生成的文章，必要时修改 |
| 14:00 | 检查第二次发布 | 下午文章是否生成 |
| 19:00 | 检查第三次发布 | 晚间文章是否生成 |
| 随时 | 处理通知 | 查看企业微信推送的运营日报 |

### 每周工作

- 检查SEO收录情况（百度/Google）
- 查看运营数据趋势
- 清理过期热点数据
- 更新内容模板（如需要）

---

## ✍️ 手动发布文章

### 方式一：直接创建Markdown文件

```bash
# 1. 进入项目目录
cd ai-marketing-site

# 2. 创建新文章
cat > content/posts/$(date +%Y-%m-%d)-my-article-title.md << 'EOF'
---
title: "我的文章标题"
date: 2026-07-28T10:00:00+08:00
draft: false
categories: ["AI技术"]
tags: ["AI营销", "实战案例"]
summary: "文章摘要，将显示在首页列表中"
---

## 引言

正文内容...

## 核心观点

详细内容...

## 总结

结论...
EOF

# 3. 本地预览
F:/marketing/hugo-v0147/hugo.exe server -D

# 4. 确认无误后提交
git add content/posts/
git commit -m "feat: 新增文章 - 我的文章标题"
git push origin main
```

### 方式二：使用Hugo命令

```bash
# 创建新文章骨架
F:/marketing/hugo-v0147/hugo.exe new posts/my-new-post.md

# 编辑生成的文件
# content/posts/my-new-post.md 会自动填充front-matter

# 本地预览
F:/marketing/hugo-v0147/hugo.exe server -D

# 提交发布
git add content/
git commit -m "feat: 新增文章 - 标题"
git push origin main
```

### 文章Front-matter模板

```yaml
---
title: "文章标题"                    # 必填
date: 2026-07-28T10:00:00+08:00     # 必填，ISO格式
draft: false                         # false=发布，true=草稿
categories: ["AI技术"]               # 分类
tags: ["AI营销", "案例"]             # 标签
summary: "文章摘要"                  # 首页显示
description: "SEO描述"              # 搜索引擎用
keywords: ["关键词1", "关键词2"]     # SEO关键词
author: "作者名"                     # 作者
toc: true                            # 是否显示目录
cover:                               # 封面图
  image: "/images/cover.jpg"
  alt: "封面描述"
---
```

---

## 🤖 自动化流程操作

### 完整流程（手动触发）

```bash
# 一键运行：采集 → 生成 → 构建 → 发布 → SEO提交
python scripts/main.py
```

### 分步执行

```bash
# 步骤1：热点采集（从微博/百度/知乎/36氪抓取AI相关热点）
python scripts/collect_hotspots.py
# 输出：data/hotspots/YYYY-MM-DD.json

# 步骤2：AI内容生成（调用Claude API生成文章）
python scripts/generate_article.py
# 输出：content/posts/YYYY-MM-DD-slug.md

# 步骤3：Hugo构建（生成静态网站）
F:/marketing/hugo-v0147/hugo.exe --minify
# 输出：public/ 目录

# 步骤4：Git发布（提交并推送到GitHub）
python scripts/publish.py
# 触发GitHub Actions自动部署

# 步骤5：SEO提交（推送链接到搜索引擎）
python scripts/submit_all.py
```

### GitHub Actions手动触发

1. 访问仓库 Actions 页面
2. 选择要运行的工作流
3. 点击 "Run workflow" 按钮
4. 可选择参数（如跳过文章生成）

### 环境变量配置

自动化脚本需要以下环境变量：

```bash
# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."       # 可选，备选AI
export BAIDU_TOKEN="your-baidu-token"
export GOOGLE_CREDENTIALS='{"type":"service_account",...}'
export BING_API_KEY="your-bing-key"
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..."

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:BAIDU_TOKEN = "your-baidu-token"
# ...
```

---

## 🔍 SEO管理

### 检查SEO状态

```bash
# 运行SEO检查脚本
python scripts/seo_check.py

# 或Bash版本
bash scripts/seo_check.sh
```

### 手动提交搜索引擎

```bash
# 提交到百度
python scripts/submit_to_baidu.py

# 提交到Google
python scripts/submit_to_google.py

# 提交到Bing
python scripts/submit_to_bing.py

# 全部提交
python scripts/submit_all.py
```

### 检查收录情况

**百度**：
```
site:aimarketing.site
```
在百度搜索框输入以上命令，查看收录页面数。

**Google**：
```
site:aimarketing.site
```
在Google搜索框输入，或使用 Google Search Console 查看。

### Sitemap验证

```bash
# 本地检查
cat public/sitemap.xml | head -20

# 在线验证
# 访问 https://aimarketing.site/sitemap.xml
# 使用 Google Rich Results Test 验证结构化数据
```

---

## ✅ 内容审核

### 审核清单

- [ ] 标题准确，无敏感词
- [ ] 内容事实正确
- [ ] 无版权风险（图片/引用）
- [ ] 链接可正常访问
- [ ] 分类/标签正确
- [ ] SEO描述合理
- [ ] 无AI生成痕迹（如"作为AI助手"）

### 修改已发布文章

```bash
# 1. 编辑文章
vim content/posts/2026-07-28-article-name.md

# 2. 本地预览
F:/marketing/hugo-v0147/hugo.exe server -D

# 3. 提交修改
git add content/
git commit -m "fix: 修正文章错误内容"
git push origin main
```

---

## 🔧 监控与排障

### 常见问题及解决

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 文章没有自动生成 | API Key无效或过期 | 检查Secrets配置 |
| 网站样式异常 | 主题submodule未拉取 | `git submodule update --init` |
| SEO提交失败 | Token过期 | 重新获取百度/Google token |
| 构建超时 | 内容过多 | 检查Hugo构建日志 |
| 图片不显示 | 路径错误 | 使用绝对路径 `/images/xxx.jpg` |
| 通知未发送 | Webhook URL错误 | 检查企业微信Webhook |

### 查看日志

```bash
# 查看自动化运行日志
cat logs/main.log
cat logs/collect.log
cat logs/generate.log
cat logs/publish.log
cat logs/seo.log

# 查看GitHub Actions日志
# 访问仓库 → Actions → 选择运行记录 → 查看各步骤输出
```

### 紧急回滚

```bash
# 如果发布的文章有问题，需要紧急撤回
git log --oneline -5                    # 找到上次正常的提交
git revert HEAD                         # 撤销最近一次提交
git push origin main                    # 推送撤销
```

---

## ⚙️ 配置修改

### 修改站点基本信息

编辑 `config.yaml`：

```yaml
baseURL: "https://aimarketing.site/"   # 域名
title: "AI营销集成服务"                 # 网站标题
params:
  description: "网站描述"              # SEO描述
  keywords: [...]                      # SEO关键词
  author: "作者名"                     # 默认作者
```

### 修改自动化参数

编辑 `scripts/main.py` 中的配置常量：

```python
MAX_ARTICLES_PER_DAY = 3        # 每日最大文章数
MIN_ARTICLE_LENGTH = 1000       # 最短文章字数
MAX_ARTICLE_LENGTH = 3000       # 最长文章字数
HOTSPIC_KEYWORDS = ["AI", ...]  # 热点筛选关键词
```

### 修改主题样式

编辑 `assets/css/extended/custom.css`：

```css
/* 修改主色调 */
:root {
  --primary-color: #1976D2;      /* 科技蓝 */
  --secondary-color: #42A5F5;    /* 浅蓝 */
}

/* 修改字体 */
body {
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}
```

### 修改菜单

编辑 `config.yaml` 中的 `menu` 部分：

```yaml
menu:
  main:
    - name: 首页
      url: /
      weight: 1
    - name: 新菜单项
      url: /new-page/
      weight: 7
```

---

## 📱 移动端测试

```bash
# 本地启动服务
F:/marketing/hugo-v0147/hugo.exe server -D

# 在手机上访问（需同一局域网）
# 查看本地IP：ipconfig (Windows) / ifconfig (Mac/Linux)
# 手机浏览器访问 http://你的IP:1313
```

或使用Chrome DevTools的移动端模拟功能。

---

## 📊 运营数据查看

### 本地报告

```bash
# 生成每日报告
python scripts/daily_report.py

# 查看报告
cat reports/daily/YYYY-MM-DD.json
```

### GitHub Analytics

- Actions 运行记录 → 查看每次构建状态
- Insights → 查看仓库活跃度

### 第三方统计

建议接入以下统计服务：
- 百度统计（国内流量）
- Google Analytics（海外流量）
- 51.la（轻量统计）

---

*最后更新：2026-07-28*
