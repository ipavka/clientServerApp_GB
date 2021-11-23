import sys
import logging
import inspect

import logs.confs.server_log_config
import logs.confs.client_log_config


if sys.argv[0].find('app_client.py') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(f'@ Вызываемая функция: <{func.__name__}> | c аргументам {args},'
                     f' {kwargs} | '
                     f'Модуль <{func.__module__}> | '
                     f'Вызов из функции <{inspect.stack()[1][3]}>', stacklevel=2)
        return result
    return wrapper
