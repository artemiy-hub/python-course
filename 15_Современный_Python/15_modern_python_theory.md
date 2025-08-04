# Теория: Современный Python (3.8+)

## 🎯 Цель раздела

Этот раздел охватывает современные возможности Python, появившиеся в версиях 3.8 и выше. Изучим новый синтаксис, улучшения производительности, и лучшие практики современной разработки на Python.

## 📋 Содержание

1. [Walrus Operator (:=)](#walrus-operator-)
2. [Structural Pattern Matching](#structural-pattern-matching)
3. [Positional-Only Parameters](#positional-only-parameters)
4. [Улучшения в типизации](#улучшения-в-типизации)
5. [Новые встроенные функции](#новые-встроенные-функции)
6. [Улучшения производительности](#улучшения-производительности)
7. [Async/Await улучшения](#asyncawait-улучшения)

---

## 🔄 Walrus Operator (:=)

Оператор "walrus" (моржовый оператор) позволяет присваивать значения переменным внутри выражений.

### Базовое использование

```python
# Традиционный подход
data = input("Введите данные: ")
if len(data) > 10:
    print(f"Длинные данные: {data}")

# С walrus operator
if (data_length := len(input("Введите данные: "))) > 10:
    print(f"Длина данных: {data_length}")

# В циклах while
while (line := input("Команда (quit для выхода): ")) != "quit":
    print(f"Выполняем: {line}")

# В list comprehensions
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
doubled_evens = [doubled for num in numbers 
                if (doubled := num * 2) % 4 == 0]
print(doubled_evens)  # [4, 8, 12, 16, 20]
```

### Продвинутое использование

```python
import re
from typing import Optional, Match

def process_text_advanced(text: str) -> dict:
    """Продвинутая обработка текста с walrus operator"""
    result = {}
    
    # Поиск email с сохранением результата
    if email_match := re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        result['email'] = email_match.group()
        result['email_domain'] = email_match.group().split('@')[1]
    
    # Поиск номеров телефонов
    if phone_matches := re.findall(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', text):
        result['phones'] = phone_matches
        result['phone_count'] = len(phone_matches)
    
    # Анализ длины слов
    words = text.split()
    long_words = [word for word in words if (word_len := len(word)) > 7]
    if long_words:
        result['long_words'] = long_words
        result['avg_long_word_length'] = sum(len(word) for word in long_words) / len(long_words)
    
    return result

# Использование в функциональном программировании
def fibonacci_sequence(n: int) -> list[int]:
    """Генерация последовательности Фибоначчи с walrus operator"""
    if n <= 0:
        return []
    
    sequence = [0, 1]
    while len(sequence) < n and (next_fib := sequence[-1] + sequence[-2]):
        sequence.append(next_fib)
    
    return sequence[:n]

# В контекстных менеджерах
class DatabaseConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        if self.connection := self._establish_connection():
            return self.connection
        raise ConnectionError("Не удалось установить соединение")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
    
    def _establish_connection(self):
        # Имитация установки соединения
        return f"Connected to {self.connection_string}"
```

### Паттерны и лучшие практики

```python
import json
from pathlib import Path
from typing import Any, Optional

def safe_file_operations(filename: str) -> Optional[dict]:
    """Безопасные файловые операции с walrus operator"""
    
    # Проверка существования файла
    if not (file_path := Path(filename)).exists():
        print(f"Файл {filename} не существует")
        return None
    
    # Проверка размера файла
    if (file_size := file_path.stat().st_size) > 1_000_000:  # 1MB
        print(f"Файл слишком большой: {file_size} байт")
        return None
    
    # Чтение и парсинг JSON
    try:
        if content := file_path.read_text(encoding='utf-8'):
            return json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Ошибка при чтении файла: {e}")
    
    return None

# Оптимизация вычислений
def expensive_computation_cache():
    """Кэширование дорогих вычислений"""
    cache = {}
    
    def compute(x: int) -> int:
        if (result := cache.get(x)) is not None:
            print(f"Возвращаем из кэша: {x} -> {result}")
            return result
        
        # Дорогое вычисление
        result = sum(i * i for i in range(x))
        cache[x] = result
        print(f"Вычислили и сохранили: {x} -> {result}")
        return result
    
    return compute

# Валидация данных
def validate_user_input(data: dict) -> dict:
    """Валидация пользовательских данных"""
    errors = {}
    
    # Проверка имени пользователя
    if not (username := data.get('username', '')).strip():
        errors['username'] = 'Имя пользователя не может быть пустым'
    elif len(username) < 3:
        errors['username'] = 'Имя пользователя должно содержать минимум 3 символа'
    
    # Проверка email
    email_pattern = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
    if not (email := data.get('email', '')):
        errors['email'] = 'Email обязателен'
    elif not email_pattern.match(email):
        errors['email'] = 'Некорректный формат email'
    
    # Проверка пароля
    if not (password := data.get('password', '')):
        errors['password'] = 'Пароль обязателен'
    elif len(password) < 8:
        errors['password'] = 'Пароль должен содержать минимум 8 символов'
    elif not any(c.isupper() for c in password):
        errors['password'] = 'Пароль должен содержать заглавные буквы'
    
    return errors
```

---

## 🎯 Structural Pattern Matching

Pattern matching (PEP 634, Python 3.10+) добавляет мощные возможности сопоставления с образцами.

### Базовый синтаксис

```python
def process_data(data):
    """Обработка данных с pattern matching"""
    
    match data:
        case int() if data > 0:
            return f"Положительное число: {data}"
        
        case int() if data < 0:
            return f"Отрицательное число: {data}"
        
        case 0:
            return "Ноль"
        
        case str() if len(data) > 0:
            return f"Непустая строка: {data}"
        
        case str():
            return "Пустая строка"
        
        case list() | tuple():
            return f"Последовательность из {len(data)} элементов"
        
        case dict():
            return f"Словарь с ключами: {list(data.keys())}"
        
        case _:
            return f"Неизвестный тип: {type(data)}"

# Сопоставление с распаковкой
def analyze_coordinates(point):
    """Анализ координат"""
    
    match point:
        case (0, 0):
            return "Начало координат"
        
        case (0, y):
            return f"На оси Y: y={y}"
        
        case (x, 0):
            return f"На оси X: x={x}"
        
        case (x, y) if x == y:
            return f"На диагонали: ({x}, {y})"
        
        case (x, y) if x > 0 and y > 0:
            return f"Первая четверть: ({x}, {y})"
        
        case (x, y):
            return f"Точка: ({x}, {y})"
        
        case _:
            return "Некорректные координаты"
```

### Продвинутые паттерны

```python
from dataclasses import dataclass
from typing import Union, Literal
from enum import Enum

# Классы для демонстрации
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
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

@dataclass
class Shape:
    geometry: Union[Circle, Rectangle]
    color: Color
    filled: bool = False

def analyze_shape(shape: Shape) -> str:
    """Анализ геометрических фигур"""
    
    match shape:
        # Красные круги
        case Shape(geometry=Circle(radius=r), color=Color.RED) if r > 10:
            return f"Большой красный круг (радиус: {r})"
        
        case Shape(geometry=Circle(radius=r), color=Color.RED):
            return f"Маленький красный круг (радиус: {r})"
        
        # Прямоугольники
        case Shape(geometry=Rectangle(width=w, height=h), filled=True) if w == h:
            return f"Заполненный квадрат {w}x{h}"
        
        case Shape(geometry=Rectangle(width=w, height=h)) if w == h:
            return f"Квадрат {w}x{h}"
        
        case Shape(geometry=Rectangle(width=w, height=h)):
            return f"Прямоугольник {w}x{h}"
        
        # Цветные фигуры
        case Shape(color=Color.GREEN):
            return "Зеленая фигура"
        
        case Shape(color=Color.BLUE, filled=True):
            return "Заполненная синяя фигура"
        
        case _:
            return "Неопознанная фигура"

# Обработка JSON-подобных структур
def process_api_response(response: dict) -> str:
    """Обработка ответов API"""
    
    match response:
        # Успешные ответы
        case {"status": "success", "data": list() as data} if len(data) > 0:
            return f"Получен список из {len(data)} элементов"
        
        case {"status": "success", "data": dict() as data}:
            return f"Получен объект с полями: {list(data.keys())}"
        
        case {"status": "success", "data": data}:
            return f"Получены данные: {data}"
        
        # Ошибки
        case {"status": "error", "code": 404}:
            return "Ресурс не найден"
        
        case {"status": "error", "code": code, "message": message}:
            return f"Ошибка {code}: {message}"
        
        case {"status": "error", "message": message}:
            return f"Ошибка: {message}"
        
        # Статусы загрузки
        case {"status": "loading", "progress": int() as progress}:
            return f"Загрузка: {progress}%"
        
        # Пагинация
        case {"data": data, "page": page, "total_pages": total}:
            return f"Страница {page} из {total}, элементов: {len(data)}"
        
        case _:
            return f"Неизвестный формат ответа: {response}"

# Парсинг команд
def parse_command(command: str) -> str:
    """Парсинг текстовых команд"""
    parts = command.strip().split()
    
    match parts:
        case ["help"]:
            return "Показать справку"
        
        case ["help", topic]:
            return f"Показать справку по теме: {topic}"
        
        case ["create", "user", username]:
            return f"Создать пользователя: {username}"
        
        case ["create", "user", username, "--admin"]:
            return f"Создать администратора: {username}"
        
        case ["delete", "user", username] if username != "admin":
            return f"Удалить пользователя: {username}"
        
        case ["delete", "user", "admin"]:
            return "Нельзя удалить администратора"
        
        case ["list", "users", "--active"]:
            return "Показать активных пользователей"
        
        case ["list", "users"]:
            return "Показать всех пользователей"
        
        case ["config", "set", key, value]:
            return f"Установить {key} = {value}"
        
        case ["config", "get", key]:
            return f"Получить значение {key}"
        
        case ["exit" | "quit"]:
            return "Выход из программы"
        
        case []:
            return "Пустая команда"
        
        case _:
            return f"Неизвестная команда: {' '.join(parts)}"
```

### Интеграция с типизацией

```python
from typing import TypedDict, Literal, Union
from dataclasses import dataclass

# Типизированные структуры для pattern matching
class UserData(TypedDict):
    id: int
    name: str
    role: Literal["admin", "user", "guest"]
    active: bool

class LoginEvent(TypedDict):
    type: Literal["login"]
    user_id: int
    timestamp: float
    ip_address: str

class LogoutEvent(TypedDict):
    type: Literal["logout"]
    user_id: int
    timestamp: float
    session_duration: float

class ErrorEvent(TypedDict):
    type: Literal["error"]
    error_code: int
    message: str
    timestamp: float

Event = Union[LoginEvent, LogoutEvent, ErrorEvent]

def process_event(event: Event) -> str:
    """Обработка событий с типизацией"""
    
    match event:
        case {"type": "login", "user_id": user_id, "ip_address": ip}:
            return f"Пользователь {user_id} вошел с IP {ip}"
        
        case {"type": "logout", "user_id": user_id, "session_duration": duration}:
            return f"Пользователь {user_id} вышел, сессия: {duration:.1f}с"
        
        case {"type": "error", "error_code": 401, "message": message}:
            return f"Ошибка авторизации: {message}"
        
        case {"type": "error", "error_code": code, "message": message}:
            return f"Ошибка {code}: {message}"
        
        case _:
            return f"Неизвестное событие: {event}"

# Обработка вложенных структур
@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    credentials: dict[str, str]

@dataclass
class RedisConfig:
    host: str
    port: int
    password: str | None = None

@dataclass
class AppConfig:
    name: str
    debug: bool
    database: DatabaseConfig | RedisConfig
    features: list[str]

def validate_config(config: AppConfig) -> list[str]:
    """Валидация конфигурации"""
    errors = []
    
    match config:
        case AppConfig(name="", **_):
            errors.append("Имя приложения не может быть пустым")
        
        case AppConfig(database=DatabaseConfig(host="", **_), **_):
            errors.append("Хост базы данных не может быть пустым")
        
        case AppConfig(database=DatabaseConfig(port=port, **_), **_) if not (1 <= port <= 65535):
            errors.append(f"Некорректный порт базы данных: {port}")
        
        case AppConfig(database=RedisConfig(password=None, **_), debug=False, **_):
            errors.append("Redis пароль обязателен в production режиме")
        
        case AppConfig(features=features, **_) if "auth" not in features:
            errors.append("Аутентификация должна быть включена")
    
    return errors
```

---

## 📌 Positional-Only Parameters

Python 3.8 добавил поддержку параметров, которые можно передавать только позиционно.

### Синтаксис и использование

```python
def greet(name, /, greeting="Hello", *, punctuation="!"):
    """
    Функция с различными типами параметров:
    - name: только позиционный
    - greeting: позиционный или именованный
    - punctuation: только именованный
    """
    return f"{greeting} {name}{punctuation}"

# Правильные вызовы
print(greet("Alice"))                          # Hello Alice!
print(greet("Bob", "Hi"))                      # Hi Bob!
print(greet("Charlie", greeting="Hey"))        # Hey Charlie!
print(greet("David", punctuation="?"))         # Hello David?
print(greet("Eve", "Hi", punctuation="!!!"))   # Hi Eve!!!

# Неправильные вызовы (вызовут TypeError)
# greet(name="Alice")              # name нельзя передать по имени
# greet("Bob", punctuation="?", "Hi")  # punctuation должен быть именованным

def create_user(user_id, /, *, name, email, role="user"):
    """Создание пользователя с четким API"""
    return {
        "id": user_id,
        "name": name,
        "email": email,
        "role": role
    }

# user_id всегда позиционный, остальные - именованные
user = create_user(123, name="Alice", email="alice@example.com")
```

### Практические применения

```python
from typing import Any, Callable, TypeVar
import functools

T = TypeVar('T')

def cached_property(func: Callable[[Any], T], /) -> property:
    """Декоратор для кэширования свойств"""
    
    @functools.wraps(func)
    def wrapper(self):
        attr_name = f"_cached_{func.__name__}"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    return property(wrapper)

class ExpensiveCalculation:
    def __init__(self, base_value: int):
        self.base_value = base_value
    
    @cached_property
    def expensive_result(self):
        """Дорогое вычисление (выполняется только раз)"""
        print("Выполняем дорогое вычисление...")
        return sum(i * i for i in range(self.base_value))

# Функции для работы с коллекциями
def find_element(collection, predicate, /, *, default=None):
    """Поиск элемента в коллекции"""
    for item in collection:
        if predicate(item):
            return item
    return default

def group_by(collection, key_func, /, *, preserve_order=False):
    """Группировка элементов коллекции"""
    from collections import defaultdict, OrderedDict
    
    groups = OrderedDict() if preserve_order else defaultdict(list)
    
    for item in collection:
        key = key_func(item)
        if preserve_order and key not in groups:
            groups[key] = []
        groups[key].append(item)
    
    return dict(groups) if preserve_order else dict(groups)

# Примеры использования
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_number = find_element(numbers, lambda x: x % 2 == 0)
print(f"Первое четное число: {even_number}")

words = ["apple", "banana", "apricot", "blueberry", "cherry"]
grouped = group_by(words, lambda w: w[0], preserve_order=True)
print(f"Группировка по первой букве: {grouped}")

# API для математических функций
def linear_interpolation(x1, y1, x2, y2, /, x, *, clamp=False):
    """Линейная интерполяция между двумя точками"""
    if x1 == x2:
        return y1
    
    t = (x - x1) / (x2 - x1)
    
    if clamp:
        t = max(0, min(1, t))
    
    return y1 + t * (y2 - y1)

# Использование
value = linear_interpolation(0, 0, 10, 100, 5)  # 50.0
clamped_value = linear_interpolation(0, 0, 10, 100, 15, clamp=True)  # 100.0
```

### Дизайн API

```python
from pathlib import Path
from typing import Union, Optional, BinaryIO, TextIO

def read_file(path, /, *, encoding="utf-8", mode="text", errors="strict"):
    """Чтение файла с четким API"""
    file_path = Path(path)
    
    if mode == "text":
        return file_path.read_text(encoding=encoding, errors=errors)
    elif mode == "binary":
        return file_path.read_bytes()
    else:
        raise ValueError(f"Неподдерживаемый режим: {mode}")

def write_file(path, content, /, *, encoding="utf-8", mode="text", create_dirs=False):
    """Запись файла с четким API"""
    file_path = Path(path)
    
    if create_dirs:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if mode == "text":
        file_path.write_text(content, encoding=encoding)
    elif mode == "binary":
        file_path.write_bytes(content)
    else:
        raise ValueError(f"Неподдерживаемый режим: {mode}")

# Функции для валидации
def validate_email(email, /, *, strict=True, allow_unicode=False):
    """Валидация email адреса"""
    import re
    
    if allow_unicode:
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    else:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if strict:
        # Дополнительные проверки для строгого режима
        if email.count('@') != 1:
            return False
        local, domain = email.split('@')
        if len(local) > 64 or len(domain) > 253:
            return False
    
    return bool(re.match(pattern, email))

def validate_phone(phone, /, *, country_code=None, format_style="international"):
    """Валидация номера телефона"""
    import re
    
    # Убираем все нецифровые символы кроме +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    if format_style == "international":
        # Международный формат
        if country_code:
            pattern = f"^\\+{country_code}\\d{{7,15}}$"
        else:
            pattern = r'^\+\d{7,15}$'
    elif format_style == "national":
        # Национальный формат
        pattern = r'^\d{7,15}$'
    else:
        raise ValueError(f"Неподдерживаемый формат: {format_style}")
    
    return bool(re.match(pattern, cleaned))

# Примеры использования
content = read_file("example.txt", encoding="utf-8")
write_file("output.txt", "Hello, World!", create_dirs=True)

is_valid_email = validate_email("user@example.com", strict=True)
is_valid_phone = validate_phone("+1-555-123-4567", country_code="1")
```

---

## 🆕 Новые встроенные функции и улучшения

### Улучшения словарей (Python 3.9+)

```python
# Операторы объединения словарей
user_defaults = {"theme": "light", "language": "en", "notifications": True}
user_preferences = {"theme": "dark", "timezone": "UTC"}

# Объединение с созданием нового словаря
merged_settings = user_defaults | user_preferences
print(merged_settings)
# {'theme': 'dark', 'language': 'en', 'notifications': True, 'timezone': 'UTC'}

# Обновление существующего словаря
user_defaults |= user_preferences
print(user_defaults)

# Практический пример: конфигурация приложения
def load_config(base_config: dict, user_config: dict = None, 
                env_config: dict = None) -> dict:
    """Загрузка конфигурации с приоритетами"""
    config = base_config.copy()
    
    if user_config:
        config |= user_config
    
    if env_config:
        config |= env_config
    
    return config

base = {"debug": False, "port": 8000, "host": "localhost"}
user = {"debug": True, "database_url": "postgresql://..."}
env = {"port": 3000}

final_config = load_config(base, user, env)
print(final_config)
```

### Улучшения строк (Python 3.9+)

```python
# removeprefix и removesuffix
filename = "document.pdf.backup"

# Удаление префикса
if filename.startswith("temp_"):
    clean_name = filename.removeprefix("temp_")

# Удаление суффикса
if filename.endswith(".backup"):
    original_name = filename.removesuffix(".backup")
    print(original_name)  # "document.pdf"

# Практические применения
def clean_filename(filename: str) -> str:
    """Очистка имени файла от служебных префиксов и суффиксов"""
    # Удаляем временные префиксы
    for prefix in ["temp_", "tmp_", "backup_", "old_"]:
        filename = filename.removeprefix(prefix)
    
    # Удаляем служебные суффиксы
    for suffix in [".tmp", ".backup", ".old", ".bak"]:
        filename = filename.removesuffix(suffix)
    
    return filename

def extract_base_domain(url: str) -> str:
    """Извлечение базового домена из URL"""
    url = url.removeprefix("https://")
    url = url.removeprefix("http://")
    url = url.removeprefix("www.")
    
    # Удаляем путь и параметры
    if "/" in url:
        url = url.split("/")[0]
    if "?" in url:
        url = url.split("?")[0]
    
    return url

# Примеры использования
files = ["temp_document.pdf.backup", "backup_image.jpg.old", "data.csv.tmp"]
cleaned = [clean_filename(f) for f in files]
print(cleaned)  # ['document.pdf', 'image.jpg', 'data.csv']

urls = ["https://www.example.com/page", "http://subdomain.site.org/path?param=1"]
domains = [extract_base_domain(url) for url in urls]
print(domains)  # ['example.com', 'subdomain.site.org']
```

### Улучшения в functools

```python
import functools
from typing import Callable, Any

# functools.cache (Python 3.9+) - более простая альтернатива lru_cache
@functools.cache
def expensive_function(x: int, y: int) -> int:
    """Дорогая функция с автоматическим кэшированием"""
    print(f"Вычисляем {x} + {y}")
    return x + y

# Использование
result1 = expensive_function(1, 2)  # Вычисляем 1 + 2
result2 = expensive_function(1, 2)  # Из кэша

# functools.cached_property для ленивых свойств
class DataProcessor:
    def __init__(self, data: list[int]):
        self.data = data
        print("DataProcessor создан")
    
    @functools.cached_property
    def sorted_data(self) -> list[int]:
        """Сортированные данные (вычисляются только при первом обращении)"""
        print("Сортируем данные...")
        return sorted(self.data)
    
    @functools.cached_property
    def statistics(self) -> dict[str, float]:
        """Статистика по данным"""
        print("Вычисляем статистику...")
        return {
            "mean": sum(self.data) / len(self.data),
            "min": min(self.data),
            "max": max(self.data),
            "count": len(self.data)
        }

# Использование
processor = DataProcessor([3, 1, 4, 1, 5, 9, 2, 6])
print(processor.sorted_data)  # Вычисляется при первом обращении
print(processor.sorted_data)  # Возвращается из кэша
print(processor.statistics)   # Вычисляется при первом обращении

# Продвинутое кэширование с TTL
import time
from datetime import datetime, timedelta

def timed_cache(ttl_seconds: int):
    """Декоратор для кэширования с TTL"""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            now = datetime.now()
            
            # Проверяем кэш
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < timedelta(seconds=ttl_seconds):
                    return result
                else:
                    del cache[key]
            
            # Вычисляем результат
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_info = lambda: {"size": len(cache)}
        return wrapper
    
    return decorator

@timed_cache(ttl_seconds=5)
def get_current_time():
    """Функция с кэшированием на 5 секунд"""
    return datetime.now().strftime("%H:%M:%S.%f")

# Тестирование TTL кэша
print(get_current_time())  # Новое значение
print(get_current_time())  # Из кэша
time.sleep(6)
print(get_current_time())  # Новое значение после истечения TTL
```

### Улучшения в itertools и других модулях

```python
import itertools
from typing import Iterator, TypeVar

T = TypeVar('T')

# Новые функции itertools
def batched(iterable: Iterator[T], n: int) -> Iterator[list[T]]:
    """Группировка элементов в батчи (появится в Python 3.12)"""
    iterator = iter(iterable)
    while batch := list(itertools.islice(iterator, n)):
        yield batch

def sliding_window(iterable: Iterator[T], n: int) -> Iterator[tuple[T, ...]]:
    """Скользящее окно по итератору"""
    it = iter(iterable)
    window = list(itertools.islice(it, n))
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window = window[1:] + [x]
        yield tuple(window)

# Практические применения
def process_data_in_batches(data: list[int], batch_size: int = 10):
    """Обработка данных батчами"""
    for batch in batched(data, batch_size):
        print(f"Обрабатываем батч из {len(batch)} элементов: {batch}")
        # Здесь может быть отправка в БД, API и т.д.

def calculate_moving_average(values: list[float], window_size: int = 3) -> list[float]:
    """Вычисление скользящего среднего"""
    averages = []
    for window in sliding_window(values, window_size):
        average = sum(window) / len(window)
        averages.append(average)
    return averages

# Примеры использования
large_dataset = list(range(1, 51))
process_data_in_batches(large_dataset, batch_size=7)

prices = [10.5, 11.2, 10.8, 12.1, 11.9, 12.5, 11.7, 10.9, 11.3]
moving_avg = calculate_moving_average(prices, window_size=3)
print(f"Скользящее среднее: {moving_avg}")

# Продвинутая работа с итераторами
def pairwise(iterable: Iterator[T]) -> Iterator[tuple[T, T]]:
    """Парные элементы (a, b), (b, c), (c, d), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def find_changes(sequence: list[T]) -> list[tuple[int, T, T]]:
    """Поиск изменений в последовательности"""
    changes = []
    for i, (prev, curr) in enumerate(pairwise(sequence)):
        if prev != curr:
            changes.append((i, prev, curr))
    return changes

# Пример использования
states = ["idle", "idle", "loading", "loading", "loaded", "error", "idle"]
changes = find_changes(states)
for position, old_state, new_state in changes:
    print(f"Позиция {position}: {old_state} -> {new_state}")
```

Этот раздел охватывает самые важные и практичные нововведения современного Python, которые делают код более выразительным, безопасным и производительным. 