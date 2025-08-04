# Современные возможности Python 3.8+
import sys
from functools import cache, lru_cache
from typing import Union
import math

print(f"Python версия: {sys.version_info}")

# Python 3.8+ возможности
if sys.version_info >= (3, 8):
    print("\n=== Python 3.8+ возможности ===")
    
    # Positional-only параметры
    def greet(name, /, greeting="Привет"):
        """name - только позиционный, greeting - может быть keyword"""
        return f"{greeting}, {name}!"
    
    print(greet("Анна"))
    print(greet("Иван", greeting="Добро пожаловать"))
    
    # f-strings с = для отладки
    x = 42
    y = 3.14
    name = "Python"
    print(f"{x=}, {y=}, {name=}")
    
    # math.prod() для произведения
    numbers = [1, 2, 3, 4, 5]
    product = math.prod(numbers)
    print(f"Произведение {numbers} = {product}")

# Python 3.9+ возможности
if sys.version_info >= (3, 9):
    print("\n=== Python 3.9+ возможности ===")
    
    # Операторы слияния словарей
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    dict3 = {"b": 20, "e": 5}
    
    # Слияние с |
    merged = dict1 | dict2 | dict3
    print(f"Слияние словарей: {merged}")
    
    # Обновление на месте с |=
    dict1 |= {"f": 6}
    print(f"Обновлённый dict1: {dict1}")
    
    # Новые методы строк
    text = "prefix_content_suffix"
    print(f"Удаление префикса: {text.removeprefix('prefix_')}")
    print(f"Удаление суффикса: {text.removesuffix('_suffix')}")
    
    # Новый синтаксис типов (встроенные коллекции)
    def process_items(items: list[str]) -> dict[str, int]:
        """Новый синтаксис вместо List[str] и Dict[str, int]"""
        return {item: len(item) for item in items}
    
    result = process_items(["hello", "world", "python"])
    print(f"Обработка элементов: {result}")
    
    # functools.cache (без ограничений)
    @cache
    def fibonacci_cached(n):
        if n < 2:
            return n
        return fibonacci_cached(n-1) + fibonacci_cached(n-2)
    
    print(f"Фибоначчи 30: {fibonacci_cached(30)}")

# Python 3.10+ возможности
if sys.version_info >= (3, 10):
    print("\n=== Python 3.10+ возможности ===")
    
    # Union types с | синтаксисом
    def process_value(value: int | str | float) -> str:
        """Новый синтаксис вместо Union[int, str, float]"""
        match value:
            case int():
                return f"Целое число: {value}"
            case str():
                return f"Строка: {value}"
            case float():
                return f"Дробное число: {value}"
    
    test_values = [42, "hello", 3.14]
    for val in test_values:
        print(process_value(val))
    
    # Улучшенные сообщения об ошибках
    def demo_error():
        try:
            data = {"users": [{"name": "John", "age": 30}]}
            # Намеренная ошибка для демонстрации
            result = data["users"][0]["salary"]  # KeyError
        except KeyError as e:
            print(f"Перехвачена ошибка: {e}")
            print("В Python 3.10+ сообщения об ошибках стали более подробными")
    
    demo_error()

# Python 3.11+ возможности  
if sys.version_info >= (3, 11):
    print("\n=== Python 3.11+ возможности ===")
    
    # Exception Groups (если поддерживается)
    try:
        # Пример Exception Groups
        print("Exception Groups доступны в Python 3.11+")
        
        # TOML support
        try:
            import tomllib
            print("TOML поддержка встроена")
        except ImportError:
            print("tomllib недоступен")
            
    except:
        print("Некоторые возможности 3.11 могут быть недоступны")

print("\n=== Универсальные улучшения ===")

# Улучшенные генераторы словарей и множеств
data = ["apple", "banana", "cherry", "apple", "banana"]
word_lengths = {word: len(word) for word in set(data)}
print(f"Длины уникальных слов: {word_lengths}")

# Множественное присваивание с *
first, *middle, last = [1, 2, 3, 4, 5, 6]
print(f"Первый: {first}, средние: {middle}, последний: {last}")

# Более мощные f-strings
precision = 2
value = 3.14159
print(f"Значение с {precision} знаками: {value:.{precision}f}")

# Аннотации переменных
name: str = "Python"
version: tuple[int, int, int] = (3, 11, 0)
features: list[str] = ["match/case", "walrus operator", "positional-only"]

print(f"Язык: {name}")
print(f"Версия: {'.'.join(map(str, version))}")
print(f"Возможности: {', '.join(features)}")

# Контекстные менеджеры с несколькими ресурсами
class DemoResource:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        print(f"Открытие ресурса: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Закрытие ресурса: {self.name}")

# Множественные контекстные менеджеры
with DemoResource("файл1"), DemoResource("файл2"):
    print("Работа с ресурсами")

print("\n=== Рекомендации по использованию ===")
print("1. Используйте новый синтаксис типов: list[int] вместо List[int]")
print("2. Применяйте walrus operator для упрощения кода")
print("3. Используйте match/case для сложной логики ветвления")
print("4. Применяйте операторы слияния словарей | и |=")
print("5. Используйте positional-only параметры для API")
print("6. Применяйте f-strings с = для отладки")
print("7. Используйте @cache вместо @lru_cache() без параметров")

# Демонстрация производительности (Python 3.11+)
if sys.version_info >= (3, 11):
    import time
    
    def performance_demo():
        start = time.perf_counter()
        
        # Простая операция
        result = sum(i ** 2 for i in range(100000))
        
        end = time.perf_counter()
        print(f"\nВремя выполнения: {end - start:.4f} сек")
        print("Python 3.11+ имеет значительные улучшения производительности")
        return result
    
    performance_demo()

print("\n=== Совместимость версий ===")
print("Используйте проверки версий для обратной совместимости:")
print("if sys.version_info >= (3, 10):")
print("    # Код для Python 3.10+")
print("else:")
print("    # Альтернативный код для старых версий") 