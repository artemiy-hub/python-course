"""
Примеры: Продвинутая типизация и аннотации в Python

Этот файл содержит практические примеры использования продвинутых возможностей
системы типов Python, включая TypeVar, протоколы, условную типизацию и
интеграцию с современными инструментами.
"""

from typing import (
    TypeVar, Generic, Protocol, Union, Optional, Any, Dict, List, Tuple,
    Callable, Iterator, Type, ClassVar, Final, Literal, TypeGuard,
    overload, runtime_checkable, get_type_hints, cast
)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import json

# =============================================================================
# Пример 1: TypeVar с ограничениями и ковариантность
# =============================================================================

# Простой TypeVar
T = TypeVar('T')

# TypeVar с ограничением (bound)
from numbers import Number
NumericType = TypeVar('NumericType', bound=Number)

# TypeVar с ограничениями (constrained)
StringOrInt = TypeVar('StringOrInt', str, int)

# Ковариантный TypeVar (для контейнеров только для чтения)
T_co = TypeVar('T_co', covariant=True)

# Контравариантный TypeVar (для функций-потребителей)
T_contra = TypeVar('T_contra', contravariant=True)

class Container(Generic[T_co]):
    """Контейнер только для чтения (ковариантный)"""
    
    def __init__(self, items: List[T_co]) -> None:
        self._items = items.copy()
    
    def get(self, index: int) -> T_co:
        return self._items[index]
    
    def __iter__(self) -> Iterator[T_co]:
        return iter(self._items)

class Processor(Generic[T_contra]):
    """Процессор данных (контравариантный)"""
    
    def __init__(self, process_func: Callable[[T_contra], None]) -> None:
        self._process_func = process_func
    
    def process(self, item: T_contra) -> None:
        self._process_func(item)

def demonstrate_variance():
    """Демонстрация ковариантности и контравариантности"""
    
    # Ковариантность: Container[Dog] можно использовать как Container[Animal]
    class Animal:
        def make_sound(self) -> str:
            return "Some sound"
    
    class Dog(Animal):
        def make_sound(self) -> str:
            return "Woof!"
    
    dogs = Container([Dog(), Dog()])
    
    # Это работает благодаря ковариантности
    def process_animals(animals: Container[Animal]) -> None:
        for animal in animals:
            print(animal.make_sound())
    
    process_animals(dogs)  # ✅ OK
    
    # Контравариантность: Processor[Animal] можно использовать как Processor[Dog]
    def feed_animal(animal: Animal) -> None:
        print(f"Feeding {type(animal).__name__}")
    
    animal_processor = Processor(feed_animal)
    
    def process_dogs(processor: Processor[Dog]) -> None:
        processor.process(Dog())
    
    process_dogs(animal_processor)  # ✅ OK

# =============================================================================
# Пример 2: Протоколы и структурная типизация
# =============================================================================

@runtime_checkable
class Drawable(Protocol):
    """Протокол для объектов, которые можно рисовать"""
    
    def draw(self) -> str:
        """Рисует объект и возвращает его представление"""
        ...
    
    def get_area(self) -> float:
        """Возвращает площадь объекта"""
        ...

@runtime_checkable
class Serializable(Protocol):
    """Протокол для сериализуемых объектов"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект в словарь"""
        ...
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Serializable':
        """Создает объект из словаря"""
        ...

class Circle:
    """Круг - реализует Drawable без явного наследования"""
    
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def draw(self) -> str:
        return f"Circle with radius {self.radius}"
    
    def get_area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "circle", "radius": self.radius}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Circle':
        return cls(data["radius"])

class Rectangle:
    """Прямоугольник - реализует оба протокола"""
    
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"Rectangle {self.width}x{self.height}"
    
    def get_area(self) -> float:
        return self.width * self.height
    
    def to_dict(self) -> Dict[str, Any]:
        return {"type": "rectangle", "width": self.width, "height": self.height}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rectangle':
        return cls(data["width"], data["height"])

def draw_shapes(shapes: List[Drawable]) -> None:
    """Функция, работающая с любыми объектами, реализующими Drawable"""
    for shape in shapes:
        print(f"{shape.draw()} - Area: {shape.get_area()}")

def demonstrate_protocols():
    """Демонстрация работы с протоколами"""
    
    shapes = [Circle(5), Rectangle(4, 6)]
    draw_shapes(shapes)
    
    # Runtime проверка протоколов
    circle = Circle(3)
    print(f"Circle is Drawable: {isinstance(circle, Drawable)}")
    print(f"Circle is Serializable: {isinstance(circle, Serializable)}")
    
    # Работа с сериализацией
    serializable_shapes = [shape for shape in shapes if isinstance(shape, Serializable)]
    for shape in serializable_shapes:
        data = shape.to_dict()
        print(f"Serialized: {data}")

# =============================================================================
# Пример 3: Type Guards и условная типизация
# =============================================================================

def is_string(value: Any) -> TypeGuard[str]:
    """Type guard для проверки строк"""
    return isinstance(value, str)

def is_int(value: Any) -> TypeGuard[int]:
    """Type guard для проверки целых чисел"""
    return isinstance(value, int)

def is_list_of_strings(value: Any) -> TypeGuard[List[str]]:
    """Type guard для проверки списка строк"""
    return (
        isinstance(value, list) and
        all(isinstance(item, str) for item in value)
    )

@overload
def process_value(value: str) -> str:
    ...

@overload
def process_value(value: int) -> int:
    ...

@overload
def process_value(value: List[str]) -> str:
    ...

def process_value(value: Union[str, int, List[str]]) -> Union[str, int]:
    """Функция с перегрузкой для разных типов"""
    
    if is_string(value):
        # Здесь TypeChecker знает, что value: str
        return value.upper()
    
    elif is_int(value):
        # Здесь TypeChecker знает, что value: int
        return value * 2
    
    elif is_list_of_strings(value):
        # Здесь TypeChecker знает, что value: List[str]
        return ", ".join(value)
    
    else:
        raise ValueError(f"Unsupported type: {type(value)}")

def demonstrate_type_guards():
    """Демонстрация type guards"""
    
    values = [
        "hello",
        42,
        ["apple", "banana", "cherry"],
        ["mixed", 123],  # Это не пройдет type guard
        None
    ]
    
    for value in values:
        try:
            if is_string(value) or is_int(value) or is_list_of_strings(value):
                result = process_value(value)
                print(f"Processed {value} -> {result}")
            else:
                print(f"Cannot process {value}: unsupported type")
        except Exception as e:
            print(f"Error processing {value}: {e}")

# =============================================================================
# Пример 4: Продвинутые Generic типы
# =============================================================================

K = TypeVar('K')
V = TypeVar('V')

class Cache(Generic[K, V]):
    """Типизированный кэш"""
    
    def __init__(self, max_size: int = 100) -> None:
        self._data: Dict[K, V] = {}
        self._max_size = max_size
        self._access_order: List[K] = []
    
    def get(self, key: K) -> Optional[V]:
        """Получить значение по ключу"""
        if key in self._data:
            # Обновляем порядок доступа
            self._access_order.remove(key)
            self._access_order.append(key)
            return self._data[key]
        return None
    
    def put(self, key: K, value: V) -> None:
        """Сохранить значение с ключом"""
        if key in self._data:
            self._access_order.remove(key)
        elif len(self._data) >= self._max_size:
            # Удаляем самый старый элемент
            oldest_key = self._access_order.pop(0)
            del self._data[oldest_key]
        
        self._data[key] = value
        self._access_order.append(key)
    
    def size(self) -> int:
        return len(self._data)

class Repository(Generic[T]):
    """Репозиторий для работы с объектами типа T"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
        self._next_id = 1
    
    def save(self, item: T) -> int:
        """Сохранить объект и вернуть его ID"""
        item_id = self._next_id
        self._next_id += 1
        
        # Добавляем ID к объекту если возможно
        if hasattr(item, 'id'):
            setattr(item, 'id', item_id)
        
        self._items.append(item)
        return item_id
    
    def find_by_id(self, item_id: int) -> Optional[T]:
        """Найти объект по ID"""
        for item in self._items:
            if hasattr(item, 'id') and getattr(item, 'id') == item_id:
                return item
        return None
    
    def find_all(self) -> List[T]:
        """Получить все объекты"""
        return self._items.copy()
    
    def delete(self, item: T) -> bool:
        """Удалить объект"""
        try:
            self._items.remove(item)
            return True
        except ValueError:
            return False

@dataclass
class User:
    name: str
    email: str
    id: Optional[int] = None

def demonstrate_generics():
    """Демонстрация Generic типов"""
    
    # Кэш для разных типов
    string_cache: Cache[str, str] = Cache(max_size=5)
    user_cache: Cache[int, User] = Cache(max_size=10)
    
    # Работа со строковым кэшом
    string_cache.put("key1", "value1")
    string_cache.put("key2", "value2")
    print(f"Retrieved: {string_cache.get('key1')}")
    
    # Работа с пользователями
    user_repo: Repository[User] = Repository()
    
    user1 = User("Alice", "alice@example.com")
    user2 = User("Bob", "bob@example.com")
    
    id1 = user_repo.save(user1)
    id2 = user_repo.save(user2)
    
    print(f"Saved users with IDs: {id1}, {id2}")
    
    found_user = user_repo.find_by_id(id1)
    if found_user:
        print(f"Found user: {found_user.name}")
    
    all_users = user_repo.find_all()
    print(f"Total users: {len(all_users)}")

# =============================================================================
# Пример 5: Интеграция с Pydantic
# =============================================================================

try:
    from pydantic import BaseModel, Field, validator, ValidationError
    
    class Address(BaseModel):
        street: str
        city: str
        country: str
        zip_code: str = Field(..., regex=r'^\d{5}(-\d{4})?$')
    
    class Person(BaseModel):
        name: str = Field(..., min_length=1, max_length=100)
        age: int = Field(..., ge=0, le=150)
        email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
        address: Optional[Address] = None
        tags: List[str] = Field(default_factory=list)
        metadata: Dict[str, Any] = Field(default_factory=dict)
        
        @validator('name')
        def name_must_not_be_empty(cls, v):
            if not v.strip():
                raise ValueError('Name cannot be empty')
            return v.strip().title()
        
        @validator('email')
        def email_must_be_lowercase(cls, v):
            return v.lower()
        
        class Config:
            # Позволяет использовать модель как тип в других аннотациях
            arbitrary_types_allowed = True
            # Валидация при присвоении
            validate_assignment = True
    
    def process_person_data(data: Dict[str, Any]) -> Person:
        """Обработка данных о человеке с валидацией"""
        return Person(**data)
    
    def demonstrate_pydantic_integration():
        """Демонстрация интеграции с Pydantic"""
        
        # Валидные данные
        valid_data = {
            "name": "  john doe  ",
            "age": 30,
            "email": "JOHN.DOE@EXAMPLE.COM",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "country": "USA",
                "zip_code": "12345"
            },
            "tags": ["developer", "python"],
            "metadata": {"department": "IT", "level": "senior"}
        }
        
        try:
            person = process_person_data(valid_data)
            print(f"Created person: {person.name}")
            print(f"Email (normalized): {person.email}")
            print(f"Address: {person.address.city if person.address else 'None'}")
            
            # JSON сериализация
            json_data = person.json()
            print(f"JSON: {json_data}")
            
            # Обратная десериализация
            person2 = Person.parse_raw(json_data)
            print(f"Deserialized: {person2.name}")
            
        except ValidationError as e:
            print(f"Validation error: {e}")
        
        # Невалидные данные
        invalid_data = {
            "name": "",
            "age": -5,
            "email": "invalid-email",
            "address": {
                "street": "123 Main St",
                "city": "Anytown", 
                "country": "USA",
                "zip_code": "invalid"
            }
        }
        
        try:
            person = process_person_data(invalid_data)
        except ValidationError as e:
            print(f"Expected validation error: {e}")
            for error in e.errors():
                print(f"  Field: {error['loc']}, Error: {error['msg']}")

except ImportError:
    def demonstrate_pydantic_integration():
        print("Pydantic not installed. Skipping Pydantic integration example.")

# =============================================================================
# Пример 6: Работа с типами во время выполнения
# =============================================================================

def analyze_type_hints(func: Callable) -> Dict[str, Any]:
    """Анализ аннотаций типов функции"""
    
    hints = get_type_hints(func)
    analysis = {
        "function_name": func.__name__,
        "parameter_types": {},
        "return_type": None,
        "has_type_hints": len(hints) > 0
    }
    
    # Анализируем параметры
    import inspect
    signature = inspect.signature(func)
    
    for param_name, param in signature.parameters.items():
        if param_name in hints:
            param_type = hints[param_name]
            analysis["parameter_types"][param_name] = {
                "type": str(param_type),
                "has_default": param.default != inspect.Parameter.empty,
                "default_value": param.default if param.default != inspect.Parameter.empty else None
            }
    
    # Анализируем возвращаемый тип
    if "return" in hints:
        analysis["return_type"] = str(hints["return"])
    
    return analysis

def typed_function(name: str, age: int, active: bool = True) -> Dict[str, Union[str, int, bool]]:
    """Функция с типами для анализа"""
    return {"name": name, "age": age, "active": active}

def demonstrate_runtime_type_analysis():
    """Демонстрация анализа типов во время выполнения"""
    
    analysis = analyze_type_hints(typed_function)
    
    print("Type analysis:")
    print(f"Function: {analysis['function_name']}")
    print(f"Has type hints: {analysis['has_type_hints']}")
    print(f"Return type: {analysis['return_type']}")
    
    print("Parameters:")
    for param_name, param_info in analysis["parameter_types"].items():
        print(f"  {param_name}: {param_info['type']}")
        if param_info["has_default"]:
            print(f"    Default: {param_info['default_value']}")

# =============================================================================
# Пример 7: Условная типизация и Literal
# =============================================================================

# Literal типы для ограничения значений
Status = Literal["pending", "processing", "completed", "failed"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

@dataclass
class Task:
    id: int
    name: str
    status: Status
    priority: Literal[1, 2, 3, 4, 5] = 3
    
    def update_status(self, new_status: Status) -> None:
        """Обновить статус задачи"""
        print(f"Task {self.id}: {self.status} -> {new_status}")
        self.status = new_status

class Logger:
    """Типизированный логгер"""
    
    def __init__(self, min_level: LogLevel = "INFO") -> None:
        self.min_level = min_level
        self._levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    def _should_log(self, level: LogLevel) -> bool:
        """Проверить, нужно ли логировать сообщение этого уровня"""
        return self._levels.index(level) >= self._levels.index(self.min_level)
    
    def log(self, level: LogLevel, message: str) -> None:
        """Записать сообщение в лог"""
        if self._should_log(level):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
    
    def debug(self, message: str) -> None:
        self.log("DEBUG", message)
    
    def info(self, message: str) -> None:
        self.log("INFO", message)
    
    def warning(self, message: str) -> None:
        self.log("WARNING", message)
    
    def error(self, message: str) -> None:
        self.log("ERROR", message)
    
    def critical(self, message: str) -> None:
        self.log("CRITICAL", message)

def demonstrate_literal_types():
    """Демонстрация Literal типов"""
    
    # Создание задач
    task1 = Task(1, "Setup database", "pending")
    task2 = Task(2, "Write tests", "processing", priority=2)
    
    # Обновление статусов (только валидные значения)
    task1.update_status("processing")
    task1.update_status("completed")
    
    # Работа с логгером
    logger = Logger("WARNING")
    
    logger.debug("This won't be shown")
    logger.info("This won't be shown either")
    logger.warning("This will be shown")
    logger.error("This will definitely be shown")

# =============================================================================
# Пример 8: Продвинутые паттерны типизации
# =============================================================================

# Final типы
class Configuration:
    """Конфигурация с Final полями"""
    
    API_VERSION: Final[str] = "v1"
    MAX_CONNECTIONS: Final[int] = 100
    DEFAULT_TIMEOUT: Final[float] = 30.0
    
    def __init__(self) -> None:
        self.base_url: str = "https://api.example.com"
        self.debug_mode: bool = False

# Абстрактный базовый класс с типизацией
class DataProcessor(ABC, Generic[T]):
    """Абстрактный процессор данных"""
    
    @abstractmethod
    def process(self, data: T) -> T:
        """Обработать данные"""
        pass
    
    @abstractmethod
    def validate(self, data: T) -> bool:
        """Валидировать данные"""
        pass

class StringProcessor(DataProcessor[str]):
    """Процессор строк"""
    
    def process(self, data: str) -> str:
        return data.strip().upper()
    
    def validate(self, data: str) -> bool:
        return isinstance(data, str) and len(data) > 0

class NumberProcessor(DataProcessor[float]):
    """Процессор чисел"""
    
    def process(self, data: float) -> float:
        return round(data, 2)
    
    def validate(self, data: float) -> bool:
        return isinstance(data, (int, float)) and data >= 0

def process_data_safely(processor: DataProcessor[T], data: T) -> Optional[T]:
    """Безопасная обработка данных с валидацией"""
    if processor.validate(data):
        return processor.process(data)
    return None

def demonstrate_advanced_patterns():
    """Демонстрация продвинутых паттернов типизации"""
    
    # Работа с Final типами
    config = Configuration()
    print(f"API Version: {config.API_VERSION}")
    print(f"Max connections: {config.MAX_CONNECTIONS}")
    
    # Работа с Generic абстрактными классами
    string_processor = StringProcessor()
    number_processor = NumberProcessor()
    
    # Обработка строк
    result1 = process_data_safely(string_processor, "  hello world  ")
    print(f"Processed string: {result1}")
    
    result2 = process_data_safely(string_processor, "")
    print(f"Empty string result: {result2}")
    
    # Обработка чисел
    result3 = process_data_safely(number_processor, 3.14159)
    print(f"Processed number: {result3}")
    
    result4 = process_data_safely(number_processor, -5.0)
    print(f"Negative number result: {result4}")

# =============================================================================
# Главная функция для демонстрации всех примеров
# =============================================================================

def main():
    """Запуск всех примеров"""
    
    print("=== Продвинутая типизация и аннотации в Python ===\n")
    
    print("1. Демонстрация ковариантности и контравариантности:")
    demonstrate_variance()
    print()
    
    print("2. Демонстрация протоколов:")
    demonstrate_protocols()
    print()
    
    print("3. Демонстрация Type Guards:")
    demonstrate_type_guards()
    print()
    
    print("4. Демонстрация Generic типов:")
    demonstrate_generics()
    print()
    
    print("5. Демонстрация интеграции с Pydantic:")
    demonstrate_pydantic_integration()
    print()
    
    print("6. Демонстрация анализа типов во время выполнения:")
    demonstrate_runtime_type_analysis()
    print()
    
    print("7. Демонстрация Literal типов:")
    demonstrate_literal_types()
    print()
    
    print("8. Демонстрация продвинутых паттернов:")
    demonstrate_advanced_patterns()

if __name__ == "__main__":
    main() 