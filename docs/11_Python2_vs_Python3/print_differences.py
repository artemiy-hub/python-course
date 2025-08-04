# Различия в print между Python 2 и 3

# Python 2 (НЕ РАБОТАЕТ в Python 3):
# print "Привет, мир!"
# print "Число:", 42

# Python 3:
print("Привет, мир!")
print("Число:", 42)

# Дополнительные возможности Python 3:
print("Один", "Два", "Три", sep="-")
print("Текст без переноса", end="")
print(" продолжение")

# Вывод в файл (Python 3):
with open("output.txt", "w") as f:
    print("В файл", file=f) 