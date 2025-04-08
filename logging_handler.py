import logging
from logging.handlers import RotatingFileHandler
from config_manager import config


LOGGING_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}
TERMINAL_LOG_LEVEL = LOGGING_LEVELS[config.get("LOG.terminal_logging_level")]
FILE_LOG_LEVEL = LOGGING_LEVELS[config.get("LOG.file_logging_level")]

# File handler - logs everything
file_handler = RotatingFileHandler(
    config.get("LOG.file_path"),
    encoding="utf-8",
    backupCount=config.get("LOG.backup_file_count"),
    maxBytes=config.get("LOG.max_file_size") * 1024 * 1024, )
file_handler.setLevel(FILE_LOG_LEVEL)

# Terminal (stream) handler - logs based on TERMINAL_LOG_LEVEL
stream_handler = logging.StreamHandler()
stream_handler.setLevel(TERMINAL_LOG_LEVEL)

export_logger = logging.getLogger("export")
preparation_logger = logging.getLogger("preparation")

logging_enabled = [config.get("LOG.export_terminal_logging"),
                   config.get("LOG.preparation_terminal_logging")]
for i, logger_instance in enumerate([export_logger, preparation_logger]):
    logger_instance.setLevel(logging.DEBUG)
    logger_instance.addHandler(file_handler)
    if logging_enabled[i]:
        logger_instance.addHandler(stream_handler)


formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)