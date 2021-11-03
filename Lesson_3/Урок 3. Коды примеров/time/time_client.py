"""Программа клиента времени"""

from socket import socket, AF_INET, SOCK_STREAM

try:
    while True:
        CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
        # коннектимся с сервером
        CLIENT_SOCK.connect(('localhost', 8888))
        # попробуйте уменьшить размер пакета и передать длинное сообщение
        # аргумент устанавливает максимальное количество байтов в сообщении.
        #  Если столько байт, сколько указано, не пришло, а
        #  какие-то данные уже появились, она всё равно возвращает всё, что имеется
        TIME_BYTES = CLIENT_SOCK.recv(1024)
        CLIENT_SOCK.close()
        print(f"Текущее время: {TIME_BYTES.decode('utf-8')}")
finally:
    CLIENT_SOCK.close()
