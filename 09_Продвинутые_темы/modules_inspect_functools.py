# Примеры модулей inspect, functools, itertools
import inspect
import functools
import itertools

def example_function(x):
    """Пример функции"""
    return x * 2

# inspect
print(inspect.getsource(example_function))
print(inspect.signature(example_function))

# functools
@functools.lru_cache(maxsize=2)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))

# itertools
for x in itertools.combinations([1, 2, 3], 2):
    print(x)

# cycle
cycle_iter = itertools.cycle([1, 2, 3])
for i, x in enumerate(cycle_iter):
    if i >= 10:
        break
    print(x, end=' ')
print() 