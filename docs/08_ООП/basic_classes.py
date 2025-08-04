# Примеры базовых классов и объектов
class Person:
    def __init__(self, name):
        self.name = name
    def say_hello(self):
        print(f"Привет, меня зовут {self.name}")

p = Person("Анна")
p.say_hello()
print(type(p)) 