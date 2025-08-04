"""
Примеры: Современный Python (3.8+)

Этот файл содержит практические примеры использования современных возможностей
Python 3.8+, включая walrus operator, pattern matching, positional-only
параметры и другие новые возможности.
"""

import sys
import json
import re
import functools
from typing import Any, Dict, List, Optional, Union, Literal
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from enum import Enum, auto

# =============================================================================
# Пример 1: Walrus Operator (:=) в различных сценариях
# =============================================================================

def walrus_in_conditions():
    """Использование walrus operator в условных выражениях"""
    
    print("=== Walrus Operator в условиях ===")
    
    # Традиционный подход
    data = [1, 2, 3, 4, 5]
    length = len(data)
    if length > 3:
        print(f"Traditional: List has {length} items (more than 3)")
    
    # С walrus operator
    if (length := len(data)) > 3:
        print(f"Walrus: List has {length} items (more than 3)")
    
    # Проверка и использование результата вычисления
    text = "Hello, World!"
    if (match := re.search(r'(\w+), (\w+)!', text)):
        greeting, target = match.groups()
        print(f"Found greeting: '{greeting}' to '{target}'")

def walrus_in_loops():
    """Использование walrus operator в циклах"""
    
    print("\n=== Walrus Operator в циклах ===")
    
    # Чтение файла построчно
    sample_lines = ["line 1", "line 2", "", "line 4", ""]
    line_iterator = iter(sample_lines)
    
    print("Processing lines:")
    while (line := next(line_iterator, None)) is not None:
        if line.strip():  # Пропускаем пустые строки
            print(f"  Processing: {line}")
        else:
            print("  Skipping empty line")
    
    # Обработка данных с условием
    numbers = [1, 4, 9, 16, 25, 36, 49]
    print(f"\nSquare roots greater than 4:")
    for num in numbers:
        if (sqrt_val := num ** 0.5) > 4:
            print(f"  √{num} = {sqrt_val:.2f}")

def walrus_in_comprehensions():
    """Использование walrus operator в comprehensions"""
    
    print("\n=== Walrus Operator в comprehensions ===")
    
    # Избегаем повторных вычислений
    def expensive_computation(x):
        """Имитация дорогого вычисления"""
        print(f"    Computing for {x}")
        return x ** 2 + x + 1
    
    data = [1, 2, 3, 4, 5]
    
    # Традиционный подход (вычисляем дважды)
    traditional = [expensive_computation(x) for x in data if expensive_computation(x) > 10]
    print(f"Traditional (computed twice): {traditional}")
    
    # С walrus operator (вычисляем один раз)
    walrus_result = [result for x in data if (result := expensive_computation(x)) > 10]
    print(f"Walrus (computed once): {walrus_result}")
    
    # Сохранение промежуточных результатов
    text_data = ["hello", "world", "python", "programming", "a"]
    uppercase_long = [
        upper_text for text in text_data 
        if len(upper_text := text.upper()) > 5
    ]
    print(f"Long uppercase words: {uppercase_long}")

# =============================================================================
# Пример 2: Structural Pattern Matching (Python 3.10+)
# =============================================================================

@dataclass
class Point:
    x: float
    y: float

@dataclass 
class Circle:
    center: Point
    radius: float

@dataclass
class Rectangle:
    top_left: Point
    width: float
    height: float

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

def pattern_matching_basics():
    """Базовые примеры pattern matching"""
    
    print("\n=== Pattern Matching: Основы ===")
    
    def describe_data(data):
        match data:
            case int() if data > 0:
                return f"Positive integer: {data}"
            case int() if data < 0:
                return f"Negative integer: {data}"
            case 0:
                return "Zero"
            case str() if len(data) > 0:
                return f"Non-empty string: '{data}'"
            case str():
                return "Empty string"
            case list() if len(data) == 0:
                return "Empty list"
            case list() if len(data) == 1:
                return f"Single-item list: {data[0]}"
            case list():
                return f"List with {len(data)} items"
            case _:
                return f"Unknown type: {type(data).__name__}"
    
    test_values = [42, -10, 0, "hello", "", [], [1], [1, 2, 3], {"key": "value"}]
    
    for value in test_values:
        result = describe_data(value)
        print(f"  {value!r} -> {result}")

def pattern_matching_structures():
    """Pattern matching для структур данных"""
    
    print("\n=== Pattern Matching: Структуры данных ===")
    
    def process_coordinates(data):
        match data:
            case {"x": x, "y": y} if x >= 0 and y >= 0:
                return f"Point in first quadrant: ({x}, {y})"
            case {"x": x, "y": y}:
                return f"Point: ({x}, {y})"
            case {"lat": lat, "lon": lon}:
                return f"GPS coordinates: {lat}, {lon}"
            case [x, y] if len(data) == 2:
                return f"2D coordinates: ({x}, {y})"
            case [x, y, z] if len(data) == 3:
                return f"3D coordinates: ({x}, {y}, {z})"
            case _:
                return "Unknown coordinate format"
    
    coordinates = [
        {"x": 10, "y": 20},
        {"x": -5, "y": 15},
        {"lat": 40.7128, "lon": -74.0060},
        [1, 2],
        [1, 2, 3],
        "invalid"
    ]
    
    for coord in coordinates:
        result = process_coordinates(coord)
        print(f"  {coord} -> {result}")

def pattern_matching_objects():
    """Pattern matching для объектов"""
    
    print("\n=== Pattern Matching: Объекты ===")
    
    def analyze_shape(shape):
        match shape:
            case Point(x=0, y=0):
                return "Origin point"
            case Point(x=x, y=y) if x == y:
                return f"Point on diagonal: ({x}, {y})"
            case Point(x=x, y=y):
                return f"Point: ({x}, {y})"
            case Circle(center=Point(x=0, y=0), radius=r):
                return f"Circle at origin with radius {r}"
            case Circle(center=center, radius=r):
                return f"Circle at {center} with radius {r}"
            case Rectangle(top_left=Point(x=0, y=0), width=w, height=h):
                return f"Rectangle at origin: {w}x{h}"
            case Rectangle(top_left=tl, width=w, height=h):
                return f"Rectangle at {tl}: {w}x{h}"
            case _:
                return f"Unknown shape: {type(shape).__name__}"
    
    shapes = [
        Point(0, 0),
        Point(5, 5),
        Point(3, 7),
        Circle(Point(0, 0), 10),
        Circle(Point(5, 5), 3),
        Rectangle(Point(0, 0), 10, 8),
        Rectangle(Point(2, 3), 6, 4)
    ]
    
    for shape in shapes:
        result = analyze_shape(shape)
        print(f"  {shape} -> {result}")

def pattern_matching_api_responses():
    """Pattern matching для обработки API ответов"""
    
    print("\n=== Pattern Matching: API ответы ===")
    
    def handle_api_response(response):
        match response:
            case {"status": "success", "data": data, "count": count}:
                return f"Success: received {count} items"
            case {"status": "success", "data": data}:
                return f"Success: received data with {len(data)} items"
            case {"status": "error", "error_code": 404, "message": msg}:
                return f"Not found error: {msg}"
            case {"status": "error", "error_code": code, "message": msg}:
                return f"Error {code}: {msg}"
            case {"status": "pending", "eta": eta}:
                return f"Request pending, ETA: {eta}"
            case {"status": status}:
                return f"Unknown status: {status}"
            case _:
                return "Invalid response format"
    
    responses = [
        {"status": "success", "data": [1, 2, 3], "count": 3},
        {"status": "success", "data": ["a", "b"]},
        {"status": "error", "error_code": 404, "message": "Resource not found"},
        {"status": "error", "error_code": 500, "message": "Internal server error"},
        {"status": "pending", "eta": "2 minutes"},
        {"status": "unknown"},
        {"invalid": "response"}
    ]
    
    for response in responses:
        result = handle_api_response(response)
        print(f"  {response} -> {result}")

# =============================================================================
# Пример 3: Positional-Only Parameters
# =============================================================================

def positional_only_examples():
    """Примеры использования positional-only параметров"""
    
    print("\n=== Positional-Only Parameters ===")
    
    def calculate_stats(values, /, *, method="mean"):
        """
        Вычисляет статистику для значений
        
        Args:
            values: список значений (positional-only)
            method: метод расчета (keyword-only)
        """
        if method == "mean":
            return sum(values) / len(values)
        elif method == "median":
            sorted_vals = sorted(values)
            n = len(sorted_vals)
            return sorted_vals[n // 2] if n % 2 else (sorted_vals[n//2-1] + sorted_vals[n//2]) / 2
        elif method == "max":
            return max(values)
        elif method == "min":
            return min(values)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    data = [1, 5, 3, 9, 2, 7]
    
    # Правильное использование
    print(f"Mean: {calculate_stats(data)}")
    print(f"Median: {calculate_stats(data, method='median')}")
    print(f"Max: {calculate_stats(data, method='max')}")
    
    # Это работает
    try:
        result = calculate_stats([1, 2, 3], method="mean")
        print(f"Valid call: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Это НЕ работает (раскомментируйте для проверки)
    # calculate_stats(values=data)  # TypeError: positional-only argument passed as keyword
    
    def flexible_function(pos_only, /, normal, *, kw_only):
        """
        Функция с тремя типами параметров
        
        Args:
            pos_only: только позиционный
            normal: может быть позиционным или именованным
            kw_only: только именованный
        """
        return f"pos_only={pos_only}, normal={normal}, kw_only={kw_only}"
    
    # Различные способы вызова
    print("\nFlexible function calls:")
    print(flexible_function(1, 2, kw_only=3))
    print(flexible_function(1, normal=2, kw_only=3))
    # print(flexible_function(pos_only=1, normal=2, kw_only=3))  # Error!

def api_design_with_positional_only():
    """Дизайн API с positional-only параметрами"""
    
    print("\n=== API Design с Positional-Only ===")
    
    def create_user(name, email, /, *, age=None, department=None, active=True):
        """
        Создает пользователя
        
        Основные параметры (name, email) - positional-only для стабильности API
        Дополнительные параметры - keyword-only для ясности
        """
        user = {
            "name": name,
            "email": email,
            "age": age,
            "department": department,
            "active": active,
            "created_at": datetime.now().isoformat()
        }
        return user
    
    # Различные способы создания пользователей
    user1 = create_user("Alice", "alice@example.com")
    user2 = create_user("Bob", "bob@example.com", age=30, department="IT")
    user3 = create_user("Charlie", "charlie@example.com", active=False, age=25)
    
    for i, user in enumerate([user1, user2, user3], 1):
        print(f"User {i}: {user['name']} ({user['email']}) - Active: {user['active']}")

# =============================================================================
# Пример 4: Улучшения f-strings
# =============================================================================

def modern_f_strings():
    """Современные возможности f-strings"""
    
    print("\n=== Современные f-strings ===")
    
    # Отладочные выражения (Python 3.8+)
    x = 42
    y = 24
    name = "Python"
    
    print("Debug expressions:")
    print(f"{x=}")  # Выведет: x=42
    print(f"{y=}")  # Выведет: y=24
    print(f"{x + y=}")  # Выведет: x + y=66
    print(f"{name.upper()=}")  # Выведет: name.upper()='PYTHON'
    
    # Вложенные кавычки (Python 3.12+)
    # Теперь можно использовать одинаковые кавычки внутри f-strings
    data = {"name": "Alice", "age": 30}
    if sys.version_info >= (3, 12):
        # В Python 3.12+ это работает
        message = f"User info: {json.dumps(data)}"
        print(f"Nested quotes: {message}")
    else:
        # Для старых версий используем другие кавычки
        message = f'User info: {json.dumps(data)}'
        print(f"Nested quotes: {message}")
    
    # Многострочные f-strings с отладкой
    values = [1, 2, 3, 4, 5]
    result = (
        f"Statistics for {values=}:\n"
        f"  Length: {len(values)=}\n"
        f"  Sum: {sum(values)=}\n"
        f"  Average: {sum(values)/len(values)=:.2f}\n"
        f"  Max: {max(values)=}\n"
        f"  Min: {min(values)=}"
    )
    print(f"\nMultiline f-string with debug:\n{result}")
    
    # Сложные выражения с отладкой
    def calculate_something(a, b):
        return a ** 2 + b ** 2
    
    a, b = 3, 4
    print(f"\nComplex expressions:")
    print(f"{calculate_something(a, b)=}")
    print(f"{[x**2 for x in range(5)]=}")
    print(f"{dict(zip(['a', 'b', 'c'], [1, 2, 3]))=}")

# =============================================================================
# Пример 5: Операторы слияния словарей
# =============================================================================

def dictionary_merge_operators():
    """Новые операторы слияния словарей"""
    
    print("\n=== Операторы слияния словарей ===")
    
    # Базовые словари
    defaults = {"timeout": 30, "retries": 3, "debug": False}
    user_config = {"timeout": 60, "host": "localhost"}
    override_config = {"debug": True, "verbose": True}
    
    print(f"Defaults: {defaults}")
    print(f"User config: {user_config}")
    print(f"Override config: {override_config}")
    
    # Оператор слияния | (создает новый словарь)
    merged_config = defaults | user_config | override_config
    print(f"\nMerged config (|): {merged_config}")
    
    # Исходные словари не изменились
    print(f"Defaults after merge: {defaults}")
    
    # Оператор обновления |= (изменяет существующий словарь)
    config_copy = defaults.copy()
    config_copy |= user_config
    config_copy |= override_config
    print(f"In-place merged (|=): {config_copy}")
    
    # Сравнение с традиционными методами
    print("\n--- Сравнение методов ---")
    
    # Старый метод с update()
    old_method = defaults.copy()
    old_method.update(user_config)
    old_method.update(override_config)
    print(f"Old method (update): {old_method}")
    
    # Старый метод с unpacking
    unpacking_method = {**defaults, **user_config, **override_config}
    print(f"Old method (unpacking): {unpacking_method}")
    
    # Новый метод
    new_method = defaults | user_config | override_config
    print(f"New method (|): {new_method}")
    
    # Проверяем, что результаты одинаковые
    print(f"All methods give same result: {old_method == unpacking_method == new_method}")

def practical_dictionary_merging():
    """Практические примеры слияния словарей"""
    
    print("\n=== Практические примеры слияния ===")
    
    # Конфигурация приложения
    default_settings = {
        "database": {"host": "localhost", "port": 5432, "timeout": 30},
        "cache": {"enabled": True, "ttl": 3600},
        "logging": {"level": "INFO", "format": "%(asctime)s - %(message)s"}
    }
    
    production_settings = {
        "database": {"host": "prod-db.example.com", "ssl": True},
        "cache": {"ttl": 7200},
        "logging": {"level": "WARNING"}
    }
    
    # Глубокое слияние (нужна специальная функция)
    def deep_merge(dict1, dict2):
        """Глубокое слияние словарей"""
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    # Поверхностное слияние
    shallow_config = default_settings | production_settings
    print("Shallow merge:")
    for section, config in shallow_config.items():
        print(f"  {section}: {config}")
    
    # Глубокое слияние
    deep_config = deep_merge(default_settings, production_settings)
    print("\nDeep merge:")
    for section, config in deep_config.items():
        print(f"  {section}: {config}")

# =============================================================================
# Пример 6: Встроенные generics (Python 3.9+)
# =============================================================================

def builtin_generics_examples():
    """Примеры встроенных generic типов"""
    
    print("\n=== Встроенные Generic типы ===")
    
    # Функция с новым синтаксисом типов
    def process_items(items: list[str]) -> dict[str, int]:
        """Обрабатывает список строк и возвращает словарь с подсчетом"""
        result: dict[str, int] = {}
        for item in items:
            result[item] = result.get(item, 0) + 1
        return result
    
    def find_common_elements(list1: list[str], list2: list[str]) -> set[str]:
        """Находит общие элементы в двух списках"""
        return set(list1) & set(list2)
    
    def group_by_length(words: list[str]) -> dict[int, list[str]]:
        """Группирует слова по длине"""
        groups: dict[int, list[str]] = {}
        for word in words:
            length = len(word)
            if length not in groups:
                groups[length] = []
            groups[length].append(word)
        return groups
    
    # Тестирование функций
    test_words = ["python", "java", "go", "rust", "javascript", "c", "ruby"]
    test_words2 = ["python", "kotlin", "swift", "go", "scala"]
    
    print(f"Word counts: {process_items(test_words)}")
    print(f"Common languages: {find_common_elements(test_words, test_words2)}")
    print(f"Grouped by length: {group_by_length(test_words)}")
    
    # Сложные generic типы
    def analyze_data(data: dict[str, list[tuple[str, int]]]) -> dict[str, dict[str, int]]:
        """Анализирует сложную структуру данных"""
        result: dict[str, dict[str, int]] = {}
        for category, items in data.items():
            category_stats: dict[str, int] = {
                "total_items": len(items),
                "total_value": sum(value for _, value in items),
                "max_value": max(value for _, value in items) if items else 0
            }
            result[category] = category_stats
        return result
    
    sample_data: dict[str, list[tuple[str, int]]] = {
        "fruits": [("apple", 5), ("banana", 3), ("orange", 8)],
        "vegetables": [("carrot", 2), ("broccoli", 4)],
        "grains": [("rice", 10), ("wheat", 15), ("oats", 7)]
    }
    
    analysis = analyze_data(sample_data)
    print(f"\nData analysis:")
    for category, stats in analysis.items():
        print(f"  {category}: {stats}")

# =============================================================================
# Пример 7: Улучшения functools
# =============================================================================

def functools_improvements():
    """Новые возможности functools"""
    
    print("\n=== Улучшения functools ===")
    
    # @cache декоратор (Python 3.9+)
    @functools.cache
    def fibonacci(n):
        """Числа Фибоначчи с кэшированием"""
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    # Демонстрация кэширования
    import time
    
    print("Fibonacci with caching:")
    start_time = time.time()
    result = fibonacci(35)
    first_call_time = time.time() - start_time
    print(f"  fibonacci(35) = {result} (first call: {first_call_time:.4f}s)")
    
    start_time = time.time()
    result = fibonacci(35)
    second_call_time = time.time() - start_time
    print(f"  fibonacci(35) = {result} (cached call: {second_call_time:.6f}s)")
    print(f"  Speedup: {first_call_time / second_call_time:.0f}x")
    
    # cached_property для классов
    class DataProcessor:
        """Класс с кэшированными свойствами"""
        
        def __init__(self, data: list[int]):
            self.data = data
        
        @functools.cached_property
        def statistics(self) -> dict[str, float]:
            """Вычисляет статистику (кэшируется после первого вызова)"""
            print("    Computing statistics...")
            return {
                "mean": sum(self.data) / len(self.data),
                "median": sorted(self.data)[len(self.data) // 2],
                "std": (sum((x - sum(self.data) / len(self.data))**2 for x in self.data) / len(self.data))**0.5
            }
        
        @functools.cached_property
        def summary(self) -> str:
            """Создает сводку (использует кэшированную статистику)"""
            stats = self.statistics
            return f"Mean: {stats['mean']:.2f}, Median: {stats['median']:.2f}, Std: {stats['std']:.2f}"
    
    processor = DataProcessor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    print("\nCached properties:")
    print(f"First call to statistics: {processor.statistics}")
    print(f"Second call to statistics: {processor.statistics}")  # Не вычисляется заново
    print(f"Summary: {processor.summary}")
    
    # singledispatch улучшения
    @functools.singledispatch
    def format_value(value):
        """Форматирует значение по умолчанию"""
        return f"Unknown type: {type(value).__name__}({value})"
    
    @format_value.register
    def _(value: int):
        return f"Integer: {value:,}"
    
    @format_value.register
    def _(value: float):
        return f"Float: {value:.2f}"
    
    @format_value.register
    def _(value: str):
        return f"String: '{value}'"
    
    @format_value.register
    def _(value: list):
        return f"List with {len(value)} items: {value[:3]}{'...' if len(value) > 3 else ''}"
    
    test_values = [42, 3.14159, "hello", [1, 2, 3, 4, 5], {"key": "value"}]
    
    print("\nSingle dispatch formatting:")
    for value in test_values:
        print(f"  {format_value(value)}")

# =============================================================================
# Пример 8: Практическое применение современного Python
# =============================================================================

class ModernAPIClient:
    """Современный API клиент с использованием новых возможностей Python"""
    
    def __init__(self, base_url: str, /, *, timeout: int = 30, retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries
        self.session_data: dict[str, Any] = {}
    
    @functools.cache
    def get_headers(self) -> dict[str, str]:
        """Получает заголовки (кэшируется)"""
        return {
            "User-Agent": "ModernAPIClient/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def make_request(self, endpoint: str, /, data: Optional[dict[str, Any]] = None, 
                    *, method: Literal["GET", "POST", "PUT", "DELETE"] = "GET") -> dict[str, Any]:
        """Выполняет HTTP запрос"""
        
        # Симуляция HTTP запроса
        request_info = {
            "url": f"{self.base_url}/{endpoint.lstrip('/')}",
            "method": method,
            "headers": self.get_headers(),
            "timeout": self.timeout
        }
        
        if data:
            request_info["data"] = data
        
        # Симуляция ответа в зависимости от endpoint
        match endpoint:
            case "users" if method == "GET":
                response = {
                    "status": "success",
                    "data": [
                        {"id": 1, "name": "Alice", "email": "alice@example.com"},
                        {"id": 2, "name": "Bob", "email": "bob@example.com"}
                    ],
                    "total": 2
                }
            case "users" if method == "POST":
                new_user = data or {}
                response = {
                    "status": "success", 
                    "data": {"id": 3, **new_user},
                    "message": "User created successfully"
                }
            case endpoint if endpoint.startswith("users/"):
                user_id = endpoint.split("/")[1]
                if user_id.isdigit():
                    response = {
                        "status": "success",
                        "data": {"id": int(user_id), "name": f"User {user_id}", "email": f"user{user_id}@example.com"}
                    }
                else:
                    response = {"status": "error", "error_code": 400, "message": "Invalid user ID"}
            case _:
                response = {"status": "error", "error_code": 404, "message": "Endpoint not found"}
        
        return response
    
    def process_response(self, response: dict[str, Any]) -> str:
        """Обрабатывает ответ API"""
        match response:
            case {"status": "success", "data": data, "total": total}:
                return f"Success: Retrieved {total} items"
            case {"status": "success", "data": data, "message": message}:
                return f"Success: {message}"
            case {"status": "success", "data": data}:
                return f"Success: Received data"
            case {"status": "error", "error_code": 404, "message": msg}:
                return f"Not Found: {msg}"
            case {"status": "error", "error_code": code, "message": msg}:
                return f"Error {code}: {msg}"
            case _:
                return "Unknown response format"

def demonstrate_modern_api_client():
    """Демонстрация современного API клиента"""
    
    print("\n=== Современный API клиент ===")
    
    # Создание клиента с positional-only и keyword-only параметрами
    client = ModernAPIClient("https://api.example.com", timeout=60, retries=5)
    
    # Тестирование различных запросов
    test_cases = [
        ("users", "GET", None),
        ("users", "POST", {"name": "Charlie", "email": "charlie@example.com"}),
        ("users/1", "GET", None),
        ("users/abc", "GET", None),
        ("nonexistent", "GET", None)
    ]
    
    for endpoint, method, data in test_cases:
        response = client.make_request(endpoint, data, method=method)
        result = client.process_response(response)
        print(f"  {method} /{endpoint}: {result}")

def practical_walrus_example():
    """Практический пример использования walrus operator"""
    
    print("\n=== Практический пример: Анализ лог-файла ===")
    
    # Симуляция лог-файла
    log_lines = [
        "2024-01-15 10:30:25 INFO User login: alice@example.com",
        "2024-01-15 10:31:45 ERROR Database connection failed",
        "2024-01-15 10:32:10 INFO User login: bob@example.com", 
        "2024-01-15 10:33:22 WARNING High memory usage: 85%",
        "2024-01-15 10:34:01 ERROR API request timeout",
        "2024-01-15 10:35:15 INFO User logout: alice@example.com",
        "2024-01-15 10:36:30 CRITICAL Database corrupted",
    ]
    
    # Анализ с walrus operator
    error_count = 0
    warning_count = 0
    users = set()
    
    for line in log_lines:
        # Извлечение информации с walrus operator
        if (match := re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)', line)):
            timestamp, level, message = match.groups()
            
            # Подсчет ошибок и предупреждений
            if level in ("ERROR", "CRITICAL"):
                error_count += 1
            elif level == "WARNING":
                warning_count += 1
            
            # Извлечение пользователей
            if (user_match := re.search(r'User \w+: (\S+@\S+)', message)):
                users.add(user_match.group(1))
            
            # Обработка критических ошибок
            if level == "CRITICAL":
                print(f"  CRITICAL ALERT: {message} at {timestamp}")
    
    print(f"Log analysis complete:")
    print(f"  Total errors: {error_count}")
    print(f"  Total warnings: {warning_count}")
    print(f"  Unique users: {len(users)} ({', '.join(users)})")

# =============================================================================
# Главная функция для демонстрации всех примеров
# =============================================================================

def main():
    """Запуск всех примеров современного Python"""
    
    print("=== Современный Python (3.8+) ===")
    
    # Walrus operator примеры
    walrus_in_conditions()
    walrus_in_loops()
    walrus_in_comprehensions()
    
    # Pattern matching (требует Python 3.10+)
    if sys.version_info >= (3, 10):
        pattern_matching_basics()
        pattern_matching_structures()
        pattern_matching_objects()
        pattern_matching_api_responses()
    else:
        print("\n=== Pattern Matching ===")
        print("Pattern matching requires Python 3.10+")
        print(f"Current version: {sys.version}")
    
    # Positional-only parameters
    positional_only_examples()
    api_design_with_positional_only()
    
    # F-strings improvements
    modern_f_strings()
    
    # Dictionary merge operators (Python 3.9+)
    if sys.version_info >= (3, 9):
        dictionary_merge_operators()
        practical_dictionary_merging()
        builtin_generics_examples()
    else:
        print("\n=== Dictionary Merge Operators ===")
        print("Dictionary merge operators require Python 3.9+")
        print(f"Current version: {sys.version}")
    
    # functools improvements
    functools_improvements()
    
    # Практические примеры
    demonstrate_modern_api_client()
    practical_walrus_example()

if __name__ == "__main__":
    main() 