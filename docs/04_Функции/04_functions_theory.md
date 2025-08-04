# Теория: Функции в Python

## 🎯 Цели раздела

После изучения этого раздела вы будете:
- Понимать принципы создания и вызова функций
- Знать различные способы передачи аргументов
- Уметь работать с областью видимости переменных
- Понимать функции высшего порядка и замыкания
- Знать декораторы и их применение
- Уметь создавать генераторы и итераторы

## 📝 Основы функций

### Что такое функция?

Функция — это именованный блок кода, который можно вызывать многократно. Функции помогают:
- **Избегать дублирования кода** (DRY принцип)
- **Разбивать сложные задачи** на простые части
- **Повышать читаемость** и поддерживаемость кода
- **Упрощать тестирование** и отладку

### Синтаксис определения функции

```python
def function_name(parameters):
    """Docstring - документация функции"""
    # Тело функции
    return value  # Необязательно
```

### Простые примеры

```python
# Функция без параметров
def greet():
    print("Привет!")

# Функция с параметрами
def greet_user(name):
    print(f"Привет, {name}!")

# Функция с возвращаемым значением
def add_numbers(a, b):
    return a + b

# Функция с документацией
def calculate_area(radius):
    """
    Вычисляет площадь круга по радиусу.
    
    Args:
        radius (float): Радиус круга
    
    Returns:
        float: Площадь круга
    """
    import math
    return math.pi * radius ** 2
```

## 🔧 Параметры и аргументы

### Типы параметров

#### 1. Позиционные параметры

```python
def introduce(name, age, city):
    print(f"Меня зовут {name}, мне {age} лет, живу в {city}")

# Вызов с позиционными аргументами
introduce("Алиса", 25, "Москва")
```

#### 2. Параметры со значениями по умолчанию

```python
def create_profile(name, age=18, city="Неизвестно"):
    return {
        "name": name,
        "age": age,
        "city": city
    }

# Различные способы вызова
profile1 = create_profile("Боб")  # age=18, city="Неизвестно"
profile2 = create_profile("Алиса", 25)  # city="Неизвестно"
profile3 = create_profile("Чарли", 30, "СПб")
```

**⚠️ Важно**: Избегайте изменяемых объектов как значений по умолчанию!

```python
# ❌ Плохо - опасная ловушка!
def add_item(item, target_list=[]):
    target_list.append(item)
    return target_list

# ✅ Правильно
def add_item(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list
```

#### 3. Именованные аргументы (keyword arguments)

```python
def book_flight(from_city, to_city, date, passengers=1, class_type="economy"):
    return f"Рейс {from_city} → {to_city}, {date}, {passengers} пасс., {class_type}"

# Именованные аргументы можно передавать в любом порядке
flight = book_flight(
    to_city="Париж",
    from_city="Москва", 
    date="2024-06-15",
    class_type="business"
)
```

#### 4. *args - произвольное количество позиционных аргументов

```python
def sum_all(*numbers):
    """Суммирует любое количество чисел"""
    return sum(numbers)

result1 = sum_all(1, 2, 3)          # 6
result2 = sum_all(1, 2, 3, 4, 5)    # 15
result3 = sum_all()                 # 0

def print_info(name, *details):
    print(f"Имя: {name}")
    for detail in details:
        print(f"- {detail}")

print_info("Алиса", "25 лет", "Программист", "Москва")
```

#### 5. **kwargs - произвольное количество именованных аргументов

```python
def create_user(**user_data):
    """Создает пользователя с произвольными данными"""
    user = {"id": generate_id()}
    user.update(user_data)
    return user

user = create_user(
    name="Алиса",
    age=25,
    email="alice@example.com",
    city="Москва",
    occupation="Developer"
)
```

#### 6. Комбинирование всех типов параметров

**Порядок параметров должен быть строго такой:**

```python
def complex_function(pos1, pos2, default_param="default", *args, **kwargs):
    print(f"Позиционные: {pos1}, {pos2}")
    print(f"По умолчанию: {default_param}")
    print(f"*args: {args}")
    print(f"**kwargs: {kwargs}")

# Пример вызова
complex_function(
    "arg1", "arg2",           # Позиционные
    "custom_default",         # Переопределяем значение по умолчанию
    "extra1", "extra2",       # Дополнительные позиционные (*args)
    key1="value1",            # Именованные (**kwargs)
    key2="value2"
)
```

### Keyword-only и positional-only параметры (Python 3.8+)

```python
# Positional-only параметры (до /)
def pos_only(a, b, /):
    return a + b

pos_only(1, 2)        # ✅ Работает
# pos_only(a=1, b=2)  # ❌ Ошибка!

# Keyword-only параметры (после *)
def kwd_only(*, x, y):
    return x * y

kwd_only(x=3, y=4)    # ✅ Работает
# kwd_only(3, 4)      # ❌ Ошибка!

# Комбинирование
def combined(pos_only, /, standard, *, kwd_only):
    return pos_only + standard + kwd_only

combined(1, 2, kwd_only=3)           # ✅ Работает
combined(1, standard=2, kwd_only=3)  # ✅ Работает
```

## 🌍 Область видимости переменных (Scope)

### Правило LEGB

Python ищет переменные в следующем порядке:

1. **L**ocal - локальная область (внутри функции)
2. **E**nclosing - объемлющая область (вложенные функции)
3. **G**lobal - глобальная область (модуль)
4. **B**uilt-in - встроенная область (встроенные имена Python)

```python
# Built-in scope
# len, print, str и др. - встроенные функции

# Global scope
global_var = "Я глобальная переменная"

def outer_function():
    # Enclosing scope
    enclosing_var = "Я из объемлющей области"
    
    def inner_function():
        # Local scope
        local_var = "Я локальная переменная"
        
        print(f"Local: {local_var}")
        print(f"Enclosing: {enclosing_var}")
        print(f"Global: {global_var}")
        print(f"Built-in: {len([1, 2, 3])}")
    
    inner_function()

outer_function()
```

### Ключевые слова global и nonlocal

```python
counter = 0  # Глобальная переменная

def increment_global():
    global counter
    counter += 1

def create_counter():
    count = 0  # Локальная для outer, enclosing для inner
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    def get_count():
        return count
    
    return increment, get_count

# Пример использования
inc, get = create_counter()
print(inc())  # 1
print(inc())  # 2
print(get())  # 2
```

## 🎭 Функции как объекты первого класса

В Python функции являются объектами первого класса, что означает:

### 1. Функции можно присваивать переменным

```python
def greet(name):
    return f"Привет, {name}!"

# Присваиваем функцию переменной
say_hello = greet
print(say_hello("Алиса"))  # "Привет, Алиса!"
```

### 2. Функции можно передавать как аргументы

```python
def apply_operation(numbers, operation):
    """Применяет операцию к списку чисел"""
    return [operation(x) for x in numbers]

def square(x):
    return x ** 2

def cube(x):
    return x ** 3

numbers = [1, 2, 3, 4, 5]
squares = apply_operation(numbers, square)  # [1, 4, 9, 16, 25]
cubes = apply_operation(numbers, cube)      # [1, 8, 27, 64, 125]
```

### 3. Функции можно возвращать из других функций

```python
def create_multiplier(factor):
    """Создает функцию-умножитель"""
    def multiply(x):
        return x * factor
    return multiply

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

### 4. Функции можно хранить в структурах данных

```python
# Словарь операций
operations = {
    "add": lambda x, y: x + y,
    "subtract": lambda x, y: x - y,
    "multiply": lambda x, y: x * y,
    "divide": lambda x, y: x / y if y != 0 else None
}

result = operations["multiply"](6, 7)  # 42
```

## 🎯 Функции высшего порядка

### map(), filter(), reduce()

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map() - применяет функцию к каждому элементу
squares = list(map(lambda x: x**2, numbers))
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# filter() - фильтрует элементы по условию
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4, 6, 8, 10]

# reduce() - сводит последовательность к одному значению
sum_all = reduce(lambda x, y: x + y, numbers)
# 55

# Более сложный пример
words = ["python", "java", "javascript", "go"]
long_words = list(filter(lambda w: len(w) > 4, words))
word_lengths = list(map(len, words))
total_length = reduce(lambda a, b: a + b, word_lengths)
```

### Функциональное программирование

```python
# Функция композиции
def compose(f, g):
    """Создает композицию функций f(g(x))"""
    return lambda x: f(g(x))

# Частичное применение
def partial(func, *args):
    """Создает функцию с частично примененными аргументами"""
    def wrapper(*remaining_args):
        return func(*(args + remaining_args))
    return wrapper

# Пример использования
def add_three_numbers(a, b, c):
    return a + b + c

add_five_and = partial(add_three_numbers, 5)
result = add_five_and(3, 2)  # 5 + 3 + 2 = 10
```

## 🔒 Замыкания (Closures)

Замыкание — это функция, которая "захватывает" переменные из окружающей области видимости.

```python
def create_account(initial_balance):
    """Создает "банковский счет" с помощью замыкания"""
    balance = initial_balance
    
    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance
    
    def withdraw(amount):
        nonlocal balance
        if amount <= balance:
            balance -= amount
            return balance
        else:
            return "Недостаточно средств"
    
    def get_balance():
        return balance
    
    # Возвращаем словарь с методами
    return {
        "deposit": deposit,
        "withdraw": withdraw,
        "balance": get_balance
    }

# Создаем счета
account1 = create_account(1000)
account2 = create_account(500)

print(account1["deposit"](200))   # 1200
print(account1["withdraw"](300))  # 900
print(account1["balance"]())      # 900

print(account2["balance"]())      # 500 (независимый счет)
```

### Практическое применение замыканий

```python
# Создание конфигурируемых функций
def create_validator(min_length, max_length):
    """Создает функцию валидации строк"""
    def validate(text):
        if not isinstance(text, str):
            return False, "Должна быть строка"
        if len(text) < min_length:
            return False, f"Минимум {min_length} символов"
        if len(text) > max_length:
            return False, f"Максимум {max_length} символов"
        return True, "OK"
    return validate

# Создаем специализированные валидаторы
username_validator = create_validator(3, 20)
password_validator = create_validator(8, 128)

print(username_validator("ab"))        # (False, "Минимум 3 символов")
print(username_validator("alice"))     # (True, "OK")
print(password_validator("123"))       # (False, "Минимум 8 символов")
```

## 🎨 Декораторы

Декоратор — это функция, которая принимает другую функцию и расширяет её поведение без изменения исходного кода.

### Простой декоратор

```python
def my_decorator(func):
    """Простой декоратор"""
    def wrapper():
        print("Что-то делаем до вызова функции")
        result = func()
        print("Что-то делаем после вызова функции")
        return result
    return wrapper

# Использование декоратора
@my_decorator
def say_hello():
    print("Привет!")

# Эквивалентно: say_hello = my_decorator(say_hello)
say_hello()
```

### Декоратор с аргументами

```python
import time
from functools import wraps

def timer(func):
    """Декоратор для измерения времени выполнения"""
    @wraps(func)  # Сохраняет метаданные оригинальной функции
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} выполнялась {end_time - start_time:.4f} сек")
        return result
    return wrapper

@timer
def slow_calculation(n):
    """Медленные вычисления"""
    return sum(i**2 for i in range(n))

result = slow_calculation(100000)
```

### Декоратор с параметрами

```python
def retry(max_attempts):
    """Декоратор для повторных попыток"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Попытка {attempt + 1} неудачна: {e}")
            return None
        return wrapper
    return decorator

@retry(max_attempts=3)
def unreliable_function():
    import random
    if random.random() < 0.7:  # 70% вероятность ошибки
        raise Exception("Случайная ошибка!")
    return "Успех!"

try:
    result = unreliable_function()
    print(result)
except Exception as e:
    print(f"Все попытки исчерпаны: {e}")
```

### Полезные встроенные декораторы

```python
class Calculator:
    def __init__(self):
        self._cache = {}
    
    @staticmethod
    def add(x, y):
        """Статический метод"""
        return x + y
    
    @classmethod
    def create_with_cache(cls):
        """Метод класса"""
        instance = cls()
        instance._cache = {"initialized": True}
        return instance
    
    @property
    def cache_size(self):
        """Свойство только для чтения"""
        return len(self._cache)
    
    @cache_size.setter
    def cache_size(self, value):
        """Setter для свойства (в данном случае не имеет смысла)"""
        pass

# Использование
calc = Calculator()
print(Calculator.add(2, 3))  # Статический метод
calc2 = Calculator.create_with_cache()  # Метод класса
print(calc.cache_size)  # Свойство
```

## 🔄 Генераторы и итераторы

### Генераторы с yield

```python
def countdown(n):
    """Генератор обратного отсчета"""
    while n > 0:
        yield n
        n -= 1

# Использование генератора
for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1

# Генератор можно использовать как итератор
counter = countdown(3)
print(next(counter))  # 3
print(next(counter))  # 2
print(next(counter))  # 1
# print(next(counter))  # StopIteration
```

### Генераторные выражения

```python
# Генераторное выражение
squares_gen = (x**2 for x in range(10))

# Ленивое вычисление - значения генерируются по требованию
for square in squares_gen:
    if square > 50:
        break
    print(square)  # 0, 1, 4, 9, 16, 25, 36, 49
```

### Сложные генераторы

```python
def fibonacci():
    """Бесконечный генератор чисел Фибоначчи"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def take(n, iterable):
    """Берет первые n элементов из итерируемого объекта"""
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item

# Первые 10 чисел Фибоначчи
fib_numbers = list(take(10, fibonacci()))
print(fib_numbers)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Генераторы для обработки больших файлов

```python
def read_large_file(file_path):
    """Генератор для чтения больших файлов построчно"""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

def process_lines(file_path, pattern):
    """Обработка строк файла с фильтрацией"""
    for line in read_large_file(file_path):
        if pattern in line:
            yield line.upper()

# Использование (файл читается по мере необходимости)
# for processed_line in process_lines("large_file.txt", "error"):
#     print(processed_line)
```

## 📚 Лучшие практики

### 1. Принцип единственной ответственности

```python
# ❌ Плохо - функция делает слишком много
def process_user_data_bad(user_data):
    # Валидация
    if not user_data.get("email"):
        raise ValueError("Email обязателен")
    
    # Обработка
    user_data["email"] = user_data["email"].lower()
    
    # Сохранение в БД
    save_to_database(user_data)
    
    # Отправка email
    send_welcome_email(user_data["email"])
    
    return user_data

# ✅ Хорошо - разделение ответственности
def validate_user_data(user_data):
    """Валидирует данные пользователя"""
    if not user_data.get("email"):
        raise ValueError("Email обязателен")
    return True

def normalize_user_data(user_data):
    """Нормализует данные пользователя"""
    normalized = user_data.copy()
    normalized["email"] = normalized["email"].lower()
    return normalized

def create_user(user_data):
    """Создает нового пользователя"""
    validate_user_data(user_data)
    normalized_data = normalize_user_data(user_data)
    
    user_id = save_to_database(normalized_data)
    send_welcome_email(normalized_data["email"])
    
    return user_id
```

### 2. Использование type hints

```python
from typing import List, Dict, Optional, Callable, Union

def calculate_average(numbers: List[float]) -> float:
    """Вычисляет среднее арифметическое"""
    if not numbers:
        raise ValueError("Список не может быть пустым")
    return sum(numbers) / len(numbers)

def process_data(
    data: Dict[str, Union[int, str]], 
    processor: Callable[[str], str],
    default_value: Optional[str] = None
) -> Dict[str, str]:
    """Обрабатывает данные с помощью функции-процессора"""
    result = {}
    for key, value in data.items():
        if isinstance(value, str):
            result[key] = processor(value)
        else:
            result[key] = default_value or str(value)
    return result
```

### 3. Документирование функций

```python
def calculate_compound_interest(
    principal: float, 
    rate: float, 
    time: float, 
    compound_frequency: int = 12
) -> float:
    """
    Вычисляет сложные проценты.
    
    Args:
        principal: Начальная сумма
        rate: Годовая процентная ставка (в долях, например 0.05 для 5%)
        time: Период в годах
        compound_frequency: Частота начисления процентов в год (по умолчанию 12)
    
    Returns:
        Итоговая сумма с процентами
    
    Raises:
        ValueError: Если какой-либо параметр отрицательный
    
    Example:
        >>> calculate_compound_interest(1000, 0.05, 2)
        1104.94
    """
    if any(param < 0 for param in [principal, rate, time, compound_frequency]):
        raise ValueError("Все параметры должны быть неотрицательными")
    
    if compound_frequency == 0:
        raise ValueError("Частота начисления не может быть нулевой")
    
    return principal * (1 + rate / compound_frequency) ** (compound_frequency * time)
```

### 4. Обработка ошибок

```python
def safe_divide(a: float, b: float) -> Optional[float]:
    """
    Безопасное деление с обработкой ошибок
    
    Returns:
        Результат деления или None при ошибке
    """
    try:
        if b == 0:
            print("Ошибка: деление на ноль")
            return None
        return a / b
    except TypeError:
        print("Ошибка: аргументы должны быть числами")
        return None

def divide_with_exception(a: float, b: float) -> float:
    """
    Деление с явным возбуждением исключений
    
    Raises:
        ZeroDivisionError: При делении на ноль
        TypeError: При неверных типах аргументов
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Аргументы должны быть числами")
    
    if b == 0:
        raise ZeroDivisionError("Деление на ноль недопустимо")
    
    return a / b
```

## 🚀 Продвинутые техники

### Мемоизация (кеширование результатов)

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci_cached(n):
    """Числа Фибоначчи с кешированием"""
    if n <= 1:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

# Намного быстрее для больших n
print(fibonacci_cached(50))  # Вычисляется мгновенно
```

### Декораторы для валидации

```python
def validate_types(**expected_types):
    """Декоратор для валидации типов аргументов"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем имена параметров функции
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Проверяем типы
            for param_name, expected_type in expected_types.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{param_name} должен быть {expected_type.__name__}, "
                            f"получен {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int, salary=float)
def create_employee(name, age, salary):
    return {"name": name, "age": age, "salary": salary}

# create_employee("Alice", "25", 50000.0)  # TypeError
create_employee("Alice", 25, 50000.0)  # ✅ Работает
```

## 🔍 Заключение

Функции — это основа структурированного программирования в Python. Понимание различных аспектов функций поможет вам:

**Ключевые принципы:**
1. **Разделяйте ответственность** - одна функция = одна задача
2. **Используйте понятные имена** и документируйте код
3. **Применяйте type hints** для лучшей читаемости
4. **Обрабатывайте ошибки** явно и предсказуемо
5. **Используйте декораторы** для кросс-функциональности
6. **Применяйте генераторы** для работы с большими данными

Функции в Python — это мощный инструмент, который при правильном использовании делает код более чистым, поддерживаемым и эффективным! 