# AI营销集成服务网站

> **北上广研发＋广西集成＋东盟应用** — AI驱动的智能营销解决方案

[![Auto Publish](https://github.com/ai-marketing/ai-marketing-site/actions/workflows/auto-publish.yml/badge.svg)](https://github.com/ai-marketing/ai-marketing-site/actions/workflows/auto-publish.yml)

## 📋 项目简介

这是一个基于 Hugo + PaperMod 主题构建的AI营销资讯网站，具备全流程自动化能力：

- 🔥 **热点采集** — 自动从微博、百度、知乎、36氪等采集AI相关热点
- 🤖 **AI内容生成** — 使用 Claude API 将热点转化为深度分析文章
- 🚀 **自动发布** — Git提交触发自动构建部署
- 🔍 **SEO优化** — 自动提交链接到百度、Google等搜索引擎

## 🏗️ 技术栈

| 组件 | 技术 |
|------|------|
| 静态网站生成 | Hugo v0.120+ |
| 主题 | PaperMod |
| 托管 | GitHub Pages |
| CI/CD | GitHub Actions |
| AI服务 | Claude API (Anthropic) |
| 编程语言 | Python 3.10+ |

## 📁 目录结构

```
ai-marketing-site/
├── config.yaml              # Hugo主配置
├── content/
│   ├── posts/               # 自动生成的文章
│   └── manual/              # 手动撰写的文章
├── themes/PaperMod/         # 主题（git submodule）
├── static/                  # 静态资源
├── scripts/                 # 自动化脚本
│   ├── collect_hotspots.py  # 热点采集
│   ├── generate_article.py  # AI内容生成
│   ├── publish.py           # Git发布
│   ├── submit_to_baidu.py   # 百度SEO提交
│   ├── submit_to_google.py  # Google SEO提交
│   ├── submit_to_bing.py    # Bing SEO提交
│   ├── submit_all.py        # 统一SEO提交
│   ├── seo_check.py         # SEO验证（Python）
│   ├── seo_check.sh         # SEO验证（Bash）
│   └── main.py             # 主流程控制
├── layouts/                 # Hugo布局覆盖（SEO增强）
│   ├── robots.txt           # 自定义robots规则
│   ├── _default/sitemap.xml # 自定义sitemap模板
│   ├── _partials/extend_head.html       # SEO meta增强
│   ├── _partials/templates/schema_json.html  # Schema.org
│   └── _markup/render-image.html        # 图片懒加载
├── templates/               # 内容模板
├── data/                    # 数据文件
├── reports/                 # SEO报告
├── .github/workflows/       # GitHub Actions
└── docs/                    # 文档
```

## 🚀 快速开始

### 本地开发

```bash
# 1. 克隆仓库
git clone --recurse-submodules https://github.com/ai-marketing/ai-marketing-site.git
cd ai-marketing-site

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 本地运行Hugo
hugo server -D

# 4. 访问 http://localhost:1313
```

### 手动发布文章

```bash
# 在 content/manual/ 或 content/posts/ 创建Markdown文件
hugo new posts/my-article.md

# 本地预览
hugo server -D

# 提交发布
git add content/
git commit -m "feat: 新增文章 - 文章标题"
git push origin main
```

### 运行自动化流程

```bash
# 完整流程：采集 -> 生成 -> 构建 -> 发布 -> SEO
python scripts/main.py

# 单独运行各步骤
python scripts/collect_hotspots.py
python scripts/generate_article.py
python scripts/publish.py
python scripts/submit_to_baidu.py
python scripts/submit_to_google.py
```

## ⚙️ 配置说明

### 环境变量（GitHub Secrets）

| 变量名 | 说明 | 获取方式 |
|--------|------|---------|
| `ANTHROPIC_API_KEY` | Claude API密钥 | [console.anthropic.com](https://console.anthropic.com/) |
| `BAIDU_TOKEN` | 百度站长平台推送token | [ziyuan.baidu.com](https://ziyuan.baidu.com/) |
| `GOOGLE_CREDENTIALS` | Google服务账号JSON (base64) | [Google Cloud Console](https://console.cloud.google.com/) |

### 站点配置

编辑 `config.yaml`：
- `baseURL`: 修改为你的域名
- `title`: 网站标题
- `params.description`: 网站描述

## 📖 文档

| 文档 | 说明 |
|------|------|
| [部署指南](docs/DEPLOYMENT.md) | 从零开始部署（环境配置、域名、GitHub Pages） |
| [自动化说明](docs/AUTOMATION.md) | 自动化工作流详解（采集→生成→发布→SEO） |
| [使用手册](USAGE.md) | 日常运维操作手册（手动发文、审核、排障） |
| [DNS配置](DNS_SETUP.md) | 域名DNS解析配置指南 |
| [脚本说明](scripts/README.md) | Python自动化脚本API文档 |

## 📊 自动化工作流

### 定时任务

| 时间 (北京) | 任务 | 说明 |
|-------------|------|------|
| 09:00 | 自动采集+生成 | 工作日第一篇 |
| 14:00 | 自动采集+生成 | 工作日第二篇 |
| 19:00 | 自动采集+生成 | 工作日第三篇 |
| 00:00 | 每日报告 | 运营数据统计 |

### 发布策略

- 工作日：每天最多3篇自动化文章
- 周末：每天最多1篇
- 支持手动发布额外文章

## 💰 成本估算

| 项目 | 月成本 |
|------|--------|
| Claude API | ¥50-100 |
| GitHub Pages | 免费 |
| 域名 | ¥50-100/年 |
| **总计** | **约¥100-150/月** |

## 🌍 多语言支持 / Multi-Language Support

本项目支持多种语言，服务东盟地区：

- [中文](README.md) - Chinese
- [English](README.en.md) - English
- [ภาษาไทย](README.th.md) - Thai
- [Tiếng Việt](README.vi.md) - Vietnamese
- [Bahasa Indonesia](README.id.md) - Indonesian
- [Bahasa Melayu](README.ms.md) - Malay
- [Filipino](README.ph.md) - Filipino

## 📄 License

MIT License
