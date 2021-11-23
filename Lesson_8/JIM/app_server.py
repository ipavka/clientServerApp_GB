import socket
import logging
import select

from common.methods_utils import (
    connect_server,
    read_message,
    write_message,
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
    RECIPIENT,
    EXIT
)
import logs.confs.server_log_config
from common.decor import log

logger = logging.getLogger('server')


@log
def validation_and_response(res: dict,
                            arr_massage: list,
                            client: socket.socket,
                            in_clients: list,
                            name_data: dict):
    """ Валидация и ответ сообщения клиента """
    logger.debug(f"Проверяем что прислал клиент: {res}")
    # Простое приветствие
    if (ACTION in res
            and res[ACTION] == PRESENCE
            and TIME in res
            and USER in res):
        if res[USER][ACCOUNT_NAME] not in name_data.keys():
            name_data[res[USER][ACCOUNT_NAME]] = client

            result = {
                RESPONSE: 200,
            }
            logger.warning(f"Ответ сервера {result}")
            write_message(client, result)  # отправляем сообщение
        else:
            result = {
                RESPONSE: 400,
                ERROR: "Такое имя уже есть!!!"
            }
            logger.warning(f"Ответ сервера {result}")
            write_message(client, result)  # отправляем сообщение
            in_clients.remove(client)
            client.close()

        return

    # Есть сообщение от клиента, добавляем в массив сообщение очереди
    elif (ACTION in res
          and res[ACTION] == MESSAGE
          and RECIPIENT in res
          and TIME in res
          and SENDER in res
          and MESSAGE_TEXT in res):
        arr_massage.append(res)
        return

    # Выход клиента
    elif (ACTION in res
          and res[ACTION] == EXIT
          and ACCOUNT_NAME in res):
        in_clients.remove(name_data[res[ACCOUNT_NAME]])
        name_data[res[ACCOUNT_NAME]].close()
        del name_data[res[ACCOUNT_NAME]]
        return

    else:
        result = {
            RESPONSE: 400,
            ERROR: BAD_REQ
        }
        logger.warning(f"Ответ сервера 400 {result}")
        write_message(client, result)  # отправляем сообщение
        return


@log
def send_message(message: dict, name_dict: dict, wait_list: list) -> None:
    """ Пишем сообщения выбранным пользователям """
    if (message[RECIPIENT] in name_dict
            and name_dict[message[RECIPIENT]] in wait_list):
        write_message(name_dict[message[RECIPIENT]], message)
        logger.info(f"Сообщение для {message[RECIPIENT]} от {message[SENDER]}")
    elif (message[RECIPIENT] in name_dict
          and name_dict[message[RECIPIENT]] not in wait_list):
        raise ConnectionError
    else:
        logger.error(f"Нет такого пользователя {message[RECIPIENT]} "
                     f"некому отправлять...")


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

    #  Хранение сокетов и соответствующих имен
    data_set = {}

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
            inputs_clients.append(
                conn)  # добавляем в массив новое подключение клиента

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
                    #  Отправляем на валидацию и дальнейшую отправку, в то числе
                    #  сокет и его имя(имя клиента)
                    validation_and_response(read_message(read),
                                            arr_massage,
                                            read,
                                            inputs_clients,
                                            data_set)
                except Exception:
                    logger.info(f"Клиент {read.getpeername()} отключен...")
                    inputs_clients.remove(
                        read)  # удаляем клиента из общего массива

        for message in arr_massage:
            try:
                send_message(message, data_set, sends)
            except Exception:
                logger.info(f"Нет связи с клиентом {message[RECIPIENT]}")
                inputs_clients.remove(data_set[message[RECIPIENT]])
                del data_set[message[RECIPIENT]]
        arr_massage.clear()


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        logger.debug(f"Подключение остановлено пользователем с клавиатуры")
        exit()
