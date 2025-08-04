# Примеры наследования и полиморфизма
class Animal:
    def speak(self):
        print("Животное издаёт звук")

class Dog(Animal):
    def speak(self):
        print("Гав!")

class Cat(Animal):
    def speak(self):
        print("Мяу!")

a = Animal()
d = Dog()
c = Cat()

for obj in (a, d, c):
    obj.speak() 