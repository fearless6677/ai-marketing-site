"""
企业微信机器人通知脚本
发布成功/失败后推送通知消息
支持：企业微信机器人、普通Webhook
"""

import os
import json
import hmac
import hashlib
import base64
import time
import logging
from datetime import datetime, date
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/notify.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent


# ─────────────────────────────────────────────────────────────
# 企业微信机器人
# ─────────────────────────────────────────────────────────────

def send_wecom_bot(webhook_url: str, content: str, mentioned_list: list = None) -> bool:
    """
    发送企业微信机器人消息（文本类型）

    Args:
        webhook_url: 企业微信机器人Webhook URL
        content: 消息内容（最大2048字节）
        mentioned_list: @成员列表（如 ["wangqing","@all"]）
    """
    payload = {
        "msgtype": "text",
        "text": {
            "content": content[:2048],
        }
    }
    if mentioned_list:
        payload["text"]["mentioned_list"] = mentioned_list

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        result = resp.json()
        if result.get('errcode') == 0:
            logger.info("企业微信机器人消息发送成功")
            return True
        else:
            logger.error(f"企业微信发送失败: {result}")
            return False
    except Exception as e:
        logger.error(f"企业微信发送异常: {e}")
        return False


def send_wecom_markdown(webhook_url: str, content: str) -> bool:
    """
    发送企业微信机器人 Markdown 消息
    """
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content[:4096]
        }
    }
    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        result = resp.json()
        if result.get('errcode') == 0:
            logger.info("企业微信Markdown消息发送成功")
            return True
        else:
            logger.error(f"企业微信Markdown发送失败: {result}")
            return False
    except Exception as e:
        logger.error(f"企业微信Markdown发送异常: {e}")
        return False


# ─────────────────────────────────────────────────────────────
# 通用 Webhook（钉钉、飞书、自定义等）
# ─────────────────────────────────────────────────────────────

def send_generic_webhook(webhook_url: str, payload: dict, secret: str = None) -> bool:
    """
    发送通用Webhook通知

    Args:
        webhook_url: Webhook URL
        payload: JSON消息体
        secret: 签名密钥（可选，用于钉钉等需要签名的平台）
    """
    if secret:
        # 钉钉签名逻辑
        timestamp = str(round(time.time() * 1000))
        string_to_sign = f'{timestamp}\n{secret}'
        hmac_code = hmac.new(
            secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        webhook_url = f"{webhook_url}&timestamp={timestamp}&sign={sign}"

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        if resp.status_code == 200:
            logger.info(f"Webhook通知发送成功: {webhook_url}")
            return True
        else:
            logger.error(f"Webhook发送失败: HTTP {resp.status_code} - {resp.text[:200]}")
            return False
    except Exception as e:
        logger.error(f"Webhook发送异常: {e}")
        return False


# ─────────────────────────────────────────────────────────────
# 通知内容构建
# ─────────────────────────────────────────────────────────────

def build_success_message(results: dict, articles: list = None) -> str:
    """构建成功通知内容（Markdown格式）"""
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M:%S")

    lines = [
        f"## ✅ 自动发布成功通知",
        f"**日期**: {today}  ",
        f"**完成时间**: {now}",
        "",
        "### 执行结果",
        "",
    ]

    for step, ok in results.items():
        icon = "✅" if ok else "❌"
        lines.append(f"- {icon} {step}: {'成功' if ok else '失败'}")

    if articles:
        lines.append("")
        lines.append("### 今日发布文章")
        lines.append("")
        for article in articles[:5]:
            lines.append(f"- **{article.get('title', '无标题')}**")

    lines.append("")
    lines.append(f"🔗 [查看网站](https://aimarketing.site)")

    return "\n".join(lines)


def build_failure_message(results: dict, error_msg: str = "") -> str:
    """构建失败通知内容"""
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M:%S")

    lines = [
        f"## ❌ 自动发布失败告警",
        f"**日期**: {today}  ",
        f"**时间**: {now}",
        "",
        "### 执行状态",
        "",
    ]

    for step, ok in results.items():
        icon = "✅" if ok else "❌"
        lines.append(f"- {icon} {step}: {'成功' if ok else '失败'}")

    if error_msg:
        lines.append("")
        lines.append(f"### 错误信息")
        lines.append(f"```")
        lines.append(error_msg[:500])
        lines.append(f"```")

    lines.append("")
    lines.append("> 请检查 GitHub Actions 日志或联系管理员")

    return "\n".join(lines)


def build_daily_summary(today_stats: dict) -> str:
    """构建每日汇总通知"""
    today = date.today().isoformat()

    lines = [
        f"## 📊 每日运营汇总",
        f"**日期**: {today}",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| 采集热点 | {today_stats.get('hotspots', 0)} 条 |",
        f"| 新增文章 | {today_stats.get('articles', 0)} 篇 |",
        f"| 发布成功 | {today_stats.get('published', 0)} 篇 |",
        f"| SEO提交 | {today_stats.get('seo_submitted', 0)} 条 |",
        "",
        f"🔗 [查看网站](https://aimarketing.site) | [查看报告](https://github.com/ai-marketing/ai-marketing-site/tree/main/reports)",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# 主发送函数
# ─────────────────────────────────────────────────────────────

def get_webhook_url() -> str:
    """获取Webhook URL（环境变量优先）"""
    return os.environ.get('WECOM_WEBHOOK_URL', '')


def send_notification(msg_type: str, content: str, webhook_url: str = None) -> bool:
    """
    统一发送通知

    Args:
        msg_type: 消息类型 'text' | 'markdown'
        content: 消息内容
        webhook_url: 指定webhook（可选，默认读环境变量）
    """
    url = webhook_url or get_webhook_url()
    if not url:
        logger.warning("Webhook URL 未配置（WECOM_WEBHOOK_URL），通知跳过")
        return False

    if msg_type == 'markdown':
        return send_wecom_markdown(url, content)
    else:
        return send_wecom_bot(url, content)


def notify_success(results: dict, articles: list = None) -> bool:
    """发送成功通知"""
    content = build_success_message(results, articles)
    return send_notification('markdown', content)


def notify_failure(results: dict, error_msg: str = "") -> bool:
    """发送失败通知"""
    content = build_failure_message(results, error_msg)
    return send_notification('markdown', content)


def notify_daily_summary(stats: dict) -> bool:
    """发送每日汇总"""
    content = build_daily_summary(stats)
    return send_notification('markdown', content)


# ─────────────────────────────────────────────────────────────
# 命令行入口
# ─────────────────────────────────────────────────────────────

def main():
    """命令行入口：发送测试消息或从JSON读取结果发送"""
    import argparse
    parser = argparse.ArgumentParser(description='通知系统')
    parser.add_argument('--test', action='store_true', help='发送测试消息')
    parser.add_argument('--type', choices=['success', 'failure', 'daily'], default='success',
                        help='通知类型')
    parser.add_argument('--results', type=str, help='JSON格式的执行结果')
    parser.add_argument('--message', type=str, help='附加消息/错误信息')
    args = parser.parse_args()

    webhook_url = get_webhook_url()

    if args.test:
        content = "## 🧪 测试通知\n\n通知系统工作正常！\n\n" + \
                  f"时间: {datetime.now().isoformat()}\n" + \
                  f"Webhook: {webhook_url[:30]}..."
        success = send_notification('markdown', content)
        print("测试通知发送成功" if success else "测试通知发送失败")
        return 0 if success else 1

    # 解析结果
    if args.results:
        try:
            results = json.loads(args.results)
        except json.JSONDecodeError:
            results = {"步骤解析失败": False}
    else:
        results = {"通知": True}

    # 发送对应类型通知
    if args.type == 'success':
        success = notify_success(results)
    elif args.type == 'failure':
        success = notify_failure(results, args.message or '')
    elif args.type == 'daily':
        success = notify_daily_summary(results)
    else:
        success = False

    return 0 if success else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
