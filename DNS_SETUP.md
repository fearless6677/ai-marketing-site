# DNS 配置指南

## 问题

当前域名 `aimarketing.site` 解析到 `145.131.10.225`（荷兰 Argeweb），需改为指向 GitHub Pages。

## 需要修改的 DNS 记录

### 方案一：A 记录（推荐）

在域名注册商（DNS 提供商）处添加以下 A 记录：

| 类型 | 主机记录 | 记录值 | TTL |
|------|----------|--------|-----|
| A | @ | 185.199.108.153 | 600 |
| A | @ | 185.199.109.153 | 600 |
| A | @ | 185.199.110.153 | 600 |
| A | @ | 185.199.111.153 | 600 |

### 方案二：CNAME 记录

如果域名注册商支持 CNAME 展平（Flattening）或别名（ALIAS），可配置：

| 类型 | 主机记录 | 记录值 | TTL |
|------|----------|--------|-----|
| CNAME/ALIAS | @ | ai-marketing.github.io | 600 |

> 注意：根域名（@）不能使用标准 CNAME，需要 DNS 提供商支持 CNAME Flattening。

### 需要删除的旧记录

- 删除指向 `145.131.10.225` 的 A 记录

## GitHub Pages 仓库配置

1. 仓库 Settings → Pages → Custom domain 填入 `aimarketing.site`
2. 勾选 "Enforce HTTPS"
3. `static/CNAME` 文件已配置为 `aimarketing.site`

## 验证 DNS 是否生效

```bash
# 等待 DNS 传播（通常 5-60 分钟）
nslookup aimarketing.site
# 或
dig aimarketing.site

# 应返回 GitHub Pages IP：
# 185.199.108.153
# 185.199.109.153
# 185.199.110.153
# 185.199.111.153
```

## 常见 DNS 提供商配置入口

- **阿里云 DNS**：https://dns.console.aliyun.com
- **腾讯云 DNS**：https://console.cloud.tencent.com/cns
- **Cloudflare**：https://dash.cloudflare.com
- **Godaddy**：https://dcc.godaddy.com/manage/dns

---

*此文件为部署参考文档，不随 Hugo 构建发布*
