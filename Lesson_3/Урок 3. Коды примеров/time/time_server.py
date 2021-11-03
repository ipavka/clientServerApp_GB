"""Программа сервера времени"""

from socket import socket, AF_INET, SOCK_STREAM
import time

# создаем объект серверного сокета
# сетевой, потоковый (TCP)
SERV_SOCK = socket(AF_INET, SOCK_STREAM)

# связываем сокет с адресом и портом
# именно через них клиент подключится к серверу
SERV_SOCK.bind(('', 8888))

# listen - сокет готов к прослушиванию.
# Метод принимает один аргумент -
# максимальное количество подключений в очереди.
SERV_SOCK.listen(1)
# попробуйте также поставить SERV_SOCK.listen(6)
# запустить лаунчер и сравнить

try:
    while True:
        # принимает подключения клиентов
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()
        print(f'Получен запрос на соединение от клиента с адресом и портом: {ADDR}')
        TIMESTR = time.ctime(time.time()) + "\n"
        # отправляем клиенту сообщение
        CLIENT_SOCK.send(TIMESTR.encode('utf-8'))
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()
