"""Модуль error_handling_mechanisms"""

# обработка ошибки кодирования с заменой символа знаком вопроса
HANDL_ERR = 'Testování'
HANDL_ERR_BYTES = HANDL_ERR.encode('ascii', 'replace')
print(HANDL_ERR_BYTES)

# обработка ошибки кодирования с заменой символа его именем
HANDL_ERR_BYTES = HANDL_ERR.encode('ascii', 'namereplace')
print(HANDL_ERR_BYTES)

# игнорирование ошибки при кодировании
HANDL_UNICODE = 'Testování'
HANDL_BYTES = HANDL_UNICODE.encode('ascii', 'ignore')
print(HANDL_BYTES)

# игнорирование лшибки при декодировании
HANDL_STR = 'Testování'
HANDL_STR_BYTES = HANDL_STR.encode('utf-8')
print(HANDL_STR_BYTES)
HANDL_STR = HANDL_STR_BYTES.decode('ascii', 'ignore')
print(HANDL_STR)

# замена ошибки при декодировании
HANDL_STR = 'Testování'
HANDL_STR_BYTES = HANDL_STR.encode('utf-8')
HANDL_STR = HANDL_STR_BYTES.decode('ascii', 'replace')
print(HANDL_STR)
