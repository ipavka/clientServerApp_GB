import socket
import logging
import select

from common.methods_utils import (
    connect_server,
    read_message,
    write_message,
    make_date,
)
from common.config import (
    MAX_CONNECT,
    ACTION,
    PRESENCE,
    USER,
    ACCOUNT_NAME,
    TIME,
    RESPONSE,
    ERROR,
    BAD_REQ,
    MESSAGE_TEXT,
    MESSAGE,
    SENDER,
)
import logs.confs.server_log_config
from common.decor import log

logger = logging.getLogger('server')


@log
def validation_and_response(res: dict,
                            arr_massage: list,
                            client: socket.socket):
    """ Валидация и ответ сообщения клиента """
    logger.debug(f"Проверяем что прислал клиент: {res}")
    # Простое приветствие
    if (ACTION in res
            and res[ACTION] == PRESENCE
            and TIME in res
            and USER in res
            and res[USER][ACCOUNT_NAME] == 'Anonymous'):
        result = {
            RESPONSE: 200,
        }
        logger.debug(f"Ответ сервера 200 {result}")
        write_message(client, result)  # отправляем сообщение
        return

    # Есть сообщение от клиента, добавляем в массив сообщение и имя клиента
    elif (ACTION in res
          and res[ACTION] == MESSAGE
          and TIME in res
          and MESSAGE_TEXT in res):
        arr_massage.append((res[ACCOUNT_NAME], res[MESSAGE_TEXT]))
        return

    else:
        result = {
            RESPONSE: 400,
            ERROR: BAD_REQ
        }
        logger.warning(f"Ответ сервера 400 {result}")
        write_message(client, result)  # отправляем сообщение
        return


def start_server():
    """ Запуск Сервера """
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    server.bind(connect_server())
    server.settimeout(0.5)  # timeout проверки

    inputs_clients = []  # массив с клиентам
    arr_massage = []  # массив с сообщениями от клиентов
    server.listen(MAX_CONNECT)

    print("Сервер запущен")
    logger.info(f'Старт сервера по адресу <{connect_server()[0]}> '
                f' На порту <{connect_server()[1]}>')

    while True:
        try:
            conn, address = server.accept()
        except OSError:
            pass  # timeout вышел
        else:
            print(F"Соединение с клиентом по адресу {address}")
            logger.info(f"Открытие соединения с {address}")
            inputs_clients.append(conn)  # добавляем в массив новое подключение клиента

        reads = []  # сокеты, готовые к чтению
        sends = []  # сокеты, которые хотят что то написать
        excepts = []  # исключения

        try:
            if inputs_clients:  # если есть подключение
                reads, sends, excepts = select.select(
                    inputs_clients,
                    inputs_clients,
                    [], 0)
                logger.debug(
                    f"Есть клиент, смотрим что он хочет {inputs_clients}")
        except OSError:
            pass

        if reads:  # Если есть сообщения
            for read in reads:
                try:
                    #  Отправляем на валидацию и дальнейшую отправку
                    validation_and_response(read_message(read),
                                            arr_massage,
                                            read)
                except Exception:
                    logger.info(f"Клиент {read.getpeername()} отключен...")
                    inputs_clients.remove(
                        read)  # удаляем клиента из общего массива

        if arr_massage and sends:  # Есть сообщения и ожидающие клиенты
            #  Формируем сообщение в словаре
            message = {
                ACTION: MESSAGE,
                SENDER: arr_massage[0][0],
                TIME: make_date(),
                MESSAGE_TEXT: arr_massage[0][1]
                }
            del arr_massage[0]
            #  рассылаем ждущим клиентам
            for send in sends:
                try:
                    write_message(send, message)
                except Exception:
                    logger.info(f"Клиент отключен")


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        logger.debug(f"Подключение остановлено пользователем с клавиатуры")
        exit()
