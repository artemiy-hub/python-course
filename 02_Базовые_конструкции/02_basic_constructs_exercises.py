#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Базовые конструкции Python

Этот файл содержит практические упражнения для закрепления знаний:
- Работа с переменными и типами данных
- Использование операторов
- Условные конструкции
- Циклы и итерации
- Ввод и обработка данных
- Область видимости

Каждое упражнение имеет описание задачи и закомментированное решение.
"""

import math
from datetime import datetime


def exercise_01():
    """
    Упражнение 1: Калькулятор типов данных
    
    Создайте программу, которая:
    1. Запрашивает у пользователя число
    2. Определяет, является ли оно целым или дробным
    3. Выводит информацию о числе (тип, размер в байтах, квадрат)
    4. Проверяет, является ли число простым (для целых)
    """
    print("=== Упражнение 1: Калькулятор типов данных ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # try:
    #     user_input = input("Введите число: ")
    #     number = float(user_input)
    #     
    #     # Проверяем, целое ли число
    #     if number.is_integer():
    #         number = int(number)
    #         print(f"Число: {number}")
    #         print(f"Тип: {type(number).__name__}")
    #         print(f"Размер в байтах: {sys.getsizeof(number)}")
    #         print(f"Квадрат: {number ** 2}")
    #         
    #         # Проверка на простое число
    #         if number > 1:
    #             is_prime = True
    #             for i in range(2, int(math.sqrt(number)) + 1):
    #                 if number % i == 0:
    #                     is_prime = False
    #                     break
    #             print(f"Простое число: {'Да' if is_prime else 'Нет'}")
    #     else:
    #         print(f"Число: {number}")
    #         print(f"Тип: {type(number).__name__}")
    #         print(f"Размер в байтах: {sys.getsizeof(number)}")
    #         print(f"Квадрат: {number ** 2}")
    #         print("Дробное число не может быть простым")
    # 
    # except ValueError:
    #     print("Ошибка: введено не число!")


def exercise_02():
    """
    Упражнение 2: Анализатор паролей
    
    Создайте функцию, которая проверяет силу пароля:
    1. Длина не менее 8 символов
    2. Содержит заглавные буквы
    3. Содержит строчные буквы
    4. Содержит цифры
    5. Содержит специальные символы
    Выведите оценку от 1 до 5 и рекомендации.
    """
    print("=== Упражнение 2: Анализатор паролей ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # password = input("Введите пароль для проверки: ")
    # 
    # score = 0
    # recommendations = []
    # 
    # # Проверка длины
    # if len(password) >= 8:
    #     score += 1
    # else:
    #     recommendations.append("Используйте не менее 8 символов")
    # 
    # # Проверка заглавных букв
    # if any(c.isupper() for c in password):
    #     score += 1
    # else:
    #     recommendations.append("Добавьте заглавные буквы")
    # 
    # # Проверка строчных букв
    # if any(c.islower() for c in password):
    #     score += 1
    # else:
    #     recommendations.append("Добавьте строчные буквы")
    # 
    # # Проверка цифр
    # if any(c.isdigit() for c in password):
    #     score += 1
    # else:
    #     recommendations.append("Добавьте цифры")
    # 
    # # Проверка специальных символов
    # special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    # if any(c in special_chars for c in password):
    #     score += 1
    # else:
    #     recommendations.append("Добавьте специальные символы")
    # 
    # # Вывод результата
    # strength_levels = {
    #     1: "Очень слабый",
    #     2: "Слабый", 
    #     3: "Средний",
    #     4: "Сильный",
    #     5: "Очень сильный"
    # }
    # 
    # print(f"Оценка пароля: {score}/5 ({strength_levels[score]})")
    # if recommendations:
    #     print("Рекомендации для улучшения:")
    #     for rec in recommendations:
    #         print(f"- {rec}")


def exercise_03():
    """
    Упражнение 3: Угадай число
    
    Реализуйте игру "Угадай число":
    1. Программа загадывает число от 1 до 100
    2. Пользователь пытается угадать
    3. Программа дает подсказки (больше/меньше)
    4. Подсчитывает количество попыток
    5. Предлагает сыграть еще раз
    """
    print("=== Упражнение 3: Угадай число ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # import random
    # 
    # def play_game():
    #     number = random.randint(1, 100)
    #     attempts = 0
    #     max_attempts = 10
    #     
    #     print(f"Я загадал число от 1 до 100. У вас {max_attempts} попыток!")
    #     
    #     while attempts < max_attempts:
    #         try:
    #             guess = int(input(f"Попытка {attempts + 1}: "))
    #             attempts += 1
    #             
    #             if guess == number:
    #                 print(f"🎉 Поздравляю! Вы угадали число {number} за {attempts} попыток!")
    #                 return True
    #             elif guess < number:
    #                 print("📈 Мое число больше")
    #             else:
    #                 print("📉 Мое число меньше")
    #                 
    #         except ValueError:
    #             print("Пожалуйста, введите целое число!")
    #             continue
    #     
    #     print(f"😞 Попытки закончились! Загаданное число было: {number}")
    #     return False
    # 
    # # Основной игровой цикл
    # while True:
    #     play_game()
    #     
    #     play_again = input("Хотите сыграть еще раз? (да/нет): ").lower()
    #     if play_again not in ['да', 'yes', 'y', 'д']:
    #         print("Спасибо за игру!")
    #         break


def exercise_04():
    """
    Упражнение 4: Калькулятор с историей
    
    Создайте калькулятор, который:
    1. Выполняет базовые операции (+, -, *, /, //, %, **)
    2. Сохраняет историю операций
    3. Позволяет просмотреть историю
    4. Позволяет очистить историю
    5. Имеет команды: 'history', 'clear', 'quit'
    """
    print("=== Упражнение 4: Калькулятор с историей ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # history = []
    # 
    # def calculate(expression):
    #     try:
    #         # Безопасное вычисление выражения
    #         allowed_chars = set('0123456789+-*/().% ')
    #         if all(c in allowed_chars for c in expression):
    #             result = eval(expression)
    #             history.append(f"{expression} = {result}")
    #             return result
    #         else:
    #             raise ValueError("Недопустимые символы в выражении")
    #     except Exception as e:
    #         return f"Ошибка: {e}"
    # 
    # print("Калькулятор запущен! Доступные команды:")
    # print("- Введите математическое выражение (например: 2 + 3 * 4)")
    # print("- 'history' - показать историю")
    # print("- 'clear' - очистить историю")
    # print("- 'quit' - выход")
    # 
    # while True:
    #     user_input = input(">>> ").strip()
    #     
    #     if user_input.lower() == 'quit':
    #         print("До свидания!")
    #         break
    #     elif user_input.lower() == 'history':
    #         if history:
    #             print("История вычислений:")
    #             for i, operation in enumerate(history, 1):
    #                 print(f"{i}. {operation}")
    #         else:
    #             print("История пуста")
    #     elif user_input.lower() == 'clear':
    #         history.clear()
    #         print("История очищена")
    #     elif user_input:
    #         result = calculate(user_input)
    #         print(f"Результат: {result}")


def exercise_05():
    """
    Упражнение 5: Анализатор текста
    
    Создайте программу анализа текста:
    1. Подсчет символов, слов, предложений
    2. Найти самое длинное и короткое слово
    3. Подсчет частоты букв
    4. Определение языка (по наличию кириллицы/латиницы)
    5. Статистика по длине слов
    """
    print("=== Упражнение 5: Анализатор текста ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # text = input("Введите текст для анализа: ")
    # 
    # if not text.strip():
    #     print("Текст не может быть пустым!")
    #     return
    # 
    # # Базовая статистика
    # char_count = len(text)
    # char_count_no_spaces = len(text.replace(' ', ''))
    # word_count = len(text.split())
    # sentence_count = text.count('.') + text.count('!') + text.count('?')
    # 
    # print(f"\n📊 Статистика текста:")
    # print(f"Символов всего: {char_count}")
    # print(f"Символов без пробелов: {char_count_no_spaces}")
    # print(f"Слов: {word_count}")
    # print(f"Предложений: {sentence_count}")
    # 
    # # Анализ слов
    # if word_count > 0:
    #     words = text.split()
    #     word_lengths = [len(word.strip('.,!?;:')) for word in words]
    #     
    #     longest_word = max(words, key=lambda w: len(w.strip('.,!?;:')))
    #     shortest_word = min(words, key=lambda w: len(w.strip('.,!?;:')))
    #     
    #     print(f"\n📝 Анализ слов:")
    #     print(f"Самое длинное слово: '{longest_word}' ({len(longest_word.strip('.,!?;:'))} символов)")
    #     print(f"Самое короткое слово: '{shortest_word}' ({len(shortest_word.strip('.,!?;:'))} символов)")
    #     print(f"Средняя длина слова: {sum(word_lengths) / len(word_lengths):.1f} символов")
    # 
    # # Частота букв
    # letter_freq = {}
    # for char in text.lower():
    #     if char.isalpha():
    #         letter_freq[char] = letter_freq.get(char, 0) + 1
    # 
    # if letter_freq:
    #     print(f"\n🔤 Топ-5 самых частых букв:")
    #     sorted_letters = sorted(letter_freq.items(), key=lambda x: x[1], reverse=True)
    #     for letter, count in sorted_letters[:5]:
    #         percentage = (count / sum(letter_freq.values())) * 100
    #         print(f"'{letter}': {count} раз ({percentage:.1f}%)")
    # 
    # # Определение языка
    # cyrillic_count = sum(1 for char in text if '\u0400' <= char <= '\u04FF')
    # latin_count = sum(1 for char in text if 'a' <= char.lower() <= 'z')
    # 
    # print(f"\n🌍 Анализ языка:")
    # if cyrillic_count > latin_count:
    #     print("Преобладает кириллица (русский/украинский/белорусский)")
    # elif latin_count > cyrillic_count:
    #     print("Преобладает латиница (английский/европейские языки)")
    # else:
    #     print("Смешанный текст или неопределенный язык")


def exercise_06():
    """
    Упражнение 6: Генератор паттернов
    
    Создайте программу, которая рисует различные паттерны:
    1. Треугольник из звездочек
    2. Ромб
    3. Таблица умножения
    4. Паттерн "елочка"
    5. Числовая пирамида
    """
    print("=== Упражнение 6: Генератор паттернов ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # def draw_triangle(height):
    #     print("🔺 Треугольник:")
    #     for i in range(1, height + 1):
    #         spaces = ' ' * (height - i)
    #         stars = '*' * (2 * i - 1)
    #         print(spaces + stars)
    # 
    # def draw_diamond(size):
    #     print("💎 Ромб:")
    #     # Верхняя часть
    #     for i in range(1, size + 1):
    #         spaces = ' ' * (size - i)
    #         stars = '*' * (2 * i - 1)
    #         print(spaces + stars)
    #     # Нижняя часть
    #     for i in range(size - 1, 0, -1):
    #         spaces = ' ' * (size - i)
    #         stars = '*' * (2 * i - 1)
    #         print(spaces + stars)
    # 
    # def draw_multiplication_table(n):
    #     print(f"📊 Таблица умножения {n}x{n}:")
    #     print("    ", end="")
    #     for i in range(1, n + 1):
    #         print(f"{i:4}", end="")
    #     print()
    #     print("   " + "-" * (4 * n + 1))
    #     
    #     for i in range(1, n + 1):
    #         print(f"{i:2} |", end="")
    #         for j in range(1, n + 1):
    #             print(f"{i*j:4}", end="")
    #         print()
    # 
    # def draw_christmas_tree(height):
    #     print("🎄 Елочка:")
    #     for i in range(1, height + 1):
    #         spaces = ' ' * (height - i)
    #         stars = '*' * (2 * i - 1)
    #         print(spaces + stars)
    #     # Ствол
    #     trunk_spaces = ' ' * (height - 1)
    #     print(trunk_spaces + '*')
    # 
    # def draw_number_pyramid(height):
    #     print("🔢 Числовая пирамида:")
    #     for i in range(1, height + 1):
    #         spaces = ' ' * (height - i)
    #         numbers = ' '.join(str(j) for j in range(1, i + 1))
    #         print(spaces + numbers)
    # 
    # # Демонстрация всех паттернов
    # size = 5
    # 
    # draw_triangle(size)
    # print()
    # draw_diamond(size)
    # print()
    # draw_multiplication_table(size)
    # print()
    # draw_christmas_tree(size)
    # print()
    # draw_number_pyramid(size)


def exercise_07():
    """
    Упражнение 7: Система оценок
    
    Создайте систему подсчета итоговых оценок:
    1. Запросите оценки по разным предметам
    2. Вычислите средний балл
    3. Определите буквенную оценку (A, B, C, D, F)
    4. Покажите статистику (лучший/худший предмет)
    5. Дайте рекомендации для улучшения
    """
    print("=== Упражнение 7: Система оценок ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # subjects = {}
    # 
    # print("Введите оценки по предметам (введите 'готово' для завершения):")
    # 
    # while True:
    #     subject = input("Название предмета: ").strip()
    #     if subject.lower() == 'готово':
    #         break
    #     
    #     try:
    #         grade = float(input(f"Оценка по предмету {subject} (0-100): "))
    #         if 0 <= grade <= 100:
    #             subjects[subject] = grade
    #         else:
    #             print("Оценка должна быть от 0 до 100!")
    #     except ValueError:
    #         print("Пожалуйста, введите числовую оценку!")
    # 
    # if not subjects:
    #     print("Не введено ни одной оценки!")
    #     return
    # 
    # # Вычисления
    # grades = list(subjects.values())
    # average = sum(grades) / len(grades)
    # 
    # # Буквенная оценка
    # def get_letter_grade(score):
    #     if score >= 90: return 'A'
    #     elif score >= 80: return 'B'
    #     elif score >= 70: return 'C'
    #     elif score >= 60: return 'D'
    #     else: return 'F'
    # 
    # letter_grade = get_letter_grade(average)
    # 
    # # Статистика
    # best_subject = max(subjects, key=subjects.get)
    # worst_subject = min(subjects, key=subjects.get)
    # 
    # print(f"\n📊 Результаты:")
    # print(f"Средний балл: {average:.2f}")
    # print(f"Буквенная оценка: {letter_grade}")
    # print(f"Лучший предмет: {best_subject} ({subjects[best_subject]:.1f})")
    # print(f"Худший предмет: {worst_subject} ({subjects[worst_subject]:.1f})")
    # 
    # # Рекомендации
    # print(f"\n💡 Рекомендации:")
    # if average >= 90:
    #     print("Отличная работа! Продолжайте в том же духе!")
    # elif average >= 80:
    #     print("Хорошие результаты! Немного усилий и будет отлично!")
    # elif average >= 70:
    #     print("Удовлетворительно. Стоит больше времени уделить изучению.")
    # else:
    #     print("Требуется серьезная работа над улучшением оценок.")
    # 
    # if subjects[worst_subject] < 70:
    #     print(f"Особое внимание стоит уделить предмету: {worst_subject}")


def exercise_08():
    """
    Упражнение 8: Конвертер систем счисления
    
    Создайте конвертер между различными системами счисления:
    1. Десятичная → двоичная, восьмеричная, шестнадцатеричная
    2. Двоичная → десятичная
    3. Проверка корректности ввода
    4. Показ промежуточных шагов
    5. Интерактивное меню
    """
    print("=== Упражнение 8: Конвертер систем счисления ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # def decimal_to_binary(n):
    #     if n == 0:
    #         return "0"
    #     
    #     binary = ""
    #     steps = []
    #     original_n = n
    #     
    #     while n > 0:
    #         remainder = n % 2
    #         binary = str(remainder) + binary
    #         steps.append(f"{n} ÷ 2 = {n // 2} (остаток {remainder})")
    #         n //= 2
    #     
    #     print(f"Преобразование {original_n} в двоичную систему:")
    #     for step in steps:
    #         print(f"  {step}")
    #     
    #     return binary
    # 
    # def binary_to_decimal(binary_str):
    #     try:
    #         decimal = 0
    #         power = 0
    #         steps = []
    #         
    #         for digit in reversed(binary_str):
    #             if digit not in '01':
    #                 raise ValueError("Некорректная двоичная запись")
    #             
    #             value = int(digit) * (2 ** power)
    #             if value > 0:
    #                 steps.append(f"{digit} × 2^{power} = {value}")
    #             decimal += value
    #             power += 1
    #         
    #         print(f"Преобразование {binary_str} в десятичную систему:")
    #         for step in steps:
    #             print(f"  {step}")
    #         if steps:
    #             print(f"  Сумма: {' + '.join(str(int(digit) * (2 ** (len(binary_str) - 1 - i))) for i, digit in enumerate(binary_str) if digit == '1')} = {decimal}")
    #         
    #         return decimal
    #     except ValueError as e:
    #         return str(e)
    # 
    # def show_menu():
    #     print("\n🔢 Конвертер систем счисления")
    #     print("1. Десятичная → Двоичная")
    #     print("2. Десятичная → Восьмеричная")
    #     print("3. Десятичная → Шестнадцатеричная")
    #     print("4. Двоичная → Десятичная")
    #     print("5. Показать все варианты для числа")
    #     print("0. Выход")
    # 
    # while True:
    #     show_menu()
    #     choice = input("Выберите опцию: ").strip()
    #     
    #     if choice == '0':
    #         print("До свидания!")
    #         break
    #     elif choice == '1':
    #         try:
    #             num = int(input("Введите десятичное число: "))
    #             result = decimal_to_binary(num)
    #             print(f"Результат: {num}₁₀ = {result}₂")
    #         except ValueError:
    #             print("Ошибка: введите целое число!")
    #     elif choice == '2':
    #         try:
    #             num = int(input("Введите десятичное число: "))
    #             result = oct(num)[2:]  # Убираем префикс '0o'
    #             print(f"Результат: {num}₁₀ = {result}₈")
    #         except ValueError:
    #             print("Ошибка: введите целое число!")
    #     elif choice == '3':
    #         try:
    #             num = int(input("Введите десятичное число: "))
    #             result = hex(num)[2:].upper()  # Убираем префикс '0x'
    #             print(f"Результат: {num}₁₀ = {result}₁₆")
    #         except ValueError:
    #             print("Ошибка: введите целое число!")
    #     elif choice == '4':
    #         binary = input("Введите двоичное число: ").strip()
    #         result = binary_to_decimal(binary)
    #         if isinstance(result, int):
    #             print(f"Результат: {binary}₂ = {result}₁₀")
    #         else:
    #             print(f"Ошибка: {result}")
    #     elif choice == '5':
    #         try:
    #             num = int(input("Введите десятичное число: "))
    #             print(f"\nВсе представления числа {num}:")
    #             print(f"Десятичная:      {num}")
    #             print(f"Двоичная:        {bin(num)[2:]}")
    #             print(f"Восьмеричная:    {oct(num)[2:]}")
    #             print(f"Шестнадцатеричная: {hex(num)[2:].upper()}")
    #         except ValueError:
    #             print("Ошибка: введите целое число!")
    #     else:
    #         print("Неверный выбор!")


def exercise_09():
    """
    Упражнение 9: Генератор математических последовательностей
    
    Создайте программу для генерации различных математических последовательностей:
    1. Арифметическая прогрессия
    2. Геометрическая прогрессия  
    3. Числа Фибоначчи
    4. Факториалы
    5. Простые числа
    """
    print("=== Упражнение 9: Генератор математических последовательностей ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # def arithmetic_sequence(first, diff, count):
    #     """Арифметическая прогрессия"""
    #     sequence = []
    #     for i in range(count):
    #         sequence.append(first + i * diff)
    #     return sequence
    # 
    # def geometric_sequence(first, ratio, count):
    #     """Геометрическая прогрессия"""
    #     sequence = []
    #     for i in range(count):
    #         sequence.append(first * (ratio ** i))
    #     return sequence
    # 
    # def fibonacci_sequence(count):
    #     """Числа Фибоначчи"""
    #     if count <= 0:
    #         return []
    #     elif count == 1:
    #         return [0]
    #     elif count == 2:
    #         return [0, 1]
    #     
    #     sequence = [0, 1]
    #     for i in range(2, count):
    #         sequence.append(sequence[i-1] + sequence[i-2])
    #     return sequence
    # 
    # def factorial_sequence(count):
    #     """Факториалы"""
    #     sequence = []
    #     for i in range(count):
    #         if i == 0:
    #             factorial = 1
    #         else:
    #             factorial = sequence[i-1] * i
    #         sequence.append(factorial)
    #     return sequence
    # 
    # def prime_sequence(count):
    #     """Простые числа"""
    #     def is_prime(n):
    #         if n < 2:
    #             return False
    #         for i in range(2, int(n ** 0.5) + 1):
    #             if n % i == 0:
    #                 return False
    #         return True
    #     
    #     primes = []
    #     num = 2
    #     while len(primes) < count:
    #         if is_prime(num):
    #             primes.append(num)
    #         num += 1
    #     return primes
    # 
    # def show_sequence_menu():
    #     print("\n🔢 Генератор математических последовательностей")
    #     print("1. Арифметическая прогрессия")
    #     print("2. Геометрическая прогрессия")
    #     print("3. Числа Фибоначчи")
    #     print("4. Факториалы")
    #     print("5. Простые числа")
    #     print("0. Выход")
    # 
    # while True:
    #     show_sequence_menu()
    #     choice = input("Выберите тип последовательности: ").strip()
    #     
    #     if choice == '0':
    #         print("До свидания!")
    #         break
    #     
    #     try:
    #         count = int(input("Сколько элементов показать: "))
    #         if count <= 0:
    #             print("Количество должно быть положительным!")
    #             continue
    #             
    #         if choice == '1':
    #             first = float(input("Первый элемент: "))
    #             diff = float(input("Разность: "))
    #             result = arithmetic_sequence(first, diff, count)
    #             print(f"Арифметическая прогрессия: {result}")
    #             print(f"Формула: a_n = {first} + (n-1) × {diff}")
    #             
    #         elif choice == '2':
    #             first = float(input("Первый элемент: "))
    #             ratio = float(input("Знаменатель: "))
    #             result = geometric_sequence(first, ratio, count)
    #             print(f"Геометрическая прогрессия: {result}")
    #             print(f"Формула: a_n = {first} × {ratio}^(n-1)")
    #             
    #         elif choice == '3':
    #             result = fibonacci_sequence(count)
    #             print(f"Числа Фибоначчи: {result}")
    #             print("Формула: F_n = F_(n-1) + F_(n-2), F_0=0, F_1=1")
    #             
    #         elif choice == '4':
    #             result = factorial_sequence(count)
    #             print(f"Факториалы: {result}")
    #             print("Формула: n! = n × (n-1) × ... × 2 × 1")
    #             
    #         elif choice == '5':
    #             result = prime_sequence(count)
    #             print(f"Простые числа: {result}")
    #             print("Простое число делится только на 1 и само себя")
    #             
    #         else:
    #             print("Неверный выбор!")
    #             
    #     except ValueError:
    #         print("Ошибка ввода! Введите корректные числа.")


def exercise_10():
    """
    Упражнение 10: Интерактивный календарь
    
    Создайте программу календаря:
    1. Показать календарь на текущий месяц
    2. Показать календарь на любой месяц/год
    3. Вычислить разность между датами
    4. Найти день недели для любой даты
    5. Показать праздники и важные даты
    """
    print("=== Упражнение 10: Интерактивный календарь ===")
    
    # TODO: Напишите ваш код здесь
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # import calendar
    # from datetime import datetime, date
    # 
    # def show_calendar(year, month):
    #     """Показать календарь на месяц"""
    #     print(f"\n📅 Календарь на {calendar.month_name[month]} {year}")
    #     print(calendar.month(year, month))
    # 
    # def get_day_of_week(year, month, day):
    #     """Определить день недели"""
    #     try:
    #         date_obj = date(year, month, day)
    #         days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 
    #                'Пятница', 'Суббота', 'Воскресенье']
    #         return days[date_obj.weekday()]
    #     except ValueError:
    #         return "Некорректная дата"
    # 
    # def calculate_date_difference(date1, date2):
    #     """Вычислить разность между датами"""
    #     try:
    #         diff = abs(date2 - date1).days
    #         return diff
    #     except:
    #         return None
    # 
    # def get_holidays(year):
    #     """Получить список праздников"""
    #     holidays = {
    #         (1, 1): "Новый год",
    #         (1, 7): "Рождество Христово",
    #         (2, 23): "День защитника Отечества",
    #         (3, 8): "Международный женский день",
    #         (5, 1): "Праздник Весны и Труда",
    #         (5, 9): "День Победы",
    #         (6, 12): "День России",
    #         (11, 4): "День народного единства"
    #     }
    #     
    #     print(f"\n🎉 Праздники {year} года:")
    #     for (month, day), name in holidays.items():
    #         day_of_week = get_day_of_week(year, month, day)
    #         print(f"{day:2}.{month:02} ({day_of_week}) - {name}")
    # 
    # def show_calendar_menu():
    #     print("\n📅 Интерактивный календарь")
    #     print("1. Текущий месяц")
    #     print("2. Календарь на месяц")
    #     print("3. День недели для даты")
    #     print("4. Разность между датами")
    #     print("5. Праздники года")
    #     print("6. Годовой календарь")
    #     print("0. Выход")
    # 
    # while True:
    #     show_calendar_menu()
    #     choice = input("Выберите опцию: ").strip()
    #     
    #     if choice == '0':
    #         print("До свидания!")
    #         break
    #         
    #     elif choice == '1':
    #         now = datetime.now()
    #         show_calendar(now.year, now.month)
    #         
    #     elif choice == '2':
    #         try:
    #             year = int(input("Введите год: "))
    #             month = int(input("Введите месяц (1-12): "))
    #             if 1 <= month <= 12:
    #                 show_calendar(year, month)
    #             else:
    #                 print("Месяц должен быть от 1 до 12!")
    #         except ValueError:
    #             print("Ошибка: введите корректные числа!")
    #             
    #     elif choice == '3':
    #         try:
    #             year = int(input("Введите год: "))
    #             month = int(input("Введите месяц: "))
    #             day = int(input("Введите день: "))
    #             day_name = get_day_of_week(year, month, day)
    #             print(f"{day:02}.{month:02}.{year} - {day_name}")
    #         except ValueError:
    #             print("Ошибка: введите корректные числа!")
    #             
    #     elif choice == '4':
    #         try:
    #             print("Первая дата:")
    #             year1 = int(input("Год: "))
    #             month1 = int(input("Месяц: "))
    #             day1 = int(input("День: "))
    #             date1 = date(year1, month1, day1)
    #             
    #             print("Вторая дата:")
    #             year2 = int(input("Год: "))
    #             month2 = int(input("Месяц: "))
    #             day2 = int(input("День: "))
    #             date2 = date(year2, month2, day2)
    #             
    #             diff = calculate_date_difference(date1, date2)
    #             print(f"Разность: {diff} дней")
    #             print(f"Это примерно {diff // 365} лет, {(diff % 365) // 30} месяцев, {(diff % 365) % 30} дней")
    #             
    #         except ValueError:
    #             print("Ошибка: некорректная дата!")
    #             
    #     elif choice == '5':
    #         try:
    #             year = int(input("Введите год: "))
    #             get_holidays(year)
    #         except ValueError:
    #             print("Ошибка: введите корректный год!")
    #             
    #     elif choice == '6':
    #         try:
    #             year = int(input("Введите год: "))
    #             print(f"\n📅 Календарь на {year} год")
    #             print(calendar.calendar(year))
    #         except ValueError:
    #             print("Ошибка: введите корректный год!")
    #             
    #     else:
    #         print("Неверный выбор!")


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Калькулятор типов данных", exercise_01),
        ("Анализатор паролей", exercise_02),
        ("Угадай число", exercise_03),
        ("Калькулятор с историей", exercise_04),
        ("Анализатор текста", exercise_05),
        ("Генератор паттернов", exercise_06),
        ("Система оценок", exercise_07),
        ("Конвертер систем счисления", exercise_08),
        ("Генератор последовательностей", exercise_09),
        ("Интерактивный календарь", exercise_10),
    ]
    
    print("🎯 Упражнения: Базовые конструкции Python")
    print("=" * 50)
    
    while True:
        print("\nДоступные упражнения:")
        for i, (name, _) in enumerate(exercises, 1):
            print(f"{i:2}. {name}")
        print(" 0. Выход")
        
        try:
            choice = int(input("\nВыберите упражнение (0-10): "))
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