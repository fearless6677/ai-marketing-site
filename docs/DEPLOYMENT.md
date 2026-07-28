# 部署指南

> 从本地开发到正式上线的完整部署流程

## 环境要求

| 工具 | 版本要求 | 说明 |
|------|---------|------|
| Hugo | >= 0.120.0 (extended) | 静态网站生成器 |
| Python | >= 3.10 | 自动化脚本运行 |
| Git | >= 2.30 | 版本控制 |
| GitHub | 账号 | 代码托管与Pages部署 |
| gh CLI | >= 2.0 (可选) | GitHub命令行工具 |

## 第一步：本地环境搭建

### 1.1 克隆仓库

```bash
git clone --recurse-submodules https://github.com/ai-marketing/ai-marketing.github.io.git
cd ai-marketing.github.io
```

> 注意：`--recurse-submodules` 会一并拉取 PaperMod 主题。如果忘记加，后续执行 `git submodule update --init --recursive`。

### 1.2 安装Python依赖

```bash
pip install -r requirements.txt
```

依赖列表：
- `requests` — HTTP请求
- `beautifulsoup4` — HTML解析
- `anthropic` — Claude API SDK
- `pyyaml` — YAML解析
- `python-dateutil` — 日期处理

### 1.3 本地运行Hugo

```bash
# Windows
F:/marketing/hugo-v0147/hugo.exe server -D

# 或全局安装的hugo
hugo server -D
```

访问 http://localhost:1313 查看效果。

### 1.4 验证构建产物

```bash
# 构建静态文件
hugo --minify

# 检查关键文件
ls public/index.html        # 首页
ls public/sitemap.xml       # Sitemap
ls public/robots.txt        # Robots规则
ls public/index.json        # JSON索引
```

## 第二步：GitHub 仓库配置

### 2.1 仓库信息

| 项目 | 值 |
|------|-----|
| 仓库地址 | https://github.com/ai-marketing/ai-marketing.github.io |
| 组织 | fearless6677 (ai-marketing) |
| 默认分支 | main |
| Pages分支 | main |
| 自定义域名 | aimarketing.site |
| HTTPS | 强制启用 |

### 2.2 推送代码

```bash
cd ai-marketing-site
git remote add origin https://github.com/ai-marketing/ai-marketing.github.io.git
git branch -M main
git push -u origin main
```

### 2.3 配置 Secrets

进入仓库 Settings → Secrets and variables → Actions，添加：

| Secret 名称 | 值 | 说明 |
|-------------|-----|------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | [获取地址](https://console.anthropic.com/settings/keys) |
| `BAIDU_TOKEN` | 百度站长平台token | [获取地址](https://ziyuan.baidu.com/linksubmit/index) |
| `GOOGLE_CREDENTIALS` | base64编码的服务账号JSON | 见下方说明 |

### 2.4 获取 Google 服务账号凭证

```bash
# 1. 访问 Google Cloud Console
# https://console.cloud.google.com/

# 2. 创建项目，启用 Indexing API

# 3. 创建服务账号，下载 JSON 密钥文件

# 4. Base64 编码
base64 -w 0 service-account.json > credentials_b64.txt

# 5. 将内容设置为 GOOGLE_CREDENTIALS secret
```

### 2.5 启用 GitHub Pages

1. 进入仓库 Settings → Pages
2. Source 选择 "GitHub Actions"（不是 "Deploy from a branch"）
3. 工作流会自动部署到 GitHub Pages
4. 首次推送代码后，约2-5分钟即可访问

### 2.6 验证部署成功

```bash
# 检查GitHub Pages部署状态
# 仓库 → Actions → 查看 "Auto Publish" 工作流是否绿色

# 验证网站可访问
curl -I https://aimarketing.site/
# 应返回 HTTP/2 200

# 验证SEO文件
curl -I https://aimarketing.site/sitemap.xml
curl -I https://aimarketing.site/robots.txt

# 验证JSON索引
curl -s https://aimarketing.site/index.json | head -1
```

## 第三步：域名配置

### 3.1 购买域名

推荐域名注册商：
- 阿里云（万网）
- 腾讯云
- Cloudflare

### 3.2 DNS 解析

如果使用 GitHub Pages，添加 CNAME 记录：

```
类型    主机记录    记录值
CNAME   @         YOUR_USERNAME.github.io
CNAME   www       YOUR_USERNAME.github.io
```

### 3.3 配置自定义域名

1. 在项目根目录创建 `static/CNAME` 文件，内容写入你的域名
2. 在 GitHub Pages 设置中填入自定义域名
3. 勾选 "Enforce HTTPS"

### 3.4 修改 Hugo 配置

编辑 `config.yaml`：

```yaml
baseURL: "https://yourdomain.com/"
```

## 第四步：百度站长平台配置

1. 访问 [百度站长平台](https://ziyuan.baidu.com/)
2. 添加站点，选择 HTML 标签验证
3. 在 Hugo 的 `layouts/partials/` 添加验证代码
4. 获取推送 token，设置为 `BAIDU_TOKEN` secret

## 第五步：验证部署

```bash
# 本地测试
hugo server -D

# 检查构建输出
ls public/

# 检查 sitemap
cat public/sitemap.xml

# 检查 robots.txt
cat public/robots.txt
```

## 常见问题

### Q: GitHub Actions 运行失败？

检查：
- Secrets 是否正确配置
- API Key 是否有效
- Python 依赖是否安装成功

### Q: 页面样式异常？

检查：
- 主题 submodule 是否正确拉取：`git submodule update --init --recursive`
- Hugo 版本是否 >= 0.120.0

### Q: 文章没有自动生成？

检查：
- `data/hotspots/` 目录是否有数据
- `ANTHROPIC_API_KEY` 是否有效
- 查看 Actions 运行日志
