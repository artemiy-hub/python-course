# Примеры работы с множествами
s = {1, 2, 3, 2}
print(s)  # {1, 2, 3}
s.add(4)
print(s)
s.remove(2)
print(s)
print(3 in s)  # True

# Операции с множествами
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)  # объединение
print(a & b)  # пересечение
print(a - b)  # разность 