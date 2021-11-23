import unittest


from common.methods_utils import get_ip_and_port
from common.config import (
    DEFAULT_IP_ADDRESS,
    DEFAULT_PORT
)

class TestsMethodsUtils(unittest.TestCase):
    """ Класс для тестирования общих методов"""

    def test_get_ip_and_port(self):
        self.assertEqual(get_ip_and_port(), (DEFAULT_IP_ADDRESS, DEFAULT_PORT))


if __name__ == '__main__':
    unittest.main()

