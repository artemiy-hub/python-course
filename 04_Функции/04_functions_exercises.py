#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Функции в Python

Этот файл содержит практические упражнения для закрепления знаний:
- Создание и использование функций
- Работа с параметрами и аргументами
- Область видимости и замыкания
- Декораторы и их применение
- Генераторы и итераторы
- Функциональное программирование

Каждое упражнение имеет описание задачи и закомментированное решение.
"""

import time
import functools
from typing import List, Dict, Callable, Optional, Any


def exercise_01():
    """
    Упражнение 1: Калькулятор с функциями
    
    Создайте калькулятор, который:
    1. Имеет отдельные функции для каждой операции (+, -, *, /, **, %)
    2. Функцию для валидации входных данных
    3. Функцию главного меню
    4. Обработку ошибок деления на ноль
    5. Историю операций (используйте замыкание)
    """
    print("=== Упражнение 1: Калькулятор с функциями ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # def create_calculator():
    #     """Создает калькулятор с историей операций"""
    #     history = []
    #     
    #     def add(a, b):
    #         result = a + b
    #         history.append(f"{a} + {b} = {result}")
    #         return result
    #     
    #     def subtract(a, b):
    #         result = a - b
    #         history.append(f"{a} - {b} = {result}")
    #         return result
    #     
    #     def multiply(a, b):
    #         result = a * b
    #         history.append(f"{a} * {b} = {result}")
    #         return result
    #     
    #     def divide(a, b):
    #         if b == 0:
    #             raise ValueError("Деление на ноль невозможно!")
    #         result = a / b
    #         history.append(f"{a} / {b} = {result}")
    #         return result
    #     
    #     def power(a, b):
    #         result = a ** b
    #         history.append(f"{a} ** {b} = {result}")
    #         return result
    #     
    #     def modulo(a, b):
    #         if b == 0:
    #             raise ValueError("Деление на ноль невозможно!")
    #         result = a % b
    #         history.append(f"{a} % {b} = {result}")
    #         return result
    #     
    #     def get_history():
    #         return history.copy()
    #     
    #     def clear_history():
    #         history.clear()
    #         return "История очищена"
    #     
    #     operations = {
    #         "+": add,
    #         "-": subtract,
    #         "*": multiply,
    #         "/": divide,
    #         "**": power,
    #         "%": modulo
    #     }
    #     
    #     def validate_numbers(a, b):
    #         """Валидация входных данных"""
    #         try:
    #             return float(a), float(b)
    #         except ValueError:
    #             raise ValueError("Введите корректные числа!")
    #     
    #     def calculate(operation, a, b):
    #         """Основная функция вычисления"""
    #         if operation not in operations:
    #             raise ValueError(f"Неизвестная операция: {operation}")
    #         
    #         num_a, num_b = validate_numbers(a, b)
    #         return operations[operation](num_a, num_b)
    #     
    #     def show_menu():
    #         """Показать меню операций"""
    #         print("\nДоступные операции:")
    #         for op in operations.keys():
    #             print(f"  {op}")
    #         print("  history - показать историю")
    #         print("  clear - очистить историю")
    #         print("  quit - выход")
    #     
    #     return {
    #         "calculate": calculate,
    #         "history": get_history,
    #         "clear": clear_history,
    #         "menu": show_menu
    #     }
    # 
    # # Демонстрация работы
    # calc = create_calculator()
    # 
    # print("Калькулятор создан!")
    # calc["menu"]()
    # 
    # # Примеры операций
    # try:
    #     print(f"\n5 + 3 = {calc['calculate']('+', 5, 3)}")
    #     print(f"10 - 4 = {calc['calculate']('-', 10, 4)}")
    #     print(f"6 * 7 = {calc['calculate']('*', 6, 7)}")
    #     print(f"15 / 3 = {calc['calculate']('/', 15, 3)}")
    #     print(f"2 ** 4 = {calc['calculate']('**', 2, 4)}")
    #     
    #     print("\nИстория операций:")
    #     for operation in calc["history"]():
    #         print(f"  {operation}")
    #         
    # except ValueError as e:
    #     print(f"Ошибка: {e}")


def exercise_02():
    """
    Упражнение 2: Система декораторов для логирования
    
    Создайте систему декораторов:
    1. @log_time - логирует время выполнения функции
    2. @log_args - логирует аргументы функции
    3. @log_result - логирует результат функции
    4. @count_calls - считает количество вызовов
    5. @cache_result - кеширует результаты функции
    """
    print("=== Упражнение 2: Система декораторов для логирования ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # def log_time(func):
    #     """Декоратор для логирования времени выполнения"""
    #     @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         start_time = time.perf_counter()
    #         result = func(*args, **kwargs)
    #         end_time = time.perf_counter()
    #         execution_time = end_time - start_time
    #         print(f"⏱️ {func.__name__} выполнялась {execution_time:.4f} секунд")
    #         return result
    #     return wrapper
    # 
    # def log_args(func):
    #     """Декоратор для логирования аргументов"""
    #     @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         args_str = ", ".join(map(str, args))
    #         kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    #         all_args = ", ".join(filter(None, [args_str, kwargs_str]))
    #         print(f"📥 {func.__name__}({all_args})")
    #         return func(*args, **kwargs)
    #     return wrapper
    # 
    # def log_result(func):
    #     """Декоратор для логирования результата"""
    #     @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         result = func(*args, **kwargs)
    #         print(f"📤 {func.__name__} вернула: {result}")
    #         return result
    #     return wrapper
    # 
    # def count_calls(func):
    #     """Декоратор для подсчета вызовов"""
    #     func.call_count = 0
    #     
    #     @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         func.call_count += 1
    #         print(f"📊 {func.__name__} вызвана {func.call_count} раз")
    #         return func(*args, **kwargs)
    #     
    #     wrapper.call_count = func.call_count
    #     return wrapper
    # 
    # def cache_result(func):
    #     """Декоратор для кеширования результатов"""
    #     cache = {}
    #     
    #     @functools.wraps(func)
    #     def wrapper(*args, **kwargs):
    #         # Создаем ключ из аргументов
    #         key = str(args) + str(sorted(kwargs.items()))
    #         
    #         if key in cache:
    #             print(f"💾 Результат из кеша для {func.__name__}")
    #             return cache[key]
    #         
    #         result = func(*args, **kwargs)
    #         cache[key] = result
    #         print(f"💿 Результат сохранен в кеш для {func.__name__}")
    #         return result
    #     
    #     wrapper.cache = cache
    #     return wrapper
    # 
    # # Тестирование декораторов
    # @log_time
    # @log_args
    # @log_result
    # @count_calls
    # @cache_result
    # def factorial(n):
    #     """Вычисляет факториал числа"""
    #     if n <= 1:
    #         return 1
    #     result = 1
    #     for i in range(2, n + 1):
    #         result *= i
    #     time.sleep(0.01)  # Имитация вычислений
    #     return result
    # 
    # print("Тестирование декораторов:")
    # print(f"factorial(5) = {factorial(5)}")
    # print(f"factorial(5) = {factorial(5)}")  # Из кеша
    # print(f"factorial(6) = {factorial(6)}")
    # print(f"Всего вызовов: {factorial.call_count}")


def exercise_03():
    """
    Упражнение 3: Генератор паролей
    
    Создайте генератор паролей с функциями:
    1. Генерация паролей разной сложности
    2. Проверка силы пароля
    3. Генератор, который создает бесконечную последовательность паролей
    4. Функция для создания множества уникальных паролей
    5. Сохранение паролей в файл (генератор для записи)
    """
    print("=== Упражнение 3: Генератор паролей ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # import random
    # import string
    # 
    # def generate_password(length=12, use_uppercase=True, use_lowercase=True, 
    #                      use_digits=True, use_symbols=True):
    #     """Генерирует пароль заданной длины и сложности"""
    #     chars = ""
    #     
    #     if use_lowercase:
    #         chars += string.ascii_lowercase
    #     if use_uppercase:
    #         chars += string.ascii_uppercase
    #     if use_digits:
    #         chars += string.digits
    #     if use_symbols:
    #         chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    #     
    #     if not chars:
    #         raise ValueError("Должен быть выбран хотя бы один тип символов!")
    #     
    #     password = ''.join(random.choice(chars) for _ in range(length))
    #     return password
    # 
    # def check_password_strength(password):
    #     """Проверяет силу пароля"""
    #     score = 0
    #     feedback = []
    #     
    #     if len(password) >= 8:
    #         score += 1
    #     else:
    #         feedback.append("Добавьте больше символов (минимум 8)")
    #     
    #     if any(c.islower() for c in password):
    #         score += 1
    #     else:
    #         feedback.append("Добавьте строчные буквы")
    #     
    #     if any(c.isupper() for c in password):
    #         score += 1
    #     else:
    #         feedback.append("Добавьте заглавные буквы")
    #     
    #     if any(c.isdigit() for c in password):
    #         score += 1
    #     else:
    #         feedback.append("Добавьте цифры")
    #     
    #     if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
    #         score += 1
    #     else:
    #         feedback.append("Добавьте специальные символы")
    #     
    #     strength_levels = {
    #         0: "Очень слабый",
    #         1: "Слабый",
    #         2: "Средний", 
    #         3: "Хороший",
    #         4: "Сильный",
    #         5: "Очень сильный"
    #     }
    #     
    #     return {
    #         "score": score,
    #         "strength": strength_levels[score],
    #         "feedback": feedback
    #     }
    # 
    # def password_generator(length=12, **kwargs):
    #     """Бесконечный генератор паролей"""
    #     while True:
    #         yield generate_password(length, **kwargs)
    # 
    # def generate_unique_passwords(count, length=12, max_attempts=1000, **kwargs):
    #     """Генерирует набор уникальных паролей"""
    #     passwords = set()
    #     attempts = 0
    #     
    #     while len(passwords) < count and attempts < max_attempts:
    #         password = generate_password(length, **kwargs)
    #         passwords.add(password)
    #         attempts += 1
    #     
    #     if len(passwords) < count:
    #         print(f"⚠️ Удалось создать только {len(passwords)} уникальных паролей из {count}")
    #     
    #     return list(passwords)
    # 
    # def save_passwords_generator(passwords, filename="passwords.txt"):
    #     """Генератор для сохранения паролей в файл"""
    #     with open(filename, 'w', encoding='utf-8') as file:
    #         for i, password in enumerate(passwords, 1):
    #             strength = check_password_strength(password)
    #             line = f"{i:3d}. {password:<20} | Сила: {strength['strength']}\n"
    #             file.write(line)
    #             yield f"Сохранен пароль {i}: {password} (сила: {strength['strength']})"
    # 
    # # Демонстрация работы
    # print("1. Генерация паролей разной сложности:")
    # simple_password = generate_password(8, use_symbols=False)
    # complex_password = generate_password(16)
    # 
    # print(f"Простой пароль: {simple_password}")
    # print(f"Сложный пароль: {complex_password}")
    # 
    # print("\n2. Проверка силы паролей:")
    # for pwd in [simple_password, complex_password, "123456", "MySecure!Pass123"]:
    #     strength = check_password_strength(pwd)
    #     print(f"'{pwd}': {strength['strength']} (балл: {strength['score']}/5)")
    #     if strength['feedback']:
    #         print(f"  Рекомендации: {', '.join(strength['feedback'])}")
    # 
    # print("\n3. Бесконечный генератор паролей:")
    # pwd_gen = password_generator(10)
    # print("Первые 5 паролей из генератора:")
    # for i, password in enumerate(pwd_gen):
    #     if i >= 5:
    #         break
    #     print(f"  {i+1}. {password}")
    # 
    # print("\n4. Генерация уникальных паролей:")
    # unique_passwords = generate_unique_passwords(5, length=8)
    # print(f"Создано {len(unique_passwords)} уникальных паролей:")
    # for i, pwd in enumerate(unique_passwords, 1):
    #     print(f"  {i}. {pwd}")
    # 
    # print("\n5. Сохранение паролей:")
    # save_gen = save_passwords_generator(unique_passwords, "temp_passwords.txt")
    # for message in save_gen:
    #     print(f"  {message}")


def exercise_04():
    """
    Упражнение 4: Функциональная обработка данных
    
    Создайте систему для обработки данных о студентах:
    1. Функции высшего порядка для фильтрации и преобразования
    2. Композицию функций для сложной обработки
    3. Частичное применение функций
    4. Каррирование функций
    5. Пайплайн обработки данных
    """
    print("=== Упражнение 4: Функциональная обработка данных ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # from functools import reduce, partial
    # 
    # # Тестовые данные
    # students = [
    #     {"name": "Алиса", "age": 20, "grades": [85, 90, 78, 92], "major": "CS"},
    #     {"name": "Боб", "age": 22, "grades": [70, 75, 80, 85], "major": "Math"},
    #     {"name": "Чарли", "age": 19, "grades": [95, 88, 91, 94], "major": "CS"},
    #     {"name": "Диана", "age": 21, "grades": [60, 65, 70, 75], "major": "Physics"},
    #     {"name": "Ева", "age": 20, "grades": [88, 85, 90, 87], "major": "CS"},
    #     {"name": "Фрэнк", "age": 23, "grades": [45, 50, 55, 60], "major": "Math"}
    # ]
    # 
    # # Функции высшего порядка
    # def filter_by(predicate, data):
    #     """Фильтрует данные по предикату"""
    #     return list(filter(predicate, data))
    # 
    # def map_by(transformer, data):
    #     """Преобразует данные с помощью функции"""
    #     return list(map(transformer, data))
    # 
    # def reduce_by(reducer, data, initial=None):
    #     """Сворачивает данные к одному значению"""
    #     if initial is None:
    #         return reduce(reducer, data)
    #     return reduce(reducer, data, initial)
    # 
    # # Композиция функций
    # def compose(*functions):
    #     """Создает композицию функций"""
    #     def composed(data):
    #         result = data
    #         for func in reversed(functions):
    #             result = func(result)
    #         return result
    #     return composed
    # 
    # def pipe(*functions):
    #     """Создает пайплайн функций (слева направо)"""
    #     def pipeline(data):
    #         result = data
    #         for func in functions:
    #             result = func(result)
    #         return result
    #     return pipeline
    # 
    # # Каррирование
    # def curry(func):
    #     """Каррирует функцию"""
    #     def curried(*args, **kwargs):
    #         if len(args) + len(kwargs) >= func.__code__.co_argcount:
    #             return func(*args, **kwargs)
    #         return lambda *more_args, **more_kwargs: curried(
    #             *(args + more_args), **{**kwargs, **more_kwargs}
    #         )
    #     return curried
    # 
    # # Вспомогательные функции для работы со студентами
    # def calculate_average(grades):
    #     """Вычисляет средний балл"""
    #     return sum(grades) / len(grades) if grades else 0
    # 
    # def add_average_grade(student):
    #     """Добавляет средний балл к данным студента"""
    #     return {**student, "average": calculate_average(student["grades"])}
    # 
    # def is_cs_student(student):
    #     """Проверяет, изучает ли студент CS"""
    #     return student["major"] == "CS"
    # 
    # def has_high_grades(student, threshold=85):
    #     """Проверяет, есть ли у студента высокие оценки"""
    #     return student.get("average", 0) >= threshold
    # 
    # @curry
    # def filter_by_major(major, student):
    #     """Каррированная функция фильтрации по специальности"""
    #     return student["major"] == major
    # 
    # @curry
    # def filter_by_age_range(min_age, max_age, student):
    #     """Каррированная функция фильтрации по возрасту"""
    #     return min_age <= student["age"] <= max_age
    # 
    # # Демонстрация функциональной обработки
    # print("1. Базовая обработка данных:")
    # 
    # # Добавляем средние баллы
    # students_with_avg = map_by(add_average_grade, students)
    # for student in students_with_avg:
    #     print(f"{student['name']}: средний балл {student['average']:.1f}")
    # 
    # print("\n2. Фильтрация данных:")
    # 
    # # Студенты CS
    # cs_students = filter_by(is_cs_student, students_with_avg)
    # print(f"Студенты CS: {[s['name'] for s in cs_students]}")
    # 
    # # Студенты с высокими баллами
    # high_performers = filter_by(lambda s: has_high_grades(s, 85), students_with_avg)
    # print(f"Отличники (средний >= 85): {[s['name'] for s in high_performers]}")
    # 
    # print("\n3. Каррированные функции:")
    # 
    # # Частичное применение
    # cs_filter = filter_by_major("CS")
    # young_filter = filter_by_age_range(18, 20)
    # 
    # cs_students = filter_by(cs_filter, students_with_avg)
    # young_students = filter_by(young_filter, students_with_avg)
    # 
    # print(f"CS студенты: {[s['name'] for s in cs_students]}")
    # print(f"Молодые студенты (18-20): {[s['name'] for s in young_students]}")
    # 
    # print("\n4. Пайплайн обработки:")
    # 
    # # Создаем пайплайн для анализа CS студентов
    # analyze_cs_students = pipe(
    #     lambda data: map_by(add_average_grade, data),
    #     lambda data: filter_by(is_cs_student, data),
    #     lambda data: filter_by(lambda s: has_high_grades(s, 80), data),
    #     lambda data: map_by(lambda s: {"name": s["name"], "average": s["average"]}, data)
    # )
    # 
    # top_cs_students = analyze_cs_students(students)
    # print("Лучшие CS студенты:")
    # for student in top_cs_students:
    #     print(f"  {student['name']}: {student['average']:.1f}")
    # 
    # print("\n5. Агрегация данных:")
    # 
    # # Статистика по специальностям
    # def group_by_major(students):
    #     """Группирует студентов по специальности"""
    #     groups = {}
    #     for student in students:
    #         major = student["major"]
    #         if major not in groups:
    #             groups[major] = []
    #         groups[major].append(student)
    #     return groups
    # 
    # grouped = group_by_major(students_with_avg)
    # print("Статистика по специальностям:")
    # for major, major_students in grouped.items():
    #     avg_grade = sum(s["average"] for s in major_students) / len(major_students)
    #     print(f"  {major}: {len(major_students)} студентов, средний балл {avg_grade:.1f}")


def exercise_05():
    """
    Упражнение 5: Система задач с декораторами и генераторами
    
    Создайте систему управления задачами:
    1. Декоратор @task для регистрации функций как задач
    2. Декоратор @retry для повторного выполнения при ошибках
    3. Генератор для выполнения задач пакетами
    4. Функции-фабрики для создания специализированных задач
    5. Система приоритетов и зависимостей
    """
    print("=== Упражнение 5: Система задач с декораторами и генераторами ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # import random
    # from collections import deque
    # 
    # class TaskManager:
    #     """Менеджер задач с поддержкой декораторов и генераторов"""
    #     
    #     def __init__(self):
    #         self.tasks = {}
    #         self.task_queue = deque()
    #         self.completed_tasks = []
    #         self.failed_tasks = []
    #     
    #     def task(self, name=None, priority=1, dependencies=None):
    #         """Декоратор для регистрации задач"""
    #         def decorator(func):
    #             task_name = name or func.__name__
    #             task_info = {
    #                 "name": task_name,
    #                 "function": func,
    #                 "priority": priority,
    #                 "dependencies": dependencies or [],
    #                 "status": "registered"
    #             }
    #             self.tasks[task_name] = task_info
    #             print(f"📝 Задача '{task_name}' зарегистрирована")
    #             return func
    #         return decorator
    #     
    #     def retry(self, max_attempts=3, delay=1):
    #         """Декоратор для повторного выполнения задач"""
    #         def decorator(func):
    #             @functools.wraps(func)
    #             def wrapper(*args, **kwargs):
    #                 for attempt in range(max_attempts):
    #                     try:
    #                         return func(*args, **kwargs)
    #                     except Exception as e:
    #                         if attempt == max_attempts - 1:
    #                             print(f"❌ Задача '{func.__name__}' провалена после {max_attempts} попыток")
    #                             raise e
    #                         print(f"⚠️ Попытка {attempt + 1} неудачна: {e}")
    #                         time.sleep(delay)
    #             return wrapper
    #         return decorator
    #     
    #     def add_to_queue(self, task_name, *args, **kwargs):
    #         """Добавляет задачу в очередь выполнения"""
    #         if task_name in self.tasks:
    #             task_item = {
    #                 "name": task_name,
    #                 "args": args,
    #                 "kwargs": kwargs,
    #                 "priority": self.tasks[task_name]["priority"]
    #             }
    #             self.task_queue.append(task_item)
    #             print(f"➕ Задача '{task_name}' добавлена в очередь")
    #         else:
    #             print(f"❌ Задача '{task_name}' не найдена")
    #     
    #     def execute_task(self, task_name, *args, **kwargs):
    #         """Выполняет одну задачу"""
    #         if task_name not in self.tasks:
    #             raise ValueError(f"Задача '{task_name}' не найдена")
    #         
    #         task_info = self.tasks[task_name]
    #         
    #         # Проверяем зависимости
    #         for dep in task_info["dependencies"]:
    #             if dep not in [t["name"] for t in self.completed_tasks]:
    #                 raise RuntimeError(f"Зависимость '{dep}' не выполнена")
    #         
    #         print(f"🔄 Выполняется задача '{task_name}'...")
    #         try:
    #             result = task_info["function"](*args, **kwargs)
    #             self.completed_tasks.append({
    #                 "name": task_name,
    #                 "result": result,
    #                 "timestamp": time.time()
    #             })
    #             print(f"✅ Задача '{task_name}' выполнена успешно")
    #             return result
    #         except Exception as e:
    #             self.failed_tasks.append({
    #                 "name": task_name,
    #                 "error": str(e),
    #                 "timestamp": time.time()
    #             })
    #             print(f"❌ Задача '{task_name}' провалена: {e}")
    #             raise
    #     
    #     def batch_executor(self, batch_size=3):
    #         """Генератор для выполнения задач пакетами"""
    #         # Сортируем по приоритету
    #         sorted_queue = sorted(self.task_queue, key=lambda x: x["priority"], reverse=True)
    #         
    #         for i in range(0, len(sorted_queue), batch_size):
    #             batch = sorted_queue[i:i + batch_size]
    #             batch_results = []
    #             
    #             print(f"\n📦 Выполняется пакет {i//batch_size + 1} из {len(batch)} задач")
    #             
    #             for task_item in batch:
    #                 try:
    #                     result = self.execute_task(
    #                         task_item["name"],
    #                         *task_item["args"],
    #                         **task_item["kwargs"]
    #                     )
    #                     batch_results.append({
    #                         "task": task_item["name"],
    #                         "result": result,
    #                         "status": "success"
    #                     })
    #                 except Exception as e:
    #                     batch_results.append({
    #                         "task": task_item["name"],
    #                         "error": str(e),
    #                         "status": "failed"
    #                     })
    #             
    #             yield batch_results
    #         
    #         # Очищаем очередь после выполнения
    #         self.task_queue.clear()
    #     
    #     def get_statistics(self):
    #         """Возвращает статистику выполнения"""
    #         return {
    #             "total_registered": len(self.tasks),
    #             "completed": len(self.completed_tasks),
    #             "failed": len(self.failed_tasks),
    #             "in_queue": len(self.task_queue)
    #         }
    # 
    # # Создаем менеджер задач
    # task_manager = TaskManager()
    # 
    # # Регистрируем задачи с помощью декораторов
    # @task_manager.task("fetch_data", priority=3)
    # @task_manager.retry(max_attempts=2)
    # def fetch_data(url):
    #     """Имитирует загрузку данных"""
    #     if random.random() < 0.3:  # 30% шанс ошибки
    #         raise Exception(f"Ошибка сети при загрузке {url}")
    #     return f"Данные с {url} загружены"
    # 
    # @task_manager.task("process_data", priority=2, dependencies=["fetch_data"])
    # def process_data(data):
    #     """Обрабатывает данные"""
    #     time.sleep(0.1)  # Имитация обработки
    #     return f"Обработано: {data}"
    # 
    # @task_manager.task("save_data", priority=1, dependencies=["process_data"])
    # def save_data(processed_data):
    #     """Сохраняет данные"""
    #     return f"Сохранено: {processed_data}"
    # 
    # @task_manager.task("cleanup", priority=1)
    # def cleanup():
    #     """Очистка временных файлов"""
    #     return "Временные файлы удалены"
    # 
    # @task_manager.task("send_notification", priority=1)
    # def send_notification(message):
    #     """Отправляет уведомление"""
    #     return f"Уведомление отправлено: {message}"
    # 
    # # Добавляем задачи в очередь
    # print("Добавление задач в очередь:")
    # task_manager.add_to_queue("fetch_data", "https://api.example.com/data")
    # task_manager.add_to_queue("cleanup")
    # task_manager.add_to_queue("send_notification", "Система запущена")
    # task_manager.add_to_queue("fetch_data", "https://api.example.com/users")
    # 
    # # Выполняем задачи пакетами
    # print("\nВыполнение задач пакетами:")
    # batch_executor = task_manager.batch_executor(batch_size=2)
    # 
    # for batch_num, batch_results in enumerate(batch_executor, 1):
    #     print(f"\nРезультаты пакета {batch_num}:")
    #     for result in batch_results:
    #         if result["status"] == "success":
    #             print(f"  ✅ {result['task']}: {result['result']}")
    #         else:
    #             print(f"  ❌ {result['task']}: {result['error']}")
    # 
    # # Статистика
    # stats = task_manager.get_statistics()
    # print(f"\n📊 Статистика:")
    # print(f"  Зарегистрировано задач: {stats['total_registered']}")
    # print(f"  Выполнено успешно: {stats['completed']}")
    # print(f"  Провалено: {stats['failed']}")
    # print(f"  В очереди: {stats['in_queue']}")


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Калькулятор с функциями", exercise_01),
        ("Система декораторов для логирования", exercise_02),
        ("Генератор паролей", exercise_03),
        ("Функциональная обработка данных", exercise_04),
        ("Система задач с декораторами и генераторами", exercise_05),
    ]
    
    print("🎯 Упражнения: Функции в Python")
    print("=" * 50)
    
    while True:
        print("\nДоступные упражнения:")
        for i, (name, _) in enumerate(exercises, 1):
            print(f"{i:2}. {name}")
        print(" 0. Выход")
        
        try:
            choice = int(input("\nВыберите упражнение (0-5): "))
            if choice == 0:
                print("До свидания!")
                break
            elif 1 <= choice <= len(exercises):
                print("\n" + "="*60)
                exercises[choice-1][1]()
                print("="*60)
                input("\nНажмите Enter для продолжения...")
            else:
                print("Неверный номер упражнения!")
        except ValueError:
            print("Введите корректный номер!")
        except KeyboardInterrupt:
            print("\n\nДо свидания!")
            break


if __name__ == "__main__":
    main() 