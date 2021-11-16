"""Два декоратора"""


def make_ext(func):
    """Первый декоратор"""
    return lambda: "<ext_tag>" + func() + "</ext_tag>"


def make_int(func):
    """Второй декоратор"""
    return lambda: "<int_tag>" + func() + "</int_tag>"


@make_ext
@make_int
def my_func():
    """Какая-то логика"""
    return "Какой-то текст"

# порядок выполнения декораторов
# сначала make_ext, потом make_int
# func = make_ext(make_int(func))

# описание вызовов
"""
hello() = lambda : "<ext_tag>" + func() + "</ext_tag>" #  где func() ->
    lambda : "<int_tag>" + func() + "</int_tag>" # где func() ->
        return "Какой-то текст"
"""

print(my_func())
