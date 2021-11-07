""" Модуль с константами, все значения лежат в "conf.yaml" """

import yaml

# Все настройки берем из "conf.yaml"
with open('common/conf.yaml', encoding='utf-8') as f:
    data_file = yaml.load(f, Loader=yaml.FullLoader)

# ip и ports
DEFAULT_PORT = data_file['host_conf'].get('DEFAULT_PORT')
DEFAULT_IP_ADDRESS = data_file['host_conf'].get('DEFAULT_IP')

# Протокол JIM основные ключи:
ACTION = data_file['jit_key'].get('ACTION')
TIME = data_file['jit_key'].get('TIME')
USER = data_file['jit_key'].get('USER')
ACCOUNT_NAME = data_file['jit_key'].get('ACCOUNT_NAME')
MESSAGE_TEXT = data_file['jit_key'].get('MESSAGE_TEXT')

# Прочие ключи, используемые в протоколе
PRESENCE = data_file['other_key'].get('PRESENCE')
RESPONSE = data_file['other_key'].get('RESPONSE')
ERROR = data_file['other_key'].get('ERROR')
BAD_REQ = data_file['other_key'].get('BAD_REQ')

# Прочие настройки
MAX_CONNECT = data_file['settings'].get('MAX_CONNECT')
MAX_LENGTH = data_file['settings'].get('MAX_LENGTH')
ENCODING = data_file['settings'].get('ENCODING')

