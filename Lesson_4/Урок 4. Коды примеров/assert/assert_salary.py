"""
Фамилия     Имя         Часов   Ставка
Иванов      Иван        45      400
Докукин     Филимон     20      1000
Ромашкин    Сидор       45      500
"""

from collections import namedtuple


Salary = namedtuple('Salary', ('surname', 'name', 'worked', 'rate'))

# Иванов Иван 45 400
def get_salary(line):
    """
    Вычисление зарплаты работника
    """
    line = line.split()

    if line:
        data = Salary(*line)
        # data -> Salary(surname='Лютиков', name='Руслан', worked='60', rate='1000')
        fio = ' '.join((data.surname, data.name))
        salary = int(data.worked) * int(data.rate)
        res = (fio, salary)
        # res -> ('Лютиков Руслан', 60000)
    else:
        res = ()
    return res


def test_get_salary_summ():
    """тест 1"""
    assert get_salary('Лютиков Руслан 60 1000')[1] == \
           60000, 'Неверная сумма'


def test_get_salary_fio():
    """тест 2"""
    assert get_salary('Лютиков Руслан 60 1000')[0] == \
           'Лютиков Руслан', 'Неверное имя'


def test_get_salary_empty():
    """тест 3"""
    assert get_salary('') == (), 'Непустые данные'


def test_get_salary_wrong_format():
    """тест 4"""
    assert get_salary(' ') == (), 'Непустые данные'


if __name__ == "__main__":
    test_get_salary_summ()
    test_get_salary_fio()
    test_get_salary_empty()
    test_get_salary_wrong_format()
