#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Модули и пакеты Python

Этот файл содержит подробные примеры для изучения:
- Создания и импорта модулей
- Работы с пакетами и подпакетами
- Механизмов поиска модулей
- Различных способов импорта
- Управления зависимостями
- Создания собственных пакетов
"""

import sys
import os
import importlib
import types
from pathlib import Path


def example_01_basic_module_usage():
    """
    Пример 1: Основы работы с модулями
    
    Демонстрирует создание простого модуля,
    различные способы импорта и использования атрибутов модуля.
    """
    print("=== Пример 1: Основы работы с модулями ===")
    
    # Создаем временный модуль в памяти для демонстрации
    math_utils_code = '''
"""
Модуль математических утилит для демонстрации
"""

import math

PI = 3.14159265359
E = 2.71828182846

def circle_area(radius):
    """Вычисляет площадь круга"""
    return PI * radius ** 2

def circle_circumference(radius):
    """Вычисляет длину окружности"""
    return 2 * PI * radius

def power_of_e(x):
    """Возводит e в степень x"""
    return E ** x

class SimpleCalculator:
    """Простой калькулятор"""
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def multiply(a, b):
        return a * b
    
    @staticmethod
    def factorial(n):
        if n <= 1:
            return 1
        return n * SimpleCalculator.factorial(n - 1)

# Переменная, доступная при импорте
module_info = {
    "name": "math_utils",
    "version": "1.0.0",
    "author": "Python Course"
}

# Код, выполняющийся при запуске как скрипт
if __name__ == "__main__":
    print("Модуль math_utils запущен как скрипт")
    print(f"PI = {PI}")
    print(f"E = {E}")
    print(f"Площадь круга радиусом 5: {circle_area(5)}")
'''
    
    # Создаем модуль динамически
    def create_module_from_code(name, code):
        """Создает модуль из строки с кодом"""
        module = types.ModuleType(name)
        module.__file__ = f"<dynamic:{name}>"
        exec(code, module.__dict__)
        sys.modules[name] = module
        return module
    
    # Создаем и импортируем модуль
    math_utils = create_module_from_code("math_utils", math_utils_code)
    
    print("1. Информация о модуле:")
    print(f"Имя модуля: {math_utils.__name__}")
    print(f"Файл модуля: {math_utils.__file__}")
    print(f"Документация: {math_utils.__doc__}")
    
    print("\n2. Использование функций модуля:")
    radius = 7
    area = math_utils.circle_area(radius)
    circumference = math_utils.circle_circumference(radius)
    print(f"Радиус: {radius}")
    print(f"Площадь: {area:.2f}")
    print(f"Длина окружности: {circumference:.2f}")
    
    print("\n3. Использование класса из модуля:")
    calc = math_utils.SimpleCalculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"4 * 6 = {calc.multiply(4, 6)}")
    print(f"5! = {calc.factorial(5)}")
    
    print("\n4. Доступ к константам и переменным:")
    print(f"PI = {math_utils.PI}")
    print(f"E = {math_utils.E}")
    print(f"Информация о модуле: {math_utils.module_info}")
    
    print("\n5. Просмотр атрибутов модуля:")
    module_attrs = [attr for attr in dir(math_utils) if not attr.startswith('_')]
    print(f"Публичные атрибуты: {module_attrs}")
    
    # Демонстрация кеширования модулей
    print("\n6. Кеширование модулей в sys.modules:")
    print(f"math_utils в sys.modules: {'math_utils' in sys.modules}")
    
    # Повторный импорт возвращает тот же объект
    math_utils2 = sys.modules['math_utils']
    print(f"Тот же объект: {math_utils is math_utils2}")


def example_02_import_methods():
    """
    Пример 2: Различные способы импорта
    
    Демонстрирует все основные способы импорта модулей
    и их влияние на пространство имен.
    """
    print("=== Пример 2: Различные способы импорта ===")
    
    # Создаем модуль для демонстрации
    demo_module_code = '''
"""Демонстрационный модуль для изучения импортов"""

# Константы
CONSTANT_A = 100
CONSTANT_B = "Hello, World!"

# Функции
def public_function():
    """Публичная функция"""
    return "Это публичная функция"

def another_function(x, y):
    """Еще одна функция"""
    return x * y + 10

def _private_function():
    """Приватная функция (с подчеркиванием)"""
    return "Это приватная функция"

# Класс
class DemoClass:
    """Демонстрационный класс"""
    
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def double_value(self):
        return self.value * 2

# Контроль экспорта при import *
__all__ = ['CONSTANT_A', 'public_function', 'DemoClass']
'''
    
    # Создаем модуль
    demo_module = types.ModuleType("demo_module")
    demo_module.__file__ = "<dynamic:demo_module>"
    exec(demo_module_code, demo_module.__dict__)
    sys.modules['demo_module'] = demo_module
    
    print("1. Импорт всего модуля:")
    import demo_module
    print(f"Тип объекта: {type(demo_module)}")
    print(f"Доступ к константе: demo_module.CONSTANT_A = {demo_module.CONSTANT_A}")
    print(f"Вызов функции: demo_module.public_function() = {demo_module.public_function()}")
    
    print("\n2. Импорт с псевдонимом:")
    import demo_module as dm
    print(f"Псевдоним работает: dm.CONSTANT_B = {dm.CONSTANT_B}")
    
    print("\n3. Импорт конкретных объектов:")
    from demo_module import public_function, CONSTANT_A, DemoClass
    print(f"Прямой доступ к функции: public_function() = {public_function()}")
    print(f"Прямой доступ к константе: CONSTANT_A = {CONSTANT_A}")
    
    obj = DemoClass(42)
    print(f"Создание объекта: DemoClass(42).double_value() = {obj.double_value()}")
    
    print("\n4. Импорт с псевдонимами:")
    from demo_module import another_function as calc_func
    print(f"Функция с псевдонимом: calc_func(5, 3) = {calc_func(5, 3)}")
    
    print("\n5. Демонстрация __all__ (контроль экспорта):")
    # Имитируем from demo_module import *
    for name in demo_module.__all__:
        if hasattr(demo_module, name):
            locals()[name] = getattr(demo_module, name)
            print(f"Импортировано: {name}")
    
    # Проверяем, что приватная функция не импортирована
    try:
        _private_function()
        print("Приватная функция доступна (не должна быть)")
    except NameError:
        print("Приватная функция недоступна (правильно)")
    
    print("\n6. Условный импорт:")
    def conditional_import_demo():
        """Демонстрация условного импорта"""
        try:
            import json
            print("json модуль доступен")
            data = {"key": "value"}
            json_string = json.dumps(data)
            print(f"JSON строка: {json_string}")
            return True
        except ImportError:
            print("json модуль недоступен")
            return False
    
    json_available = conditional_import_demo()
    
    # Попытка импорта несуществующего модуля
    try:
        import nonexistent_module
    except ImportError as e:
        print(f"Ошибка импорта: {e}")


def example_03_module_search_path():
    """
    Пример 3: Механизм поиска модулей
    
    Демонстрирует, как Python ищет модули и как можно
    влиять на этот процесс.
    """
    print("=== Пример 3: Механизм поиска модулей ===")
    
    print("1. Текущие пути поиска модулей (sys.path):")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
    
    print(f"\nВсего путей: {len(sys.path)}")
    
    print("\n2. Информация о стандартных модулях:")
    import os
    import datetime
    
    standard_modules = [
        ('os', os),
        ('datetime', datetime),
        ('sys', sys)
    ]
    
    for name, module in standard_modules:
        file_path = getattr(module, '__file__', 'Встроенный модуль')
        package = getattr(module, '__package__', 'Не пакет')
        print(f"{name}:")
        print(f"  Файл: {file_path}")
        print(f"  Пакет: {package}")
    
    print("\n3. Временное добавление пути:")
    # Сохраняем оригинальный sys.path
    original_path = sys.path.copy()
    
    # Добавляем временный путь
    temp_path = "/tmp/my_modules"
    sys.path.insert(0, temp_path)
    print(f"Добавлен путь: {temp_path}")
    print(f"Новый первый путь: {sys.path[0]}")
    
    # Восстанавливаем оригинальный путь
    sys.path = original_path
    print("Путь восстановлен")
    
    print("\n4. Работа с importlib:")
    import importlib.util
    
    # Информация о спецификации модуля
    spec = importlib.util.find_spec("json")
    if spec:
        print(f"Модуль json найден:")
        print(f"  Имя: {spec.name}")
        print(f"  Происхождение: {spec.origin}")
        print(f"  Подмодули: {spec.submodule_search_locations}")
    
    print("\n5. Проверка существования модуля:")
    def check_module_exists(module_name):
        """Проверяет, существует ли модуль"""
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    
    test_modules = ["os", "json", "requests", "nonexistent_module"]
    for module in test_modules:
        exists = check_module_exists(module)
        status = "✓" if exists else "✗"
        print(f"  {status} {module}")
    
    print("\n6. Динамическая загрузка модуля:")
    def dynamic_import(module_name):
        """Динамически импортирует модуль"""
        try:
            module = importlib.import_module(module_name)
            print(f"Модуль {module_name} загружен динамически")
            return module
        except ImportError as e:
            print(f"Не удалось загрузить {module_name}: {e}")
            return None
    
    # Пример динамической загрузки
    collections_module = dynamic_import("collections")
    if collections_module:
        # Используем Counter из динамически загруженного модуля
        counter = collections_module.Counter("hello world")
        print(f"Counter результат: {dict(counter)}")


def example_04_package_creation():
    """
    Пример 4: Создание пакетов
    
    Демонстрирует создание структуры пакета,
    файлов __init__.py и работу с подпакетами.
    """
    print("=== Пример 4: Создание пакетов ===")
    
    print("1. Создание структуры пакета в памяти:")
    
    # Создаем главный пакет
    def create_package_structure():
        """Создает структуру пакета в sys.modules"""
        
        # Главный пакет mypackage
        main_package = types.ModuleType("mypackage")
        main_package.__file__ = "<dynamic:mypackage>"
        main_package.__path__ = ["<dynamic:mypackage>"]
        main_package.__package__ = "mypackage"
        
        # __init__.py содержимое для главного пакета
        init_code = '''
"""
Демонстрационный пакет
"""

__version__ = "1.0.0"
__author__ = "Python Course"

# Импорты для удобства пользователей
from .core import CoreClass, core_function
from .utils import utility_function
from .constants import PI, E

# Контроль экспорта
__all__ = [
    'CoreClass',
    'core_function', 
    'utility_function',
    'PI',
    'E',
    '__version__'
]

def package_info():
    """Возвращает информацию о пакете"""
    return {
        "name": __name__,
        "version": __version__,
        "author": __author__,
        "modules": __all__
    }

print(f"Инициализация пакета {__name__} версии {__version__}")
'''
        exec(init_code, main_package.__dict__)
        sys.modules["mypackage"] = main_package
        
        # Модуль core
        core_module = types.ModuleType("mypackage.core")
        core_module.__file__ = "<dynamic:mypackage.core>"
        core_module.__package__ = "mypackage"
        
        core_code = '''
"""Основной модуль пакета"""

class CoreClass:
    """Основной класс пакета"""
    
    def __init__(self, value):
        self.value = value
    
    def process(self):
        """Обрабатывает значение"""
        return self.value * 2
    
    def __repr__(self):
        return f"CoreClass({self.value})"

def core_function(x, y):
    """Основная функция пакета"""
    return x ** y + 42

def internal_function():
    """Внутренняя функция (не экспортируется)"""
    return "internal"
'''
        exec(core_code, core_module.__dict__)
        sys.modules["mypackage.core"] = core_module
        
        # Модуль utils
        utils_module = types.ModuleType("mypackage.utils")
        utils_module.__file__ = "<dynamic:mypackage.utils>"
        utils_module.__package__ = "mypackage"
        
        utils_code = '''
"""Утилиты пакета"""

def utility_function(text):
    """Полезная функция"""
    return f"Processed: {text.upper()}"

def format_number(num, decimals=2):
    """Форматирует число"""
    return f"{num:.{decimals}f}"

class Helper:
    """Вспомогательный класс"""
    
    @staticmethod
    def reverse_string(s):
        return s[::-1]
'''
        exec(utils_code, utils_module.__dict__)
        sys.modules["mypackage.utils"] = utils_module
        
        # Модуль constants
        constants_module = types.ModuleType("mypackage.constants")
        constants_module.__file__ = "<dynamic:mypackage.constants>"
        constants_module.__package__ = "mypackage"
        
        constants_code = '''
"""Константы пакета"""

PI = 3.14159265359
E = 2.71828182846
GOLDEN_RATIO = 1.61803398875

CONFIG = {
    "debug": False,
    "version": "1.0.0",
    "max_items": 1000
}

SUPPORTED_FORMATS = ["json", "xml", "csv", "yaml"]
'''
        exec(constants_code, constants_module.__dict__)
        sys.modules["mypackage.constants"] = constants_module
        
        return main_package
    
    # Создаем пакет
    mypackage = create_package_structure()
    
    print("2. Информация о созданном пакете:")
    print(f"Имя пакета: {mypackage.__name__}")
    print(f"Версия: {mypackage.__version__}")
    print(f"Автор: {mypackage.__author__}")
    print(f"Путь пакета: {mypackage.__path__}")
    
    print("\n3. Использование пакета:")
    
    # Импорт из пакета
    from mypackage import CoreClass, core_function, utility_function
    from mypackage.constants import PI, CONFIG
    
    # Использование классов и функций
    obj = CoreClass(21)
    print(f"Создан объект: {obj}")
    print(f"Результат обработки: {obj.process()}")
    
    result = core_function(2, 3)
    print(f"core_function(2, 3) = {result}")
    
    formatted_text = utility_function("hello world")
    print(f"utility_function результат: {formatted_text}")
    
    print(f"Константа PI из пакета: {PI}")
    print(f"Конфигурация: {CONFIG}")
    
    print("\n4. Информация о пакете:")
    package_info = mypackage.package_info()
    for key, value in package_info.items():
        print(f"  {key}: {value}")
    
    print("\n5. Модули в пакете:")
    package_modules = [name for name in sys.modules.keys() if name.startswith("mypackage")]
    for module_name in sorted(package_modules):
        print(f"  {module_name}")


def example_05_relative_imports():
    """
    Пример 5: Относительные импорты
    
    Демонстрирует использование относительных импортов
    в пакетах и подпакетах.
    """
    print("=== Пример 5: Относительные импорты ===")
    
    print("1. Создание пакета с подпакетами:")
    
    def create_complex_package():
        """Создает пакет со сложной структурой"""
        
        # Главный пакет
        main_pkg = types.ModuleType("complexpackage")
        main_pkg.__file__ = "<dynamic:complexpackage>"
        main_pkg.__path__ = ["<dynamic:complexpackage>"]
        main_pkg.__package__ = "complexpackage"
        
        main_init = '''
"""Комплексный пакет с подпакетами"""

__version__ = "2.0.0"

# Импорты из подпакетов для удобства
from .core.engine import Engine
from .utils.helpers import format_data
from .api.client import ApiClient

__all__ = ['Engine', 'format_data', 'ApiClient']
'''
        exec(main_init, main_pkg.__dict__)
        sys.modules["complexpackage"] = main_pkg
        
        # Подпакет core
        core_pkg = types.ModuleType("complexpackage.core")
        core_pkg.__file__ = "<dynamic:complexpackage.core>"
        core_pkg.__path__ = ["<dynamic:complexpackage.core>"]
        core_pkg.__package__ = "complexpackage.core"
        
        core_init = '''
"""Основной подпакет"""

from .engine import Engine
from .processor import Processor

__all__ = ['Engine', 'Processor']
'''
        exec(core_init, core_pkg.__dict__)
        sys.modules["complexpackage.core"] = core_pkg
        
        # Модуль engine в подпакете core
        engine_module = types.ModuleType("complexpackage.core.engine")
        engine_module.__file__ = "<dynamic:complexpackage.core.engine>"
        engine_module.__package__ = "complexpackage.core"
        
        engine_code = '''
"""Модуль движка"""

# Относительные импорты
from ..utils.helpers import format_data  # Из родительского пакета
from .processor import Processor         # Из того же подпакета

class Engine:
    """Основной движок"""
    
    def __init__(self, name):
        self.name = name
        self.processor = Processor()
    
    def run(self, data):
        """Запускает обработку данных"""
        processed = self.processor.process(data)
        formatted = format_data(processed)
        return f"Engine {self.name}: {formatted}"
    
    def __repr__(self):
        return f"Engine({self.name})"
'''
        exec(engine_code, engine_module.__dict__)
        sys.modules["complexpackage.core.engine"] = engine_module
        
        # Модуль processor
        processor_module = types.ModuleType("complexpackage.core.processor")
        processor_module.__file__ = "<dynamic:complexpackage.core.processor>"
        processor_module.__package__ = "complexpackage.core"
        
        processor_code = '''
"""Модуль процессора"""

class Processor:
    """Процессор данных"""
    
    def process(self, data):
        """Обрабатывает данные"""
        if isinstance(data, str):
            return data.upper()
        elif isinstance(data, list):
            return [str(item) for item in data]
        else:
            return str(data)
'''
        exec(processor_code, processor_module.__dict__)
        sys.modules["complexpackage.core.processor"] = processor_module
        
        # Подпакет utils
        utils_pkg = types.ModuleType("complexpackage.utils")
        utils_pkg.__file__ = "<dynamic:complexpackage.utils>"
        utils_pkg.__path__ = ["<dynamic:complexpackage.utils>"]
        utils_pkg.__package__ = "complexpackage.utils"
        
        utils_init = '''
"""Подпакет утилит"""

from .helpers import format_data, validate_input

__all__ = ['format_data', 'validate_input']
'''
        exec(utils_init, utils_pkg.__dict__)
        sys.modules["complexpackage.utils"] = utils_pkg
        
        # Модуль helpers
        helpers_module = types.ModuleType("complexpackage.utils.helpers")
        helpers_module.__file__ = "<dynamic:complexpackage.utils.helpers>"
        helpers_module.__package__ = "complexpackage.utils"
        
        helpers_code = '''
"""Вспомогательные функции"""

def format_data(data):
    """Форматирует данные"""
    return f"[FORMATTED] {data}"

def validate_input(data):
    """Валидирует входные данные"""
    if data is None:
        raise ValueError("Данные не могут быть None")
    return True
'''
        exec(helpers_code, helpers_module.__dict__)
        sys.modules["complexpackage.utils.helpers"] = helpers_module
        
        # Подпакет api
        api_pkg = types.ModuleType("complexpackage.api")
        api_pkg.__file__ = "<dynamic:complexpackage.api>"
        api_pkg.__path__ = ["<dynamic:complexpackage.api>"]
        api_pkg.__package__ = "complexpackage.api"
        
        api_init = '''
"""API подпакет"""

from .client import ApiClient

__all__ = ['ApiClient']
'''
        exec(api_init, api_pkg.__dict__)
        sys.modules["complexpackage.api"] = api_pkg
        
        # Модуль client
        client_module = types.ModuleType("complexpackage.api.client")
        client_module.__file__ = "<dynamic:complexpackage.api.client>"
        client_module.__package__ = "complexpackage.api"
        
        client_code = '''
"""API клиент"""

# Относительный импорт из другого подпакета
from ..core.engine import Engine
from ..utils.helpers import validate_input

class ApiClient:
    """API клиент"""
    
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.engine = Engine("API-Engine")
    
    def request(self, data):
        """Выполняет запрос"""
        validate_input(data)
        result = self.engine.run(data)
        return f"API[{self.endpoint}]: {result}"
'''
        exec(client_code, client_module.__dict__)
        sys.modules["complexpackage.api.client"] = client_module
        
        return main_pkg
    
    # Создаем комплексный пакет
    complex_pkg = create_complex_package()
    
    print("2. Структура созданного пакета:")
    package_modules = [name for name in sys.modules.keys() if name.startswith("complexpackage")]
    for module_name in sorted(package_modules):
        print(f"  {module_name}")
    
    print("\n3. Использование пакета с относительными импортами:")
    
    # Импорт из главного пакета
    from complexpackage import Engine, format_data, ApiClient
    
    # Создание и использование объектов
    engine = Engine("TestEngine")
    print(f"Создан движок: {engine}")
    
    result = engine.run("test data")
    print(f"Результат работы движка: {result}")
    
    # Использование API клиента
    client = ApiClient("https://api.example.com")
    api_result = client.request(["item1", "item2", "item3"])
    print(f"Результат API запроса: {api_result}")
    
    print("\n4. Прямое использование вспомогательных функций:")
    formatted = format_data("raw data")
    print(f"Форматированные данные: {formatted}")


def example_06_dynamic_imports():
    """
    Пример 6: Динамические импорты
    
    Демонстрирует различные способы динамической загрузки модулей
    и работу с importlib.
    """
    print("=== Пример 6: Динамические импорты ===")
    
    print("1. Базовые функции importlib:")
    
    # Динамический импорт модуля
    math_module = importlib.import_module("math")
    print(f"Динамически импортированный math: {math_module}")
    print(f"math.pi = {math_module.pi}")
    print(f"math.sqrt(16) = {math_module.sqrt(16)}")
    
    print("\n2. Импорт атрибута из модуля:")
    
    def import_attribute(module_name, attribute_name):
        """Импортирует конкретный атрибут из модуля"""
        try:
            module = importlib.import_module(module_name)
            return getattr(module, attribute_name)
        except (ImportError, AttributeError) as e:
            print(f"Ошибка импорта {module_name}.{attribute_name}: {e}")
            return None
    
    # Импорт конкретных функций
    datetime_class = import_attribute("datetime", "datetime")
    if datetime_class:
        now = datetime_class.now()
        print(f"Текущее время: {now}")
    
    json_loads = import_attribute("json", "loads")
    if json_loads:
        data = json_loads('{"key": "value"}')
        print(f"Разобранный JSON: {data}")
    
    print("\n3. Условный импорт с fallback:")
    
    def safe_import(primary_module, fallback_module=None):
        """Безопасный импорт с резервным модулем"""
        try:
            return importlib.import_module(primary_module)
        except ImportError:
            if fallback_module:
                try:
                    print(f"Модуль {primary_module} недоступен, используется {fallback_module}")
                    return importlib.import_module(fallback_module)
                except ImportError:
                    print(f"Оба модуля недоступны: {primary_module}, {fallback_module}")
                    return None
            else:
                print(f"Модуль {primary_module} недоступен")
                return None
    
    # Попытка импорта с fallback
    ujson_or_json = safe_import("ujson", "json")
    if ujson_or_json:
        test_data = {"test": "data"}
        json_string = ujson_or_json.dumps(test_data)
        print(f"JSON строка: {json_string}")
    
    print("\n4. Загрузка модулей из строки:")
    
    def load_module_from_string(name, source_code):
        """Загружает модуль из строки с кодом"""
        import tempfile
        import importlib.util
        
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(source_code)
            temp_filename = f.name
        
        try:
            # Создаем спецификацию модуля
            spec = importlib.util.spec_from_file_location(name, temp_filename)
            module = importlib.util.module_from_spec(spec)
            
            # Загружаем модуль
            sys.modules[name] = module
            spec.loader.exec_module(module)
            
            return module
        finally:
            # Удаляем временный файл
            os.unlink(temp_filename)
    
    # Код для загрузки
    dynamic_code = '''
"""Динамически загруженный модуль"""

def greet(name):
    return f"Привет, {name}! Я загружен динамически."

class DynamicClass:
    def __init__(self, value):
        self.value = value
    
    def display(self):
        return f"Динамическое значение: {self.value}"

DYNAMIC_CONSTANT = "Я из динамического модуля!"
'''
    
    dynamic_module = load_module_from_string("dynamic_test", dynamic_code)
    if dynamic_module:
        print(f"Загружен модуль: {dynamic_module.__name__}")
        print(f"Приветствие: {dynamic_module.greet('Python')}")
        
        obj = dynamic_module.DynamicClass("тест")
        print(f"Объект: {obj.display()}")
        print(f"Константа: {dynamic_module.DYNAMIC_CONSTANT}")
    
    print("\n5. Перезагрузка модулей:")
    
    def reload_module_demo():
        """Демонстрирует перезагрузку модуля"""
        # Создаем модуль с переменной
        test_module_code = '''
counter = 0

def increment():
    global counter
    counter += 1
    return counter

def get_counter():
    return counter
'''
        
        test_module = types.ModuleType("reload_test")
        test_module.__file__ = "<dynamic:reload_test>"
        exec(test_module_code, test_module.__dict__)
        sys.modules["reload_test"] = test_module
        
        print("До перезагрузки:")
        print(f"Счетчик: {test_module.get_counter()}")
        print(f"После increment(): {test_module.increment()}")
        print(f"После increment(): {test_module.increment()}")
        
        # Перезагружаем модуль
        importlib.reload(test_module)
        
        print("После перезагрузки:")
        print(f"Счетчик сброшен: {test_module.get_counter()}")
    
    reload_module_demo()
    
    print("\n6. Ленивая загрузка модулей:")
    
    class LazyLoader:
        """Ленивая загрузка модулей"""
        
        def __init__(self, module_name):
            self.module_name = module_name
            self._module = None
        
        def __getattr__(self, name):
            if self._module is None:
                print(f"Ленивая загрузка модуля: {self.module_name}")
                self._module = importlib.import_module(self.module_name)
            return getattr(self._module, name)
    
    # Модуль не загружается до первого обращения
    lazy_os = LazyLoader("os")
    print("LazyLoader создан, модуль еще не загружен")
    
    # Теперь модуль загружается
    current_dir = lazy_os.getcwd()
    print(f"Текущая директория: {current_dir}")


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Основы работы с модулями", example_01_basic_module_usage),
        ("Различные способы импорта", example_02_import_methods),
        ("Механизм поиска модулей", example_03_module_search_path),
        ("Создание пакетов", example_04_package_creation),
        ("Относительные импорты", example_05_relative_imports),
        ("Динамические импорты", example_06_dynamic_imports),
    ]
    
    print("📦 Примеры: Модули и пакеты Python")
    print("=" * 50)
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")
        print("-" * (len(name) + 3))
        try:
            func()
        except Exception as e:
            print(f"Ошибка при выполнении примера: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(examples):
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main() 