# Различия в input между Python 2 и 3

# Python 2:
# name = raw_input("Введите имя: ")  # всегда строка
# number = input("Введите число: ")  # выполняет как eval()

# Python 3:
name = input("Введите имя: ")  # всегда строка
print(f"Тип имени: {type(name)}")

# Для числа нужно явное преобразование:
try:
    number = int(input("Введите число: "))
    print(f"Число: {number}, тип: {type(number)}")
except ValueError:
    print("Это не число!") 