# Теория: Продвинутая типизация и аннотации в Python

## 🎯 Цель раздела

Этот раздел углубляется в продвинутые аспекты системы типов Python, включая современные возможности типизации, практические паттерны использования типов в реальных проектах, и интеграцию с современными инструментами разработки.

## 📋 Содержание

1. [Продвинутые аннотации типов](#продвинутые-аннотации-типов)
2. [Dataclasses и типизация](#dataclasses-и-типизация)
3. [Протоколы и структурная типизация](#протоколы-и-структурная-типизация)
4. [Обобщенные типы в реальных проектах](#обобщенные-типы-в-реальных-проектах)
5. [Типизация асинхронного кода](#типизация-асинхронного-кода)
6. [Интеграция с IDE и инструментами](#интеграция-с-ide-и-инструментами)
7. [Миграция к типизации](#миграция-к-типизации)

---

## 🚀 Продвинутые аннотации типов

### TypeVar с ограничениями и связыванием

```python
from typing import TypeVar, Protocol, Union, overload
from abc import abstractmethod

# Ограниченный TypeVar
Number = TypeVar('Number', int, float, complex)

def add_numbers(a: Number, b: Number) -> Number:
    """Сложение чисел с сохранением типа"""
    return a + b

# Bound TypeVar
class Comparable(Protocol):
    @abstractmethod
    def __lt__(self, other) -> bool: ...

T = TypeVar('T', bound=Comparable)

def sort_items(items: list[T]) -> list[T]:
    """Сортировка сравнимых элементов"""
    return sorted(items)

# Variance в типах
from typing import TypeVar, Generic, Callable

T_co = TypeVar('T_co', covariant=True)  # Ковариантный
T_contra = TypeVar('T_contra', contravariant=True)  # Контрвариантный

class Producer(Generic[T_co]):
    """Производитель данных (только возвращает T)"""
    def produce(self) -> T_co: ...

class Consumer(Generic[T_contra]):
    """Потребитель данных (только принимает T)"""
    def consume(self, item: T_contra) -> None: ...
```

### Условная типизация и Type Guards

```python
from typing import TypeGuard, Union, Any, cast
import sys

def is_string_list(val: list[Any]) -> TypeGuard[list[str]]:
    """Type guard для проверки списка строк"""
    return all(isinstance(x, str) for x in val)

def process_strings(items: list[Any]) -> None:
    """Обработка элементов с проверкой типов"""
    if is_string_list(items):
        # Теперь mypy знает, что items: list[str]
        for item in items:
            print(item.upper())  # Безопасно вызывать строковые методы

# Условная типизация на основе версии Python
if sys.version_info >= (3, 10):
    from typing import TypeAlias
    JSONValue: TypeAlias = Union[str, int, float, bool, None, 
                                dict[str, 'JSONValue'], 
                                list['JSONValue']]
else:
    from typing import Dict, List
    JSONValue = Union[str, int, float, bool, None, 
                     Dict[str, 'JSONValue'], 
                     List['JSONValue']]

# Прямая аннотация (Forward Reference)
class Node:
    def __init__(self, value: int, parent: 'Node | None' = None):
        self.value = value
        self.parent = parent
        self.children: list['Node'] = []
```

### Literal типы и перечисления

```python
from typing import Literal, Union
from enum import Enum, auto

# Literal типы для точного управления значениями
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

def make_request(method: HttpMethod, url: str) -> dict[str, Any]:
    """HTTP запрос с типизированным методом"""
    ...

# Комбинирование Literal с Enum
class Status(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()

StatusLiteral = Literal[Status.PENDING, Status.PROCESSING, 
                       Status.COMPLETED, Status.FAILED]

# Literal для версионирования API
APIVersion = Literal["v1", "v2", "v3"]

def handle_api_request(version: APIVersion, data: dict) -> dict:
    """Обработка API запроса с версионированием"""
    if version == "v1":
        return handle_v1(data)
    elif version == "v2":
        return handle_v2(data)
    elif version == "v3":
        return handle_v3(data)
```

---

## 📦 Dataclasses и типизация

### Продвинутое использование dataclasses

```python
from dataclasses import dataclass, field, InitVar, asdict, astuple
from typing import ClassVar, Optional, Any, Dict, List
from datetime import datetime
import json

@dataclass(frozen=True, order=True)
class Point:
    """Неизменяемая точка с возможностью сравнения"""
    x: float
    y: float
    z: float = 0.0
    
    def distance_to(self, other: 'Point') -> float:
        """Расстояние до другой точки"""
        return ((self.x - other.x) ** 2 + 
                (self.y - other.y) ** 2 + 
                (self.z - other.z) ** 2) ** 0.5

@dataclass
class User:
    """Пользователь с валидацией и метаданными"""
    
    # Обычные поля
    id: int
    username: str
    email: str
    
    # Поля с значениями по умолчанию
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    # Поля, исключенные из определенных операций
    password_hash: str = field(repr=False, compare=False)
    login_count: int = field(default=0, compare=False)
    
    # Поля с фабричными функциями
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Классовые переменные
    _instances: ClassVar[Dict[int, 'User']] = {}
    
    # InitVar для данных инициализации
    initial_password: InitVar[Optional[str]] = None
    
    def __post_init__(self, initial_password: Optional[str]):
        """Пост-инициализация с валидацией"""
        if not self.username or len(self.username) < 3:
            raise ValueError("Username должен содержать минимум 3 символа")
        
        if "@" not in self.email:
            raise ValueError("Некорректный email")
        
        if initial_password:
            self.password_hash = self._hash_password(initial_password)
        
        # Регистрируем пользователя
        User._instances[self.id] = self
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Хеширование пароля (упрощенная версия)"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Сериализация в словарь"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Сериализация в JSON"""
        data = self.to_dict()
        # Преобразуем datetime в ISO формат
        data['created_at'] = self.created_at.isoformat()
        return json.dumps(data, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Десериализация из словаря"""
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)

# Наследование dataclasses
@dataclass
class AdminUser(User):
    """Администратор с дополнительными правами"""
    
    permissions: List[str] = field(default_factory=list)
    super_admin: bool = False
    
    def __post_init__(self, initial_password: Optional[str]):
        """Расширенная пост-инициализация"""
        super().__post_init__(initial_password)
        
        # Добавляем базовые права администратора
        if not self.permissions:
            self.permissions = ["read", "write", "delete"]

# Dataclass с кастомными методами сравнения
@dataclass
class Version:
    """Версия с семантическим сравнением"""
    major: int
    minor: int
    patch: int
    pre_release: Optional[str] = None
    
    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre_release:
            version += f"-{self.pre_release}"
        return version
    
    def __lt__(self, other: 'Version') -> bool:
        """Семантическое сравнение версий"""
        if not isinstance(other, Version):
            return NotImplemented
        
        # Сравниваем основные компоненты
        self_tuple = (self.major, self.minor, self.patch)
        other_tuple = (other.major, other.minor, other.patch)
        
        if self_tuple != other_tuple:
            return self_tuple < other_tuple
        
        # Если основные версии равны, сравниваем pre-release
        if self.pre_release is None and other.pre_release is None:
            return False
        if self.pre_release is None:
            return False  # Релиз больше pre-release
        if other.pre_release is None:
            return True   # pre-release меньше релиза
        
        return self.pre_release < other.pre_release
```

### Интеграция с Pydantic

```python
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, validator, Field
from enum import Enum

class UserRole(str, Enum):
    """Роли пользователей"""
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class UserProfile(BaseModel):
    """Профиль пользователя с валидацией Pydantic"""
    
    id: int = Field(..., gt=0, description="Уникальный идентификатор")
    username: str = Field(..., min_length=3, max_length=50, 
                         regex=r'^[a-zA-Z0-9_]+$')
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    full_name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=13, le=120)
    role: UserRole = UserRole.USER
    tags: List[str] = Field(default_factory=list, max_items=10)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    
    class Config:
        """Конфигурация модели"""
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "age": 30,
                "role": "user",
                "tags": ["python", "developer"],
                "is_active": True
            }
        }
    
    @validator('username')
    def username_must_not_contain_spaces(cls, v):
        """Валидация username"""
        if ' ' in v:
            raise ValueError('Username не должен содержать пробелы')
        return v.lower()
    
    @validator('tags')
    def validate_tags(cls, v):
        """Валидация тегов"""
        if v:
            # Удаляем дубликаты и приводим к нижнему регистру
            return list(set(tag.lower().strip() for tag in v if tag.strip()))
        return v
    
    @validator('full_name')
    def validate_full_name(cls, v):
        """Валидация полного имени"""
        # Удаляем лишние пробелы
        return ' '.join(v.split())
    
    def is_admin(self) -> bool:
        """Проверка на администратора"""
        return self.role == UserRole.ADMIN
    
    def add_tag(self, tag: str) -> None:
        """Добавление тега"""
        if tag and tag.lower() not in self.tags:
            self.tags.append(tag.lower())
    
    def to_dict(self) -> Dict[str, Any]:
        """Сериализация в словарь"""
        return self.dict()
    
    def to_json(self) -> str:
        """Сериализация в JSON"""
        return self.json(ensure_ascii=False)
```

---

## 🔗 Протоколы и структурная типизация

### Продвинутые протоколы

```python
from typing import Protocol, runtime_checkable, TypeVar, Generic
from abc import abstractmethod

# Базовые протоколы
@runtime_checkable
class Drawable(Protocol):
    """Протокол для рисуемых объектов"""
    
    def draw(self) -> str:
        """Нарисовать объект"""
        ...
    
    def get_bounds(self) -> tuple[float, float, float, float]:
        """Получить границы объекта (x, y, width, height)"""
        ...

@runtime_checkable
class Serializable(Protocol):
    """Протокол для сериализуемых объектов"""
    
    def serialize(self) -> dict[str, Any]:
        """Сериализовать объект"""
        ...
    
    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> 'Serializable':
        """Десериализовать объект"""
        ...

# Обобщенные протоколы
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Container(Protocol, Generic[T]):
    """Протокол контейнера"""
    
    def add(self, item: T) -> None:
        """Добавить элемент"""
        ...
    
    def remove(self, item: T) -> bool:
        """Удалить элемент"""
        ...
    
    def __contains__(self, item: T) -> bool:
        """Проверить наличие элемента"""
        ...
    
    def __len__(self) -> int:
        """Количество элементов"""
        ...

class Mapping(Protocol, Generic[K, V]):
    """Протокол отображения"""
    
    def __getitem__(self, key: K) -> V: ...
    def __setitem__(self, key: K, value: V) -> None: ...
    def __delitem__(self, key: K) -> None: ...
    def __contains__(self, key: K) -> bool: ...
    def keys(self) -> Iterator[K]: ...
    def values(self) -> Iterator[V]: ...
    def items(self) -> Iterator[tuple[K, V]]: ...

# Протокол с callback'ами
class EventHandler(Protocol):
    """Протокол обработчика событий"""
    
    def handle_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Обработать событие"""
        ...

class Observable(Protocol):
    """Протокол наблюдаемого объекта"""
    
    def add_handler(self, handler: EventHandler) -> None:
        """Добавить обработчик"""
        ...
    
    def remove_handler(self, handler: EventHandler) -> None:
        """Удалить обработчик"""
        ...
    
    def notify(self, event_type: str, data: dict[str, Any]) -> None:
        """Уведомить обработчики"""
        ...

# Протокол для работы с ресурсами
class Resource(Protocol):
    """Протокол ресурса"""
    
    def acquire(self) -> None:
        """Захватить ресурс"""
        ...
    
    def release(self) -> None:
        """Освободить ресурс"""
        ...
    
    def __enter__(self) -> 'Resource':
        """Вход в контекстный менеджер"""
        ...
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Выход из контекстного менеджера"""
        ...

# Композиция протоколов
class DrawableSerializable(Drawable, Serializable, Protocol):
    """Объект, который можно рисовать и сериализовать"""
    pass

# Конкретные реализации
class Circle:
    """Круг - реализует протоколы неявно"""
    
    def __init__(self, x: float, y: float, radius: float):
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self) -> str:
        return f"Круг в ({self.x}, {self.y}) радиусом {self.radius}"
    
    def get_bounds(self) -> tuple[float, float, float, float]:
        return (self.x - self.radius, self.y - self.radius, 
                2 * self.radius, 2 * self.radius)
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "circle",
            "x": self.x,
            "y": self.y,
            "radius": self.radius
        }
    
    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> 'Circle':
        return cls(data["x"], data["y"], data["radius"])

# Использование протоколов в функциях
def render_objects(objects: list[Drawable]) -> list[str]:
    """Рендеринг объектов"""
    return [obj.draw() for obj in objects]

def save_objects(objects: list[Serializable], filename: str) -> None:
    """Сохранение объектов в файл"""
    import json
    data = [obj.serialize() for obj in objects]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_container(container: Container[str], items: list[str]) -> None:
    """Обработка контейнера"""
    for item in items:
        container.add(item)
    
    print(f"Контейнер содержит {len(container)} элементов")
    
    if "test" in container:
        container.remove("test")
```

---

## 🎯 Обобщенные типы в реальных проектах

### Система кэширования с типами

```python
from typing import TypeVar, Generic, Optional, Dict, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import weakref
import threading
from abc import ABC, abstractmethod

K = TypeVar('K')  # Тип ключа
V = TypeVar('V')  # Тип значения

@dataclass(frozen=True)
class CacheEntry(Generic[V]):
    """Запись в кэше"""
    value: V
    created_at: datetime
    expires_at: Optional[datetime] = None
    hit_count: int = 0
    
    def is_expired(self) -> bool:
        """Проверка истечения срока"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def with_hit(self) -> 'CacheEntry[V]':
        """Создать новую запись с увеличенным счетчиком обращений"""
        return CacheEntry(
            value=self.value,
            created_at=self.created_at,
            expires_at=self.expires_at,
            hit_count=self.hit_count + 1
        )

class CacheStrategy(ABC, Generic[K, V]):
    """Абстрактная стратегия кэширования"""
    
    @abstractmethod
    def should_evict(self, key: K, entry: CacheEntry[V], 
                    cache_size: int, max_size: int) -> bool:
        """Определить, следует ли удалить запись"""
        ...

class LRUStrategy(CacheStrategy[K, V]):
    """Стратегия LRU (Least Recently Used)"""
    
    def __init__(self):
        self.access_times: Dict[K, datetime] = {}
    
    def should_evict(self, key: K, entry: CacheEntry[V], 
                    cache_size: int, max_size: int) -> bool:
        """LRU логика удаления"""
        if cache_size <= max_size:
            return False
        
        # Находим самую старую запись
        oldest_key = min(self.access_times.keys(), 
                        key=lambda k: self.access_times[k])
        return key == oldest_key
    
    def record_access(self, key: K) -> None:
        """Записать время доступа"""
        self.access_times[key] = datetime.now()
    
    def remove_key(self, key: K) -> None:
        """Удалить ключ из отслеживания"""
        self.access_times.pop(key, None)

class TTLStrategy(CacheStrategy[K, V]):
    """Стратегия TTL (Time To Live)"""
    
    def should_evict(self, key: K, entry: CacheEntry[V], 
                    cache_size: int, max_size: int) -> bool:
        """TTL логика удаления"""
        return entry.is_expired()

class Cache(Generic[K, V]):
    """Типизированный кэш с различными стратегиями"""
    
    def __init__(self, 
                 max_size: int = 1000,
                 default_ttl: Optional[timedelta] = None,
                 strategy: Optional[CacheStrategy[K, V]] = None):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.strategy = strategy or LRUStrategy[K, V]()
        
        self._cache: Dict[K, CacheEntry[V]] = {}
        self._lock = threading.RLock()
        
        # Статистика
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
    
    def get(self, key: K) -> Optional[V]:
        """Получить значение из кэша"""
        with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                self.stats["misses"] += 1
                return None
            
            if entry.is_expired():
                del self._cache[key]
                if hasattr(self.strategy, 'remove_key'):
                    self.strategy.remove_key(key)
                self.stats["misses"] += 1
                return None
            
            # Обновляем статистику
            self._cache[key] = entry.with_hit()
            if hasattr(self.strategy, 'record_access'):
                self.strategy.record_access(key)
            
            self.stats["hits"] += 1
            return entry.value
    
    def put(self, key: K, value: V, ttl: Optional[timedelta] = None) -> None:
        """Добавить значение в кэш"""
        with self._lock:
            # Определяем время истечения
            expires_at = None
            if ttl or self.default_ttl:
                expires_at = datetime.now() + (ttl or self.default_ttl)
            
            entry = CacheEntry(
                value=value,
                created_at=datetime.now(),
                expires_at=expires_at
            )
            
            self._cache[key] = entry
            if hasattr(self.strategy, 'record_access'):
                self.strategy.record_access(key)
            
            # Проверяем необходимость удаления
            self._evict_if_needed()
    
    def _evict_if_needed(self) -> None:
        """Удалить записи при необходимости"""
        keys_to_remove = []
        
        for key, entry in self._cache.items():
            if self.strategy.should_evict(key, entry, 
                                        len(self._cache), self.max_size):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self._cache[key]
            if hasattr(self.strategy, 'remove_key'):
                self.strategy.remove_key(key)
            self.stats["evictions"] += 1
    
    def clear(self) -> None:
        """Очистить кэш"""
        with self._lock:
            self._cache.clear()
            if hasattr(self.strategy, 'access_times'):
                self.strategy.access_times.clear()
    
    def size(self) -> int:
        """Размер кэша"""
        return len(self._cache)
    
    def hit_ratio(self) -> float:
        """Коэффициент попаданий"""
        total = self.stats["hits"] + self.stats["misses"]
        return self.stats["hits"] / total if total > 0 else 0.0

# Декоратор для кэширования функций
def cached(cache: Cache[str, Any], 
          ttl: Optional[timedelta] = None) -> Callable:
    """Декоратор для кэширования результатов функций"""
    
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Создаем ключ кэша
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Проверяем кэш
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Вычисляем результат
            result = func(*args, **kwargs)
            
            # Сохраняем в кэш
            cache.put(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator
```

### Система событий с типизацией

```python
from typing import TypeVar, Generic, Callable, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
import asyncio
from enum import Enum

# Типы событий
EventType = TypeVar('EventType')
EventData = TypeVar('EventData')

@dataclass(frozen=True)
class Event(Generic[EventData]):
    """Типизированное событие"""
    type: str
    data: EventData
    timestamp: datetime = datetime.now()
    source: str = "unknown"
    correlation_id: Optional[str] = None
    
    def with_correlation_id(self, correlation_id: str) -> 'Event[EventData]':
        """Создать событие с correlation ID"""
        return Event(
            type=self.type,
            data=self.data,
            timestamp=self.timestamp,
            source=self.source,
            correlation_id=correlation_id
        )

# Обработчики событий
EventHandler = Callable[[Event[EventData]], None]
AsyncEventHandler = Callable[[Event[EventData]], Awaitable[None]]

class EventBus(Generic[EventData]):
    """Типизированная шина событий"""
    
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler[EventData]]] = {}
        self._async_handlers: Dict[str, List[AsyncEventHandler[EventData]]] = {}
        self._middleware: List[Callable[[Event[EventData]], Event[EventData]]] = []
        
    def subscribe(self, event_type: str, 
                 handler: EventHandler[EventData]) -> None:
        """Подписаться на события"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def subscribe_async(self, event_type: str, 
                       handler: AsyncEventHandler[EventData]) -> None:
        """Подписаться на события (асинхронно)"""
        if event_type not in self._async_handlers:
            self._async_handlers[event_type] = []
        self._async_handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, 
                   handler: EventHandler[EventData]) -> None:
        """Отписаться от событий"""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
            except ValueError:
                pass
    
    def add_middleware(self, 
                      middleware: Callable[[Event[EventData]], Event[EventData]]) -> None:
        """Добавить middleware"""
        self._middleware.append(middleware)
    
    def publish(self, event: Event[EventData]) -> None:
        """Опубликовать событие"""
        # Применяем middleware
        processed_event = event
        for middleware in self._middleware:
            processed_event = middleware(processed_event)
        
        # Уведомляем обработчиков
        handlers = self._handlers.get(processed_event.type, [])
        for handler in handlers:
            try:
                handler(processed_event)
            except Exception as e:
                print(f"Ошибка в обработчике события: {e}")
    
    async def publish_async(self, event: Event[EventData]) -> None:
        """Опубликовать событие асинхронно"""
        # Применяем middleware
        processed_event = event
        for middleware in self._middleware:
            processed_event = middleware(processed_event)
        
        # Уведомляем синхронных обработчиков
        self.publish(processed_event)
        
        # Уведомляем асинхронных обработчиков
        async_handlers = self._async_handlers.get(processed_event.type, [])
        if async_handlers:
            tasks = [handler(processed_event) for handler in async_handlers]
            await asyncio.gather(*tasks, return_exceptions=True)

# Конкретные типы событий
@dataclass
class UserEvent:
    """События пользователя"""
    user_id: int
    action: str
    details: Dict[str, Any]

@dataclass
class SystemEvent:
    """Системные события"""
    component: str
    level: str
    message: str
    metadata: Dict[str, Any]

# Специализированные шины событий
UserEventBus = EventBus[UserEvent]
SystemEventBus = EventBus[SystemEvent]

# Пример использования
def create_event_system():
    """Создание системы событий"""
    
    # Создаем шины событий
    user_bus = UserEventBus()
    system_bus = SystemEventBus()
    
    # Обработчики пользовательских событий
    def handle_user_login(event: Event[UserEvent]) -> None:
        print(f"Пользователь {event.data.user_id} вошел в систему")
    
    def handle_user_logout(event: Event[UserEvent]) -> None:
        print(f"Пользователь {event.data.user_id} вышел из системы")
    
    # Асинхронные обработчики
    async def log_user_activity(event: Event[UserEvent]) -> None:
        # Имитация записи в БД
        await asyncio.sleep(0.1)
        print(f"Активность пользователя {event.data.user_id} записана в БД")
    
    # Подписываемся на события
    user_bus.subscribe("user.login", handle_user_login)
    user_bus.subscribe("user.logout", handle_user_logout)
    user_bus.subscribe_async("user.login", log_user_activity)
    user_bus.subscribe_async("user.logout", log_user_activity)
    
    # Middleware для логирования
    def logging_middleware(event: Event[UserEvent]) -> Event[UserEvent]:
        print(f"[LOG] Событие: {event.type} в {event.timestamp}")
        return event
    
    user_bus.add_middleware(logging_middleware)
    
    return user_bus, system_bus
```

Этот раздел представляет продвинутые концепции типизации Python, включая современные возможности языка, интеграцию с реальными проектами и практические паттерны использования типов для создания надежного и поддерживаемого кода. 