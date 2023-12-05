import logging
import os
from logging import handlers

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


class ProgramLogger:
    log_file_path = os.getcwd()
    filename = f"app_default.log"
    lg = os.path.join(log_file_path, filename)

    def __init__(self, name: str, log_path: object = lg, log_format: object = None, info_level: object = None):
        try:
            if name is None:
                raise ValueError("Name argument not specified")
            if not log_format:
                logformat = '%(message)s'
            else:
                logformat = log_format
            if not info_level:
                info_level = "info"
            self.log_path = log_path
            self.logformat = logformat
            self.name = name.upper()
            self.logger = logging.getLogger(self.name)
            log_level = self.level_to_int(info_level)
            self.logger.setLevel(log_level)
            self.add_consolehandler(log_level, logformat)

        except Exception as e:
            if self.logger:
                self.logger.error(str(e))

    @staticmethod
    def level_to_int(level):
        # LEVELS NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, and CRITICAL=50
        level = str(level).lower()
        if level == "debug":
            return 10
        elif level == "info":
            return 20
        elif level == "warn":
            return 30
        elif level == "error":
            return 40
        elif level == "critical":
            return 50
        else:
            return 20

    def error(self, message):
        self.logger.error(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

    def critical(self, message):
        self.logger.critical(message)

    def set_level(self, info_level):
        # To dynamically reset the loglevel, you need to also change the parent levels as well as all handlers!
        self.logger.parent.setLevel(info_level)
        for handler in self.logger.parent.handlers:
            handler.setLevel(info_level)

        self.logger.setLevel(info_level)
        for handler in self.logger.handlers:
            handler.setLevel(info_level)

        return self.logger.level

    def add_consolehandler(self, info_level=logging.INFO,
                           logformat='%(asctime)s %(levelname)s %(name)s %(funcName)s %(message)s'):
        sh = logging.StreamHandler()
        sh.setLevel(info_level)
        fl = handlers.RotatingFileHandler(self.log_path, maxBytes=2048000, backupCount=100, encoding='utf-8')
        fl.setLevel(info_level)
        formatter = logging.Formatter(logformat)
        sh.setFormatter(formatter)
        fl.setFormatter(formatter)
        self.logger.addHandler(sh)
        self.logger.addHandler(fl)
