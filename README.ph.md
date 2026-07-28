# AI Marketing Integration Service

> **R&D sa First-Tier na Lungsod + Integrasyon sa Guangxi + Aplikasyon sa ASEAN** — AI-Powered na Matalinong Solusyon sa Pemasaran

[![Auto Publish](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml/badge.svg)](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml)

## 📋 Pangkalahatang-ideya

Ito ay isang AI marketing news website na binuo gamit ang Hugo + PaperMod theme, na may full-process automation capabilities:

- 🔥 **Pagkolekta ng Mga Mainit na Paksa** — Awtomatikong nangongolekta ng mga AI-related na mainit na paksa mula sa Weibo, Baidu, Zhihu, 36Kr, atbp.
- 🤖 **AI Content Generation** — Gumagamit ng Claude API upang gawing malalim na pagsusuri ang mga mainit na paksa
- 🚀 **Auto Publishing** — Ang mga Git commit ay nag-trigger ng automatic build at deployment
- 🔍 **SEO Optimization** — Awtomatikong isinusumite ang mga link sa mga search engine tulad ng Baidu at Google

## 🏗️ Tech Stack

| Bahagi | Teknolohiya |
|--------|-------------|
| Static Site Generator | Hugo v0.120+ |
| Tema | PaperMod |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
| AI Service | Claude API (Anthropic) |
| Programming Language | Python 3.10+ |

## 🚀 Mabilis na Pagsisimula

### Lokal na Development

```bash
# 1. I-clone ang repository
git clone --recurse-submodules https://github.com/fearless6677/ai-marketing-site.git
cd ai-marketing-site

# 2. I-install ang mga Python dependencies
pip install -r requirements.txt

# 3. Patakbuhin ang Hugo nang lokal
hugo server -D

# 4. Bisitahin ang http://localhost:1313
```

### Manual na Pag-post ng Artikulo

```bash
# Gumawa ng Markdown file sa content/manual/ o content/posts/
hugo new posts/my-article.md

# Lokal na preview
hugo server -D

# I-commit at i-publish
git add content/
git commit -m "feat: Bagong artikulo - Pamagat ng artikulo"
git push origin main
```

## 🌍 Suporta sa Maraming Wika

Sinusuportahan ng proyektong ito ang maraming wika upang maglingkod sa rehiyon ng ASEAN:

- [中文](README.md) - Intsik
- [English](README.en.md) - Ingles
- [ภาษาไทย](README.th.md) - Thai
- [Tiếng Việt](README.vi.md) - Vietnamese
- [Bahasa Indonesia](README.id.md) - Indonesian
- [Bahasa Melayu](README.ms.md) - Malay
- [Filipino](README.ph.md) - Filipino

## 📄 Lisensya

MIT License
