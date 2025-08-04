# Примеры декораторов
def my_decorator(func):
    def wrapper():
        print("До вызова")
        func()
        print("После вызова")
    return wrapper

@my_decorator
def hello():
    print("Привет!")

hello()

# Декоратор с аргументами
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Привет, {name}!")

greet("Анна") 