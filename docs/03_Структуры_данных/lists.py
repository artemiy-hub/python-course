# Примеры работы со списками
lst = [1, 2, 3, "a", [4, 5]]
print(lst)
lst.append(6)
print(lst)
lst[0] = 10
print(lst)
print(lst[4][1])  # 5
print(lst[-2:])   # [[4, 5], 6]

# Основные методы списков
lst = [3, 1, 2]
lst.sort()
print(lst)
lst.reverse()
print(lst)
lst.pop()
print(lst)
lst.insert(1, 100)
print(lst) 