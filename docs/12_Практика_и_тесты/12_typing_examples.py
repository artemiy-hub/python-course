#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Типизация и аннотации типов в Python

Этот файл содержит примеры для изучения:
- Базовых типов и аннотаций
- Обобщенных типов и протоколов
- Dataclasses и TypedDict
- Продвинутых техник типизации
- Статического анализа
"""

from typing import (
    List, Dict, Set, Tuple, Optional, Union, Any, Callable,
    TypeVar, Generic, Protocol, runtime_checkable, overload,
    Literal, Final, ClassVar, TYPE_CHECKING
)
from dataclasses import dataclass, field
from abc import abstractmethod
import json

# Условные импорты для демонстрации
if TYPE_CHECKING:
    from datetime import datetime


def example_01_basic_type_annotations():
    """
    Пример 1: Базовые аннотации типов
    
    Демонстрирует основные принципы типизации в Python:
    примитивные типы, коллекции, Optional и Union.
    """
    print("=== Пример 1: Базовые аннотации типов ===")
    
    # Примитивные типы
    def greet_user(name: str, age: int, is_premium: bool = False) -> str:
        """Приветствует пользователя с указанием статуса"""
        status = "премиум" if is_premium else "обычный"
        return f"Привет, {name}! Возраст: {age}, статус: {status}"
    
    # Коллекции
    def calculate_average(numbers: List[float]) -> float:
        """Вычисляет среднее арифметическое"""
        if not numbers:
            raise ValueError("Список не может быть пустым")
        return sum(numbers) / len(numbers)
    
    def count_words(text: str) -> Dict[str, int]:
        """Подсчитывает количество слов в тексте"""
        words = text.lower().split()
        word_count: Dict[str, int] = {}
        
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        return word_count
    
    # Optional и Union
    def find_user_by_id(user_id: int, users: Dict[int, str]) -> Optional[str]:
        """Находит пользователя по ID, возвращает None если не найден"""
        return users.get(user_id)
    
    def parse_number(value: Union[str, int, float]) -> float:
        """Парсит число из различных типов"""
        if isinstance(value, str):
            return float(value)
        elif isinstance(value, (int, float)):
            return float(value)
        else:
            raise TypeError(f"Неподдерживаемый тип: {type(value)}")
    
    # Современный синтаксис (Python 3.10+)
    def modern_syntax_example(data: list[str] | None) -> dict[str, int]:
        """Пример современного синтаксиса типов"""
        if data is None:
            return {}
        
        return {item: len(item) for item in data}
    
    # Демонстрация
    print("1. Приветствие пользователя:")
    greeting = greet_user("Алиса", 25, True)
    print(f"   {greeting}")
    
    print("\n2. Вычисление среднего:")
    numbers = [85.5, 92.0, 78.5, 95.0, 88.0]
    avg = calculate_average(numbers)
    print(f"   Среднее: {avg:.2f}")
    
    print("\n3. Подсчет слов:")
    text = "Python это отличный язык программирования Python"
    word_counts = count_words(text)
    print(f"   Слова: {word_counts}")
    
    print("\n4. Поиск пользователя:")
    users = {1: "Алиса", 2: "Боб", 3: "Чарли"}
    user = find_user_by_id(2, users)
    print(f"   Найден пользователь: {user}")
    
    user_not_found = find_user_by_id(99, users)
    print(f"   Пользователь не найден: {user_not_found}")
    
    print("\n5. Парсинг чисел:")
    values = ["42.5", 100, 3.14]
    for val in values:
        parsed = parse_number(val)
        print(f"   {val} ({type(val).__name__}) -> {parsed} (float)")
    
    print("✅ Пример 1 завершен")


def example_02_generic_types_and_protocols():
    """
    Пример 2: Обобщенные типы и протоколы
    
    Показывает использование TypeVar, Generic классов,
    Protocol для структурной типизации.
    """
    print("=== Пример 2: Обобщенные типы и протоколы ===")
    
    # TypeVar и Generic
    T = TypeVar('T')
    
    class Stack(Generic[T]):
        """Типизированный стек"""
        
        def __init__(self) -> None:
            self._items: List[T] = []
        
        def push(self, item: T) -> None:
            """Добавить элемент в стек"""
            self._items.append(item)
        
        def pop(self) -> Optional[T]:
            """Извлечь элемент из стека"""
            if self._items:
                return self._items.pop()
            return None
        
        def peek(self) -> Optional[T]:
            """Посмотреть верхний элемент без извлечения"""
            if self._items:
                return self._items[-1]
            return None
        
        def size(self) -> int:
            """Размер стека"""
            return len(self._items)
        
        def is_empty(self) -> bool:
            """Проверить, пуст ли стек"""
            return len(self._items) == 0
    
    # Протокол для сравнимых объектов
    @runtime_checkable
    class Comparable(Protocol):
        """Протокол для объектов, которые можно сравнивать"""
        
        @abstractmethod
        def __lt__(self, other) -> bool:
            """Меньше чем"""
            ...
    
    # Ограниченный TypeVar
    ComparableType = TypeVar('ComparableType', bound=Comparable)
    
    def find_max(items: List[ComparableType]) -> Optional[ComparableType]:
        """Находит максимальный элемент среди сравнимых объектов"""
        if not items:
            return None
        
        max_item = items[0]
        for item in items[1:]:
            if item > max_item:  # type: ignore
                max_item = item
        
        return max_item
    
    # Протокол для объектов с методом draw
    class Drawable(Protocol):
        """Протокол для рисуемых объектов"""
        
        def draw(self) -> str:
            """Нарисовать объект"""
            ...
        
        def get_area(self) -> float:
            """Получить площадь объекта"""
            ...
    
    # Классы, реализующие протокол неявно
    class Circle:
        """Круг"""
        
        def __init__(self, radius: float) -> None:
            self.radius = radius
        
        def draw(self) -> str:
            return f"Круг радиусом {self.radius}"
        
        def get_area(self) -> float:
            return 3.14159 * self.radius ** 2
    
    class Rectangle:
        """Прямоугольник"""
        
        def __init__(self, width: float, height: float) -> None:
            self.width = width
            self.height = height
        
        def draw(self) -> str:
            return f"Прямоугольник {self.width}x{self.height}"
        
        def get_area(self) -> float:
            return self.width * self.height
    
    def render_shapes(shapes: List[Drawable]) -> None:
        """Рендерит список фигур"""
        total_area = 0.0
        
        print("   Рендеринг фигур:")
        for i, shape in enumerate(shapes, 1):
            description = shape.draw()
            area = shape.get_area()
            total_area += area
            print(f"     {i}. {description} - площадь: {area:.2f}")
        
        print(f"   Общая площадь: {total_area:.2f}")
    
    # Демонстрация
    print("1. Типизированный стек:")
    
    # Стек целых чисел
    int_stack: Stack[int] = Stack()
    int_stack.push(10)
    int_stack.push(20)
    int_stack.push(30)
    
    print(f"   Размер стека: {int_stack.size()}")
    print(f"   Верхний элемент: {int_stack.peek()}")
    print(f"   Извлекаем: {int_stack.pop()}")
    print(f"   Новый размер: {int_stack.size()}")
    
    # Стек строк
    str_stack: Stack[str] = Stack()
    str_stack.push("первый")
    str_stack.push("второй")
    
    print(f"   Стек строк: {str_stack.pop()}, {str_stack.pop()}")
    
    print("\n2. Поиск максимума:")
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    max_number = find_max(numbers)
    print(f"   Максимальное число: {max_number}")
    
    words = ["apple", "banana", "cherry", "date"]
    max_word = find_max(words)
    print(f"   Максимальное слово: {max_word}")
    
    print("\n3. Структурная типизация (протоколы):")
    shapes = [
        Circle(5.0),
        Rectangle(10.0, 20.0),
        Circle(3.0)
    ]
    
    render_shapes(shapes)
    
    # Проверка протокола в runtime
    circle = Circle(2.0)
    print(f"\n   Circle реализует Drawable: {isinstance(circle, Drawable)}")
    
    print("✅ Пример 2 завершен")


def example_03_dataclasses_and_typed_dict():
    """
    Пример 3: Dataclasses и TypedDict
    
    Демонстрирует современные способы создания типизированных
    структур данных с автогенерацией методов.
    """
    print("=== Пример 3: Dataclasses и TypedDict ===")
    
    from typing import TypedDict
    from datetime import datetime
    
    # Базовый dataclass
    @dataclass
    class User:
        """Пользователь системы"""
        id: int
        name: str
        email: str
        is_active: bool = True
        created_at: Optional[datetime] = None
        
        def __post_init__(self) -> None:
            """Инициализация после создания объекта"""
            if self.created_at is None:
                self.created_at = datetime.now()
    
    # Dataclass с валидацией
    @dataclass
    class Product:
        """Товар в магазине"""
        id: int
        name: str
        price: float
        category: str
        in_stock: bool = True
        tags: List[str] = field(default_factory=list)
        
        def __post_init__(self) -> None:
            """Валидация данных"""
            if self.price < 0:
                raise ValueError("Цена не может быть отрицательной")
            
            if not self.name.strip():
                raise ValueError("Название товара не может быть пустым")
        
        def add_tag(self, tag: str) -> None:
            """Добавить тег к товару"""
            if tag not in self.tags:
                self.tags.append(tag)
        
        def calculate_discounted_price(self, discount_percent: float) -> float:
            """Вычислить цену со скидкой"""
            if not 0 <= discount_percent <= 100:
                raise ValueError("Скидка должна быть от 0 до 100%")
            
            return self.price * (1 - discount_percent / 100)
    
    # Неизменяемый dataclass
    @dataclass(frozen=True)
    class Point:
        """Неизменяемая точка в пространстве"""
        x: float
        y: float
        z: float = 0.0
        
        def distance_to(self, other: 'Point') -> float:
            """Расстояние до другой точки"""
            return (
                (self.x - other.x) ** 2 +
                (self.y - other.y) ** 2 +
                (self.z - other.z) ** 2
            ) ** 0.5
    
    # TypedDict для структурированных данных
    class UserData(TypedDict):
        """Структура данных пользователя"""
        id: int
        name: str
        email: str
        age: int
    
    class UserProfile(TypedDict, total=False):
        """Дополнительные данные профиля (все поля опциональны)"""
        bio: str
        website: str
        location: str
        avatar_url: str
    
    # Комбинированная структура
    class FullUserData(UserData, UserProfile):
        """Полные данные пользователя"""
        pass
    
    def process_user_data(data: UserData) -> str:
        """Обработка данных пользователя"""
        return f"Пользователь {data['name']} ({data['email']}) - {data['age']} лет"
    
    def save_user_profile(profile: UserProfile) -> None:
        """Сохранение профиля пользователя"""
        fields = []
        for key, value in profile.items():
            fields.append(f"{key}: {value}")
        
        print(f"   Сохраняем профиль: {', '.join(fields)}")
    
    # Демонстрация
    print("1. Базовые dataclasses:")
    
    # Создание пользователей
    user1 = User(1, "Алиса", "alice@example.com")
    user2 = User(2, "Боб", "bob@example.com", False)
    
    print(f"   Пользователь 1: {user1}")
    print(f"   Пользователь 2: {user2}")
    print(f"   Равны ли пользователи: {user1 == user2}")
    
    print("\n2. Dataclass с валидацией:")
    
    # Создание товаров
    try:
        laptop = Product(1, "Ноутбук", 99999.99, "Электроника")
        laptop.add_tag("компьютер")
        laptop.add_tag("работа")
        
        print(f"   Товар: {laptop}")
        print(f"   Теги: {laptop.tags}")
        
        discounted_price = laptop.calculate_discounted_price(15)
        print(f"   Цена со скидкой 15%: {discounted_price:.2f}")
        
        # Попытка создать товар с неверной ценой
        # invalid_product = Product(2, "Тест", -100, "Тест")  # Вызовет ValueError
        
    except ValueError as e:
        print(f"   Ошибка валидации: {e}")
    
    print("\n3. Неизменяемые dataclasses:")
    
    point1 = Point(0, 0, 0)
    point2 = Point(3, 4, 0)
    
    distance = point1.distance_to(point2)
    print(f"   Расстояние между точками: {distance}")
    
    # point1.x = 10  # Вызовет ошибку - объект неизменяемый
    
    print("\n4. TypedDict:")
    
    # Типизированные словари
    user_data: UserData = {
        'id': 1,
        'name': 'Алиса',
        'email': 'alice@example.com',
        'age': 25
    }
    
    result = process_user_data(user_data)
    print(f"   {result}")
    
    # Опциональные поля
    profile: UserProfile = {
        'bio': 'Разработчик Python',
        'website': 'https://alice.dev',
        'location': 'Москва'
    }
    
    save_user_profile(profile)
    
    # Комбинированные данные
    full_data: FullUserData = {
        'id': 2,
        'name': 'Боб',
        'email': 'bob@example.com',
        'age': 30,
        'bio': 'DevOps инженер',
        'location': 'Санкт-Петербург'
    }
    
    print(f"   Полные данные: {process_user_data(full_data)}")
    
    print("✅ Пример 3 завершен")


def example_04_advanced_typing_patterns():
    """
    Пример 4: Продвинутые паттерны типизации
    
    Демонстрирует сложные концепции: Literal, Final, NewType,
    overload, условную типизацию и другие продвинутые техники.
    """
    print("=== Пример 4: Продвинутые паттерны типизации ===")
    
    from typing import NewType, overload
    
    # NewType для создания различимых типов
    UserId = NewType('UserId', int)
    ProductId = NewType('ProductId', int)
    
    # Literal типы для ограничения значений
    LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]
    
    # Final константы
    MAX_RETRIES: Final[int] = 3
    API_VERSION: Final[str] = "v1.0"
    
    class APIClient:
        """Клиент API с типизацией"""
        
        BASE_URL: ClassVar[str] = "https://api.example.com"
        
        def __init__(self, api_key: str) -> None:
            self.api_key: Final[str] = api_key
            self._session_id: Optional[str] = None
        
        def set_log_level(self, level: LogLevel) -> None:
            """Установить уровень логирования"""
            print(f"   Уровень логирования установлен: {level}")
        
        def make_request(self, method: HttpMethod, endpoint: str) -> Dict[str, Any]:
            """Выполнить HTTP запрос"""
            print(f"   {method} {self.BASE_URL}{endpoint}")
            
            # Имитация ответа
            return {
                "status": "success",
                "method": method,
                "endpoint": endpoint,
                "api_version": API_VERSION
            }
    
    # Overload для функций с разными сигнатурами
    @overload
    def get_user_info(user_id: UserId) -> Dict[str, Any]: ...
    
    @overload
    def get_user_info(user_id: UserId, include_profile: Literal[True]) -> Dict[str, Any]: ...
    
    @overload
    def get_user_info(user_id: UserId, include_profile: Literal[False]) -> Dict[str, str]: ...
    
    def get_user_info(
        user_id: UserId, 
        include_profile: bool = False
    ) -> Union[Dict[str, Any], Dict[str, str]]:
        """Получить информацию о пользователе"""
        
        base_info = {
            "id": str(user_id),
            "name": f"User_{user_id}",
            "email": f"user{user_id}@example.com"
        }
        
        if include_profile:
            return {
                **base_info,
                "profile": {
                    "bio": "Пользователь системы",
                    "location": "Неизвестно",
                    "joined_date": "2024-01-01"
                }
            }
        
        return base_info
    
    # Условная типизация
    def process_config(config: Dict[str, Any]) -> None:
        """Обработка конфигурации с условной типизацией"""
        
        # Проверяем наличие ключей во время выполнения
        if "debug" in config:
            debug_mode: bool = config["debug"]
            print(f"   Режим отладки: {debug_mode}")
        
        if "max_connections" in config:
            max_conn: int = config["max_connections"]
            print(f"   Максимум соединений: {max_conn}")
        
        if "features" in config:
            features: List[str] = config["features"]
            print(f"   Включенные функции: {', '.join(features)}")
    
    # Функция с Callable типом
    def apply_operation(
        data: List[int], 
        operation: Callable[[int], int],
        filter_func: Optional[Callable[[int], bool]] = None
    ) -> List[int]:
        """Применить операцию к данным с опциональной фильтрацией"""
        
        working_data = data
        
        if filter_func:
            working_data = [x for x in data if filter_func(x)]
            print(f"   Отфильтровано: {working_data}")
        
        result = [operation(x) for x in working_data]
        print(f"   Результат операции: {result}")
        
        return result
    
    # Демонстрация
    print("1. NewType и различимые типы:")
    
    user_id = UserId(12345)
    product_id = ProductId(67890)
    
    print(f"   User ID: {user_id} (тип: {type(user_id).__name__})")
    print(f"   Product ID: {product_id} (тип: {type(product_id).__name__})")
    
    # На уровне типизации это разные типы, но в runtime - обычные int
    print(f"   Фактически user_id это int: {isinstance(user_id, int)}")
    
    print("\n2. Literal типы:")
    
    client = APIClient("secret-api-key")
    client.set_log_level("INFO")  # Только допустимые значения
    
    response = client.make_request("GET", "/users")
    print(f"   Ответ API: {response}")
    
    print("\n3. Final константы:")
    print(f"   Максимум попыток: {MAX_RETRIES}")
    print(f"   Версия API: {API_VERSION}")
    
    # MAX_RETRIES = 5  # mypy выдаст ошибку - нельзя изменять Final
    
    print("\n4. Overload функции:")
    
    # Разные варианты вызова с разными типами возврата
    basic_info = get_user_info(user_id)
    print(f"   Базовая информация: {basic_info}")
    
    full_info = get_user_info(user_id, True)
    print(f"   Полная информация включает профиль: {'profile' in full_info}")
    
    print("\n5. Условная типизация:")
    
    config_data = {
        "debug": True,
        "max_connections": 100,
        "features": ["auth", "logging", "metrics"],
        "database_url": "postgresql://localhost/mydb"
    }
    
    process_config(config_data)
    
    print("\n6. Callable типы:")
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Операция: возведение в квадрат
    def square(x: int) -> int:
        return x * x
    
    # Фильтр: только четные числа
    def is_even(x: int) -> bool:
        return x % 2 == 0
    
    result = apply_operation(numbers, square, is_even)
    
    # Без фильтра
    result_all = apply_operation(numbers[:5], square)
    
    print("✅ Пример 4 завершен")


def example_05_type_checking_and_tools():
    """
    Пример 5: Инструменты статического анализа
    
    Демонстрирует работу с mypy, настройку проверок типов,
    обработку type: ignore и другие практические аспекты.
    """
    print("=== Пример 5: Инструменты статического анализа ===")
    
    # Пример кода с различными типами ошибок
    def demonstration_function() -> None:
        """Функция для демонстрации различных ситуаций с типами"""
        
        # 1. Правильно типизированный код
        def correct_typing(numbers: List[int]) -> float:
            """Правильно типизированная функция"""
            return sum(numbers) / len(numbers) if numbers else 0.0
        
        # 2. Код с потенциальными ошибками типов
        def potential_errors() -> None:
            """Демонстрация потенциальных ошибок"""
            
            # Этот код вызовет предупреждения mypy
            data: List[int] = [1, 2, 3]
            
            # Неправильное использование типов (для демонстрации)
            # result = data + "string"  # mypy error: unsupported operand type(s)
            
            # Правильный способ
            result = data + [4, 5, 6]
            print(f"   Правильное объединение списков: {result}")
        
        # 3. Использование Any для временного отключения проверок
        def working_with_any(data: Any) -> Any:
            """Функция с Any типами (не рекомендуется)"""
            # Any отключает проверку типов
            return data.some_method().chain().result()  # mypy не проверит это
        
        # 4. Правильный способ работы с неизвестными типами
        def safe_json_processing(json_data: str) -> Dict[str, Any]:
            """Безопасная обработка JSON данных"""
            try:
                parsed: Dict[str, Any] = json.loads(json_data)
                return parsed
            except json.JSONDecodeError:
                return {}
        
        # 5. Type guards для runtime проверок
        def is_string_list(obj: Any) -> bool:
            """Проверяет, является ли объект списком строк"""
            return (
                isinstance(obj, list) and
                all(isinstance(item, str) for item in obj)
            )
        
        def process_string_list(data: Any) -> List[str]:
            """Обработка списка строк с проверкой типов"""
            if is_string_list(data):
                # После проверки mypy знает, что data это List[str]
                return [item.upper() for item in data]  # type: ignore
            else:
                raise TypeError("Ожидается список строк")
        
        # Демонстрация
        print("   1. Правильная типизация:")
        nums = [10, 20, 30, 40]
        average = correct_typing(nums)
        print(f"      Среднее: {average}")
        
        print("   2. Потенциальные ошибки:")
        potential_errors()
        
        print("   3. Работа с JSON:")
        json_str = '{"name": "Alice", "age": 25, "skills": ["Python", "TypeScript"]}'
        parsed_data = safe_json_processing(json_str)
        print(f"      Распарсенные данные: {parsed_data}")
        
        print("   4. Type guards:")
        test_data = ["apple", "banana", "cherry"]
        try:
            processed = process_string_list(test_data)
            print(f"      Обработанные строки: {processed}")
        except TypeError as e:
            print(f"      Ошибка типа: {e}")
    
    # Примеры конфигурации mypy (в комментариях)
    def mypy_configuration_examples() -> None:
        """Примеры конфигурации mypy"""
        
        print("   Примеры конфигурации mypy:")
        print("   ")
        print("   # mypy.ini")
        print("   [mypy]")
        print("   python_version = 3.9")
        print("   warn_return_any = True")
        print("   warn_unused_configs = True")
        print("   disallow_untyped_defs = True")
        print("   ")
        print("   # Игнорирование конкретных модулей")
        print("   [mypy-some_external_package.*]")
        print("   ignore_missing_imports = True")
        print("   ")
        print("   # Строгая проверка для критических модулей")
        print("   [mypy-myapp.core.*]")
        print("   disallow_any_generics = True")
        print("   disallow_any_unimported = True")
    
    # Практические советы по типизации
    def practical_typing_tips() -> None:
        """Практические советы по типизации"""
        
        print("   Практические советы:")
        print("   ")
        print("   1. Начинайте с функций:")
        print("      - Добавляйте типы параметров и возвращаемых значений")
        print("      - Это дает максимальную пользу при минимальных усилиях")
        print("   ")
        print("   2. Используйте Optional явно:")
        print("      - Optional[str] лучше чем Union[str, None]")
        print("      - str | None в Python 3.10+")
        print("   ")
        print("   3. Предпочитайте конкретные типы:")
        print("      - List[str] лучше чем List[Any]")
        print("      - Dict[str, int] лучше чем Dict")
        print("   ")
        print("   4. Используйте Protocols для утиной типизации:")
        print("      - Определяйте интерфейсы через протоколы")
        print("      - Структурная типизация лучше наследования")
        print("   ")
        print("   5. Настройте CI/CD:")
        print("      - Добавьте mypy в pre-commit hooks")
        print("      - Интегрируйте проверку типов в CI")
    
    # Запуск демонстрации
    demonstration_function()
    print("\n   Конфигурация mypy:")
    mypy_configuration_examples()
    print("\n   Советы по типизации:")
    practical_typing_tips()
    
    print("✅ Пример 5 завершен")


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Базовые аннотации типов", example_01_basic_type_annotations),
        ("Обобщенные типы и протоколы", example_02_generic_types_and_protocols),
        ("Dataclasses и TypedDict", example_03_dataclasses_and_typed_dict),
        ("Продвинутые паттерны типизации", example_04_advanced_typing_patterns),
        ("Инструменты статического анализа", example_05_type_checking_and_tools),
    ]
    
    print("🏷️ Примеры: Типизация и аннотации типов в Python")
    print("=" * 70)
    print("Эти примеры демонстрируют:")
    print("- Основы системы типов Python")
    print("- Современные подходы к типизации")
    print("- Практическое применение типов")
    print("- Инструменты статического анализа")
    print("- Лучшие практики типизации")
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
    
    print("\n🎉 Все примеры типизации завершены!")


if __name__ == "__main__":
    main() 