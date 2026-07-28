# บริการการตลาดแบบบูรณาการ AI

> **วิจัยและพัฒนาในเมืองชั้นหนึ่ง + บูรณาการในกว่างซี + ประยุกต์ใช้ในอาเซียน** — โซลูชันการตลาดอัจฉริยะที่ขับเคลื่อนด้วย AI

[![Auto Publish](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml/badge.svg)](https://github.com/fearless6677/ai-marketing-site/actions/workflows/auto-publish.yml)

## 📋 ภาพรวม

นี่คือเว็บไซต์ข่าวสารการตลาด AI ที่สร้างด้วย Hugo + ธีม PaperMod พร้อมความสามารถในการทำงานอัตโนมัติแบบเต็มรูปแบบ:

- 🔥 **การรวบรวมหัวข้อร้อน** — รวบรวมหัวข้อที่เกี่ยวข้องกับ AI จาก Weibo, Baidu, Zhihu, 36Kr โดยอัตโนมัติ
- 🤖 **การสร้างเนื้อหาด้วย AI** — ใช้ Claude API แปลงหัวข้อร้อนเป็นบทความวิเคราะห์เชิงลึก
- 🚀 **การเผยแพร่อัตโนมัติ** — การ commit Git ทริกเกอร์การ build และ deploy อัตโนมัติ
- 🔍 **การปรับปรุง SEO** — ส่งลิงก์ไปยังเครื่องมือค้นหาเช่น Baidu และ Google โดยอัตโนมัติ

## 🏗️ เทคโนโลยี

| ส่วนประกอบ | เทคโนโลยี |
|------------|----------|
| เครื่องมือสร้างเว็บไซต์แบบ static | Hugo v0.120+ |
| ธีม | PaperMod |
| โฮสติ้ง | GitHub Pages |
| CI/CD | GitHub Actions |
| บริการ AI | Claude API (Anthropic) |
| ภาษาโปรแกรม | Python 3.10+ |

## 🚀 เริ่มต้นอย่างรวดเร็ว

### การพัฒนาในเครื่อง

```bash
# 1. Clone repository
git clone --recurse-submodules https://github.com/fearless6677/ai-marketing-site.git
cd ai-marketing-site

# 2. ติดตั้ง dependencies ของ Python
pip install -r requirements.txt

# 3. รัน Hugo ในเครื่อง
hugo server -D

# 4. เข้าชมที่ http://localhost:1313
```

### การเผยแพร่บทความด้วยตนเอง

```bash
# สร้างไฟล์ Markdown ใน content/manual/ หรือ content/posts/
hugo new posts/my-article.md

# ดูตัวอย่างในเครื่อง
hugo server -D

# Commit และเผยแพร่
git add content/
git commit -m "feat: บทความใหม่ - ชื่อบทความ"
git push origin main
```

## 🌍 การรองรับหลายภาษา

โปรเจกต์นี้รองรับหลายภาษาเพื่อให้บริการภูมิภาคอาเซียน:

- [中文](README.md) - จีน
- [English](README.en.md) - อังกฤษ
- [ภาษาไทย](README.th.md) - ไทย
- [Tiếng Việt](README.vi.md) - เวียดนาม
- [Bahasa Indonesia](README.id.md) - อินโดนีเซีย
- [Bahasa Melayu](README.ms.md) - มาเลย์
- [Filipino](README.ph.md) - ฟิลิปปินส์

## 📄 สิทธิ์การใช้งาน

MIT License
