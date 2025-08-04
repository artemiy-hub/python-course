#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Модули и пакеты в Python

Этот файл содержит подробные примеры для изучения:
- Создания и использования модулей
- Различных способов импорта
- Создания пакетов
- Динамического импорта
- Системы плагинов
- Управления зависимостями
- Лучших практик организации кода
"""

import sys
import os
import importlib
import importlib.util
import types
import json
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional


def example_01_basic_module_creation():
    """
    Пример 1: Создание и использование простых модулей
    
    Демонстрирует создание модуля, различные способы импорта
    и работу с атрибутами модуля.
    """
    print("=== Пример 1: Создание и использование простых модулей ===")
    
    # Создаем временную директорию для модулей
    temp_dir = tempfile.mkdtemp()
    sys.path.insert(0, temp_dir)
    
    print(f"Временная директория для модулей: {temp_dir}")
    
    try:
        # 1. Создание простого модуля
        math_utils_code = '''
"""
Модуль математических утилит
Демонстрирует основы создания модулей
"""

__version__ = "1.0.0"
__author__ = "Python Developer"

# Константы
PI = 3.14159265359
E = 2.71828182846

# Переменные модуля
calculation_count = 0

def square(x):
    """Возвести число в квадрат"""
    global calculation_count
    calculation_count += 1
    return x * x

def cube(x):
    """Возвести число в куб"""
    global calculation_count
    calculation_count += 1
    return x * x * x

def circle_area(radius):
    """Вычислить площадь круга"""
    global calculation_count
    calculation_count += 1
    return PI * square(radius)

def factorial(n):
    """Вычислить факториал"""
    global calculation_count
    calculation_count += 1
    
    if n <= 1:
        return 1
    return n * factorial(n - 1)

class Calculator:
    """Простой калькулятор"""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def get_history(self):
        return self.history.copy()

# Код, выполняемый при импорте
print(f"Модуль {__name__} загружен, версия {__version__}")

if __name__ == "__main__":
    print("Тестирование модуля math_utils:")
    print(f"5^2 = {square(5)}")
    print(f"Площадь круга (r=3): {circle_area(3)}")
    print(f"5! = {factorial(5)}")
    
    calc = Calculator()
    print(f"10 + 5 = {calc.add(10, 5)}")
    print(f"История: {calc.get_history()}")
'''
        
        # Сохраняем модуль в файл
        math_utils_path = os.path.join(temp_dir, "math_utils.py")
        with open(math_utils_path, 'w') as f:
            f.write(math_utils_code)
        
        print("1. Модуль math_utils создан")
        
        # 2. Различные способы импорта
        print("\n2. Различные способы импорта:")
        
        # Полный импорт модуля
        import math_utils
        print(f"Полный импорт - версия: {math_utils.__version__}")
        print(f"Автор: {math_utils.__author__}")
        print(f"Квадрат 7: {math_utils.square(7)}")
        
        # Импорт конкретных функций
        from math_utils import circle_area, PI
        print(f"Импорт функций - PI: {PI}")
        print(f"Площадь круга (r=4): {circle_area(4)}")
        
        # Импорт с псевдонимом
        import math_utils as mu
        print(f"Импорт с псевдонимом - куб 3: {mu.cube(3)}")
        
        # Импорт класса
        from math_utils import Calculator
        calc = Calculator()
        result = calc.multiply(6, 7)
        print(f"Использование класса: 6 * 7 = {result}")
        
        # 3. Исследование атрибутов модуля
        print("\n3. Атрибуты модуля:")
        print(f"Имя модуля: {math_utils.__name__}")
        print(f"Файл модуля: {math_utils.__file__}")
        print(f"Документация: {math_utils.__doc__[:50]}...")
        print(f"Количество вычислений: {math_utils.calculation_count}")
        
        # 4. Динамические атрибуты
        print("\n4. Динамическое изменение модуля:")
        
        # Добавляем новую функцию в модуль
        def power(base, exponent):
            return base ** exponent
        
        math_utils.power = power
        print(f"Добавили функцию power: 2^8 = {math_utils.power(2, 8)}")
        
        # Изменяем константу
        old_pi = math_utils.PI
        math_utils.PI = 3.14159
        print(f"Изменили PI с {old_pi} на {math_utils.PI}")
        
        # 5. Список всех атрибутов модуля
        print("\n5. Все публичные атрибуты модуля:")
        public_attrs = [attr for attr in dir(math_utils) if not attr.startswith('_')]
        for attr in public_attrs:
            value = getattr(math_utils, attr)
            attr_type = type(value).__name__
            print(f"  {attr}: {attr_type}")
        
        # 6. Создание модуля с __all__
        string_utils_code = '''
"""
Модуль для работы со строками
Демонстрирует использование __all__
"""

def capitalize_words(text):
    """Сделать первую букву каждого слова заглавной"""
    return ' '.join(word.capitalize() for word in text.split())

def reverse_string(text):
    """Обратить строку"""
    return text[::-1]

def count_vowels(text):
    """Подсчитать гласные"""
    vowels = 'aeiouAEIOU'
    return sum(1 for char in text if char in vowels)

def _internal_helper(text):
    """Внутренняя функция (не экспортируется)"""
    return text.lower()

# Определяем публичный API
__all__ = ['capitalize_words', 'reverse_string', 'count_vowels']

# Эта функция не в __all__, но все равно доступна при прямом импорте
def hidden_function():
    return "Я скрыта от wildcard импорта"
'''
        
        string_utils_path = os.path.join(temp_dir, "string_utils.py")
        with open(string_utils_path, 'w') as f:
            f.write(string_utils_code)
        
        print("\n6. Модуль с __all__ создан:")
        
        import string_utils
        
        # Проверяем __all__
        print(f"__all__ определяет: {string_utils.__all__}")
        
        # Тестируем функции
        test_text = "hello world python"
        print(f"Исходный текст: {test_text}")
        print(f"Капитализация: {string_utils.capitalize_words(test_text)}")
        print(f"Обращение: {string_utils.reverse_string(test_text)}")
        print(f"Гласные: {string_utils.count_vowels(test_text)}")
        
        # Доступ к скрытой функции
        print(f"Скрытая функция: {string_utils.hidden_function()}")
        
        # Wildcard импорт (в реальном коде не рекомендуется)
        exec("from string_utils import *")
        
    finally:
        # Очищаем временные файлы
        sys.path.remove(temp_dir)
        shutil.rmtree(temp_dir)
        print(f"\nВременная директория {temp_dir} удалена")


def example_02_package_creation():
    """
    Пример 2: Создание и использование пакетов
    
    Демонстрирует создание иерархической структуры пакетов,
    различные виды импорта и организацию кода.
    """
    print("=== Пример 2: Создание и использование пакетов ===")
    
    # Создаем временную директорию для пакета
    temp_dir = tempfile.mkdtemp()
    sys.path.insert(0, temp_dir)
    
    print(f"Создаем пакет в: {temp_dir}")
    
    try:
        # Структура пакета:
        # myapp/
        #   __init__.py
        #   core/
        #     __init__.py
        #     database.py
        #     models.py
        #   utils/
        #     __init__.py
        #     helpers.py
        #     validators.py
        #   api/
        #     __init__.py
        #     handlers.py
        
        # 1. Создаем основной пакет
        package_dir = os.path.join(temp_dir, "myapp")
        os.makedirs(package_dir)
        
        # Основной __init__.py
        main_init = '''
"""
MyApp - демонстрационное приложение
Показывает структуру пакета и импорты
"""

__version__ = "1.0.0"
__author__ = "Python Developer"

# Импортируем основные компоненты для удобного доступа
from .core.models import User, Product
from .core.database import Database
from .utils.helpers import format_date, generate_id
from .api.handlers import APIHandler

# Определяем публичный API пакета
__all__ = [
    'User', 'Product', 'Database', 
    'format_date', 'generate_id', 'APIHandler'
]

# Инициализация пакета
print(f"MyApp v{__version__} инициализирован")

def get_version():
    """Получить версию пакета"""
    return __version__
'''
        
        with open(os.path.join(package_dir, "__init__.py"), 'w') as f:
            f.write(main_init)
        
        # 2. Создаем подпакет core
        core_dir = os.path.join(package_dir, "core")
        os.makedirs(core_dir)
        
        # core/__init__.py
        core_init = '''
"""
Основная логика приложения
"""

from .database import Database
from .models import User, Product

__all__ = ['Database', 'User', 'Product']
'''
        
        with open(os.path.join(core_dir, "__init__.py"), 'w') as f:
            f.write(core_init)
        
        # core/database.py
        database_code = '''
"""
Модуль для работы с базой данных
"""

from typing import Dict, List, Any, Optional
from ..utils.helpers import generate_id

class Database:
    """Простая база данных в памяти"""
    
    def __init__(self):
        self._data = {}
        self._tables = set()
    
    def create_table(self, table_name: str):
        """Создать таблицу"""
        if table_name not in self._tables:
            self._data[table_name] = {}
            self._tables.add(table_name)
            print(f"Таблица '{table_name}' создана")
        else:
            print(f"Таблица '{table_name}' уже существует")
    
    def insert(self, table_name: str, data: Dict[str, Any]) -> str:
        """Вставить запись"""
        if table_name not in self._tables:
            self.create_table(table_name)
        
        record_id = data.get('id', generate_id())
        data['id'] = record_id
        self._data[table_name][record_id] = data
        print(f"Запись {record_id} добавлена в {table_name}")
        return record_id
    
    def find(self, table_name: str, record_id: str) -> Optional[Dict]:
        """Найти запись по ID"""
        if table_name in self._data:
            return self._data[table_name].get(record_id)
        return None
    
    def find_all(self, table_name: str) -> List[Dict]:
        """Получить все записи таблицы"""
        if table_name in self._data:
            return list(self._data[table_name].values())
        return []
    
    def update(self, table_name: str, record_id: str, data: Dict[str, Any]):
        """Обновить запись"""
        if table_name in self._data and record_id in self._data[table_name]:
            self._data[table_name][record_id].update(data)
            print(f"Запись {record_id} обновлена")
            return True
        return False
    
    def delete(self, table_name: str, record_id: str):
        """Удалить запись"""
        if table_name in self._data and record_id in self._data[table_name]:
            del self._data[table_name][record_id]
            print(f"Запись {record_id} удалена")
            return True
        return False
    
    def get_stats(self):
        """Статистика базы данных"""
        stats = {}
        for table in self._tables:
            stats[table] = len(self._data.get(table, {}))
        return stats
'''
        
        with open(os.path.join(core_dir, "database.py"), 'w') as f:
            f.write(database_code)
        
        # core/models.py
        models_code = '''
"""
Модели данных приложения
"""

from datetime import datetime
from typing import Dict, Any
from ..utils.validators import validate_email
from ..utils.helpers import generate_id

class BaseModel:
    """Базовая модель"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', generate_id())
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update(self, **kwargs):
        """Обновить модель"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

class User(BaseModel):
    """Модель пользователя"""
    
    def __init__(self, name: str, email: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.email = self._validate_email(email)
        self.active = kwargs.get('active', True)
    
    def _validate_email(self, email: str) -> str:
        """Валидация email"""
        if not validate_email(email):
            raise ValueError(f"Некорректный email: {email}")
        return email
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'email': self.email,
            'active': self.active
        })
        return data
    
    def deactivate(self):
        """Деактивировать пользователя"""
        self.active = False
        self.update()
    
    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"

class Product(BaseModel):
    """Модель продукта"""
    
    def __init__(self, name: str, price: float, category: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.price = self._validate_price(price)
        self.category = category
        self.in_stock = kwargs.get('in_stock', True)
        self.quantity = kwargs.get('quantity', 0)
    
    def _validate_price(self, price: float) -> float:
        """Валидация цены"""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        return price
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'in_stock': self.in_stock,
            'quantity': self.quantity
        })
        return data
    
    def set_price(self, new_price: float):
        """Установить новую цену"""
        self.price = self._validate_price(new_price)
        self.update()
    
    def add_stock(self, quantity: int):
        """Добавить на склад"""
        self.quantity += quantity
        if self.quantity > 0:
            self.in_stock = True
        self.update()
    
    def remove_stock(self, quantity: int):
        """Убрать со склада"""
        self.quantity = max(0, self.quantity - quantity)
        if self.quantity == 0:
            self.in_stock = False
        self.update()
    
    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price})"
'''
        
        with open(os.path.join(core_dir, "models.py"), 'w') as f:
            f.write(models_code)
        
        # 3. Создаем подпакет utils
        utils_dir = os.path.join(package_dir, "utils")
        os.makedirs(utils_dir)
        
        # utils/__init__.py
        utils_init = '''
"""
Утилиты приложения
"""

from .helpers import format_date, generate_id, format_currency
from .validators import validate_email, validate_phone

__all__ = ['format_date', 'generate_id', 'format_currency', 'validate_email', 'validate_phone']
'''
        
        with open(os.path.join(utils_dir, "__init__.py"), 'w') as f:
            f.write(utils_init)
        
        # utils/helpers.py
        helpers_code = '''
"""
Вспомогательные функции
"""

import uuid
from datetime import datetime
from typing import Any

def generate_id() -> str:
    """Генерировать уникальный ID"""
    return str(uuid.uuid4())[:8]

def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Форматировать дату"""
    return date.strftime(format_str)

def format_currency(amount: float, currency: str = "RUB") -> str:
    """Форматировать валюту"""
    return f"{amount:.2f} {currency}"

def safe_get(dictionary: dict, key: str, default: Any = None) -> Any:
    """Безопасно получить значение из словаря"""
    return dictionary.get(key, default)

def chunk_list(lst: list, chunk_size: int) -> list:
    """Разбить список на части"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def flatten_dict(nested_dict: dict, separator: str = '.') -> dict:
    """Преобразовать вложенный словарь в плоский"""
    def _flatten(obj, parent_key=''):
        items = []
        for key, value in obj.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(_flatten(value, new_key).items())
            else:
                items.append((new_key, value))
        return dict(items)
    
    return _flatten(nested_dict)
'''
        
        with open(os.path.join(utils_dir, "helpers.py"), 'w') as f:
            f.write(helpers_code)
        
        # utils/validators.py
        validators_code = '''
"""
Функции валидации
"""

import re
from typing import Any

def validate_email(email: str) -> bool:
    """Валидация email адреса"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Валидация номера телефона"""
    # Простая валидация для российских номеров
    pattern = r'^\\+?[78]?[\\s\\-]?\\(?\\d{3}\\)?[\\s\\-]?\\d{3}[\\s\\-]?\\d{2}[\\s\\-]?\\d{2}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))

def validate_range(value: Any, min_val: Any = None, max_val: Any = None) -> bool:
    """Валидация значения в диапазоне"""
    try:
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True
    except TypeError:
        return False

def validate_length(text: str, min_length: int = 0, max_length: int = None) -> bool:
    """Валидация длины строки"""
    length = len(text)
    if length < min_length:
        return False
    if max_length is not None and length > max_length:
        return False
    return True

def validate_not_empty(value: Any) -> bool:
    """Проверка на непустое значение"""
    if value is None:
        return False
    if isinstance(value, (str, list, dict)) and len(value) == 0:
        return False
    return True
'''
        
        with open(os.path.join(utils_dir, "validators.py"), 'w') as f:
            f.write(validators_code)
        
        # 4. Создаем подпакет api
        api_dir = os.path.join(package_dir, "api")
        os.makedirs(api_dir)
        
        # api/__init__.py
        api_init = '''
"""
API модуль приложения
"""

from .handlers import APIHandler

__all__ = ['APIHandler']
'''
        
        with open(os.path.join(api_dir, "__init__.py"), 'w') as f:
            f.write(api_init)
        
        # api/handlers.py
        handlers_code = '''
"""
Обработчики API
"""

from typing import Dict, List, Any
from ..core.database import Database
from ..core.models import User, Product
from ..utils.helpers import format_date, format_currency
from datetime import datetime

class APIHandler:
    """Обработчик API запросов"""
    
    def __init__(self):
        self.db = Database()
        self.db.create_table('users')
        self.db.create_table('products')
    
    def create_user(self, name: str, email: str) -> Dict[str, Any]:
        """Создать пользователя"""
        try:
            user = User(name=name, email=email)
            user_id = self.db.insert('users', user.to_dict())
            return {
                'success': True,
                'user_id': user_id,
                'message': f'Пользователь {name} создан'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Получить пользователя"""
        user_data = self.db.find('users', user_id)
        if user_data:
            return {
                'success': True,
                'user': user_data
            }
        return {
            'success': False,
            'error': 'Пользователь не найден'
        }
    
    def create_product(self, name: str, price: float, category: str, quantity: int = 0) -> Dict[str, Any]:
        """Создать продукт"""
        try:
            product = Product(name=name, price=price, category=category, quantity=quantity)
            product_id = self.db.insert('products', product.to_dict())
            return {
                'success': True,
                'product_id': product_id,
                'message': f'Продукт {name} создан'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """Получить продукты по категории"""
        all_products = self.db.find_all('products')
        return [p for p in all_products if p.get('category') == category]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику"""
        db_stats = self.db.get_stats()
        return {
            'timestamp': format_date(datetime.now()),
            'database_stats': db_stats,
            'total_records': sum(db_stats.values())
        }
'''
        
        with open(os.path.join(api_dir, "handlers.py"), 'w') as f:
            f.write(handlers_code)
        
        print("Структура пакета создана:")
        
        # Показываем структуру
        def show_tree(path, prefix="", max_depth=3, current_depth=0):
            if current_depth >= max_depth:
                return
            
            items = sorted(os.listdir(path))
            for i, item in enumerate(items):
                if item.startswith('.'):
                    continue
                
                item_path = os.path.join(path, item)
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item}")
                
                if os.path.isdir(item_path) and current_depth < max_depth - 1:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    show_tree(item_path, next_prefix, max_depth, current_depth + 1)
        
        show_tree(package_dir)
        
        # 5. Тестирование пакета
        print("\n5. Тестирование пакета:")
        
        # Импорт всего пакета
        import myapp
        print(f"Импортирован пакет myapp v{myapp.get_version()}")
        
        # Использование импортированных компонентов
        print("\n6. Создание и работа с данными:")
        
        # Создаем API handler
        api = myapp.APIHandler()
        
        # Создаем пользователей
        user1_result = api.create_user("Алиса Иванова", "alice@example.com")
        user2_result = api.create_user("Боб Петров", "bob@example.com")
        
        print(f"Создание пользователя 1: {user1_result}")
        print(f"Создание пользователя 2: {user2_result}")
        
        # Создаем продукты
        product1_result = api.create_product("Ноутбук", 50000.0, "Электроника", 10)
        product2_result = api.create_product("Мышь", 1500.0, "Электроника", 50)
        product3_result = api.create_product("Книга Python", 2000.0, "Книги", 20)
        
        print(f"Создание продукта 1: {product1_result}")
        print(f"Создание продукта 2: {product2_result}")
        print(f"Создание продукта 3: {product3_result}")
        
        # Получаем статистику
        stats = api.get_statistics()
        print(f"\nСтатистика: {stats}")
        
        # Поиск продуктов по категории
        electronics = api.get_products_by_category("Электроника")
        print(f"\nПродукты в категории 'Электроника': {len(electronics)}")
        for product in electronics:
            print(f"  - {product['name']}: {myapp.format_currency(product['price'])}")
        
        # 7. Различные способы импорта из пакета
        print("\n7. Различные способы импорта:")
        
        # Импорт из подпакета
        from myapp.core import Database
        db = Database()
        print("Импорт Database из core подпакета")
        
        # Импорт с полным путем
        from myapp.utils.helpers import generate_id
        new_id = generate_id()
        print(f"Сгенерированный ID: {new_id}")
        
        # Импорт класса модели
        from myapp.core.models import User
        user = User("Тест Пользователь", "test@example.com")
        print(f"Создан пользователь: {user}")
        
        # Относительный импорт (демонстрация)
        print("\n8. Пример относительного импорта в коде пакета:")
        print("В models.py используется: from ..utils.validators import validate_email")
        print("В database.py используется: from ..utils.helpers import generate_id")
        
    finally:
        # Очищаем
        sys.path.remove(temp_dir)
        shutil.rmtree(temp_dir)
        print(f"\nВременная директория удалена")


def example_03_dynamic_imports():
    """
    Пример 3: Динамический импорт модулей
    
    Демонстрирует различные способы динамического импорта,
    загрузку модулей из файлов и создание модулей из строк.
    """
    print("=== Пример 3: Динамический импорт модулей ===")
    
    # Создаем временную директорию
    temp_dir = tempfile.mkdtemp()
    sys.path.insert(0, temp_dir)
    
    try:
        print("1. Импорт модулей по имени:")
        
        # Функция для динамического импорта
        def import_module_by_name(module_name):
            """Динамический импорт модуля"""
            try:
                module = importlib.import_module(module_name)
                print(f"✅ Успешно импортирован {module_name}")
                return module
            except ImportError as e:
                print(f"❌ Не удалось импортировать {module_name}: {e}")
                return None
        
        # Тестируем с различными модулями
        test_modules = ['json', 'datetime', 'nonexistent_module', 'os']
        
        imported_modules = {}
        for module_name in test_modules:
            module = import_module_by_name(module_name)
            if module:
                imported_modules[module_name] = module
        
        # Используем динамически импортированные модули
        if 'json' in imported_modules:
            json_module = imported_modules['json']
            test_data = {"name": "Python", "version": 3.12}
            json_string = json_module.dumps(test_data)
            print(f"JSON сериализация: {json_string}")
        
        if 'datetime' in imported_modules:
            datetime_module = imported_modules['datetime']
            now = datetime_module.datetime.now()
            print(f"Текущее время: {now}")
        
        print("\n2. Условный импорт модулей:")
        
        def get_best_json_module():
            """Получить лучший доступный JSON модуль"""
            json_modules = ['ujson', 'rapidjson', 'json']
            
            for module_name in json_modules:
                try:
                    module = importlib.import_module(module_name)
                    print(f"Используем {module_name} для JSON")
                    return module
                except ImportError:
                    continue
            
            raise ImportError("Ни один JSON модуль недоступен")
        
        json_lib = get_best_json_module()
        test_data = {"dynamic": True, "modules": ["json"]}
        print(f"Лучший JSON модуль: {json_lib.dumps(test_data)}")
        
        print("\n3. Загрузка модуля из файла:")
        
        # Создаем модуль в файле
        plugin_code = '''
"""
Плагин для демонстрации загрузки из файла
"""

__version__ = "1.0.0"
__author__ = "Plugin Developer"

def process_data(data):
    """Обработать данные"""
    if isinstance(data, list):
        return [item * 2 for item in data]
    elif isinstance(data, str):
        return data.upper()
    else:
        return str(data)

def get_info():
    """Получить информацию о плагине"""
    return {
        "name": "Demo Plugin",
        "version": __version__,
        "author": __author__
    }

class DataProcessor:
    """Процессор данных"""
    
    def __init__(self, multiplier=1):
        self.multiplier = multiplier
    
    def process(self, value):
        return value * self.multiplier
    
    def get_stats(self):
        return {"multiplier": self.multiplier}

# Код выполняется при загрузке
print(f"Плагин {__name__} загружен")
'''
        
        plugin_path = os.path.join(temp_dir, "demo_plugin.py")
        with open(plugin_path, 'w') as f:
            f.write(plugin_code)
        
        def load_module_from_file(file_path, module_name=None):
            """Загрузить модуль из файла"""
            if module_name is None:
                module_name = Path(file_path).stem
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                raise ImportError(f"Не удалось создать спецификацию для {file_path}")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            return module
        
        # Загружаем плагин
        plugin = load_module_from_file(plugin_path, "demo_plugin")
        
        print(f"Загружен плагин: {plugin.get_info()}")
        
        # Тестируем функции плагина
        test_list = [1, 2, 3, 4, 5]
        test_string = "hello world"
        
        print(f"Обработка списка: {test_list} -> {plugin.process_data(test_list)}")
        print(f"Обработка строки: {test_string} -> {plugin.process_data(test_string)}")
        
        # Используем класс из плагина
        processor = plugin.DataProcessor(3)
        print(f"Процессор: {processor.process(10)} (10 * 3)")
        print(f"Статистика процессора: {processor.get_stats()}")
        
        print("\n4. Создание модуля из строки:")
        
        def create_module_from_string(code, module_name):
            """Создать модуль из строки кода"""
            module = types.ModuleType(module_name)
            module.__file__ = f"<string:{module_name}>"
            
            # Выполняем код в контексте модуля
            exec(code, module.__dict__)
            
            # Регистрируем модуль
            sys.modules[module_name] = module
            
            return module
        
        # Код для динамического модуля
        dynamic_code = '''
"""
Динамически созданный модуль
"""

def fibonacci(n):
    """Вычислить последовательность Фибоначчи"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def factorial(n):
    """Вычислить факториал"""
    if n <= 1:
        return 1
    return n * factorial(n-1)

class MathOperations:
    """Математические операции"""
    
    @staticmethod
    def gcd(a, b):
        """Наибольший общий делитель"""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a, b):
        """Наименьшее общее кратное"""
        return abs(a * b) // MathOperations.gcd(a, b)

# Константы модуля
PI = 3.14159265359
E = 2.71828182846

print(f"Динамический модуль {__name__} создан")
'''
        
        # Создаем модуль
        dynamic_module = create_module_from_string(dynamic_code, "dynamic_math")
        
        print(f"Создан динамический модуль: {dynamic_module.__name__}")
        
        # Тестируем динамический модуль
        print(f"Фибоначчи(10): {dynamic_module.fibonacci(10)}")
        print(f"Факториал(5): {dynamic_module.factorial(5)}")
        
        math_ops = dynamic_module.MathOperations()
        print(f"НОД(48, 18): {math_ops.gcd(48, 18)}")
        print(f"НОК(12, 15): {math_ops.lcm(12, 15)}")
        print(f"Константы: PI={dynamic_module.PI}, E={dynamic_module.E}")
        
        print("\n5. Проверка загруженных модулей:")
        
        # Проверяем, что модули зарегистрированы в sys.modules
        dynamic_modules = ['demo_plugin', 'dynamic_math']
        
        for module_name in dynamic_modules:
            if module_name in sys.modules:
                module = sys.modules[module_name]
                print(f"✅ Модуль {module_name} в sys.modules")
                print(f"   Файл: {getattr(module, '__file__', 'не определен')}")
                print(f"   Атрибуты: {len([a for a in dir(module) if not a.startswith('_')])}")
        
        print("\n6. Перезагрузка модуля:")
        
        # Изменяем код плагина
        updated_plugin_code = plugin_code.replace(
            'return [item * 2 for item in data]',
            'return [item * 3 for item in data]'
        )
        
        with open(plugin_path, 'w') as f:
            f.write(updated_plugin_code)
        
        # Перезагружаем модуль
        importlib.reload(plugin)
        
        print("Модуль перезагружен с изменениями")
        print(f"Обновленная обработка: {test_list} -> {plugin.process_data(test_list)}")
        
    finally:
        # Очищаем
        sys.path.remove(temp_dir)
        
        # Удаляем модули из sys.modules
        modules_to_remove = ['demo_plugin', 'dynamic_math']
        for module_name in modules_to_remove:
            if module_name in sys.modules:
                del sys.modules[module_name]
        
        shutil.rmtree(temp_dir)
        print("\nВременные файлы и модули очищены")


def example_04_plugin_system():
    """
    Пример 4: Система плагинов
    
    Демонстрирует создание гибкой системы плагинов с автоматической
    регистрацией, загрузкой и выполнением плагинов.
    """
    print("=== Пример 4: Система плагинов ===")
    
    temp_dir = tempfile.mkdtemp()
    plugins_dir = os.path.join(temp_dir, "plugins")
    os.makedirs(plugins_dir)
    sys.path.insert(0, temp_dir)
    
    try:
        print("1. Создание базового интерфейса плагина:")
        
        # Базовый класс для всех плагинов
        from abc import ABC, abstractmethod
        
        class Plugin(ABC):
            """Базовый класс для всех плагинов"""
            
            @property
            @abstractmethod
            def name(self) -> str:
                """Имя плагина"""
                pass
            
            @property
            @abstractmethod
            def version(self) -> str:
                """Версия плагина"""
                pass
            
            @property
            @abstractmethod
            def description(self) -> str:
                """Описание плагина"""
                pass
            
            @abstractmethod
            def execute(self, *args, **kwargs) -> Any:
                """Выполнить основную функцию плагина"""
                pass
            
            def initialize(self):
                """Инициализация плагина (опционально)"""
                pass
            
            def cleanup(self):
                """Очистка ресурсов плагина (опционально)"""
                pass
        
        print("2. Создание менеджера плагинов:")
        
        class PluginManager:
            """Менеджер плагинов"""
            
            def __init__(self, plugin_directory: str):
                self.plugin_directory = plugin_directory
                self.plugins = {}
                self.loaded_modules = {}
            
            def load_plugins(self):
                """Загрузить все плагины из директории"""
                if not os.path.exists(self.plugin_directory):
                    print(f"Директория плагинов не найдена: {self.plugin_directory}")
                    return
                
                print(f"Поиск плагинов в: {self.plugin_directory}")
                
                for filename in os.listdir(self.plugin_directory):
                    if filename.endswith('.py') and not filename.startswith('__'):
                        self._load_plugin_file(filename)
            
            def _load_plugin_file(self, filename: str):
                """Загрузить один файл плагина"""
                plugin_path = os.path.join(self.plugin_directory, filename)
                module_name = f"plugin_{filename[:-3]}"
                
                try:
                    # Загружаем модуль
                    spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                    module = importlib.util.module_from_spec(spec)
                    self.loaded_modules[module_name] = module
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    
                    # Ищем классы плагинов в модуле
                    for name in dir(module):
                        obj = getattr(module, name)
                        if (isinstance(obj, type) and 
                            issubclass(obj, Plugin) and 
                            obj is not Plugin):
                            
                            try:
                                plugin_instance = obj()
                                plugin_instance.initialize()
                                self.plugins[plugin_instance.name] = plugin_instance
                                
                                print(f"✅ Загружен плагин: {plugin_instance.name} v{plugin_instance.version}")
                                print(f"   Описание: {plugin_instance.description}")
                                
                            except Exception as e:
                                print(f"❌ Ошибка инициализации плагина {name}: {e}")
                
                except Exception as e:
                    print(f"❌ Ошибка загрузки файла {filename}: {e}")
            
            def get_plugin(self, name: str) -> Optional[Plugin]:
                """Получить плагин по имени"""
                return self.plugins.get(name)
            
            def list_plugins(self) -> List[str]:
                """Список всех загруженных плагинов"""
                return list(self.plugins.keys())
            
            def execute_plugin(self, name: str, *args, **kwargs) -> Any:
                """Выполнить плагин"""
                plugin = self.get_plugin(name)
                if plugin:
                    try:
                        result = plugin.execute(*args, **kwargs)
                        return {
                            'success': True,
                            'result': result,
                            'plugin': name
                        }
                    except Exception as e:
                        return {
                            'success': False,
                            'error': str(e),
                            'plugin': name
                        }
                else:
                    return {
                        'success': False,
                        'error': f'Плагин {name} не найден'
                    }
            
            def reload_plugin(self, name: str):
                """Перезагрузить плагин"""
                if name in self.plugins:
                    plugin = self.plugins[name]
                    plugin.cleanup()
                    del self.plugins[name]
                
                # Найти и перезагрузить соответствующий модуль
                for module_name, module in self.loaded_modules.items():
                    if hasattr(module, name) or any(
                        hasattr(getattr(module, attr), 'name', None) and 
                        getattr(getattr(module, attr), 'name', None) == name
                        for attr in dir(module)
                        if not attr.startswith('_')
                    ):
                        importlib.reload(module)
                        self._extract_plugins_from_module(module)
                        break
            
            def unload_all(self):
                """Выгрузить все плагины"""
                for plugin in self.plugins.values():
                    plugin.cleanup()
                self.plugins.clear()
                
                # Удаляем модули из sys.modules
                for module_name in self.loaded_modules:
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                self.loaded_modules.clear()
        
        print("3. Создание примеров плагинов:")
        
        # Плагин для математических операций
        math_plugin_code = '''
from abc import ABC, abstractmethod

class Plugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @property
    @abstractmethod
    def version(self) -> str: pass
    
    @property
    @abstractmethod
    def description(self) -> str: pass
    
    @abstractmethod
    def execute(self, *args, **kwargs): pass
    
    def initialize(self): pass
    def cleanup(self): pass

class MathPlugin(Plugin):
    """Плагин математических операций"""
    
    @property
    def name(self) -> str:
        return "math_operations"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Выполняет основные математические операции"
    
    def execute(self, operation: str, a: float, b: float = None) -> float:
        """Выполнить математическую операцию"""
        operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else None,
            'power': lambda x, y: x ** y,
            'sqrt': lambda x, y=None: x ** 0.5,
            'abs': lambda x, y=None: abs(x)
        }
        
        func = operations.get(operation)
        if not func:
            raise ValueError(f"Неизвестная операция: {operation}")
        
        if operation in ['sqrt', 'abs']:
            return func(a)
        elif b is not None:
            return func(a, b)
        else:
            raise ValueError(f"Операция {operation} требует два аргумента")
'''
        
        # Плагин для работы со строками
        string_plugin_code = '''
from abc import ABC, abstractmethod
import re

class Plugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @property
    @abstractmethod
    def version(self) -> str: pass
    
    @property
    @abstractmethod
    def description(self) -> str: pass
    
    @abstractmethod
    def execute(self, *args, **kwargs): pass
    
    def initialize(self): pass
    def cleanup(self): pass

class StringPlugin(Plugin):
    """Плагин для работы со строками"""
    
    @property
    def name(self) -> str:
        return "string_operations"
    
    @property
    def version(self) -> str:
        return "1.2.0"
    
    @property
    def description(self) -> str:
        return "Выполняет операции со строками"
    
    def execute(self, operation: str, text: str, *args, **kwargs) -> str:
        """Выполнить операцию со строкой"""
        operations = {
            'uppercase': lambda t: t.upper(),
            'lowercase': lambda t: t.lower(),
            'reverse': lambda t: t[::-1],
            'capitalize': lambda t: t.capitalize(),
            'title': lambda t: t.title(),
            'count_words': lambda t: len(t.split()),
            'remove_spaces': lambda t: t.replace(' ', ''),
            'count_chars': lambda t: len(t),
            'extract_numbers': lambda t: re.findall(r'\\d+', t)
        }
        
        func = operations.get(operation)
        if not func:
            raise ValueError(f"Неизвестная операция: {operation}")
        
        return func(text)
'''
        
        # Плагин для форматирования данных
        formatter_plugin_code = '''
from abc import ABC, abstractmethod
from datetime import datetime
import json

class Plugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @property
    @abstractmethod
    def version(self) -> str: pass
    
    @property
    @abstractmethod
    def description(self) -> str: pass
    
    @abstractmethod
    def execute(self, *args, **kwargs): pass
    
    def initialize(self): pass
    def cleanup(self): pass

class FormatterPlugin(Plugin):
    """Плагин для форматирования данных"""
    
    @property
    def name(self) -> str:
        return "data_formatter"
    
    @property
    def version(self) -> str:
        return "2.0.0"
    
    @property
    def description(self) -> str:
        return "Форматирует различные типы данных"
    
    def initialize(self):
        """Инициализация плагина"""
        self.formats_used = {}
        print("FormatterPlugin инициализирован")
    
    def cleanup(self):
        """Очистка ресурсов"""
        print(f"FormatterPlugin завершил работу. Использованных форматов: {len(self.formats_used)}")
    
    def execute(self, format_type: str, data, **options):
        """Форматировать данные"""
        # Отслеживаем использование форматов
        self.formats_used[format_type] = self.formats_used.get(format_type, 0) + 1
        
        formatters = {
            'json': self._format_json,
            'currency': self._format_currency,
            'date': self._format_date,
            'percentage': self._format_percentage,
            'table': self._format_table
        }
        
        formatter = formatters.get(format_type)
        if not formatter:
            raise ValueError(f"Неизвестный формат: {format_type}")
        
        return formatter(data, **options)
    
    def _format_json(self, data, indent=2, **kwargs):
        """Форматировать как JSON"""
        return json.dumps(data, indent=indent, ensure_ascii=False)
    
    def _format_currency(self, amount, currency="RUB", **kwargs):
        """Форматировать как валюту"""
        return f"{amount:.2f} {currency}"
    
    def _format_date(self, date_obj, format_str="%Y-%m-%d %H:%M:%S", **kwargs):
        """Форматировать дату"""
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime(format_str)
    
    def _format_percentage(self, value, decimals=2, **kwargs):
        """Форматировать как процент"""
        return f"{value:.{decimals}f}%"
    
    def _format_table(self, data, headers=None, **kwargs):
        """Форматировать как таблицу"""
        if not data:
            return "Нет данных"
        
        if headers is None:
            if isinstance(data[0], dict):
                headers = list(data[0].keys())
            else:
                headers = [f"Колонка {i+1}" for i in range(len(data[0]))]
        
        # Простое табличное форматирование
        result = " | ".join(headers) + "\\n"
        result += "-" * len(result) + "\\n"
        
        for row in data:
            if isinstance(row, dict):
                row_data = [str(row.get(h, "")) for h in headers]
            else:
                row_data = [str(cell) for cell in row]
            result += " | ".join(row_data) + "\\n"
        
        return result
'''
        
        # Сохраняем плагины в файлы
        plugins_code = [
            ("math_plugin.py", math_plugin_code),
            ("string_plugin.py", string_plugin_code),
            ("formatter_plugin.py", formatter_plugin_code)
        ]
        
        for filename, code in plugins_code:
            plugin_path = os.path.join(plugins_dir, filename)
            with open(plugin_path, 'w') as f:
                f.write(code)
        
        print("4. Тестирование системы плагинов:")
        
        # Создаем менеджер плагинов
        plugin_manager = PluginManager(plugins_dir)
        
        # Загружаем плагины
        plugin_manager.load_plugins()
        
        print(f"\nЗагружено плагинов: {len(plugin_manager.list_plugins())}")
        print(f"Список плагинов: {plugin_manager.list_plugins()}")
        
        print("\n5. Тестирование плагинов:")
        
        # Тестируем математический плагин
        print("\nМатематические операции:")
        math_tests = [
            ('add', 10, 5),
            ('multiply', 7, 8),
            ('power', 2, 10),
            ('sqrt', 16),
            ('divide', 20, 4)
        ]
        
        for operation, a, *args in math_tests:
            result = plugin_manager.execute_plugin('math_operations', operation, a, *args)
            if result['success']:
                if args:
                    print(f"  {a} {operation} {args[0]} = {result['result']}")
                else:
                    print(f"  {operation}({a}) = {result['result']}")
            else:
                print(f"  Ошибка: {result['error']}")
        
        # Тестируем строковый плагин
        print("\nОперации со строками:")
        string_tests = [
            ('uppercase', 'hello world'),
            ('reverse', 'Python'),
            ('count_words', 'Это строка из пяти слов'),
            ('extract_numbers', 'Телефон: +7-800-123-45-67'),
            ('title', 'заголовок строки')
        ]
        
        for operation, text in string_tests:
            result = plugin_manager.execute_plugin('string_operations', operation, text)
            if result['success']:
                print(f"  {operation}('{text}') = {result['result']}")
            else:
                print(f"  Ошибка: {result['error']}")
        
        # Тестируем плагин форматирования
        print("\nФорматирование данных:")
        
        # JSON форматирование
        test_data = {"name": "Python", "version": 3.12, "features": ["динамическая типизация", "ООП"]}
        json_result = plugin_manager.execute_plugin('data_formatter', 'json', test_data, indent=4)
        if json_result['success']:
            print("JSON форматирование:")
            print(json_result['result'])
        
        # Валютное форматирование
        currency_result = plugin_manager.execute_plugin('data_formatter', 'currency', 1234.56, currency='USD')
        if currency_result['success']:
            print(f"Валюта: {currency_result['result']}")
        
        # Табличное форматирование
        table_data = [
            {"name": "Алиса", "age": 25, "city": "Москва"},
            {"name": "Боб", "age": 30, "city": "СПб"},
            {"name": "Чарли", "age": 35, "city": "Казань"}
        ]
        table_result = plugin_manager.execute_plugin('data_formatter', 'table', table_data)
        if table_result['success']:
            print("Табличное форматирование:")
            print(table_result['result'])
        
        print("\n6. Информация о плагинах:")
        
        for plugin_name in plugin_manager.list_plugins():
            plugin = plugin_manager.get_plugin(plugin_name)
            if plugin:
                print(f"\nПлагин: {plugin.name}")
                print(f"  Версия: {plugin.version}")
                print(f"  Описание: {plugin.description}")
        
    finally:
        # Очищаем
        plugin_manager.unload_all()
        sys.path.remove(temp_dir)
        shutil.rmtree(temp_dir)
        print("\nСистема плагинов выгружена, временные файлы удалены")


def example_05_advanced_import_techniques():
    """
    Пример 5: Продвинутые техники импорта
    
    Демонстрирует сложные случаи импорта, оптимизацию производительности,
    работу с namespace пакетами и решение проблем импорта.
    """
    print("=== Пример 5: Продвинутые техники импорта ===")
    
    print("1. Ленивый импорт для оптимизации производительности:")
    
    class LazyImporter:
        """Ленивый импортер для тяжелых библиотек"""
        
        def __init__(self):
            self._modules = {}
        
        def __getattr__(self, name):
            if name not in self._modules:
                print(f"Выполняется ленивый импорт: {name}")
                
                # Мапинг имен на модули
                module_map = {
                    'json': 'json',
                    'datetime': 'datetime',
                    'collections': 'collections',
                    'itertools': 'itertools',
                    'functools': 'functools',
                    'os': 'os',
                    'sys': 'sys',
                    'math': 'math'
                }
                
                module_name = module_map.get(name, name)
                
                try:
                    self._modules[name] = importlib.import_module(module_name)
                except ImportError:
                    raise AttributeError(f"Модуль {name} недоступен")
            
            return self._modules[name]
    
    # Использование ленивого импорта
    libs = LazyImporter()
    
    print("Ленивый импортер создан, модули еще не загружены")
    
    # Модули импортируются только при первом обращении
    current_time = libs.datetime.datetime.now()
    print(f"Текущее время (через ленивый импорт): {current_time}")
    
    data = {"test": "data"}
    json_string = libs.json.dumps(data)
    print(f"JSON (через ленивый импорт): {json_string}")
    
    print("\n2. Условный импорт и fallback решения:")
    
    def get_optimized_module(primary_modules, fallback_module):
        """Получить оптимизированный модуль с fallback"""
        for module_name in primary_modules:
            try:
                module = importlib.import_module(module_name)
                print(f"Используется оптимизированный модуль: {module_name}")
                return module, module_name
            except ImportError:
                continue
        
        # Fallback на стандартный модуль
        try:
            module = importlib.import_module(fallback_module)
            print(f"Используется fallback модуль: {fallback_module}")
            return module, fallback_module
        except ImportError:
            raise ImportError(f"Ни один из модулей недоступен: {primary_modules + [fallback_module]}")
    
    # Пример: быстрые JSON библиотеки
    json_module, json_name = get_optimized_module(['ujson', 'orjson'], 'json')
    test_data = {"name": "Python", "numbers": [1, 2, 3, 4, 5]}
    serialized = json_module.dumps(test_data)
    print(f"Сериализация через {json_name}: {serialized}")
    
    print("\n3. Импорт с версионной совместимостью:")
    
    def import_with_version_check():
        """Импорт с проверкой версии Python"""
        import sys
        
        if sys.version_info >= (3, 8):
            try:
                from functools import cached_property
                print("Используется cached_property из Python 3.8+")
                return cached_property
            except ImportError:
                pass
        
        # Fallback реализация для старых версий
        print("Используется собственная реализация cached_property")
        
        class cached_property:
            """Простая реализация cached_property"""
            
            def __init__(self, func):
                self.func = func
                self.attrname = None
                self.__doc__ = func.__doc__
            
            def __set_name__(self, owner, name):
                self.attrname = name
            
            def __get__(self, instance, owner=None):
                if instance is None:
                    return self
                if self.attrname is None:
                    raise TypeError("cached_property should be used as a decorator")
                
                val = self.func(instance)
                setattr(instance, self.attrname, val)
                return val
        
        return cached_property
    
    cached_property_impl = import_with_version_check()
    
    # Демонстрация использования
    class ExampleClass:
        def __init__(self, value):
            self.value = value
        
        @cached_property_impl
        def expensive_computation(self):
            print("Выполняется дорогое вычисление...")
            return self.value ** 2 + self.value * 10
    
    obj = ExampleClass(5)
    print(f"Первый вызов: {obj.expensive_computation}")  # Вычисляется
    print(f"Второй вызов: {obj.expensive_computation}")   # Из кеша
    
    print("\n4. Проверка доступности модулей:")
    
    def check_module_availability():
        """Проверить доступность различных модулей"""
        modules_to_check = [
            ('json', 'Работа с JSON'),
            ('datetime', 'Работа с датами'),
            ('requests', 'HTTP клиент'),
            ('numpy', 'Численные вычисления'),
            ('pandas', 'Анализ данных'),
            ('nonexistent_module', 'Несуществующий модуль')
        ]
        
        available_modules = {}
        
        for module_name, description in modules_to_check:
            try:
                module = importlib.import_module(module_name)
                version = getattr(module, '__version__', 'неизвестна')
                available_modules[module_name] = {
                    'available': True,
                    'version': version,
                    'description': description,
                    'file': getattr(module, '__file__', 'не определен')
                }
                status = "✅"
            except ImportError as e:
                available_modules[module_name] = {
                    'available': False,
                    'error': str(e),
                    'description': description
                }
                status = "❌"
            
            print(f"{status} {module_name}: {description}")
            
            if available_modules[module_name]['available']:
                info = available_modules[module_name]
                print(f"    Версия: {info['version']}")
                if 'file' in info and info['file'] != 'не определен':
                    print(f"    Файл: {Path(info['file']).name}")
        
        return available_modules
    
    available = check_module_availability()
    
    print(f"\nДоступно модулей: {sum(1 for m in available.values() if m['available'])}")
    print(f"Недоступно модулей: {sum(1 for m in available.values() if not m['available'])}")
    
    print("\n5. Управление путями импорта:")
    
    def demonstrate_path_management():
        """Демонстрация управления sys.path"""
        print(f"Текущее количество путей: {len(sys.path)}")
        print("Первые 5 путей:")
        for i, path in enumerate(sys.path[:5]):
            print(f"  {i+1}. {path}")
        
        # Временное добавление пути
        temp_path = "/tmp/custom_modules"
        
        print(f"\nДобавляем временный путь: {temp_path}")
        sys.path.insert(0, temp_path)
        print(f"Новое количество путей: {len(sys.path)}")
        
        # Контекстный менеджер для временного пути
        from contextlib import contextmanager
        
        @contextmanager
        def temporary_path(path):
            """Временно добавить путь в sys.path"""
            sys.path.insert(0, path)
            try:
                yield
            finally:
                if path in sys.path:
                    sys.path.remove(path)
        
        # Использование контекстного менеджера
        test_path = "/tmp/test_modules"
        print(f"\nИспользование контекстного менеджера для {test_path}")
        
        with temporary_path(test_path):
            print(f"Внутри контекста: {len(sys.path)} путей")
            print(f"Первый путь: {sys.path[0]}")
        
        print(f"После контекста: {len(sys.path)} путей")
        
        # Удаляем ранее добавленный путь
        if temp_path in sys.path:
            sys.path.remove(temp_path)
            print(f"Временный путь удален: {len(sys.path)} путей")
    
    demonstrate_path_management()
    
    print("\n6. Анализ зависимостей модуля:")
    
    def analyze_module_dependencies(module_name):
        """Анализ зависимостей модуля"""
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            print(f"Не удалось импортировать {module_name}: {e}")
            return
        
        print(f"\nАнализ модуля: {module_name}")
        print(f"Файл: {getattr(module, '__file__', 'встроенный')}")
        print(f"Пакет: {getattr(module, '__package__', 'нет')}")
        
        # Анализ атрибутов
        attributes = dir(module)
        functions = []
        classes = []
        modules = []
        others = []
        
        for attr_name in attributes:
            if attr_name.startswith('_'):
                continue
            
            try:
                attr = getattr(module, attr_name)
                if callable(attr) and hasattr(attr, '__name__'):
                    functions.append(attr_name)
                elif isinstance(attr, type):
                    classes.append(attr_name)
                elif hasattr(attr, '__file__'):
                    modules.append(attr_name)
                else:
                    others.append(attr_name)
            except:
                pass
        
        print(f"Функции ({len(functions)}): {', '.join(functions[:5])}{'...' if len(functions) > 5 else ''}")
        print(f"Классы ({len(classes)}): {', '.join(classes[:5])}{'...' if len(classes) > 5 else ''}")
        print(f"Модули ({len(modules)}): {', '.join(modules[:3])}{'...' if len(modules) > 3 else ''}")
        print(f"Другое ({len(others)}): {', '.join(others[:5])}{'...' if len(others) > 5 else ''}")
    
    # Анализируем несколько стандартных модулей
    modules_to_analyze = ['json', 'datetime', 'collections']
    
    for module_name in modules_to_analyze:
        analyze_module_dependencies(module_name)
    
    print("\n7. Измерение времени импорта:")
    
    import time
    
    def measure_import_time(module_name, reload=False):
        """Измерить время импорта модуля"""
        if reload and module_name in sys.modules:
            del sys.modules[module_name]
        
        start_time = time.perf_counter()
        
        try:
            module = importlib.import_module(module_name)
            end_time = time.perf_counter()
            
            import_time = (end_time - start_time) * 1000
            
            return {
                'success': True,
                'time_ms': import_time,
                'module': module
            }
        except ImportError as e:
            end_time = time.perf_counter()
            return {
                'success': False,
                'time_ms': (end_time - start_time) * 1000,
                'error': str(e)
            }
    
    print("\nВремя импорта различных модулей:")
    
    modules_to_time = ['json', 'datetime', 'collections', 'itertools', 'os', 'sys']
    
    for module_name in modules_to_time:
        result = measure_import_time(module_name)
        if result['success']:
            print(f"✅ {module_name}: {result['time_ms']:.2f} мс")
        else:
            print(f"❌ {module_name}: {result['time_ms']:.2f} мс (ошибка)")
    
    print("\nПримечание: время может варьироваться в зависимости от системы и кеша")


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Создание и использование простых модулей", example_01_basic_module_creation),
        ("Создание и использование пакетов", example_02_package_creation),
        ("Динамический импорт модулей", example_03_dynamic_imports),
        ("Система плагинов", example_04_plugin_system),
        ("Продвинутые техники импорта", example_05_advanced_import_techniques),
    ]
    
    print("📦 Примеры: Модули и пакеты в Python")
    print("=" * 70)
    print("Эти примеры демонстрируют:")
    print("- Создание и структурирование модулей")
    print("- Организацию кода в пакеты")
    print("- Различные способы импорта")
    print("- Динамическую загрузку модулей")
    print("- Создание системы плагинов")
    print("- Оптимизацию импортов")
    print("=" * 70)
    
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