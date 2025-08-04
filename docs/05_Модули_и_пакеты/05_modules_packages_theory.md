# Теория: Модули и пакеты Python

## 🎯 Цели раздела

После изучения этого раздела вы будете:
- Понимать концепцию модулей и пакетов в Python
- Уметь создавать и импортировать модули
- Знать различные способы импорта
- Понимать механизм поиска модулей
- Уметь создавать пакеты и подпакеты
- Знать современные инструменты управления зависимостями

## 📦 Что такое модули?

**Модуль** — это файл с расширением `.py`, содержащий Python код. Модули позволяют:

- **Организовать код** в логические единицы
- **Переиспользовать код** в разных проектах
- **Избежать конфликтов имен** через пространства имен
- **Упростить сопровождение** больших проектов

### Создание простого модуля

```python
# math_utils.py
"""
Модуль для математических операций
"""

PI = 3.14159265359

def circle_area(radius):
    """Вычисляет площадь круга"""
    return PI * radius ** 2

def circle_circumference(radius):
    """Вычисляет длину окружности"""
    return 2 * PI * radius

class Calculator:
    """Простой калькулятор"""
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def multiply(a, b):
        return a * b

# Код, который выполняется при запуске модуля как скрипта
if __name__ == "__main__":
    print("Тестирование модуля math_utils")
    print(f"Площадь круга радиусом 5: {circle_area(5)}")
    print(f"Длина окружности радиусом 5: {circle_circumference(5)}")
```

## 📥 Импорт модулей

### 1. Импорт всего модуля

```python
import math_utils

# Использование через имя модуля
area = math_utils.circle_area(10)
calc = math_utils.Calculator()
result = calc.add(5, 3)
```

### 2. Импорт с псевдонимом

```python
import math_utils as mu

area = mu.circle_area(10)
```

### 3. Импорт конкретных объектов

```python
from math_utils import circle_area, PI

area = circle_area(10)  # Используем без префикса модуля
print(f"PI = {PI}")
```

### 4. Импорт всего содержимого (не рекомендуется)

```python
from math_utils import *

# Все объекты доступны напрямую
area = circle_area(10)
calc = Calculator()
```

**⚠️ Почему `from module import *` плохо:**
- Засоряет пространство имен
- Может вызвать конфликты имен
- Усложняет отладку
- Снижает читаемость кода

### 5. Условный импорт

```python
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("NumPy не установлен, используется альтернативная реализация")

def advanced_calculation(data):
    if HAS_NUMPY:
        return np.mean(data)
    else:
        return sum(data) / len(data)
```

## 🔍 Механизм поиска модулей

### Порядок поиска модулей

Python ищет модули в следующем порядке:

1. **Текущая директория** (где запущен скрипт)
2. **PYTHONPATH** (переменная окружения)
3. **Стандартные библиотеки** (site-packages)
4. **Пути, добавленные в sys.path**

```python
import sys

# Просмотр путей поиска модулей
print("Пути поиска модулей:")
for path in sys.path:
    print(f"  {path}")

# Добавление пути во время выполнения
sys.path.append("/path/to/my/modules")
```

### Переменная окружения PYTHONPATH

```bash
# Linux/Mac
export PYTHONPATH="/path/to/modules:$PYTHONPATH"

# Windows
set PYTHONPATH=C:\path\to\modules;%PYTHONPATH%
```

### Файл .pth для постоянного добавления путей

```python
# Создаем файл mymodules.pth в site-packages
# Содержимое файла:
/path/to/my/modules
/another/path/to/modules
```

## 📁 Атрибуты модуля

Каждый модуль имеет встроенные атрибуты:

```python
# my_module.py
"""Документация модуля"""

def my_function():
    """Функция модуля"""
    print(f"Модуль: {__name__}")
    print(f"Файл: {__file__}")
    print(f"Документация: {__doc__}")

# Информация о модуле
print(f"Имя модуля: {__name__}")
print(f"Файл модуля: {__file__}")
print(f"Документация: {__doc__}")

# Все атрибуты модуля
print(f"Атрибуты модуля: {dir()}")
```

### Полезные атрибуты:

- `__name__` — имя модуля
- `__file__` — путь к файлу модуля
- `__doc__` — строка документации
- `__package__` — имя пакета
- `__path__` — список путей (для пакетов)

## 📦 Пакеты

**Пакет** — это директория, содержащая файл `__init__.py` и другие модули/подпакеты.

### Структура пакета

```
mypackage/
    __init__.py          # Инициализация пакета
    module1.py           # Модуль 1
    module2.py           # Модуль 2
    subpackage/          # Подпакет
        __init__.py
        submodule.py
    utils/               # Еще один подпакет
        __init__.py
        helpers.py
        constants.py
```

### Файл __init__.py

```python
# mypackage/__init__.py
"""
Мой пакет для демонстрации
"""

# Импорты для удобства пользователей
from .module1 import important_function
from .module2 import UsefulClass
from .utils.constants import VERSION

# Контроль экспорта
__all__ = [
    'important_function',
    'UsefulClass', 
    'VERSION'
]

# Версия пакета
__version__ = "1.0.0"

# Инициализация пакета
print(f"Инициализация пакета {__name__} версии {__version__}")

def package_info():
    """Информация о пакете"""
    return {
        "name": __name__,
        "version": __version__,
        "modules": __all__
    }
```

### Примеры модулей в пакете

```python
# mypackage/module1.py
"""Первый модуль пакета"""

def important_function(x, y):
    """Важная функция"""
    return x * y + 42

def internal_function():
    """Внутренняя функция (не экспортируется)"""
    return "secret"
```

```python
# mypackage/module2.py
"""Второй модуль пакета"""

class UsefulClass:
    """Полезный класс"""
    
    def __init__(self, value):
        self.value = value
    
    def process(self):
        return self.value * 2
```

```python
# mypackage/utils/constants.py
"""Константы пакета"""

VERSION = "1.0.0"
MAX_SIZE = 1000
DEFAULT_CONFIG = {
    "debug": False,
    "timeout": 30
}
```

### Импорт из пакетов

```python
# Различные способы импорта
import mypackage
from mypackage import important_function
from mypackage.module2 import UsefulClass
from mypackage.utils.constants import VERSION

# Использование
result = mypackage.important_function(5, 3)
obj = UsefulClass(10)
print(f"Версия: {VERSION}")
```

## 🔄 Относительные импорты

### Абсолютные vs относительные импорты

```python
# mypackage/subpackage/submodule.py

# Абсолютный импорт (рекомендуется)
from mypackage.module1 import important_function
from mypackage.utils.constants import VERSION

# Относительный импорт
from ..module1 import important_function      # На уровень вверх
from ..utils.constants import VERSION        # На уровень вверх, затем в utils
from .helpers import helper_function         # В той же директории

# Относительные импорты работают только внутри пакетов!
```

### Правила относительных импортов:

- `.` — текущая директория
- `..` — родительская директория  
- `...` — директория на два уровня вверх
- Работают только внутри пакетов
- Не работают в главном модуле (`__main__`)

## 🌟 Продвинутые техники

### 1. Ленивая загрузка модулей

```python
# mypackage/__init__.py
"""Пакет с ленивой загрузкой"""

def __getattr__(name):
    """Ленивая загрузка модулей"""
    if name == "heavy_module":
        from . import heavy_module
        return heavy_module
    elif name == "optional_module":
        try:
            from . import optional_module
            return optional_module
        except ImportError:
            raise AttributeError(f"Модуль {name} недоступен")
    
    raise AttributeError(f"Модуль {name} не найден")

# Теперь модули загружаются только при обращении
# import mypackage
# mypackage.heavy_module  # Загружается только сейчас
```

### 2. Динамическое создание модулей

```python
import types
import sys

def create_dynamic_module(name, content):
    """Создает модуль динамически"""
    
    # Создаем новый модуль
    module = types.ModuleType(name)
    module.__file__ = f"<dynamic:{name}>"
    
    # Выполняем код в контексте модуля
    exec(content, module.__dict__)
    
    # Добавляем в sys.modules
    sys.modules[name] = module
    
    return module

# Использование
code = '''
def dynamic_function():
    return "Я создана динамически!"

DYNAMIC_CONSTANT = 42
'''

dynamic_mod = create_dynamic_module("dynamic_module", code)
print(dynamic_mod.dynamic_function())
print(dynamic_mod.DYNAMIC_CONSTANT)
```

### 3. Модули как синглтоны

```python
# config.py - модуль-синглтон для конфигурации
"""Модуль конфигурации (синглтон)"""

# Состояние модуля сохраняется между импортами
_config = {}
_initialized = False

def initialize(config_dict):
    """Инициализация конфигурации"""
    global _config, _initialized
    if not _initialized:
        _config.update(config_dict)
        _initialized = True
        print("Конфигурация инициализирована")
    else:
        print("Конфигурация уже инициализирована")

def get(key, default=None):
    """Получить значение конфигурации"""
    return _config.get(key, default)

def set(key, value):
    """Установить значение конфигурации"""
    _config[key] = value

def all_config():
    """Получить всю конфигурацию"""
    return _config.copy()
```

### 4. Модули с состоянием

```python
# counter.py - модуль со счетчиком
"""Модуль-счетчик с состоянием"""

_count = 0
_history = []

def increment(step=1):
    """Увеличить счетчик"""
    global _count
    _count += step
    _history.append(f"increment({step}) -> {_count}")
    return _count

def decrement(step=1):
    """Уменьшить счетчик"""
    global _count
    _count -= step
    _history.append(f"decrement({step}) -> {_count}")
    return _count

def get_count():
    """Получить текущее значение"""
    return _count

def get_history():
    """Получить историю операций"""
    return _history.copy()

def reset():
    """Сбросить счетчик"""
    global _count
    _count = 0
    _history.clear()
    _history.append("reset() -> 0")
```

## 🛠️ Инструменты управления зависимостями

### 1. pip - менеджер пакетов

```bash
# Установка пакетов
pip install requests
pip install pandas numpy matplotlib

# Установка конкретной версии
pip install Django==3.2.0
pip install "numpy>=1.19.0,<1.21.0"

# Установка из requirements.txt
pip install -r requirements.txt

# Обновление пакетов
pip install --upgrade requests
pip list --outdated

# Удаление пакетов
pip uninstall requests

# Информация о пакете
pip show pandas
pip list
```

### 2. requirements.txt

```txt
# requirements.txt
# Основные зависимости
requests>=2.25.0
pandas>=1.3.0
numpy>=1.19.0

# Зависимости для разработки
pytest>=6.0.0
black>=21.0.0
flake8>=3.8.0

# Зависимости с точными версиями
Django==3.2.13
celery==5.2.0

# Зависимости из git
git+https://github.com/user/repo.git@v1.0.0

# Зависимости с дополнительными возможностями
requests[security,socks]
```

### 3. Виртуальные окружения

```bash
# Создание виртуального окружения
python -m venv myenv
python3 -m venv myenv

# Активация
# Linux/Mac:
source myenv/bin/activate
# Windows:
myenv\Scripts\activate

# Деактивация
deactivate

# Удаление
rm -rf myenv  # Linux/Mac
rmdir /s myenv  # Windows
```

### 4. pipenv - современный менеджер зависимостей

```bash
# Установка pipenv
pip install pipenv

# Создание проекта
pipenv --python 3.9
pipenv install requests pandas

# Установка зависимостей для разработки
pipenv install pytest --dev

# Активация окружения
pipenv shell

# Запуск команд в окружении
pipenv run python script.py
pipenv run pytest

# Генерация requirements.txt
pipenv requirements > requirements.txt
```

#### Pipfile

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = "*"
pandas = ">=1.3.0"
django = "==3.2.13"

[dev-packages]
pytest = "*"
black = "*"
flake8 = "*"

[requires]
python_version = "3.9"

[scripts]
test = "pytest"
format = "black ."
lint = "flake8 ."
```

### 5. Poetry - продвинутый менеджер

```bash
# Установка Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Создание проекта
poetry new myproject
cd myproject

# Добавление зависимостей
poetry add requests pandas
poetry add pytest --group dev

# Установка зависимостей
poetry install

# Запуск команд
poetry run python script.py
poetry run pytest

# Сборка пакета
poetry build
```

#### pyproject.toml

```toml
[tool.poetry]
name = "myproject"
version = "0.1.0"
description = "My awesome project"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.25.0"
pandas = "^1.3.0"

[tool.poetry.group.dev.dependencies]
pytest = "^6.0.0"
black = "^21.0.0"
flake8 = "^3.8.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.scripts]
myapp = "myproject.main:main"
```

## 🏗️ Создание собственных пакетов

### 1. Структура проекта

```
myawesome_package/
├── README.md
├── LICENSE
├── setup.py
├── pyproject.toml
├── requirements.txt
├── myawesome_package/
│   ├── __init__.py
│   ├── core.py
│   ├── utils.py
│   └── submodule/
│       ├── __init__.py
│       └── advanced.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── docs/
│   └── README.md
└── examples/
    └── basic_usage.py
```

### 2. setup.py (классический способ)

```python
# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="myawesome-package",
    version="0.1.0",
    author="Your Name",
    author_email="you@example.com",
    description="An awesome Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/myawesome-package",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=6.0", "black>=21.0", "flake8>=3.8"],
        "docs": ["sphinx>=4.0", "sphinx-rtd-theme>=0.5"],
    },
    entry_points={
        "console_scripts": [
            "myawesome=myawesome_package.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
```

### 3. pyproject.toml (современный способ)

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "myawesome-package"
authors = [
    {name = "Your Name", email = "you@example.com"},
]
description = "An awesome Python package"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]
dynamic = ["version"]
dependencies = [
    "requests>=2.25.0",
    "click>=7.0",
]

[project.optional-dependencies]
dev = ["pytest>=6.0", "black>=21.0", "flake8>=3.8"]
docs = ["sphinx>=4.0", "sphinx-rtd-theme>=0.5"]

[project.urls]
Homepage = "https://github.com/yourusername/myawesome-package"
"Bug Reports" = "https://github.com/yourusername/myawesome-package/issues"
"Source" = "https://github.com/yourusername/myawesome-package"

[project.scripts]
myawesome = "myawesome_package.cli:main"

[tool.setuptools_scm]
write_to = "myawesome_package/_version.py"
```

### 4. Пример пакета

```python
# myawesome_package/__init__.py
"""
MyAwesome Package - демонстрационный пакет
"""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from .core import AwesomeClass, awesome_function
from .utils import helper_function

__all__ = [
    'AwesomeClass',
    'awesome_function', 
    'helper_function',
    '__version__'
]
```

```python
# myawesome_package/core.py
"""Основная функциональность пакета"""

class AwesomeClass:
    """Потрясающий класс"""
    
    def __init__(self, value):
        self.value = value
    
    def process(self):
        """Обрабатывает значение"""
        return self.value * 2
    
    def __repr__(self):
        return f"AwesomeClass({self.value})"

def awesome_function(x, y):
    """Потрясающая функция"""
    return x + y + 42
```

### 5. Сборка и публикация

```bash
# Сборка пакета
python -m build

# Установка локально для тестирования
pip install -e .

# Публикация в TestPyPI
python -m twine upload --repository testpypi dist/*

# Публикация в PyPI
python -m twine upload dist/*
```

## 🔧 Лучшие практики

### 1. Структура проекта

```
project/
├── README.md              # Описание проекта
├── LICENSE                # Лицензия
├── .gitignore            # Игнорируемые файлы
├── requirements.txt       # Зависимости
├── setup.py / pyproject.toml  # Конфигурация пакета
├── src/                   # Исходный код (альтернативная структура)
│   └── mypackage/
├── mypackage/            # Основной пакет
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── tests/                # Тесты
│   ├── __init__.py
│   └── test_*.py
├── docs/                 # Документация
└── examples/             # Примеры использования
```

### 2. Именование

```python
# Хорошие имена модулей и пакетов
utils.py
math_helpers.py
user_management.py

# Плохие имена
Helpers.py           # CamelCase не принят для модулей
utilities-module.py  # дефисы недопустимы
2math.py            # не может начинаться с цифры
```

### 3. Импорты

```python
# Порядок импортов (PEP 8)
# 1. Стандартная библиотека
import os
import sys
from pathlib import Path

# 2. Сторонние библиотеки
import requests
import pandas as pd
import numpy as np

# 3. Локальные импорты
from .core import AwesomeClass
from .utils import helper_function
```

### 4. Использование __all__

```python
# mymodule.py
"""Модуль с контролем экспорта"""

def public_function():
    """Публичная функция"""
    pass

def _private_function():
    """Приватная функция"""
    pass

def internal_function():
    """Внутренняя функция"""
    pass

# Контролируем что экспортируется при from module import *
__all__ = ['public_function']
```

### 5. Документирование модулей

```python
# documented_module.py
"""
Подробно документированный модуль

Этот модуль демонстрирует лучшие практики документирования.
Включает описание назначения, примеры использования и список функций.

Example:
    >>> from documented_module import calculate
    >>> result = calculate(5, 3)
    >>> print(result)
    8

Attributes:
    DEFAULT_VALUE (int): Значение по умолчанию
    MAX_ITERATIONS (int): Максимальное количество итераций
"""

DEFAULT_VALUE = 10
MAX_ITERATIONS = 1000

def calculate(a, b):
    """
    Вычисляет сумму двух чисел.
    
    Args:
        a (int): Первое число
        b (int): Второе число
    
    Returns:
        int: Сумма a и b
    
    Raises:
        TypeError: Если аргументы не являются числами
    
    Example:
        >>> calculate(2, 3)
        5
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Аргументы должны быть числами")
    
    return a + b
```

## 🚀 Заключение

Модули и пакеты — это основа организации кода в Python. Правильное использование позволяет:

### Ключевые принципы:
1. **Один модуль = одна логическая функция**
2. **Используйте пакеты для группировки связанных модулей**
3. **Предпочитайте абсолютные импорты относительным**
4. **Контролируйте экспорт с помощью `__all__`**
5. **Документируйте модули и функции**
6. **Используйте виртуальные окружения**
7. **Следуйте PEP 8 для именования и структуры**

### Современные инструменты:
- **Poetry** или **pipenv** для управления зависимостями
- **pyproject.toml** для конфигурации пакетов
- **Type hints** для лучшей документации API
- **Тестирование** модулей и пакетов

Модули и пакеты делают Python код масштабируемым, поддерживаемым и переиспользуемым! 