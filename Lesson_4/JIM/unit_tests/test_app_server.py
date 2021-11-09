import unittest
import random

from app_server import validation_and_response
from common.config import (
    RESPONSE,
    ERROR,
    BAD_REQ,
    ACTION,
    PRESENCE,
    TIME,
    MESSAGE_TEXT,
    USER,
    ACCOUNT_NAME,
)
from common.methods_utils import GREETINGS


class ServerAppTest(unittest.TestCase):
    """ Тесты для одной функции сервера """
    # генерация случайного приветствия
    random_greetings = random.choice(GREETINGS)

    dict_true = {
        RESPONSE: 200,
        MESSAGE_TEXT: random_greetings,
    }
    error_dict = {
        RESPONSE: 400,
        ERROR: BAD_REQ
    }

    dict_test_1 = {
        ACTION: PRESENCE,
        TIME: '2021/11/09 13:18:05',
        MESSAGE_TEXT: 'Hello',
        USER: {ACCOUNT_NAME: 'Anonymous'}
    }

    dict_test_2 = {
        ACTION: 'jim',
        TIME: '2021/11/09 13:18:05',
        MESSAGE_TEXT: 'Привет Сервер',
        USER: {ACCOUNT_NAME: 'Anonymous'}
    }

    dict_test_3 = {
        TIME: '2021/11/09 13:18:05',
        MESSAGE_TEXT: 'Привет Сервер',
        USER: {ACCOUNT_NAME: 'Anonymous'}
    }

    dict_test_4 = {
        ACTION: PRESENCE,
        MESSAGE_TEXT: 'Привет Сервер',
        USER: {ACCOUNT_NAME: 'Anonymous'}
    }

    dict_test_5 = {
        ACTION: PRESENCE,
        TIME: '2021/11/09 13:18:05',
        MESSAGE_TEXT: 'Hello',
    }

    dict_test_6 = {
        ACTION: PRESENCE,
        TIME: '2021/11/09 13:18:05',
        MESSAGE_TEXT: 'Hello',
        USER: {ACCOUNT_NAME: 'max'}
    }

    def test_empty_request(self):
        """ Пустой запрос """
        self.assertEqual(validation_and_response({}), self.error_dict)

    def test_true_request(self):
        """ Верный запрос """
        # для совпадения случайное приветствие генерируем при вызове
        correct_call = validation_and_response(self.dict_test_1)
        correct_call[MESSAGE_TEXT] = self.random_greetings
        self.assertEqual(correct_call, self.dict_true)

    def test_wrong_action(self):
        """ Неверное значение ACTION """
        self.assertEqual(validation_and_response(
            self.dict_test_2), self.error_dict)

    def test_not_action(self):
        """ Отсутствие ACTION """
        self.assertEqual(validation_and_response(
            self.dict_test_3), self.error_dict)

    def test_not_time(self):
        """ Отсутствие TIME """
        self.assertEqual(validation_and_response(
            self.dict_test_4), self.error_dict)

    def test_not_user(self):
        """ Отсутствие USER """
        self.assertEqual(validation_and_response(
            self.dict_test_5), self.error_dict)

    def test_wrong_time(self):
        """ Неверное значение USER """
        self.assertEqual(validation_and_response(
            self.dict_test_6), self.error_dict)


if __name__ == '__main__':
    unittest.main()
