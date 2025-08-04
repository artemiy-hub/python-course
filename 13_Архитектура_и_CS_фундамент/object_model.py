# Объектная модель Python
import sys

# Исследование PyObject
class MyClass:
    class_var = "class variable"
    
    def __init__(self, value):
        self.value = value
    
    def method(self):
        return f"Method called with {self.value}"

obj = MyClass(42)

print("=== Исследование объектов ===")
print(f"Тип объекта: {type(obj)}")
print(f"Тип типа: {type(type(obj))}")
print(f"ID объекта: {id(obj)}")
print(f"Размер объекта: {sys.getsizeof(obj)} байт")

# MRO (Method Resolution Order)
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

print("\n=== Method Resolution Order ===")
print(f"MRO для D: {[cls.__name__ for cls in D.__mro__]}")
print(f"D().method(): {D().method()}")

# Метаклассы в действии
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value

print("\n=== Метаклассы (Singleton) ===")
s1 = Singleton(1)
s2 = Singleton(2)
print(f"s1 is s2: {s1 is s2}")
print(f"s1.value: {s1.value}")
print(f"s2.value: {s2.value}")

# Дескрипторы
class LoggedAttribute:
    def __init__(self, name):
        self.name = name
        self._value = None
    
    def __get__(self, obj, objtype=None):
        print(f"Получение {self.name}")
        return self._value
    
    def __set__(self, obj, value):
        print(f"Установка {self.name} = {value}")
        self._value = value
    
    def __delete__(self, obj):
        print(f"Удаление {self.name}")
        self._value = None

class MyClass2:
    x = LoggedAttribute("x")
    
    def __init__(self):
        self.x = 0

print("\n=== Дескрипторы ===")
obj2 = MyClass2()
obj2.x = 42
print(f"Значение: {obj2.x}")

# Slots для экономии памяти
class WithSlots:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

print("\n=== Slots vs обычные классы ===")
with_slots = WithSlots(1, 2)
without_slots = WithoutSlots(1, 2)

print(f"С slots: {sys.getsizeof(with_slots)} байт")
print(f"Без slots: {sys.getsizeof(without_slots)} байт")
print(f"Экономия: {sys.getsizeof(without_slots) - sys.getsizeof(with_slots)} байт")

# try:
#     with_slots.z = 3  # Ошибка: нет слота 'z'
# except AttributeError as e:
#     print(f"Ошибка slots: {e}")

# Исследование атрибутов
print("\n=== Атрибуты объекта ===")
print(f"Атрибуты объекта: {vars(obj)}")
print(f"Атрибуты класса: {vars(MyClass)}")
print(f"Все атрибуты: {dir(obj)}")

# Магические методы
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

print("\n=== Магические методы ===")
p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2
print(f"p1: {p1}")
print(f"p2: {p2}")
print(f"p1 + p2: {p3}")
print(f"p1 == Point(1, 2): {p1 == Point(1, 2)}")
print(f"hash(p1): {hash(p1)}")

# Можно использовать Point как ключ словаря
points_dict = {p1: "первая точка", p2: "вторая точка"}
print(f"Словарь точек: {points_dict}")

# Исследование типов
print("\n=== Типы данных ===")
for obj in [42, 3.14, "hello", [1, 2, 3], {"a": 1}]:
    print(f"{obj} -> {type(obj).__name__} -> {type(type(obj)).__name__}") 