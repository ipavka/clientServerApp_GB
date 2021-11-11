import socket
import random
import json
import logging

from common.methods_utils import (
    connect_server,
    read_message,
    write_message,
    GREETINGS,
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
)
import logs.confs.server_log_config

logger = logging.getLogger('server')

def validation_and_response(res: dict) -> dict:
    """ Валидация и ответ сообщения клиента """
    logger.debug(f"Проверяем что прислал клиент: {res}")
    if (ACTION in res
            and res[ACTION] == PRESENCE
            and TIME in res
            and USER in res
            and res[USER][ACCOUNT_NAME] == 'Anonymous'):
        result = {
            RESPONSE: 200,
            MESSAGE_TEXT: random.choice(GREETINGS),
        }
        logger.debug(f"Ответ сервера 200 {result}")
        return result

    else:
        result = {
            RESPONSE: 400,
            ERROR: BAD_REQ
        }
        logger.warning(f"Ответ сервера 400 {result}")
        return result


def start_server():
    """ Запуск Сервера """
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    server.bind(connect_server())
    server.listen(MAX_CONNECT)

    while True:
        conn, address = server.accept()
        logger.info(f"Открытие соединения с {address}")
        try:
            client_message = read_message(conn)
            logger.debug(f"Сообщение от клиента: {client_message}")

            server_response = validation_and_response(client_message)
            logger.debug(f"Ответ клиенту: {client_message}")
            write_message(conn, server_response)

            logger.debug(f"Закрытие соединения с: {address}")
            conn.close()
        except (ValueError, json.JSONDecodeError):
            logger.warning(f"Ошибка декодирования сообщения клиента {address}")


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        logger.debug(f"Подключение остановлено пользователем с клавиатуры")
        exit()
