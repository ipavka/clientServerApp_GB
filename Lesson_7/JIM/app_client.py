import socket
import json
import logging
import sys

from common.methods_utils import (
    connect_server,
    make_date,
    write_message,
    read_message,
    connect_client,
)
from common.config import (
    PRESENCE,
    TIME,
    USER,
    ACCOUNT_NAME,
    MESSAGE_TEXT,
    MESSAGE,
    ACTION,
    RESPONSE,
    ERROR,
    SENDER,
)
import logs.confs.client_log_config
from common.decor import log

logger = logging.getLogger('client')


@log
def validation_massage(message: dict) -> None:
    """ Обработка сообщений с сервера от других клиентов """
    if (ACTION in message
            and message[ACTION] == MESSAGE
            and SENDER in message
            and MESSAGE_TEXT in message):
        print(f"Пользователь {message[SENDER]} написал: {message[MESSAGE_TEXT]}")
        logger.info(f'Пользователь <{message[SENDER]}>'
                    f' отправил сообщение <{message[MESSAGE_TEXT]}>')
    else:
        logger.error(f"Некорректное сообщение...")


@log
def make_message(client: socket.socket, name: str = 'Anonymous') -> dict:
    """ Запрос сообщения от клиента и формирование ответа
        или закрытие сессии """
    input_message = input('Сообщение...')
    if input_message == 'q':
        client.close()
        logger.info('Клиент завершил работу...')
        sys.exit(0)
    result = {
        ACTION: MESSAGE,
        TIME: make_date(),
        ACCOUNT_NAME: name,
        MESSAGE_TEXT: input_message
    }
    logger.debug(f'Сообщение клиента: {result}')
    return result


@log
def prepare_request(name: str = 'Anonymous') -> dict:
    """ Функция формирует запрос/сообщение на сервер """
    result = {
        ACTION: PRESENCE,
        TIME: make_date(),
        USER: {
            ACCOUNT_NAME: name
        }
    }
    logger.debug(f"Сформировано сообщение {result} от клиента {name}")
    return result

@log
def validation_server_response(res: dict) -> str:
    """ Валидация ответа сервера """
    logger.debug(f"Проверяем что прислал сервер: {res}")
    if RESPONSE in res:
        if res[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {res[ERROR]}'
    raise ValueError


def run_client():
    """ Запуск клинта """
    host_server, port_server, operation_modes = connect_client()
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    client.connect((host_server, port_server))

    try:

        message_to_server = prepare_request()
        logger.debug(f"Отправка сообщение серверу: {message_to_server}")
        write_message(client, message_to_server)
        server_response = validation_server_response(read_message(client))
        logger.debug(f"Ответ сервера: {server_response}")

    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования сообщения...")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Некорректное сообщения от сервера: {e}")
        sys.exit(1)

    else:
        if operation_modes == 'write':
            print("Режим отправки сообщений, для выхода 'q'")
        else:
            print("Режим чтения сообщений")
        while True:
            if operation_modes == 'write':
                try:
                    write_message(client, make_message(client))
                except (ConnectionResetError, ConnectionError,
                        ConnectionAbortedError):
                    logger.critical("Соединение разорвано!")
                    sys.exit(1)

            if operation_modes == 'listen':
                try:
                    validation_massage(read_message(client))
                except (ConnectionResetError, ConnectionError,
                        ConnectionAbortedError):
                    logger.critical("Соединение разорвано!")
                    sys.exit(1)


if __name__ == '__main__':
    try:
        run_client()
    except ConnectionResetError:
        logger.critical(
            f"Сервер {connect_server()} отверг запрос на подключение")
        exit()
