#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Практические примеры: Структуры данных Python

Этот файл содержит подробные примеры для изучения:
- Списков и их методов
- Кортежей и именованных кортежей
- Словарей и их возможностей
- Множеств и операций с ними
- Сравнения производительности
- Вложенных структур данных
"""

import sys
import time
import timeit
from collections import namedtuple, defaultdict, Counter, deque, OrderedDict, ChainMap
import copy


def example_01_lists_basics():
    """
    Пример 1: Основы работы со списками
    
    Демонстрирует создание списков, основные операции,
    методы и особенности работы с ними.
    """
    print("=== Пример 1: Основы работы со списками ===")
    
    # Создание списков различными способами
    print("1. Создание списков:")
    empty_list = []
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True, [1, 2]]
    range_list = list(range(5))
    string_list = list("hello")
    
    print(f"Пустой список: {empty_list}")
    print(f"Числа: {numbers}")
    print(f"Смешанный: {mixed}")
    print(f"Из range: {range_list}")
    print(f"Из строки: {string_list}")
    
    # Основные операции
    print("\n2. Основные операции:")
    fruits = ["яблоко", "банан", "апельсин"]
    
    # Добавление элементов
    fruits.append("груша")  # В конец
    print(f"После append: {fruits}")
    
    fruits.insert(1, "киви")  # По индексу
    print(f"После insert: {fruits}")
    
    fruits.extend(["манго", "ананас"])  # Несколько элементов
    print(f"После extend: {fruits}")
    
    # Удаление элементов
    removed = fruits.pop()  # Последний элемент
    print(f"Удален последний: {removed}, остались: {fruits}")
    
    fruits.remove("киви")  # Первое вхождение
    print(f"После remove: {fruits}")
    
    # Поиск и подсчет
    print(f"\nИндекс 'банан': {fruits.index('банан')}")
    print(f"Количество 'яблоко': {fruits.count('яблоко')}")
    
    # Сортировка
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"\nДо сортировки: {numbers}")
    numbers.sort()
    print(f"После sort(): {numbers}")
    
    numbers.sort(reverse=True)
    print(f"После sort(reverse=True): {numbers}")
    
    # Обращение порядка
    letters = list("python")
    print(f"\nДо reverse: {letters}")
    letters.reverse()
    print(f"После reverse(): {letters}")


def example_02_list_slicing():
    """
    Пример 2: Срезы списков
    
    Подробно демонстрирует различные способы получения
    подсписков с помощью срезов.
    """
    print("=== Пример 2: Срезы списков ===")
    
    numbers = list(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Исходный список: {numbers}")
    
    # Базовые срезы
    print("\n1. Базовые срезы:")
    print(f"numbers[2:5] = {numbers[2:5]}")        # [2, 3, 4]
    print(f"numbers[:5] = {numbers[:5]}")          # [0, 1, 2, 3, 4]
    print(f"numbers[5:] = {numbers[5:]}")          # [5, 6, 7, 8, 9]
    print(f"numbers[:] = {numbers[:]}")            # Полная копия
    
    # Срезы с шагом
    print("\n2. Срезы с шагом:")
    print(f"numbers[::2] = {numbers[::2]}")        # [0, 2, 4, 6, 8]
    print(f"numbers[1::2] = {numbers[1::2]}")      # [1, 3, 5, 7, 9]
    print(f"numbers[::3] = {numbers[::3]}")        # [0, 3, 6, 9]
    
    # Отрицательные индексы
    print("\n3. Отрицательные индексы:")
    print(f"numbers[-3:] = {numbers[-3:]}")        # [7, 8, 9]
    print(f"numbers[:-3] = {numbers[:-3]}")        # [0, 1, 2, 3, 4, 5, 6]
    print(f"numbers[-5:-2] = {numbers[-5:-2]}")    # [5, 6, 7]
    
    # Обращение порядка
    print("\n4. Обращение порядка:")
    print(f"numbers[::-1] = {numbers[::-1]}")      # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    print(f"numbers[8:3:-1] = {numbers[8:3:-1]}")  # [8, 7, 6, 5, 4]
    
    # Изменение через срезы
    print("\n5. Изменение через срезы:")
    test_list = [0, 1, 2, 3, 4, 5]
    print(f"До изменения: {test_list}")
    
    test_list[1:4] = [10, 20, 30]
    print(f"После замены [1:4]: {test_list}")
    
    test_list[::2] = [100, 200, 300]
    print(f"После замены [::2]: {test_list}")


def example_03_list_comprehensions():
    """
    Пример 3: Списковые включения
    
    Демонстрирует различные способы создания списков
    с помощью включений (list comprehensions).
    """
    print("=== Пример 3: Списковые включения ===")
    
    # Базовые включения
    print("1. Базовые включения:")
    squares = [x**2 for x in range(5)]
    print(f"Квадраты: {squares}")
    
    words = ["python", "java", "javascript", "go"]
    upper_words = [word.upper() for word in words]
    print(f"Верхний регистр: {upper_words}")
    
    # Включения с условием
    print("\n2. Включения с условием:")
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"Квадраты четных: {even_squares}")
    
    long_words = [word for word in words if len(word) > 4]
    print(f"Длинные слова: {long_words}")
    
    # Условные выражения в включениях
    print("\n3. Условные выражения:")
    abs_values = [x if x >= 0 else -x for x in [-2, -1, 0, 1, 2]]
    print(f"Абсолютные значения: {abs_values}")
    
    categories = ["четное" if x % 2 == 0 else "нечетное" for x in range(5)]
    print(f"Категории: {categories}")
    
    # Вложенные включения
    print("\n4. Вложенные включения:")
    matrix = [[i+j for j in range(3)] for i in range(3)]
    print(f"Матрица: {matrix}")
    
    # Распаковка вложенного списка
    nested = [[1, 2], [3, 4], [5, 6]]
    flattened = [item for sublist in nested for item in sublist]
    print(f"Распакованный: {flattened}")
    
    # Сложные включения
    print("\n5. Сложные включения:")
    # Найти все пары (x, y) где x < y
    pairs = [(x, y) for x in range(3) for y in range(3) if x < y]
    print(f"Пары x < y: {pairs}")
    
    # Обработка строк
    text = "Hello World Python"
    vowel_positions = [(i, char) for i, char in enumerate(text.lower()) 
                      if char in "aeiou"]
    print(f"Позиции гласных: {vowel_positions}")


def example_04_tuples_basics():
    """
    Пример 4: Основы работы с кортежами
    
    Демонстрирует создание кортежей, их особенности,
    распаковку и использование как ключей словарей.
    """
    print("=== Пример 4: Основы работы с кортежами ===")
    
    # Создание кортежей
    print("1. Создание кортежей:")
    empty_tuple = ()
    single_item = (42,)  # Запятая обязательна!
    coordinates = (10, 20)
    mixed_tuple = (1, "hello", 3.14, True)
    nested_tuple = ((1, 2), (3, 4), (5, 6))
    
    print(f"Пустой кортеж: {empty_tuple}")
    print(f"Один элемент: {single_item}")
    print(f"Координаты: {coordinates}")
    print(f"Смешанный: {mixed_tuple}")
    print(f"Вложенный: {nested_tuple}")
    
    # Создание из других типов
    from_list = tuple([1, 2, 3, 4])
    from_string = tuple("hello")
    from_range = tuple(range(5))
    
    print(f"Из списка: {from_list}")
    print(f"Из строки: {from_string}")
    print(f"Из range: {from_range}")
    
    # Основные операции
    print("\n2. Основные операции:")
    numbers = (1, 2, 3, 4, 5, 2, 3)
    
    print(f"Длина: {len(numbers)}")
    print(f"Элемент [2]: {numbers[2]}")
    print(f"Срез [1:4]: {numbers[1:4]}")
    print(f"Индекс элемента 3: {numbers.index(3)}")
    print(f"Количество элементов 2: {numbers.count(2)}")
    print(f"Минимум: {min(numbers)}")
    print(f"Максимум: {max(numbers)}")
    print(f"Сумма: {sum(numbers)}")
    
    # Распаковка кортежей
    print("\n3. Распаковка кортежей:")
    point = (10, 20)
    x, y = point
    print(f"Координаты: x={x}, y={y}")
    
    # Обмен значений
    a, b = 5, 10
    print(f"До обмена: a={a}, b={b}")
    a, b = b, a
    print(f"После обмена: a={a}, b={b}")
    
    # Распаковка с остатком
    first, *middle, last = (1, 2, 3, 4, 5)
    print(f"Первый: {first}, средние: {middle}, последний: {last}")
    
    # Возврат нескольких значений из функции
    def get_name_age():
        return "Alice", 25
    
    name, age = get_name_age()
    print(f"Имя: {name}, возраст: {age}")
    
    # Кортежи как ключи словарей
    print("\n4. Кортежи как ключи словарей:")
    locations = {
        (0, 0): "дом",
        (1, 0): "магазин",
        (0, 1): "школа",
        (1, 1): "парк"
    }
    print(f"Локации: {locations}")
    print(f"В точке (1, 0): {locations[(1, 0)]}")


def example_05_named_tuples():
    """
    Пример 5: Именованные кортежи
    
    Демонстрирует создание и использование именованных
    кортежей для более читаемого кода.
    """
    print("=== Пример 5: Именованные кортежи ===")
    
    # Создание именованного кортежа
    print("1. Создание именованного кортежа:")
    Point = namedtuple('Point', ['x', 'y'])
    Person = namedtuple('Person', ['name', 'age', 'city'])
    
    # Создание экземпляров
    p1 = Point(10, 20)
    p2 = Point(x=30, y=40)
    
    person = Person("Alice", 25, "Moscow")
    
    print(f"Точка 1: {p1}")
    print(f"Точка 2: {p2}")
    print(f"Человек: {person}")
    
    # Доступ к полям
    print("\n2. Доступ к полям:")
    print(f"Координата x: {p1.x}")
    print(f"Координата y: {p1.y}")
    print(f"Имя: {person.name}")
    print(f"Возраст: {person.age}")
    
    # Доступ по индексу (как обычный кортеж)
    print(f"По индексу p1[0]: {p1[0]}")
    print(f"По индексу person[1]: {person[1]}")
    
    # Методы именованных кортежей
    print("\n3. Методы именованных кортежей:")
    
    # _asdict() - преобразование в словарь
    person_dict = person._asdict()
    print(f"Как словарь: {person_dict}")
    
    # _replace() - создание нового с измененными полями
    older_person = person._replace(age=26)
    print(f"Человек постарше: {older_person}")
    
    moved_person = person._replace(city="Saint Petersburg")
    print(f"После переезда: {moved_person}")
    
    # _fields - список полей
    print(f"Поля Point: {Point._fields}")
    print(f"Поля Person: {Person._fields}")
    
    # Создание из итерируемого объекта
    print("\n4. Создание из других объектов:")
    point_data = [50, 60]
    p3 = Point._make(point_data)
    print(f"Из списка: {p3}")
    
    # Практический пример - работа с данными
    print("\n5. Практический пример:")
    Employee = namedtuple('Employee', ['id', 'name', 'department', 'salary'])
    
    employees = [
        Employee(1, "Alice", "IT", 75000),
        Employee(2, "Bob", "HR", 65000),
        Employee(3, "Charlie", "IT", 80000),
    ]
    
    # Вычисление средней зарплаты в IT
    it_salaries = [emp.salary for emp in employees if emp.department == "IT"]
    avg_it_salary = sum(it_salaries) / len(it_salaries)
    print(f"Средняя зарплата в IT: {avg_it_salary}")
    
    # Группировка по отделам
    departments = {}
    for emp in employees:
        if emp.department not in departments:
            departments[emp.department] = []
        departments[emp.department].append(emp.name)
    
    print(f"Сотрудники по отделам: {departments}")


def example_06_dictionaries_basics():
    """
    Пример 6: Основы работы со словарями
    
    Демонстрирует создание словарей, основные операции,
    методы и особенности работы с ними.
    """
    print("=== Пример 6: Основы работы со словарями ===")
    
    # Создание словарей
    print("1. Создание словарей:")
    empty_dict = {}
    person = {"name": "Alice", "age": 25, "city": "Moscow"}
    
    # Различные способы создания
    from_pairs = dict([("a", 1), ("b", 2), ("c", 3)])
    from_kwargs = dict(name="Bob", age=30, city="SPb")
    from_keys = dict.fromkeys(["x", "y", "z"], 0)
    
    print(f"Пустой словарь: {empty_dict}")
    print(f"Человек: {person}")
    print(f"Из пар: {from_pairs}")
    print(f"Из kwargs: {from_kwargs}")
    print(f"Из ключей: {from_keys}")
    
    # Основные операции
    print("\n2. Основные операции:")
    
    # Доступ к элементам
    print(f"Имя: {person['name']}")
    print(f"Возраст: {person.get('age')}")
    print(f"Работа: {person.get('job', 'Не указано')}")  # Значение по умолчанию
    
    # Добавление и изменение
    person["job"] = "Developer"
    person["age"] = 26
    print(f"После изменений: {person}")
    
    # Удаление
    removed_city = person.pop("city")
    print(f"Удален город: {removed_city}")
    print(f"После удаления: {person}")
    
    # Метод setdefault
    person.setdefault("skills", []).append("Python")
    person.setdefault("skills", []).append("JavaScript")
    print(f"С навыками: {person}")
    
    # Обновление из другого словаря
    additional_info = {"experience": 3, "education": "University"}
    person.update(additional_info)
    print(f"После обновления: {person}")
    
    # Проверка наличия ключей
    print("\n3. Проверка наличия ключей:")
    print(f"'name' в словаре: {'name' in person}")
    print(f"'salary' в словаре: {'salary' in person}")
    
    # Представления словаря
    print("\n4. Представления словаря:")
    print(f"Ключи: {list(person.keys())}")
    print(f"Значения: {list(person.values())}")
    print(f"Пары: {list(person.items())}")
    
    # Итерация по словарю
    print("\n5. Итерация по словарю:")
    print("По ключам:")
    for key in person:
        print(f"  {key}: {person[key]}")
    
    print("По парам ключ-значение:")
    for key, value in person.items():
        print(f"  {key} = {value}")


def example_07_dict_comprehensions():
    """
    Пример 7: Словарные включения
    
    Демонстрирует создание словарей с помощью
    словарных включений (dict comprehensions).
    """
    print("=== Пример 7: Словарные включения ===")
    
    # Базовые словарные включения
    print("1. Базовые словарные включения:")
    squares = {x: x**2 for x in range(5)}
    print(f"Квадраты: {squares}")
    
    # Преобразование списков
    words = ["apple", "banana", "cherry"]
    word_lengths = {word: len(word) for word in words}
    print(f"Длины слов: {word_lengths}")
    
    # С условием
    print("\n2. С условием:")
    even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
    print(f"Квадраты четных: {even_squares}")
    
    # Фильтрация существующего словаря
    grades = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 96}
    high_grades = {name: grade for name, grade in grades.items() if grade >= 90}
    print(f"Высокие оценки: {high_grades}")
    
    # Преобразование значений
    print("\n3. Преобразование значений:")
    temperatures_c = {"Москва": 15, "Сочи": 25, "Мурманск": 5}
    temperatures_f = {city: (temp * 9/5) + 32 for city, temp in temperatures_c.items()}
    print(f"Температуры в Фаренгейтах: {temperatures_f}")
    
    # Обмен ключей и значений
    original = {"a": 1, "b": 2, "c": 3}
    swapped = {value: key for key, value in original.items()}
    print(f"Исходный: {original}")
    print(f"Обмененный: {swapped}")
    
    # Группировка данных
    print("\n4. Группировка данных:")
    words = ["apple", "banana", "apricot", "blueberry", "cherry", "coconut"]
    by_first_letter = {}
    for word in words:
        first_letter = word[0]
        if first_letter not in by_first_letter:
            by_first_letter[first_letter] = []
        by_first_letter[first_letter].append(word)
    
    print(f"Группировка по первой букве: {by_first_letter}")
    
    # То же самое через словарное включение с defaultdict
    from collections import defaultdict
    grouped = defaultdict(list)
    for word in words:
        grouped[word[0]].append(word)
    
    print(f"Через defaultdict: {dict(grouped)}")
    
    # Вложенные словарные включения
    print("\n5. Вложенные словарные включения:")
    matrix = {
        i: {j: i*j for j in range(1, 4)} 
        for i in range(1, 4)
    }
    print(f"Таблица умножения: {matrix}")


def example_08_advanced_dicts():
    """
    Пример 8: Продвинутые возможности словарей
    
    Демонстрирует специальные типы словарей из модуля collections
    и их практическое применение.
    """
    print("=== Пример 8: Продвинутые возможности словарей ===")
    
    # defaultdict
    print("1. defaultdict:")
    dd = defaultdict(list)
    
    # Автоматическое создание списков
    dd["fruits"].append("apple")
    dd["fruits"].append("banana")
    dd["vegetables"].append("carrot")
    
    print(f"defaultdict с списками: {dict(dd)}")
    
    # defaultdict с int для подсчета
    counter = defaultdict(int)
    text = "hello world"
    for char in text:
        counter[char] += 1
    
    print(f"Подсчет символов: {dict(counter)}")
    
    # Counter
    print("\n2. Counter:")
    from collections import Counter
    
    # Подсчет элементов
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    word_count = Counter(words)
    print(f"Подсчет слов: {word_count}")
    
    # Наиболее частые элементы
    print(f"Топ-2: {word_count.most_common(2)}")
    
    # Операции с Counter
    counter1 = Counter("hello")
    counter2 = Counter("world")
    print(f"Counter 1: {counter1}")
    print(f"Counter 2: {counter2}")
    print(f"Сложение: {counter1 + counter2}")
    print(f"Вычитание: {counter1 - counter2}")
    print(f"Пересечение: {counter1 & counter2}")
    print(f"Объединение: {counter1 | counter2}")
    
    # OrderedDict (для примера, в современном Python dict сохраняет порядок)
    print("\n3. OrderedDict:")
    od = OrderedDict([("first", 1), ("second", 2), ("third", 3)])
    print(f"OrderedDict: {od}")
    
    # Перемещение элемента в конец
    od.move_to_end("first")
    print(f"После move_to_end: {od}")
    
    # ChainMap
    print("\n4. ChainMap:")
    defaults = {"color": "red", "user": "guest"}
    environment = {"user": "admin"}
    command_line = {"color": "blue"}
    
    combined = ChainMap(command_line, environment, defaults)
    print(f"ChainMap: {dict(combined)}")
    print(f"Цвет: {combined['color']}")  # Из command_line
    print(f"Пользователь: {combined['user']}")  # Из environment
    
    # Практический пример - конфигурация приложения
    print("\n5. Практический пример - конфигурация:")
    
    def get_config():
        """Получение конфигурации с приоритетами"""
        # Значения по умолчанию
        defaults = {
            "host": "localhost",
            "port": 8000,
            "debug": False,
            "database_url": "sqlite:///app.db"
        }
        
        # Переменные окружения (имитация)
        env_vars = {
            "host": "production.server.com",
            "debug": False
        }
        
        # Аргументы командной строки (имитация)
        cli_args = {
            "port": 9000
        }
        
        # Объединение с приоритетами
        config = ChainMap(cli_args, env_vars, defaults)
        return dict(config)
    
    config = get_config()
    print(f"Итоговая конфигурация: {config}")


def example_09_sets_basics():
    """
    Пример 9: Основы работы с множествами
    
    Демонстрирует создание множеств, операции с ними
    и практическое применение.
    """
    print("=== Пример 9: Основы работы с множествами ===")
    
    # Создание множеств
    print("1. Создание множеств:")
    empty_set = set()  # НЕ {}, это пустой словарь!
    numbers = {1, 2, 3, 4, 5}
    from_list = set([1, 2, 2, 3, 3, 4])  # Дубликаты удаляются
    from_string = set("hello")
    
    print(f"Пустое множество: {empty_set}")
    print(f"Числа: {numbers}")
    print(f"Из списка: {from_list}")
    print(f"Из строки: {from_string}")
    
    # Основные операции
    print("\n2. Основные операции:")
    fruits = {"apple", "banana", "cherry"}
    
    # Добавление элементов
    fruits.add("orange")
    print(f"После add: {fruits}")
    
    fruits.update(["grape", "melon"])
    print(f"После update: {fruits}")
    
    # Удаление элементов
    fruits.remove("banana")  # KeyError если элемента нет
    print(f"После remove: {fruits}")
    
    fruits.discard("kiwi")  # Безопасное удаление (без ошибки)
    print(f"После discard несуществующего: {fruits}")
    
    # Случайное удаление
    removed = fruits.pop()
    print(f"Случайно удален: {removed}, остались: {fruits}")
    
    # Проверка принадлежности
    print(f"'apple' в множестве: {'apple' in fruits}")
    print(f"'banana' в множестве: {'banana' in fruits}")
    
    # Математические операции
    print("\n3. Математические операции:")
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}
    
    print(f"Множество A: {set_a}")
    print(f"Множество B: {set_b}")
    
    # Объединение (union)
    union = set_a | set_b
    print(f"Объединение A | B: {union}")
    
    # Пересечение (intersection)
    intersection = set_a & set_b
    print(f"Пересечение A & B: {intersection}")
    
    # Разность (difference)
    difference = set_a - set_b
    print(f"Разность A - B: {difference}")
    
    # Симметрическая разность (symmetric difference)
    sym_diff = set_a ^ set_b
    print(f"Симметрическая разность A ^ B: {sym_diff}")
    
    # Методы с тем же функционалом
    print("\n4. Методы для операций:")
    print(f"union(): {set_a.union(set_b)}")
    print(f"intersection(): {set_a.intersection(set_b)}")
    print(f"difference(): {set_a.difference(set_b)}")
    print(f"symmetric_difference(): {set_a.symmetric_difference(set_b)}")
    
    # Проверки отношений
    print("\n5. Проверки отношений:")
    small_set = {2, 3}
    big_set = {1, 2, 3, 4, 5}
    disjoint_set = {6, 7, 8}
    
    print(f"Малое множество: {small_set}")
    print(f"Большое множество: {big_set}")
    print(f"Непересекающееся: {disjoint_set}")
    
    print(f"Малое подмножество большого: {small_set.issubset(big_set)}")
    print(f"Большое надмножество малого: {big_set.issuperset(small_set)}")
    print(f"Малое и непересекающееся не пересекаются: {small_set.isdisjoint(disjoint_set)}")


def example_10_set_applications():
    """
    Пример 10: Практическое применение множеств
    
    Демонстрирует реальные сценарии использования множеств
    для решения практических задач.
    """
    print("=== Пример 10: Практическое применение множеств ===")
    
    # Удаление дубликатов
    print("1. Удаление дубликатов:")
    numbers_with_duplicates = [1, 2, 3, 2, 4, 3, 5, 1, 6]
    unique_numbers = list(set(numbers_with_duplicates))
    print(f"Исходный список: {numbers_with_duplicates}")
    print(f"Уникальные элементы: {unique_numbers}")
    
    # Сохранение порядка при удалении дубликатов
    def remove_duplicates_preserve_order(items):
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    ordered_unique = remove_duplicates_preserve_order(numbers_with_duplicates)
    print(f"Уникальные с сохранением порядка: {ordered_unique}")
    
    # Поиск общих элементов
    print("\n2. Поиск общих элементов:")
    alice_skills = {"Python", "JavaScript", "SQL", "Git"}
    bob_skills = {"Java", "Python", "Docker", "Git"}
    charlie_skills = {"Python", "C++", "Git", "Linux"}
    
    print(f"Навыки Alice: {alice_skills}")
    print(f"Навыки Bob: {bob_skills}")
    print(f"Навыки Charlie: {charlie_skills}")
    
    # Общие навыки всех троих
    common_skills = alice_skills & bob_skills & charlie_skills
    print(f"Общие навыки всех: {common_skills}")
    
    # Навыки, которые есть у Alice, но нет у Bob
    alice_exclusive = alice_skills - bob_skills
    print(f"Эксклюзивные навыки Alice: {alice_exclusive}")
    
    # Все уникальные навыки команды
    team_skills = alice_skills | bob_skills | charlie_skills
    print(f"Все навыки команды: {team_skills}")
    
    # Фильтрация и валидация
    print("\n3. Фильтрация и валидация:")
    
    # Разрешенные пользователи
    allowed_users = {"admin", "user1", "user2", "guest"}
    
    def check_access(username):
        return username in allowed_users
    
    print(f"Доступ для 'admin': {check_access('admin')}")
    print(f"Доступ для 'hacker': {check_access('hacker')}")
    
    # Проверка разрешений
    required_permissions = {"read", "write"}
    user_permissions = {"read", "write", "execute"}
    
    has_all_permissions = required_permissions.issubset(user_permissions)
    print(f"Есть все необходимые разрешения: {has_all_permissions}")
    
    # Анализ данных
    print("\n4. Анализ данных:")
    
    # Посетители сайта по дням
    monday_visitors = {"user1", "user2", "user3", "user4"}
    tuesday_visitors = {"user2", "user3", "user5", "user6"}
    wednesday_visitors = {"user1", "user3", "user6", "user7"}
    
    print(f"Понедельник: {monday_visitors}")
    print(f"Вторник: {tuesday_visitors}")
    print(f"Среда: {wednesday_visitors}")
    
    # Постоянные посетители (были все дни)
    regular_visitors = monday_visitors & tuesday_visitors & wednesday_visitors
    print(f"Постоянные посетители: {regular_visitors}")
    
    # Новые посетители в среду
    new_wednesday = wednesday_visitors - (monday_visitors | tuesday_visitors)
    print(f"Новые посетители в среду: {new_wednesday}")
    
    # Всего уникальных посетителей
    total_unique = monday_visitors | tuesday_visitors | wednesday_visitors
    print(f"Всего уникальных посетителей: {len(total_unique)}")
    
    # Замороженные множества
    print("\n5. Замороженные множества:")
    
    # Использование как ключей словаря
    groups = {
        frozenset(["alice", "bob"]): "team_alpha",
        frozenset(["charlie", "diana"]): "team_beta",
        frozenset(["eve", "frank", "grace"]): "team_gamma"
    }
    
    print("Команды:")
    for members, team_name in groups.items():
        print(f"  {team_name}: {set(members)}")
    
    # Поиск команды по участнику
    def find_team(person):
        for members, team_name in groups.items():
            if person in members:
                return team_name
        return "Не найден"
    
    print(f"Команда Alice: {find_team('alice')}")
    print(f"Команда Charlie: {find_team('charlie')}")


def example_11_performance_comparison():
    """
    Пример 11: Сравнение производительности структур данных
    
    Демонстрирует различия в производительности операций
    для разных структур данных.
    """
    print("=== Пример 11: Сравнение производительности структур данных ===")
    
    # Подготовка данных
    size = 10000
    test_data = list(range(size))
    test_list = test_data.copy()
    test_set = set(test_data)
    test_dict = {i: f"value_{i}" for i in test_data}
    
    search_item = size - 1  # Последний элемент (худший случай для списка)
    
    print(f"Тестирование на {size} элементах")
    print(f"Поиск элемента: {search_item}")
    
    # Тест поиска элемента
    print("\n1. Скорость поиска элемента:")
    
    # Поиск в списке - O(n)
    start_time = time.perf_counter()
    result = search_item in test_list
    list_time = time.perf_counter() - start_time
    
    # Поиск в множестве - O(1)
    start_time = time.perf_counter()
    result = search_item in test_set
    set_time = time.perf_counter() - start_time
    
    # Поиск в словаре - O(1)
    start_time = time.perf_counter()
    result = search_item in test_dict
    dict_time = time.perf_counter() - start_time
    
    print(f"Список: {list_time:.6f} сек")
    print(f"Множество: {set_time:.6f} сек")
    print(f"Словарь: {dict_time:.6f} сек")
    print(f"Множество быстрее списка в {list_time/set_time:.1f} раз")
    
    # Тест добавления элементов
    print("\n2. Скорость добавления элементов:")
    
    def test_list_append():
        lst = []
        for i in range(1000):
            lst.append(i)
        return lst
    
    def test_set_add():
        s = set()
        for i in range(1000):
            s.add(i)
        return s
    
    def test_dict_assign():
        d = {}
        for i in range(1000):
            d[i] = f"value_{i}"
        return d
    
    list_append_time = timeit.timeit(test_list_append, number=100)
    set_add_time = timeit.timeit(test_set_add, number=100)
    dict_assign_time = timeit.timeit(test_dict_assign, number=100)
    
    print(f"Добавление в список: {list_append_time:.6f} сек")
    print(f"Добавление в множество: {set_add_time:.6f} сек")
    print(f"Добавление в словарь: {dict_assign_time:.6f} сек")
    
    # Использование памяти
    print("\n3. Использование памяти:")
    
    sample_data = list(range(1000))
    sample_list = sample_data.copy()
    sample_tuple = tuple(sample_data)
    sample_set = set(sample_data)
    sample_dict = {i: i for i in sample_data}
    
    print(f"Список (1000 элементов): {sys.getsizeof(sample_list)} байт")
    print(f"Кортеж (1000 элементов): {sys.getsizeof(sample_tuple)} байт")
    print(f"Множество (1000 элементов): {sys.getsizeof(sample_set)} байт")
    print(f"Словарь (1000 элементов): {sys.getsizeof(sample_dict)} байт")
    
    # Практические рекомендации
    print("\n4. Практические рекомендации:")
    print("Используйте:")
    print("• Список - для упорядоченных данных с доступом по индексу")
    print("• Кортеж - для неизменяемых упорядоченных данных")
    print("• Множество - для уникальных элементов и быстрого поиска")
    print("• Словарь - для связи ключ-значение с быстрым доступом")


def example_12_nested_structures():
    """
    Пример 12: Вложенные структуры данных
    
    Демонстрирует работу со сложными вложенными структурами,
    их обход и модификацию.
    """
    print("=== Пример 12: Вложенные структуры данных ===")
    
    # Сложная структура данных
    print("1. Сложная структура данных:")
    
    company = {
        "name": "TechCorp",
        "founded": 2010,
        "departments": {
            "IT": {
                "head": "Alice Johnson",
                "employees": [
                    {"name": "Bob Smith", "position": "Developer", "skills": ["Python", "JavaScript"]},
                    {"name": "Carol Brown", "position": "DevOps", "skills": ["Docker", "Kubernetes"]},
                    {"name": "David Wilson", "position": "Developer", "skills": ["Java", "Spring"]}
                ],
                "budget": 500000
            },
            "HR": {
                "head": "Eve Davis",
                "employees": [
                    {"name": "Frank Miller", "position": "Recruiter", "skills": ["Interviewing", "Sourcing"]},
                    {"name": "Grace Lee", "position": "HR Manager", "skills": ["Management", "Policy"]}
                ],
                "budget": 200000
            }
        },
        "technologies": {"Python", "JavaScript", "Java", "Docker", "Kubernetes"}
    }
    
    print(f"Компания: {company['name']}")
    print(f"Основана: {company['founded']}")
    
    # Обход вложенной структуры
    print("\n2. Обход и анализ данных:")
    
    total_employees = 0
    all_skills = set()
    
    for dept_name, dept_info in company["departments"].items():
        print(f"\nОтдел {dept_name}:")
        print(f"  Руководитель: {dept_info['head']}")
        print(f"  Бюджет: ${dept_info['budget']:,}")
        print(f"  Сотрудники:")
        
        for employee in dept_info["employees"]:
            print(f"    {employee['name']} - {employee['position']}")
            total_employees += 1
            all_skills.update(employee["skills"])
    
    print(f"\nВсего сотрудников: {total_employees}")
    print(f"Все навыки в компании: {all_skills}")
    
    # Поиск в вложенной структуре
    print("\n3. Поиск в структуре:")
    
    def find_employee(company_data, employee_name):
        """Найти сотрудника по имени"""
        for dept_name, dept_info in company_data["departments"].items():
            for employee in dept_info["employees"]:
                if employee["name"] == employee_name:
                    return {
                        "department": dept_name,
                        "employee": employee,
                        "head": dept_info["head"]
                    }
        return None
    
    search_name = "Bob Smith"
    result = find_employee(company, search_name)
    if result:
        print(f"Найден {search_name}:")
        print(f"  Отдел: {result['department']}")
        print(f"  Должность: {result['employee']['position']}")
        print(f"  Руководитель: {result['head']}")
    
    # Модификация вложенной структуры
    print("\n4. Модификация структуры:")
    
    # Добавление нового сотрудника
    new_employee = {
        "name": "Helen Taylor",
        "position": "Data Scientist", 
        "skills": ["Python", "Machine Learning", "SQL"]
    }
    
    company["departments"]["IT"]["employees"].append(new_employee)
    company["technologies"].update(new_employee["skills"])
    
    print(f"Добавлен новый сотрудник: {new_employee['name']}")
    print(f"Обновленные технологии: {company['technologies']}")
    
    # Агрегация данных
    print("\n5. Агрегация данных:")
    
    # Группировка сотрудников по должностям
    positions = {}
    for dept_info in company["departments"].values():
        for employee in dept_info["employees"]:
            position = employee["position"]
            if position not in positions:
                positions[position] = []
            positions[position].append(employee["name"])
    
    print("Сотрудники по должностям:")
    for position, names in positions.items():
        print(f"  {position}: {', '.join(names)}")
    
    # Подсчет навыков
    skill_count = {}
    for dept_info in company["departments"].values():
        for employee in dept_info["employees"]:
            for skill in employee["skills"]:
                skill_count[skill] = skill_count.get(skill, 0) + 1
    
    print("\nПопулярность навыков:")
    sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
    for skill, count in sorted_skills:
        print(f"  {skill}: {count} человек")
    
    # Глубокое и поверхностное копирование
    print("\n6. Копирование сложных структур:")
    
    # Поверхностное копирование - опасно для вложенных структур
    shallow_copy = company.copy()
    shallow_copy["departments"]["IT"]["budget"] = 600000
    
    print(f"Исходный бюджет IT: {company['departments']['IT']['budget']}")
    print("Поверхностное копирование изменило исходные данные!")
    
    # Глубокое копирование
    deep_copy = copy.deepcopy(company)
    deep_copy["departments"]["IT"]["budget"] = 700000
    
    print(f"После глубокого копирования исходный бюджет: {company['departments']['IT']['budget']}")
    print(f"Бюджет в глубокой копии: {deep_copy['departments']['IT']['budget']}")


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Основы работы со списками", example_01_lists_basics),
        ("Срезы списков", example_02_list_slicing),
        ("Списковые включения", example_03_list_comprehensions),
        ("Основы работы с кортежами", example_04_tuples_basics),
        ("Именованные кортежи", example_05_named_tuples),
        ("Основы работы со словарями", example_06_dictionaries_basics),
        ("Словарные включения", example_07_dict_comprehensions),
        ("Продвинутые возможности словарей", example_08_advanced_dicts),
        ("Основы работы с множествами", example_09_sets_basics),
        ("Практическое применение множеств", example_10_set_applications),
        ("Сравнение производительности", example_11_performance_comparison),
        ("Вложенные структуры данных", example_12_nested_structures),
    ]
    
    print("🏗️ Примеры: Структуры данных Python")
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