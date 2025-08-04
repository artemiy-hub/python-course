#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Базовые конструкции Python

Этот файл содержит подробные примеры для изучения:
- Переменных и типов данных
- Операторов
- Условных конструкций
- Циклов
- Ввода и вывода данных
- Области видимости
"""

import sys
import math
from datetime import datetime

def example_01_variables_and_types():
    """
    Пример 1: Переменные и типы данных
    
    Демонстрирует создание переменных, динамическую типизацию
    и работу с различными типами данных.
    """
    print("=== Пример 1: Переменные и типы данных ===")
    
    # Динамическая типизация - тип определяется автоматически
    print("1. Динамическая типизация:")
    x = 42
    print(f"x = {x}, тип: {type(x).__name__}")
    
    x = "Теперь я строка"
    print(f"x = '{x}', тип: {type(x).__name__}")
    
    x = [1, 2, 3]
    print(f"x = {x}, тип: {type(x).__name__}")
    
    # Множественное присваивание
    print("\n2. Множественное присваивание:")
    a, b, c = 1, 2, 3
    print(f"a={a}, b={b}, c={c}")
    
    # Обмен значениями
    print(f"До обмена: a={a}, b={b}")
    a, b = b, a
    print(f"После обмена: a={a}, b={b}")
    
    # Присваивание одного значения нескольким переменным
    x = y = z = 0
    print(f"x={x}, y={y}, z={z}")
    
    # Числовые типы
    print("\n3. Числовые типы:")
    
    # Целые числа
    integer_decimal = 42
    integer_binary = 0b101010      # Двоичная запись числа 42
    integer_octal = 0o52          # Восьмеричная запись числа 42
    integer_hex = 0x2A            # Шестнадцатеричная запись числа 42
    
    print(f"Decimal: {integer_decimal}")
    print(f"Binary: {integer_binary} (0b101010)")
    print(f"Octal: {integer_octal} (0o52)")
    print(f"Hex: {integer_hex} (0x2A)")
    
    # Большие числа с разделителями
    big_number = 1_000_000_000
    print(f"Большое число: {big_number:,}")
    
    # Числа с плавающей точкой
    float_normal = 3.14159
    float_scientific = 1.5e-4    # 0.00015
    print(f"Обычная запись: {float_normal}")
    print(f"Научная нотация: {float_scientific}")
    
    # Комплексные числа
    complex_num = 3 + 4j
    print(f"Комплексное число: {complex_num}")
    print(f"Действительная часть: {complex_num.real}")
    print(f"Мнимая часть: {complex_num.imag}")
    print(f"Модуль: {abs(complex_num)}")
    
    print()

def example_02_string_operations():
    """
    Пример 2: Операции со строками
    
    Подробная демонстрация работы со строками:
    создание, форматирование, методы.
    """
    print("=== Пример 2: Операции со строками ===")
    
    # Способы создания строк
    print("1. Создание строк:")
    single_quotes = 'Одинарные кавычки'
    double_quotes = "Двойные кавычки"
    triple_quotes = """Тройные кавычки
    для многострочного
    текста"""
    
    print(f"Одинарные: {single_quotes}")
    print(f"Двойные: {double_quotes}")
    print(f"Тройные: {repr(triple_quotes)}")
    
    # Escape-последовательности
    print("\n2. Escape-последовательности:")
    escape_examples = [
        ("\\n", "Новая строка"),
        ("\\t", "Табуляция"),
        ("\\\\", "Обратная косая черта"),
        ("\\'", "Одинарная кавычка"),
        ("\\\"", "Двойная кавычка"),
    ]
    
    for escape, description in escape_examples:
        print(f"{escape:4} → {description}")
    
    # Raw строки
    path_normal = "C:\\Users\\Name\\Documents"
    path_raw = r"C:\Users\Name\Documents"
    print(f"\nОбычная строка: {path_normal}")
    print(f"Raw строка: {path_raw}")
    
    # Форматирование строк
    print("\n3. Форматирование строк:")
    name = "Анна"
    age = 25
    height = 165.5
    
    # f-строки (рекомендуемый способ)
    f_string = f"Меня зовут {name}, мне {age} лет, рост {height:.1f} см"
    print(f"f-строки: {f_string}")
    
    # Метод format()
    format_string = "Меня зовут {}, мне {} лет, рост {:.1f} см".format(name, age, height)
    print(f"format(): {format_string}")
    
    # Именованные параметры в format()
    named_format = "Меня зовут {name}, мне {age} лет".format(name=name, age=age)
    print(f"Именованные: {named_format}")
    
    # Методы строк
    print("\n4. Методы строк:")
    text = "  Python Programming Language  "
    
    methods_demo = [
        ("strip()", text.strip()),
        ("upper()", text.strip().upper()),
        ("lower()", text.strip().lower()),
        ("title()", text.strip().title()),
        ("replace()", text.strip().replace("Python", "Java")),
        ("split()", text.strip().split()),
        ("find('gram')", text.strip().find("gram")),
        ("count('g')", text.strip().count("g")),
        ("startswith('Py')", text.strip().startswith("Py")),
        ("endswith('age')", text.strip().endswith("age")),
    ]
    
    for method, result in methods_demo:
        print(f"{method:20} → {result}")
    
    # Проверки типа содержимого
    print("\n5. Проверки содержимого:")
    test_strings = ["123", "abc", "ABC", "Hello123", "hello world", "   "]
    
    for test_str in test_strings:
        checks = [
            f"isdigit(): {test_str.isdigit()}",
            f"isalpha(): {test_str.isalpha()}",
            f"isalnum(): {test_str.isalnum()}",
            f"isupper(): {test_str.isupper()}",
            f"islower(): {test_str.islower()}",
            f"isspace(): {test_str.isspace()}"
        ]
        print(f"'{test_str}': {', '.join(checks)}")
    
    print()

def example_03_operators():
    """
    Пример 3: Операторы
    
    Демонстрирует арифметические, логические операторы,
    операторы сравнения и присваивания.
    """
    print("=== Пример 3: Операторы ===")
    
    # Арифметические операторы
    print("1. Арифметические операторы:")
    a, b = 17, 5
    
    operations = [
        ("+", a + b, "сложение"),
        ("-", a - b, "вычитание"),
        ("*", a * b, "умножение"),
        ("/", a / b, "деление"),
        ("//", a // b, "целочисленное деление"),
        ("%", a % b, "остаток от деления"),
        ("**", a ** b, "возведение в степень"),
    ]
    
    for op, result, description in operations:
        print(f"{a} {op} {b} = {result:>10} ({description})")
    
    # Операторы сравнения
    print(f"\n2. Операторы сравнения (a={a}, b={b}):")
    comparisons = [
        ("==", a == b, "равно"),
        ("!=", a != b, "не равно"),
        ("<", a < b, "меньше"),
        ("<=", a <= b, "меньше или равно"),
        (">", a > b, "больше"),
        (">=", a >= b, "больше или равно"),
    ]
    
    for op, result, description in comparisons:
        print(f"{a} {op} {b} = {result:>5} ({description})")
    
    # Цепочки сравнений
    x = 15
    print(f"\n3. Цепочки сравнений (x={x}):")
    print(f"10 < x < 20: {10 < x < 20}")
    print(f"x <= 15 <= 20: {x <= 15 <= 20}")
    
    # Логические операторы
    print("\n4. Логические операторы:")
    p, q = True, False
    
    logical_ops = [
        ("and", p and q, f"{p} and {q}"),
        ("or", p or q, f"{p} or {q}"),
        ("not p", not p, f"not {p}"),
        ("not q", not q, f"not {q}"),
    ]
    
    for op, result, expression in logical_ops:
        print(f"{expression:15} = {result}")
    
    # Короткое замыкание
    print("\n5. Короткое замыкание:")
    
    def true_func():
        print("  true_func() вызвана")
        return True
    
    def false_func():
        print("  false_func() вызвана")
        return False
    
    print("False and true_func():")
    result = False and true_func()  # true_func() не вызывается
    print(f"Результат: {result}")
    
    print("\nTrue or false_func():")
    result = True or false_func()   # false_func() не вызывается
    print(f"Результат: {result}")
    
    # Операторы присваивания
    print("\n6. Операторы присваивания:")
    x = 10
    print(f"Начальное значение x: {x}")
    
    assignment_ops = [
        ("+=", 5),
        ("-=", 3),
        ("*=", 2),
        ("/=", 4),
        ("//=", 2),
        ("%=", 3),
        ("**=", 2),
    ]
    
    for op, value in assignment_ops:
        if op == "+=":
            x += value
        elif op == "-=":
            x -= value
        elif op == "*=":
            x *= value
        elif op == "/=":
            x /= value
        elif op == "//=":
            x //= value
        elif op == "%=":
            x %= value
        elif op == "**=":
            x **= value
        
        print(f"x {op} {value} → x = {x}")
    
    print()

def example_04_conditional_statements():
    """
    Пример 4: Условные конструкции
    
    Демонстрирует различные формы условных операторов
    и практические примеры их использования.
    """
    print("=== Пример 4: Условные конструкции ===")
    
    # Простое условие if
    print("1. Простое условие if:")
    age = 20
    if age >= 18:
        print(f"Возраст {age}: совершеннолетний")
    
    # Полная конструкция if-elif-else
    print("\n2. Полная конструкция if-elif-else:")
    
    def get_grade(score):
        if score >= 90:
            return "A (Отлично)"
        elif score >= 80:
            return "B (Хорошо)"
        elif score >= 70:
            return "C (Удовлетворительно)"
        elif score >= 60:
            return "D (Плохо)"
        else:
            return "F (Провал)"
    
    test_scores = [95, 87, 73, 65, 45]
    for score in test_scores:
        grade = get_grade(score)
        print(f"Оценка {score}: {grade}")
    
    # Тернарный оператор
    print("\n3. Тернарный оператор:")
    numbers = [5, -3, 0, 12, -8]
    
    for num in numbers:
        # Полная запись
        if num > 0:
            status_full = "положительное"
        else:
            status_full = "отрицательное или ноль"
        
        # Тернарный оператор
        status_ternary = "положительное" if num > 0 else "отрицательное или ноль"
        
        print(f"Число {num:2}: {status_ternary}")
    
    # Вложенные условия
    print("\n4. Вложенные условия:")
    
    def describe_weather(temperature, is_sunny, is_windy):
        if temperature > 25:
            if is_sunny:
                if is_windy:
                    return "Жарко, солнечно и ветрено"
                else:
                    return "Жарко и солнечно"
            else:
                return "Жарко, но не солнечно"
        elif temperature > 15:
            if is_sunny:
                return "Тепло и солнечно"
            else:
                return "Тепло, но облачно"
        else:
            return "Прохладно"
    
    weather_conditions = [
        (30, True, False),
        (28, True, True),
        (20, True, False),
        (18, False, False),
        (10, True, False),
    ]
    
    for temp, sunny, windy in weather_conditions:
        description = describe_weather(temp, sunny, windy)
        print(f"T={temp}°C, солнце={sunny}, ветер={windy}: {description}")
    
    # Множественные условия
    print("\n5. Множественные условия:")
    
    def check_access(username, password, is_active, role):
        if username == "admin" and password == "secret" and is_active:
            if role == "administrator":
                return "Полный доступ"
            else:
                return "Ограниченный доступ"
        elif username == "admin" and password == "secret":
            return "Аккаунт заблокирован"
        elif username == "admin":
            return "Неверный пароль"
        else:
            return "Пользователь не найден"
    
    access_tests = [
        ("admin", "secret", True, "administrator"),
        ("admin", "secret", True, "user"),
        ("admin", "secret", False, "administrator"),
        ("admin", "wrong", True, "administrator"),
        ("user", "password", True, "user"),
    ]
    
    for username, password, is_active, role in access_tests:
        result = check_access(username, password, is_active, role)
        print(f"{username}/{password}, active={is_active}, role={role}: {result}")
    
    print()

def example_05_loops():
    """
    Пример 5: Циклы
    
    Демонстрирует различные типы циклов и их применение.
    """
    print("=== Пример 5: Циклы ===")
    
    # Цикл for с range()
    print("1. Цикл for с range():")
    
    print("range(5):", end=" ")
    for i in range(5):
        print(i, end=" ")
    print()
    
    print("range(2, 8):", end=" ")
    for i in range(2, 8):
        print(i, end=" ")
    print()
    
    print("range(0, 10, 2):", end=" ")
    for i in range(0, 10, 2):
        print(i, end=" ")
    print()
    
    print("range(10, 0, -1):", end=" ")
    for i in range(10, 0, -1):
        print(i, end=" ")
    print()
    
    # Цикл for с последовательностями
    print("\n2. Цикл for с последовательностями:")
    
    # Строка
    word = "Python"
    print(f"Символы в '{word}':", end=" ")
    for char in word:
        print(char, end=" ")
    print()
    
    # Список
    fruits = ["яблоко", "банан", "апельсин"]
    print("Фрукты:")
    for fruit in fruits:
        print(f"  - {fruit}")
    
    # enumerate() для получения индексов
    print("Фрукты с индексами:")
    for i, fruit in enumerate(fruits):
        print(f"  {i}: {fruit}")
    
    # zip() для параллельной итерации
    colors = ["красный", "жёлтый", "оранжевый"]
    print("Фрукты и цвета:")
    for fruit, color in zip(fruits, colors):
        print(f"  {fruit} - {color}")
    
    # Цикл while
    print("\n3. Цикл while:")
    
    # Простой while
    print("Обратный отсчёт:")
    count = 5
    while count > 0:
        print(f"  {count}")
        count -= 1
    print("  Пуск!")
    
    # While с более сложным условием
    print("\nПоиск числа:")
    numbers = [1, 3, 7, 9, 12, 15, 18]
    target = 12
    index = 0
    
    while index < len(numbers):
        if numbers[index] == target:
            print(f"Число {target} найдено на позиции {index}")
            break
        index += 1
    else:
        print(f"Число {target} не найдено")
    
    # Управление циклами: break и continue
    print("\n4. Управление циклами (break и continue):")
    
    print("Поиск первого чётного числа:")
    numbers = [1, 3, 7, 8, 9, 12, 15]
    for num in numbers:
        if num % 2 == 1:  # Нечётное число
            print(f"  Пропускаем {num} (нечётное)")
            continue
        else:  # Чётное число
            print(f"  Найдено первое чётное: {num}")
            break
    
    print("\nВывод только положительных чисел:")
    numbers = [-2, -1, 0, 1, 2, 3, -4, 5]
    for num in numbers:
        if num <= 0:
            continue
        print(f"  Положительное: {num}")
    
    # Вложенные циклы
    print("\n5. Вложенные циклы:")
    
    print("Таблица умножения 3x3:")
    for i in range(1, 4):
        for j in range(1, 4):
            product = i * j
            print(f"{i}x{j}={product:2}", end="  ")
        print()  # Новая строка после каждого ряда
    
    # Блок else в циклах
    print("\n6. Блок else в циклах:")
    
    print("Поиск числа 7 в списке [1, 3, 5, 7, 9]:")
    numbers = [1, 3, 5, 7, 9]
    for num in numbers:
        print(f"  Проверяем {num}")
        if num == 7:
            print("  Число 7 найдено!")
            break
    else:
        print("  Число 7 не найдено")
    
    print("\nПоиск числа 6 в том же списке:")
    for num in numbers:
        print(f"  Проверяем {num}")
        if num == 6:
            print("  Число 6 найдено!")
            break
    else:
        print("  Число 6 не найдено (else блок выполнился)")
    
    print()

def example_06_input_output():
    """
    Пример 6: Ввод и вывод данных
    
    Демонстрирует функции input() и print() с различными параметрами.
    """
    print("=== Пример 6: Ввод и вывод данных ===")
    
    # Функция print() с различными параметрами
    print("1. Функция print() с параметрами:")
    
    # Базовый вывод
    print("Простой вывод")
    
    # Множественные аргументы
    print("Несколько", "аргументов", "через", "запятую")
    
    # Параметр sep (разделитель)
    print("A", "B", "C", sep="-")
    print("2023", "12", "25", sep="/")
    
    # Параметр end (завершение)
    print("Первая часть", end=" ")
    print("Вторая часть")
    
    print("Загрузка", end="")
    for i in range(5):
        print(".", end="", flush=True)
        # В реальном коде здесь была бы пауза: time.sleep(0.5)
    print(" Готово!")
    
    # Форматированный вывод
    print("\n2. Форматированный вывод:")
    
    name = "Анна"
    age = 28
    salary = 75000.75
    
    # f-строки с различными форматами
    print(f"Имя: {name}")
    print(f"Возраст: {age} лет")
    print(f"Зарплата: {salary:.2f} руб.")
    print(f"Зарплата: {salary:,.2f} руб.")  # С разделителями тысяч
    print(f"Зарплата: {salary:>15,.2f} руб.")  # Выравнивание по правому краю
    
    # Форматирование чисел
    pi = 3.14159265359
    print(f"π = {pi:.2f}")
    print(f"π = {pi:.5f}")
    print(f"π = {pi:10.3f}")  # Ширина поля 10, 3 знака после запятой
    
    # Форматирование даты и времени
    now = datetime.now()
    print(f"Текущее время: {now:%Y-%m-%d %H:%M:%S}")
    print(f"Дата: {now:%d.%m.%Y}")
    
    # Имитация функции input() (в реальном коде раскомментируйте)
    print("\n3. Функция input() (имитация):")
    
    # В реальном коде:
    # name = input("Введите ваше имя: ")
    # print(f"Привет, {name}!")
    
    # Имитация для демонстрации
    print("Имитация: Введите ваше имя: ", end="")
    name = "Пользователь"  # Имитируем ввод
    print(name)
    print(f"Привет, {name}!")
    
    # Ввод чисел с обработкой ошибок
    print("\n4. Ввод чисел с обработкой ошибок:")
    
    def safe_input_int(prompt):
        """Безопасный ввод целого числа"""
        while True:
            try:
                # В реальном коде: value = input(prompt)
                # Для демонстрации используем заранее заданные значения
                print(f"Имитация: {prompt}", end="")
                value = "25"  # Имитируем ввод
                print(value)
                return int(value)
            except ValueError:
                print("Ошибка: введите целое число!")
    
    def safe_input_float(prompt):
        """Безопасный ввод числа с плавающей точкой"""
        while True:
            try:
                # В реальном коде: value = input(prompt)
                print(f"Имитация: {prompt}", end="")
                value = "175.5"  # Имитируем ввод
                print(value)
                return float(value)
            except ValueError:
                print("Ошибка: введите число!")
    
    age = safe_input_int("Введите ваш возраст: ")
    height = safe_input_float("Введите ваш рост (см): ")
    
    print(f"Возраст: {age} лет")
    print(f"Рост: {height} см")
    
    # Создание таблицы
    print("\n5. Создание таблицы:")
    
    students = [
        ("Анна", 85, 92, 78),
        ("Борис", 91, 88, 84),
        ("Виктор", 76, 82, 90),
        ("Галина", 88, 95, 87),
    ]
    
    # Заголовок таблицы
    print("┌" + "─" * 10 + "┬" + "─" * 8 + "┬" + "─" * 8 + "┬" + "─" * 8 + "┬" + "─" * 10 + "┐")
    print(f"│{'Имя':^10}│{'Мат':^8}│{'Физ':^8}│{'Инф':^8}│{'Средний':^10}│")
    print("├" + "─" * 10 + "┼" + "─" * 8 + "┼" + "─" * 8 + "┼" + "─" * 8 + "┼" + "─" * 10 + "┤")
    
    # Строки данных
    for name, math, physics, cs in students:
        average = (math + physics + cs) / 3
        print(f"│{name:^10}│{math:^8}│{physics:^8}│{cs:^8}│{average:^10.1f}│")
    
    # Подвал таблицы
    print("└" + "─" * 10 + "┴" + "─" * 8 + "┴" + "─" * 8 + "┴" + "─" * 8 + "┴" + "─" * 10 + "┘")
    
    print()

def example_07_scope():
    """
    Пример 7: Область видимости переменных
    
    Демонстрирует локальные, глобальные переменные
    и правило LEGB.
    """
    print("=== Пример 7: Область видимости переменных ===")
    
    # Глобальная переменная
    global_var = "Я глобальная переменная"
    
    print("1. Локальные и глобальные переменные:")
    
    def demo_scope():
        local_var = "Я локальная переменная"
        print(f"  Внутри функции - глобальная: {global_var}")
        print(f"  Внутри функции - локальная: {local_var}")
        return local_var
    
    result = demo_scope()
    print(f"Вне функции - глобальная: {global_var}")
    print(f"Возвращённое значение: {result}")
    # print(local_var)  # Это вызовет ошибку!
    
    # Изменение глобальной переменной
    print("\n2. Изменение глобальной переменной:")
    
    counter = 0
    
    def increment_global():
        global counter
        counter += 1
        print(f"  Внутри функции counter = {counter}")
    
    def increment_local():
        counter = 1  # Создаёт локальную переменную!
        counter += 1
        print(f"  Локальная переменная counter = {counter}")
    
    print(f"Начальное значение counter: {counter}")
    increment_global()
    print(f"После increment_global(): {counter}")
    increment_local()
    print(f"После increment_local(): {counter}")
    
    # Правило LEGB
    print("\n3. Правило LEGB (Local, Enclosing, Global, Built-in):")
    
    x = "глобальная x"
    
    def outer():
        x = "enclosing x"
        print(f"  В outer() до inner(): {x}")
        
        def inner():
            x = "локальная x"
            print(f"    В inner(): {x}")
        
        inner()
        print(f"  В outer() после inner(): {x}")
    
    print(f"В глобальной области: {x}")
    outer()
    print(f"Снова в глобальной области: {x}")
    
    # Демонстрация поиска в разных областях
    print("\n4. Поиск переменных в разных областях:")
    
    # Встроенная функция
    print(f"Built-in: len('hello') = {len('hello')}")
    
    # Глобальная переменная
    message = "Глобальное сообщение"
    
    def demonstrate_legb():
        # Локальная переменная с тем же именем
        message = "Локальное сообщение"
        
        def inner_function():
            # Здесь Python найдёт локальную переменную из outer функции
            print(f"    Внутри inner_function: {message}")
        
        print(f"  В demonstrate_legb: {message}")
        inner_function()
    
    print(f"В глобальной области: {message}")
    demonstrate_legb()
    
    # nonlocal keyword
    print("\n5. Ключевое слово nonlocal:")
    
    def outer_with_nonlocal():
        x = "outer x"
        
        def inner_modify():
            nonlocal x  # Изменяем переменную из объемлющей области
            x = "изменённая x"
            print(f"    В inner_modify: {x}")
        
        print(f"  В outer до inner_modify: {x}")
        inner_modify()
        print(f"  В outer после inner_modify: {x}")
    
    outer_with_nonlocal()
    
    print()

def example_08_practical_applications():
    """
    Пример 8: Практические применения
    
    Реальные примеры использования изученных конструкций.
    """
    print("=== Пример 8: Практические применения ===")
    
    # Калькулятор
    print("1. Простой калькулятор:")
    
    def calculator(a, b, operation):
        """Простой калькулятор"""
        if operation == "+":
            return a + b
        elif operation == "-":
            return a - b
        elif operation == "*":
            return a * b
        elif operation == "/":
            if b != 0:
                return a / b
            else:
                return "Ошибка: деление на ноль"
        else:
            return "Ошибка: неизвестная операция"
    
    # Тестируем калькулятор
    test_operations = [
        (10, 5, "+"),
        (10, 5, "-"),
        (10, 5, "*"),
        (10, 5, "/"),
        (10, 0, "/"),
        (10, 5, "%"),
    ]
    
    for a, b, op in test_operations:
        result = calculator(a, b, op)
        print(f"  {a} {op} {b} = {result}")
    
    # Анализ текста
    print("\n2. Анализ текста:")
    
    def analyze_text(text):
        """Анализирует текст и возвращает статистику"""
        # Подсчёт символов
        total_chars = len(text)
        chars_no_spaces = len(text.replace(" ", ""))
        
        # Подсчёт слов
        words = text.split()
        word_count = len(words)
        
        # Подсчёт гласных и согласных
        vowels = "аеёиоуыэюяaeiouy"
        vowel_count = sum(1 for char in text.lower() if char in vowels)
        
        # Подсчёт предложений (упрощённо)
        sentence_count = text.count(".") + text.count("!") + text.count("?")
        
        return {
            "символов": total_chars,
            "символов_без_пробелов": chars_no_spaces,
            "слов": word_count,
            "гласных": vowel_count,
            "предложений": sentence_count,
        }
    
    sample_text = "Python — это высокоуровневый язык программирования. Он прост в изучении!"
    analysis = analyze_text(sample_text)
    
    print(f"Текст: '{sample_text}'")
    print("Анализ:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    # Генератор паролей
    print("\n3. Генератор паролей:")
    
    def generate_password(length=8, include_symbols=True):
        """Генерирует пароль заданной длины"""
        import string
        import random
        
        # Наборы символов
        letters = string.ascii_letters  # a-z, A-Z
        digits = string.digits          # 0-9
        symbols = "!@#$%^&*"
        
        # Базовый набор
        chars = letters + digits
        if include_symbols:
            chars += symbols
        
        # Генерируем пароль
        password = ""
        for _ in range(length):
            password += random.choice(chars)
        
        return password
    
    print("Сгенерированные пароли:")
    for length in [8, 12, 16]:
        password = generate_password(length)
        print(f"  Длина {length}: {password}")
    
    # Конвертер единиц измерения
    print("\n4. Конвертер единиц измерения:")
    
    def convert_temperature(value, from_unit, to_unit):
        """Конвертирует температуру между разными единицами"""
        # Сначала переводим в Цельсии
        if from_unit.lower() == "f":  # Fahrenheit
            celsius = (value - 32) * 5 / 9
        elif from_unit.lower() == "k":  # Kelvin
            celsius = value - 273.15
        else:  # Celsius
            celsius = value
        
        # Затем переводим в нужную единицу
        if to_unit.lower() == "f":  # Fahrenheit
            return celsius * 9 / 5 + 32
        elif to_unit.lower() == "k":  # Kelvin
            return celsius + 273.15
        else:  # Celsius
            return celsius
    
    conversions = [
        (0, "C", "F"),
        (100, "C", "F"),
        (32, "F", "C"),
        (273.15, "K", "C"),
        (25, "C", "K"),
    ]
    
    print("Конверсии температуры:")
    for value, from_u, to_u in conversions:
        result = convert_temperature(value, from_u, to_u)
        print(f"  {value}°{from_u} = {result:.2f}°{to_u}")
    
    # Игра "Угадай число"
    print("\n5. Игра 'Угадай число' (автоматическая версия):")
    
    def guess_number_auto(target, max_attempts=10):
        """Автоматическая версия игры 'угадай число'"""
        import random
        
        low, high = 1, 100
        attempts = 0
        
        print(f"  Загадано число от 1 до 100: {target}")
        
        while attempts < max_attempts:
            attempts += 1
            guess = random.randint(low, high)
            
            print(f"  Попытка {attempts}: пробую {guess}")
            
            if guess == target:
                print(f"  Угадал за {attempts} попыток!")
                return attempts
            elif guess < target:
                print(f"    Мало")
                low = guess + 1
            else:
                print(f"    Много")
                high = guess - 1
        
        print(f"  Не угадал за {max_attempts} попыток")
        return max_attempts
    
    # Запускаем игру
    target_number = 42
    attempts_used = guess_number_auto(target_number)
    
    print()

def main():
    """
    Главная функция для запуска всех примеров
    """
    print("🔧 ПРАКТИЧЕСКИЕ ПРИМЕРЫ: БАЗОВЫЕ КОНСТРУКЦИИ PYTHON")
    print("=" * 70)
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    examples = [
        example_01_variables_and_types,
        example_02_string_operations,
        example_03_operators,
        example_04_conditional_statements,
        example_05_loops,
        example_06_input_output,
        example_07_scope,
        example_08_practical_applications,
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"❌ Ошибка в примере {i}: {e}")
            print()
    
    print("=" * 70)
    print("✅ Все примеры выполнены успешно!")
    print("📚 Переходите к изучению следующего раздела: Структуры данных")
    print("=" * 70)

if __name__ == "__main__":
    main() 