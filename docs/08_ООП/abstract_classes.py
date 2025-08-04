# Примеры абстрактных классов
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14 * self.r ** 2

class Square(Shape):
    def __init__(self, a):
        self.a = a
    def area(self):
        return self.a ** 2

c = Circle(2)
s = Square(3)
print(c.area())
print(s.area()) 