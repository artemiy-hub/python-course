# Профилирование и анализ производительности
import cProfile
import pstats
import timeit
import time
from functools import wraps

# Декоратор для измерения времени
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} выполнена за {end - start:.6f} секунд")
        return result
    return wrapper

@timer
def slow_function():
    """Медленная функция для демонстрации"""
    total = 0
    for i in range(1000000):
        total += i ** 2
    return total

@timer
def fast_function():
    """Быстрая функция для сравнения"""
    return sum(i ** 2 for i in range(1000000))

# Сравнение производительности
print("=== Сравнение функций ===")
result1 = slow_function()
result2 = fast_function()

# Использование timeit
print("\n=== Детальное измерение с timeit ===")
slow_time = timeit.timeit(slow_function, number=1)
fast_time = timeit.timeit(fast_function, number=1)
print(f"Медленная функция: {slow_time:.6f} сек")
print(f"Быстрая функция: {fast_time:.6f} сек")
print(f"Ускорение: {slow_time / fast_time:.2f}x")

# Профилирование с cProfile
def fibonacci_slow(n):
    if n < 2:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

def fibonacci_fast(n, memo={}):
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fibonacci_fast(n-1, memo) + fibonacci_fast(n-2, memo)
    return memo[n]

print("\n=== Профилирование cProfile ===")
print("Медленный Фибоначчи:")
pr = cProfile.Profile()
pr.enable()
result = fibonacci_slow(30)
pr.disable()

stats = pstats.Stats(pr)
stats.sort_stats('cumulative')
stats.print_stats(10)  # топ 10 функций

print(f"\nРезультат: {result}")

print("\nБыстрый Фибоначчи:")
start = time.perf_counter()
result = fibonacci_fast(30)
end = time.perf_counter()
print(f"Время: {end - start:.6f} сек")
print(f"Результат: {result}")

# Анализ сложности алгоритмов
def linear_search(arr, target):
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

print("\n=== Сравнение алгоритмов поиска ===")
data = list(range(100000))
target = 99999

linear_time = timeit.timeit(lambda: linear_search(data, target), number=10)
binary_time = timeit.timeit(lambda: binary_search(data, target), number=10)

print(f"Линейный поиск: {linear_time:.6f} сек")
print(f"Бинарный поиск: {binary_time:.6f} сек")
print(f"Ускорение: {linear_time / binary_time:.0f}x") 