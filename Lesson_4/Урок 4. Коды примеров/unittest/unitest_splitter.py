"""unittest_splitter"""

import unittest


def split(line, types=None, delimiter=None):
    """ Разбивает текстовую строку и при необходимости
        выполняет преобразование типов.
        Например:
        >>> split('GOOG 100 490.50')
        ['GOOG', '100', '490.50']
        >>> split('GOOG 100 490.50',[str, int, float])
        ['GOOG', 100, 490.5]
        >>>
        По умолчанию разбиение производится по пробельным символам,
        но имеется возможность указать другой символ-разделитель, в виде именованного аргумента:

        >>> split('GOOG,100,490.50',delimiter=',')
        ['GOOG', '100', '490.50']
        >>>
    """
    fields = line.split(delimiter)
    if types:
        fields = [ty(val) for ty, val in zip(types, fields)]
    return fields

#print(split('GOOG 100 490.50'))
#print(split('GOOG 100 490.50', [str, int, float]))
#print(split('GOOG,100,490.50', [str, int, float], delimiter=','))


# Модульные тесты
# (удобно выносить тесты в отдельный модуль, в примерах этого не делается для упрощения)
class TestSplitFunction(unittest.TestCase):
    """class"""
    def setUp(self):
        """Выполнить настройку тестов (если необходимо)"""
        pass

    def tearDown(self):
        """Выполнить завершающие действия (если необходимо)"""
        pass

    def testsimplestring(self):
        """test1"""
        res = split('GOOG 100 490.50')
        self.assertEqual(res, ['GOOG', '100', '490.50'])

    def testtypeconvert(self):
        """test2"""
        res = split('GOOG 100 490.50', [str, int, float])
        self.assertEqual(res, ['GOOG', 100, 490.5])

    def testdelimiter(self):
        """test3"""
        res = split('GOOG,100,490.50', delimiter=',')
        self.assertEqual(res, ['GOOG', '100', '490.50'])


# Запустить тестирование
if __name__ == '__main__':
    unittest.main()
