# Примеры дескрипторов
class Descriptor:
    def __get__(self, obj, objtype=None):
        return 'значение дескриптора'

class MyClass:
    attr = Descriptor()

obj = MyClass()
print(obj.attr)

# Более сложный дескриптор
class Positive:
    def __get__(self, obj, objtype=None):
        return obj._value
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("Значение должно быть положительным")
        obj._value = value

class MyNumber:
    val = Positive()
    def __init__(self):
        self.val = 1

n = MyNumber()
print(n.val)
n.val = 5
print(n.val)
# n.val = -1  # ValueError 