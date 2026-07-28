# 自动化流程说明

## 工作流概览

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  热点采集    │ →  │  AI内容生成  │ →  │  Hugo构建   │ →  │  Git发布    │ →  │  SEO提交    │
│ collect_    │    │ generate_   │    │   hugo      │    │  publish.py │    │ submit_to_* │
│ hotspots.py │    │ article.py  │    │  --minify   │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 定时任务

GitHub Actions 配置了以下定时任务：

### auto-publish.yml

| 触发时间 (UTC) | 触发时间 (北京) | 说明 |
|----------------|----------------|------|
| 01:00 | 09:00 | 工作日上午第一篇 |
| 06:00 | 14:00 | 工作日下午第二篇 |
| 11:00 | 19:00 | 工作日晚上第三篇 |

### daily-report.yml

| 触发时间 (UTC) | 触发时间 (北京) | 说明 |
|----------------|----------------|------|
| 16:00 | 00:00 | 生成每日运营报告 |

## 热点采集流程

### 数据源

1. **微博热搜** — 每小时更新，社交热点
2. **百度热搜** — 每2小时更新，搜索热点
3. **知乎热榜** — 每3小时更新，深度讨论
4. **36氪** — 每6小时更新，科技商业

### 筛选规则

- 关键词匹配：AI、科技、营销、广西、东盟等
- 热度排名：Top 50
- 去重：相似度 > 0.8 的只保留一条
- 存储：`data/hotspots/YYYY-MM-DD.json`

## AI内容生成

### 模型选择

- 默认：Claude 3.5 Sonnet
- 备选：GPT-4、GLM-4

### 提示词模板

- 热点文章：`templates/prompts/hotspot_prompt.txt`
- 政策解读：`templates/prompts/policy_prompt.txt`

### 质量控制

1. 字数检查：1000-3000字
2. 敏感词过滤
3. Front-matter 完整性
4. 最多重试3次

### 成本估算

- 每篇文章：约 ¥0.5-2（Claude API）
- 每日3篇：约 ¥1.5-6/天
- 每月：约 ¥50-180/月

## Git发布流程

```bash
# 1. 添加新文件
git add content/posts/ data/ logs/

# 2. 提交
git commit -m "feat: 新增文章 - {title}"

# 3. 拉取最新（防止冲突）
git pull --rebase origin main

# 4. 推送
git push origin main

# 5. 触发 GitHub Actions 自动部署
```

## SEO提交

### 百度

- API：百度搜索开放平台 - 主动推送
- 配额：普通收录每天100条
- 实现：`scripts/submit_to_baidu.py`

### Google

- API：Google Indexing API
- 配额：每天200条
- 实现：`scripts/submit_to_google.py`

### 其他

- 360搜索、搜狗、Bing 通过 sitemap.xml 提交

## 错误处理

| 错误类型 | 处理方式 |
|----------|---------|
| API调用失败 | 重试3次，记录日志 |
| Git冲突 | 自动 pull rebase 后重试 |
| 构建失败 | 回滚到上一版本 |
| 部署失败 | 发送告警通知 |
| 质量检查不通过 | 重新生成或跳过 |

## 日志文件

| 文件 | 内容 |
|------|------|
| `logs/collect.log` | 热点采集日志 |
| `logs/generate.log` | 内容生成日志 |
| `logs/publish.log` | 发布日志 |
| `logs/seo.log` | SEO提交日志 |
| `logs/main.log` | 主流程日志 |

## 手动触发

```bash
# 手动运行完整流程
python scripts/main.py

# 或通过 GitHub Actions
# 在仓库 Actions 页面选择工作流，点击 "Run workflow"
```

## 监控与告警

建议配置以下监控：

1. **GitHub Actions 状态** — 失败时邮件通知
2. **API 成本** — 在 Anthropic Console 设置预算告警
3. **网站可用性** — 使用 UptimeRobot 等服务监控
4. **SEO 效果** — 每周检查百度/Google 收录情况
