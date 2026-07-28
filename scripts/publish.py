"""
自动发布脚本
处理Git操作和部署流程
"""

import os
import subprocess
import logging
from datetime import date
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/publish.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / 'content' / 'posts'


def run_git(args: list, cwd: str = None) -> tuple:
    """执行Git命令"""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd or str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        logger.error(f"Git命令超时: git {' '.join(args)}")
        return 1, '', 'timeout'
    except Exception as e:
        logger.error(f"Git命令异常: {e}")
        return 1, '', str(e)


def get_new_files() -> list:
    """获取新增的文章文件"""
    code, stdout, _ = run_git(['status', '--porcelain', 'content/posts/'])
    if code != 0:
        return []

    new_files = []
    for line in stdout.split('\n'):
        line = line.strip()
        if line.startswith('??') or line.startswith(' A ') or line.startswith(' M '):
            filepath = line[3:].strip()
            if filepath.endswith('.md'):
                new_files.append(filepath)
    return new_files


def git_add(files: list) -> bool:
    """Git add文件"""
    if not files:
        logger.info("没有需要添加的文件")
        return True

    code, _, stderr = run_git(['add'] + files)
    if code != 0:
        logger.error(f"git add失败: {stderr}")
        return False

    logger.info(f"已添加 {len(files)} 个文件")
    return True


def git_commit(message: str) -> bool:
    """Git提交"""
    code, _, stderr = run_git(['commit', '-m', message])
    if code != 0:
        if 'nothing to commit' in stderr or 'nothing to commit' in stderr:
            logger.info("没有需要提交的内容")
            return True
        logger.error(f"git commit失败: {stderr}")
        return False

    logger.info(f"已提交: {message}")
    return True


def git_push() -> bool:
    """Git推送"""
    # 先拉取最新代码
    code, _, stderr = run_git(['pull', '--rebase', 'origin', 'main'])
    if code != 0:
        logger.warning(f"git pull失败，尝试继续: {stderr}")

    code, stdout, stderr = run_git(['push', 'origin', 'main'])
    if code != 0:
        logger.error(f"git push失败: {stderr}")
        return False

    logger.info("已推送到远程仓库")
    return True


def extract_title(filepath: str) -> str:
    """从Markdown文件提取标题"""
    try:
        with open(BASE_DIR / filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    return line[2:].strip()
                if line.startswith('title:'):
                    return line.split(':', 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return '新文章'


def publish():
    """发布流程"""
    logger.info("=" * 50)
    logger.info("开始发布流程")
    logger.info("=" * 50)

    # 获取新文件
    new_files = get_new_files()
    if not new_files:
        logger.info("没有新的文章需要发布")
        return False

    logger.info(f"发现 {len(new_files)} 个新文件")

    # Git add
    if not git_add(new_files):
        return False

    # 生成提交信息
    if len(new_files) == 1:
        title = extract_title(new_files[0])
        message = f"feat: 新增文章 - {title}"
    else:
        message = f"feat: 新增 {len(new_files)} 篇文章 ({date.today().isoformat()})"

    # Git commit
    if not git_commit(message):
        return False

    # Git push
    if not git_push():
        return False

    logger.info("发布完成！")
    return True


def rollback():
    """回滚到上一个版本"""
    logger.warning("执行回滚操作...")
    code, _, stderr = run_git(['reset', '--hard', 'HEAD~1'])
    if code == 0:
        run_git(['push', '--force', 'origin', 'main'])
        logger.info("回滚完成")
    else:
        logger.error(f"回滚失败: {stderr}")


if __name__ == '__main__':
    success = publish()
    if not success:
        logger.error("发布失败")
        exit(1)
