# Dịch Vụ Tích Hợp Tiếp Thị AI

> **Nghiên cứu & Phát triển tại Thành phố Loại Một + Tích hợp tại Quảng Tây + Ứng dụng tại ASEAN** — Giải Pháp Tiếp Thị Thông Minh Được Điều Khiển Bởi AI

[![Auto Publish](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml/badge.svg)](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml)

## 📋 Tổng Quan

Đây là website tin tức tiếp thị AI được xây dựng với Hugo + theme PaperMod, với khả năng tự động hóa toàn bộ quy trình:

- 🔥 **Thu Thập Chủ Đề Nóng** — Tự động thu thập các chủ đề liên quan đến AI từ Weibo, Baidu, Zhihu, 36Kr, v.v.
- 🤖 **Tạo Nội Dung AI** — Sử dụng Claude API để biến các chủ đề nóng thành bài viết phân tích chuyên sâu
- 🚀 **Xuất Bản Tự Động** — Git commits kích hoạt build và deploy tự động
- 🔍 **Tối Ưu SEO** — Tự động gửi liên kết đến các công cụ tìm kiếm như Baidu và Google

## 🏗️ Công Nghệ

| Thành Phần | Công Nghệ |
|------------|-----------|
| Máy Tạo Trang Tĩnh | Hugo v0.120+ |
| Theme | PaperMod |
| Lưu Trữ | GitHub Pages |
| CI/CD | GitHub Actions |
| Dịch Vụ AI | Claude API (Anthropic) |
| Ngôn Ngữ Lập Trình | Python 3.10+ |

## 🚀 Bắt Đầu Nhanh

### Phát Triển Cục Bộ

```bash
# 1. Clone repository
git clone --recurse-submodules https://github.com/fearless6677/ai-marketing-site.git
cd ai-marketing-site

# 2. Cài đặt dependencies Python
pip install -r requirements.txt

# 3. Chạy Hugo cục bộ
hugo server -D

# 4. Truy cập http://localhost:1313
```

### Xuất Bản Bài Viết Thủ Công

```bash
# Tạo file Markdown trong content/manual/ hoặc content/posts/
hugo new posts/my-article.md

# Xem trước cục bộ
hugo server -D

# Commit và xuất bản
git add content/
git commit -m "feat: Bài viết mới - Tiêu đề bài viết"
git push origin main
```

## 🌍 Hỗ Trợ Đa Ngôn Ngữ

Dự án này hỗ trợ nhiều ngôn ngữ để phục vụ khu vực ASEAN:

- [中文](README.md) - Tiếng Trung
- [English](README.en.md) - Tiếng Anh
- [ภาษาไทย](README.th.md) - Tiếng Thái
- [Tiếng Việt](README.vi.md) - Tiếng Việt
- [Bahasa Indonesia](README.id.md) - Tiếng Indonesia
- [Bahasa Melayu](README.ms.md) - Tiếng Malay
- [Filipino](README.ph.md) - Tiếng Filipino

## 📄 Giấy Phép

MIT License
