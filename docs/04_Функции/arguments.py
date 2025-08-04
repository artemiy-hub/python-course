# Примеры различных типов аргументов
def func(a, b=10, *args, **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")

func(1)
func(1, 2, 3, 4, x=5, y=6)

# Позиционные и именованные аргументы
def person(name, age, city):
    print(f"{name}, {age} лет, из {city}")

person("Анна", 25, "Москва")  # позиционные
person(name="Иван", age=30, city="СПб")  # именованные
person("Петр", city="Казань", age=28)  # смешанные 