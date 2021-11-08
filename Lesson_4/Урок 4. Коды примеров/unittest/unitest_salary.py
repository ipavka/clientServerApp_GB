"""
Фамилия     Имя         Часов   Ставка
Иванов      Иван        45      400
Докукин     Филимон     20      1000
Ромашкин    Сидор       45      500
"""

from collections import namedtuple
import unittest

Salary = namedtuple('Salary', ('surname', 'name', 'worked', 'rate'))


def get_salary(line):
    """Вычисление зарплаты работника"""

    line = line.split()
    if line:
        data = Salary(*line)
        fio = ' '.join((data.surname, data.name))
        salary = int(data.worked) * int(data.rate)
        res = (fio, salary)
    else:
        res = ()
    return res


class TestSalary(unittest.TestCase):
    """class"""

    def test_get_salary_summ(self):
        """test1"""
        self.assertEqual(get_salary('Лютиков   Руслан     60    1000'),
                         ('Лютиков Руслан', 60000))

    def test_get_salary_fio(self):
        """test2"""
        self.assertEqual(get_salary('Лютиков   Руслан     60    1000')[0],
                         'Лютиков Руслан')

    def test_get_salary_empty(self):
        """test3"""
        self.assertEqual(get_salary(''), ())


if __name__ == "__main__":
    unittest.main()
