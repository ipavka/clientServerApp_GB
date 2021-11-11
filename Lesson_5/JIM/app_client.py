import socket
import random
import json
import logging

from common.methods_utils import (
    connect_server,
    make_date,
    write_message,
    read_message,
    GREETINGS,
)
from common.config import (
    PRESENCE,
    TIME,
    USER,
    ACCOUNT_NAME,
    MESSAGE_TEXT,
    ACTION,
    RESPONSE,
    ERROR,
)
import logs.confs.client_log_config

logger = logging.getLogger('client')


def prepare_request(name: str = 'Anonymous') -> dict:
    """ Функция формирует запрос/сообщение на сервер """
    result = {
        ACTION: PRESENCE,
        TIME: make_date(),
        MESSAGE_TEXT: random.choice(GREETINGS),
        USER: {
            ACCOUNT_NAME: name
        }
    }
    logger.debug(f"Сформировано сообщение {result} от клиента {name}")
    return result


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
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    client.connect(connect_server())

    try:
        message_to_server = prepare_request()
        logger.debug(f"Отправка сообщение серверу: {message_to_server}")
        write_message(client, message_to_server)
        server_response = validation_server_response(read_message(client))
        logger.debug(f"Ответ сервера: {server_response}")

    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования сообщения...")
    except ValueError as e:
        logger.error(f"Некорректное сообщения от сервера: {e}")


if __name__ == '__main__':
    try:
        run_client()
    except ConnectionResetError:
        logger.critical(
            f"Сервер {connect_server()} отверг запрос на подключение")
        exit()
