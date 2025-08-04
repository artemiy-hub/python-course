# Теория: Модули и пакеты в Python

## 🎯 Цель раздела

Модули и пакеты - это основа структурирования кода в Python. Они позволяют разбивать программы на логические части, переиспользовать код и создавать масштабируемые приложения. Этот раздел охватывает все аспекты работы с модулями и пакетами в Python.

## 📋 Содержание

1. [Основы модулей](#основы-модулей)
2. [Импорт модулей](#импорт-модулей)
3. [Создание модулей](#создание-модулей)
4. [Пакеты](#пакеты)
5. [Пути поиска модулей](#пути-поиска-модулей)
6. [Динамический импорт](#динамический-импорт)
7. [Атрибуты модулей](#атрибуты-модулей)
8. [Управление зависимостями](#управление-зависимостями)
9. [Лучшие практики](#лучшие-практики)

---

## 📦 Основы модулей

### Что такое модуль?

**Модуль** - это файл с расширением `.py`, содержащий код Python. Модули позволяют:
- Организовать код в логические единицы
- Переиспользовать код в разных проектах
- Создавать пространства имен
- Разделять ответственность между компонентами

```python
# math_utils.py - простой модуль
"""
Модуль математических утилит
"""

PI = 3.14159265359

def square(x):
    """Возвести в квадрат"""
    return x * x

def circle_area(radius):
    """Площадь круга"""
    return PI * square(radius)

def factorial(n):
    """Факториал числа"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Переменные модуля
_private_constant = "Это приватная константа"
PUBLIC_CONSTANT = "Это публичная константа"

# Код, который выполняется при импорте
print(f"Модуль {__name__} загружен")
```

### Типы модулей

```python
# 1. Встроенные модули (написаны на C, встроены в интерпретатор)
import sys
import os
import math

print("Встроенные модули:")
print(f"sys.version: {sys.version_info}")
print(f"os.name: {os.name}")
print(f"math.pi: {math.pi}")

# 2. Стандартная библиотека (написаны на Python, поставляются с интерпретатором)
import json
import datetime
import collections

print("\nСтандартная библиотека:")
data = {"name": "Python", "version": 3.12}
print(f"JSON: {json.dumps(data)}")
print(f"Дата: {datetime.datetime.now()}")
print(f"Counter: {collections.Counter(['a', 'b', 'a'])}")

# 3. Сторонние модули (устанавливаются через pip)
try:
    import requests
    import numpy as np
    print("\nСторонние модули доступны")
except ImportError as e:
    print(f"\nСторонние модули недоступны: {e}")

# 4. Пользовательские модули
# import math_utils  # Наш собственный модуль
```

### Когда создавать модули

```python
# Создавайте модули когда:

# 1. Код становится слишком длинным (>500-1000 строк)
# main.py (до рефакторинга)
class User:
    pass

class Product:
    pass

class Order:
    pass

def validate_email(email):
    pass

def send_email(to, subject, body):
    pass

def connect_to_database():
    pass

def create_user(user_data):
    pass

# main.py (после рефакторинга)
from models import User, Product, Order
from validators import validate_email
from email_service import send_email
from database import connect_to_database, create_user

# 2. Логически связанные функции можно сгруппировать
# string_utils.py
def capitalize_words(text):
    """Сделать первую букву каждого слова заглавной"""
    return ' '.join(word.capitalize() for word in text.split())

def remove_duplicates(text):
    """Удалить дублирующиеся символы"""
    return ''.join(dict.fromkeys(text))

def count_words(text):
    """Подсчитать количество слов"""
    return len(text.split())

# 3. Код используется в нескольких местах
# config.py
DATABASE_URL = "postgresql://localhost:5432/mydb"
API_KEY = "your-api-key-here"
DEBUG = True

# 4. Нужно создать переиспользуемый компонент
# logger.py
import logging

def setup_logger(name, level=logging.INFO):
    """Настроить логгер"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
```

---

## 📥 Импорт модулей

### Основные способы импорта

```python
# 1. Импорт всего модуля
import math
import os.path
import xml.etree.ElementTree

# Использование
result = math.sqrt(16)
filepath = os.path.join("folder", "file.txt")

# 2. Импорт с псевдонимом
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Использование
array = np.array([1, 2, 3])
df = pd.DataFrame({'a': [1, 2, 3]})

# 3. Импорт конкретных функций/классов
from math import sqrt, pi, sin, cos
from os.path import join, exists, dirname
from datetime import datetime, timedelta

# Использование (без префикса модуля)
result = sqrt(16)
now = datetime.now()

# 4. Импорт с псевдонимом
from numpy import array as np_array
from pandas import DataFrame as DF

# 5. Импорт всего содержимого (не рекомендуется)
from math import *  # Импортирует все публичные имена

# Почему не рекомендуется:
# - Засоряет пространство имен
# - Может перезаписать существующие имена
# - Делает код менее читаемым
```

### Условный импорт

```python
# Импорт с обработкой ошибок
try:
    import ujson as json  # Быстрая библиотека JSON
except ImportError:
    import json  # Стандартная библиотека

try:
    from PIL import Image  # Pillow
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def process_image(image_path):
    if not HAS_PIL:
        raise RuntimeError("PIL/Pillow не установлен")
    return Image.open(image_path)

# Условный импорт для совместимости версий
import sys

if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    # Простая реализация для старых версий
    class cached_property:
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
                raise TypeError("cached_property must be used as a decorator")
            val = self.func(instance)
            setattr(instance, self.attrname, val)
            return val

# Платформо-зависимый импорт
import platform

if platform.system() == "Windows":
    import winsound
    def beep():
        winsound.Beep(1000, 500)
elif platform.system() == "Darwin":  # macOS
    import subprocess
    def beep():
        subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])
else:  # Linux
    def beep():
        print("\a")  # ASCII bell
```

### Отложенный импорт

```python
# Импорт только при необходимости (lazy import)
def get_data_from_api():
    import requests  # Импорт только при вызове функции
    
    response = requests.get("https://api.example.com/data")
    return response.json()

def process_large_dataset(data):
    import pandas as pd  # Тяжелая библиотека импортируется только здесь
    
    df = pd.DataFrame(data)
    return df.describe()

# Импорт в классе
class DataProcessor:
    def __init__(self):
        self._np = None
    
    @property
    def np(self):
        if self._np is None:
            import numpy as np
            self._np = np
        return self._np
    
    def process(self, data):
        return self.np.array(data).mean()

# Контекстный импорт
def with_tqdm():
    """Контекстный менеджер для прогресс-бара"""
    try:
        from tqdm import tqdm
        return tqdm
    except ImportError:
        # Заглушка, если tqdm не установлен
        class DummyTqdm:
            def __init__(self, iterable, *args, **kwargs):
                self.iterable = iterable
            def __iter__(self):
                return iter(self.iterable)
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return DummyTqdm

# Использование
for item in with_tqdm()(range(100), desc="Processing"):
    # Обработка элемента
    pass
```

---

## 🛠️ Создание модулей

### Структура модуля

```python
# example_module.py
"""
Пример хорошо структурированного модуля

Этот модуль демонстрирует лучшие практики создания модулей:
- Документация
- Импорты
- Константы
- Функции
- Классы
- Исполняемый код
"""

# 1. Импорты (в порядке: стандартная библиотека, сторонние, локальные)
import os
import sys
from typing import List, Dict, Optional
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# 2. Константы и конфигурация
__version__ = "1.0.0"
__author__ = "Ваше Имя"
__email__ = "email@example.com"

# Публичные константы
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Приватные константы
_DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
_CONFIG_PATH = Path(__file__).parent / "config.json"

# 3. Исключения модуля
class ModuleError(Exception):
    """Базовое исключение модуля"""
    pass

class ConfigurationError(ModuleError):
    """Ошибка конфигурации"""
    pass

class NetworkError(ModuleError):
    """Ошибка сети"""
    pass

# 4. Приватные функции и переменные
def _load_config():
    """Загрузить конфигурацию (приватная функция)"""
    if _CONFIG_PATH.exists():
        import json
        with open(_CONFIG_PATH) as f:
            return json.load(f)
    return {}

def _validate_url(url: str) -> bool:
    """Валидация URL (приватная функция)"""
    return url.startswith(('http://', 'https://'))

# Приватные переменные модуля
_config = _load_config()
_session = None

# 5. Публичные функции
def init_session(timeout: int = DEFAULT_TIMEOUT) -> None:
    """
    Инициализировать HTTP сессию
    
    Args:
        timeout: Таймаут в секундах
        
    Raises:
        ConfigurationError: Если requests недоступен
    """
    global _session
    
    if requests is None:
        raise ConfigurationError("Библиотека requests не установлена")
    
    _session = requests.Session()
    _session.timeout = timeout

def get_data(url: str, params: Optional[Dict] = None) -> Dict:
    """
    Получить данные по URL
    
    Args:
        url: URL для запроса
        params: Параметры запроса
        
    Returns:
        Данные в формате JSON
        
    Raises:
        NetworkError: При ошибке сети
        ModuleError: При других ошибках
    """
    if not _validate_url(url):
        raise ModuleError(f"Недопустимый URL: {url}")
    
    if _session is None:
        init_session()
    
    try:
        response = _session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise NetworkError(f"Ошибка сети: {e}")

# 6. Классы
class DataProcessor:
    """
    Класс для обработки данных
    
    Attributes:
        name: Имя процессора
        config: Конфигурация процессора
    """
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or _config.copy()
        self._cache = {}
    
    def process(self, data: List[Dict]) -> List[Dict]:
        """
        Обработать данные
        
        Args:
            data: Список словарей для обработки
            
        Returns:
            Обработанные данные
        """
        result = []
        for item in data:
            processed_item = self._process_item(item)
            result.append(processed_item)
        return result
    
    def _process_item(self, item: Dict) -> Dict:
        """Обработать один элемент (приватный метод)"""
        # Кэширование результатов
        item_id = item.get('id')
        if item_id in self._cache:
            return self._cache[item_id]
        
        # Обработка
        processed = {
            'id': item_id,
            'processed_at': str(datetime.now()),
            'data': item
        }
        
        self._cache[item_id] = processed
        return processed

# 7. Переменные уровня модуля
default_processor = None

# 8. Функции инициализации
def get_default_processor() -> DataProcessor:
    """Получить процессор по умолчанию (ленивая инициализация)"""
    global default_processor
    
    if default_processor is None:
        default_processor = DataProcessor("default")
    
    return default_processor

# 9. Код, выполняемый при импорте
if _DEBUG:
    print(f"Модуль {__name__} загружен в режиме отладки")

# 10. Код для выполнения модуля как скрипта
def main():
    """Главная функция модуля"""
    print(f"Запуск модуля {__name__} v{__version__}")
    
    # Пример использования
    try:
        processor = get_default_processor()
        test_data = [
            {'id': 1, 'value': 'test1'},
            {'id': 2, 'value': 'test2'}
        ]
        
        result = processor.process(test_data)
        print(f"Обработано {len(result)} элементов")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Управление видимостью

```python
# visibility_example.py
"""
Демонстрация управления видимостью в модуле
"""

# Все имена, начинающиеся с _, считаются приватными
_private_constant = "Приватная константа"
_private_var = 42

def _private_function():
    """Приватная функция"""
    return "Это приватная функция"

class _PrivateClass:
    """Приватный класс"""
    pass

# Публичные имена
PUBLIC_CONSTANT = "Публичная константа"
public_var = 100

def public_function():
    """Публичная функция"""
    return "Это публичная функция"

class PublicClass:
    """Публичный класс"""
    pass

# Управление экспортом через __all__
__all__ = [
    'PUBLIC_CONSTANT',
    'public_function',
    'PublicClass',
    'get_version'  # Функция, определенная ниже
]

def get_version():
    """Получить версию модуля"""
    return "1.0.0"

def helper_function():
    """
    Эта функция не включена в __all__,
    поэтому не будет импортирована при from module import *
    """
    return "Вспомогательная функция"

# Пример использования:
# from visibility_example import *
# Будут импортированы только: PUBLIC_CONSTANT, public_function, PublicClass, get_version
```

---

## 📚 Пакеты

### Что такое пакет?

**Пакет** - это директория, содержащая файл `__init__.py` и другие модули. Пакеты позволяют организовать модули в иерархическую структуру.

```
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        submodule1.py
        submodule2.py
```

### Создание пакета

```python
# mypackage/__init__.py
"""
Главный пакет приложения

Этот файл делает директорию пакетом и может содержать:
- Код инициализации пакета
- Импорты для упрощения доступа к модулям
- Определение __all__
- Настройку логирования
"""

# Версия пакета
__version__ = "1.0.0"

# Автор и метаинформация
__author__ = "Ваше Имя"
__email__ = "email@example.com"
__description__ = "Описание пакета"

# Импорты для удобного доступа
from .module1 import important_function, ImportantClass
from .module2 import utility_function
from .subpackage import SubModule

# Создание псевдонимов
quick_func = important_function

# Инициализация пакета
_initialized = False

def initialize():
    """Инициализация пакета"""
    global _initialized
    
    if _initialized:
        return
    
    print(f"Инициализация пакета {__name__} v{__version__}")
    
    # Настройка логирования
    import logging
    logging.getLogger(__name__).setLevel(logging.INFO)
    
    _initialized = True

# Автоматическая инициализация при импорте
initialize()

# Определение публичного API
__all__ = [
    'important_function',
    'ImportantClass',
    'utility_function',
    'SubModule',
    'quick_func'
]

# mypackage/module1.py
"""Первый модуль пакета"""

class ImportantClass:
    """Важный класс"""
    
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

def important_function(x, y):
    """Важная функция"""
    return x + y

# mypackage/module2.py
"""Второй модуль пакета"""

def utility_function(text):
    """Утилитарная функция"""
    return text.upper()

# mypackage/subpackage/__init__.py
"""Подпакет"""

from .submodule1 import SubModule

__all__ = ['SubModule']

# mypackage/subpackage/submodule1.py
"""Модуль в подпакете"""

class SubModule:
    """Класс из подмодуля"""
    
    def __init__(self):
        self.data = []
    
    def add_data(self, item):
        self.data.append(item)
```

### Использование пакетов

```python
# Способы импорта пакетов

# 1. Импорт всего пакета
import mypackage

# Использование
obj = mypackage.ImportantClass(42)
result = mypackage.important_function(10, 20)

# 2. Импорт конкретных модулей
from mypackage import module1, module2

# Использование
obj = module1.ImportantClass(42)
text = module2.utility_function("hello")

# 3. Импорт конкретных функций/классов
from mypackage import ImportantClass, important_function
from mypackage.subpackage import SubModule

# Использование
obj = ImportantClass(42)
result = important_function(10, 20)
sub = SubModule()

# 4. Импорт из подпакетов
from mypackage.subpackage.submodule1 import SubModule

# 5. Абсолютные vs относительные импорты
# В mypackage/module1.py:

# Абсолютный импорт (рекомендуется)
from mypackage.module2 import utility_function
from mypackage.subpackage import SubModule

# Относительный импорт
from .module2 import utility_function
from .subpackage import SubModule
from ..other_package import some_function  # На уровень вверх
```

### Namespace пакеты (PEP 420)

```python
# Namespace пакеты позволяют разделить пакет между несколькими местами
# Без файла __init__.py

# Структура:
# site-packages/
#     mycompany/
#         package1/
#             module1.py
#     /another/location/
#         mycompany/
#             package2/
#                 module2.py

# Использование:
# import mycompany.package1.module1
# import mycompany.package2.module2

# Пример создания namespace пакета:
# 1. Создаем директории без __init__.py
# 2. Python автоматически создает namespace пакет

import sys
from pathlib import Path

# Добавляем пути к namespace пакету
namespace_paths = [
    Path("/path/to/first/location"),
    Path("/path/to/second/location")
]

for path in namespace_paths:
    if path.exists():
        sys.path.append(str(path))

# Теперь можно импортировать из namespace пакета
# import mycompany.package1
# import mycompany.package2
```

---

## 🔍 Пути поиска модулей

### Как Python находит модули

```python
import sys
import os

print("Пути поиска модулей (sys.path):")
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")

# sys.path содержит:
# 1. Директория с запущенным скриптом
# 2. PYTHONPATH (переменная окружения)
# 3. Стандартные пути библиотек
# 4. Site-packages (сторонние пакеты)

print("\nПеременная PYTHONPATH:")
pythonpath = os.environ.get('PYTHONPATH', 'Не установлена')
print(pythonpath)

# Динамическое добавление путей
sys.path.insert(0, '/path/to/my/modules')  # В начало списка
sys.path.append('/another/path')           # В конец списка

# Временное добавление пути
import contextlib

@contextlib.contextmanager
def add_to_path(path):
    """Контекстный менеджер для временного добавления пути"""
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path.remove(path)

# Использование
with add_to_path('/temp/modules'):
    import temp_module  # Модуль из временного пути
```

### Поиск модулей в runtime

```python
import importlib.util
import os

def find_module(module_name, search_paths=None):
    """
    Найти модуль в указанных путях
    
    Args:
        module_name: Имя модуля
        search_paths: Список путей для поиска
        
    Returns:
        Путь к модулю или None
    """
    if search_paths is None:
        search_paths = sys.path
    
    for path in search_paths:
        # Поиск .py файла
        module_path = os.path.join(path, f"{module_name}.py")
        if os.path.isfile(module_path):
            return module_path
        
        # Поиск пакета
        package_path = os.path.join(path, module_name, "__init__.py")
        if os.path.isfile(package_path):
            return os.path.dirname(package_path)
    
    return None

def module_exists(module_name):
    """Проверить существование модуля"""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def get_module_path(module_name):
    """Получить путь к модулю"""
    spec = importlib.util.find_spec(module_name)
    if spec and spec.origin:
        return spec.origin
    return None

# Примеры использования
print("Поиск модулей:")
print(f"os модуль существует: {module_exists('os')}")
print(f"несуществующий модуль: {module_exists('nonexistent_module')}")
print(f"Путь к json модулю: {get_module_path('json')}")
print(f"Путь к math модулю: {get_module_path('math')}")

# Проверка всех доступных модулей
def list_available_modules():
    """Список всех доступных модулей"""
    import pkgutil
    
    modules = []
    for importer, modname, ispkg in pkgutil.iter_modules():
        modules.append((modname, ispkg))
    
    return sorted(modules)

# Получить первые 10 модулей
available_modules = list_available_modules()[:10]
print(f"\nПервые 10 доступных модулей:")
for name, is_package in available_modules:
    type_str = "пакет" if is_package else "модуль"
    print(f"  {name} ({type_str})")
```

---

## ⚡ Динамический импорт

### Импорт модулей во время выполнения

```python
import importlib
import sys

def import_module_by_name(module_name):
    """Импортировать модуль по имени"""
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError as e:
        print(f"Не удалось импортировать {module_name}: {e}")
        return None

# Примеры использования
math_module = import_module_by_name('math')
if math_module:
    print(f"π = {math_module.pi}")

json_module = import_module_by_name('json')
if json_module:
    data = {"key": "value"}
    print(f"JSON: {json_module.dumps(data)}")

def import_from_module(module_name, attr_name):
    """Импортировать атрибут из модуля"""
    module = import_module_by_name(module_name)
    if module and hasattr(module, attr_name):
        return getattr(module, attr_name)
    return None

# Импорт конкретных функций
sqrt_func = import_from_module('math', 'sqrt')
if sqrt_func:
    print(f"sqrt(16) = {sqrt_func(16)}")

# Условный импорт модулей
def get_json_module():
    """Получить наиболее быстрый JSON модуль"""
    for module_name in ['ujson', 'rapidjson', 'json']:
        module = import_module_by_name(module_name)
        if module:
            print(f"Используется {module_name} для JSON")
            return module
    
    raise ImportError("Ни один JSON модуль недоступен")

json_lib = get_json_module()
```

### Загрузка модулей из файлов

```python
import importlib.util
import types

def load_module_from_file(file_path, module_name=None):
    """
    Загрузить модуль из файла
    
    Args:
        file_path: Путь к .py файлу
        module_name: Имя модуля (по умолчанию - имя файла)
        
    Returns:
        Загруженный модуль
    """
    if module_name is None:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
    
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Не удалось создать спецификацию для {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    
    # Добавляем модуль в sys.modules
    sys.modules[module_name] = module
    
    # Выполняем код модуля
    spec.loader.exec_module(module)
    
    return module

def load_module_from_string(code, module_name):
    """
    Создать модуль из строки с кодом
    
    Args:
        code: Код Python в виде строки
        module_name: Имя модуля
        
    Returns:
        Созданный модуль
    """
    module = types.ModuleType(module_name)
    module.__file__ = f"<string:{module_name}>"
    
    # Выполняем код в контексте модуля
    exec(code, module.__dict__)
    
    # Добавляем в sys.modules
    sys.modules[module_name] = module
    
    return module

# Примеры использования
print("Динамическая загрузка модулей:")

# Загрузка из строки
dynamic_code = """
def hello(name):
    return f"Привет, {name}!"

PI = 3.14159

class Calculator:
    def add(self, a, b):
        return a + b
"""

dynamic_module = load_module_from_string(dynamic_code, "dynamic_math")
print(f"Функция из динамического модуля: {dynamic_module.hello('Мир')}")
print(f"Константа из динамического модуля: {dynamic_module.PI}")

calc = dynamic_module.Calculator()
print(f"Класс из динамического модуля: {calc.add(2, 3)}")

# Проверяем, что модуль добавлен в sys.modules
print(f"Динамический модуль в sys.modules: {'dynamic_math' in sys.modules}")
```

### Плагин-система

```python
import os
import inspect
from abc import ABC, abstractmethod

# Базовый класс для плагинов
class Plugin(ABC):
    """Базовый класс для всех плагинов"""
    
    @property
    @abstractmethod
    def name(self):
        """Имя плагина"""
        pass
    
    @property
    @abstractmethod
    def version(self):
        """Версия плагина"""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Выполнить функцию плагина"""
        pass

class PluginManager:
    """Менеджер плагинов"""
    
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.plugins = {}
    
    def load_plugins(self):
        """Загрузить все плагины из директории"""
        if not os.path.exists(self.plugin_dir):
            print(f"Директория плагинов не найдена: {self.plugin_dir}")
            return
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                self._load_plugin(filename)
    
    def _load_plugin(self, filename):
        """Загрузить один плагин"""
        plugin_path = os.path.join(self.plugin_dir, filename)
        module_name = f"plugin_{os.path.splitext(filename)[0]}"
        
        try:
            module = load_module_from_file(plugin_path, module_name)
            
            # Ищем классы плагинов в модуле
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, Plugin) and 
                    obj is not Plugin and 
                    hasattr(obj, 'name')):
                    
                    plugin_instance = obj()
                    self.plugins[plugin_instance.name] = plugin_instance
                    print(f"Загружен плагин: {plugin_instance.name} v{plugin_instance.version}")
        
        except Exception as e:
            print(f"Ошибка загрузки плагина {filename}: {e}")
    
    def get_plugin(self, name):
        """Получить плагин по имени"""
        return self.plugins.get(name)
    
    def list_plugins(self):
        """Список всех плагинов"""
        return list(self.plugins.keys())
    
    def execute_plugin(self, name, *args, **kwargs):
        """Выполнить плагин"""
        plugin = self.get_plugin(name)
        if plugin:
            return plugin.execute(*args, **kwargs)
        else:
            raise ValueError(f"Плагин {name} не найден")

# Пример плагина (сохранить в plugins/math_plugin.py)
class MathPlugin(Plugin):
    """Математический плагин"""
    
    @property
    def name(self):
        return "math_operations"
    
    @property
    def version(self):
        return "1.0.0"
    
    def execute(self, operation, a, b):
        """Выполнить математическую операцию"""
        operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else None
        }
        
        func = operations.get(operation)
        if func:
            return func(a, b)
        else:
            raise ValueError(f"Неизвестная операция: {operation}")

# Использование системы плагинов
plugin_manager = PluginManager("plugins")
plugin_manager.load_plugins()

print(f"Доступные плагины: {plugin_manager.list_plugins()}")

# Попытка выполнить плагин (если он загружен)
try:
    result = plugin_manager.execute_plugin("math_operations", "add", 10, 5)
    print(f"Результат выполнения плагина: {result}")
except (ValueError, FileNotFoundError) as e:
    print(f"Плагин недоступен: {e}")
```

---

## 🏷️ Атрибуты модулей

### Специальные атрибуты

```python
# module_attributes.py
"""
Демонстрация атрибутов модулей
"""

import os
import sys
import inspect

def explore_module_attributes():
    """Исследовать атрибуты текущего модуля"""
    
    print("Специальные атрибуты модуля:")
    print(f"__name__: {__name__}")           # Имя модуля
    print(f"__file__: {__file__}")           # Путь к файлу модуля
    print(f"__doc__: {__doc__}")             # Документация модуля
    print(f"__package__: {__package__}")     # Пакет, содержащий модуль
    
    # Дополнительные атрибуты
    if hasattr(sys.modules[__name__], '__version__'):
        print(f"__version__: {sys.modules[__name__].__version__}")
    
    if hasattr(sys.modules[__name__], '__author__'):
        print(f"__author__: {sys.modules[__name__].__author__}")

def get_module_info(module):
    """Получить информацию о модуле"""
    info = {
        'name': getattr(module, '__name__', 'Неизвестно'),
        'file': getattr(module, '__file__', 'Неизвестно'),
        'doc': getattr(module, '__doc__', 'Нет документации'),
        'package': getattr(module, '__package__', 'Не в пакете'),
        'version': getattr(module, '__version__', 'Версия не указана'),
        'all': getattr(module, '__all__', 'Не определено')
    }
    
    return info

def list_module_attributes(module):
    """Список всех атрибутов модуля"""
    attributes = {
        'functions': [],
        'classes': [],
        'variables': [],
        'modules': []
    }
    
    for name in dir(module):
        if name.startswith('_'):
            continue  # Пропускаем приватные атрибуты
        
        attr = getattr(module, name)
        
        if inspect.isfunction(attr):
            attributes['functions'].append(name)
        elif inspect.isclass(attr):
            attributes['classes'].append(name)
        elif inspect.ismodule(attr):
            attributes['modules'].append(name)
        else:
            attributes['variables'].append(name)
    
    return attributes

# Версия и метаинформация модуля
__version__ = "1.0.0"
__author__ = "Разработчик"
__email__ = "dev@example.com"

# Пример использования
if __name__ == "__main__":
    explore_module_attributes()
    
    # Исследуем другие модули
    import math
    import json
    
    print("\nИнформация о модуле math:")
    math_info = get_module_info(math)
    for key, value in math_info.items():
        print(f"  {key}: {value}")
    
    print("\nАтрибуты модуля json:")
    json_attrs = list_module_attributes(json)
    for category, items in json_attrs.items():
        if items:  # Показываем только непустые категории
            print(f"  {category}: {', '.join(items[:5])}")  # Первые 5
```

### Динамическое изменение модулей

```python
import sys
import types

def add_function_to_module(module_name, func_name, func):
    """Добавить функцию в существующий модуль"""
    if module_name in sys.modules:
        setattr(sys.modules[module_name], func_name, func)
        return True
    return False

def modify_module_attribute(module_name, attr_name, new_value):
    """Изменить атрибут модуля"""
    if module_name in sys.modules:
        setattr(sys.modules[module_name], attr_name, new_value)
        return True
    return False

def create_module_at_runtime(module_name, **kwargs):
    """Создать модуль во время выполнения"""
    module = types.ModuleType(module_name)
    
    # Добавляем атрибуты
    for name, value in kwargs.items():
        setattr(module, name, value)
    
    # Регистрируем модуль
    sys.modules[module_name] = module
    return module

# Примеры использования
print("Динамическое изменение модулей:")

# Создаем модуль во время выполнения
runtime_module = create_module_at_runtime(
    'runtime_utils',
    version='1.0.0',
    author='Dynamic Creator',
    greeting=lambda name: f"Привет, {name}!"
)

# Добавляем функцию в модуль
def calculate_area(radius):
    return 3.14159 * radius ** 2

add_function_to_module('runtime_utils', 'calculate_area', calculate_area)

# Используем динамически созданный модуль
import runtime_utils

print(f"Версия: {runtime_utils.version}")
print(f"Автор: {runtime_utils.author}")
print(f"Приветствие: {runtime_utils.greeting('Мир')}")
print(f"Площадь круга: {runtime_utils.calculate_area(5)}")

# Изменяем атрибут существующего модуля
modify_module_attribute('runtime_utils', 'version', '2.0.0')
print(f"Новая версия: {runtime_utils.version}")
```

---

## 📦 Управление зависимостями

### Requirements и виртуальные окружения

```python
# requirements.txt
"""
requests>=2.25.0
numpy>=1.20.0
pandas>=1.3.0
flask==2.0.1
pytest>=6.0.0
black
flake8
mypy
"""

# requirements-dev.txt (для разработки)
"""
-r requirements.txt
pytest-cov
sphinx
jupyter
ipykernel
"""

# pyproject.toml (современный способ)
"""
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "myproject"
version = "0.1.0"
description = "Описание проекта"
authors = [
    {name = "Автор", email = "author@example.com"}
]
dependencies = [
    "requests>=2.25.0",
    "numpy>=1.20.0",
    "pandas>=1.3.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "black",
    "flake8",
    "mypy"
]
web = [
    "flask>=2.0.0",
    "gunicorn"
]

[tool.setuptools]
packages = ["myproject"]
"""
```

### Программная проверка зависимостей

```python
import sys
import subprocess
import importlib.util
from packaging import version
import pkg_resources

def check_dependency(package_name, min_version=None):
    """
    Проверить наличие и версию зависимости
    
    Args:
        package_name: Имя пакета
        min_version: Минимальная версия (опционально)
        
    Returns:
        dict: Информация о зависимости
    """
    result = {
        'name': package_name,
        'installed': False,
        'version': None,
        'meets_requirement': False,
        'error': None
    }
    
    try:
        # Проверяем, можно ли импортировать
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            result['error'] = 'Пакет не найден'
            return result
        
        result['installed'] = True
        
        # Получаем версию через pkg_resources
        try:
            distribution = pkg_resources.get_distribution(package_name)
            result['version'] = distribution.version
            
            # Проверяем версию
            if min_version:
                if version.parse(result['version']) >= version.parse(min_version):
                    result['meets_requirement'] = True
                else:
                    result['error'] = f'Версия {result["version"]} < {min_version}'
            else:
                result['meets_requirement'] = True
                
        except pkg_resources.DistributionNotFound:
            result['error'] = 'Информация о версии недоступна'
            
    except Exception as e:
        result['error'] = str(e)
    
    return result

def check_all_dependencies(requirements):
    """
    Проверить все зависимости
    
    Args:
        requirements: Список кортежей (package_name, min_version)
        
    Returns:
        dict: Результаты проверки
    """
    results = {}
    
    for package_name, min_version in requirements:
        results[package_name] = check_dependency(package_name, min_version)
    
    return results

def install_missing_packages(packages, upgrade=False):
    """
    Установить недостающие пакеты
    
    Args:
        packages: Список имен пакетов
        upgrade: Обновить до последних версий
    """
    for package in packages:
        try:
            cmd = [sys.executable, '-m', 'pip', 'install']
            if upgrade:
                cmd.append('--upgrade')
            cmd.append(package)
            
            print(f"Устанавливаем {package}...")
            subprocess.check_call(cmd)
            print(f"✅ {package} установлен успешно")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки {package}: {e}")

def generate_requirements_file(output_file='requirements-auto.txt'):
    """Генерировать файл requirements из установленных пакетов"""
    try:
        installed_packages = [d for d in pkg_resources.working_set]
        
        with open(output_file, 'w') as f:
            for package in sorted(installed_packages, key=lambda x: x.key):
                f.write(f"{package.key}=={package.version}\n")
        
        print(f"Файл {output_file} создан с {len(installed_packages)} пакетами")
        
    except Exception as e:
        print(f"Ошибка создания файла requirements: {e}")

# Пример использования
if __name__ == "__main__":
    # Список зависимостей для проверки
    required_packages = [
        ('requests', '2.20.0'),
        ('numpy', '1.18.0'),
        ('pandas', '1.0.0'),
        ('flask', None),  # Без ограничения версии
        ('nonexistent_package', None)  # Для демонстрации ошибки
    ]
    
    print("Проверка зависимостей:")
    print("=" * 50)
    
    results = check_all_dependencies(required_packages)
    
    missing_packages = []
    outdated_packages = []
    
    for package_name, info in results.items():
        status = "✅" if info['meets_requirement'] else "❌"
        print(f"{status} {package_name}")
        
        if info['installed']:
            print(f"   Версия: {info['version']}")
        
        if info['error']:
            print(f"   Ошибка: {info['error']}")
        
        if not info['installed']:
            missing_packages.append(package_name)
        elif info['installed'] and not info['meets_requirement']:
            outdated_packages.append(package_name)
        
        print()
    
    # Предложение установки недостающих пакетов
    if missing_packages:
        print(f"Недостающие пакеты: {', '.join(missing_packages)}")
        print("Для автоматической установки раскомментируйте следующую строку:")
        print(f"# install_missing_packages({missing_packages})")
    
    if outdated_packages:
        print(f"Устаревшие пакеты: {', '.join(outdated_packages)}")
        print("Для обновления раскомментируйте следующую строку:")
        print(f"# install_missing_packages({outdated_packages}, upgrade=True)")
```

---

## ✨ Лучшие практики

### Структура проекта

```
myproject/
├── README.md                 # Описание проекта
├── LICENSE                   # Лицензия
├── pyproject.toml           # Конфигурация проекта
├── requirements.txt         # Зависимости
├── requirements-dev.txt     # Зависимости для разработки
├── .gitignore              # Игнорируемые файлы
├── setup.py                # Настройка пакета (если нужен)
├── myproject/              # Основной пакет
│   ├── __init__.py
│   ├── core/               # Основная логика
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── services.py
│   ├── utils/              # Утилиты
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── validators.py
│   ├── api/                # API слой
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   └── config/             # Конфигурация
│       ├── __init__.py
│       ├── settings.py
│       └── constants.py
├── tests/                  # Тесты
│   ├── __init__.py
│   ├── test_core/
│   ├── test_utils/
│   └── test_api/
├── docs/                   # Документация
│   ├── conf.py
│   ├── index.rst
│   └── api.rst
├── scripts/                # Скрипты
│   ├── setup.sh
│   └── deploy.py
└── examples/              # Примеры использования
    ├── basic_usage.py
    └── advanced_usage.py
```

### Правила именования

```python
# Хорошие имена модулей и пакетов
# ✅ Правильно:
import user_management
import data_processing
import email_utils
from core.models import User
from utils.validators import validate_email

# ❌ Неправильно:
import UserManagement  # CamelCase не рекомендуется
import data-processing  # Дефисы недопустимы
import 123module       # Не может начинаться с цифры

# Правила:
# 1. Используйте snake_case для модулей и пакетов
# 2. Короткие, описательные имена
# 3. Избегайте конфликтов с встроенными модулями
# 4. Используйте осмысленные имена

# Примеры хороших имен
modules_examples = {
    'database': 'db',  # Короткий псевдоним для частого использования
    'configuration': 'config',
    'utilities': 'utils',
    'authentication': 'auth',
    'application_programming_interface': 'api'
}
```

### Документирование модулей

```python
# well_documented_module.py
"""
Хорошо документированный модуль

Этот модуль демонстрирует лучшие практики документирования:
- Описание назначения модуля
- Примеры использования
- Информация об авторе и версии
- Список публичного API

Пример использования:
    from well_documented_module import process_data, DataProcessor
    
    # Обработка данных
    result = process_data([1, 2, 3, 4, 5])
    
    # Использование класса
    processor = DataProcessor(threshold=0.5)
    processed = processor.process([1, 2, 3])

Автор: Разработчик <dev@example.com>
Версия: 1.0.0
Лицензия: MIT
"""

__version__ = "1.0.0"
__author__ = "Разработчик"
__email__ = "dev@example.com"
__license__ = "MIT"

# Определяем публичный API
__all__ = [
    'process_data',
    'DataProcessor',
    'DataError'
]

import logging
from typing import List, Optional, Union

# Настройка логирования для модуля
logger = logging.getLogger(__name__)

class DataError(Exception):
    """
    Исключение для ошибок обработки данных
    
    Attributes:
        message: Сообщение об ошибке
        error_code: Код ошибки
    """
    
    def __init__(self, message: str, error_code: int = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

def process_data(data: List[Union[int, float]], 
                 operation: str = 'sum') -> Union[int, float]:
    """
    Обработать список численных данных
    
    Функция выполняет различные операции над списком чисел.
    
    Args:
        data: Список чисел для обработки
        operation: Тип операции ('sum', 'mean', 'max', 'min')
        
    Returns:
        Результат обработки в зависимости от операции
        
    Raises:
        DataError: Если данные некорректны или операция неизвестна
        
    Example:
        >>> process_data([1, 2, 3, 4, 5], 'sum')
        15
        >>> process_data([1, 2, 3, 4, 5], 'mean')
        3.0
        
    Note:
        Функция логирует все операции для отладки
    """
    if not data:
        raise DataError("Список данных не может быть пустым", 1001)
    
    if not all(isinstance(x, (int, float)) for x in data):
        raise DataError("Все элементы должны быть числами", 1002)
    
    logger.info(f"Обработка {len(data)} элементов операцией '{operation}'")
    
    operations = {
        'sum': sum,
        'mean': lambda x: sum(x) / len(x),
        'max': max,
        'min': min
    }
    
    if operation not in operations:
        available = ', '.join(operations.keys())
        raise DataError(
            f"Неизвестная операция '{operation}'. "
            f"Доступные: {available}", 
            1003
        )
    
    result = operations[operation](data)
    logger.info(f"Результат операции '{operation}': {result}")
    
    return result

class DataProcessor:
    """
    Класс для обработки данных с настраиваемыми параметрами
    
    Attributes:
        threshold: Пороговое значение для фильтрации
        normalize: Флаг нормализации данных
        
    Example:
        >>> processor = DataProcessor(threshold=0.5, normalize=True)
        >>> result = processor.process([1, 2, 3, 4, 5])
        >>> print(result)
        [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    
    def __init__(self, threshold: float = 0.0, normalize: bool = False):
        """
        Инициализация процессора
        
        Args:
            threshold: Минимальное значение для включения в результат
            normalize: Нормализовать результат к диапазону [0, 1]
        """
        self.threshold = threshold
        self.normalize = normalize
        self._processed_count = 0
        
        logger.info(f"Создан DataProcessor с threshold={threshold}, "
                   f"normalize={normalize}")
    
    def process(self, data: List[Union[int, float]]) -> List[float]:
        """
        Обработать данные согласно настройкам
        
        Args:
            data: Список чисел для обработки
            
        Returns:
            Обработанный список чисел
            
        Raises:
            DataError: При некорректных данных
        """
        if not data:
            raise DataError("Список данных не может быть пустым")
        
        # Фильтрация по порогу
        filtered_data = [x for x in data if x >= self.threshold]
        
        if not filtered_data:
            logger.warning(f"Все данные отфильтрованы порогом {self.threshold}")
            return []
        
        result = filtered_data.copy()
        
        # Нормализация
        if self.normalize:
            min_val = min(result)
            max_val = max(result)
            
            if max_val > min_val:
                result = [(x - min_val) / (max_val - min_val) for x in result]
            else:
                result = [0.0] * len(result)
        
        self._processed_count += len(data)
        logger.info(f"Обработано {len(data)} элементов, "
                   f"получено {len(result)} результатов")
        
        return result
    
    def get_stats(self) -> dict:
        """
        Получить статистику обработки
        
        Returns:
            Словарь со статистикой
        """
        return {
            'total_processed': self._processed_count,
            'threshold': self.threshold,
            'normalize': self.normalize
        }
    
    def reset_stats(self):
        """Сбросить статистику"""
        self._processed_count = 0
        logger.info("Статистика сброшена")

# Вспомогательные функции (не в __all__)
def _validate_numeric_data(data):
    """Внутренняя функция валидации данных"""
    return all(isinstance(x, (int, float)) for x in data)

# Пример использования модуля
def main():
    """Главная функция для демонстрации модуля"""
    print(f"Демонстрация модуля {__name__} v{__version__}")
    
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    
    # Тестовые данные
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Использование функции
    try:
        result = process_data(test_data, 'mean')
        print(f"Среднее значение: {result}")
        
        # Использование класса
        processor = DataProcessor(threshold=5, normalize=True)
        processed = processor.process(test_data)
        print(f"Обработанные данные: {processed}")
        
        # Статистика
        stats = processor.get_stats()
        print(f"Статистика: {stats}")
        
    except DataError as e:
        print(f"Ошибка обработки данных: {e}")

if __name__ == "__main__":
    main()
```

### Оптимизация импортов

```python
# Медленные импорты в начале файла
import time

start_time = time.time()

# ❌ Медленный способ - импорт тяжелых библиотек сразу
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import tensorflow as tf

print(f"Быстрый запуск за {time.time() - start_time:.3f}с")

# ✅ Быстрый способ - ленивый импорт
class LazyImporter:
    """Ленивый импортер для тяжелых библиотек"""
    
    def __init__(self):
        self._pandas = None
        self._numpy = None
        self._matplotlib = None
    
    @property
    def pandas(self):
        if self._pandas is None:
            import pandas as pd
            self._pandas = pd
        return self._pandas
    
    @property
    def numpy(self):
        if self._numpy is None:
            import numpy as np
            self._numpy = np
        return self._numpy
    
    @property
    def matplotlib(self):
        if self._matplotlib is None:
            import matplotlib.pyplot as plt
            self._matplotlib = plt
        return self._matplotlib

# Глобальный экземпляр
libs = LazyImporter()

def process_dataframe(data):
    """Функция использует pandas только при необходимости"""
    df = libs.pandas.DataFrame(data)
    return df.describe()

def create_plot(x, y):
    """Функция использует matplotlib только при необходимости"""
    libs.matplotlib.plot(x, y)
    return "График создан"

# Альтернативный способ - декоратор
def requires(*modules):
    """Декоратор для импорта модулей при первом вызове"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for module_name in modules:
                if module_name not in globals():
                    if module_name == 'pd':
                        import pandas as pd
                        globals()['pd'] = pd
                    elif module_name == 'np':
                        import numpy as np
                        globals()['np'] = np
                    # Добавьте другие модули по необходимости
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@requires('pd', 'np')
def advanced_analysis(data):
    """Функция с автоматическим импортом зависимостей"""
    df = pd.DataFrame(data)
    array = np.array(data)
    return df.mean(), array.std()
```

Эта теоретическая часть охватывает все основные аспекты работы с модулями и пакетами в Python, от базовых концепций до продвинутых техник и лучших практик. 