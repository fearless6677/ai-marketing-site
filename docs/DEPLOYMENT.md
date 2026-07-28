# 部署指南

## 环境要求

- Hugo >= 0.120.0 (extended)
- Python >= 3.10
- Git
- GitHub 账号

## 第一步：GitHub 仓库配置

### 1.1 创建仓库

1. 在 GitHub 创建新仓库 `ai-marketing-site`
2. 推送本地代码：

```bash
cd ai-marketing-site
git remote add origin https://github.com/YOUR_USERNAME/ai-marketing-site.git
git push -u origin main
```

### 1.2 配置 Secrets

进入仓库 Settings → Secrets and variables → Actions，添加：

| Secret 名称 | 值 | 说明 |
|-------------|-----|------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | [获取地址](https://console.anthropic.com/settings/keys) |
| `BAIDU_TOKEN` | 百度站长平台token | [获取地址](https://ziyuan.baidu.com/linksubmit/index) |
| `GOOGLE_CREDENTIALS` | base64编码的服务账号JSON | 见下方说明 |

### 1.3 获取 Google 服务账号凭证

```bash
# 1. 访问 Google Cloud Console
# https://console.cloud.google.com/

# 2. 创建项目，启用 Indexing API

# 3. 创建服务账号，下载 JSON 密钥文件

# 4. Base64 编码
base64 -w 0 service-account.json > credentials_b64.txt

# 5. 将内容设置为 GOOGLE_CREDENTIALS secret
```

### 1.4 启用 GitHub Pages

1. Settings → Pages
2. Source 选择 "GitHub Actions"
3. 工作流会自动部署

## 第二步：域名配置

### 2.1 购买域名

推荐域名注册商：
- 阿里云（万网）
- 腾讯云
- Cloudflare

### 2.2 DNS 解析

如果使用 GitHub Pages，添加 CNAME 记录：

```
类型    主机记录    记录值
CNAME   @         YOUR_USERNAME.github.io
CNAME   www       YOUR_USERNAME.github.io
```

### 2.3 配置自定义域名

1. 在项目根目录创建 `static/CNAME` 文件，内容写入你的域名
2. 在 GitHub Pages 设置中填入自定义域名
3. 勾选 "Enforce HTTPS"

### 2.4 修改 Hugo 配置

编辑 `config.yaml`：

```yaml
baseURL: "https://yourdomain.com/"
```

## 第三步：百度站长平台配置

1. 访问 [百度站长平台](https://ziyuan.baidu.com/)
2. 添加站点，选择 HTML 标签验证
3. 在 Hugo 的 `layouts/partials/` 添加验证代码
4. 获取推送 token，设置为 `BAIDU_TOKEN` secret

## 第四步：验证部署

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
