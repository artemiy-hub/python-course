# Примеры обработки исключений
try:
    x = int(input("Введите число: "))
    print(10 / x)
except ValueError:
    print("Это не число!")
except ZeroDivisionError:
    print("Деление на ноль!")
else:
    print("Ошибок не было!")
finally:
    print("Блок finally всегда выполняется") 