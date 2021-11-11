import unittest
import random

from app_client import prepare_request, validation_server_response
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
from common.methods_utils import make_date, GREETINGS


class ClientAppTest(unittest.TestCase):
    """ Тесты для двух функции клиента """
    true_data = make_date()
    random_greetings = random.choice(GREETINGS)

    true_request = {
        ACTION: PRESENCE,
        TIME: true_data,
        MESSAGE_TEXT: random_greetings,
        USER: {
            ACCOUNT_NAME: 'Anonymous'
        }
    }

    test_true = '200 : OK'
    test_error = f'400 : {BAD_REQ}'

    dict_test = {
        RESPONSE: 200
    }

    dict_test_1 = {
        RESPONSE: 200
    }

    dict_test_2 = {
        RESPONSE: 400,
        ERROR: BAD_REQ
    }

    def test_true_prepare_request(self):
        """ Проверка на верный запрос/сообщение """
        correct_call = prepare_request()
        correct_call[TIME] = self.true_data
        correct_call[MESSAGE_TEXT] = self.random_greetings
        self.assertEqual(correct_call, self.true_request)

    def test_true_response(self):
        """ Проверка на верный ответ """
        self.assertEqual(validation_server_response(self.dict_test),
                         self.test_true)

    def test_not_response(self):
        """ Отсутствие 'RESPONSE' """
        self.assertRaises(ValueError, validation_server_response, self.test_error)

    def test_bad_request(self):
        """ Проверка на 'Bad Request' """
        self.assertEqual(validation_server_response(self.dict_test_2),
                         self.test_error)


if __name__ == '__main__':
    unittest.main()
