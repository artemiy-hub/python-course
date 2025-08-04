# Теория: Типизация и аннотации типов в Python

## 🎯 Цель раздела

Типизация в Python — это мощный инструмент для повышения качества кода, улучшения читаемости и предотвращения ошибок. Этот раздел охватывает систему типов Python, начиная с базовых аннотаций и заканчивая продвинутыми концепциями.

## 📋 Содержание

1. [Введение в типизацию](#введение-в-типизацию)
2. [Базовые типы](#базовые-типы)
3. [Составные типы](#составные-типы)
4. [Обобщенные типы](#обобщенные-типы)
5. [Протоколы и интерфейсы](#протоколы-и-интерфейсы)
6. [Dataclasses](#dataclasses)
7. [Статический анализ](#статический-анализ)
8. [Продвинутые концепции](#продвинутые-концепции)

---

## 🏷️ Введение в типизацию

### Зачем нужна типизация?

Python — динамически типизированный язык, но аннотации типов (введенные в PEP 484) позволяют:

- **Улучшить читаемость кода**
- **Предотвращать ошибки** на этапе разработки
- **Упростить рефакторинг**
- **Улучшить IDE поддержку**
- **Документировать API**

```python
# Без типизации
def calculate_area(length, width):
    return length * width

# С типизацией
def calculate_area(length: float, width: float) -> float:
    return length * width
```

### Градуальная типизация

Python поддерживает **градуальную типизацию** — можно добавлять типы постепенно:

```python
# Полностью без типов
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result

# Частичная типизация
def process_data(data) -> list:
    result = []
    for item in data:
        result.append(item * 2)
    return result

# Полная типизация
def process_data(data: list[int]) -> list[int]:
    result: list[int] = []
    for item in data:
        result.append(item * 2)
    return result
```

### Время выполнения vs статический анализ

```python
from typing import List

def greet_users(names: List[str]) -> None:
    for name in names:
        print(f"Привет, {name}!")

# Во время выполнения типы не проверяются
greet_users([1, 2, 3])  # Выполнится, но вызовет ошибку

# Статический анализатор (mypy) найдет ошибку:
# error: Argument 1 to "greet_users" has incompatible type "List[int]"; expected "List[str]"
```

---

## 🔤 Базовые типы

### Встроенные типы

```python
# Примитивные типы
age: int = 25
price: float = 99.99
name: str = "Алиса"
is_active: bool = True

# None тип
def log_message(message: str) -> None:
    print(f"LOG: {message}")

# Любой тип
from typing import Any
data: Any = "может быть чем угодно"
```

### Коллекции

```python
from typing import List, Dict, Set, Tuple

# Списки
numbers: List[int] = [1, 2, 3, 4, 5]
names: List[str] = ["Алиса", "Боб", "Чарли"]

# Словари
user_ages: Dict[str, int] = {"Алиса": 25, "Боб": 30}
config: Dict[str, Any] = {"debug": True, "port": 8080}

# Множества
unique_ids: Set[int] = {1, 2, 3, 4}
tags: Set[str] = {"python", "typing", "programming"}

# Кортежи (фиксированная длина)
coordinates: Tuple[float, float] = (55.7558, 37.6176)
rgb_color: Tuple[int, int, int] = (255, 128, 0)

# Кортежи переменной длины
scores: Tuple[int, ...] = (95, 87, 92, 88)
```

### Современный синтаксис (Python 3.9+)

```python
# Python 3.9+ - встроенные коллекции как типы
numbers: list[int] = [1, 2, 3]
user_data: dict[str, str] = {"name": "Алиса", "email": "alice@example.com"}
coordinates: tuple[float, float] = (55.7558, 37.6176)
unique_values: set[str] = {"a", "b", "c"}
```

---

## 🔗 Составные типы

### Optional и Union

```python
from typing import Optional, Union

# Optional - может быть значением или None
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Алиса", 2: "Боб"}
    return users.get(user_id)  # Возвращает str или None

# Эквивалентно Union[str, None]
def find_user_alt(user_id: int) -> Union[str, None]:
    users = {1: "Алиса", 2: "Боб"}
    return users.get(user_id)

# Union - несколько возможных типов
def parse_id(value: Union[int, str]) -> int:
    if isinstance(value, str):
        return int(value)
    return value

# Современный синтаксис (Python 3.10+)
def find_user_modern(user_id: int) -> str | None:
    users = {1: "Алиса", 2: "Боб"}
    return users.get(user_id)

def parse_id_modern(value: int | str) -> int:
    if isinstance(value, str):
        return int(value)
    return value
```

### Literal типы

```python
from typing import Literal

# Ограничение значений
def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> None:
    print(f"Уровень логирования: {level}")

# Для булевых флагов
def toggle_feature(enabled: Literal[True, False]) -> None:
    if enabled:
        print("Функция включена")
    else:
        print("Функция отключена")

# Числовые литералы
def set_priority(level: Literal[1, 2, 3, 4, 5]) -> None:
    print(f"Приоритет: {level}")
```

### Callable типы

```python
from typing import Callable

# Функция как параметр
def apply_operation(numbers: List[int], operation: Callable[[int], int]) -> List[int]:
    return [operation(num) for num in numbers]

def square(x: int) -> int:
    return x * x

result = apply_operation([1, 2, 3, 4], square)

# Более сложные сигнатуры
def process_data(
    data: List[str], 
    validator: Callable[[str], bool],
    transformer: Callable[[str], str]
) -> List[str]:
    return [transformer(item) for item in data if validator(item)]

# Callback с несколькими параметрами
def async_operation(
    callback: Callable[[bool, Optional[str]], None]
) -> None:
    # Имитация асинхронной операции
    success = True
    error_message = None
    callback(success, error_message)
```

---

## 🎭 Обобщенные типы

### TypeVar - переменные типов

```python
from typing import TypeVar, List, Callable

T = TypeVar('T')

def get_first_item(items: List[T]) -> Optional[T]:
    """Возвращает первый элемент списка или None"""
    if items:
        return items[0]
    return None

# Использование
first_number = get_first_item([1, 2, 3])  # Тип: Optional[int]
first_name = get_first_item(["Алиса", "Боб"])  # Тип: Optional[str]

# Ограниченные TypeVar
Number = TypeVar('Number', int, float)

def add_numbers(a: Number, b: Number) -> Number:
    return a + b

# Bound TypeVar
from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...

ComparableType = TypeVar('ComparableType', bound=Comparable)

def sort_items(items: List[ComparableType]) -> List[ComparableType]:
    return sorted(items)
```

### Generic классы

```python
from typing import Generic, TypeVar

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Stack(Generic[T]):
    """Типизированный стек"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        if self._items:
            return self._items.pop()
        return None
    
    def peek(self) -> Optional[T]:
        if self._items:
            return self._items[-1]
        return None
    
    def is_empty(self) -> bool:
        return len(self._items) == 0

# Использование
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")

# Множественные параметры типов
class Cache(Generic[K, V]):
    """Типизированный кэш"""
    
    def __init__(self) -> None:
        self._data: Dict[K, V] = {}
    
    def get(self, key: K) -> Optional[V]:
        return self._data.get(key)
    
    def set(self, key: K, value: V) -> None:
        self._data[key] = value
    
    def delete(self, key: K) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False

# Использование
user_cache: Cache[int, str] = Cache()
user_cache.set(1, "Алиса")
user_cache.set(2, "Боб")
```

---

## 🤝 Протоколы и интерфейсы

### Protocol - структурная типизация

```python
from typing import Protocol

class Drawable(Protocol):
    """Протокол для объектов, которые можно рисовать"""
    
    def draw(self) -> None:
        """Нарисовать объект"""
        ...
    
    def get_area(self) -> float:
        """Получить площадь объекта"""
        ...

class Circle:
    """Круг - реализует протокол Drawable неявно"""
    
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def draw(self) -> None:
        print(f"Рисуем круг радиусом {self.radius}")
    
    def get_area(self) -> float:
        return 3.14159 * self.radius ** 2

class Rectangle:
    """Прямоугольник - тоже реализует протокол Drawable"""
    
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    
    def draw(self) -> None:
        print(f"Рисуем прямоугольник {self.width}x{self.height}")
    
    def get_area(self) -> float:
        return self.width * self.height

def render_shapes(shapes: List[Drawable]) -> None:
    """Рендерим список фигур"""
    total_area = 0.0
    
    for shape in shapes:
        shape.draw()
        total_area += shape.get_area()
    
    print(f"Общая площадь: {total_area}")

# Использование
shapes = [Circle(5.0), Rectangle(10.0, 20.0), Circle(3.0)]
render_shapes(shapes)  # Работает благодаря структурной типизации
```

### Runtime-проверяемые протоколы

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    """Протокол для сериализуемых объектов"""
    
    def serialize(self) -> str:
        """Сериализовать объект в строку"""
        ...

class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
    
    def serialize(self) -> str:
        return f"{self.name},{self.email}"

class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price
    
    def serialize(self) -> str:
        return f"{self.name}:{self.price}"

def save_objects(objects: List[Serializable]) -> None:
    """Сохраняем сериализуемые объекты"""
    for obj in objects:
        if isinstance(obj, Serializable):  # Runtime проверка
            print(f"Сохраняем: {obj.serialize()}")
        else:
            print(f"Объект {obj} не сериализуем")

# Использование
user = User("Алиса", "alice@example.com")
product = Product("Ноутбук", 99999.99)

save_objects([user, product])
```

---

## 📦 Dataclasses

### Базовое использование

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """Пользователь системы"""
    id: int
    name: str
    email: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    def __post_init__(self) -> None:
        """Вызывается после инициализации"""
        if self.created_at is None:
            self.created_at = datetime.now()

# Автоматически генерируется __init__, __repr__, __eq__
user = User(id=1, name="Алиса", email="alice@example.com")
print(user)  # User(id=1, name='Алиса', email='alice@example.com', is_active=True, created_at=...)

# Сравнение работает из коробки
user2 = User(id=1, name="Алиса", email="alice@example.com")
print(user == user2)  # True (если created_at одинаковые)
```

### Продвинутые возможности

```python
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass(frozen=True)  # Неизменяемый класс
class Point:
    """Точка в 2D пространстве"""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """Расстояние до другой точки"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

@dataclass(order=True)  # Поддержка сравнения (<, >, <=, >=)
class Student:
    """Студент с оценками"""
    name: str
    grade: float
    subjects: List[str] = field(default_factory=list)
    
    # Поле, не участвующее в сравнении
    metadata: Dict[str, str] = field(default_factory=dict, compare=False)
    
    def add_subject(self, subject: str) -> None:
        """Добавить предмет"""
        self.subjects.append(subject)

# Использование
students = [
    Student("Алиса", 4.8),
    Student("Боб", 4.2),
    Student("Чарли", 4.9)
]

# Сортировка работает благодаря order=True
sorted_students = sorted(students)
print([s.name for s in sorted_students])  # ['Боб', 'Алиса', 'Чарли']
```

### Dataclass с валидацией

```python
from dataclasses import dataclass, field
from typing import ClassVar
import re

@dataclass
class Email:
    """Email с валидацией"""
    address: str
    
    # Классовая переменная для паттерна
    EMAIL_PATTERN: ClassVar[re.Pattern] = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    def __post_init__(self) -> None:
        """Валидация email при создании"""
        if not self.EMAIL_PATTERN.match(self.address):
            raise ValueError(f"Некорректный email: {self.address}")
    
    @property
    def domain(self) -> str:
        """Получить домен email"""
        return self.address.split('@')[1]

@dataclass
class BankAccount:
    """Банковский счет с валидацией"""
    account_number: str
    balance: float = field(default=0.0)
    
    def __post_init__(self) -> None:
        """Валидация данных счета"""
        if len(self.account_number) != 16:
            raise ValueError("Номер счета должен содержать 16 цифр")
        
        if not self.account_number.isdigit():
            raise ValueError("Номер счета должен содержать только цифры")
        
        if self.balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
    
    def deposit(self, amount: float) -> None:
        """Пополнить счет"""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += amount
    
    def withdraw(self, amount: float) -> bool:
        """Снять деньги со счета"""
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        
        if amount > self.balance:
            return False  # Недостаточно средств
        
        self.balance -= amount
        return True

# Использование
try:
    email = Email("alice@example.com")
    print(f"Email домен: {email.domain}")
    
    account = BankAccount("1234567890123456", 1000.0)
    account.deposit(500.0)
    print(f"Баланс: {account.balance}")
    
except ValueError as e:
    print(f"Ошибка валидации: {e}")
```

---

## 🔍 Статический анализ

### MyPy - основной инструмент

```bash
# Установка mypy
pip install mypy

# Базовая проверка
mypy script.py

# Конфигурация в mypy.ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### Практический пример

```python
# example.py
from typing import List, Optional

def calculate_average(numbers: List[float]) -> float:
    """Вычисляет среднее арифметическое"""
    if not numbers:
        raise ValueError("Список не может быть пустым")
    
    return sum(numbers) / len(numbers)

def find_max_value(values: List[int]) -> Optional[int]:
    """Находит максимальное значение"""
    if not values:
        return None
    
    return max(values)

# Ошибки, которые найдет mypy:

# 1. Неправильный тип аргумента
result1 = calculate_average([1, 2, "3"])  # error: List item 2 has incompatible type "str"

# 2. Неправильное использование Optional
max_val = find_max_value([1, 2, 3])
print(max_val + 1)  # error: Unsupported operand types for + ("int | None" and "int")

# Правильное использование:
if max_val is not None:
    print(max_val + 1)  # OK
```

### Настройка проверок

```python
# Type: ignore для подавления предупреждений
import json
data = json.loads('{"key": "value"}')  # type: ignore

# Более точная аннотация
from typing import Dict, Any
data: Dict[str, Any] = json.loads('{"key": "value"}')

# Условные импорты для типизации
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from expensive_module import ExpensiveClass

def process_data(obj: 'ExpensiveClass') -> None:
    """Функция использует тип только для аннотации"""
    pass
```

---

## 🚀 Продвинутые концепции

### NewType - создание различимых типов

```python
from typing import NewType

# Создание новых типов на основе существующих
UserId = NewType('UserId', int)
ProductId = NewType('ProductId', int)

def get_user(user_id: UserId) -> str:
    """Получить пользователя по ID"""
    return f"User {user_id}"

def get_product(product_id: ProductId) -> str:
    """Получить продукт по ID"""
    return f"Product {product_id}"

# Использование
user_id = UserId(123)
product_id = ProductId(456)

print(get_user(user_id))      # OK
print(get_product(product_id)) # OK

# Ошибка типизации (но не runtime ошибка)
# print(get_user(product_id))  # mypy error: Expected UserId, got ProductId
```

### TypedDict - типизированные словари

```python
from typing import TypedDict, Optional

class UserData(TypedDict):
    """Структура данных пользователя"""
    id: int
    name: str
    email: str
    is_active: bool

class UserDataOptional(TypedDict, total=False):
    """Структура с опциональными полями"""
    phone: Optional[str]
    address: Optional[str]

def create_user(data: UserData) -> None:
    """Создать пользователя"""
    print(f"Создаем пользователя: {data['name']}")

# Использование
user_info: UserData = {
    'id': 1,
    'name': 'Алиса',
    'email': 'alice@example.com',
    'is_active': True
}

create_user(user_info)

# Расширенная структура
class ExtendedUserData(UserData, UserDataOptional):
    """Расширенная структура пользователя"""
    pass

extended_user: ExtendedUserData = {
    'id': 2,
    'name': 'Боб',
    'email': 'bob@example.com',
    'is_active': True,
    'phone': '+7-123-456-7890'
}
```

### Overload - перегрузка функций

```python
from typing import overload, Union

@overload
def process_id(value: int) -> str: ...

@overload
def process_id(value: str) -> int: ...

def process_id(value: Union[int, str]) -> Union[str, int]:
    """Обработка ID - конвертация между int и str"""
    if isinstance(value, int):
        return f"ID_{value:06d}"
    elif isinstance(value, str):
        if value.startswith("ID_"):
            return int(value[3:])
        return int(value)
    else:
        raise TypeError("Ожидается int или str")

# Использование
str_id = process_id(123)      # Тип: str
int_id = process_id("ID_000123")  # Тип: int
```

### Final и ClassVar

```python
from typing import Final, ClassVar
from dataclasses import dataclass

# Final - неизменяемые значения
MAX_RETRIES: Final[int] = 3
API_VERSION: Final[str] = "v1.0"

@dataclass
class APIClient:
    """Клиент API"""
    
    # Классовые переменные
    BASE_URL: ClassVar[str] = "https://api.example.com"
    TIMEOUT: ClassVar[int] = 30
    
    # Финальные поля экземпляра
    api_key: Final[str]
    
    def __post_init__(self) -> None:
        # api_key нельзя изменить после инициализации
        pass

# Использование
client = APIClient(api_key="secret123")
# client.api_key = "new_key"  # mypy error: Cannot assign to final name "api_key"
```

### Дженерики с ограничениями

```python
from typing import TypeVar, Generic, Protocol
from abc import abstractmethod

class Comparable(Protocol):
    """Протокол для сравнимых объектов"""
    
    @abstractmethod
    def __lt__(self, other) -> bool: ...

T = TypeVar('T', bound=Comparable)

class SortedList(Generic[T]):
    """Автоматически сортируемый список"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        """Добавить элемент с сохранением сортировки"""
        self._items.append(item)
        self._items.sort()
    
    def get_items(self) -> List[T]:
        """Получить отсортированный список"""
        return self._items.copy()

# Использование только с сравнимыми типами
int_list: SortedList[int] = SortedList()
int_list.add(3)
int_list.add(1)
int_list.add(2)
print(int_list.get_items())  # [1, 2, 3]

str_list: SortedList[str] = SortedList()
str_list.add("charlie")
str_list.add("alice")
str_list.add("bob")
print(str_list.get_items())  # ['alice', 'bob', 'charlie']
```

### Условная типизация

```python
from typing import TYPE_CHECKING, Any
import sys

# Условные импорты
if TYPE_CHECKING:
    from pandas import DataFrame
    from numpy import ndarray
else:
    DataFrame = Any
    ndarray = Any

def analyze_data(data: 'DataFrame') -> 'ndarray':
    """Анализ данных (требует pandas и numpy)"""
    if TYPE_CHECKING:
        # Код для статического анализа
        return data.values
    else:
        # Фактическая реализация
        try:
            return data.values
        except AttributeError:
            raise TypeError("Ожидается pandas DataFrame")

# Версионная типизация
if sys.version_info >= (3, 10):
    def modern_union(value: int | str) -> str:
        return str(value)
else:
    from typing import Union
    def modern_union(value: Union[int, str]) -> str:
        return str(value)
```

## 🎯 Практические рекомендации

### Лучшие практики

```python
# ✅ Хорошо: Явные типы
def calculate_tax(price: Decimal, rate: Decimal) -> Decimal:
    return price * rate

# ❌ Плохо: Неявные типы
def calculate_tax(price, rate):
    return price * rate

# ✅ Хорошо: Использование Optional
def find_user(user_id: int) -> Optional[User]:
    return users.get(user_id)

# ❌ Плохо: Возврат None без указания
def find_user(user_id: int) -> User:
    return users.get(user_id)  # Может вернуть None!

# ✅ Хорошо: Конкретные типы коллекций
def process_names(names: List[str]) -> Set[str]:
    return {name.lower() for name in names}

# ❌ Плохо: Слишком общие типы
def process_names(names: Any) -> Any:
    return {name.lower() for name in names}
```

### Миграция к типизации

```python
# Этап 1: Добавление типов к новому коду
def new_function(data: List[str]) -> int:
    return len(data)

# Этап 2: Постепенное добавление типов к существующему коду
def existing_function(data):  # type: ignore
    # TODO: Добавить типы
    return len(data)

# Этап 3: Полная типизация
def fully_typed_function(data: List[str]) -> int:
    return len(data)
```

Этот раздел предоставляет полное введение в систему типов Python, от базовых концепций до продвинутых техник. Типизация помогает создавать более надежный и поддерживаемый код, особенно в больших проектах. 