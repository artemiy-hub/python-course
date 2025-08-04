# Пример собственного исключения
class MyError(Exception):
    pass

def check_positive(x):
    if x < 0:
        raise MyError("Число должно быть положительным!")

try:
    check_positive(-1)
except MyError as e:
    print(e) 