# Примеры контекстных менеджеров
class MyContext:
    def __enter__(self):
        print("Вход в контекст")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Выход из контекста")

with MyContext():
    print("Внутри блока")

# Контекстный менеджер с помощью contextlib
from contextlib import contextmanager

@contextmanager
def my_context():
    print("Вход")
    try:
        yield "значение"
    finally:
        print("Выход")

with my_context() as value:
    print(f"Значение: {value}") 