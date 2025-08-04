# Примеры продвинутых декораторов
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Время выполнения: {time.time() - start}")
        return result
    return wrapper

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@timer
@log
def slow_function():
    time.sleep(1)
    return "готово"

result = slow_function()
print(result) 