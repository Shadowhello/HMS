import logging.config
import logging

def get_log_class():

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "simple": {
                "format": "%(levelname)s %(message)s"
            },
        },
        "handlers": {
            "null": {
                "level": "DEBUG",
                "class": "logging.NullHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose"
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                # 当达到10MB时分割日志
                "maxBytes": 1024 * 1024 * 10,
                # 最多保留50份文件
                "backupCount": 50,
                # If delay is true,
                # then file opening is deferred until the first call to emit().
                "delay": True,
                "filename": "hms.log",
                "formatter": "verbose"
            }
        },
        "loggers": {
            "": {
                "handlers": ["file"],
                "level": "INFO",
            },
        }
    })

    log = logging.getLogger(__name__)

    return log

