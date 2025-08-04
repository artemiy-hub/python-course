#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Исключения в Python

Этот файл содержит подробные примеры для изучения:
- Основных типов исключений
- Обработки исключений try-except-finally
- Создания пользовательских исключений
- Декораторов для обработки ошибок
- Контекстных менеджеров
- Асинхронной обработки исключений
- Профилирования и мониторинга ошибок
"""

import asyncio
import functools
import logging
import time
import traceback
import sys
from datetime import datetime
from typing import Optional, Any, Callable, Type
from contextlib import contextmanager
import json


def example_01_basic_exceptions():
    """
    Пример 1: Основные типы исключений
    
    Демонстрирует различные встроенные исключения Python
    и базовые принципы их обработки.
    """
    print("=== Пример 1: Основные типы исключений ===")
    
    # Функция для демонстрации различных исключений
    def demonstrate_exception(exception_type, description):
        print(f"\n{description}:")
        try:
            if exception_type == "ZeroDivisionError":
                result = 10 / 0
            elif exception_type == "IndexError":
                items = [1, 2, 3]
                value = items[10]
            elif exception_type == "KeyError":
                data = {"a": 1, "b": 2}
                value = data["c"]
            elif exception_type == "ValueError":
                number = int("не число")
            elif exception_type == "TypeError":
                result = "строка" + 42
            elif exception_type == "AttributeError":
                value = "строка".nonexistent_method()
            elif exception_type == "FileNotFoundError":
                with open("несуществующий_файл.txt") as f:
                    content = f.read()
            elif exception_type == "ImportError":
                import несуществующий_модуль
            else:
                print("Неизвестный тип исключения")
                
        except Exception as e:
            print(f"  Поймано исключение: {type(e).__name__}")
            print(f"  Сообщение: {e}")
            print(f"  Модуль: {type(e).__module__}")
    
    # Демонстрация различных исключений
    exceptions_demo = [
        ("ZeroDivisionError", "Деление на ноль"),
        ("IndexError", "Индекс вне диапазона"),
        ("KeyError", "Несуществующий ключ словаря"),
        ("ValueError", "Неправильное значение для типа"),
        ("TypeError", "Операция с несовместимыми типами"),
        ("AttributeError", "Несуществующий атрибут"),
        ("FileNotFoundError", "Файл не найден"),
        ("ImportError", "Модуль не найден"),
    ]
    
    for exc_type, description in exceptions_demo:
        demonstrate_exception(exc_type, description)
    
    print("\n" + "="*50)
    print("Иерархия исключений (примеры наследования):")
    
    # Демонстрация иерархии
    def show_exception_hierarchy():
        try:
            # Это вызовет IndexError
            [1, 2, 3][10]
        except LookupError as e:  # IndexError наследует от LookupError
            print(f"Поймано как LookupError: {type(e).__name__}")
        except Exception as e:
            print(f"Поймано как Exception: {type(e).__name__}")
    
    show_exception_hierarchy()
    
    # Демонстрация информации об исключении
    print("\nПодробная информация об исключении:")
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        print(f"Тип: {type(e)}")
        print(f"Аргументы: {e.args}")
        print(f"Строковое представление: {str(e)}")
        print(f"repr: {repr(e)}")
        
        # Получение информации о трассировке
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"Тип из sys.exc_info(): {exc_type}")
        print(f"Значение из sys.exc_info(): {exc_value}")


def example_02_try_except_patterns():
    """
    Пример 2: Паттерны try-except
    
    Демонстрирует различные способы обработки исключений,
    включая else и finally блоки.
    """
    print("=== Пример 2: Паттерны try-except ===")
    
    def safe_divide(a, b):
        """Безопасное деление с подробной обработкой ошибок"""
        print(f"\nПопытка деления {a} на {b}:")
        
        try:
            # Проверка типов
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                raise TypeError("Аргументы должны быть числами")
            
            # Проверка деления на ноль
            if b == 0:
                raise ZeroDivisionError("Деление на ноль невозможно")
            
            # Выполнение деления
            result = a / b
            
        except TypeError as e:
            print(f"  ❌ Ошибка типа: {e}")
            return None
            
        except ZeroDivisionError as e:
            print(f"  ❌ Математическая ошибка: {e}")
            return None
            
        except Exception as e:
            print(f"  ❌ Неожиданная ошибка: {type(e).__name__}: {e}")
            return None
            
        else:
            # Выполняется только если исключений не было
            print(f"  ✅ Деление успешно: {result}")
            return result
            
        finally:
            # Выполняется всегда
            print(f"  🔄 Операция деления завершена")
    
    # Тестирование различных случаев
    test_cases = [
        (10, 2),      # Нормальный случай
        (10, 0),      # Деление на ноль
        ("10", 2),    # Неправильный тип
        (10.5, 2.1),  # Числа с плавающей точкой
    ]
    
    for a, b in test_cases:
        result = safe_divide(a, b)
        if result is not None:
            print(f"    Результат: {result}")
    
    print("\n" + "="*50)
    print("Множественная обработка исключений:")
    
    def process_data(data):
        """Обработка данных с множественными исключениями"""
        try:
            # Различные операции, которые могут вызвать разные исключения
            if not data:
                raise ValueError("Данные не могут быть пустыми")
            
            if not isinstance(data, dict):
                raise TypeError("Данные должны быть словарем")
            
            if "id" not in data:
                raise KeyError("Отсутствует обязательное поле 'id'")
            
            user_id = int(data["id"])
            
            if user_id <= 0:
                raise ValueError("ID должен быть положительным числом")
            
            # Имитация обработки
            return {"processed_id": user_id, "status": "success"}
            
        except (ValueError, TypeError) as e:
            # Обработка ошибок валидации
            print(f"Ошибка валидации: {e}")
            return {"error": str(e), "type": "validation"}
            
        except KeyError as e:
            # Обработка отсутствующих полей
            print(f"Отсутствует поле: {e}")
            return {"error": f"Отсутствует поле {e}", "type": "missing_field"}
            
        except Exception as e:
            # Обработка всех остальных ошибок
            print(f"Неожиданная ошибка: {e}")
            return {"error": str(e), "type": "unexpected"}
    
    # Тестирование обработки данных
    test_data = [
        {"id": "123"},          # Нормальный случай
        {"id": "0"},            # Неправильное значение
        {"name": "test"},       # Отсутствует ID
        "not a dict",           # Неправильный тип
        None,                   # Пустые данные
        {"id": "не число"},     # Неправильный формат ID
    ]
    
    for data in test_data:
        print(f"\nОбработка данных: {data}")
        result = process_data(data)
        print(f"Результат: {result}")


def example_03_custom_exceptions():
    """
    Пример 3: Пользовательские исключения
    
    Демонстрирует создание собственной иерархии исключений
    для различных типов ошибок в приложении.
    """
    print("=== Пример 3: Пользовательские исключения ===")
    
    # Базовое исключение приложения
    class AppError(Exception):
        """Базовое исключение для приложения"""
        
        def __init__(self, message, error_code=None, context=None):
            super().__init__(message)
            self.error_code = error_code
            self.context = context or {}
            self.timestamp = datetime.now()
        
        def __str__(self):
            msg = self.args[0]
            if self.error_code:
                msg = f"[{self.error_code}] {msg}"
            return msg
        
        def to_dict(self):
            """Преобразование в словарь для JSON"""
            return {
                "error_type": self.__class__.__name__,
                "message": self.args[0],
                "error_code": self.error_code,
                "context": self.context,
                "timestamp": self.timestamp.isoformat()
            }
    
    # Специализированные исключения
    class ValidationError(AppError):
        """Ошибки валидации данных"""
        
        def __init__(self, message, field=None, value=None, error_code=None):
            super().__init__(message, error_code)
            self.field = field
            self.value = value
            self.context.update({
                "field": field,
                "value": value
            })
    
    class BusinessLogicError(AppError):
        """Ошибки бизнес-логики"""
        
        def __init__(self, message, rule=None, error_code=None):
            super().__init__(message, error_code)
            self.rule = rule
            self.context["rule"] = rule
    
    class ExternalServiceError(AppError):
        """Ошибки внешних сервисов"""
        
        def __init__(self, message, service_name=None, status_code=None, error_code=None):
            super().__init__(message, error_code)
            self.service_name = service_name
            self.status_code = status_code
            self.context.update({
                "service": service_name,
                "status_code": status_code
            })
    
    class DatabaseError(AppError):
        """Ошибки базы данных"""
        
        def __init__(self, message, operation=None, table=None, error_code=None):
            super().__init__(message, error_code)
            self.operation = operation
            self.table = table
            self.context.update({
                "operation": operation,
                "table": table
            })
    
    # Пример использования пользовательских исключений
    class UserService:
        """Сервис для работы с пользователями"""
        
        def __init__(self):
            self.users = {"1": {"name": "Алиса", "email": "alice@example.com"}}
        
        def validate_user_data(self, data):
            """Валидация данных пользователя"""
            if not isinstance(data, dict):
                raise ValidationError(
                    "Данные пользователя должны быть словарем",
                    error_code="INVALID_TYPE"
                )
            
            if not data.get("name"):
                raise ValidationError(
                    "Имя пользователя обязательно",
                    field="name",
                    value=data.get("name"),
                    error_code="REQUIRED_FIELD"
                )
            
            if len(data["name"]) < 2:
                raise ValidationError(
                    "Имя должно содержать минимум 2 символа",
                    field="name",
                    value=data["name"],
                    error_code="MIN_LENGTH"
                )
            
            email = data.get("email", "")
            if email and "@" not in email:
                raise ValidationError(
                    "Неправильный формат email",
                    field="email",
                    value=email,
                    error_code="INVALID_FORMAT"
                )
        
        def check_business_rules(self, data):
            """Проверка бизнес-правил"""
            email = data.get("email", "")
            
            # Проверка уникальности email
            for user_id, user in self.users.items():
                if user.get("email") == email:
                    raise BusinessLogicError(
                        f"Email {email} уже используется",
                        rule="unique_email",
                        error_code="DUPLICATE_EMAIL"
                    )
            
            # Имитация проверки через внешний сервис
            if email.endswith("@blocked.com"):
                raise ExternalServiceError(
                    "Email заблокирован службой безопасности",
                    service_name="security_service",
                    status_code=403,
                    error_code="EMAIL_BLOCKED"
                )
        
        def save_user(self, data):
            """Сохранение пользователя"""
            # Имитация ошибки БД
            if data.get("name") == "error":
                raise DatabaseError(
                    "Ошибка при сохранении пользователя",
                    operation="INSERT",
                    table="users",
                    error_code="DB_INSERT_FAILED"
                )
            
            user_id = str(len(self.users) + 1)
            self.users[user_id] = data
            return user_id
        
        def create_user(self, user_data):
            """Создание нового пользователя"""
            try:
                # Валидация
                self.validate_user_data(user_data)
                
                # Проверка бизнес-правил
                self.check_business_rules(user_data)
                
                # Сохранение
                user_id = self.save_user(user_data)
                
                return {"success": True, "user_id": user_id}
                
            except ValidationError as e:
                print(f"❌ Ошибка валидации: {e}")
                return {"success": False, "error": e.to_dict()}
                
            except BusinessLogicError as e:
                print(f"❌ Ошибка бизнес-логики: {e}")
                return {"success": False, "error": e.to_dict()}
                
            except ExternalServiceError as e:
                print(f"❌ Ошибка внешнего сервиса: {e}")
                return {"success": False, "error": e.to_dict()}
                
            except DatabaseError as e:
                print(f"❌ Ошибка базы данных: {e}")
                return {"success": False, "error": e.to_dict()}
                
            except Exception as e:
                # Неожиданная ошибка - оборачиваем в AppError
                app_error = AppError(f"Неожиданная ошибка: {e}", error_code="UNEXPECTED")
                print(f"❌ {app_error}")
                return {"success": False, "error": app_error.to_dict()}
    
    # Тестирование пользовательских исключений
    service = UserService()
    
    test_users = [
        {"name": "Боб", "email": "bob@example.com"},    # Успешный случай
        {"email": "no_name@example.com"},               # Нет имени
        {"name": "A"},                                  # Слишком короткое имя
        {"name": "Чарли", "email": "invalid-email"},    # Неправильный email
        {"name": "Диана", "email": "alice@example.com"}, # Дублирующийся email
        {"name": "Ева", "email": "eva@blocked.com"},    # Заблокированный email
        {"name": "error", "email": "error@example.com"}, # Ошибка БД
        "не словарь",                                   # Неправильный тип
    ]
    
    print("Тестирование создания пользователей:")
    for i, user_data in enumerate(test_users, 1):
        print(f"\n{i}. Создание пользователя: {user_data}")
        result = service.create_user(user_data)
        
        if result["success"]:
            print(f"   ✅ Пользователь создан с ID: {result['user_id']}")
        else:
            error = result["error"]
            print(f"   ❌ {error['error_type']}: {error['message']}")
            if error.get("context"):
                print(f"      Контекст: {error['context']}")


def example_04_exception_decorators():
    """
    Пример 4: Декораторы для обработки исключений
    
    Демонстрирует создание и использование декораторов
    для автоматической обработки исключений.
    """
    print("=== Пример 4: Декораторы для обработки исключений ===")
    
    def retry(max_attempts=3, delay=1, backoff=1, exceptions=(Exception,)):
        """
        Декоратор для повторения функции при исключениях
        
        Args:
            max_attempts: Максимальное количество попыток
            delay: Начальная задержка между попытками
            backoff: Множитель для увеличения задержки
            exceptions: Типы исключений для повтора
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                current_delay = delay
                last_exception = None
                
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt == max_attempts - 1:
                            # Последняя попытка - перебрасываем исключение
                            raise
                        
                        print(f"Попытка {attempt + 1} неудачна: {e}")
                        print(f"Повтор через {current_delay} секунд...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                
                # Это не должно выполниться, но для безопасности
                raise last_exception
            
            return wrapper
        return decorator
    
    def handle_exceptions(*exception_types, default_return=None, log_errors=True):
        """
        Декоратор для обработки исключений с возвратом значения по умолчанию
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except exception_types as e:
                    if log_errors:
                        print(f"Обработано исключение в {func.__name__}: {e}")
                    return default_return
                except Exception as e:
                    if log_errors:
                        print(f"Неожиданное исключение в {func.__name__}: {e}")
                    raise
            return wrapper
        return decorator
    
    def validate_types(**type_checks):
        """
        Декоратор для валидации типов аргументов
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Получаем имена параметров функции
                import inspect
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                
                # Проверяем типы
                for param_name, expected_type in type_checks.items():
                    if param_name in bound_args.arguments:
                        value = bound_args.arguments[param_name]
                        if not isinstance(value, expected_type):
                            raise TypeError(
                                f"Параметр '{param_name}' должен быть типа {expected_type.__name__}, "
                                f"получен {type(value).__name__}"
                            )
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def log_exceptions(logger_name=None):
        """
        Декоратор для логирования исключений
        """
        def decorator(func):
            logger = logging.getLogger(logger_name or func.__module__)
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception(f"Исключение в {func.__name__}")
                    raise
            return wrapper
        return decorator
    
    # Настройка логирования для примера
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Примеры использования декораторов
    
    @retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError, TimeoutError))
    def unreliable_network_call(success_rate=0.3):
        """Ненадежный сетевой вызов"""
        import random
        if random.random() > success_rate:
            raise ConnectionError("Сетевая ошибка")
        return "Успешный ответ от сервера"
    
    @handle_exceptions(ValueError, TypeError, default_return=0)
    def safe_division(a, b):
        """Безопасное деление с обработкой ошибок"""
        return a / b
    
    @validate_types(name=str, age=int, email=str)
    def create_person(name, age, email):
        """Создание персоны с валидацией типов"""
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным")
        return {"name": name, "age": age, "email": email}
    
    @log_exceptions("user_service")
    @handle_exceptions(ValueError, default_return=None)
    def process_user(user_data):
        """Обработка данных пользователя с логированием"""
        if not user_data:
            raise ValueError("Данные пользователя не могут быть пустыми")
        return f"Обработан пользователь: {user_data.get('name', 'Неизвестный')}"
    
    # Тестирование декораторов
    print("1. Тестирование retry декоратора:")
    try:
        result = unreliable_network_call(success_rate=0.7)
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Окончательная ошибка: {e}")
    
    print("\n2. Тестирование обработки исключений:")
    print(f"Безопасное деление 10/2: {safe_division(10, 2)}")
    print(f"Безопасное деление 10/0: {safe_division(10, 0)}")
    print(f"Безопасное деление '10'/2: {safe_division('10', 2)}")
    
    print("\n3. Тестирование валидации типов:")
    try:
        person = create_person("Алиса", 25, "alice@example.com")
        print(f"Персона создана: {person}")
    except Exception as e:
        print(f"Ошибка создания персоны: {e}")
    
    try:
        person = create_person("Боб", "25", "bob@example.com")  # Неправильный тип возраста
    except Exception as e:
        print(f"Ошибка валидации: {e}")
    
    print("\n4. Тестирование логирования:")
    result = process_user({"name": "Тест"})
    print(f"Результат обработки: {result}")
    
    result = process_user(None)  # Вызовет исключение
    print(f"Результат с ошибкой: {result}")


def example_05_context_managers():
    """
    Пример 5: Контекстные менеджеры и исключения
    
    Демонстрирует создание контекстных менеджеров
    для автоматической очистки ресурсов при исключениях.
    """
    print("=== Пример 5: Контекстные менеджеры и исключения ===")
    
    class DatabaseConnection:
        """Имитация подключения к базе данных"""
        
        def __init__(self, connection_string):
            self.connection_string = connection_string
            self.connected = False
            self.transaction_active = False
        
        def connect(self):
            print(f"Подключение к БД: {self.connection_string}")
            # Имитация возможной ошибки подключения
            if "invalid" in self.connection_string:
                raise ConnectionError("Не удалось подключиться к базе данных")
            self.connected = True
        
        def disconnect(self):
            if self.connected:
                print("Отключение от БД")
                self.connected = False
        
        def begin_transaction(self):
            if not self.connected:
                raise RuntimeError("Нет подключения к БД")
            print("Начало транзакции")
            self.transaction_active = True
        
        def commit(self):
            if self.transaction_active:
                print("Коммит транзакции")
                self.transaction_active = False
        
        def rollback(self):
            if self.transaction_active:
                print("Откат транзакции")
                self.transaction_active = False
    
    class DatabaseManager:
        """Контекстный менеджер для работы с БД"""
        
        def __init__(self, connection_string, auto_transaction=True):
            self.connection_string = connection_string
            self.auto_transaction = auto_transaction
            self.connection = None
        
        def __enter__(self):
            self.connection = DatabaseConnection(self.connection_string)
            self.connection.connect()
            
            if self.auto_transaction:
                self.connection.begin_transaction()
            
            return self.connection
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.connection:
                if self.auto_transaction:
                    if exc_type is None:
                        # Нет исключения - коммитим
                        self.connection.commit()
                    else:
                        # Есть исключение - откатываем
                        print(f"Исключение {exc_type.__name__}: {exc_val}")
                        self.connection.rollback()
                
                self.connection.disconnect()
            
            # Не подавляем исключение
            return False
    
    @contextmanager
    def error_handler(error_mapping=None, default_handler=None):
        """
        Контекстный менеджер для централизованной обработки ошибок
        """
        errors = []
        try:
            yield errors
        except Exception as e:
            errors.append(e)
            
            # Ищем специфический обработчик
            if error_mapping:
                for error_type, handler in error_mapping.items():
                    if isinstance(e, error_type):
                        handler(e)
                        return  # Исключение обработано
            
            # Используем обработчик по умолчанию
            if default_handler:
                default_handler(e)
            else:
                # Перебрасываем исключение
                raise
    
    class ResourceManager:
        """Контекстный менеджер для управления ресурсами"""
        
        def __init__(self, resource_name):
            self.resource_name = resource_name
            self.resource = None
            self.allocated = False
        
        def __enter__(self):
            print(f"Выделение ресурса: {self.resource_name}")
            
            # Имитация возможной ошибки выделения
            if "fail" in self.resource_name:
                raise RuntimeError(f"Не удалось выделить ресурс: {self.resource_name}")
            
            self.resource = f"resource_{self.resource_name}"
            self.allocated = True
            return self.resource
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.allocated:
                print(f"Освобождение ресурса: {self.resource_name}")
                if exc_type:
                    print(f"  Ресурс освобожден из-за исключения: {exc_type.__name__}")
                else:
                    print(f"  Ресурс освобожден нормально")
                self.allocated = False
    
    # Тестирование контекстных менеджеров
    
    print("1. Тестирование DatabaseManager:")
    
    # Успешная операция
    try:
        with DatabaseManager("postgresql://localhost:5432/test") as db:
            print("Выполнение операций с БД...")
            # Имитация работы с БД
            print("Операция завершена успешно")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\n" + "-"*30)
    
    # Операция с исключением
    try:
        with DatabaseManager("postgresql://localhost:5432/test") as db:
            print("Выполнение операций с БД...")
            # Имитация ошибки
            raise ValueError("Ошибка в бизнес-логике")
    except Exception as e:
        print(f"Обработано исключение: {e}")
    
    print("\n" + "-"*30)
    
    # Ошибка подключения
    try:
        with DatabaseManager("invalid://connection") as db:
            print("Этот код не выполнится")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n2. Тестирование централизованной обработки ошибок:")
    
    def handle_validation_error(error):
        print(f"📝 Обработка ошибки валидации: {error}")
    
    def handle_network_error(error):
        print(f"🌐 Обработка сетевой ошибки: {error}")
    
    def handle_default_error(error):
        print(f"⚠️ Обработка общей ошибки: {error}")
    
    error_handlers = {
        ValueError: handle_validation_error,
        ConnectionError: handle_network_error,
    }
    
    # Тестирование различных типов ошибок
    test_errors = [
        lambda: ValueError("Неправильные данные"),
        lambda: ConnectionError("Сетевая ошибка"),
        lambda: RuntimeError("Системная ошибка"),
    ]
    
    for i, error_func in enumerate(test_errors, 1):
        print(f"\nТест {i}:")
        with error_handler(error_handlers, handle_default_error):
            raise error_func()
    
    print("\n3. Тестирование управления ресурсами:")
    
    # Успешное выделение и освобождение
    try:
        with ResourceManager("memory_pool") as resource:
            print(f"Работа с ресурсом: {resource}")
            # Имитация работы
            time.sleep(0.1)
    except Exception as e:
        print(f"Ошибка с ресурсом: {e}")
    
    print("\n" + "-"*20)
    
    # Исключение во время работы с ресурсом
    try:
        with ResourceManager("network_socket") as resource:
            print(f"Работа с ресурсом: {resource}")
            raise RuntimeError("Ошибка во время работы с ресурсом")
    except Exception as e:
        print(f"Обработано исключение: {e}")
    
    print("\n" + "-"*20)
    
    # Ошибка выделения ресурса
    try:
        with ResourceManager("fail_resource") as resource:
            print("Этот код не выполнится")
    except Exception as e:
        print(f"Ошибка выделения ресурса: {e}")


def example_06_async_exceptions():
    """
    Пример 6: Асинхронная обработка исключений
    
    Демонстрирует обработку исключений в асинхронном коде,
    включая корутины и параллельное выполнение задач.
    """
    print("=== Пример 6: Асинхронная обработка исключений ===")
    
    async def unreliable_async_operation(operation_id, success_rate=0.5, delay=1):
        """Ненадежная асинхронная операция"""
        await asyncio.sleep(delay)
        
        import random
        if random.random() > success_rate:
            if random.random() > 0.5:
                raise ConnectionError(f"Сетевая ошибка в операции {operation_id}")
            else:
                raise TimeoutError(f"Таймаут в операции {operation_id}")
        
        return f"Результат операции {operation_id}"
    
    async def async_retry(coro_func, max_attempts=3, delay=1, *args, **kwargs):
        """Асинхронный retry для корутин"""
        for attempt in range(max_attempts):
            try:
                return await coro_func(*args, **kwargs)
            except (ConnectionError, TimeoutError) as e:
                if attempt == max_attempts - 1:
                    raise
                print(f"Попытка {attempt + 1} неудачна: {e}")
                await asyncio.sleep(delay)
    
    async def safe_async_operation(operation_id, **kwargs):
        """Безопасная асинхронная операция с обработкой ошибок"""
        try:
            result = await async_retry(
                unreliable_async_operation, 
                max_attempts=3, 
                delay=0.5,
                operation_id=operation_id,
                **kwargs
            )
            return {"success": True, "result": result, "operation_id": operation_id}
        except Exception as e:
            return {
                "success": False, 
                "error": str(e), 
                "error_type": type(e).__name__,
                "operation_id": operation_id
            }
    
    async def batch_async_operations(operation_configs):
        """Выполнение группы асинхронных операций"""
        print(f"Запуск {len(operation_configs)} асинхронных операций...")
        
        # Создаем задачи
        tasks = []
        for config in operation_configs:
            task = asyncio.create_task(
                safe_async_operation(**config),
                name=f"operation_{config['operation_id']}"
            )
            tasks.append(task)
        
        # Ждем завершения всех задач
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Обрабатываем результаты
        successful = 0
        failed = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Задача {i}: Исключение - {result}")
                failed += 1
            elif result.get("success"):
                print(f"✅ Операция {result['operation_id']}: {result['result']}")
                successful += 1
            else:
                print(f"❌ Операция {result['operation_id']}: {result['error']}")
                failed += 1
        
        print(f"\nИтого: {successful} успешных, {failed} неудачных")
        return results
    
    class AsyncContextManager:
        """Асинхронный контекстный менеджер"""
        
        def __init__(self, resource_name):
            self.resource_name = resource_name
            self.resource = None
        
        async def __aenter__(self):
            print(f"Асинхронное выделение ресурса: {self.resource_name}")
            # Имитация асинхронного выделения ресурса
            await asyncio.sleep(0.1)
            
            if "fail" in self.resource_name:
                raise RuntimeError(f"Не удалось выделить ресурс: {self.resource_name}")
            
            self.resource = f"async_resource_{self.resource_name}"
            return self.resource
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            print(f"Асинхронное освобождение ресурса: {self.resource_name}")
            if exc_type:
                print(f"  Освобождение из-за исключения: {exc_type.__name__}")
            
            # Имитация асинхронной очистки
            await asyncio.sleep(0.1)
            return False  # Не подавляем исключения
    
    async def test_async_context_manager():
        """Тестирование асинхронного контекстного менеджера"""
        print("\nТестирование асинхронного контекстного менеджера:")
        
        # Успешный случай
        try:
            async with AsyncContextManager("database") as resource:
                print(f"Работа с ресурсом: {resource}")
                await asyncio.sleep(0.1)
                print("Операция завершена")
        except Exception as e:
            print(f"Ошибка: {e}")
        
        print("\n" + "-"*20)
        
        # Случай с исключением
        try:
            async with AsyncContextManager("network") as resource:
                print(f"Работа с ресурсом: {resource}")
                raise ValueError("Ошибка в обработке")
        except Exception as e:
            print(f"Обработано исключение: {e}")
        
        print("\n" + "-"*20)
        
        # Ошибка выделения ресурса
        try:
            async with AsyncContextManager("fail_resource") as resource:
                print("Этот код не выполнится")
        except Exception as e:
            print(f"Ошибка выделения: {e}")
    
    # Функция для запуска асинхронных примеров
    async def run_async_examples():
        # Конфигурация операций
        operations = [
            {"operation_id": 1, "success_rate": 0.8, "delay": 0.5},
            {"operation_id": 2, "success_rate": 0.3, "delay": 0.3},
            {"operation_id": 3, "success_rate": 0.9, "delay": 0.7},
            {"operation_id": 4, "success_rate": 0.1, "delay": 0.2},
            {"operation_id": 5, "success_rate": 0.7, "delay": 0.4},
        ]
        
        # Запуск группы операций
        await batch_async_operations(operations)
        
        # Тестирование асинхронного контекстного менеджера
        await test_async_context_manager()
    
    # Запуск асинхронных примеров
    try:
        asyncio.run(run_async_examples())
    except Exception as e:
        print(f"Ошибка в асинхронном коде: {e}")


def example_07_exception_monitoring():
    """
    Пример 7: Мониторинг и профилирование исключений
    
    Демонстрирует создание системы для отслеживания
    и анализа исключений в приложении.
    """
    print("=== Пример 7: Мониторинг и профилирование исключений ===")
    
    from collections import defaultdict, Counter
    import threading
    
    class ExceptionMonitor:
        """Система мониторинга исключений"""
        
        def __init__(self):
            self.exception_stats = defaultdict(lambda: {
                'count': 0,
                'total_time': 0,
                'first_seen': None,
                'last_seen': None,
                'locations': Counter(),
                'messages': Counter(),
                'contexts': []
            })
            self.enabled = True
            self.lock = threading.Lock()
        
        def record_exception(self, exc_type, exc_value, exc_traceback, context=None):
            """Записать информацию об исключении"""
            if not self.enabled:
                return
            
            with self.lock:
                exc_name = exc_type.__name__
                now = datetime.now()
                
                stats = self.exception_stats[exc_name]
                stats['count'] += 1
                
                if stats['first_seen'] is None:
                    stats['first_seen'] = now
                stats['last_seen'] = now
                
                # Извлекаем информацию о месте возникновения
                if exc_traceback:
                    tb_lines = traceback.extract_tb(exc_traceback)
                    if tb_lines:
                        last_frame = tb_lines[-1]
                        location = f"{last_frame.filename}:{last_frame.lineno}"
                        stats['locations'][location] += 1
                
                # Сообщение об ошибке
                message = str(exc_value)
                stats['messages'][message] += 1
                
                # Контекст (если предоставлен)
                if context:
                    stats['contexts'].append({
                        'timestamp': now.isoformat(),
                        'context': context
                    })
                    # Ограничиваем количество сохраненных контекстов
                    if len(stats['contexts']) > 100:
                        stats['contexts'] = stats['contexts'][-50:]
        
        def monitor_function(self, func):
            """Декоратор для мониторинга функции"""
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    # Записываем статистику
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    
                    context = {
                        'function': func.__name__,
                        'module': func.__module__,
                        'duration': duration,
                        'args_count': len(args),
                        'kwargs_keys': list(kwargs.keys())
                    }
                    
                    self.record_exception(exc_type, exc_value, exc_traceback, context)
                    
                    # Добавляем время к статистике
                    with self.lock:
                        self.exception_stats[exc_type.__name__]['total_time'] += duration
                    
                    # Перебрасываем исключение
                    raise
            
            return wrapper
        
        def get_report(self, top_n=10):
            """Получить отчет по исключениям"""
            with self.lock:
                if not self.exception_stats:
                    return "Исключения не зафиксированы"
                
                report = ["🔍 ОТЧЕТ ПО ИСКЛЮЧЕНИЯМ", "=" * 50]
                
                # Сортируем по количеству
                sorted_exceptions = sorted(
                    self.exception_stats.items(),
                    key=lambda x: x[1]['count'],
                    reverse=True
                )
                
                for exc_type, stats in sorted_exceptions[:top_n]:
                    avg_time = stats['total_time'] / stats['count'] if stats['count'] > 0 else 0
                    
                    report.append(f"\n🔥 {exc_type}:")
                    report.append(f"   Количество: {stats['count']}")
                    report.append(f"   Общее время: {stats['total_time']:.3f}s")
                    report.append(f"   Среднее время: {avg_time:.3f}s")
                    report.append(f"   Первое: {stats['first_seen']}")
                    report.append(f"   Последнее: {stats['last_seen']}")
                    
                    # Топ локаций
                    if stats['locations']:
                        report.append("   Топ локации:")
                        for location, count in stats['locations'].most_common(3):
                            report.append(f"     {location}: {count}")
                    
                    # Топ сообщения
                    if stats['messages']:
                        report.append("   Топ сообщения:")
                        for message, count in stats['messages'].most_common(3):
                            short_msg = message[:50] + "..." if len(message) > 50 else message
                            report.append(f"     '{short_msg}': {count}")
                
                return "\n".join(report)
        
        def get_stats_json(self):
            """Получить статистику в формате JSON"""
            with self.lock:
                result = {}
                for exc_type, stats in self.exception_stats.items():
                    result[exc_type] = {
                        'count': stats['count'],
                        'total_time': stats['total_time'],
                        'avg_time': stats['total_time'] / stats['count'] if stats['count'] > 0 else 0,
                        'first_seen': stats['first_seen'].isoformat() if stats['first_seen'] else None,
                        'last_seen': stats['last_seen'].isoformat() if stats['last_seen'] else None,
                        'top_locations': dict(stats['locations'].most_common(5)),
                        'top_messages': dict(stats['messages'].most_common(5))
                    }
                return result
        
        def reset_stats(self):
            """Сброс статистики"""
            with self.lock:
                self.exception_stats.clear()
    
    # Глобальный монитор исключений
    monitor = ExceptionMonitor()
    
    # Примеры функций для мониторинга
    @monitor.monitor_function
    def problematic_function(operation_type, data=None):
        """Функция с различными типами ошибок"""
        if operation_type == "division_by_zero":
            return 10 / 0
        elif operation_type == "index_error":
            return [1, 2, 3][10]
        elif operation_type == "key_error":
            return {"a": 1}["b"]
        elif operation_type == "value_error":
            return int("не число")
        elif operation_type == "type_error":
            return "строка" + 42
        elif operation_type == "custom_error":
            raise RuntimeError(f"Пользовательская ошибка с данными: {data}")
        elif operation_type == "success":
            return "Операция выполнена успешно"
        else:
            raise ValueError(f"Неизвестный тип операции: {operation_type}")
    
    @monitor.monitor_function
    def network_simulation(endpoint, timeout=1):
        """Имитация сетевых запросов"""
        import random
        time.sleep(timeout * random.random())
        
        if "timeout" in endpoint:
            raise TimeoutError(f"Таймаут при запросе к {endpoint}")
        elif "error" in endpoint:
            raise ConnectionError(f"Ошибка соединения с {endpoint}")
        elif "not_found" in endpoint:
            raise ValueError(f"Ресурс не найден: {endpoint}")
        else:
            return f"Ответ от {endpoint}"
    
    @monitor.monitor_function
    def data_processor(data_batch):
        """Обработка пакета данных"""
        if not data_batch:
            raise ValueError("Пакет данных не может быть пустым")
        
        if not isinstance(data_batch, list):
            raise TypeError("Пакет должен быть списком")
        
        if len(data_batch) > 1000:
            raise RuntimeError("Слишком большой пакет данных")
        
        # Имитация обработки
        processed = 0
        for item in data_batch:
            if item is None:
                raise ValueError("Элемент пакета не может быть None")
            processed += 1
        
        return f"Обработано {processed} элементов"
    
    # Тестирование мониторинга
    print("Запуск тестов с мониторингом исключений...")
    
    # Тестируем различные типы ошибок
    test_operations = [
        ("success", None),
        ("division_by_zero", None),
        ("index_error", None),
        ("key_error", None),
        ("value_error", None),
        ("type_error", None),
        ("custom_error", {"user_id": 123}),
        ("unknown_operation", None),
    ] * 3  # Повторяем для статистики
    
    for operation, data in test_operations:
        try:
            result = problematic_function(operation, data)
            print(f"✅ {operation}: {result}")
        except Exception as e:
            print(f"❌ {operation}: {type(e).__name__}: {e}")
    
    # Тестируем сетевые операции
    endpoints = [
        "api/users",
        "api/timeout_service",
        "api/error_service", 
        "api/not_found_resource",
        "api/data",
    ] * 2
    
    for endpoint in endpoints:
        try:
            result = network_simulation(endpoint, timeout=0.1)
            print(f"✅ {endpoint}: {result}")
        except Exception as e:
            print(f"❌ {endpoint}: {type(e).__name__}: {e}")
    
    # Тестируем обработку данных
    test_batches = [
        [1, 2, 3, 4, 5],
        [],
        "не список",
        [1, 2, None, 4],
        list(range(1001)),  # Слишком большой
    ]
    
    for batch in test_batches:
        try:
            result = data_processor(batch)
            print(f"✅ Пакет данных: {result}")
        except Exception as e:
            print(f"❌ Пакет данных: {type(e).__name__}: {e}")
    
    # Выводим отчет
    print("\n" + monitor.get_report())
    
    # Сохраняем статистику в JSON
    stats_json = monitor.get_stats_json()
    print(f"\nСтатистика в JSON формате:")
    print(json.dumps(stats_json, ensure_ascii=False, indent=2))


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Основные типы исключений", example_01_basic_exceptions),
        ("Паттерны try-except", example_02_try_except_patterns),
        ("Пользовательские исключения", example_03_custom_exceptions),
        ("Декораторы для исключений", example_04_exception_decorators),
        ("Контекстные менеджеры", example_05_context_managers),
        ("Асинхронные исключения", example_06_async_exceptions),
        ("Мониторинг исключений", example_07_exception_monitoring),
    ]
    
    print("🔥 Примеры: Исключения в Python")
    print("=" * 50)
    
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