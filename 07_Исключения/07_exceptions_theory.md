# Теория: Исключения в Python

## 🎯 Цель раздела

Исключения в Python - это мощный механизм обработки ошибок, который позволяет программам корректно реагировать на непредвиденные ситуации. Изучение исключений критически важно для создания надежных и устойчивых приложений.

## 📋 Содержание

1. [Основы исключений](#основы-исключений)
2. [Иерархия исключений](#иерархия-исключений)
3. [Обработка исключений](#обработка-исключений)
4. [Создание собственных исключений](#создание-собственных-исключений)
5. [Продвинутые техники](#продвинутые-техники)
6. [Лучшие практики](#лучшие-практики)
7. [Отладка и логирование](#отладка-и-логирование)

---

## 🔥 Основы исключений

### Что такое исключения

**Исключение** (Exception) - это событие, которое происходит во время выполнения программы и нарушает нормальный поток выполнения инструкций. В Python исключения представлены объектами, которые содержат информацию об ошибке.

### Основные типы ошибок

```python
# SyntaxError - синтаксическая ошибка
# print("Hello"  # Пропущена закрывающая скобка

# NameError - неопределенная переменная
# print(undefined_variable)

# TypeError - неправильный тип
# "string" + 5

# ValueError - правильный тип, но неправильное значение
# int("not_a_number")

# IndexError - индекс вне диапазона
# [1, 2, 3][10]

# KeyError - несуществующий ключ
# {"a": 1}["b"]

# FileNotFoundError - файл не найден
# open("nonexistent.txt")

# ZeroDivisionError - деление на ноль
# 10 / 0
```

### Анатомия исключения

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Ошибка: {e}")
    print(f"Тип исключения: {type(e)}")
    print(f"Аргументы: {e.args}")
    print(f"Строковое представление: {str(e)}")
```

**Результат:**
```
Ошибка: division by zero
Тип исключения: <class 'ZeroDivisionError'>
Аргументы: ('division by zero',)
Строковое представление: division by zero
```

---

## 🏗️ Иерархия исключений

### Базовая иерархия

Python имеет хорошо структурированную иерархию исключений:

```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── StopAsyncIteration
    ├── ArithmeticError
    │   ├── FloatingPointError
    │   ├── OverflowError
    │   └── ZeroDivisionError
    ├── AssertionError
    ├── AttributeError
    ├── BufferError
    ├── EOFError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── MemoryError
    ├── NameError
    │   └── UnboundLocalError
    ├── OSError
    │   ├── BlockingIOError
    │   ├── ChildProcessError
    │   ├── ConnectionError
    │   │   ├── BrokenPipeError
    │   │   ├── ConnectionAbortedError
    │   │   ├── ConnectionRefusedError
    │   │   └── ConnectionResetError
    │   ├── FileExistsError
    │   ├── FileNotFoundError
    │   ├── InterruptedError
    │   ├── IsADirectoryError
    │   ├── NotADirectoryError
    │   ├── PermissionError
    │   ├── ProcessLookupError
    │   └── TimeoutError
    ├── ReferenceError
    ├── RuntimeError
    │   ├── NotImplementedError
    │   └── RecursionError
    ├── SyntaxError
    │   └── IndentationError
    │       └── TabError
    ├── SystemError
    ├── TypeError
    ├── ValueError
    │   └── UnicodeError
    │       ├── UnicodeDecodeError
    │       ├── UnicodeEncodeError
    │       └── UnicodeTranslateError
    └── Warning
        ├── DeprecationWarning
        ├── PendingDeprecationWarning
        ├── RuntimeWarning
        ├── SyntaxWarning
        ├── UserWarning
        ├── FutureWarning
        ├── ImportWarning
        ├── UnicodeWarning
        ├── BytesWarning
        └── ResourceWarning
```

### Категории исключений

#### 1. **ArithmeticError** - Арифметические ошибки

```python
# ZeroDivisionError
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Деление на ноль!")

# OverflowError (редко в Python 3)
import math
try:
    result = math.exp(1000)
except OverflowError:
    print("Переполнение!")

# FloatingPointError
import numpy as np
try:
    np.seterr(all='raise')
    result = np.float64(1) / np.float64(0)
except FloatingPointError:
    print("Ошибка плавающей точки!")
```

#### 2. **LookupError** - Ошибки поиска

```python
# IndexError
try:
    items = [1, 2, 3]
    print(items[10])
except IndexError:
    print("Индекс вне диапазона!")

# KeyError
try:
    data = {"a": 1, "b": 2}
    print(data["c"])
except KeyError:
    print("Ключ не найден!")
```

#### 3. **OSError** - Ошибки операционной системы

```python
# FileNotFoundError
try:
    with open("nonexistent.txt") as f:
        content = f.read()
except FileNotFoundError:
    print("Файл не найден!")

# PermissionError
try:
    with open("/root/restricted.txt", "w") as f:
        f.write("data")
except PermissionError:
    print("Нет прав доступа!")

# ConnectionError (и его подтипы)
import requests
try:
    response = requests.get("http://nonexistent-domain.xyz")
except ConnectionError:
    print("Ошибка соединения!")
```

#### 4. **ValueError** - Неправильные значения

```python
# Неправильное значение для типа
try:
    number = int("not_a_number")
except ValueError:
    print("Не удается преобразовать в число!")

# Неправильные параметры функции
try:
    import math
    result = math.sqrt(-1)
except ValueError:
    print("Квадратный корень из отрицательного числа!")

# UnicodeError
try:
    text = b'\x80\x81'.decode('utf-8')
except UnicodeDecodeError:
    print("Ошибка декодирования Unicode!")
```

#### 5. **TypeError** - Неправильные типы

```python
# Операции с несовместимыми типами
try:
    result = "строка" + 42
except TypeError:
    print("Нельзя складывать строку и число!")

# Неправильное количество аргументов
def greet(name, age):
    return f"Привет, {name}! Тебе {age} лет."

try:
    message = greet("Алиса")  # Не хватает аргумента
except TypeError:
    print("Неправильное количество аргументов!")

# Неправильный тип аргумента
try:
    result = len(42)  # len() ожидает последовательность
except TypeError:
    print("Объект не имеет длины!")
```

---

## 🛡️ Обработка исключений

### Базовый синтаксис try-except

```python
try:
    # Код, который может вызвать исключение
    risky_operation()
except SpecificException:
    # Обработка конкретного исключения
    handle_specific_error()
except AnotherException as e:
    # Обработка с доступом к объекту исключения
    handle_another_error(e)
except (Exception1, Exception2):
    # Обработка нескольких типов исключений
    handle_multiple_errors()
except Exception as e:
    # Обработка всех остальных исключений
    handle_general_error(e)
else:
    # Выполняется, если исключений не было
    success_operation()
finally:
    # Выполняется всегда
    cleanup_operation()
```

### Детальные примеры обработки

#### Обработка файловых операций

```python
def safe_file_read(filename):
    """Безопасное чтение файла с обработкой различных ошибок"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден")
        return None
        
    except PermissionError:
        print(f"Ошибка: Нет прав для чтения файла '{filename}'")
        return None
        
    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки: {e}")
        # Попробуем другую кодировку
        try:
            with open(filename, 'r', encoding='cp1251') as file:
                content = file.read()
        except:
            print("Не удалось определить кодировку файла")
            return None
            
    except OSError as e:
        print(f"Ошибка операционной системы: {e}")
        return None
        
    except Exception as e:
        print(f"Неожиданная ошибка: {type(e).__name__}: {e}")
        return None
        
    else:
        print(f"Файл '{filename}' успешно прочитан")
        return content
        
    finally:
        print("Операция чтения файла завершена")

# Использование
content = safe_file_read("example.txt")
if content:
    print(f"Содержимое: {content[:100]}...")
```

#### Обработка сетевых запросов

```python
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

def safe_http_request(url, timeout=10, retries=3):
    """Безопасное выполнение HTTP запроса"""
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Поднимает HTTPError для плохих статусов
            
        except ConnectionError:
            print(f"Попытка {attempt + 1}: Ошибка соединения с {url}")
            if attempt == retries - 1:
                raise
            continue
            
        except Timeout:
            print(f"Попытка {attempt + 1}: Превышено время ожидания для {url}")
            if attempt == retries - 1:
                raise
            continue
            
        except requests.HTTPError as e:
            print(f"HTTP ошибка: {e.response.status_code} - {e.response.reason}")
            raise
            
        except RequestException as e:
            print(f"Ошибка запроса: {e}")
            raise
            
        else:
            print(f"Запрос к {url} выполнен успешно")
            return response.json()
    
    raise ConnectionError(f"Не удалось подключиться к {url} после {retries} попыток")

# Использование
try:
    data = safe_http_request("https://api.github.com/users/octocat")
    print(f"Получены данные: {data['name']}")
except Exception as e:
    print(f"Финальная ошибка: {e}")
```

#### Обработка пользовательского ввода

```python
def get_user_age():
    """Получение возраста пользователя с валидацией"""
    
    while True:
        try:
            age_input = input("Введите ваш возраст: ").strip()
            
            if not age_input:
                raise ValueError("Возраст не может быть пустым")
            
            age = int(age_input)
            
            if age < 0:
                raise ValueError("Возраст не может быть отрицательным")
            elif age > 150:
                raise ValueError("Возраст не может быть больше 150")
                
        except ValueError as e:
            if "invalid literal" in str(e):
                print("Ошибка: Введите число")
            else:
                print(f"Ошибка: {e}")
            continue
            
        except KeyboardInterrupt:
            print("\nОперация прервана пользователем")
            return None
            
        except EOFError:
            print("\nДостигнут конец ввода")
            return None
            
        else:
            return age

# Использование
age = get_user_age()
if age is not None:
    print(f"Ваш возраст: {age} лет")
```

### Цепочки исключений

Python 3 поддерживает цепочки исключений, которые помогают сохранить контекст оригинального исключения:

```python
def process_data(data):
    try:
        # Какая-то обработка данных
        result = complex_calculation(data)
    except ValueError as e:
        # Поднимаем новое исключение, сохраняя оригинальное
        raise RuntimeError("Ошибка обработки данных") from e

def complex_calculation(data):
    if not isinstance(data, (int, float)):
        raise ValueError("Данные должны быть числом")
    return data * 2

try:
    result = process_data("invalid")
except RuntimeError as e:
    print(f"Основная ошибка: {e}")
    print(f"Причина: {e.__cause__}")
    print(f"Тип причины: {type(e.__cause__)}")
```

**Результат:**
```
Основная ошибка: Ошибка обработки данных
Причина: Данные должны быть числом
Тип причины: <class 'ValueError'>
```

---

## 🏭 Создание собственных исключений

### Базовые принципы

```python
# Простое пользовательское исключение
class CustomError(Exception):
    """Базовое пользовательское исключение"""
    pass

# Исключение с дополнительной информацией
class ValidationError(Exception):
    """Исключение для ошибок валидации"""
    
    def __init__(self, message, field=None, value=None):
        super().__init__(message)
        self.field = field
        self.value = value
        
    def __str__(self):
        if self.field:
            return f"Ошибка валидации поля '{self.field}': {self.args[0]}"
        return self.args[0]

# Использование
try:
    raise ValidationError("Неправильный формат email", 
                         field="email", 
                         value="invalid-email")
except ValidationError as e:
    print(f"Ошибка: {e}")
    print(f"Поле: {e.field}")
    print(f"Значение: {e.value}")
```

### Иерархия пользовательских исключений

```python
# Базовое исключение для приложения
class AppError(Exception):
    """Базовое исключение для приложения"""
    
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.timestamp = datetime.now()

# Исключения для различных подсистем
class DatabaseError(AppError):
    """Ошибки базы данных"""
    pass

class ConnectionError(DatabaseError):
    """Ошибки соединения с БД"""
    pass

class QueryError(DatabaseError):
    """Ошибки выполнения запросов"""
    
    def __init__(self, message, query=None, error_code=None):
        super().__init__(message, error_code)
        self.query = query

class AuthenticationError(AppError):
    """Ошибки аутентификации"""
    pass

class AuthorizationError(AppError):
    """Ошибки авторизации"""
    
    def __init__(self, message, required_permission=None, error_code=None):
        super().__init__(message, error_code)
        self.required_permission = required_permission

class ValidationError(AppError):
    """Ошибки валидации данных"""
    
    def __init__(self, message, field=None, value=None, error_code=None):
        super().__init__(message, error_code)
        self.field = field
        self.value = value
        self.errors = {}
    
    def add_error(self, field, message):
        """Добавить ошибку для конкретного поля"""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)

# Пример использования иерархии
class UserService:
    def create_user(self, user_data):
        try:
            # Валидация
            if not user_data.get('email'):
                raise ValidationError(
                    "Email обязателен", 
                    field="email", 
                    error_code="REQUIRED_FIELD"
                )
            
            if '@' not in user_data['email']:
                raise ValidationError(
                    "Неправильный формат email", 
                    field="email", 
                    value=user_data['email'],
                    error_code="INVALID_FORMAT"
                )
            
            # Проверка в БД
            if self.email_exists(user_data['email']):
                raise ValidationError(
                    "Email уже используется", 
                    field="email",
                    value=user_data['email'],
                    error_code="DUPLICATE_EMAIL"
                )
            
            # Сохранение
            return self.save_user(user_data)
            
        except ValidationError:
            # Перебрасываем ошибки валидации как есть
            raise
        except DatabaseError as e:
            # Оборачиваем ошибки БД
            raise AppError(f"Не удалось создать пользователя: {e}") from e
    
    def email_exists(self, email):
        # Имитация проверки в БД
        return email == "existing@example.com"
    
    def save_user(self, user_data):
        # Имитация сохранения
        return {"id": 123, **user_data}

# Использование с обработкой разных типов ошибок
service = UserService()

test_cases = [
    {},  # Пустые данные
    {"email": "invalid-email"},  # Неправильный формат
    {"email": "existing@example.com"},  # Существующий email
    {"email": "new@example.com"}  # Корректные данные
]

for user_data in test_cases:
    try:
        result = service.create_user(user_data)
        print(f"✓ Пользователь создан: {result}")
        
    except ValidationError as e:
        print(f"✗ Ошибка валидации: {e}")
        print(f"  Код ошибки: {e.error_code}")
        if e.field:
            print(f"  Поле: {e.field}")
        if e.value:
            print(f"  Значение: {e.value}")
            
    except DatabaseError as e:
        print(f"✗ Ошибка БД: {e}")
        print(f"  Код ошибки: {e.error_code}")
        
    except AppError as e:
        print(f"✗ Ошибка приложения: {e}")
        print(f"  Время: {e.timestamp}")
        
    print()
```

### Исключения с контекстом

```python
class BusinessLogicError(Exception):
    """Исключение для ошибок бизнес-логики"""
    
    def __init__(self, message, context=None, suggestions=None):
        super().__init__(message)
        self.context = context or {}
        self.suggestions = suggestions or []
    
    def add_context(self, key, value):
        """Добавить контекстную информацию"""
        self.context[key] = value
    
    def add_suggestion(self, suggestion):
        """Добавить предложение по исправлению"""
        self.suggestions.append(suggestion)
    
    def __str__(self):
        msg = self.args[0]
        
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            msg += f" (Контекст: {context_str})"
        
        if self.suggestions:
            suggestions_str = "; ".join(self.suggestions)
            msg += f" [Предложения: {suggestions_str}]"
        
        return msg

# Пример использования
def process_order(order_id, items):
    error = BusinessLogicError("Не удалось обработать заказ")
    error.add_context("order_id", order_id)
    error.add_context("items_count", len(items))
    
    if not items:
        error.add_suggestion("Добавьте товары в заказ")
        raise error
    
    total_cost = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
    error.add_context("total_cost", total_cost)
    
    if total_cost <= 0:
        error.add_suggestion("Проверьте цены и количество товаров")
        raise error
    
    if total_cost > 10000:
        error.add_suggestion("Разделите заказ на несколько частей")
        error.add_suggestion("Обратитесь к менеджеру для больших заказов")
        raise error

try:
    process_order(12345, [
        {"name": "Laptop", "price": 8000, "quantity": 2}
    ])
except BusinessLogicError as e:
    print(f"Ошибка: {e}")
```

---

## ⚡ Продвинутые техники

### Декораторы для обработки исключений

```python
import functools
import logging
import time
from typing import Type, Union, Tuple

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Декоратор для повторения функции при исключениях"""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Попытка {attempt + 1} неудачна: {e}")
                    time.sleep(delay)
            
        return wrapper
    return decorator

def handle_exceptions(*exception_types, default_return=None, log_errors=True):
    """Декоратор для обработки исключений"""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_types as e:
                if log_errors:
                    logging.error(f"Ошибка в {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator

def validate_args(**validators):
    """Декоратор для валидации аргументов функции"""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем имена параметров
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Валидируем каждый аргумент
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        raise ValidationError(
                            f"Неправильное значение для параметра '{param_name}': {value}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Примеры использования декораторов

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def unreliable_network_call():
    """Ненадежный сетевой вызов"""
    import random
    if random.random() < 0.7:  # 70% вероятность ошибки
        raise ConnectionError("Сетевая ошибка")
    return "Успешный ответ"

@handle_exceptions(ValueError, TypeError, default_return=0, log_errors=True)
def safe_division(a, b):
    """Безопасное деление"""
    return a / b

@validate_args(
    name=lambda x: isinstance(x, str) and len(x) > 0,
    age=lambda x: isinstance(x, int) and 0 <= x <= 150,
    email=lambda x: isinstance(x, str) and '@' in x
)
def create_person(name, age, email):
    """Создание персоны с валидацией"""
    return {"name": name, "age": age, "email": email}

# Тестирование декораторов
try:
    result = unreliable_network_call()
    print(f"Результат сетевого вызова: {result}")
except Exception as e:
    print(f"Окончательная ошибка: {e}")

print(f"Безопасное деление: {safe_division(10, 2)}")  # 5.0
print(f"Безопасное деление: {safe_division(10, 0)}")  # 0

try:
    person = create_person("Алиса", 25, "alice@example.com")
    print(f"Персона создана: {person}")
except ValidationError as e:
    print(f"Ошибка валидации: {e}")

try:
    person = create_person("", 25, "alice@example.com")  # Пустое имя
except ValidationError as e:
    print(f"Ошибка валидации: {e}")
```

### Контекстные менеджеры с исключениями

```python
class TransactionManager:
    """Контекстный менеджер для управления транзакциями"""
    
    def __init__(self, connection):
        self.connection = connection
        self.transaction = None
    
    def __enter__(self):
        try:
            self.transaction = self.connection.begin()
            return self.transaction
        except Exception as e:
            raise DatabaseError(f"Не удалось начать транзакцию: {e}") from e
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # Нет исключения - коммитим
            try:
                self.transaction.commit()
            except Exception as e:
                # Если коммит не удался, откатываем
                try:
                    self.transaction.rollback()
                except:
                    pass
                raise DatabaseError(f"Не удалось зафиксировать транзакцию: {e}") from e
        else:
            # Есть исключение - откатываем
            try:
                self.transaction.rollback()
            except Exception as rollback_error:
                # Логируем ошибку отката, но не перекрываем оригинальное исключение
                logging.error(f"Ошибка отката транзакции: {rollback_error}")
        
        # Возвращаем False, чтобы исключение не подавлялось
        return False

class ErrorHandler:
    """Контекстный менеджер для централизованной обработки ошибок"""
    
    def __init__(self, error_mapping=None, default_action=None):
        self.error_mapping = error_mapping or {}
        self.default_action = default_action
        self.errors = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        
        # Записываем ошибку
        self.errors.append((exc_type, exc_val, exc_tb))
        
        # Ищем обработчик для конкретного типа исключения
        for error_type, handler in self.error_mapping.items():
            if issubclass(exc_type, error_type):
                try:
                    handler(exc_val)
                    return True  # Подавляем исключение
                except Exception as handler_error:
                    logging.error(f"Ошибка в обработчике: {handler_error}")
                    break
        
        # Используем обработчик по умолчанию
        if self.default_action:
            try:
                self.default_action(exc_val)
                return True
            except Exception as handler_error:
                logging.error(f"Ошибка в обработчике по умолчанию: {handler_error}")
        
        # Не подавляем исключение
        return False
    
    def add_handler(self, exception_type, handler):
        """Добавить обработчик для типа исключения"""
        self.error_mapping[exception_type] = handler

# Использование контекстных менеджеров
def save_user_data(user_data):
    """Сохранение данных пользователя с обработкой ошибок"""
    
    def handle_validation_error(error):
        print(f"Ошибка валидации: {error}")
        # Логирование, отправка уведомления и т.д.
    
    def handle_database_error(error):
        print(f"Ошибка БД: {error}")
        # Попытка переподключения, использование резервной БД и т.д.
    
    def handle_general_error(error):
        print(f"Общая ошибка: {error}")
        # Логирование, уведомление администратора
    
    error_handler = ErrorHandler(
        error_mapping={
            ValidationError: handle_validation_error,
            DatabaseError: handle_database_error,
        },
        default_action=handle_general_error
    )
    
    with error_handler:
        # Валидация данных
        if not user_data.get('email'):
            raise ValidationError("Email обязателен")
        
        # Имитация работы с БД
        if user_data['email'] == 'error@example.com':
            raise DatabaseError("Ошибка подключения к БД")
        
        if user_data['email'] == 'unknown@example.com':
            raise RuntimeError("Неожиданная ошибка")
        
        print(f"Пользователь сохранен: {user_data}")

# Тестирование
test_users = [
    {"email": "valid@example.com", "name": "Алиса"},
    {"name": "Боб"},  # Нет email
    {"email": "error@example.com", "name": "Чарли"},  # Ошибка БД
    {"email": "unknown@example.com", "name": "Диана"},  # Неожиданная ошибка
]

for user in test_users:
    print(f"\nОбработка пользователя: {user}")
    save_user_data(user)
```

### Асинхронная обработка исключений

```python
import asyncio
import aiohttp
from typing import List, Dict, Any

class AsyncRetry:
    """Асинхронный ретрай декоратор"""
    
    def __init__(self, max_attempts=3, delay=1, backoff=1, exceptions=(Exception,)):
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions
    
    def __call__(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = self.delay
            
            for attempt in range(self.max_attempts):
                try:
                    return await func(*args, **kwargs)
                except self.exceptions as e:
                    if attempt == self.max_attempts - 1:
                        raise
                    
                    print(f"Попытка {attempt + 1} неудачна: {e}")
                    await asyncio.sleep(current_delay)
                    current_delay *= self.backoff
            
        return wrapper

async def fetch_url_safe(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Безопасное получение данных по URL"""
    
    @AsyncRetry(max_attempts=3, delay=0.5, backoff=2, 
                exceptions=(aiohttp.ClientError, asyncio.TimeoutError))
    async def _fetch():
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientResponseError as e:
            if e.status >= 500:
                # Серверные ошибки - можно повторить
                raise
            else:
                # Клиентские ошибки - не повторяем
                return {"error": f"HTTP {e.status}: {e.message}", "url": url}
                
        except aiohttp.ClientConnectionError:
            raise ConnectionError(f"Не удалось подключиться к {url}")
            
        except asyncio.TimeoutError:
            raise TimeoutError(f"Превышено время ожидания для {url}")
    
    try:
        return await _fetch()
    except Exception as e:
        return {"error": str(e), "url": url}

async def fetch_multiple_urls(urls: List[str]) -> List[Dict[str, Any]]:
    """Получение данных от нескольких URL с обработкой ошибок"""
    
    async with aiohttp.ClientSession() as session:
        # Создаем задачи для всех URL
        tasks = [fetch_url_safe(session, url) for url in urls]
        
        # Выполняем все задачи параллельно
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Обрабатываем результаты
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "error": str(result),
                    "url": urls[i],
                    "exception_type": type(result).__name__
                })
            else:
                processed_results.append(result)
        
        return processed_results

# Пример использования асинхронной обработки ошибок
async def main():
    urls = [
        "https://api.github.com/users/octocat",
        "https://httpbin.org/status/500",  # Серверная ошибка
        "https://httpbin.org/status/404",  # Клиентская ошибка
        "https://nonexistent-domain-12345.com",  # Ошибка соединения
        "https://httpbin.org/delay/10",  # Таймаут
    ]
    
    print("Запуск асинхронных запросов...")
    results = await fetch_multiple_urls(urls)
    
    for i, result in enumerate(results):
        print(f"\nURL {i + 1}: {urls[i]}")
        if "error" in result:
            print(f"  ❌ Ошибка: {result['error']}")
        else:
            print(f"  ✅ Успех: {len(str(result))} символов данных")

# Запуск асинхронного примера
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
```

---

## 🎯 Лучшие практики

### 1. Принцип специфичности

```python
# ❌ Плохо - слишком общий except
try:
    data = json.loads(text)
    result = process_data(data)
except Exception:
    print("Что-то пошло не так")

# ✅ Хорошо - специфичные исключения
try:
    data = json.loads(text)
    result = process_data(data)
except json.JSONDecodeError as e:
    print(f"Ошибка парсинга JSON: {e}")
except ValueError as e:
    print(f"Неправильные данные: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
    # Логирование полной информации об ошибке
    logging.exception("Неожиданная ошибка в process_data")
```

### 2. Принцип раннего возврата

```python
# ❌ Плохо - глубокая вложенность
def process_user_data(user_data):
    try:
        if user_data:
            if 'email' in user_data:
                if '@' in user_data['email']:
                    # Обработка...
                    return result
                else:
                    raise ValidationError("Неправильный email")
            else:
                raise ValidationError("Email отсутствует")
        else:
            raise ValidationError("Данные пользователя отсутствуют")
    except ValidationError:
        # Обработка ошибки
        pass

# ✅ Хорошо - ранние проверки
def process_user_data(user_data):
    if not user_data:
        raise ValidationError("Данные пользователя отсутствуют")
    
    if 'email' not in user_data:
        raise ValidationError("Email отсутствует")
    
    if '@' not in user_data['email']:
        raise ValidationError("Неправильный email")
    
    # Основная логика
    return process_valid_data(user_data)
```

### 3. Принцип информативности

```python
# ❌ Плохо - неинформативные сообщения
try:
    user = get_user(user_id)
    update_user(user, new_data)
except Exception:
    print("Ошибка")

# ✅ Хорошо - подробные сообщения
try:
    user = get_user(user_id)
    if not user:
        raise ValueError(f"Пользователь с ID {user_id} не найден")
    
    update_user(user, new_data)
    
except ValueError as e:
    print(f"Ошибка валидации: {e}")
    logging.warning(f"Попытка обновления несуществующего пользователя: {user_id}")
    
except DatabaseError as e:
    print(f"Ошибка базы данных при обновлении пользователя {user_id}: {e}")
    logging.error(f"DB error for user {user_id}: {e}", exc_info=True)
    
except Exception as e:
    print(f"Неожиданная ошибка при обновлении пользователя {user_id}: {e}")
    logging.exception(f"Unexpected error updating user {user_id}")
```

### 4. Принцип очистки ресурсов

```python
# ❌ Плохо - ресурсы могут не освободиться
def process_file(filename):
    file = open(filename)
    try:
        data = file.read()
        # Обработка данных
        return process_data(data)
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
    finally:
        file.close()  # Может не выполниться, если open() упал

# ✅ Хорошо - контекстные менеджеры
def process_file(filename):
    try:
        with open(filename) as file:
            data = file.read()
            return process_data(data)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except PermissionError:
        print(f"Нет прав для чтения файла {filename}")
        return None
    except Exception as e:
        print(f"Ошибка обработки файла {filename}: {e}")
        logging.exception(f"Error processing file {filename}")
        return None
```

### 5. Принцип логирования

```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def robust_function(data):
    """Функция с правильным логированием ошибок"""
    
    try:
        logger.info(f"Начало обработки данных: {len(data)} элементов")
        
        # Валидация
        if not isinstance(data, list):
            raise TypeError(f"Ожидается список, получен {type(data)}")
        
        if not data:
            logger.warning("Получен пустой список данных")
            return []
        
        # Обработка
        results = []
        for i, item in enumerate(data):
            try:
                result = process_item(item)
                results.append(result)
            except Exception as e:
                logger.error(f"Ошибка обработки элемента {i}: {e}")
                # Продолжаем обработку остальных элементов
                continue
        
        logger.info(f"Обработка завершена: {len(results)} из {len(data)} элементов")
        return results
        
    except TypeError as e:
        logger.error(f"Ошибка типа данных: {e}")
        raise
        
    except Exception as e:
        logger.exception("Неожиданная ошибка в robust_function")
        raise

def process_item(item):
    """Обработка одного элемента"""
    if not isinstance(item, dict):
        raise ValueError(f"Элемент должен быть словарем, получен {type(item)}")
    
    # Имитация обработки
    return {"processed": True, "original": item}
```

---

## 🔍 Отладка и логирование

### Получение трассировки стека

```python
import traceback
import sys

def detailed_error_info():
    """Получение подробной информации об ошибке"""
    
    try:
        # Код, который может вызвать ошибку
        risky_operation()
        
    except Exception as e:
        # Получение информации об исключении
        exc_type, exc_value, exc_traceback = sys.exc_info()
        
        print("=== Информация об ошибке ===")
        print(f"Тип исключения: {exc_type.__name__}")
        print(f"Сообщение: {exc_value}")
        print(f"Модуль: {exc_type.__module__}")
        
        print("\n=== Трассировка стека ===")
        traceback.print_exc()
        
        print("\n=== Подробная трассировка ===")
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for line in tb_lines:
            print(line.rstrip())
        
        print("\n=== Только последний вызов ===")
        filename, line_number, function_name, text = traceback.extract_tb(exc_traceback)[-1]
        print(f"Файл: {filename}")
        print(f"Строка: {line_number}")
        print(f"Функция: {function_name}")
        print(f"Код: {text}")

def risky_operation():
    """Функция, которая вызывает ошибку"""
    def inner_function():
        x = 1 / 0  # ZeroDivisionError
    
    inner_function()

# Запуск примера
detailed_error_info()
```

### Кастомный обработчик исключений

```python
import sys
import traceback
import logging
from datetime import datetime

class CustomExceptionHandler:
    """Кастомный обработчик исключений"""
    
    def __init__(self, log_file='errors.log'):
        self.log_file = log_file
        self.setup_logging()
        
        # Устанавливаем глобальный обработчик
        sys.excepthook = self.handle_exception
    
    def setup_logging(self):
        """Настройка логирования"""
        self.logger = logging.getLogger('exception_handler')
        self.logger.setLevel(logging.ERROR)
        
        # Обработчик для файла
        file_handler = logging.FileHandler(self.log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Обработка необработанных исключений"""
        
        if issubclass(exc_type, KeyboardInterrupt):
            # Не логируем KeyboardInterrupt
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        # Создаем подробный отчет об ошибке
        error_report = self.create_error_report(exc_type, exc_value, exc_traceback)
        
        # Логируем ошибку
        self.logger.error(error_report)
        
        # Выводим пользователю понятное сообщение
        print("❌ Произошла критическая ошибка!")
        print(f"Тип ошибки: {exc_type.__name__}")
        print(f"Описание: {exc_value}")
        print(f"Подробности сохранены в {self.log_file}")
        
        # Вызываем стандартный обработчик для разработки
        if __debug__:  # В режиме отладки показываем полную трассировку
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
    
    def create_error_report(self, exc_type, exc_value, exc_traceback):
        """Создание подробного отчета об ошибке"""
        
        timestamp = datetime.now().isoformat()
        
        report = [
            f"КРИТИЧЕСКАЯ ОШИБКА - {timestamp}",
            "=" * 50,
            f"Тип исключения: {exc_type.__name__}",
            f"Модуль: {exc_type.__module__}",
            f"Сообщение: {exc_value}",
            "",
            "Трассировка стека:",
        ]
        
        # Добавляем трассировку
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        report.extend(tb_lines)
        
        # Добавляем информацию о системе
        report.extend([
            "",
            "Системная информация:",
            f"Python версия: {sys.version}",
            f"Платформа: {sys.platform}",
            f"Путь к Python: {sys.executable}",
        ])
        
        return "\n".join(report)

# Установка кастомного обработчика
handler = CustomExceptionHandler()

# Тестирование
def test_error_handling():
    """Тестирование обработки ошибок"""
    
    # Различные типы ошибок
    test_cases = [
        lambda: 1 / 0,  # ZeroDivisionError
        lambda: [1, 2, 3][10],  # IndexError
        lambda: {"a": 1}["b"],  # KeyError
        lambda: int("не число"),  # ValueError
    ]
    
    for i, test_case in enumerate(test_cases):
        try:
            print(f"\nТест {i + 1}:")
            test_case()
        except Exception as e:
            print(f"Обработано исключение: {type(e).__name__}: {e}")

# Запуск тестов
test_error_handling()

# Пример необработанного исключения (будет обработано глобальным обработчиком)
# raise RuntimeError("Это тестовая критическая ошибка")
```

### Профилирование исключений

```python
import time
import functools
from collections import defaultdict, Counter

class ExceptionProfiler:
    """Профайлер для анализа исключений"""
    
    def __init__(self):
        self.exception_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'locations': Counter(),
            'messages': Counter()
        })
        self.enabled = True
    
    def profile_exceptions(self, func):
        """Декоратор для профилирования исключений"""
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self.enabled:
                return func(*args, **kwargs)
            
            start_time = time.time()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                
                # Записываем статистику
                exc_type = type(e).__name__
                location = f"{func.__module__}.{func.__name__}"
                message = str(e)
                
                stats = self.exception_stats[exc_type]
                stats['count'] += 1
                stats['total_time'] += duration
                stats['locations'][location] += 1
                stats['messages'][message] += 1
                
                # Перебрасываем исключение
                raise
        
        return wrapper
    
    def get_report(self):
        """Получение отчета по исключениям"""
        
        if not self.exception_stats:
            return "Исключения не зафиксированы"
        
        report = ["=== ОТЧЕТ ПО ИСКЛЮЧЕНИЯМ ===\n"]
        
        # Сортируем по количеству
        sorted_exceptions = sorted(
            self.exception_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        for exc_type, stats in sorted_exceptions:
            avg_time = stats['total_time'] / stats['count']
            
            report.append(f"🔥 {exc_type}:")
            report.append(f"   Количество: {stats['count']}")
            report.append(f"   Общее время: {stats['total_time']:.3f}s")
            report.append(f"   Среднее время: {avg_time:.3f}s")
            
            # Топ локаций
            report.append("   Топ локаций:")
            for location, count in stats['locations'].most_common(3):
                report.append(f"     {location}: {count}")
            
            # Топ сообщений
            report.append("   Топ сообщения:")
            for message, count in stats['messages'].most_common(3):
                short_msg = message[:50] + "..." if len(message) > 50 else message
                report.append(f"     '{short_msg}': {count}")
            
            report.append("")
        
        return "\n".join(report)
    
    def reset_stats(self):
        """Сброс статистики"""
        self.exception_stats.clear()

# Использование профайлера
profiler = ExceptionProfiler()

@profiler.profile_exceptions
def problematic_function(value):
    """Функция с различными исключениями"""
    
    if value == "zero":
        return 1 / 0
    elif value == "index":
        return [1, 2, 3][10]
    elif value == "key":
        return {"a": 1}["b"]
    elif value == "value":
        return int("не число")
    else:
        return f"Обработано: {value}"

@profiler.profile_exceptions
def another_function(data):
    """Другая проблемная функция"""
    
    if not data:
        raise ValueError("Данные не могут быть пустыми")
    
    if len(data) > 10:
        raise ValueError("Слишком много данных")
    
    return len(data)

# Тестирование с профилированием
test_values = ["zero", "index", "key", "value", "normal"] * 10
test_data = [[], "a" * 15, "normal", "test"] * 5

print("Запуск тестов с профилированием исключений...\n")

# Тестируем первую функцию
for value in test_values:
    try:
        result = problematic_function(value)
        print(f"✓ {value}: {result}")
    except Exception as e:
        print(f"✗ {value}: {type(e).__name__}")

# Тестируем вторую функцию
for data in test_data:
    try:
        result = another_function(data)
        print(f"✓ {repr(data)}: {result}")
    except Exception as e:
        print(f"✗ {repr(data)}: {type(e).__name__}")

# Выводим отчет
print("\n" + profiler.get_report())
```

---

## 📚 Заключение

Исключения в Python - это мощный инструмент для создания надежных приложений. Основные принципы эффективной работы с исключениями:

### Ключевые принципы:

1. **Специфичность** - ловите конкретные исключения, а не общий `Exception`
2. **Информативность** - предоставляйте подробную информацию об ошибках
3. **Очистка ресурсов** - используйте `finally` или контекстные менеджеры
4. **Логирование** - ведите подробные логи для отладки
5. **Восстановление** - предусматривайте механизмы восстановления после ошибок

### Практические советы:

- Используйте иерархию собственных исключений для больших приложений
- Применяйте декораторы для унификации обработки ошибок
- Профилируйте исключения в критических системах
- Тестируйте обработку ошибок так же тщательно, как и основную логику
- Документируйте возможные исключения в функциях

### Антипаттерны (чего избегать):

```python
# ❌ Пустой except
try:
    risky_operation()
except:
    pass

# ❌ Слишком общая обработка
try:
    complex_operation()
except Exception:
    print("Ошибка")

# ❌ Игнорирование контекста
try:
    process_file(filename)
except FileNotFoundError:
    print("Файл не найден")  # Какой файл?

# ❌ Подавление всех исключений
def safe_operation():
    try:
        return dangerous_operation()
    except:
        return None  # Теряем информацию об ошибке
```

Правильная обработка исключений - это искусство баланса между надежностью, производительностью и удобством использования. Изучите паттерны вашего приложения, тестируйте различные сценарии ошибок и всегда думайте о пользователе, который столкнется с этими ошибками. 