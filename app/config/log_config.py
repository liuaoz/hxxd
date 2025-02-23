import logging
import logging.config

# 配置日志
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(module)s - %(funcName)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {  # Root logger
            "level": "INFO",
            "handlers": ["console", "file"],
        },
        "uvicorn": {  # For Uvicorn logs
            "level": "INFO",
            "handlers": ["console"],
        },
    },
}

# 标志变量，确保日志配置只加载一次
_logging_configured = False


def setup_logging():
    global _logging_configured
    if not _logging_configured:
        logging.config.dictConfig(LOGGING_CONFIG)
        _logging_configured = True
