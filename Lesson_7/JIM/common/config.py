""" Модуль с константами, все значения лежат в "conf.yaml" """

import yaml
import os

MODULE_DIR = os.path.dirname(__file__)

# Все настройки берем из "conf.yaml"
with open(MODULE_DIR + '/conf.yaml', encoding='utf-8') as f:
    data_file = yaml.load(f, Loader=yaml.FullLoader)

# ip и ports
DEFAULT_PORT = data_file['host_conf'].get('DEFAULT_PORT')
DEFAULT_IP_ADDRESS = data_file['host_conf'].get('DEFAULT_IP')

# Протокол JIM основные ключи:
ACTION = data_file['jit_key'].get('ACTION')
TIME = data_file['jit_key'].get('TIME')
USER = data_file['jit_key'].get('USER')
SENDER = data_file['jit_key'].get('SENDER')
ACCOUNT_NAME = data_file['jit_key'].get('ACCOUNT_NAME')
MESSAGE_TEXT = data_file['jit_key'].get('MESSAGE_TEXT')
MESSAGE = data_file['jit_key'].get('MESSAGE')

# Прочие ключи, используемые в протоколе
PRESENCE = data_file['other_key'].get('PRESENCE')
RESPONSE = data_file['other_key'].get('RESPONSE')
ERROR = data_file['other_key'].get('ERROR')
BAD_REQ = data_file['other_key'].get('BAD_REQ')

# Прочие настройки
MAX_CONNECT = data_file['settings'].get('MAX_CONNECT')
MAX_LENGTH = data_file['settings'].get('MAX_LENGTH')
ENCODING = data_file['settings'].get('ENCODING')

# Логирование
LEVEL_CRITICAL = data_file['logging_level'].get('CRITICAL')
LEVEL_ERROR = data_file['logging_level'].get('ERROR')
LEVEL_WARNING = data_file['logging_level'].get('WARNING')
LEVEL_INFO = data_file['logging_level'].get('INFO')
LEVEL_DEBUG = data_file['logging_level'].get('DEBUG')
