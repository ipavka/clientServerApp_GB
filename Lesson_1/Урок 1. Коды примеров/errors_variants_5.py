"""Модуль errors_variants"""

# ошибка - преобразование кириллицы в байты
ERR_STR = 'Программа'
print(ERR_STR.encode('ascii'))

# ошибка - строку, преобразованную в байты в кодировке utf-8
# преобразуем в строку в кодировке ascii
ERR_STR = 'Программа'
ERR_STR_BYTES = ERR_STR.encode('utf-8')
ERR_STR = ERR_STR_BYTES.decode('ascii')
print(ERR_STR)

# ошибка - разные кодировки для преобразований
ERR_STR = 'Testování'
ERR_STR_BYTES = ERR_STR.encode('utf-16')
ERR_STR = ERR_STR_BYTES.decode('utf-8')
print(ERR_STR)
