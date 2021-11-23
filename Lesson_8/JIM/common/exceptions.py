""" Модуль для собственных исключений, пока не пригодился,
 оставлю как заглушку """

class NotIPOrPortError(Exception):
    """ Отсутствие  ip или порта """
    pass

class IncorrectMode(Exception):
    """ Некорректный режим работы клиента"""
    def __str__(self):
        return f"Неверный режим работы клиента, возможные варианты: listen | write"


class IncorrectSocketMessage(Exception):
    """ Ошибка сообщения сокета """
    def __str__(self):
        return f"Неверное сообщение!"
