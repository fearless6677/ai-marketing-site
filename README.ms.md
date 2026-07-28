# Perkhidmatan Pemasaran Bersepadu AI

> **R&D di Bandar Tahap Satu + Integrasi di Guangxi + Aplikasi di ASEAN** — Penyelesaian Pemasaran Pintar Digerakkan oleh AI

[![Auto Publish](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml/badge.svg)](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml)

## 📋 Gambaran Keseluruhan

Ini adalah laman web berita pemasaran AI yang dibina dengan Hugo + tema PaperMod, dengan keupayaan automasi proses penuh:

- 🔥 **Pengumpulan Topik Hangat** — Secara automatik mengumpul topik berkaitan AI dari Weibo, Baidu, Zhihu, 36Kr, dll.
- 🤖 **Penjanaan Kandungan AI** — Menggunakan Claude API untuk menukar topik hangat menjadi artikel analisis mendalam
- 🚀 **Penerbitan Automatik** — Git commit mencetuskan bina dan penggunaan automatik
- 🔍 **Pengoptimuman SEO** — Secara automatik menghantar pautan ke enjin carian seperti Baidu dan Google

## 🏗️ Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Penjana Laman Statik | Hugo v0.120+ |
| Tema | PaperMod |
| Pengehosan | GitHub Pages |
| CI/CD | GitHub Actions |
| Perkhidmatan AI | Claude API (Anthropic) |
| Bahasa Pengaturcaraan | Python 3.10+ |

## 🚀 Permulaan Pantas

### Pembangunan Tempatan

```bash
# 1. Klon repository
git clone --recurse-submodules https://github.com/fearless6677/ai-marketing-site.git
cd ai-marketing-site

# 2. Pasang kebergantungan Python
pip install -r requirements.txt

# 3. Jalankan Hugo secara tempatan
hugo server -D

# 4. Lawati http://localhost:1313
```

### Penerbitan Artikel Manual

```bash
# Buat fail Markdown dalam content/manual/ atau content/posts/
hugo new posts/my-article.md

# Pratonton tempatan
hugo server -D

# Komit dan terbitkan
git add content/
git commit -m "feat: Artikel baru - Tajuk artikel"
git push origin main
```

## 🌍 Sokongan Pelbagai Bahasa

Projek ini menyokong pelbagai bahasa untuk melayani rantau ASEAN:

- [中文](README.md) - Cina
- [English](README.en.md) - Inggeris
- [ภาษาไทย](README.th.md) - Thai
- [Tiếng Việt](README.vi.md) - Vietnam
- [Bahasa Indonesia](README.id.md) - Indonesia
- [Bahasa Melayu](README.ms.md) - Melayu
- [Filipino](README.ph.md) - Filipino

## 📄 Lesen

MIT License
