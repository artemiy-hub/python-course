# Примеры метаклассов
class MyMeta(type):
    def __new__(cls, name, bases, dct):
        dct['id'] = 123
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=MyMeta):
    pass

print(MyClass.id)

# Более сложный пример метакласса
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value

s1 = Singleton(1)
s2 = Singleton(2)
print(s1 is s2)  # True
print(s1.value)  # 1 