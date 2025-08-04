# Примеры генераторов и итераторов
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up_to(3):
    print(num)

# Генераторное выражение
squares = (x**2 for x in range(5))
print(list(squares))

# Бесконечный генератор
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib), end=' ')
print() 