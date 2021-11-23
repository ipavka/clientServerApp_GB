import logging.handlers
import logging
import os
import sys
from common.config import LEVEL_ERROR, LEVEL_DEBUG

server_log_path = os.path.abspath(os.path.join(__file__, "../../dir_logs/cli/"))
PATH = os.path.join(server_log_path, 'client.log')

str_fmt = f"[%(asctime)s] [%(levelname)s]  %(filename)s  %(message)s"
date_fmt = '%d %b %Y %H:%M:%S'
LOG_FORMAT = logging.Formatter(fmt=str_fmt, datefmt=date_fmt)

LOG_STREAM = logging.StreamHandler(sys.stderr)
LOG_STREAM.setFormatter(LOG_FORMAT)
LOG_STREAM.setLevel(LEVEL_ERROR)

FILE_LOG = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8')
FILE_LOG.setFormatter(LOG_FORMAT)

logger = logging.getLogger('client')
logger.addHandler(LOG_STREAM)
logger.addHandler(FILE_LOG)
logger.setLevel(LEVEL_DEBUG)


if __name__ == '__main__':
    logger.critical("Критическая")
    logger.error("Ошибка")
    logger.warning("Предупреждение")
    logger.debug("Отладка")
    logger.info("Инфо")
