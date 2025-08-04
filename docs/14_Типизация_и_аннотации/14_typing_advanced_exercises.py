"""
Упражнения: Продвинутая типизация и аннотации в Python

Этот файл содержит практические упражнения для изучения продвинутых возможностей
системы типов Python. Каждое упражнение включает задание, решение и тесты.
"""

from typing import (
    TypeVar, Generic, Protocol, Union, Optional, Any, Dict, List, Tuple,
    Callable, Iterator, Type, ClassVar, Final, Literal, TypeGuard,
    overload, runtime_checkable, get_type_hints
)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import unittest

# =============================================================================
# Упражнение 1: Создание Generic Repository с TypeVar
# =============================================================================

"""
ЗАДАНИЕ 1: Generic Repository Pattern

Создайте типизированный репозиторий, который может работать с любыми объектами.
Требования:
1. Используйте TypeVar для обеспечения типобезопасности
2. Объекты должны иметь поле 'id' (используйте bound TypeVar)
3. Реализуйте методы: save, find_by_id, find_all, delete
4. Добавьте метод filter с предикатом
"""

# Ваш код здесь:
T = TypeVar('T', bound=object)  # Замените на правильный bound

class Identifiable(Protocol):
    """Протокол для объектов с ID"""
    id: Optional[int]

IdentifiableT = TypeVar('IdentifiableT', bound=Identifiable)

class Repository(Generic[IdentifiableT]):
    """Типизированный репозиторий"""
    
    def __init__(self) -> None:
        self._items: List[IdentifiableT] = []
        self._next_id = 1
    
    def save(self, item: IdentifiableT) -> IdentifiableT:
        """
        Сохранить объект в репозитории
        Если у объекта нет ID, присвоить новый
        """
        # TODO: Реализуйте метод
        pass
    
    def find_by_id(self, item_id: int) -> Optional[IdentifiableT]:
        """Найти объект по ID"""
        # TODO: Реализуйте метод
        pass
    
    def find_all(self) -> List[IdentifiableT]:
        """Получить все объекты"""
        # TODO: Реализуйте метод
        pass
    
    def delete(self, item_id: int) -> bool:
        """Удалить объект по ID"""
        # TODO: Реализуйте метод
        pass
    
    def filter(self, predicate: Callable[[IdentifiableT], bool]) -> List[IdentifiableT]:
        """Фильтровать объекты по предикату"""
        # TODO: Реализуйте метод
        pass

# Тестовые классы
@dataclass
class User:
    name: str
    email: str
    id: Optional[int] = None

@dataclass 
class Product:
    title: str
    price: float
    id: Optional[int] = None

# Решение:
class RepositorySolution(Generic[IdentifiableT]):
    """Решение: Типизированный репозиторий"""
    
    def __init__(self) -> None:
        self._items: List[IdentifiableT] = []
        self._next_id = 1
    
    def save(self, item: IdentifiableT) -> IdentifiableT:
        if item.id is None:
            item.id = self._next_id
            self._next_id += 1
            self._items.append(item)
        else:
            # Обновляем существующий
            for i, existing in enumerate(self._items):
                if existing.id == item.id:
                    self._items[i] = item
                    break
            else:
                self._items.append(item)
        return item
    
    def find_by_id(self, item_id: int) -> Optional[IdentifiableT]:
        for item in self._items:
            if item.id == item_id:
                return item
        return None
    
    def find_all(self) -> List[IdentifiableT]:
        return self._items.copy()
    
    def delete(self, item_id: int) -> bool:
        for i, item in enumerate(self._items):
            if item.id == item_id:
                del self._items[i]
                return True
        return False
    
    def filter(self, predicate: Callable[[IdentifiableT], bool]) -> List[IdentifiableT]:
        return [item for item in self._items if predicate(item)]

# =============================================================================
# Упражнение 2: Protocol и structural typing
# =============================================================================

"""
ЗАДАНИЕ 2: Система уведомлений с протоколами

Создайте систему уведомлений, используя протоколы для определения интерфейсов.
Требования:
1. Создайте протокол Notifiable с методом send_notification
2. Создайте протокол Formattable с методом format_message
3. Реализуйте классы: EmailNotifier, SMSNotifier, PushNotifier
4. Создайте NotificationService, который работает с любыми Notifiable объектами
5. Используйте @runtime_checkable для возможности проверки isinstance
"""

# Ваши протоколы здесь:
@runtime_checkable
class Notifiable(Protocol):
    """Протокол для отправки уведомлений"""
    # TODO: Определите метод send_notification
    pass

@runtime_checkable
class Formattable(Protocol):
    """Протокол для форматирования сообщений"""
    # TODO: Определите метод format_message
    pass

# Ваши реализации здесь:
class EmailNotifier:
    """Уведомления по email"""
    # TODO: Реализуйте класс
    pass

class SMSNotifier:
    """SMS уведомления"""
    # TODO: Реализуйте класс
    pass

class NotificationService:
    """Сервис уведомлений"""
    # TODO: Реализуйте класс
    pass

# Решение:
@runtime_checkable
class NotifiableSolution(Protocol):
    def send_notification(self, recipient: str, message: str) -> bool:
        """Отправить уведомление получателю"""
        ...

@runtime_checkable
class FormattableSolution(Protocol):
    def format_message(self, template: str, **kwargs: Any) -> str:
        """Форматировать сообщение по шаблону"""
        ...

class EmailNotifierSolution:
    def send_notification(self, recipient: str, message: str) -> bool:
        print(f"📧 Email to {recipient}: {message}")
        return True
    
    def format_message(self, template: str, **kwargs: Any) -> str:
        return f"[EMAIL] {template.format(**kwargs)}"

class SMSNotifierSolution:
    def send_notification(self, recipient: str, message: str) -> bool:
        if len(message) > 160:
            print(f"📱 SMS to {recipient}: {message[:157]}...")
        else:
            print(f"📱 SMS to {recipient}: {message}")
        return True
    
    def format_message(self, template: str, **kwargs: Any) -> str:
        formatted = template.format(**kwargs)
        return formatted[:160]  # SMS limit

class NotificationServiceSolution:
    def __init__(self) -> None:
        self.notifiers: List[NotifiableSolution] = []
    
    def add_notifier(self, notifier: NotifiableSolution) -> None:
        if isinstance(notifier, NotifiableSolution):
            self.notifiers.append(notifier)
        else:
            raise TypeError("Notifier must implement Notifiable protocol")
    
    def send_to_all(self, recipient: str, message: str) -> List[bool]:
        results = []
        for notifier in self.notifiers:
            # Форматируем сообщение если возможно
            if isinstance(notifier, FormattableSolution):
                formatted_message = notifier.format_message(message, recipient=recipient)
            else:
                formatted_message = message
            
            result = notifier.send_notification(recipient, formatted_message)
            results.append(result)
        return results

# =============================================================================
# Упражнение 3: Type Guards и условная типизация
# =============================================================================

"""
ЗАДАНИЕ 3: Система валидации данных с Type Guards

Создайте систему валидации данных с использованием TypeGuard.
Требования:
1. Создайте type guards для различных типов данных
2. Реализуйте функцию validate_user_data с overload
3. Используйте Union типы и условную типизацию
4. Добавьте валидацию для email, phone, age
"""

# Ваши type guards здесь:
def is_valid_email(value: Any) -> TypeGuard[str]:
    """Type guard для проверки email"""
    # TODO: Реализуйте проверку email
    pass

def is_valid_phone(value: Any) -> TypeGuard[str]:
    """Type guard для проверки телефона"""
    # TODO: Реализуйте проверку телефона
    pass

def is_valid_age(value: Any) -> TypeGuard[int]:
    """Type guard для проверки возраста"""
    # TODO: Реализуйте проверку возраста
    pass

# Ваши overload функции здесь:
UserData = Union[str, int, Dict[str, Any]]

@overload
def validate_user_data(data: str, field_type: Literal["email"]) -> str: ...

@overload
def validate_user_data(data: str, field_type: Literal["phone"]) -> str: ...

@overload
def validate_user_data(data: int, field_type: Literal["age"]) -> int: ...

def validate_user_data(data: UserData, field_type: str) -> Any:
    """Валидация пользовательских данных"""
    # TODO: Реализуйте функцию
    pass

# Решение:
import re

def is_valid_email_solution(value: Any) -> TypeGuard[str]:
    if not isinstance(value, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, value))

def is_valid_phone_solution(value: Any) -> TypeGuard[str]:
    if not isinstance(value, str):
        return False
    # Простая проверка российского номера
    pattern = r'^(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
    return bool(re.match(pattern, value.replace(' ', '').replace('-', '')))

def is_valid_age_solution(value: Any) -> TypeGuard[int]:
    return isinstance(value, int) and 0 <= value <= 150

def validate_user_data_solution(data: UserData, field_type: str) -> Any:
    if field_type == "email":
        if is_valid_email_solution(data):
            return data.lower().strip()
        raise ValueError(f"Invalid email: {data}")
    
    elif field_type == "phone":
        if is_valid_phone_solution(data):
            # Нормализуем номер
            normalized = re.sub(r'[\s\-\(\)]', '', str(data))
            if normalized.startswith('8'):
                normalized = '+7' + normalized[1:]
            elif not normalized.startswith('+7'):
                normalized = '+7' + normalized
            return normalized
        raise ValueError(f"Invalid phone: {data}")
    
    elif field_type == "age":
        if is_valid_age_solution(data):
            return data
        raise ValueError(f"Invalid age: {data}")
    
    else:
        raise ValueError(f"Unknown field type: {field_type}")

# =============================================================================
# Упражнение 4: Продвинутые Generic типы
# =============================================================================

"""
ЗАДАНИЕ 4: Система кэширования с продвинутыми Generic

Создайте продвинутую систему кэширования с использованием Generic типов.
Требования:
1. Создайте Generic класс Cache с ключом K и значением V
2. Реализуйте разные стратегии вытеснения (LRU, FIFO, LFU)
3. Используйте Protocol для определения интерфейса стратегии
4. Добавьте декоратор для кэширования функций
"""

K = TypeVar('K')
V = TypeVar('V')

class EvictionStrategy(Protocol[K]):
    """Протокол для стратегий вытеснения"""
    # TODO: Определите методы протокола
    pass

class Cache(Generic[K, V]):
    """Продвинутый кэш с различными стратегиями"""
    
    def __init__(self, max_size: int, strategy: EvictionStrategy[K]) -> None:
        # TODO: Реализуйте инициализацию
        pass
    
    def get(self, key: K) -> Optional[V]:
        """Получить значение по ключу"""
        # TODO: Реализуйте метод
        pass
    
    def put(self, key: K, value: V) -> None:
        """Сохранить значение с ключом"""
        # TODO: Реализуйте метод
        pass
    
    def clear(self) -> None:
        """Очистить кэш"""
        # TODO: Реализуйте метод
        pass

# Стратегии вытеснения:
class LRUStrategy:
    """Стратегия Least Recently Used"""
    # TODO: Реализуйте стратегию
    pass

class FIFOStrategy:
    """Стратегия First In, First Out"""
    # TODO: Реализуйте стратегию
    pass

# Декоратор для кэширования:
def cached(max_size: int = 128):
    """Декоратор для кэширования результатов функций"""
    # TODO: Реализуйте декоратор
    pass

# Решение:
from collections import OrderedDict
from typing import DefaultDict
from collections import defaultdict

class EvictionStrategySolution(Protocol[K]):
    def on_access(self, key: K) -> None:
        """Вызывается при доступе к ключу"""
        ...
    
    def on_insert(self, key: K) -> None:
        """Вызывается при вставке нового ключа"""
        ...
    
    def get_victim(self) -> Optional[K]:
        """Возвращает ключ для удаления"""
        ...
    
    def on_remove(self, key: K) -> None:
        """Вызывается при удалении ключа"""
        ...

class LRUStrategySolution:
    def __init__(self) -> None:
        self._access_order: OrderedDict[K, None] = OrderedDict()
    
    def on_access(self, key: K) -> None:
        if key in self._access_order:
            del self._access_order[key]
        self._access_order[key] = None
    
    def on_insert(self, key: K) -> None:
        self._access_order[key] = None
    
    def get_victim(self) -> Optional[K]:
        return next(iter(self._access_order)) if self._access_order else None
    
    def on_remove(self, key: K) -> None:
        self._access_order.pop(key, None)

class FIFOStrategySolution:
    def __init__(self) -> None:
        self._insertion_order: List[K] = []
    
    def on_access(self, key: K) -> None:
        pass  # FIFO не зависит от доступа
    
    def on_insert(self, key: K) -> None:
        self._insertion_order.append(key)
    
    def get_victim(self) -> Optional[K]:
        return self._insertion_order[0] if self._insertion_order else None
    
    def on_remove(self, key: K) -> None:
        if key in self._insertion_order:
            self._insertion_order.remove(key)

class CacheSolution(Generic[K, V]):
    def __init__(self, max_size: int, strategy: EvictionStrategySolution[K]) -> None:
        self._max_size = max_size
        self._strategy = strategy
        self._data: Dict[K, V] = {}
    
    def get(self, key: K) -> Optional[V]:
        if key in self._data:
            self._strategy.on_access(key)
            return self._data[key]
        return None
    
    def put(self, key: K, value: V) -> None:
        if key in self._data:
            self._data[key] = value
            self._strategy.on_access(key)
        else:
            if len(self._data) >= self._max_size:
                victim = self._strategy.get_victim()
                if victim is not None:
                    del self._data[victim]
                    self._strategy.on_remove(victim)
            
            self._data[key] = value
            self._strategy.on_insert(key)
    
    def clear(self) -> None:
        self._data.clear()
        # Очищаем стратегию
        if hasattr(self._strategy, '_access_order'):
            self._strategy._access_order.clear()
        if hasattr(self._strategy, '_insertion_order'):
            self._strategy._insertion_order.clear()

def cached_solution(max_size: int = 128):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache: CacheSolution[Tuple[Any, ...], Any] = CacheSolution(
            max_size, LRUStrategySolution()
        )
        
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Создаем ключ из аргументов
            key = (args, tuple(sorted(kwargs.items())))
            
            result = cache.get(key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache.put(key, result)
            return result
        
        wrapper.cache_clear = cache.clear
        wrapper.cache = cache
        return wrapper
    
    return decorator

# =============================================================================
# Упражнение 5: Интеграция с Pydantic (бонусное)
# =============================================================================

"""
ЗАДАНИЕ 5: API модель с Pydantic и типами

Создайте систему для работы с API, используя Pydantic модели и типизацию.
Требования:
1. Создайте Pydantic модели для User, Address, Company
2. Используйте валидаторы для проверки данных
3. Создайте Generic класс APIResponse[T]
4. Реализуйте типизированный API клиент
"""

try:
    from pydantic import BaseModel, Field, validator, ValidationError
    
    # Ваши Pydantic модели здесь:
    class Address(BaseModel):
        # TODO: Определите поля адреса
        pass
    
    class User(BaseModel):
        # TODO: Определите поля пользователя
        pass
    
    class Company(BaseModel):
        # TODO: Определите поля компании
        pass
    
    # Generic API Response:
    ResponseData = TypeVar('ResponseData', bound=BaseModel)
    
    class APIResponse(BaseModel, Generic[ResponseData]):
        # TODO: Определите структуру ответа API
        pass
    
    class APIClient:
        """Типизированный API клиент"""
        # TODO: Реализуйте клиент
        pass
    
    # Решение:
    class AddressSolution(BaseModel):
        street: str = Field(..., min_length=1, max_length=200)
        city: str = Field(..., min_length=1, max_length=100)
        state: Optional[str] = Field(None, max_length=50)
        zip_code: str = Field(..., regex=r'^\d{5}(-\d{4})?$')
        country: str = Field(default="US", max_length=2)
        
        @validator('country')
        def country_must_be_uppercase(cls, v):
            return v.upper()
    
    class UserSolution(BaseModel):
        id: Optional[int] = None
        name: str = Field(..., min_length=1, max_length=100)
        email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
        age: Optional[int] = Field(None, ge=0, le=150)
        address: Optional[AddressSolution] = None
        is_active: bool = True
        
        @validator('email')
        def email_must_be_lowercase(cls, v):
            return v.lower()
        
        @validator('name')
        def name_must_be_title_case(cls, v):
            return v.strip().title()
    
    class CompanySolution(BaseModel):
        id: Optional[int] = None
        name: str = Field(..., min_length=1, max_length=200)
        description: Optional[str] = Field(None, max_length=1000)
        employees: List[UserSolution] = Field(default_factory=list)
        headquarters: Optional[AddressSolution] = None
        founded_year: Optional[int] = Field(None, ge=1800, le=2024)
        
        @validator('employees')
        def validate_employees(cls, v):
            if len(v) > 10000:
                raise ValueError('Too many employees')
            return v
    
    class APIResponseSolution(BaseModel, Generic[ResponseData]):
        success: bool
        data: Optional[ResponseData] = None
        error: Optional[str] = None
        timestamp: datetime = Field(default_factory=datetime.now)
        
        @validator('data', 'error')
        def validate_data_error_exclusivity(cls, v, values):
            success = values.get('success', False)
            if success and v is None and 'data' in values:
                raise ValueError('Success response must have data')
            elif not success and v is None and 'error' in values:
                raise ValueError('Error response must have error message')
            return v
    
    class APIClientSolution:
        def __init__(self, base_url: str):
            self.base_url = base_url
        
        def get_user(self, user_id: int) -> APIResponseSolution[UserSolution]:
            # Симуляция API вызова
            try:
                user_data = {
                    "id": user_id,
                    "name": "john doe",
                    "email": "JOHN@EXAMPLE.COM",
                    "age": 30,
                    "address": {
                        "street": "123 Main St",
                        "city": "Anytown",
                        "zip_code": "12345",
                        "country": "us"
                    }
                }
                user = UserSolution(**user_data)
                return APIResponseSolution[UserSolution](success=True, data=user)
            except ValidationError as e:
                return APIResponseSolution[UserSolution](success=False, error=str(e))
        
        def create_user(self, user_data: Dict[str, Any]) -> APIResponseSolution[UserSolution]:
            try:
                user = UserSolution(**user_data)
                user.id = 123  # Симуляция присвоения ID
                return APIResponseSolution[UserSolution](success=True, data=user)
            except ValidationError as e:
                return APIResponseSolution[UserSolution](success=False, error=str(e))

except ImportError:
    print("Pydantic not installed. Skipping Pydantic exercises.")

# =============================================================================
# Тесты для проверки решений
# =============================================================================

class TestAdvancedTyping(unittest.TestCase):
    """Тесты для упражнений по продвинутой типизации"""
    
    def test_repository(self):
        """Тест Generic Repository"""
        repo = RepositorySolution[User]()
        
        user = User("Alice", "alice@example.com")
        saved_user = repo.save(user)
        
        self.assertIsNotNone(saved_user.id)
        self.assertEqual(saved_user.name, "Alice")
        
        found_user = repo.find_by_id(saved_user.id)
        self.assertEqual(found_user, saved_user)
        
        all_users = repo.find_all()
        self.assertEqual(len(all_users), 1)
        
        # Тест фильтрации
        repo.save(User("Bob", "bob@example.com"))
        alice_users = repo.filter(lambda u: u.name == "Alice")
        self.assertEqual(len(alice_users), 1)
        self.assertEqual(alice_users[0].name, "Alice")
    
    def test_notification_protocols(self):
        """Тест протоколов уведомлений"""
        service = NotificationServiceSolution()
        
        email_notifier = EmailNotifierSolution()
        sms_notifier = SMSNotifierSolution()
        
        # Проверяем, что объекты соответствуют протоколам
        self.assertIsInstance(email_notifier, NotifiableSolution)
        self.assertIsInstance(sms_notifier, NotifiableSolution)
        
        service.add_notifier(email_notifier)
        service.add_notifier(sms_notifier)
        
        results = service.send_to_all("user@example.com", "Test message")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(results))
    
    def test_type_guards(self):
        """Тест Type Guards"""
        # Тест email
        self.assertTrue(is_valid_email_solution("test@example.com"))
        self.assertFalse(is_valid_email_solution("invalid-email"))
        
        # Тест телефона
        self.assertTrue(is_valid_phone_solution("+7 495 123-45-67"))
        self.assertTrue(is_valid_phone_solution("8(495)1234567"))
        self.assertFalse(is_valid_phone_solution("123"))
        
        # Тест возраста
        self.assertTrue(is_valid_age_solution(25))
        self.assertFalse(is_valid_age_solution(-5))
        self.assertFalse(is_valid_age_solution(200))
        
        # Тест валидации данных
        email = validate_user_data_solution("TEST@EXAMPLE.COM", "email")
        self.assertEqual(email, "test@example.com")
        
        phone = validate_user_data_solution("8-495-123-45-67", "phone")
        self.assertTrue(phone.startswith("+7"))
    
    def test_cache(self):
        """Тест системы кэширования"""
        lru_strategy = LRUStrategySolution[str]()
        cache = CacheSolution[str, int](max_size=2, strategy=lru_strategy)
        
        cache.put("a", 1)
        cache.put("b", 2)
        
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)
        
        # Добавляем третий элемент - должен вытеснить наименее используемый
        cache.put("c", 3)
        
        # Проверяем, что кэш работает правильно
        self.assertIsNotNone(cache.get("a"))  # Недавно использовался
        self.assertIsNotNone(cache.get("c"))  # Новый элемент
    
    @unittest.skipIf('pydantic' not in globals(), "Pydantic not available")
    def test_pydantic_integration(self):
        """Тест интеграции с Pydantic"""
        try:
            client = APIClientSolution("https://api.example.com")
            
            # Тест получения пользователя
            response = client.get_user(1)
            self.assertTrue(response.success)
            self.assertIsNotNone(response.data)
            self.assertEqual(response.data.name, "John Doe")  # Должен быть title case
            self.assertEqual(response.data.email, "john@example.com")  # Должен быть lowercase
            
            # Тест создания пользователя
            user_data = {
                "name": "jane doe",
                "email": "JANE@EXAMPLE.COM",
                "age": 25
            }
            
            response = client.create_user(user_data)
            self.assertTrue(response.success)
            self.assertIsNotNone(response.data)
            self.assertEqual(response.data.name, "Jane Doe")
            
        except ImportError:
            self.skipTest("Pydantic not installed")

def run_tests():
    """Запуск всех тестов"""
    unittest.main(verbosity=2, exit=False)

if __name__ == "__main__":
    print("=== Упражнения: Продвинутая типизация ===\n")
    print("Запуск тестов для проверки решений...\n")
    run_tests() 