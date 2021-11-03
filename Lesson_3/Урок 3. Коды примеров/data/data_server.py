""" Программа сервера для получения приветствия от клиента и отправки ответа """

from socket import socket, AF_INET, SOCK_STREAM

SERV_SOCK = socket(AF_INET, SOCK_STREAM)
SERV_SOCK.bind(('', 8007))
SERV_SOCK.listen(1)

try:
    while True:
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()
        # попробуйте уменьшить размер пакета и передать длинное сообщение
        # аргумент устанавливает максимальное количество байтов в сообщении.
        #  Если столько байт, сколько указано, не пришло, а
        #  какие-то данные уже появились, она всё равно возвращает всё, что имеется
        DATA = CLIENT_SOCK.recv(4096)
        print(f"Сообщение: {DATA.decode('utf-8')} было отправлено клиентом: {ADDR})")
        MSG = f'Привет, клиент'
        CLIENT_SOCK.send(MSG.encode('utf-8'))
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()
