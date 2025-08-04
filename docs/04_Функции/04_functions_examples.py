#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Функции в Python

Этот файл содержит подробные примеры для изучения:
- Основ создания и вызова функций
- Различных типов параметров и аргументов
- Области видимости переменных
- Функций высшего порядка и замыканий
- Декораторов и их применения
- Генераторов и итераторов
"""

import time
import functools
import itertools
from typing import List, Dict, Callable, Optional, Any
from collections import defaultdict


def example_01_basic_functions():
    """
    Пример 1: Основы создания и использования функций
    
    Демонстрирует базовый синтаксис функций, параметры,
    возвращаемые значения и документирование.
    """
    print("=== Пример 1: Основы создания и использования функций ===")
    
    # Простая функция без параметров
    def greet():
        """Простое приветствие"""
        return "Привет, мир!"
    
    print("1. Функция без параметров:")
    print(greet())
    
    # Функция с параметрами
    def greet_person(name, age):
        """
        Персональное приветствие
        
        Args:
            name (str): Имя человека
            age (int): Возраст человека
        
        Returns:
            str: Персонализированное приветствие
        """
        return f"Привет, {name}! Тебе {age} лет."
    
    print("\n2. Функция с параметрами:")
    print(greet_person("Алиса", 25))
    
    # Функция с значениями по умолчанию
    def create_user(name, age=18, city="Москва", active=True):
        """Создает профиль пользователя с настройками по умолчанию"""
        return {
            "name": name,
            "age": age,
            "city": city,
            "active": active,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    print("\n3. Функция с параметрами по умолчанию:")
    user1 = create_user("Боб")
    user2 = create_user("Алиса", 30, "СПб")
    print(f"Пользователь 1: {user1}")
    print(f"Пользователь 2: {user2}")
    
    # Функция с различными типами возвращаемых значений
    def analyze_number(num):
        """
        Анализирует число и возвращает различную информацию
        
        Returns:
            tuple: (is_positive, is_even, square, description)
        """
        is_positive = num > 0
        is_even = num % 2 == 0
        square = num ** 2
        
        if num == 0:
            description = "ноль"
        elif is_positive:
            description = "положительное" if is_even else "положительное нечетное"
        else:
            description = "отрицательное" if is_even else "отрицательное нечетное"
        
        return is_positive, is_even, square, description
    
    print("\n4. Функция с множественными возвращаемыми значениями:")
    numbers_to_test = [5, -4, 0, 7]
    for num in numbers_to_test:
        pos, even, sq, desc = analyze_number(num)
        print(f"Число {num}: {desc}, квадрат = {sq}")


def example_02_advanced_parameters():
    """
    Пример 2: Продвинутые возможности параметров
    
    Демонстрирует *args, **kwargs, keyword-only параметры
    и различные способы передачи аргументов.
    """
    print("=== Пример 2: Продвинутые возможности параметров ===")
    
    # Функция с *args
    def sum_all(*numbers):
        """Суммирует любое количество чисел"""
        if not numbers:
            return 0
        
        total = sum(numbers)
        print(f"Сумма чисел {numbers} = {total}")
        return total
    
    print("1. Функция с *args:")
    sum_all(1, 2, 3)
    sum_all(10, 20, 30, 40, 50)
    sum_all()
    
    # Функция с **kwargs
    def create_report(**data):
        """Создает отчет из произвольных данных"""
        print("\n📊 Отчет:")
        for key, value in data.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        return data
    
    print("\n2. Функция с **kwargs:")
    create_report(
        total_sales=150000,
        new_customers=45,
        satisfaction_rate=4.7,
        top_product="Python Course"
    )
    
    # Комбинированная функция
    def flexible_function(required_param, default_param="default", *args, **kwargs):
        """Демонстрирует все типы параметров"""
        print(f"\nОбязательный параметр: {required_param}")
        print(f"Параметр по умолчанию: {default_param}")
        
        if args:
            print(f"Дополнительные позиционные аргументы: {args}")
        
        if kwargs:
            print(f"Именованные аргументы: {kwargs}")
        
        return {
            "required": required_param,
            "default": default_param,
            "args": args,
            "kwargs": kwargs
        }
    
    print("\n3. Комбинированная функция:")
    result = flexible_function(
        "обязательный",
        "переопределенный",
        "extra1", "extra2",
        option1="значение1",
        option2="значение2"
    )
    
    # Keyword-only параметры (Python 3+)
    def configure_connection(host, port, *, timeout=30, ssl=True, retries=3):
        """Конфигурирует соединение с keyword-only параметрами"""
        config = {
            "host": host,
            "port": port,
            "timeout": timeout,
            "ssl": ssl,
            "retries": retries
        }
        print(f"\n🔗 Конфигурация соединения: {config}")
        return config
    
    print("\n4. Keyword-only параметры:")
    # configure_connection("localhost", 8080, 60)  # Ошибка!
    configure_connection("localhost", 8080, timeout=60, ssl=False)
    
    # Распаковка аргументов
    def calculate_rectangle(length, width, height=1):
        """Вычисляет площадь и объем прямоугольника"""
        area = length * width
        volume = area * height
        return area, volume
    
    print("\n5. Распаковка аргументов:")
    dimensions = [5, 3]
    options = {"height": 2}
    
    area, volume = calculate_rectangle(*dimensions, **options)
    print(f"Площадь: {area}, Объем: {volume}")


def example_03_scope_and_closures():
    """
    Пример 3: Область видимости и замыкания
    
    Демонстрирует правило LEGB, замыкания и практическое
    применение захвата переменных.
    """
    print("=== Пример 3: Область видимости и замыкания ===")
    
    # Глобальная переменная
    global_counter = 0
    
    def demonstrate_scope():
        """Демонстрирует различные области видимости"""
        global global_counter
        
        # Локальная переменная
        local_var = "Я локальная"
        
        # Изменение глобальной переменной
        global_counter += 1
        
        print(f"Локальная переменная: {local_var}")
        print(f"Глобальный счетчик: {global_counter}")
        
        # Встроенная область видимости
        print(f"Длина строки (встроенная функция): {len('Python')}")
    
    print("1. Демонстрация областей видимости:")
    demonstrate_scope()
    demonstrate_scope()
    
    # Замыкания
    def create_multiplier(factor):
        """Создает функцию-умножитель с помощью замыкания"""
        def multiply(number):
            return number * factor  # Захватываем factor из внешней области
        
        return multiply
    
    print("\n2. Простые замыкания:")
    double = create_multiplier(2)
    triple = create_multiplier(3)
    
    print(f"double(5) = {double(5)}")
    print(f"triple(4) = {triple(4)}")
    
    # Более сложный пример замыкания - счетчик
    def create_counter(initial=0, step=1):
        """Создает счетчик с настраиваемыми параметрами"""
        count = initial
        
        def increment():
            nonlocal count
            count += step
            return count
        
        def decrement():
            nonlocal count
            count -= step
            return count
        
        def get_current():
            return count
        
        def reset():
            nonlocal count
            count = initial
            return count
        
        # Возвращаем словарь с методами
        return {
            "increment": increment,
            "decrement": decrement,
            "current": get_current,
            "reset": reset
        }
    
    print("\n3. Счетчик с замыканием:")
    counter1 = create_counter(10, 2)
    counter2 = create_counter(0, 5)
    
    print(f"Счетчик 1 - начальное значение: {counter1['current']()}")
    print(f"Счетчик 1 - после increment: {counter1['increment']()}")
    print(f"Счетчик 1 - после increment: {counter1['increment']()}")
    print(f"Счетчик 1 - после decrement: {counter1['decrement']()}")
    
    print(f"Счетчик 2 - начальное значение: {counter2['current']()}")
    print(f"Счетчик 2 - после increment: {counter2['increment']()}")
    
    # Замыкание для создания конфигурируемых функций
    def create_validator(min_len=0, max_len=100, required_chars=None):
        """Создает валидатор строк с настраиваемыми правилами"""
        required_chars = required_chars or set()
        
        def validate(text):
            errors = []
            
            if len(text) < min_len:
                errors.append(f"Минимум {min_len} символов")
            
            if len(text) > max_len:
                errors.append(f"Максимум {max_len} символов")
            
            if required_chars and not required_chars.issubset(set(text)):
                missing = required_chars - set(text)
                errors.append(f"Отсутствуют символы: {missing}")
            
            return len(errors) == 0, errors
        
        return validate
    
    print("\n4. Конфигурируемый валидатор:")
    password_validator = create_validator(
        min_len=8, 
        max_len=50, 
        required_chars={'@', '!', '#'}
    )
    
    test_passwords = ["123", "mypassword", "mypass@!", "verylongpassword123!@#"]
    for pwd in test_passwords:
        is_valid, errors = password_validator(pwd)
        status = "✅ Валиден" if is_valid else f"❌ Ошибки: {', '.join(errors)}"
        print(f"  '{pwd}': {status}")


def example_04_higher_order_functions():
    """
    Пример 4: Функции высшего порядка
    
    Демонстрирует map, filter, reduce, custom HOF
    и функциональное программирование.
    """
    print("=== Пример 4: Функции высшего порядка ===")
    
    # Подготовка данных
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    words = ["python", "java", "javascript", "go", "rust", "c++"]
    
    print("1. Встроенные функции высшего порядка:")
    
    # map() - применение функции к каждому элементу
    squares = list(map(lambda x: x**2, numbers))
    print(f"Квадраты: {squares}")
    
    uppercased = list(map(str.upper, words))
    print(f"Верхний регистр: {uppercased}")
    
    # filter() - фильтрация по условию
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Четные числа: {even_numbers}")
    
    long_words = list(filter(lambda w: len(w) > 4, words))
    print(f"Длинные слова: {long_words}")
    
    # reduce() - свертка к одному значению
    from functools import reduce
    
    sum_all = reduce(lambda a, b: a + b, numbers)
    print(f"Сумма всех чисел: {sum_all}")
    
    longest_word = reduce(lambda a, b: a if len(a) > len(b) else b, words)
    print(f"Самое длинное слово: {longest_word}")
    
    # Создание собственных функций высшего порядка
    def apply_to_pairs(func, lst):
        """Применяет функцию к парам соседних элементов"""
        return [func(lst[i], lst[i+1]) for i in range(len(lst)-1)]
    
    def compose(f, g):
        """Создает композицию функций f(g(x))"""
        return lambda x: f(g(x))
    
    print("\n2. Собственные функции высшего порядка:")
    
    # Применение к парам
    differences = apply_to_pairs(lambda a, b: b - a, numbers[:5])
    print(f"Разности соседних элементов: {differences}")
    
    # Композиция функций
    square_and_double = compose(lambda x: x * 2, lambda x: x ** 2)
    result = square_and_double(3)  # (3^2) * 2 = 18
    print(f"Композиция (квадрат и удвоение) для 3: {result}")
    
    # Частичное применение функций
    def partial_apply(func, *partial_args):
        """Создает функцию с частично применеными аргументами"""
        def wrapper(*remaining_args):
            return func(*(partial_args + remaining_args))
        return wrapper
    
    def multiply_three(a, b, c):
        return a * b * c
    
    multiply_by_2_and = partial_apply(multiply_three, 2)
    result1 = multiply_by_2_and(3, 4)  # 2 * 3 * 4 = 24
    print(f"Частичное применение (2 * 3 * 4): {result1}")
    
    # Функция для обработки данных в функциональном стиле
    def process_data(data, *operations):
        """Применяет цепочку операций к данным"""
        result = data
        for operation in operations:
            result = operation(result)
        return result
    
    print("\n3. Функциональная обработка данных:")
    
    # Цепочка обработки
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    result = process_data(
        test_data,
        lambda x: list(filter(lambda n: n % 2 == 0, x)),  # Только четные
        lambda x: list(map(lambda n: n ** 2, x)),         # Квадраты
        lambda x: sum(x)                                   # Сумма
    )
    
    print(f"Исходные данные: {test_data}")
    print(f"Результат (сумма квадратов четных): {result}")


def example_05_decorators():
    """
    Пример 5: Декораторы
    
    Демонстрирует создание и использование декораторов
    для различных целей: логирование, кеширование, валидация.
    """
    print("=== Пример 5: Декораторы ===")
    
    # Простой декоратор для логирования
    def log_calls(func):
        """Декоратор для логирования вызовов функций"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"🔍 Вызов функции {func.__name__} с аргументами {args}, {kwargs}")
            result = func(*args, **kwargs)
            print(f"✅ Функция {func.__name__} вернула: {result}")
            return result
        return wrapper
    
    # Декоратор для измерения времени выполнения
    def timer(func):
        """Декоратор для измерения времени выполнения"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"⏱️ {func.__name__} выполнялась {execution_time:.4f} секунд")
            return result
        return wrapper
    
    print("1. Простые декораторы:")
    
    @log_calls
    @timer
    def calculate_fibonacci(n):
        """Вычисляет n-е число Фибоначчи (неэффективно)"""
        if n <= 1:
            return n
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    
    result = calculate_fibonacci(10)
    print(f"Результат: {result}")
    
    # Декоратор с параметрами
    def retry(max_attempts=3, delay=1):
        """Декоратор для повторных попыток"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            print(f"❌ Все {max_attempts} попыток исчерпаны")
                            raise e
                        print(f"⚠️ Попытка {attempt + 1} неудачна: {e}. Повтор через {delay} сек...")
                        time.sleep(delay)
            return wrapper
        return decorator
    
    print("\n2. Декоратор с параметрами:")
    
    @retry(max_attempts=3, delay=0.5)
    def unreliable_function():
        """Функция, которая иногда падает"""
        import random
        if random.random() < 0.7:  # 70% вероятность ошибки
            raise Exception("Случайная ошибка!")
        return "Успех!"
    
    try:
        result = unreliable_function()
        print(f"✅ Результат: {result}")
    except Exception as e:
        print(f"❌ Финальная ошибка: {e}")
    
    # Декоратор для кеширования
    def memoize(func):
        """Декоратор для кеширования результатов функций"""
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ из аргументов
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                print(f"💾 Результат из кеша для {func.__name__}")
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            print(f"💿 Результат сохранен в кеш для {func.__name__}")
            return result
        
        wrapper.cache = cache  # Предоставляем доступ к кешу
        return wrapper
    
    print("\n3. Декоратор для кеширования:")
    
    @memoize
    def expensive_calculation(n):
        """Имитирует дорогие вычисления"""
        print(f"🔄 Выполняю дорогие вычисления для {n}")
        time.sleep(0.1)  # Имитация задержки
        return n ** 3
    
    # Демонстрация работы кеша
    print(f"Первый вызов: {expensive_calculation(5)}")
    print(f"Второй вызов: {expensive_calculation(5)}")  # Из кеша
    print(f"Третий вызов: {expensive_calculation(3)}")
    print(f"Четвертый вызов: {expensive_calculation(5)}")  # Из кеша
    
    # Декоратор-класс
    class CountCalls:
        """Декоратор-класс для подсчета вызовов функций"""
        def __init__(self, func):
            self.func = func
            self.count = 0
            functools.update_wrapper(self, func)
        
        def __call__(self, *args, **kwargs):
            self.count += 1
            print(f"📊 Функция {self.func.__name__} вызвана {self.count} раз")
            return self.func(*args, **kwargs)
    
    print("\n4. Декоратор-класс:")
    
    @CountCalls
    def say_hello(name):
        return f"Привет, {name}!"
    
    for name in ["Алиса", "Боб", "Чарли"]:
        print(say_hello(name))


def example_06_generators():
    """
    Пример 6: Генераторы и итераторы
    
    Демонстрирует создание генераторов с yield,
    генераторные выражения и практические применения.
    """
    print("=== Пример 6: Генераторы и итераторы ===")
    
    # Простой генератор
    def countdown(n):
        """Генератор обратного отсчета"""
        print(f"🚀 Начинаем обратный отсчет с {n}")
        while n > 0:
            yield n
            n -= 1
        print("🎯 Отсчет завершен!")
    
    print("1. Простой генератор:")
    for num in countdown(5):
        print(f"  {num}")
    
    # Генератор чисел Фибоначчи
    def fibonacci_generator(limit=None):
        """Генератор чисел Фибоначчи"""
        a, b = 0, 1
        count = 0
        while limit is None or count < limit:
            yield a
            a, b = b, a + b
            count += 1
    
    print("\n2. Генератор Фибоначчи:")
    fib_gen = fibonacci_generator(10)
    fib_numbers = list(fib_gen)
    print(f"Первые 10 чисел Фибоначчи: {fib_numbers}")
    
    # Генератор для чтения файлов (имитация)
    def read_lines(content):
        """Генератор для чтения строк (имитация файла)"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            print(f"📖 Читаем строку {i}")
            yield line.strip()
    
    print("\n3. Генератор для чтения строк:")
    sample_content = """Первая строка
Вторая строка
Третья строка
Четвертая строка"""
    
    for line in read_lines(sample_content):
        if line:  # Пропускаем пустые строки
            print(f"  Обработана: '{line}'")
    
    # Генераторные выражения
    print("\n4. Генераторные выражения:")
    
    # Генерация квадратов четных чисел
    even_squares = (x**2 for x in range(10) if x % 2 == 0)
    print(f"Квадраты четных чисел: {list(even_squares)}")
    
    # Обработка больших объемов данных
    def process_large_dataset():
        """Имитирует обработку большого набора данных"""
        print("🔄 Обработка большого набора данных...")
        
        # Генератор данных
        data_generator = (f"item_{i}" for i in range(1000000))
        
        # Обработка по частям (ленивые вычисления)
        processed_count = 0
        for item in data_generator:
            # Имитируем обработку
            if "999" in item:  # Находим специальные элементы
                processed_count += 1
                if processed_count <= 5:  # Показываем только первые 5
                    print(f"  Найден специальный элемент: {item}")
            
            # Останавливаемся после нахождения 5 элементов
            if processed_count >= 5:
                break
        
        print(f"✅ Обработано элементов с '999': {processed_count}")
    
    print("\n5. Обработка больших данных:")
    process_large_dataset()
    
    # Генератор с состоянием
    def stateful_generator():
        """Генератор с внутренним состоянием"""
        state = {"count": 0, "sum": 0}
        
        while True:
            value = yield state.copy()  # Возвращаем копию состояния
            if value is not None:
                state["count"] += 1
                state["sum"] += value
                state["average"] = state["sum"] / state["count"]
    
    print("\n6. Генератор с состоянием:")
    stat_gen = stateful_generator()
    next(stat_gen)  # Инициализация
    
    numbers_to_process = [10, 20, 30, 40, 50]
    for num in numbers_to_process:
        state = stat_gen.send(num)
        print(f"  Добавлено {num}: {state}")
    
    # Комбинирование генераторов
    def chain_generators(*generators):
        """Объединяет несколько генераторов в один"""
        for gen in generators:
            yield from gen
    
    print("\n7. Комбинирование генераторов:")
    gen1 = (x for x in range(3))
    gen2 = (x for x in range(10, 13))
    gen3 = (x for x in range(20, 23))
    
    combined = chain_generators(gen1, gen2, gen3)
    print(f"Объединенные генераторы: {list(combined)}")


def example_07_functional_programming():
    """
    Пример 7: Функциональное программирование
    
    Демонстрирует принципы функционального программирования:
    чистые функции, неизменяемость, композицию.
    """
    print("=== Пример 7: Функциональное программирование ===")
    
    # Чистые функции (без побочных эффектов)
    def pure_add(a, b):
        """Чистая функция сложения"""
        return a + b
    
    def pure_multiply_list(numbers, factor):
        """Чистая функция умножения списка (возвращает новый список)"""
        return [num * factor for num in numbers]
    
    print("1. Чистые функции:")
    original_list = [1, 2, 3, 4, 5]
    doubled_list = pure_multiply_list(original_list, 2)
    print(f"Исходный список: {original_list}")
    print(f"Удвоенный список: {doubled_list}")
    print(f"Исходный список не изменился: {original_list}")
    
    # Функции высшего порядка для обработки данных
    def pipe(*functions):
        """Создает конвейер из функций"""
        def pipeline(data):
            result = data
            for func in functions:
                result = func(result)
            return result
        return pipeline
    
    def curry(func):
        """Каррирование функции (упрощенная версия)"""
        def curried(*args, **kwargs):
            if len(args) + len(kwargs) >= func.__code__.co_argcount:
                return func(*args, **kwargs)
            return lambda *more_args, **more_kwargs: curried(*(args + more_args), **{**kwargs, **more_kwargs})
        return curried
    
    print("\n2. Конвейер функций:")
    
    # Создаем функции для обработки
    def filter_even(numbers):
        return [n for n in numbers if n % 2 == 0]
    
    def square_all(numbers):
        return [n ** 2 for n in numbers]
    
    def sum_all(numbers):
        return sum(numbers)
    
    # Создаем конвейер
    process_numbers = pipe(filter_even, square_all, sum_all)
    
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = process_numbers(test_data)
    print(f"Исходные данные: {test_data}")
    print(f"Результат (сумма квадратов четных): {result}")
    
    # Каррирование
    print("\n3. Каррирование:")
    
    @curry
    def multiply_three_numbers(a, b, c):
        return a * b * c
    
    # Частичное применение
    multiply_by_2 = multiply_three_numbers(2)
    multiply_by_2_and_3 = multiply_by_2(3)
    
    result1 = multiply_by_2_and_3(4)  # 2 * 3 * 4 = 24
    result2 = multiply_by_2(5, 6)     # 2 * 5 * 6 = 60
    
    print(f"Каррированная функция (2 * 3 * 4): {result1}")
    print(f"Каррированная функция (2 * 5 * 6): {result2}")
    
    # Работа с неизменяемыми структурами данных
    def immutable_update(data, key, value):
        """Обновляет словарь, возвращая новый экземпляр"""
        return {**data, key: value}
    
    def immutable_append(lst, item):
        """Добавляет элемент в список, возвращая новый список"""
        return lst + [item]
    
    print("\n4. Неизменяемые обновления:")
    original_dict = {"name": "Алиса", "age": 25}
    updated_dict = immutable_update(original_dict, "city", "Москва")
    
    print(f"Исходный словарь: {original_dict}")
    print(f"Обновленный словарь: {updated_dict}")
    
    original_list = [1, 2, 3]
    extended_list = immutable_append(original_list, 4)
    
    print(f"Исходный список: {original_list}")
    print(f"Расширенный список: {extended_list}")
    
    # Функциональная обработка коллекций
    def map_values(func, collection):
        """Применяет функцию к значениям словаря"""
        return {key: func(value) for key, value in collection.items()}
    
    def filter_dict(predicate, collection):
        """Фильтрует словарь по предикату"""
        return {key: value for key, value in collection.items() if predicate(key, value)}
    
    print("\n5. Функциональная обработка коллекций:")
    scores = {"Алиса": 85, "Боб": 92, "Чарли": 78, "Диана": 96}
    
    # Конвертация баллов в проценты
    percentages = map_values(lambda score: f"{score}%", scores)
    print(f"Проценты: {percentages}")
    
    # Фильтрация высоких баллов
    high_scores = filter_dict(lambda name, score: score >= 90, scores)
    print(f"Высокие баллы: {high_scores}")


def example_08_advanced_techniques():
    """
    Пример 8: Продвинутые техники
    
    Демонстрирует метапрограммирование, динамическое создание функций
    и продвинутые паттерны.
    """
    print("=== Пример 8: Продвинутые техники ===")
    
    # Динамическое создание функций
    def create_operation_function(operation):
        """Создает функцию для математической операции"""
        operations = {
            "add": lambda a, b: a + b,
            "multiply": lambda a, b: a * b,
            "power": lambda a, b: a ** b,
            "modulo": lambda a, b: a % b
        }
        
        if operation not in operations:
            raise ValueError(f"Неизвестная операция: {operation}")
        
        base_func = operations[operation]
        
        def operation_function(a, b):
            result = base_func(a, b)
            print(f"{operation}({a}, {b}) = {result}")
            return result
        
        operation_function.__name__ = f"{operation}_function"
        operation_function.__doc__ = f"Выполняет операцию {operation}"
        
        return operation_function
    
    print("1. Динамическое создание функций:")
    
    # Создаем функции динамически
    add_func = create_operation_function("add")
    multiply_func = create_operation_function("multiply")
    
    add_func(5, 3)
    multiply_func(4, 7)
    
    # Фабрика декораторов
    def create_validator_decorator(validation_func, error_message):
        """Создает декоратор для валидации аргументов"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not validation_func(*args, **kwargs):
                    raise ValueError(error_message)
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    print("\n2. Фабрика декораторов:")
    
    # Создаем специализированные декораторы
    positive_numbers = create_validator_decorator(
        lambda *args, **kwargs: all(isinstance(arg, (int, float)) and arg > 0 
                                   for arg in args if isinstance(arg, (int, float))),
        "Все числовые аргументы должны быть положительными"
    )
    
    non_empty_strings = create_validator_decorator(
        lambda *args, **kwargs: all(isinstance(arg, str) and len(arg) > 0 
                                   for arg in args if isinstance(arg, str)),
        "Все строковые аргументы должны быть непустыми"
    )
    
    @positive_numbers
    @non_empty_strings
    def create_product(name, price, quantity):
        """Создает продукт с валидацией"""
        return {
            "name": name,
            "price": price,
            "quantity": quantity,
            "total_value": price * quantity
        }
    
    try:
        product1 = create_product("Телефон", 50000, 2)
        print(f"Продукт создан: {product1}")
        
        # Это вызовет ошибку валидации
        # product2 = create_product("", 50000, 2)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
    
    # Система плагинов с функциями
    class PluginSystem:
        """Простая система плагинов"""
        def __init__(self):
            self.plugins = {}
        
        def register(self, name):
            """Декоратор для регистрации плагинов"""
            def decorator(func):
                self.plugins[name] = func
                print(f"🔌 Плагин '{name}' зарегистрирован")
                return func
            return decorator
        
        def execute(self, name, *args, **kwargs):
            """Выполняет плагин по имени"""
            if name in self.plugins:
                return self.plugins[name](*args, **kwargs)
            else:
                raise ValueError(f"Плагин '{name}' не найден")
        
        def list_plugins(self):
            """Список всех плагинов"""
            return list(self.plugins.keys())
    
    print("\n3. Система плагинов:")
    
    plugin_system = PluginSystem()
    
    @plugin_system.register("calculator")
    def calculator_plugin(operation, a, b):
        operations = {
            "add": a + b,
            "sub": a - b,
            "mul": a * b,
            "div": a / b if b != 0 else "Division by zero"
        }
        return operations.get(operation, "Unknown operation")
    
    @plugin_system.register("formatter")
    def formatter_plugin(text, style="upper"):
        styles = {
            "upper": text.upper(),
            "lower": text.lower(),
            "title": text.title(),
            "reverse": text[::-1]
        }
        return styles.get(style, text)
    
    # Использование плагинов
    print(f"Доступные плагины: {plugin_system.list_plugins()}")
    
    calc_result = plugin_system.execute("calculator", "add", 10, 5)
    print(f"Результат вычисления: {calc_result}")
    
    formatted_text = plugin_system.execute("formatter", "hello world", "title")
    print(f"Отформатированный текст: {formatted_text}")
    
    # Мемоизация с TTL (Time To Live)
    def memoize_with_ttl(ttl_seconds=60):
        """Мемоизация с временем жизни кеша"""
        def decorator(func):
            cache = {}
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                import time
                
                key = str(args) + str(sorted(kwargs.items()))
                current_time = time.time()
                
                # Проверяем, есть ли результат в кеше и не истекло ли время
                if key in cache:
                    result, timestamp = cache[key]
                    if current_time - timestamp < ttl_seconds:
                        print(f"💾 Результат из кеша (возраст: {current_time - timestamp:.1f}с)")
                        return result
                    else:
                        print(f"⏰ Кеш истек, пересчитываем...")
                        del cache[key]
                
                # Вычисляем и кешируем результат
                result = func(*args, **kwargs)
                cache[key] = (result, current_time)
                print(f"💿 Результат сохранен в кеш с TTL {ttl_seconds}с")
                return result
            
            return wrapper
        return decorator
    
    print("\n4. Мемоизация с TTL:")
    
    @memoize_with_ttl(ttl_seconds=2)
    def slow_calculation(n):
        """Медленные вычисления"""
        print(f"🔄 Выполняю медленные вычисления для {n}")
        time.sleep(0.1)
        return n ** 3
    
    # Демонстрация работы TTL кеша
    print(f"Первый вызов: {slow_calculation(5)}")
    print(f"Второй вызов: {slow_calculation(5)}")  # Из кеша
    time.sleep(2.1)  # Ждем истечения TTL
    print(f"Третий вызов: {slow_calculation(5)}")  # Пересчет


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Основы создания и использования функций", example_01_basic_functions),
        ("Продвинутые возможности параметров", example_02_advanced_parameters),
        ("Область видимости и замыкания", example_03_scope_and_closures),
        ("Функции высшего порядка", example_04_higher_order_functions),
        ("Декораторы", example_05_decorators),
        ("Генераторы и итераторы", example_06_generators),
        ("Функциональное программирование", example_07_functional_programming),
        ("Продвинутые техники", example_08_advanced_techniques),
    ]
    
    print("🎯 Примеры: Функции в Python")
    print("=" * 50)
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")
        print("-" * (len(name) + 3))
        try:
            func()
        except Exception as e:
            print(f"Ошибка при выполнении примера: {e}")
        
        if i < len(examples):
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main() 