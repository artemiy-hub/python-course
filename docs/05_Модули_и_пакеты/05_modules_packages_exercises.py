#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Модули и пакеты Python

Этот файл содержит практические упражнения для закрепления знаний:
- Создание и импорт модулей
- Работа с пакетами и подпакетами
- Механизм поиска модулей
- Различные способы импорта
- Управление зависимостями
- Создание собственных пакетов

Каждое упражнение имеет описание задачи и закомментированное решение.
"""

import sys
import os
import importlib
import types
from pathlib import Path


def exercise_01():
    """
    Упражнение 1: Математическая библиотека
    
    Создайте модуль математических операций, который включает:
    1. Константы (PI, E, GOLDEN_RATIO)
    2. Функции для геометрических вычислений (площадь, периметр различных фигур)
    3. Класс Calculator с методами для базовых операций
    4. Функцию для генерации последовательности Фибоначчи
    5. Проверку __name__ == "__main__" с демонстрацией всех функций
    6. Контроль экспорта через __all__
    """
    print("=== Упражнение 1: Математическая библиотека ===")
    
    # TODO: Напишите ваш код здесь
    # Создайте модуль math_library.py в памяти или как строку
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # math_library_code = '''
    # """
    # Математическая библиотека для различных вычислений
    # """
    # 
    # import math
    # 
    # # Константы
    # PI = 3.14159265359
    # E = 2.71828182846
    # GOLDEN_RATIO = 1.61803398875
    # 
    # # Геометрические функции
    # def circle_area(radius):
    #     """Вычисляет площадь круга"""
    #     return PI * radius ** 2
    # 
    # def circle_perimeter(radius):
    #     """Вычисляет периметр круга"""
    #     return 2 * PI * radius
    # 
    # def rectangle_area(width, height):
    #     """Вычисляет площадь прямоугольника"""
    #     return width * height
    # 
    # def rectangle_perimeter(width, height):
    #     """Вычисляет периметр прямоугольника"""
    #     return 2 * (width + height)
    # 
    # def triangle_area(base, height):
    #     """Вычисляет площадь треугольника"""
    #     return 0.5 * base * height
    # 
    # # Класс калькулятора
    # class Calculator:
    #     """Калькулятор для базовых операций"""
    #     
    #     @staticmethod
    #     def add(a, b):
    #         return a + b
    #     
    #     @staticmethod
    #     def subtract(a, b):
    #         return a - b
    #     
    #     @staticmethod
    #     def multiply(a, b):
    #         return a * b
    #     
    #     @staticmethod
    #     def divide(a, b):
    #         if b == 0:
    #             raise ValueError("Деление на ноль невозможно")
    #         return a / b
    #     
    #     @staticmethod
    #     def power(base, exponent):
    #         return base ** exponent
    #     
    #     @staticmethod
    #     def factorial(n):
    #         if n < 0:
    #             raise ValueError("Факториал от отрицательного числа не определен")
    #         if n <= 1:
    #             return 1
    #         return n * Calculator.factorial(n - 1)
    # 
    # # Последовательность Фибоначчи
    # def fibonacci_sequence(n):
    #     """Генерирует последовательность Фибоначчи до n элементов"""
    #     if n <= 0:
    #         return []
    #     elif n == 1:
    #         return [0]
    #     elif n == 2:
    #         return [0, 1]
    #     
    #     sequence = [0, 1]
    #     for i in range(2, n):
    #         sequence.append(sequence[i-1] + sequence[i-2])
    #     
    #     return sequence
    # 
    # def fibonacci_nth(n):
    #     """Возвращает n-й элемент последовательности Фибоначчи"""
    #     if n <= 0:
    #         raise ValueError("n должно быть положительным числом")
    #     elif n == 1:
    #         return 0
    #     elif n == 2:
    #         return 1
    #     
    #     a, b = 0, 1
    #     for _ in range(2, n):
    #         a, b = b, a + b
    #     
    #     return b
    # 
    # # Контроль экспорта
    # __all__ = [
    #     'PI', 'E', 'GOLDEN_RATIO',
    #     'circle_area', 'circle_perimeter',
    #     'rectangle_area', 'rectangle_perimeter', 
    #     'triangle_area',
    #     'Calculator',
    #     'fibonacci_sequence', 'fibonacci_nth'
    # ]
    # 
    # # Демонстрация при запуске как скрипт
    # if __name__ == "__main__":
    #     print("=== Демонстрация математической библиотеки ===")
    #     
    #     print(f"Константы: PI={PI}, E={E}, Золотое сечение={GOLDEN_RATIO}")
    #     
    #     print("\n--- Геометрические вычисления ---")
    #     radius = 5
    #     print(f"Круг (r={radius}): площадь={circle_area(radius):.2f}, периметр={circle_perimeter(radius):.2f}")
    #     
    #     width, height = 4, 6
    #     print(f"Прямоугольник ({width}x{height}): площадь={rectangle_area(width, height)}, периметр={rectangle_perimeter(width, height)}")
    #     
    #     base, h = 8, 3
    #     print(f"Треугольник (основание={base}, высота={h}): площадь={triangle_area(base, h)}")
    #     
    #     print("\n--- Калькулятор ---")
    #     calc = Calculator()
    #     print(f"10 + 5 = {calc.add(10, 5)}")
    #     print(f"10 - 5 = {calc.subtract(10, 5)}")
    #     print(f"10 * 5 = {calc.multiply(10, 5)}")
    #     print(f"10 / 5 = {calc.divide(10, 5)}")
    #     print(f"2^8 = {calc.power(2, 8)}")
    #     print(f"5! = {calc.factorial(5)}")
    #     
    #     print("\n--- Последовательность Фибоначчи ---")
    #     fib_seq = fibonacci_sequence(10)
    #     print(f"Первые 10 чисел Фибоначчи: {fib_seq}")
    #     print(f"15-й элемент Фибоначчи: {fibonacci_nth(15)}")
    # '''
    # 
    # # Создание модуля
    # math_library = types.ModuleType("math_library")
    # math_library.__file__ = "<dynamic:math_library>"
    # exec(math_library_code, math_library.__dict__)
    # sys.modules["math_library"] = math_library
    # 
    # # Тестирование модуля
    # print("Модуль создан и загружен!")
    # print(f"Константы: PI={math_library.PI}, E={math_library.E}")
    # 
    # # Импорт конкретных объектов
    # from math_library import Calculator, circle_area, fibonacci_nth
    # 
    # calc = Calculator()
    # print(f"Тест калькулятора: 15 + 25 = {calc.add(15, 25)}")
    # print(f"Площадь круга (r=10): {circle_area(10):.2f}")
    # print(f"10-й элемент Фибоначчи: {fibonacci_nth(10)}")
    # 
    # print(f"Экспортируемые объекты: {math_library.__all__}")


def exercise_02():
    """
    Упражнение 2: Система конфигурации
    
    Создайте пакет для управления конфигурацией приложения:
    1. Главный пакет 'config_system'
    2. Модуль 'loaders' - загрузка из JSON, YAML, ENV
    3. Модуль 'validators' - валидация конфигурации
    4. Модуль 'cache' - кеширование конфигурации
    5. Подпакет 'formats' с модулями для разных форматов
    6. Используйте относительные импорты
    7. Реализуйте паттерн Singleton для конфигурации
    """
    print("=== Упражнение 2: Система конфигурации ===")
    
    # TODO: Напишите ваш код здесь
    # Создайте структуру пакета с подпакетами и модулями
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # def create_config_system():
    #     """Создает пакет системы конфигурации"""
    #     
    #     # Главный пакет
    #     main_pkg = types.ModuleType("config_system")
    #     main_pkg.__file__ = "<dynamic:config_system>"
    #     main_pkg.__path__ = ["<dynamic:config_system>"]
    #     main_pkg.__package__ = "config_system"
    #     
    #     main_init = '''
    # """
    # Система управления конфигурацией
    # """
    # 
    # __version__ = "1.0.0"
    # 
    # from .manager import ConfigManager
    # from .loaders import JSONLoader, YAMLLoader, EnvLoader
    # from .validators import ConfigValidator
    # from .cache import ConfigCache
    # 
    # __all__ = [
    #     'ConfigManager',
    #     'JSONLoader', 'YAMLLoader', 'EnvLoader',
    #     'ConfigValidator',
    #     'ConfigCache'
    # ]
    # 
    # # Создаем глобальный экземпляр менеджера
    # config = ConfigManager()
    # '''
    #     exec(main_init, main_pkg.__dict__)
    #     sys.modules["config_system"] = main_pkg
    #     
    #     # Модуль manager
    #     manager_module = types.ModuleType("config_system.manager")
    #     manager_module.__file__ = "<dynamic:config_system.manager>"
    #     manager_module.__package__ = "config_system"
    #     
    #     manager_code = '''
    # """Менеджер конфигурации"""
    # 
    # from .loaders import JSONLoader, EnvLoader
    # from .validators import ConfigValidator
    # from .cache import ConfigCache
    # 
    # class ConfigManager:
    #     """Менеджер конфигурации (Singleton)"""
    #     
    #     _instance = None
    #     _config_data = {}
    #     
    #     def __new__(cls):
    #         if cls._instance is None:
    #             cls._instance = super().__new__(cls)
    #             cls._instance._initialized = False
    #         return cls._instance
    #     
    #     def __init__(self):
    #         if not self._initialized:
    #             self.loaders = {
    #                 'json': JSONLoader(),
    #                 'env': EnvLoader()
    #             }
    #             self.validator = ConfigValidator()
    #             self.cache = ConfigCache()
    #             self._initialized = True
    #     
    #     def load_config(self, source, loader_type='json'):
    #         """Загружает конфигурацию"""
    #         if loader_type not in self.loaders:
    #             raise ValueError(f"Неподдерживаемый тип загрузчика: {loader_type}")
    #         
    #         config_data = self.loaders[loader_type].load(source)
    #         
    #         if self.validator.validate(config_data):
    #             self._config_data.update(config_data)
    #             self.cache.store(config_data)
    #             return True
    #         return False
    #     
    #     def get(self, key, default=None):
    #         """Получает значение конфигурации"""
    #         return self._config_data.get(key, default)
    #     
    #     def set(self, key, value):
    #         """Устанавливает значение конфигурации"""
    #         self._config_data[key] = value
    #         self.cache.invalidate()
    #     
    #     def get_all(self):
    #         """Возвращает всю конфигурацию"""
    #         return self._config_data.copy()
    # '''
    #     exec(manager_code, manager_module.__dict__)
    #     sys.modules["config_system.manager"] = manager_module
    #     
    #     # Модуль loaders
    #     loaders_module = types.ModuleType("config_system.loaders")
    #     loaders_module.__file__ = "<dynamic:config_system.loaders>"
    #     loaders_module.__package__ = "config_system"
    #     
    #     loaders_code = '''
    # """Загрузчики конфигурации"""
    # 
    # import json
    # import os
    # 
    # class BaseLoader:
    #     """Базовый класс загрузчика"""
    #     
    #     def load(self, source):
    #         """Загружает конфигурацию из источника"""
    #         raise NotImplementedError
    # 
    # class JSONLoader(BaseLoader):
    #     """Загрузчик JSON конфигурации"""
    #     
    #     def load(self, source):
    #         """Загружает из JSON строки или файла"""
    #         if os.path.isfile(source):
    #             with open(source, 'r', encoding='utf-8') as f:
    #                 return json.load(f)
    #         else:
    #             return json.loads(source)
    # 
    # class YAMLLoader(BaseLoader):
    #     """Загрузчик YAML конфигурации"""
    #     
    #     def load(self, source):
    #         """Загружает из YAML (имитация)"""
    #         # В реальной реализации здесь был бы import yaml
    #         print("YAML загрузчик (требует библиотеку PyYAML)")
    #         return {"yaml_loaded": True, "source": source}
    # 
    # class EnvLoader(BaseLoader):
    #     """Загрузчик переменных окружения"""
    #     
    #     def load(self, prefix="APP_"):
    #         """Загружает переменные окружения с префиксом"""
    #         config = {}
    #         for key, value in os.environ.items():
    #             if key.startswith(prefix):
    #                 config_key = key[len(prefix):].lower()
    #                 config[config_key] = value
    #         return config
    # '''
    #     exec(loaders_code, loaders_module.__dict__)
    #     sys.modules["config_system.loaders"] = loaders_module
    #     
    #     # Модуль validators
    #     validators_module = types.ModuleType("config_system.validators")
    #     validators_module.__file__ = "<dynamic:config_system.validators>"
    #     validators_module.__package__ = "config_system"
    #     
    #     validators_code = '''
    # """Валидаторы конфигурации"""
    # 
    # class ConfigValidator:
    #     """Валидатор конфигурации"""
    #     
    #     def __init__(self):
    #         self.required_keys = []
    #         self.rules = {}
    #     
    #     def add_required_key(self, key):
    #         """Добавляет обязательный ключ"""
    #         self.required_keys.append(key)
    #     
    #     def add_rule(self, key, validator_func):
    #         """Добавляет правило валидации для ключа"""
    #         self.rules[key] = validator_func
    #     
    #     def validate(self, config_data):
    #         """Валидирует конфигурацию"""
    #         if not isinstance(config_data, dict):
    #             print("Конфигурация должна быть словарем")
    #             return False
    #         
    #         # Проверка обязательных ключей
    #         for key in self.required_keys:
    #             if key not in config_data:
    #                 print(f"Отсутствует обязательный ключ: {key}")
    #                 return False
    #         
    #         # Проверка правил
    #         for key, rule in self.rules.items():
    #             if key in config_data:
    #                 if not rule(config_data[key]):
    #                     print(f"Валидация не прошла для ключа: {key}")
    #                     return False
    #         
    #         return True
    # 
    # # Предопределенные валидаторы
    # def is_string(value):
    #     return isinstance(value, str)
    # 
    # def is_positive_int(value):
    #     return isinstance(value, int) and value > 0
    # 
    # def is_valid_url(value):
    #     return isinstance(value, str) and (value.startswith('http://') or value.startswith('https://'))
    # '''
    #     exec(validators_code, validators_module.__dict__)
    #     sys.modules["config_system.validators"] = validators_module
    #     
    #     # Модуль cache
    #     cache_module = types.ModuleType("config_system.cache")
    #     cache_module.__file__ = "<dynamic:config_system.cache>"
    #     cache_module.__package__ = "config_system"
    #     
    #     cache_code = '''
    # """Кеш конфигурации"""
    # 
    # import time
    # 
    # class ConfigCache:
    #     """Кеш для конфигурации"""
    #     
    #     def __init__(self, ttl=300):  # TTL 5 минут
    #         self.ttl = ttl
    #         self._cache = {}
    #         self._timestamps = {}
    #     
    #     def store(self, config_data):
    #         """Сохраняет конфигурацию в кеш"""
    #         timestamp = time.time()
    #         for key, value in config_data.items():
    #             self._cache[key] = value
    #             self._timestamps[key] = timestamp
    #     
    #     def get(self, key):
    #         """Получает значение из кеша"""
    #         if key not in self._cache:
    #             return None
    #         
    #         # Проверяем TTL
    #         if time.time() - self._timestamps[key] > self.ttl:
    #             del self._cache[key]
    #             del self._timestamps[key]
    #             return None
    #         
    #         return self._cache[key]
    #     
    #     def invalidate(self, key=None):
    #         """Очищает кеш"""
    #         if key:
    #             self._cache.pop(key, None)
    #             self._timestamps.pop(key, None)
    #         else:
    #             self._cache.clear()
    #             self._timestamps.clear()
    #     
    #     def is_valid(self, key):
    #         """Проверяет, действителен ли кеш для ключа"""
    #         if key not in self._timestamps:
    #             return False
    #         return time.time() - self._timestamps[key] <= self.ttl
    # '''
    #     exec(cache_code, cache_module.__dict__)
    #     sys.modules["config_system.cache"] = cache_module
    #     
    #     return main_pkg
    # 
    # # Создаем пакет
    # config_pkg = create_config_system()
    # 
    # print("Пакет системы конфигурации создан!")
    # 
    # # Тестирование системы
    # from config_system import ConfigManager, ConfigValidator
    # from config_system.validators import is_string, is_positive_int
    # 
    # # Создаем менеджер конфигурации
    # config_manager = ConfigManager()
    # 
    # # Настраиваем валидатор
    # config_manager.validator.add_required_key("app_name")
    # config_manager.validator.add_rule("app_name", is_string)
    # config_manager.validator.add_rule("port", is_positive_int)
    # 
    # # Загружаем конфигурацию из JSON
    # json_config = '{"app_name": "MyApp", "port": 8080, "debug": true}'
    # success = config_manager.load_config(json_config, 'json')
    # print(f"Конфигурация загружена: {success}")
    # 
    # # Получаем значения
    # print(f"Имя приложения: {config_manager.get('app_name')}")
    # print(f"Порт: {config_manager.get('port')}")
    # print(f"Режим отладки: {config_manager.get('debug')}")
    # 
    # # Проверяем Singleton
    # another_manager = ConfigManager()
    # print(f"Singleton работает: {config_manager is another_manager}")
    # print(f"Конфигурация сохранена: {another_manager.get('app_name')}")


def exercise_03():
    """
    Упражнение 3: Система плагинов
    
    Создайте систему динамической загрузки плагинов:
    1. Базовый класс Plugin с интерфейсом
    2. PluginManager для загрузки и управления плагинами
    3. Несколько примеров плагинов (TextProcessor, DataConverter)
    4. Динамическая загрузка плагинов из строк
    5. Система приоритетов и зависимостей плагинов
    6. Автоматическое обнаружение плагинов
    """
    print("=== Упражнение 3: Система плагинов ===")
    
    # TODO: Напишите ваш код здесь
    # Создайте систему плагинов с динамической загрузкой
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # # Базовый класс плагина
    # class Plugin:
    #     """Базовый класс для всех плагинов"""
    #     
    #     name = "BasePlugin"
    #     version = "1.0.0"
    #     priority = 0
    #     dependencies = []
    #     
    #     def __init__(self):
    #         self.enabled = True
    #     
    #     def initialize(self):
    #         """Инициализация плагина"""
    #         pass
    #     
    #     def execute(self, data):
    #         """Выполнение основной функции плагина"""
    #         raise NotImplementedError("Метод execute должен быть реализован")
    #     
    #     def cleanup(self):
    #         """Очистка ресурсов плагина"""
    #         pass
    #     
    #     def get_info(self):
    #         """Информация о плагине"""
    #         return {
    #             "name": self.name,
    #             "version": self.version,
    #             "priority": self.priority,
    #             "dependencies": self.dependencies,
    #             "enabled": self.enabled
    #         }
    # 
    # # Менеджер плагинов
    # class PluginManager:
    #     """Менеджер для загрузки и управления плагинами"""
    #     
    #     def __init__(self):
    #         self.plugins = {}
    #         self.loaded_plugins = []
    #     
    #     def register_plugin(self, plugin_class):
    #         """Регистрирует класс плагина"""
    #         if not issubclass(plugin_class, Plugin):
    #             raise ValueError("Плагин должен наследоваться от класса Plugin")
    #         
    #         plugin_instance = plugin_class()
    #         self.plugins[plugin_instance.name] = plugin_instance
    #         print(f"Плагин '{plugin_instance.name}' зарегистрирован")
    #     
    #     def load_plugin_from_code(self, name, code):
    #         """Загружает плагин из строки с кодом"""
    #         try:
    #             # Создаем модуль для плагина
    #             plugin_module = types.ModuleType(f"plugin_{name}")
    #             plugin_module.__file__ = f"<dynamic:plugin_{name}>"
    #             
    #             # Добавляем базовый класс в пространство имен модуля
    #             plugin_module.Plugin = Plugin
    #             
    #             # Выполняем код плагина
    #             exec(code, plugin_module.__dict__)
    #             
    #             # Ищем класс плагина в модуле
    #             plugin_class = None
    #             for attr_name in dir(plugin_module):
    #                 attr = getattr(plugin_module, attr_name)
    #                 if (isinstance(attr, type) and 
    #                     issubclass(attr, Plugin) and 
    #                     attr != Plugin):
    #                     plugin_class = attr
    #                     break
    #             
    #             if plugin_class:
    #                 self.register_plugin(plugin_class)
    #                 return True
    #             else:
    #                 print(f"Не найден класс плагина в коде для '{name}'")
    #                 return False
    #                 
    #         except Exception as e:
    #             print(f"Ошибка загрузки плагина '{name}': {e}")
    #             return False
    #     
    #     def load_plugins(self):
    #         """Загружает все зарегистрированные плагины с учетом зависимостей"""
    #         # Сортируем плагины по приоритету
    #         sorted_plugins = sorted(
    #             self.plugins.values(), 
    #             key=lambda p: p.priority, 
    #             reverse=True
    #         )
    #         
    #         loaded_names = set()
    #         
    #         def load_plugin_recursive(plugin):
    #             """Рекурсивно загружает плагин с зависимостями"""
    #             if plugin.name in loaded_names:
    #                 return True
    #             
    #             # Загружаем зависимости
    #             for dep_name in plugin.dependencies:
    #                 if dep_name not in self.plugins:
    #                     print(f"Зависимость '{dep_name}' не найдена для плагина '{plugin.name}'")
    #                     return False
    #                 
    #                 if not load_plugin_recursive(self.plugins[dep_name]):
    #                     return False
    #             
    #             # Инициализируем плагин
    #             try:
    #                 plugin.initialize()
    #                 self.loaded_plugins.append(plugin)
    #                 loaded_names.add(plugin.name)
    #                 print(f"Плагин '{plugin.name}' загружен")
    #                 return True
    #             except Exception as e:
    #                 print(f"Ошибка инициализации плагина '{plugin.name}': {e}")
    #                 return False
    #         
    #         # Загружаем все плагины
    #         for plugin in sorted_plugins:
    #             if plugin.enabled:
    #                 load_plugin_recursive(plugin)
    #     
    #     def execute_plugins(self, data):
    #         """Выполняет все загруженные плагины"""
    #         results = {}
    #         for plugin in self.loaded_plugins:
    #             if plugin.enabled:
    #                 try:
    #                     result = plugin.execute(data)
    #                     results[plugin.name] = result
    #                 except Exception as e:
    #                     print(f"Ошибка выполнения плагина '{plugin.name}': {e}")
    #                     results[plugin.name] = None
    #         return results
    #     
    #     def get_plugin_info(self):
    #         """Возвращает информацию о всех плагинах"""
    #         return {name: plugin.get_info() for name, plugin in self.plugins.items()}
    #     
    #     def unload_plugins(self):
    #         """Выгружает все плагины"""
    #         for plugin in reversed(self.loaded_plugins):
    #             try:
    #                 plugin.cleanup()
    #                 print(f"Плагин '{plugin.name}' выгружен")
    #             except Exception as e:
    #                 print(f"Ошибка выгрузки плагина '{plugin.name}': {e}")
    #         self.loaded_plugins.clear()
    # 
    # # Создаем менеджер плагинов
    # plugin_manager = PluginManager()
    # 
    # # Код плагина обработки текста
    # text_processor_code = '''
    # class TextProcessorPlugin(Plugin):
    #     """Плагин для обработки текста"""
    #     
    #     name = "TextProcessor"
    #     version = "1.0.0"
    #     priority = 10
    #     dependencies = []
    #     
    #     def initialize(self):
    #         print("TextProcessor инициализирован")
    #     
    #     def execute(self, data):
    #         if isinstance(data, str):
    #             # Обрабатываем текст: удаляем лишние пробелы, приводим к нижнему регистру
    #             processed = " ".join(data.strip().lower().split())
    #             return f"Обработанный текст: {processed}"
    #         return "Данные не являются текстом"
    #     
    #     def cleanup(self):
    #         print("TextProcessor очищен")
    # '''
    # 
    # # Код плагина конвертера данных
    # data_converter_code = '''
    # class DataConverterPlugin(Plugin):
    #     """Плагин для конвертации данных"""
    #     
    #     name = "DataConverter"
    #     version = "1.0.0"
    #     priority = 5
    #     dependencies = ["TextProcessor"]
    #     
    #     def initialize(self):
    #         print("DataConverter инициализирован")
    #     
    #     def execute(self, data):
    #         if isinstance(data, str):
    #             # Пытаемся конвертировать в разные типы
    #             conversions = {}
    #             
    #             # В число
    #             try:
    #                 if '.' in data:
    #                     conversions['float'] = float(data)
    #                 else:
    #                     conversions['int'] = int(data)
    #             except ValueError:
    #                 pass
    #             
    #             # В список (разделение по запятым)
    #             if ',' in data:
    #                 conversions['list'] = [item.strip() for item in data.split(',')]
    #             
    #             # В булево значение
    #             if data.lower() in ['true', 'false', 'yes', 'no']:
    #                 conversions['bool'] = data.lower() in ['true', 'yes']
    #             
    #             return f"Возможные конвертации: {conversions}"
    #         
    #         return f"Тип данных: {type(data).__name__}"
    #     
    #     def cleanup(self):
    #         print("DataConverter очищен")
    # '''
    # 
    # # Код плагина валидатора
    # validator_code = '''
    # class ValidatorPlugin(Plugin):
    #     """Плагин для валидации данных"""
    #     
    #     name = "Validator"
    #     version = "1.0.0"
    #     priority = 15
    #     dependencies = []
    #     
    #     def initialize(self):
    #         print("Validator инициализирован")
    #     
    #     def execute(self, data):
    #         validations = {
    #             'not_empty': bool(data),
    #             'is_string': isinstance(data, str),
    #             'length': len(str(data)),
    #             'has_digits': any(c.isdigit() for c in str(data)),
    #             'has_alpha': any(c.isalpha() for c in str(data))
    #         }
    #         
    #         return f"Результаты валидации: {validations}"
    #     
    #     def cleanup(self):
    #         print("Validator очищен")
    # '''
    # 
    # # Загружаем плагины
    # print("Загрузка плагинов...")
    # plugin_manager.load_plugin_from_code("TextProcessor", text_processor_code)
    # plugin_manager.load_plugin_from_code("DataConverter", data_converter_code)
    # plugin_manager.load_plugin_from_code("Validator", validator_code)
    # 
    # # Информация о плагинах
    # print("\nИнформация о плагинах:")
    # for name, info in plugin_manager.get_plugin_info().items():
    #     print(f"  {name}: приоритет={info['priority']}, зависимости={info['dependencies']}")
    # 
    # # Загружаем плагины с учетом зависимостей
    # print("\nЗагрузка плагинов с зависимостями...")
    # plugin_manager.load_plugins()
    # 
    # # Тестируем плагины
    # print("\nТестирование плагинов...")
    # test_data = "  Hello, World! 123  "
    # results = plugin_manager.execute_plugins(test_data)
    # 
    # for plugin_name, result in results.items():
    #     print(f"\n{plugin_name}: {result}")
    # 
    # # Выгружаем плагины
    # print("\nВыгрузка плагинов...")
    # plugin_manager.unload_plugins()


def exercise_04():
    """
    Упражнение 4: Модульная система логирования
    
    Создайте модульную систему логирования:
    1. Базовый модуль 'logging_system' с интерфейсами
    2. Различные обработчики (ConsoleHandler, FileHandler, NetworkHandler)
    3. Форматтеры сообщений (SimpleFormatter, JSONFormatter, XMLFormatter)
    4. Фильтры логов (LevelFilter, RegexFilter, TimeFilter)
    5. Конфигурацию через JSON/YAML
    6. Ротацию логов и архивирование
    """
    print("=== Упражнение 4: Модульная система логирования ===")
    
    # TODO: Напишите ваш код здесь
    # Создайте систему логирования с модульной архитектурой
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # import json
    # import time
    # import re
    # from datetime import datetime
    # from enum import Enum
    # 
    # # Уровни логирования
    # class LogLevel(Enum):
    #     DEBUG = 10
    #     INFO = 20
    #     WARNING = 30
    #     ERROR = 40
    #     CRITICAL = 50
    # 
    # # Запись лога
    # class LogRecord:
    #     """Запись лога"""
    #     
    #     def __init__(self, level, message, logger_name="root", **kwargs):
    #         self.level = level
    #         self.message = message
    #         self.logger_name = logger_name
    #         self.timestamp = datetime.now()
    #         self.extra = kwargs
    #     
    #     def to_dict(self):
    #         return {
    #             'timestamp': self.timestamp.isoformat(),
    #             'level': self.level.name,
    #             'logger': self.logger_name,
    #             'message': self.message,
    #             'extra': self.extra
    #         }
    # 
    # # Базовые классы
    # class BaseHandler:
    #     """Базовый обработчик логов"""
    #     
    #     def __init__(self, level=LogLevel.INFO):
    #         self.level = level
    #         self.formatter = None
    #         self.filters = []
    #     
    #     def set_formatter(self, formatter):
    #         self.formatter = formatter
    #     
    #     def add_filter(self, filter_obj):
    #         self.filters.append(filter_obj)
    #     
    #     def can_handle(self, record):
    #         """Проверяет, может ли обработчик обработать запись"""
    #         if record.level.value < self.level.value:
    #             return False
    #         
    #         for filter_obj in self.filters:
    #             if not filter_obj.filter(record):
    #                 return False
    #         
    #         return True
    #     
    #     def handle(self, record):
    #         """Обрабатывает запись лога"""
    #         if self.can_handle(record):
    #             formatted_message = self.format(record)
    #             self.emit(formatted_message, record)
    #     
    #     def format(self, record):
    #         """Форматирует запись"""
    #         if self.formatter:
    #             return self.formatter.format(record)
    #         return f"{record.timestamp} - {record.level.name} - {record.message}"
    #     
    #     def emit(self, formatted_message, record):
    #         """Выводит отформатированное сообщение"""
    #         raise NotImplementedError
    # 
    # class BaseFormatter:
    #     """Базовый форматтер"""
    #     
    #     def format(self, record):
    #         raise NotImplementedError
    # 
    # class BaseFilter:
    #     """Базовый фильтр"""
    #     
    #     def filter(self, record):
    #         return True
    # 
    # # Обработчики
    # class ConsoleHandler(BaseHandler):
    #     """Обработчик вывода в консоль"""
    #     
    #     def emit(self, formatted_message, record):
    #         print(formatted_message)
    # 
    # class FileHandler(BaseHandler):
    #     """Обработчик записи в файл"""
    #     
    #     def __init__(self, filename, level=LogLevel.INFO):
    #         super().__init__(level)
    #         self.filename = filename
    #         self.file_handle = None
    #     
    #     def emit(self, formatted_message, record):
    #         # В реальной реализации здесь была бы запись в файл
    #         print(f"[FILE:{self.filename}] {formatted_message}")
    # 
    # class NetworkHandler(BaseHandler):
    #     """Обработчик отправки по сети"""
    #     
    #     def __init__(self, host, port, level=LogLevel.WARNING):
    #         super().__init__(level)
    #         self.host = host
    #         self.port = port
    #     
    #     def emit(self, formatted_message, record):
    #         # В реальной реализации здесь была бы отправка по сети
    #         print(f"[NETWORK:{self.host}:{self.port}] {formatted_message}")
    # 
    # # Форматтеры
    # class SimpleFormatter(BaseFormatter):
    #     """Простой форматтер"""
    #     
    #     def __init__(self, format_string="{timestamp} - {level} - {logger} - {message}"):
    #         self.format_string = format_string
    #     
    #     def format(self, record):
    #         return self.format_string.format(
    #             timestamp=record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
    #             level=record.level.name,
    #             logger=record.logger_name,
    #             message=record.message
    #         )
    # 
    # class JSONFormatter(BaseFormatter):
    #     """JSON форматтер"""
    #     
    #     def format(self, record):
    #         return json.dumps(record.to_dict(), ensure_ascii=False)
    # 
    # class XMLFormatter(BaseFormatter):
    #     """XML форматтер"""
    #     
    #     def format(self, record):
    #         data = record.to_dict()
    #         xml = f"<log>"
    #         for key, value in data.items():
    #             if key == 'extra' and isinstance(value, dict):
    #                 xml += f"<{key}>"
    #                 for k, v in value.items():
    #                     xml += f"<{k}>{v}</{k}>"
    #                 xml += f"</{key}>"
    #             else:
    #                 xml += f"<{key}>{value}</{key}>"
    #         xml += "</log>"
    #         return xml
    # 
    # # Фильтры
    # class LevelFilter(BaseFilter):
    #     """Фильтр по уровню"""
    #     
    #     def __init__(self, min_level, max_level=None):
    #         self.min_level = min_level
    #         self.max_level = max_level or LogLevel.CRITICAL
    #     
    #     def filter(self, record):
    #         return self.min_level.value <= record.level.value <= self.max_level.value
    # 
    # class RegexFilter(BaseFilter):
    #     """Фильтр по регулярному выражению"""
    #     
    #     def __init__(self, pattern):
    #         self.pattern = re.compile(pattern)
    #     
    #     def filter(self, record):
    #         return self.pattern.search(record.message) is not None
    # 
    # class TimeFilter(BaseFilter):
    #     """Фильтр по времени"""
    #     
    #     def __init__(self, start_hour=0, end_hour=23):
    #         self.start_hour = start_hour
    #         self.end_hour = end_hour
    #     
    #     def filter(self, record):
    #         hour = record.timestamp.hour
    #         return self.start_hour <= hour <= self.end_hour
    # 
    # # Логгер
    # class Logger:
    #     """Основной логгер"""
    #     
    #     def __init__(self, name="root", level=LogLevel.INFO):
    #         self.name = name
    #         self.level = level
    #         self.handlers = []
    #         self.parent = None
    #     
    #     def add_handler(self, handler):
    #         self.handlers.append(handler)
    #     
    #     def remove_handler(self, handler):
    #         if handler in self.handlers:
    #             self.handlers.remove(handler)
    #     
    #     def log(self, level, message, **kwargs):
    #         if level.value >= self.level.value:
    #             record = LogRecord(level, message, self.name, **kwargs)
    #             for handler in self.handlers:
    #                 handler.handle(record)
    #     
    #     def debug(self, message, **kwargs):
    #         self.log(LogLevel.DEBUG, message, **kwargs)
    #     
    #     def info(self, message, **kwargs):
    #         self.log(LogLevel.INFO, message, **kwargs)
    #     
    #     def warning(self, message, **kwargs):
    #         self.log(LogLevel.WARNING, message, **kwargs)
    #     
    #     def error(self, message, **kwargs):
    #         self.log(LogLevel.ERROR, message, **kwargs)
    #     
    #     def critical(self, message, **kwargs):
    #         self.log(LogLevel.CRITICAL, message, **kwargs)
    # 
    # # Создаем систему логирования
    # print("Создание системы логирования...")
    # 
    # # Создаем логгер
    # logger = Logger("MyApp", LogLevel.DEBUG)
    # 
    # # Создаем обработчики
    # console_handler = ConsoleHandler(LogLevel.INFO)
    # file_handler = FileHandler("app.log", LogLevel.DEBUG)
    # network_handler = NetworkHandler("localhost", 9999, LogLevel.ERROR)
    # 
    # # Создаем форматтеры
    # simple_formatter = SimpleFormatter()
    # json_formatter = JSONFormatter()
    # xml_formatter = XMLFormatter()
    # 
    # # Создаем фильтры
    # error_filter = LevelFilter(LogLevel.ERROR)
    # regex_filter = RegexFilter(r"важно|critical|error")
    # work_hours_filter = TimeFilter(9, 18)
    # 
    # # Настраиваем обработчики
    # console_handler.set_formatter(simple_formatter)
    # file_handler.set_formatter(json_formatter)
    # network_handler.set_formatter(xml_formatter)
    # network_handler.add_filter(error_filter)
    # 
    # # Добавляем обработчики к логгеру
    # logger.add_handler(console_handler)
    # logger.add_handler(file_handler)
    # logger.add_handler(network_handler)
    # 
    # # Тестируем систему логирования
    # print("\nТестирование системы логирования:")
    # 
    # logger.debug("Отладочное сообщение", user_id=123)
    # logger.info("Информационное сообщение", action="login")
    # logger.warning("Предупреждение: высокая загрузка CPU", cpu_usage=85)
    # logger.error("Ошибка подключения к базе данных", db_host="localhost")
    # logger.critical("Критическая ошибка системы!", error_code=500)
    # 
    # print("\nСистема логирования работает корректно!")


def exercise_05():
    """
    Упражнение 5: Менеджер зависимостей
    
    Создайте простой менеджер зависимостей:
    1. Класс Dependency для описания зависимостей
    2. DependencyResolver для разрешения зависимостей
    3. PackageManager для управления пакетами
    4. Обнаружение циклических зависимостей
    5. Версионирование и совместимость
    6. Виртуальные окружения (имитация)
    """
    print("=== Упражнение 5: Менеджер зависимостей ===")
    
    # TODO: Напишите ваш код здесь
    # Создайте систему управления зависимостями
    
    # РЕШЕНИЕ (раскомментируйте после попытки):
    # from dataclasses import dataclass
    # from typing import List, Dict, Set, Optional
    # from packaging import version  # В реальности потребовалась бы библиотека packaging
    # 
    # # Используем простую версию без внешних зависимостей
    # class Version:
    #     """Простая реализация версионирования"""
    #     
    #     def __init__(self, version_str):
    #         self.version_str = version_str
    #         self.parts = [int(x) for x in version_str.split('.')]
    #     
    #     def __str__(self):
    #         return self.version_str
    #     
    #     def __eq__(self, other):
    #         return self.parts == other.parts
    #     
    #     def __lt__(self, other):
    #         return self.parts < other.parts
    #     
    #     def __le__(self, other):
    #         return self.parts <= other.parts
    #     
    #     def __gt__(self, other):
    #         return self.parts > other.parts
    #     
    #     def __ge__(self, other):
    #         return self.parts >= other.parts
    #     
    #     def satisfies(self, requirement):
    #         """Проверяет, удовлетворяет ли версия требованию"""
    #         op, req_version = requirement.split()
    #         req_ver = Version(req_version)
    #         
    #         if op == "==":
    #             return self == req_ver
    #         elif op == ">=":
    #             return self >= req_ver
    #         elif op == "<=":
    #             return self <= req_ver
    #         elif op == ">":
    #             return self > req_ver
    #         elif op == "<":
    #             return self < req_ver
    #         else:
    #             return False
    # 
    # @dataclass
    # class Dependency:
    #     """Описание зависимости"""
    #     name: str
    #     version_requirement: str = "*"
    #     optional: bool = False
    #     
    #     def __post_init__(self):
    #         if self.version_requirement == "*":
    #             self.version_requirement = ">= 0.0.0"
    #     
    #     def is_satisfied_by(self, package_version):
    #         """Проверяет, удовлетворяется ли зависимость версией пакета"""
    #         if self.version_requirement == "*":
    #             return True
    #         
    #         version_obj = Version(package_version)
    #         return version_obj.satisfies(self.version_requirement)
    # 
    # @dataclass
    # class Package:
    #     """Описание пакета"""
    #     name: str
    #     version: str
    #     dependencies: List[Dependency]
    #     description: str = ""
    #     
    #     def __post_init__(self):
    #         self.version_obj = Version(self.version)
    # 
    # class DependencyResolver:
    #     """Разрешение зависимостей"""
    #     
    #     def __init__(self):
    #         self.packages = {}  # name -> {version -> Package}
    #     
    #     def add_package(self, package):
    #         """Добавляет пакет в репозиторий"""
    #         if package.name not in self.packages:
    #             self.packages[package.name] = {}
    #         self.packages[package.name][package.version] = package
    #     
    #     def find_package(self, dependency):
    #         """Находит пакет, удовлетворяющий зависимости"""
    #         if dependency.name not in self.packages:
    #             return None
    #         
    #         # Ищем подходящую версию
    #         suitable_versions = []
    #         for version, package in self.packages[dependency.name].items():
    #             if dependency.is_satisfied_by(version):
    #                 suitable_versions.append((Version(version), package))
    #         
    #         if not suitable_versions:
    #             return None
    #         
    #         # Возвращаем самую новую подходящую версию
    #         suitable_versions.sort(key=lambda x: x[0], reverse=True)
    #         return suitable_versions[0][1]
    #     
    #     def resolve_dependencies(self, root_dependencies):
    #         """Разрешает зависимости"""
    #         resolved = {}  # name -> Package
    #         visited = set()
    #         visiting = set()
    #         
    #         def resolve_recursive(dependency):
    #             """Рекурсивное разрешение зависимостей"""
    #             if dependency.name in visiting:
    #                 raise ValueError(f"Циклическая зависимость обнаружена: {dependency.name}")
    #             
    #             if dependency.name in resolved:
    #                 return resolved[dependency.name]
    #             
    #             if dependency.optional and dependency.name not in self.packages:
    #                 return None
    #             
    #             package = self.find_package(dependency)
    #             if not package:
    #                 if dependency.optional:
    #                     return None
    #                 raise ValueError(f"Не удалось найти пакет: {dependency.name} {dependency.version_requirement}")
    #             
    #             visiting.add(dependency.name)
    #             
    #             # Разрешаем зависимости пакета
    #             for sub_dep in package.dependencies:
    #                 resolve_recursive(sub_dep)
    #             
    #             visiting.remove(dependency.name)
    #             visited.add(dependency.name)
    #             resolved[dependency.name] = package
    #             
    #             return package
    #         
    #         # Разрешаем все корневые зависимости
    #         for dep in root_dependencies:
    #             resolve_recursive(dep)
    #         
    #         return resolved
    #     
    #     def get_dependency_tree(self, resolved_packages):
    #         """Строит дерево зависимостей"""
    #         tree = {}
    #         
    #         for name, package in resolved_packages.items():
    #             tree[name] = {
    #                 'version': package.version,
    #                 'dependencies': [dep.name for dep in package.dependencies]
    #             }
    #         
    #         return tree
    # 
    # class PackageManager:
    #     """Менеджер пакетов"""
    #     
    #     def __init__(self):
    #         self.resolver = DependencyResolver()
    #         self.installed_packages = {}
    #         self.virtual_envs = {}
    #         self.current_env = "global"
    #     
    #     def create_virtual_env(self, name):
    #         """Создает виртуальное окружение"""
    #         self.virtual_envs[name] = {}
    #         print(f"Виртуальное окружение '{name}' создано")
    #     
    #     def activate_virtual_env(self, name):
    #         """Активирует виртуальное окружение"""
    #         if name not in self.virtual_envs:
    #             raise ValueError(f"Виртуальное окружение '{name}' не существует")
    #         self.current_env = name
    #         print(f"Активировано виртуальное окружение '{name}'")
    #     
    #     def get_current_packages(self):
    #         """Возвращает пакеты текущего окружения"""
    #         if self.current_env == "global":
    #             return self.installed_packages
    #         return self.virtual_envs.get(self.current_env, {})
    #     
    #     def install_package(self, dependency):
    #         """Устанавливает пакет с зависимостями"""
    #         try:
    #             resolved = self.resolver.resolve_dependencies([dependency])
    #             current_packages = self.get_current_packages()
    #             
    #             print(f"Установка пакета {dependency.name}...")
    #             print("Разрешенные зависимости:")
    #             
    #             for name, package in resolved.items():
    #                 print(f"  {name} {package.version}")
    #                 current_packages[name] = package
    #             
    #             print(f"Пакет {dependency.name} успешно установлен в окружение '{self.current_env}'")
    #             return True
    #             
    #         except ValueError as e:
    #             print(f"Ошибка установки: {e}")
    #             return False
    #     
    #     def uninstall_package(self, package_name):
    #         """Удаляет пакет"""
    #         current_packages = self.get_current_packages()
    #         if package_name in current_packages:
    #             del current_packages[package_name]
    #             print(f"Пакет {package_name} удален из окружения '{self.current_env}'")
    #         else:
    #             print(f"Пакет {package_name} не установлен в окружении '{self.current_env}'")
    #     
    #     def list_packages(self):
    #         """Выводит список установленных пакетов"""
    #         current_packages = self.get_current_packages()
    #         if not current_packages:
    #             print(f"В окружении '{self.current_env}' нет установленных пакетов")
    #         else:
    #             print(f"Установленные пакеты в '{self.current_env}':")
    #             for name, package in current_packages.items():
    #                 print(f"  {name} {package.version}")
    #     
    #     def show_dependency_tree(self, package_name):
    #         """Показывает дерево зависимостей пакета"""
    #         current_packages = self.get_current_packages()
    #         if package_name not in current_packages:
    #             print(f"Пакет {package_name} не установлен")
    #             return
    #         
    #         tree = self.resolver.get_dependency_tree(current_packages)
    #         self._print_tree(package_name, tree, set(), "")
    #     
    #     def _print_tree(self, package_name, tree, visited, prefix):
    #         """Рекурсивно выводит дерево зависимостей"""
    #         if package_name in visited:
    #             print(f"{prefix}{package_name} (циклическая зависимость)")
    #             return
    #         
    #         if package_name not in tree:
    #             print(f"{prefix}{package_name} (не найден)")
    #             return
    #         
    #         package_info = tree[package_name]
    #         print(f"{prefix}{package_name} {package_info['version']}")
    #         
    #         visited.add(package_name)
    #         for dep in package_info['dependencies']:
    #             self._print_tree(dep, tree, visited.copy(), prefix + "  ├─ ")
    # 
    # # Создаем тестовые пакеты
    # print("Создание репозитория пакетов...")
    # 
    # # Создаем менеджер
    # package_manager = PackageManager()
    # 
    # # Создаем пакеты
    # requests_pkg = Package(
    #     name="requests",
    #     version="2.28.0",
    #     dependencies=[
    #         Dependency("urllib3", ">= 1.21.1"),
    #         Dependency("certifi", ">= 2017.4.17"),
    #         Dependency("charset-normalizer", ">= 2.0.0")
    #     ],
    #     description="HTTP библиотека для Python"
    # )
    # 
    # urllib3_pkg = Package(
    #     name="urllib3",
    #     version="1.26.12",
    #     dependencies=[],
    #     description="HTTP клиент для Python"
    # )
    # 
    # certifi_pkg = Package(
    #     name="certifi",
    #     version="2022.9.24",
    #     dependencies=[],
    #     description="Сертификаты Mozilla CA Bundle"
    # )
    # 
    # charset_pkg = Package(
    #     name="charset-normalizer",
    #     version="2.1.1",
    #     dependencies=[],
    #     description="Детектор кодировки"
    # )
    # 
    # pandas_pkg = Package(
    #     name="pandas",
    #     version="1.5.0",
    #     dependencies=[
    #         Dependency("numpy", ">= 1.20.0"),
    #         Dependency("python-dateutil", ">= 2.8.1"),
    #         Dependency("pytz", ">= 2020.1")
    #     ],
    #     description="Анализ данных"
    # )
    # 
    # numpy_pkg = Package(
    #     name="numpy",
    #     version="1.23.4",
    #     dependencies=[],
    #     description="Научные вычисления"
    # )
    # 
    # dateutil_pkg = Package(
    #     name="python-dateutil",
    #     version="2.8.2",
    #     dependencies=[],
    #     description="Расширения для datetime"
    # )
    # 
    # pytz_pkg = Package(
    #     name="pytz",
    #     version="2022.6",
    #     dependencies=[],
    #     description="Часовые пояса"
    # )
    # 
    # # Добавляем пакеты в резолвер
    # packages = [requests_pkg, urllib3_pkg, certifi_pkg, charset_pkg, 
    #             pandas_pkg, numpy_pkg, dateutil_pkg, pytz_pkg]
    # 
    # for pkg in packages:
    #     package_manager.resolver.add_package(pkg)
    # 
    # print("Репозиторий создан!")
    # 
    # # Тестируем систему
    # print("\nТестирование менеджера пакетов:")
    # 
    # # Создаем виртуальное окружение
    # package_manager.create_virtual_env("myproject")
    # package_manager.activate_virtual_env("myproject")
    # 
    # # Устанавливаем пакеты
    # package_manager.install_package(Dependency("requests", ">= 2.25.0"))
    # package_manager.install_package(Dependency("pandas", ">= 1.0.0"))
    # 
    # # Показываем установленные пакеты
    # print("\n" + "="*50)
    # package_manager.list_packages()
    # 
    # # Показываем дерево зависимостей
    # print("\n" + "="*50)
    # print("Дерево зависимостей для requests:")
    # package_manager.show_dependency_tree("requests")
    # 
    # print("\n" + "="*50)
    # print("Дерево зависимостей для pandas:")
    # package_manager.show_dependency_tree("pandas")
    # 
    # print("\nМенеджер зависимостей работает корректно!")


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Математическая библиотека", exercise_01),
        ("Система конфигурации", exercise_02),
        ("Система плагинов", exercise_03),
        ("Модульная система логирования", exercise_04),
        ("Менеджер зависимостей", exercise_05),
    ]
    
    print("📦 Упражнения: Модули и пакеты Python")
    print("=" * 50)
    
    for i, (name, func) in enumerate(exercises, 1):
        print(f"\n{i}. {name}")
        print("-" * (len(name) + 3))
        try:
            func()
        except Exception as e:
            print(f"Ошибка при выполнении упражнения: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(exercises):
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main() 