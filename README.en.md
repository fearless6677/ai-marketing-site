# AI Marketing Integration Service

> **R&D in First-Tier Cities + Integration in Guangxi + Application in ASEAN** — AI-Powered Intelligent Marketing Solutions

[![Auto Publish](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml/badge.svg)](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml)

## 📋 Overview

This is an AI marketing news website built with Hugo + PaperMod theme, featuring full-process automation capabilities:

- 🔥 **Hot Topic Collection** — Automatically collects AI-related hot topics from Weibo, Baidu, Zhihu, 36Kr, etc.
- 🤖 **AI Content Generation** — Uses Claude API to transform hot topics into in-depth analysis articles
- 🚀 **Auto Publishing** — Git commits trigger automatic build and deployment
- 🔍 **SEO Optimization** — Automatically submits links to search engines like Baidu and Google

## 🏗️ Tech Stack

| Component | Technology |
|-----------|------------|
| Static Site Generator | Hugo v0.120+ |
| Theme | PaperMod |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
| AI Service | Claude API (Anthropic) |
| Programming Language | Python 3.10+ |

## 📁 Directory Structure

```
ai-marketing-site/
├── config.yaml              # Hugo main configuration
├── content/
│   ├── posts/               # Auto-generated articles
│   └── manual/              # Manually written articles
├── themes/PaperMod/         # Theme (git submodule)
├── static/                  # Static resources
├── scripts/                 # Automation scripts
│   ├── collect_hotspots.py  # Hot topic collection
│   ├── generate_article.py  # AI content generation
│   ├── publish.py           # Git publishing
│   ├── submit_to_baidu.py   # Baidu SEO submission
│   ├── submit_to_google.py  # Google SEO submission
│   ├── submit_to_bing.py    # Bing SEO submission
│   ├── submit_all.py        # Unified SEO submission
│   ├── seo_check.py         # SEO verification (Python)
│   ├── seo_check.sh         # SEO verification (Bash)
│   └── main.py             # Main workflow control
├── layouts/                 # Hugo layout overrides (SEO enhanced)
│   ├── robots.txt           # Custom robots rules
│   ├── _default/sitemap.xml # Custom sitemap template
│   ├── _partials/extend_head.html       # SEO meta enhancement
│   ├── _partials/templates/schema_json.html  # Schema.org
│   └── _markup/render-image.html        # Image lazy loading
├── templates/               # Content templates
├── data/                    # Data files
├── reports/                 # SEO reports
├── .github/workflows/       # GitHub Actions
└── docs/                    # Documentation
```

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone --recurse-submodules https://github.com/fearless6677/ai-marketing-site.git
cd ai-marketing-site

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run Hugo locally
hugo server -D

# 4. Visit http://localhost:1313
```

### Manual Article Publishing

```bash
# Create Markdown file in content/manual/ or content/posts/
hugo new posts/my-article.md

# Local preview
hugo server -D

# Commit and publish
git add content/
git commit -m "feat: New article - Article Title"
git push origin main
```

### Run Automation Workflow

```bash
# Complete workflow: Collect -> Generate -> Build -> Publish -> SEO
python scripts/main.py

# Run individual steps
python scripts/collect_hotspots.py
python scripts/generate_article.py
python scripts/publish.py
python scripts/submit_to_baidu.py
python scripts/submit_to_google.py
```

## ⚙️ Configuration

### Environment Variables (GitHub Secrets)

| Variable | Description | How to Obtain |
|----------|-------------|---------------|
| `ANTHROPIC_API_KEY` | Claude API key | [console.anthropic.com](https://console.anthropic.com/) |
| `BAIDU_TOKEN` | Baidu Webmaster Platform push token | [ziyuan.baidu.com](https://ziyuan.baidu.com/) |
| `GOOGLE_CREDENTIALS` | Google service account JSON (base64) | [Google Cloud Console](https://console.cloud.google.com/) |

### Site Configuration

Edit `config.yaml`:
- `baseURL`: Change to your domain
- `title`: Website title
- `params.description`: Website description

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Deployment Guide](docs/DEPLOYMENT.md) | Deploy from scratch (environment setup, domain, GitHub Pages) |
| [Automation Guide](docs/AUTOMATION.md) | Automation workflow details (collection→generation→publishing→SEO) |
| [User Manual](USAGE.md) | Daily operations manual (manual posting, review, troubleshooting) |
| [DNS Setup](DNS_SETUP.md) | Domain DNS resolution configuration guide |
| [Script Documentation](scripts/README.md) | Python automation script API documentation |

## 📊 Automation Workflow

### Scheduled Tasks

| Time (Beijing) | Task | Description |
|----------------|------|-------------|
| 09:00 | Auto collection + generation | First article on workdays |
| 14:00 | Auto collection + generation | Second article on workdays |
| 19:00 | Auto collection + generation | Third article on workdays |
| 00:00 | Daily report | Operational statistics |

### Publishing Strategy

- Workdays: Up to 3 automated articles per day
- Weekends: Up to 1 article per day
- Supports manual publishing of additional articles

## 💰 Cost Estimation

| Item | Monthly Cost |
|------|--------------|
| Claude API | ¥50-100 |
| GitHub Pages | Free |
| Domain | ¥50-100/year |
| **Total** | **~¥100-150/month** |

## 🌍 Multi-Language Support

This project supports multiple languages to serve the ASEAN region:

- [中文](README.md) - Chinese
- [English](README.en.md) - English
- [ภาษาไทย](README.th.md) - Thai
- [Tiếng Việt](README.vi.md) - Vietnamese
- [Bahasa Indonesia](README.id.md) - Indonesian
- [Bahasa Melayu](README.ms.md) - Malay
- [Filipino](README.ph.md) - Filipino

## 📄 License

MIT License
