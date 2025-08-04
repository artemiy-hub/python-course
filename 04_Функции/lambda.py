# Примеры анонимных функций (lambda)
f = lambda x, y: x + y
print(f(2, 3))  # 5

# Сортировка с lambda
lst = ["aaa", "b", "cccc"]
lst.sort(key=lambda s: len(s))
print(lst)

# Фильтрация с lambda
numbers = [1, 2, 3, 4, 5, 6]
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)

# Преобразование с lambda
squares = list(map(lambda x: x ** 2, numbers))
print(squares) 