#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Введение в Python

Этот файл содержит базовые примеры для изучения основ Python:
- Первые программы
- Основные типы данных
- Простые операции
- Интерактивная работа с пользователем
"""

import sys
import platform
from datetime import datetime

def example_01_hello_world():
    """
    Пример 1: Классическая программа "Hello, World!"
    
    Это первая программа, которую пишут на любом языке программирования.
    """
    print("=== Пример 1: Hello, World! ===")
    
    # Простейший вывод
    print("Hello, World!")
    
    # Вывод с переменной
    message = "Привет, мир Python!"
    print(message)
    
    # Форматированный вывод
    language = "Python"
    version = "3.9"
    print(f"Изучаем {language} версии {version}")
    
    print()

def example_02_basic_data_types():
    """
    Пример 2: Основные типы данных Python
    
    Python имеет несколько встроенных типов данных:
    - int (целые числа)
    - float (числа с плавающей точкой)
    - str (строки)
    - bool (логические значения)
    """
    print("=== Пример 2: Основные типы данных ===")
    
    # Целые числа (int)
    age = 25
    year = 2023
    big_number = 1_000_000  # Можно использовать подчёркивания для читаемости
    
    print(f"Возраст: {age} (тип: {type(age).__name__})")
    print(f"Год: {year} (тип: {type(year).__name__})")
    print(f"Большое число: {big_number:,}")  # Форматирование с разделителями
    
    # Числа с плавающей точкой (float)
    height = 175.5
    pi = 3.14159
    scientific = 1.23e-4  # Научная нотация
    
    print(f"Рост: {height} см (тип: {type(height).__name__})")
    print(f"Число π: {pi:.2f}")  # Округление до 2 знаков после запятой
    print(f"Научная нотация: {scientific}")
    
    # Строки (str)
    name = "Анна"
    surname = 'Иванова'  # Можно использовать одинарные кавычки
    full_name = name + " " + surname  # Конкатенация строк
    
    print(f"Имя: {name} (тип: {type(name).__name__})")
    print(f"Полное имя: {full_name}")
    print(f"Длина полного имени: {len(full_name)} символов")
    
    # Логические значения (bool)
    is_student = True
    is_working = False
    
    print(f"Студент: {is_student} (тип: {type(is_student).__name__})")
    print(f"Работает: {is_working}")
    
    # Автоматическое определение типа
    auto_int = 42
    auto_float = 3.14
    auto_str = "Python"
    auto_bool = True
    
    print(f"\nАвтоматическое определение типов:")
    print(f"{auto_int} → {type(auto_int).__name__}")
    print(f"{auto_float} → {type(auto_float).__name__}")
    print(f"'{auto_str}' → {type(auto_str).__name__}")
    print(f"{auto_bool} → {type(auto_bool).__name__}")
    
    print()

def example_03_basic_operations():
    """
    Пример 3: Основные операции с данными
    
    Демонстрирует арифметические, логические операции
    и работу со строками.
    """
    print("=== Пример 3: Основные операции ===")
    
    # Арифметические операции
    a = 15
    b = 4
    
    print(f"Числа: a = {a}, b = {b}")
    print(f"Сложение: {a} + {b} = {a + b}")
    print(f"Вычитание: {a} - {b} = {a - b}")
    print(f"Умножение: {a} * {b} = {a * b}")
    print(f"Деление: {a} / {b} = {a / b}")
    print(f"Целочисленное деление: {a} // {b} = {a // b}")
    print(f"Остаток от деления: {a} % {b} = {a % b}")
    print(f"Возведение в степень: {a} ** {b} = {a ** b}")
    
    # Операции сравнения
    x = 10
    y = 20
    
    print(f"\nСравнения: x = {x}, y = {y}")
    print(f"x < y: {x < y}")
    print(f"x > y: {x > y}")
    print(f"x == y: {x == y}")
    print(f"x != y: {x != y}")
    print(f"x <= 10: {x <= 10}")
    print(f"y >= 20: {y >= 20}")
    
    # Логические операции
    is_sunny = True
    is_warm = False
    
    print(f"\nЛогические операции: sunny = {is_sunny}, warm = {is_warm}")
    print(f"sunny and warm: {is_sunny and is_warm}")
    print(f"sunny or warm: {is_sunny or is_warm}")
    print(f"not sunny: {not is_sunny}")
    
    # Операции со строками
    first_name = "Иван"
    last_name = "Петров"
    
    print(f"\nОперации со строками:")
    print(f"Конкатенация: '{first_name}' + ' ' + '{last_name}' = '{first_name + ' ' + last_name}'")
    print(f"Повторение: '{first_name}' * 3 = '{first_name * 3}'")
    print(f"Длина строки: len('{first_name}') = {len(first_name)}")
    print(f"Верхний регистр: '{first_name}'.upper() = '{first_name.upper()}'")
    print(f"Нижний регистр: '{first_name}'.lower() = '{first_name.lower()}'")
    
    print()

def example_04_user_interaction():
    """
    Пример 4: Взаимодействие с пользователем
    
    Показывает, как получать ввод от пользователя
    и обрабатывать его.
    """
    print("=== Пример 4: Взаимодействие с пользователем ===")
    
    # Простой ввод строки
    print("Демонстрация ввода данных:")
    print("(В реальном использовании раскомментируйте строки с input())")
    
    # name = input("Введите ваше имя: ")
    # print(f"Привет, {name}!")
    
    # Для демонстрации используем заранее заданные значения
    name = "Пользователь"
    print(f"Имитация ввода имени: {name}")
    print(f"Привет, {name}!")
    
    # Ввод чисел (требует преобразования типов)
    # age_str = input("Введите ваш возраст: ")
    # age = int(age_str)  # Преобразование строки в число
    
    age = 25  # Для демонстрации
    print(f"Имитация ввода возраста: {age}")
    
    if age >= 18:
        print("Вы совершеннолетний")
    else:
        print("Вы несовершеннолетний")
    
    # Ввод числа с плавающей точкой
    # height_str = input("Введите ваш рост в см: ")
    # height = float(height_str)
    
    height = 175.5  # Для демонстрации
    print(f"Имитация ввода роста: {height} см")
    
    if height > 180:
        print("Вы высокого роста")
    elif height > 160:
        print("У вас средний рост")
    else:
        print("Вы невысокого роста")
    
    print()

def example_05_string_formatting():
    """
    Пример 5: Форматирование строк
    
    Различные способы форматирования строк в Python.
    """
    print("=== Пример 5: Форматирование строк ===")
    
    name = "Мария"
    age = 28
    salary = 75000.5
    
    # Старый способ (% форматирование)
    old_format = "Меня зовут %s, мне %d лет, зарплата %.2f руб." % (name, age, salary)
    print(f"Старый способ: {old_format}")
    
    # Метод .format()
    format_method = "Меня зовут {}, мне {} лет, зарплата {:.2f} руб.".format(name, age, salary)
    print(f"Метод .format(): {format_method}")
    
    # Метод .format() с именованными параметрами
    named_format = "Меня зовут {name}, мне {age} лет, зарплата {salary:.2f} руб.".format(
        name=name, age=age, salary=salary
    )
    print(f"Именованные параметры: {named_format}")
    
    # f-строки (рекомендуемый способ в Python 3.6+)
    f_string = f"Меня зовут {name}, мне {age} лет, зарплата {salary:.2f} руб."
    print(f"f-строки: {f_string}")
    
    # Дополнительные возможности f-строк
    print(f"\nДополнительные возможности f-строк:")
    print(f"Выражения в f-строках: 2 + 2 = {2 + 2}")
    print(f"Методы в f-строках: {name.upper()}")
    print(f"Форматирование чисел: {salary:,.2f}")  # С разделителями тысяч
    print(f"Дата и время: {datetime.now():%Y-%m-%d %H:%M:%S}")
    
    # Многострочные строки
    multiline = f"""
    Информация о пользователе:
    - Имя: {name}
    - Возраст: {age}
    - Зарплата: {salary:,.2f} руб.
    """
    print(f"Многострочная строка:{multiline}")
    
    print()

def example_06_system_info():
    """
    Пример 6: Информация о системе
    
    Получение информации о Python и операционной системе.
    """
    print("=== Пример 6: Информация о системе ===")
    
    # Информация о Python
    print("Информация о Python:")
    print(f"Версия Python: {sys.version}")
    print(f"Версия Python (кратко): {platform.python_version()}")
    print(f"Реализация Python: {platform.python_implementation()}")
    print(f"Путь к интерпретатору: {sys.executable}")
    
    # Информация об операционной системе
    print(f"\nИнформация об ОС:")
    print(f"Операционная система: {platform.system()}")
    print(f"Версия ОС: {platform.release()}")
    print(f"Архитектура: {platform.machine()}")
    print(f"Процессор: {platform.processor()}")
    print(f"Имя узла: {platform.node()}")
    
    # Информация о кодировке
    print(f"\nИнформация о кодировке:")
    print(f"Кодировка по умолчанию: {sys.getdefaultencoding()}")
    print(f"Кодировка файловой системы: {sys.getfilesystemencoding()}")
    
    # Переменные окружения (примеры)
    import os
    print(f"\nПеременные окружения:")
    print(f"Домашняя папка: {os.path.expanduser('~')}")
    print(f"Текущая папка: {os.getcwd()}")
    
    print()

def example_07_zen_of_python():
    """
    Пример 7: Дзен Python
    
    Демонстрация философии Python через примеры кода.
    """
    print("=== Пример 7: Дзен Python ===")
    
    print("Философия Python (The Zen of Python):")
    print("Для просмотра выполните: import this")
    
    # Примеры применения принципов Дзен Python
    
    # 1. "Красивое лучше уродливого"
    print("\n1. Красивое лучше уродливого:")
    
    # Красиво
    def calculate_circle_area(radius):
        """Вычисляет площадь круга по радиусу."""
        pi = 3.14159
        return pi * radius ** 2
    
    # Менее красиво
    def calc_area(r):
        return 3.14159*r*r
    
    print("Красиво: def calculate_circle_area(radius):")
    print("Уродливо: def calc_area(r):")
    
    # 2. "Явное лучше неявного"
    print("\n2. Явное лучше неявного:")
    
    # Явно
    import math
    explicit_result = math.sqrt(16)
    
    # Неявно (менее понятно)
    implicit_result = 16 ** 0.5
    
    print(f"Явно: math.sqrt(16) = {explicit_result}")
    print(f"Неявно: 16 ** 0.5 = {implicit_result}")
    
    # 3. "Простое лучше сложного"
    print("\n3. Простое лучше сложного:")
    
    numbers = [1, 2, 3, 4, 5]
    
    # Простое
    even_numbers = [n for n in numbers if n % 2 == 0]
    
    # Сложное
    even_numbers_complex = []
    for i in range(len(numbers)):
        if numbers[i] % 2 == 0:
            even_numbers_complex.append(numbers[i])
    
    print(f"Простое: [n for n in numbers if n % 2 == 0] = {even_numbers}")
    print(f"Сложное: цикл с индексами = {even_numbers_complex}")
    
    # 4. "Читаемость имеет значение"
    print("\n4. Читаемость имеет значение:")
    
    # Читаемо
    user_age = 25
    minimum_voting_age = 18
    can_vote = user_age >= minimum_voting_age
    
    # Менее читаемо
    x = 25
    y = 18
    z = x >= y
    
    print("Читаемо: can_vote = user_age >= minimum_voting_age")
    print("Менее читаемо: z = x >= y")
    
    print()

def example_08_common_mistakes():
    """
    Пример 8: Типичные ошибки начинающих
    
    Показывает распространённые ошибки и как их избежать.
    """
    print("=== Пример 8: Типичные ошибки начинающих ===")
    
    # Ошибка 1: Смешивание типов данных
    print("1. Ошибка типов данных:")
    try:
        # Это вызовет ошибку
        # result = "5" + 3
        pass
    except TypeError as e:
        print(f"Ошибка: {e}")
    
    # Правильно:
    correct_result = int("5") + 3
    print(f"Правильно: int('5') + 3 = {correct_result}")
    
    # Ошибка 2: Неправильное именование переменных
    print("\n2. Именование переменных:")
    print("❌ Плохо: x, data, temp, a1, b2")
    print("✅ Хорошо: user_name, total_price, student_age")
    
    # Ошибка 3: Неправильная работа с отступами
    print("\n3. Отступы в Python:")
    print("Python использует отступы для определения блоков кода")
    
    age = 20
    if age >= 18:
        print("Пользователь совершеннолетний")  # 4 пробела отступа
        if age >= 21:
            print("Может употреблять алкоголь в США")  # 8 пробелов отступа
    
    # Ошибка 4: Сравнение с True/False
    print("\n4. Сравнение с булевыми значениями:")
    
    is_active = True
    
    # Плохо
    if is_active == True:
        print("Плохо: if is_active == True")
    
    # Хорошо
    if is_active:
        print("Хорошо: if is_active")
    
    # Ошибка 5: Изменение переменной в цикле
    print("\n5. Изменение списка во время итерации:")
    numbers = [1, 2, 3, 4, 5]
    
    # Неправильно (может пропустить элементы)
    # for num in numbers:
    #     if num % 2 == 0:
    #         numbers.remove(num)
    
    # Правильно
    numbers_copy = numbers.copy()
    for num in numbers_copy:
        if num % 2 == 0:
            numbers.remove(num)
    
    print(f"Удаление чётных чисел: {numbers}")
    
    print()

def main():
    """
    Главная функция для запуска всех примеров.
    """
    print("🐍 ПРАКТИЧЕСКИЕ ПРИМЕРЫ: ВВЕДЕНИЕ В PYTHON 🐍")
    print("=" * 60)
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Версия Python: {platform.python_version()}")
    print("=" * 60)
    print()
    
    # Запуск всех примеров
    example_01_hello_world()
    example_02_basic_data_types()
    example_03_basic_operations()
    example_04_user_interaction()
    example_05_string_formatting()
    example_06_system_info()
    example_07_zen_of_python()
    example_08_common_mistakes()
    
    print("=" * 60)
    print("✅ Все примеры выполнены успешно!")
    print("📚 Переходите к изучению следующего раздела: Базовые конструкции")
    print("=" * 60)

if __name__ == "__main__":
    main() 