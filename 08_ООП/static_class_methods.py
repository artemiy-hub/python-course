# Примеры статических и классовых методов
class Math:
    @staticmethod
    def add(a, b):
        return a + b
    @classmethod
    def info(cls):
        print(f"Это класс {cls.__name__}")

print(Math.add(2, 3))
Math.info() 