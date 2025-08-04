#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Типизация и аннотации типов в Python

Этот файл содержит практические упражнения для закрепления знаний:
- Создание типизированных систем
- Применение продвинутых паттернов типизации
- Разработка безопасных API
"""

from typing import (
    List, Dict, Set, Tuple, Optional, Union, Any, Callable, TypeVar, Generic,
    Protocol, runtime_checkable, overload, Literal, Final, ClassVar,
    TypedDict, NewType
)
from dataclasses import dataclass, field
from abc import abstractmethod
from datetime import datetime, timedelta
import json
from enum import Enum


def exercise_01_type_safe_database_orm():
    """
    Упражнение 1: Типобезопасная ORM система
    
    Задача:
    Создайте типизированную систему для работы с базой данных,
    включающую модели, репозитории и безопасные запросы.
    """
    print("=== Упражнение 1: Типобезопасная ORM система ===")
    
    # РЕШЕНИЕ:
    
    # Базовые типы для ID
    EntityId = NewType('EntityId', int)
    UserId = NewType('UserId', EntityId)
    PostId = NewType('PostId', EntityId)
    CategoryId = NewType('CategoryId', EntityId)
    
    # Протокол для моделей с ID
    @runtime_checkable
    class HasId(Protocol):
        """Протокол для сущностей с ID"""
        id: EntityId
    
    # Базовая модель
    @dataclass
    class BaseModel:
        """Базовая модель для всех сущностей"""
        id: EntityId
        created_at: datetime = field(default_factory=datetime.now)
        updated_at: datetime = field(default_factory=datetime.now)
        
        def update_timestamp(self) -> None:
            """Обновить время последнего изменения"""
            self.updated_at = datetime.now()
    
    # Модели
    @dataclass
    class User(BaseModel):
        """Модель пользователя"""
        id: UserId  # type: ignore
        username: str
        email: str
        full_name: str
        is_active: bool = True
        
        def __post_init__(self) -> None:
            """Валидация пользователя"""
            if not self.username.strip():
                raise ValueError("Username не может быть пустым")
            
            if '@' not in self.email:
                raise ValueError("Некорректный email")
    
    @dataclass
    class Category(BaseModel):
        """Модель категории"""
        id: CategoryId  # type: ignore
        name: str
        description: str
        parent_id: Optional[CategoryId] = None
        
        def is_root_category(self) -> bool:
            """Проверить, является ли категория корневой"""
            return self.parent_id is None
    
    @dataclass
    class Post(BaseModel):
        """Модель поста"""
        id: PostId  # type: ignore
        title: str
        content: str
        author_id: UserId
        category_id: CategoryId
        is_published: bool = False
        tags: List[str] = field(default_factory=list)
        
        def add_tag(self, tag: str) -> None:
            """Добавить тег к посту"""
            if tag not in self.tags:
                self.tags.append(tag.lower())
        
        def word_count(self) -> int:
            """Подсчитать количество слов в посте"""
            return len(self.content.split())
    
    # Типы для запросов
    ModelType = TypeVar('ModelType', bound=BaseModel)
    
    # Условия фильтрации
    class FilterCondition(TypedDict, total=False):
        """Условия для фильтрации"""
        field: str
        value: Any
        operator: Literal["eq", "ne", "gt", "lt", "gte", "lte", "in", "like"]
    
    class QueryParams(TypedDict, total=False):
        """Параметры запроса"""
        limit: int
        offset: int
        order_by: str
        order_desc: bool
        filters: List[FilterCondition]
    
    # Результат запроса
    @dataclass
    class QueryResult(Generic[ModelType]):
        """Результат запроса с метаданными"""
        items: List[ModelType]
        total_count: int
        page: int
        page_size: int
        has_next: bool
        has_prev: bool
        
        @property
        def total_pages(self) -> int:
            """Общее количество страниц"""
            return (self.total_count + self.page_size - 1) // self.page_size
    
    # Репозиторий
    class Repository(Generic[ModelType]):
        """Базовый репозиторий для работы с моделями"""
        
        def __init__(self, model_class: type[ModelType]) -> None:
            self.model_class = model_class
            self._data: Dict[EntityId, ModelType] = {}
            self._next_id = 1
        
        def save(self, model: ModelType) -> ModelType:
            """Сохранить модель"""
            if model.id == 0:  # Новая модель
                model.id = EntityId(self._next_id)  # type: ignore
                self._next_id += 1
            else:
                model.update_timestamp()
            
            self._data[model.id] = model
            return model
        
        def find_by_id(self, entity_id: EntityId) -> Optional[ModelType]:
            """Найти модель по ID"""
            return self._data.get(entity_id)
        
        def find_all(self, params: Optional[QueryParams] = None) -> QueryResult[ModelType]:
            """Найти все модели с фильтрацией"""
            items = list(self._data.values())
            
            # Применяем фильтры
            if params and 'filters' in params:
                items = self._apply_filters(items, params['filters'])
            
            # Сортировка
            if params and 'order_by' in params:
                reverse = params.get('order_desc', False)
                items.sort(
                    key=lambda x: getattr(x, params['order_by']),
                    reverse=reverse
                )
            
            total_count = len(items)
            
            # Пагинация
            offset = params.get('offset', 0) if params else 0
            limit = params.get('limit', len(items)) if params else len(items)
            
            page_items = items[offset:offset + limit]
            page_size = limit
            current_page = offset // limit + 1 if limit > 0 else 1
            
            return QueryResult(
                items=page_items,
                total_count=total_count,
                page=current_page,
                page_size=page_size,
                has_next=offset + limit < total_count,
                has_prev=offset > 0
            )
        
        def delete(self, entity_id: EntityId) -> bool:
            """Удалить модель по ID"""
            if entity_id in self._data:
                del self._data[entity_id]
                return True
            return False
        
        def _apply_filters(self, items: List[ModelType], filters: List[FilterCondition]) -> List[ModelType]:
            """Применить фильтры к списку элементов"""
            result = items
            
            for filter_cond in filters:
                field_name = filter_cond['field']
                value = filter_cond['value']
                operator = filter_cond.get('operator', 'eq')
                
                if operator == 'eq':
                    result = [item for item in result if getattr(item, field_name, None) == value]
                elif operator == 'ne':
                    result = [item for item in result if getattr(item, field_name, None) != value]
                elif operator == 'in':
                    result = [item for item in result if getattr(item, field_name, None) in value]
                elif operator == 'like':
                    result = [item for item in result if value.lower() in str(getattr(item, field_name, '')).lower()]
            
            return result
    
    # Специализированные репозитории
    class UserRepository(Repository[User]):
        """Репозиторий пользователей"""
        
        def find_by_username(self, username: str) -> Optional[User]:
            """Найти пользователя по имени"""
            for user in self._data.values():
                if user.username == username:
                    return user
            return None
        
        def find_by_email(self, email: str) -> Optional[User]:
            """Найти пользователя по email"""
            for user in self._data.values():
                if user.email == email:
                    return user
            return None
        
        def find_active_users(self) -> List[User]:
            """Найти всех активных пользователей"""
            return [user for user in self._data.values() if user.is_active]
    
    class PostRepository(Repository[Post]):
        """Репозиторий постов"""
        
        def find_by_author(self, author_id: UserId) -> List[Post]:
            """Найти посты автора"""
            return [post for post in self._data.values() if post.author_id == author_id]
        
        def find_by_category(self, category_id: CategoryId) -> List[Post]:
            """Найти посты в категории"""
            return [post for post in self._data.values() if post.category_id == category_id]
        
        def find_published(self) -> List[Post]:
            """Найти опубликованные посты"""
            return [post for post in self._data.values() if post.is_published]
        
        def find_by_tag(self, tag: str) -> List[Post]:
            """Найти посты по тегу"""
            return [post for post in self._data.values() if tag.lower() in post.tags]
    
    # Сервисный слой
    class BlogService:
        """Сервис для работы с блогом"""
        
        def __init__(self) -> None:
            self.user_repo = UserRepository(User)
            self.post_repo = PostRepository(Post)
            self.category_repo = Repository(Category)
        
        def create_user(self, username: str, email: str, full_name: str) -> User:
            """Создать пользователя"""
            if self.user_repo.find_by_username(username):
                raise ValueError(f"Пользователь {username} уже существует")
            
            if self.user_repo.find_by_email(email):
                raise ValueError(f"Email {email} уже используется")
            
            user = User(
                id=UserId(0),  # Будет назначен в репозитории
                username=username,
                email=email,
                full_name=full_name
            )
            
            return self.user_repo.save(user)
        
        def create_post(
            self, 
            author_id: UserId, 
            category_id: CategoryId,
            title: str, 
            content: str,
            tags: Optional[List[str]] = None
        ) -> Post:
            """Создать пост"""
            # Проверяем существование автора и категории
            if not self.user_repo.find_by_id(author_id):
                raise ValueError(f"Автор с ID {author_id} не найден")
            
            if not self.category_repo.find_by_id(category_id):
                raise ValueError(f"Категория с ID {category_id} не найдена")
            
            post = Post(
                id=PostId(0),  # Будет назначен в репозитории
                title=title,
                content=content,
                author_id=author_id,
                category_id=category_id,
                tags=tags or []
            )
            
            return self.post_repo.save(post)
        
        def publish_post(self, post_id: PostId) -> bool:
            """Опубликовать пост"""
            post = self.post_repo.find_by_id(post_id)
            if not post:
                return False
            
            post.is_published = True
            self.post_repo.save(post)
            return True
        
        def get_user_stats(self, user_id: UserId) -> Dict[str, Any]:
            """Получить статистику пользователя"""
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise ValueError(f"Пользователь с ID {user_id} не найден")
            
            user_posts = self.post_repo.find_by_author(user_id)
            published_posts = [p for p in user_posts if p.is_published]
            
            total_words = sum(post.word_count() for post in published_posts)
            
            return {
                'username': user.username,
                'total_posts': len(user_posts),
                'published_posts': len(published_posts),
                'total_words': total_words,
                'avg_words_per_post': total_words / len(published_posts) if published_posts else 0
            }
    
    # Демонстрация
    print("Создание типобезопасной ORM системы...")
    
    service = BlogService()
    
    # Создаем категории
    tech_category = Category(
        id=CategoryId(0),
        name="Технологии",
        description="Статьи о технологиях"
    )
    tech_category = service.category_repo.save(tech_category)
    
    # Создаем пользователей
    alice = service.create_user("alice", "alice@example.com", "Алиса Иванова")
    bob = service.create_user("bob", "bob@example.com", "Боб Петров")
    
    print(f"Создан пользователь: {alice.username} (ID: {alice.id})")
    print(f"Создан пользователь: {bob.username} (ID: {bob.id})")
    
    # Создаем посты
    post1 = service.create_post(
        alice.id, tech_category.id,
        "Введение в типизацию Python",
        "Типизация в Python помогает создавать более надежный код...",
        ["python", "typing", "programming"]
    )
    
    post2 = service.create_post(
        bob.id, tech_category.id,
        "Продвинутые паттерны типизации",
        "Рассмотрим сложные концепции типизации в Python...",
        ["python", "advanced", "patterns"]
    )
    
    # Публикуем посты
    service.publish_post(post1.id)
    service.publish_post(post2.id)
    
    print(f"Создан и опубликован пост: {post1.title}")
    print(f"Создан и опубликован пост: {post2.title}")
    
    # Получаем статистику
    alice_stats = service.get_user_stats(alice.id)
    print(f"\nСтатистика Алисы: {alice_stats}")
    
    # Поиск постов
    python_posts = service.post_repo.find_by_tag("python")
    print(f"\nПостов с тегом 'python': {len(python_posts)}")
    
    # Фильтрация с QueryParams
    published_query: QueryParams = {
        'filters': [{'field': 'is_published', 'value': True, 'operator': 'eq'}],
        'limit': 10,
        'offset': 0
    }
    
    published_result = service.post_repo.find_all(published_query)
    print(f"Опубликованных постов: {published_result.total_count}")
    
    print("✅ Упражнение 1 завершено")


def exercise_02_api_type_system():
    """
    Упражнение 2: Типизированная система API
    
    Задача:
    Создайте полностью типизированную систему для REST API
    с валидацией запросов, ответов и обработкой ошибок.
    """
    print("=== Упражнение 2: Типизированная система API ===")
    
    # РЕШЕНИЕ:
    
    from enum import Enum
    from typing import TypedDict, NotRequired
    
    # HTTP статусы
    class HTTPStatus(Enum):
        """HTTP статус коды"""
        OK = 200
        CREATED = 201
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        FORBIDDEN = 403
        NOT_FOUND = 404
        INTERNAL_ERROR = 500
    
    # Типы для API
    class ErrorResponse(TypedDict):
        """Структура ошибки API"""
        error: str
        message: str
        status_code: int
        details: NotRequired[Dict[str, Any]]
    
    class SuccessResponse(TypedDict):
        """Структура успешного ответа"""
        data: Any
        status_code: int
        message: NotRequired[str]
    
    # API Response type
    APIResponse = Union[SuccessResponse, ErrorResponse]
    
    # Request типы
    class CreateUserRequest(TypedDict):
        """Запрос на создание пользователя"""
        username: str
        email: str
        password: str
        full_name: str
        age: NotRequired[int]
    
    class UpdateUserRequest(TypedDict, total=False):
        """Запрос на обновление пользователя"""
        username: str
        email: str
        full_name: str
        age: int
    
    class UserFilter(TypedDict, total=False):
        """Фильтры для поиска пользователей"""
        username: str
        email: str
        min_age: int
        max_age: int
        is_active: bool
    
    # Response типы
    class UserResponse(TypedDict):
        """Ответ с данными пользователя"""
        id: int
        username: str
        email: str
        full_name: str
        age: Optional[int]
        is_active: bool
        created_at: str
    
    class PaginatedResponse(TypedDict):
        """Пагинированный ответ"""
        items: List[Dict[str, Any]]
        total: int
        page: int
        page_size: int
        has_next: bool
        has_prev: bool
    
    # Протокол для валидаторов
    class Validator(Protocol):
        """Протокол для валидаторов данных"""
        
        def validate(self, data: Any) -> Tuple[bool, List[str]]:
            """Валидировать данные, вернуть (успех, список ошибок)"""
            ...
    
    # Конкретные валидаторы
    class UserValidator:
        """Валидатор данных пользователя"""
        
        def validate(self, data: CreateUserRequest) -> Tuple[bool, List[str]]:
            """Валидация данных пользователя"""
            errors: List[str] = []
            
            # Проверка username
            username = data.get('username', '').strip()
            if not username:
                errors.append("Username обязателен")
            elif len(username) < 3:
                errors.append("Username должен содержать минимум 3 символа")
            elif not username.replace('_', '').isalnum():
                errors.append("Username может содержать только буквы, цифры и _")
            
            # Проверка email
            email = data.get('email', '').strip()
            if not email:
                errors.append("Email обязателен")
            elif '@' not in email or '.' not in email:
                errors.append("Некорректный формат email")
            
            # Проверка пароля
            password = data.get('password', '')
            if not password:
                errors.append("Пароль обязателен")
            elif len(password) < 8:
                errors.append("Пароль должен содержать минимум 8 символов")
            
            # Проверка имени
            full_name = data.get('full_name', '').strip()
            if not full_name:
                errors.append("Полное имя обязательно")
            
            # Проверка возраста
            age = data.get('age')
            if age is not None and (age < 13 or age > 120):
                errors.append("Возраст должен быть от 13 до 120 лет")
            
            return len(errors) == 0, errors
    
    # Декоратор для валидации
    def validate_request(validator: Validator) -> Callable:
        """Декоратор для валидации запросов"""
        def decorator(func: Callable) -> Callable:
            def wrapper(self, data: Any, *args, **kwargs) -> APIResponse:
                is_valid, errors = validator.validate(data)
                
                if not is_valid:
                    return ErrorResponse(
                        error="validation_error",
                        message="Ошибки валидации",
                        status_code=HTTPStatus.BAD_REQUEST.value,
                        details={"validation_errors": errors}
                    )
                
                return func(self, data, *args, **kwargs)
            return wrapper
        return decorator
    
    # API Controller
    class UserController:
        """Контроллер для работы с пользователями"""
        
        def __init__(self) -> None:
            self.users: Dict[int, UserResponse] = {}
            self.next_id = 1
            self.user_validator = UserValidator()
        
        @validate_request(UserValidator())
        def create_user(self, data: CreateUserRequest) -> APIResponse:
            """Создать пользователя"""
            
            # Проверка уникальности username
            for user in self.users.values():
                if user['username'] == data['username']:
                    return ErrorResponse(
                        error="user_exists",
                        message=f"Пользователь {data['username']} уже существует",
                        status_code=HTTPStatus.BAD_REQUEST.value
                    )
            
            # Создание пользователя
            user: UserResponse = {
                'id': self.next_id,
                'username': data['username'],
                'email': data['email'],
                'full_name': data['full_name'],
                'age': data.get('age'),
                'is_active': True,
                'created_at': datetime.now().isoformat()
            }
            
            self.users[self.next_id] = user
            self.next_id += 1
            
            return SuccessResponse(
                data=user,
                status_code=HTTPStatus.CREATED.value,
                message="Пользователь создан успешно"
            )
        
        def get_user(self, user_id: int) -> APIResponse:
            """Получить пользователя по ID"""
            
            if user_id not in self.users:
                return ErrorResponse(
                    error="user_not_found",
                    message=f"Пользователь с ID {user_id} не найден",
                    status_code=HTTPStatus.NOT_FOUND.value
                )
            
            return SuccessResponse(
                data=self.users[user_id],
                status_code=HTTPStatus.OK.value
            )
        
        def update_user(self, user_id: int, data: UpdateUserRequest) -> APIResponse:
            """Обновить пользователя"""
            
            if user_id not in self.users:
                return ErrorResponse(
                    error="user_not_found",
                    message=f"Пользователь с ID {user_id} не найден",
                    status_code=HTTPStatus.NOT_FOUND.value
                )
            
            user = self.users[user_id].copy()
            
            # Обновляем только переданные поля
            for key, value in data.items():
                if key in user:
                    user[key] = value  # type: ignore
            
            self.users[user_id] = user
            
            return SuccessResponse(
                data=user,
                status_code=HTTPStatus.OK.value,
                message="Пользователь обновлен"
            )
        
        def list_users(
            self, 
            filters: Optional[UserFilter] = None,
            page: int = 1,
            page_size: int = 10
        ) -> APIResponse:
            """Получить список пользователей с фильтрацией и пагинацией"""
            
            users = list(self.users.values())
            
            # Применяем фильтры
            if filters:
                if 'username' in filters:
                    users = [u for u in users if filters['username'] in u['username']]
                
                if 'email' in filters:
                    users = [u for u in users if filters['email'] in u['email']]
                
                if 'min_age' in filters:
                    users = [u for u in users if u['age'] and u['age'] >= filters['min_age']]
                
                if 'max_age' in filters:
                    users = [u for u in users if u['age'] and u['age'] <= filters['max_age']]
                
                if 'is_active' in filters:
                    users = [u for u in users if u['is_active'] == filters['is_active']]
            
            total = len(users)
            
            # Пагинация
            start = (page - 1) * page_size
            end = start + page_size
            page_users = users[start:end]
            
            response: PaginatedResponse = {
                'items': page_users,
                'total': total,
                'page': page,
                'page_size': page_size,
                'has_next': end < total,
                'has_prev': page > 1
            }
            
            return SuccessResponse(
                data=response,
                status_code=HTTPStatus.OK.value
            )
        
        def delete_user(self, user_id: int) -> APIResponse:
            """Удалить пользователя"""
            
            if user_id not in self.users:
                return ErrorResponse(
                    error="user_not_found",
                    message=f"Пользователь с ID {user_id} не найден",
                    status_code=HTTPStatus.NOT_FOUND.value
                )
            
            del self.users[user_id]
            
            return SuccessResponse(
                data={"deleted": True},
                status_code=HTTPStatus.OK.value,
                message="Пользователь удален"
            )
    
    # Вспомогательные функции
    def print_api_response(response: APIResponse) -> None:
        """Печать ответа API в читаемом формате"""
        if 'error' in response:
            error_resp = response  # type: ignore
            print(f"❌ Ошибка ({error_resp['status_code']}): {error_resp['message']}")
            if 'details' in error_resp:
                print(f"   Детали: {error_resp['details']}")
        else:
            success_resp = response  # type: ignore
            print(f"✅ Успех ({success_resp['status_code']})")
            if 'message' in success_resp:
                print(f"   Сообщение: {success_resp['message']}")
    
    # Демонстрация
    print("Создание типизированной системы API...")
    
    controller = UserController()
    
    print("\n1. Создание пользователей:")
    
    # Правильный запрос
    valid_request: CreateUserRequest = {
        'username': 'alice_dev',
        'email': 'alice@example.com',
        'password': 'secure123',
        'full_name': 'Алиса Разработчик',
        'age': 28
    }
    
    response = controller.create_user(valid_request)
    print_api_response(response)
    
    # Неправильный запрос
    invalid_request: CreateUserRequest = {
        'username': 'a',  # Слишком короткий
        'email': 'invalid-email',  # Некорректный email
        'password': '123',  # Короткий пароль
        'full_name': ''  # Пустое имя
    }
    
    response = controller.create_user(invalid_request)
    print_api_response(response)
    
    # Еще один правильный запрос
    bob_request: CreateUserRequest = {
        'username': 'bob_admin',
        'email': 'bob@example.com',
        'password': 'password123',
        'full_name': 'Боб Администратор'
    }
    
    response = controller.create_user(bob_request)
    print_api_response(response)
    
    print("\n2. Получение пользователя:")
    
    response = controller.get_user(1)
    print_api_response(response)
    if 'data' in response:
        user_data = response['data']  # type: ignore
        print(f"   Пользователь: {user_data['username']} ({user_data['email']})")
    
    print("\n3. Обновление пользователя:")
    
    update_data: UpdateUserRequest = {
        'full_name': 'Алиса Старший Разработчик',
        'age': 29
    }
    
    response = controller.update_user(1, update_data)
    print_api_response(response)
    
    print("\n4. Список пользователей с фильтрацией:")
    
    # Все пользователи
    response = controller.list_users()
    print_api_response(response)
    if 'data' in response:
        data = response['data']  # type: ignore
        print(f"   Всего пользователей: {data['total']}")
    
    # Фильтрация по возрасту
    age_filter: UserFilter = {
        'min_age': 25,
        'max_age': 35
    }
    
    response = controller.list_users(filters=age_filter)
    print_api_response(response)
    if 'data' in response:
        data = response['data']  # type: ignore
        print(f"   Пользователей в возрасте 25-35: {len(data['items'])}")
    
    print("\n5. Удаление пользователя:")
    
    response = controller.delete_user(2)
    print_api_response(response)
    
    # Попытка получить удаленного пользователя
    response = controller.get_user(2)
    print_api_response(response)
    
    print("✅ Упражнение 2 завершено")


def exercise_03_advanced_generic_system():
    """
    Упражнение 3: Продвинутая система с дженериками
    
    Задача:
    Создайте продвинутую систему с использованием обобщенных типов,
    протоколов, метаклассов и других сложных концепций типизации.
    """
    print("=== Упражнение 3: Продвинутая система с дженериками ===")
    
    # РЕШЕНИЕ:
    
    from typing import ParamSpec, Concatenate
    
    # Параметры для функций
    P = ParamSpec('P')
    T = TypeVar('T')
    U = TypeVar('U')
    R = TypeVar('R')
    
    # Протокол для сериализуемых объектов
    @runtime_checkable
    class Serializable(Protocol):
        """Протокол для сериализуемых объектов"""
        
        def serialize(self) -> Dict[str, Any]:
            """Сериализовать объект в словарь"""
            ...
        
        @classmethod
        def deserialize(cls, data: Dict[str, Any]) -> 'Serializable':
            """Десериализовать объект из словаря"""
            ...
    
    # Протокол для кэшируемых объектов
    class Cacheable(Protocol):
        """Протокол для кэшируемых объектов"""
        
        def get_cache_key(self) -> str:
            """Получить ключ для кэширования"""
            ...
        
        def get_cache_ttl(self) -> int:
            """Получить время жизни в кэше (секунды)"""
            ...
    
    # Ограниченный TypeVar
    SerializableType = TypeVar('SerializableType', bound=Serializable)
    CacheableType = TypeVar('CacheableType', bound=Cacheable)
    
    # Обобщенный кэш
    class Cache(Generic[T]):
        """Типизированный кэш"""
        
        def __init__(self, default_ttl: int = 3600) -> None:
            self._data: Dict[str, Tuple[T, datetime]] = {}
            self._default_ttl = default_ttl
        
        def set(self, key: str, value: T, ttl: Optional[int] = None) -> None:
            """Сохранить значение в кэше"""
            expire_time = datetime.now() + timedelta(seconds=ttl or self._default_ttl)
            self._data[key] = (value, expire_time)
        
        def get(self, key: str) -> Optional[T]:
            """Получить значение из кэша"""
            if key not in self._data:
                return None
            
            value, expire_time = self._data[key]
            
            if datetime.now() > expire_time:
                del self._data[key]
                return None
            
            return value
        
        def delete(self, key: str) -> bool:
            """Удалить значение из кэша"""
            if key in self._data:
                del self._data[key]
                return True
            return False
        
        def clear(self) -> None:
            """Очистить кэш"""
            self._data.clear()
        
        def size(self) -> int:
            """Размер кэша"""
            # Удаляем истекшие записи
            now = datetime.now()
            expired_keys = [
                key for key, (_, expire_time) in self._data.items()
                if now > expire_time
            ]
            
            for key in expired_keys:
                del self._data[key]
            
            return len(self._data)
    
    # Декоратор с типизацией
    def cached(cache: Cache[R]) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Декоратор для кэширования результатов функций"""
        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                # Создаем ключ кэша из аргументов
                cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
                
                # Проверяем кэш
                cached_result = cache.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Вычисляем результат
                result = func(*args, **kwargs)
                
                # Сохраняем в кэш
                cache.set(cache_key, result)
                
                return result
            
            return wrapper
        return decorator
    
    # Repository с обобщенными типами
    class GenericRepository(Generic[T]):
        """Обобщенный репозиторий"""
        
        def __init__(self, entity_type: type[T]) -> None:
            self.entity_type = entity_type
            self._storage: Dict[str, T] = {}
            self._cache: Cache[T] = Cache()
        
        def save(self, entity: T) -> T:
            """Сохранить сущность"""
            if isinstance(entity, Cacheable):
                key = entity.get_cache_key()
                self._storage[key] = entity
                self._cache.set(key, entity, entity.get_cache_ttl())
            else:
                key = str(id(entity))
                self._storage[key] = entity
                self._cache.set(key, entity)
            
            return entity
        
        def find_by_key(self, key: str) -> Optional[T]:
            """Найти сущность по ключу"""
            # Сначала проверяем кэш
            cached = self._cache.get(key)
            if cached is not None:
                return cached
            
            # Затем проверяем хранилище
            if key in self._storage:
                entity = self._storage[key]
                # Добавляем в кэш
                if isinstance(entity, Cacheable):
                    self._cache.set(key, entity, entity.get_cache_ttl())
                else:
                    self._cache.set(key, entity)
                return entity
            
            return None
        
        def find_all(self) -> List[T]:
            """Получить все сущности"""
            return list(self._storage.values())
        
        def delete(self, key: str) -> bool:
            """Удалить сущность"""
            self._cache.delete(key)
            if key in self._storage:
                del self._storage[key]
                return True
            return False
    
    # Конкретные модели
    @dataclass
    class Product:
        """Модель продукта"""
        id: str
        name: str
        price: float
        category: str
        
        def serialize(self) -> Dict[str, Any]:
            """Сериализация продукта"""
            return {
                'id': self.id,
                'name': self.name,
                'price': self.price,
                'category': self.category
            }
        
        @classmethod
        def deserialize(cls, data: Dict[str, Any]) -> 'Product':
            """Десериализация продукта"""
            return cls(
                id=data['id'],
                name=data['name'],
                price=data['price'],
                category=data['category']
            )
        
        def get_cache_key(self) -> str:
            """Ключ для кэширования"""
            return f"product:{self.id}"
        
        def get_cache_ttl(self) -> int:
            """Время жизни в кэше"""
            return 1800  # 30 минут
    
    @dataclass
    class User:
        """Модель пользователя"""
        id: str
        username: str
        email: str
        is_premium: bool = False
        
        def serialize(self) -> Dict[str, Any]:
            """Сериализация пользователя"""
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'is_premium': self.is_premium
            }
        
        @classmethod
        def deserialize(cls, data: Dict[str, Any]) -> 'User':
            """Десериализация пользователя"""
            return cls(
                id=data['id'],
                username=data['username'],
                email=data['email'],
                is_premium=data.get('is_premium', False)
            )
        
        def get_cache_key(self) -> str:
            """Ключ для кэширования"""
            return f"user:{self.id}"
        
        def get_cache_ttl(self) -> int:
            """Время жизни в кэше"""
            return 3600 if self.is_premium else 1800  # Премиум дольше
    
    # Сервис с обобщенными методами
    class DataService:
        """Сервис для работы с данными"""
        
        def __init__(self) -> None:
            self.product_repo: GenericRepository[Product] = GenericRepository(Product)
            self.user_repo: GenericRepository[User] = GenericRepository(User)
            self._string_cache: Cache[str] = Cache()
        
        @cached(Cache[List[Product]]())
        def get_products_by_category(self, category: str) -> List[Product]:
            """Получить продукты по категории (с кэшированием)"""
            all_products = self.product_repo.find_all()
            return [p for p in all_products if p.category == category]
        
        @cached(Cache[int]())
        def count_premium_users(self) -> int:
            """Подсчитать премиум пользователей (с кэшированием)"""
            all_users = self.user_repo.find_all()
            return sum(1 for user in all_users if user.is_premium)
        
        def export_data(self, entities: List[SerializableType]) -> str:
            """Экспорт сериализуемых сущностей в JSON"""
            serialized = [entity.serialize() for entity in entities]
            return json.dumps(serialized, indent=2, ensure_ascii=False)
        
        def import_data(
            self, 
            json_data: str, 
            entity_class: type[SerializableType]
        ) -> List[SerializableType]:
            """Импорт сущностей из JSON"""
            try:
                data_list = json.loads(json_data)
                return [entity_class.deserialize(item) for item in data_list]
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                raise ValueError(f"Ошибка импорта данных: {e}")
        
        def bulk_cache_entities(self, entities: List[CacheableType]) -> None:
            """Массовое кэширование сущностей"""
            for entity in entities:
                if isinstance(entity, Product):
                    self.product_repo.save(entity)
                elif isinstance(entity, User):
                    self.user_repo.save(entity)
    
    # Демонстрация
    print("Создание продвинутой системы с дженериками...")
    
    service = DataService()
    
    print("\n1. Создание и сохранение данных:")
    
    # Создаем продукты
    products = [
        Product("1", "Ноутбук", 99999.99, "Электроника"),
        Product("2", "Смартфон", 49999.99, "Электроника"),
        Product("3", "Книга Python", 2999.99, "Книги"),
        Product("4", "Кружка программиста", 999.99, "Сувениры")
    ]
    
    for product in products:
        service.product_repo.save(product)
    
    print(f"Сохранено {len(products)} продуктов")
    
    # Создаем пользователей
    users = [
        User("1", "alice", "alice@example.com", True),
        User("2", "bob", "bob@example.com", False),
        User("3", "charlie", "charlie@example.com", True)
    ]
    
    for user in users:
        service.user_repo.save(user)
    
    print(f"Сохранено {len(users)} пользователей")
    
    print("\n2. Кэшированные запросы:")
    
    # Первый вызов - вычисляется
    electronics = service.get_products_by_category("Электроника")
    print(f"Продуктов в категории 'Электроника': {len(electronics)}")
    
    # Второй вызов - из кэша
    electronics_cached = service.get_products_by_category("Электроника")
    print(f"Повторный запрос (из кэша): {len(electronics_cached)}")
    
    # Подсчет премиум пользователей
    premium_count = service.count_premium_users()
    print(f"Премиум пользователей: {premium_count}")
    
    print("\n3. Сериализация и импорт/экспорт:")
    
    # Экспорт продуктов
    products_json = service.export_data(products[:2])
    print(f"Экспорт продуктов в JSON:")
    print(products_json[:200] + "...")
    
    # Импорт продуктов
    imported_products = service.import_data(products_json, Product)
    print(f"Импортировано продуктов: {len(imported_products)}")
    
    print("\n4. Проверка типов в runtime:")
    
    # Проверка протоколов
    laptop = products[0]
    print(f"Ноутбук является Serializable: {isinstance(laptop, Serializable)}")
    print(f"Ноутбук является Cacheable: {isinstance(laptop, Cacheable)}")
    
    print("\n5. Статистика кэша:")
    
    product_cache_size = service.product_repo._cache.size()
    user_cache_size = service.user_repo._cache.size()
    
    print(f"Размер кэша продуктов: {product_cache_size}")
    print(f"Размер кэша пользователей: {user_cache_size}")
    
    print("✅ Упражнение 3 завершено")


def main():
    """Главная функция для запуска всех упражнений"""
    
    exercises = [
        ("Типобезопасная ORM система", exercise_01_type_safe_database_orm),
        ("Типизированная система API", exercise_02_api_type_system),
        ("Продвинутая система с дженериками", exercise_03_advanced_generic_system),
    ]
    
    print("🏷️ Упражнения: Типизация и аннотации типов в Python")
    print("=" * 70)
    print("Эти упражнения помогут освоить:")
    print("- Создание сложных типизированных систем")
    print("- Применение продвинутых паттернов типизации")
    print("- Разработку безопасных API с валидацией")
    print("- Работу с обобщенными типами и протоколами")
    print("=" * 70)
    
    for i, (name, func) in enumerate(exercises, 1):
        print(f"\n{i}. {name}")
        print("-" * (len(name) + 3))
        try:
            func()
        except Exception as e:
            print(f"Ошибка при выполнении упражнения: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(exercises):
            input("\nНажмите Enter для продолжения...")
    
    print("\n🎉 Все упражнения по типизации завершены!")


if __name__ == "__main__":
    main() 