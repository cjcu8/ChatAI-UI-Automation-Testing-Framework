import logging
import datetime
import time
from pathlib import Path
from logging.handlers import RotatingFileHandler

# =========================
# 日志基础配置
# =========================

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 日志目录
LOG_DIR = BASE_DIR / "logs"

# 日志文件等级
LOG_LEVEL = logging.INFO

# 控制台日志等级
STREAM_LOG_LEVEL = logging.INFO

# 日志保留天数
LOG_KEEP_DAYS = 30

# 单个日志文件最大大小：5MB
LOG_MAX_BYTES = 5 * 1024 * 1024

# 日志滚动备份数量
LOG_BACKUP_COUNT = 7

# 日志文件名
LOG_FILE_NAME = f"ui_test.{time.strftime('%Y%m%d')}.log"

# 日志完整路径
LOG_FILE_PATH = LOG_DIR / LOG_FILE_NAME


class RecordLog:
    """
    UI 自动化日志生成器
    """

    def __init__(self):
        self.log_dir = LOG_DIR
        self.log_file_path = LOG_FILE_PATH

        self.create_log_dir()
        self.handle_overdue_log()

    def create_log_dir(self):
        """
        创建日志目录
        """
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)

    def handle_overdue_log(self):
        """
        清理过期日志文件，默认保留 30 天
        """
        now_time = datetime.datetime.now()
        overdue_time = now_time + datetime.timedelta(days=-LOG_KEEP_DAYS)
        overdue_timestamp = overdue_time.timestamp()

        for file_path in self.log_dir.iterdir():
            if not file_path.is_file():
                continue

            file_create_time = file_path.stat().st_ctime

            if file_create_time < overdue_timestamp:
                file_path.unlink()

    def get_logger(self):
        """
        获取 logger 对象
        """
        logger = logging.getLogger("ui_auto_test")

        # 防止重复添加 handler，避免日志重复打印
        if not logger.handlers:
            logger.setLevel(LOG_LEVEL)

            log_format = logging.Formatter(
                "%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d "
                "- [%(module)s:%(funcName)s] - %(message)s"
            )

            # 文件日志
            file_handler = RotatingFileHandler(
                filename=self.log_file_path,
                mode="a",
                maxBytes=LOG_MAX_BYTES,
                backupCount=LOG_BACKUP_COUNT,
                encoding="utf-8"
            )
            file_handler.setLevel(LOG_LEVEL)
            file_handler.setFormatter(log_format)
            logger.addHandler(file_handler)

            # 控制台日志
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(STREAM_LOG_LEVEL)
            stream_handler.setFormatter(log_format)
            logger.addHandler(stream_handler)

            # 防止日志向 root logger 继续传递，避免重复输出
            logger.propagate = False

        return logger


# 对外提供统一日志对象
uilog = RecordLog()
logs = uilog.get_logger()
