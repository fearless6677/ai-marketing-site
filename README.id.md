# Layanan Pemasaran Terintegrasi AI

> **R&D di Kota Tingkat Satu + Integrasi di Guangxi + Aplikasi di ASEAN** — Solusi Pemasaran Cerdas yang Digerakkan oleh AI

[![Auto Publish](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml/badge.svg)](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml)

## 📋 Ringkasan

Ini adalah website berita pemasaran AI yang dibangun dengan Hugo + tema PaperMod, dengan kemampuan otomatisasi proses penuh:

- 🔥 **Pengumpulan Topik Hangat** — Secara otomatis mengumpulkan topik terkait AI dari Weibo, Baidu, Zhihu, 36Kr, dll.
- 🤖 **Pembuatan Konten AI** — Menggunakan Claude API untuk mengubah topik hangat menjadi artikel analisis mendalam
- 🚀 **Penerbitan Otomatis** — Git commit memicu build dan deployment otomatis
- 🔍 **Optimasi SEO** — Secara otomatis mengirimkan tautan ke mesin pencari seperti Baidu dan Google

## 🏗️ Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Generator Situs Statis | Hugo v0.120+ |
| Tema | PaperMod |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
| Layanan AI | Claude API (Anthropic) |
| Bahasa Pemrograman | Python 3.10+ |

## 🚀 Mulai Cepat

### Pengembangan Lokal

```bash
# 1. Clone repository
git clone --recurse-submodules https://github.com/fearless6677/ai-marketing-site.git
cd ai-marketing-site

# 2. Instal dependensi Python
pip install -r requirements.txt

# 3. Jalankan Hugo secara lokal
hugo server -D

# 4. Kunjungi http://localhost:1313
```

### Penerbitan Artikel Manual

```bash
# Buat file Markdown di content/manual/ atau content/posts/
hugo new posts/my-article.md

# Pratinjau lokal
hugo server -D

# Commit dan terbitkan
git add content/
git commit -m "feat: Artikel baru - Judul artikel"
git push origin main
```

## 🌍 Dukungan Multi-Bahasa

Proyek ini mendukung beberapa bahasa untuk melayani kawasan ASEAN:

- [中文](README.md) - Cina
- [English](README.en.md) - Inggris
- [ภาษาไทย](README.th.md) - Thai
- [Tiếng Việt](README.vi.md) - Vietnam
- [Bahasa Indonesia](README.id.md) - Indonesia
- [Bahasa Melayu](README.ms.md) - Melayu
- [Filipino](README.ph.md) - Filipino

## 📄 Lisensi

MIT License
