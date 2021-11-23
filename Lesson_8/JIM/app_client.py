import socket
import json
import logging
import sys
import threading
import time

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
    MANUAL,
    RECIPIENT,
    EXIT
)
from common.exceptions import IncorrectSocketMessage
import logs.confs.client_log_config
from common.decor import log

logger = logging.getLogger('client')


@log
def message_exit(account_name: str) -> dict:
    """ Формируем сообщение о выходе в сокет """
    result = {
        ACTION: EXIT,
        TIME: make_date(),
        ACCOUNT_NAME: account_name
    }
    return result


@log
def server_message(client: socket.socket, user_name: str) -> None:
    """ Прием и обработка сообщений пользователя с сервера """
    while True:
        try:
            input_massage = read_message(client)
            if (ACTION in input_massage
                    and input_massage[ACTION] == MESSAGE
                    and SENDER in input_massage
                    and RECIPIENT in input_massage
                    and MESSAGE_TEXT in input_massage
                    and input_massage[RECIPIENT] == user_name):
                print(
                    f"\nСообщение < {input_massage[MESSAGE_TEXT]} > от пользователя "
                    f"{input_massage[SENDER]}")

                logger.info(
                    f"Сообщение {input_massage[MESSAGE_TEXT]} от пользователя "
                    f"{input_massage[SENDER]}")

        except IncorrectSocketMessage:
            logger.error(f"Ошибка декодирования сообщения!")
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            logger.critical(f"Ошибка соединения с сервером!!!")
            break


@log
def make_message(client: socket.socket, user_name: str = 'Anon'):
    """ Формируем сообщение от клиента для выбранного адресанта и отправляем
     на сервер """
    target_user = input('Имя получателя... ')
    input_message = input('Сообщение... ')
    result = {
        ACTION: MESSAGE,
        SENDER: user_name,
        RECIPIENT: target_user,
        TIME: make_date(),
        MESSAGE_TEXT: input_message
    }
    logger.debug(f"Пользователь {user_name} сформировал сообщение {result}")
    try:
        write_message(client, result)
        logger.info(
            f"Отправлено сообщение пользователю {target_user}")
    except Exception:
        logger.critical(f"Сервер не доступен")
        sys.exit(1)


@log
def interface_client(client: socket.socket, user: str) -> None:
    """ Взаимодействие с клиентом """
    print(MANUAL)  # Подсказки команд
    while True:
        input_command = input("Введите команду: ")
        if input_command == "m":
            make_message(client, user)
        elif input_command == "h":
            print(MANUAL)
        elif input_command == "q":
            write_message(client, message_exit(user))
            print("Клиент завершил работу")
            logger.info('Клиент завершил работу...')
            time.sleep(0.5)
            break

        else:
            print(f"Неверная команда\n"
                  f"{MANUAL}")


@log
def prepare_request(name: str) -> dict:
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
    host_server, port_server, name_client = connect_client()
    print(f"Клиентский модуль клиента: < {name_client} >")
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    client.connect((host_server, port_server))
    logger.info(f"Запуск Клиента < {name_client} "
                f"хост: <{host_server}> порт: <{port_server}>")

    try:
        message_to_server = prepare_request(name_client)
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
        # Процесс приема сообщений
        recipient = threading.Thread(target=server_message,
                                     args=(client, name_client))
        recipient.daemon = True
        recipient.start()

        # Логика взаимодействия пользователя
        client_logic = threading.Thread(target=interface_client,
                                        args=(client, name_client))
        client_logic.daemon = True
        client_logic.start()
        logger.debug('что то про процессы')

        while True:
            #  Проверка работают ли потоки
            time.sleep(1)
            if recipient.is_alive() and client_logic.is_alive():
                continue
            break


if __name__ == '__main__':
    try:
        run_client()
    except ConnectionResetError:
        logger.critical(
            f"Сервер {connect_server()} отверг запрос на подключение")
        exit()
