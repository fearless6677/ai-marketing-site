"""
主流程控制脚本
编排: 采集 -> 生成 -> 构建 -> 发布 -> SEO提交
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent


def run_step(name: str, func, *args, **kwargs) -> bool:
    """执行一个步骤"""
    logger.info(f"\n{'='*50}")
    logger.info(f"步骤: {name}")
    logger.info(f"{'='*50}")
    try:
        result = func(*args, **kwargs)
        if result is False:
            logger.warning(f"步骤 [{name}] 返回失败")
            return False
        logger.info(f"步骤 [{name}] 完成")
        return True
    except Exception as e:
        logger.error(f"步骤 [{name}] 异常: {e}")
        return False


def step_collect():
    """步骤1: 热点采集"""
    from collect_hotspots import main
    return main()


def step_generate():
    """步骤2: AI内容生成"""
    from generate_article import main
    files = main()
    return len(files) > 0 if files else False


def step_build():
    """步骤3: Hugo构建"""
    import subprocess
    result = subprocess.run(
        ['hugo', '--minify'],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        timeout=120
    )
    if result.returncode != 0:
        logger.error(f"Hugo构建失败: {result.stderr}")
        return False
    logger.info("Hugo构建成功")
    return True


def step_publish():
    """步骤4: Git发布"""
    from publish import publish
    return publish()


def step_seo_submit():
    """步骤5: SEO提交"""
    from submit_to_baidu import main as baidu_main
    from submit_to_google import main as google_main

    baidu_ok = baidu_main()
    google_ok = google_main()
    return baidu_ok and google_ok


def step_notify(results: dict, error_msg: str = ""):
    """步骤6: 发送通知"""
    try:
        from notify import notify_success, notify_failure, notify_daily_summary

        # 判断整体是否成功
        all_ok = all(results.values())

        if all_ok:
            # 收集今日统计
            today_stats = _collect_today_stats()
            notify_daily_summary(today_stats)
        elif any(results.values()):
            # 部分成功
            notify_success(results)
        else:
            # 全部失败
            notify_failure(results, error_msg)

        return True
    except Exception as e:
        logger.warning(f"通知步骤失败（不影响整体流程）: {e}")
        return True  # 通知失败不算关键失败


def _collect_today_stats() -> dict:
    """收集今日运营统计数据"""
    from daily_report import count_today_articles, count_hotspots

    return {
        'hotspots': count_hotspots(),
        'articles': count_today_articles(),
        'published': count_today_articles(),
        'seo_submitted': 0,  # 实际数量在SEO步骤统计
    }


def main():
    """主函数"""
    logger.info(f"\n{'#'*60}")
    logger.info(f"# AI营销自动化 - 开始执行")
    logger.info(f"# 时间: {datetime.now().isoformat()}")
    logger.info(f"{'#'*60}\n")

    # 确保日志目录存在
    (BASE_DIR / 'logs').mkdir(exist_ok=True)

    steps = [
        ('热点数据采集', step_collect),
        ('AI内容生成', step_generate),
        ('Hugo构建', step_build),
        ('Git发布', step_publish),
        ('SEO提交', step_seo_submit),
    ]

    results = {}
    for name, func in steps:
        results[name] = run_step(name, func)

    # 输出汇总
    logger.info(f"\n{'='*50}")
    logger.info("执行汇总:")
    for name, ok in results.items():
        status = '✅ 成功' if ok else '❌ 失败'
        logger.info(f"  {name}: {status}")
    logger.info(f"{'='*50}")

    # 发送通知
    error_msg = ""
    if not results.get('热点数据采集') or not results.get('Hugo构建'):
        error_msg = "关键步骤（采集或构建）失败，请检查日志"

    step_notify(results, error_msg)

    # 关键步骤失败则退出码1
    if not results.get('热点数据采集') or not results.get('Hugo构建'):
        logger.error("关键步骤失败")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
