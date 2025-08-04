#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Исключения в Python

Этот файл содержит практические упражнения для закрепления знаний:
- Обработка различных типов исключений
- Создание пользовательских исключений
- Использование декораторов для обработки ошибок
- Работа с контекстными менеджерами
- Асинхронная обработка исключений

Каждое упражнение включает:
- Подробное описание задачи
- Примеры входных и выходных данных
- Решение с комментариями
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import functools
from contextlib import contextmanager


def exercise_01_exception_hierarchy():
    """
    Упражнение 1: Иерархия исключений для системы электронной коммерции
    
    Задача:
    Создайте полную иерархию пользовательских исключений для системы 
    электронной коммерции. Система должна включать:
    1. Базовое исключение ECommerceError
    2. Исключения для различных подсистем (User, Product, Order, Payment)
    3. Специфические исключения для каждой подсистемы
    4. Контекстную информацию в исключениях
    5. Методы для форматирования ошибок для пользователя и разработчика
    
    Требования:
    - Каждое исключение должно содержать код ошибки
    - Возможность добавления контекстной информации
    - Методы to_dict() и get_user_message()
    - Поддержка многоязычности (en/ru)
    """
    print("=== Упражнение 1: Иерархия исключений для e-commerce ===")
    
    # ЗАДАЧА: Реализуйте полную иерархию исключений
    
    # РЕШЕНИЕ:
    
    class ECommerceError(Exception):
        """Базовое исключение для системы электронной коммерции"""
        
        def __init__(self, message, error_code=None, context=None, severity="ERROR"):
            super().__init__(message)
            self.error_code = error_code
            self.context = context or {}
            self.severity = severity
            self.timestamp = datetime.now()
            
            # Сообщения для пользователей (многоязычность)
            self.user_messages = {
                'en': "An error occurred. Please try again later.",
                'ru': "Произошла ошибка. Пожалуйста, попробуйте позже."
            }
        
        def add_context(self, key, value):
            """Добавить контекстную информацию"""
            self.context[key] = value
        
        def to_dict(self):
            """Преобразование в словарь для JSON API"""
            return {
                "error_type": self.__class__.__name__,
                "error_code": self.error_code,
                "message": str(self),
                "severity": self.severity,
                "context": self.context,
                "timestamp": self.timestamp.isoformat()
            }
        
        def get_user_message(self, language='ru'):
            """Получить сообщение для пользователя"""
            return self.user_messages.get(language, self.user_messages['en'])
        
        def log_error(self, logger):
            """Логирование ошибки"""
            log_level = {
                'DEBUG': logger.debug,
                'INFO': logger.info,
                'WARNING': logger.warning,
                'ERROR': logger.error,
                'CRITICAL': logger.critical
            }.get(self.severity, logger.error)
            
            log_level(f"{self.error_code}: {self} | Context: {self.context}")
    
    # === ПОЛЬЗОВАТЕЛЬСКИЕ ИСКЛЮЧЕНИЯ ===
    
    class UserError(ECommerceError):
        """Базовое исключение для пользователей"""
        pass
    
    class UserNotFoundError(UserError):
        """Пользователь не найден"""
        
        def __init__(self, user_id=None, email=None):
            message = f"User not found"
            if user_id:
                message += f" (ID: {user_id})"
            if email:
                message += f" (Email: {email})"
            
            super().__init__(message, "USER_NOT_FOUND")
            self.user_messages = {
                'en': "User account not found.",
                'ru': "Учетная запись пользователя не найдена."
            }
            
            if user_id:
                self.add_context("user_id", user_id)
            if email:
                self.add_context("email", email)
    
    class UserValidationError(UserError):
        """Ошибка валидации пользователя"""
        
        def __init__(self, field, value, reason):
            super().__init__(f"Invalid {field}: {reason}", "USER_VALIDATION_ERROR")
            self.field = field
            self.value = value
            self.reason = reason
            
            self.user_messages = {
                'en': f"Invalid {field}: {reason}",
                'ru': f"Неверное значение {field}: {reason}"
            }
            
            self.add_context("field", field)
            self.add_context("value", value)
            self.add_context("reason", reason)
    
    class UserAuthenticationError(UserError):
        """Ошибка аутентификации"""
        
        def __init__(self, email=None, reason="Invalid credentials"):
            super().__init__(f"Authentication failed: {reason}", "AUTH_FAILED")
            
            self.user_messages = {
                'en': "Invalid email or password.",
                'ru': "Неверный email или пароль."
            }
            
            if email:
                self.add_context("email", email)
    
    # === ТОВАРНЫЕ ИСКЛЮЧЕНИЯ ===
    
    class ProductError(ECommerceError):
        """Базовое исключение для товаров"""
        pass
    
    class ProductNotFoundError(ProductError):
        """Товар не найден"""
        
        def __init__(self, product_id=None, sku=None):
            message = "Product not found"
            if product_id:
                message += f" (ID: {product_id})"
            if sku:
                message += f" (SKU: {sku})"
            
            super().__init__(message, "PRODUCT_NOT_FOUND")
            
            self.user_messages = {
                'en': "Product not found or no longer available.",
                'ru': "Товар не найден или более недоступен."
            }
    
    class InsufficientStockError(ProductError):
        """Недостаточно товара на складе"""
        
        def __init__(self, product_id, requested, available):
            super().__init__(
                f"Insufficient stock for product {product_id}: "
                f"requested {requested}, available {available}",
                "INSUFFICIENT_STOCK"
            )
            
            self.user_messages = {
                'en': f"Only {available} items available in stock.",
                'ru': f"В наличии только {available} товаров."
            }
            
            self.add_context("product_id", product_id)
            self.add_context("requested", requested)
            self.add_context("available", available)
    
    # === ЗАКАЗНЫЕ ИСКЛЮЧЕНИЯ ===
    
    class OrderError(ECommerceError):
        """Базовое исключение для заказов"""
        pass
    
    class OrderValidationError(OrderError):
        """Ошибка валидации заказа"""
        
        def __init__(self, order_id, issues):
            super().__init__(f"Order validation failed: {', '.join(issues)}", "ORDER_VALIDATION_ERROR")
            
            self.user_messages = {
                'en': "Order contains invalid items or information.",
                'ru': "Заказ содержит неверные товары или информацию."
            }
            
            self.add_context("order_id", order_id)
            self.add_context("issues", issues)
    
    class OrderStatusError(OrderError):
        """Неверный статус заказа для операции"""
        
        def __init__(self, order_id, current_status, required_status):
            super().__init__(
                f"Cannot perform operation on order {order_id}: "
                f"status is {current_status}, required {required_status}",
                "ORDER_STATUS_ERROR"
            )
            
            self.user_messages = {
                'en': "Cannot modify order in current state.",
                'ru': "Невозможно изменить заказ в текущем состоянии."
            }
    
    # === ПЛАТЕЖНЫЕ ИСКЛЮЧЕНИЯ ===
    
    class PaymentError(ECommerceError):
        """Базовое исключение для платежей"""
        pass
    
    class PaymentDeclinedError(PaymentError):
        """Платеж отклонен"""
        
        def __init__(self, transaction_id, reason):
            super().__init__(f"Payment declined: {reason}", "PAYMENT_DECLINED")
            
            self.user_messages = {
                'en': "Payment was declined. Please check your payment method.",
                'ru': "Платеж отклонен. Проверьте способ оплаты."
            }
            
            self.add_context("transaction_id", transaction_id)
            self.add_context("reason", reason)
    
    class PaymentGatewayError(PaymentError):
        """Ошибка платежного шлюза"""
        
        def __init__(self, gateway, error_code, message):
            super().__init__(f"Payment gateway error: {message}", "PAYMENT_GATEWAY_ERROR")
            
            self.user_messages = {
                'en': "Payment service is temporarily unavailable.",
                'ru': "Сервис платежей временно недоступен."
            }
            
            self.add_context("gateway", gateway)
            self.add_context("gateway_error_code", error_code)
    
    # === ПРИМЕР ИСПОЛЬЗОВАНИЯ ===
    
    class ECommerceService:
        """Сервис электронной коммерции с обработкой исключений"""
        
        def __init__(self):
            self.users = {}
            self.products = {}
            self.orders = {}
            self.logger = logging.getLogger(__name__)
        
        def create_user(self, email, password, name):
            """Создание пользователя"""
            try:
                # Валидация email
                if '@' not in email:
                    raise UserValidationError("email", email, "Invalid format")
                
                # Проверка уникальности
                if email in self.users:
                    raise UserValidationError("email", email, "Already exists")
                
                # Валидация пароля
                if len(password) < 8:
                    raise UserValidationError("password", "***", "Too short (min 8 chars)")
                
                user_id = len(self.users) + 1
                self.users[email] = {
                    "id": user_id,
                    "email": email,
                    "name": name,
                    "password": password  # В реальности - хеш
                }
                
                return {"user_id": user_id, "status": "created"}
                
            except ECommerceError as e:
                e.log_error(self.logger)
                return {"error": e.to_dict(), "user_message": e.get_user_message()}
        
        def add_product(self, name, price, stock):
            """Добавление товара"""
            product_id = len(self.products) + 1
            self.products[product_id] = {
                "id": product_id,
                "name": name,
                "price": price,
                "stock": stock
            }
            return product_id
        
        def place_order(self, user_email, items):
            """Размещение заказа"""
            try:
                # Проверка пользователя
                if user_email not in self.users:
                    raise UserNotFoundError(email=user_email)
                
                # Валидация товаров
                issues = []
                for item in items:
                    product_id = item['product_id']
                    quantity = item['quantity']
                    
                    if product_id not in self.products:
                        raise ProductNotFoundError(product_id=product_id)
                    
                    product = self.products[product_id]
                    if product['stock'] < quantity:
                        raise InsufficientStockError(
                            product_id, quantity, product['stock']
                        )
                
                # Создание заказа
                order_id = len(self.orders) + 1
                self.orders[order_id] = {
                    "id": order_id,
                    "user_email": user_email,
                    "items": items,
                    "status": "pending",
                    "created_at": datetime.now()
                }
                
                # Обновление остатков
                for item in items:
                    self.products[item['product_id']]['stock'] -= item['quantity']
                
                return {"order_id": order_id, "status": "created"}
                
            except ECommerceError as e:
                e.log_error(self.logger)
                return {"error": e.to_dict(), "user_message": e.get_user_message()}
        
        def process_payment(self, order_id, payment_method):
            """Обработка платежа"""
            try:
                if order_id not in self.orders:
                    raise OrderError(f"Order {order_id} not found", "ORDER_NOT_FOUND")
                
                order = self.orders[order_id]
                if order['status'] != 'pending':
                    raise OrderStatusError(order_id, order['status'], 'pending')
                
                # Имитация обработки платежа
                import random
                if random.random() < 0.2:  # 20% вероятность отклонения
                    raise PaymentDeclinedError(f"txn_{order_id}", "Insufficient funds")
                
                if random.random() < 0.1:  # 10% вероятность ошибки шлюза
                    raise PaymentGatewayError("stripe", "500", "Internal server error")
                
                # Успешный платеж
                order['status'] = 'paid'
                return {"transaction_id": f"txn_{order_id}", "status": "success"}
                
            except ECommerceError as e:
                e.log_error(self.logger)
                return {"error": e.to_dict(), "user_message": e.get_user_message()}
    
    # === ТЕСТИРОВАНИЕ ===
    
    # Настройка логирования
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    service = ECommerceService()
    
    # Добавляем тестовые товары
    product1 = service.add_product("Laptop", 1000.0, 5)
    product2 = service.add_product("Mouse", 50.0, 10)
    
    print("Тестирование системы исключений:")
    
    # Тест 1: Создание пользователей
    print("\n1. Создание пользователей:")
    test_users = [
        ("valid@example.com", "password123", "Valid User"),  # Успешно
        ("invalid-email", "password123", "Invalid User"),   # Неверный email
        ("valid@example.com", "password123", "Duplicate"),  # Дубликат
        ("short@example.com", "123", "Short Password"),     # Короткий пароль
    ]
    
    for email, password, name in test_users:
        print(f"Создание пользователя {email}:")
        result = service.create_user(email, password, name)
        if "error" in result:
            print(f"  ❌ {result['error']['error_code']}: {result['user_message']}")
        else:
            print(f"  ✅ Создан пользователь ID: {result['user_id']}")
    
    # Тест 2: Размещение заказов
    print("\n2. Размещение заказов:")
    test_orders = [
        ("valid@example.com", [{"product_id": product1, "quantity": 2}]),  # Успешно
        ("nonexistent@example.com", [{"product_id": product1, "quantity": 1}]),  # Пользователь не найден
        ("valid@example.com", [{"product_id": 999, "quantity": 1}]),  # Товар не найден
        ("valid@example.com", [{"product_id": product1, "quantity": 10}]),  # Недостаточно товара
    ]
    
    for email, items in test_orders:
        print(f"Заказ от {email}:")
        result = service.place_order(email, items)
        if "error" in result:
            print(f"  ❌ {result['error']['error_code']}: {result['user_message']}")
        else:
            print(f"  ✅ Создан заказ ID: {result['order_id']}")
    
    # Тест 3: Обработка платежей
    print("\n3. Обработка платежей:")
    for order_id in range(1, 3):  # Тестируем первые 2 заказа
        if order_id in service.orders:
            print(f"Платеж для заказа {order_id}:")
            result = service.process_payment(order_id, "credit_card")
            if "error" in result:
                print(f"  ❌ {result['error']['error_code']}: {result['user_message']}")
            else:
                print(f"  ✅ Платеж успешен: {result['transaction_id']}")
    
    print("\n✅ Упражнение 1 завершено!")


def exercise_02_decorator_error_handling():
    """
    Упражнение 2: Система декораторов для обработки ошибок
    
    Задача:
    Создайте комплексную систему декораторов для обработки ошибок:
    1. @retry - повтор с различными стратегиями backoff
    2. @circuit_breaker - автоматическое отключение при частых ошибках
    3. @timeout - ограничение времени выполнения
    4. @validate - валидация входных параметров
    5. @audit_log - логирование всех вызовов и ошибок
    6. @fallback - резервный метод при ошибке
    
    Декораторы должны работать вместе и быть настраиваемыми.
    """
    print("=== Упражнение 2: Система декораторов для обработки ошибок ===")
    
    # ЗАДАЧА: Реализуйте систему декораторов
    
    # РЕШЕНИЕ:
    
    import threading
    import signal
    from collections import defaultdict
    from enum import Enum
    
    class BackoffStrategy(Enum):
        """Стратегии backoff для retry"""
        LINEAR = "linear"
        EXPONENTIAL = "exponential"
        FIXED = "fixed"
        RANDOM = "random"
    
    class CircuitState(Enum):
        """Состояния Circuit Breaker"""
        CLOSED = "closed"      # Нормальная работа
        OPEN = "open"          # Отключен из-за ошибок
        HALF_OPEN = "half_open"  # Тестирование восстановления
    
    def retry(max_attempts=3, delay=1, backoff=BackoffStrategy.EXPONENTIAL, 
              exceptions=(Exception,), backoff_multiplier=2):
        """
        Декоратор retry с различными стратегиями backoff
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                current_delay = delay
                
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        
                        if attempt == max_attempts - 1:
                            break
                        
                        # Вычисляем задержку
                        if backoff == BackoffStrategy.LINEAR:
                            wait_time = delay * (attempt + 1)
                        elif backoff == BackoffStrategy.EXPONENTIAL:
                            wait_time = delay * (backoff_multiplier ** attempt)
                        elif backoff == BackoffStrategy.FIXED:
                            wait_time = delay
                        elif backoff == BackoffStrategy.RANDOM:
                            import random
                            wait_time = delay * random.uniform(0.5, 1.5)
                        else:
                            wait_time = delay
                        
                        print(f"Retry {attempt + 1}/{max_attempts} for {func.__name__} "
                              f"after {wait_time:.2f}s: {e}")
                        time.sleep(wait_time)
                
                raise last_exception
            
            return wrapper
        return decorator
    
    class CircuitBreaker:
        """Circuit Breaker для автоматического отключения проблемных сервисов"""
        
        def __init__(self, failure_threshold=5, recovery_timeout=60, expected_exception=Exception):
            self.failure_threshold = failure_threshold
            self.recovery_timeout = recovery_timeout
            self.expected_exception = expected_exception
            
            self.failure_count = 0
            self.last_failure_time = None
            self.state = CircuitState.CLOSED
            self.lock = threading.Lock()
        
        def __call__(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self.lock:
                    if self.state == CircuitState.OPEN:
                        if time.time() - self.last_failure_time > self.recovery_timeout:
                            self.state = CircuitState.HALF_OPEN
                            print(f"Circuit breaker HALF_OPEN for {func.__name__}")
                        else:
                            raise RuntimeError(f"Circuit breaker OPEN for {func.__name__}")
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Успешное выполнение
                    with self.lock:
                        if self.state == CircuitState.HALF_OPEN:
                            self.state = CircuitState.CLOSED
                            self.failure_count = 0
                            print(f"Circuit breaker CLOSED for {func.__name__}")
                    
                    return result
                    
                except self.expected_exception as e:
                    with self.lock:
                        self.failure_count += 1
                        self.last_failure_time = time.time()
                        
                        if self.failure_count >= self.failure_threshold:
                            self.state = CircuitState.OPEN
                            print(f"Circuit breaker OPEN for {func.__name__} "
                                  f"({self.failure_count} failures)")
                    
                    raise
            
            return wrapper
    
    def timeout(seconds):
        """Декоратор для ограничения времени выполнения"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Обработчик таймаута
                def timeout_handler(signum, frame):
                    raise TimeoutError(f"Function {func.__name__} timed out after {seconds}s")
                
                # Устанавливаем таймер
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(seconds)
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    # Отменяем таймер
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)
            
            return wrapper
        return decorator
    
    def validate(**validators):
        """Декоратор для валидации параметров"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                import inspect
                
                # Получаем параметры функции
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                
                # Валидируем каждый параметр
                for param_name, validator in validators.items():
                    if param_name in bound_args.arguments:
                        value = bound_args.arguments[param_name]
                        
                        if callable(validator):
                            if not validator(value):
                                raise ValueError(f"Validation failed for {param_name}: {value}")
                        elif isinstance(validator, type):
                            if not isinstance(value, validator):
                                raise TypeError(f"{param_name} must be {validator.__name__}")
                        elif isinstance(validator, dict):
                            # Комплексная валидация
                            for check_name, check_func in validator.items():
                                if not check_func(value):
                                    raise ValueError(f"{param_name} failed {check_name} check")
                
                return func(*args, **kwargs)
            
            return wrapper
        return decorator
    
    class AuditLogger:
        """Система аудита для логирования вызовов функций"""
        
        def __init__(self, logger_name="audit"):
            self.logger = logging.getLogger(logger_name)
            self.call_stats = defaultdict(lambda: {
                'total_calls': 0,
                'successful_calls': 0,
                'failed_calls': 0,
                'total_time': 0,
                'errors': defaultdict(int)
            })
        
        def __call__(self, include_args=True, include_result=False):
            def decorator(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    call_id = f"{func.__module__}.{func.__name__}"
                    start_time = time.time()
                    
                    # Логируем начало вызова
                    log_data = {
                        'function': call_id,
                        'timestamp': datetime.now().isoformat(),
                        'call_id': f"{call_id}_{int(start_time)}"
                    }
                    
                    if include_args:
                        log_data['args'] = str(args)[:100]  # Ограничиваем длину
                        log_data['kwargs'] = str(kwargs)[:100]
                    
                    try:
                        result = func(*args, **kwargs)
                        end_time = time.time()
                        duration = end_time - start_time
                        
                        # Успешное выполнение
                        self.call_stats[call_id]['total_calls'] += 1
                        self.call_stats[call_id]['successful_calls'] += 1
                        self.call_stats[call_id]['total_time'] += duration
                        
                        log_data.update({
                            'status': 'SUCCESS',
                            'duration': duration
                        })
                        
                        if include_result:
                            log_data['result'] = str(result)[:100]
                        
                        self.logger.info(f"AUDIT: {json.dumps(log_data)}")
                        return result
                        
                    except Exception as e:
                        end_time = time.time()
                        duration = end_time - start_time
                        
                        # Ошибка
                        self.call_stats[call_id]['total_calls'] += 1
                        self.call_stats[call_id]['failed_calls'] += 1
                        self.call_stats[call_id]['total_time'] += duration
                        self.call_stats[call_id]['errors'][type(e).__name__] += 1
                        
                        log_data.update({
                            'status': 'ERROR',
                            'duration': duration,
                            'error_type': type(e).__name__,
                            'error_message': str(e)
                        })
                        
                        self.logger.error(f"AUDIT: {json.dumps(log_data)}")
                        raise
                
                return wrapper
            return decorator
        
        def get_stats(self):
            """Получить статистику вызовов"""
            return dict(self.call_stats)
    
    def fallback(fallback_func, exceptions=(Exception,)):
        """Декоратор для использования резервного метода при ошибке"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Primary function {func.__name__} failed: {e}")
                    print(f"Using fallback function: {fallback_func.__name__}")
                    return fallback_func(*args, **kwargs)
            
            return wrapper
        return decorator
    
    # === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===
    
    # Настройка логирования
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    
    # Создаем экземпляр аудитора
    auditor = AuditLogger()
    
    # Создаем circuit breaker
    api_circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
    
    # Резервные функции
    def fallback_api_call(*args, **kwargs):
        """Резервный API вызов"""
        return {"status": "fallback", "data": "cached_data"}
    
    def fallback_database_query(*args, **kwargs):
        """Резервный запрос к БД"""
        return []
    
    # === ДЕКОРИРОВАННЫЕ ФУНКЦИИ ===
    
    @auditor(include_args=True, include_result=True)
    @fallback(fallback_api_call, exceptions=(ConnectionError, TimeoutError))
    @retry(max_attempts=3, delay=1, backoff=BackoffStrategy.EXPONENTIAL)
    @api_circuit_breaker
    @validate(url=str, timeout={'positive': lambda x: x > 0})
    def external_api_call(url, timeout=30):
        """Вызов внешнего API с полной защитой"""
        import random
        
        # Имитация различных ошибок
        rand = random.random()
        if rand < 0.3:
            raise ConnectionError("Network connection failed")
        elif rand < 0.5:
            raise TimeoutError("Request timed out")
        elif rand < 0.7:
            raise ValueError("Invalid response format")
        
        return {"status": "success", "data": f"Response from {url}"}
    
    @auditor(include_args=False)
    @fallback(fallback_database_query)
    @retry(max_attempts=2, backoff=BackoffStrategy.LINEAR)
    @validate(query=str, limit={'range': lambda x: 1 <= x <= 1000})
    def database_query(query, limit=100):
        """Запрос к базе данных"""
        import random
        
        if random.random() < 0.4:
            raise ConnectionError("Database connection lost")
        
        return [f"Record {i}" for i in range(min(limit, 5))]
    
    @auditor()
    @validate(
        amount={'positive': lambda x: x > 0, 'max': lambda x: x <= 10000},
        currency=str
    )
    def process_payment(amount, currency="USD"):
        """Обработка платежа"""
        import random
        
        if random.random() < 0.2:
            raise ValueError("Invalid payment method")
        
        return {"transaction_id": f"txn_{int(time.time())}", "amount": amount}
    
    # === ТЕСТИРОВАНИЕ ===
    
    print("Тестирование системы декораторов:")
    
    # Тест 1: API вызовы с различными ошибками
    print("\n1. Тестирование API вызовов:")
    for i in range(8):
        try:
            result = external_api_call("https://api.example.com/data", timeout=5)
            print(f"  ✅ Вызов {i+1}: {result['status']}")
        except Exception as e:
            print(f"  ❌ Вызов {i+1}: {type(e).__name__}: {e}")
        
        time.sleep(0.5)  # Небольшая пауза
    
    # Тест 2: Запросы к БД
    print("\n2. Тестирование запросов к БД:")
    for i in range(5):
        try:
            result = database_query("SELECT * FROM users", limit=10)
            print(f"  ✅ Запрос {i+1}: {len(result)} записей")
        except Exception as e:
            print(f"  ❌ Запрос {i+1}: {type(e).__name__}: {e}")
    
    # Тест 3: Валидация параметров
    print("\n3. Тестирование валидации:")
    test_payments = [
        (100, "USD"),      # Успешно
        (-50, "USD"),      # Отрицательная сумма
        (15000, "EUR"),    # Слишком большая сумма
        (100, 123),        # Неверный тип валюты
    ]
    
    for amount, currency in test_payments:
        try:
            result = process_payment(amount, currency)
            print(f"  ✅ Платеж {amount} {currency}: {result['transaction_id']}")
        except Exception as e:
            print(f"  ❌ Платеж {amount} {currency}: {type(e).__name__}: {e}")
    
    # Тест 4: Статистика аудита
    print("\n4. Статистика вызовов функций:")
    stats = auditor.get_stats()
    for func_name, stat in stats.items():
        success_rate = (stat['successful_calls'] / stat['total_calls'] * 100) if stat['total_calls'] > 0 else 0
        avg_time = stat['total_time'] / stat['total_calls'] if stat['total_calls'] > 0 else 0
        
        print(f"  {func_name}:")
        print(f"    Всего вызовов: {stat['total_calls']}")
        print(f"    Успешных: {stat['successful_calls']} ({success_rate:.1f}%)")
        print(f"    Ошибок: {stat['failed_calls']}")
        print(f"    Среднее время: {avg_time:.3f}s")
        if stat['errors']:
            print(f"    Типы ошибок: {dict(stat['errors'])}")
    
    print("\n✅ Упражнение 2 завершено!")


def exercise_03_async_exception_handling():
    """
    Упражнение 3: Асинхронная обработка исключений
    
    Задача:
    Создайте систему для асинхронной обработки задач с обработкой исключений:
    1. Асинхронный retry с backoff
    2. Ограничение количества параллельных задач (semaphore)
    3. Timeout для асинхронных операций
    4. Graceful shutdown при критических ошибках
    5. Мониторинг состояния задач
    6. Восстановление после сбоев
    """
    print("=== Упражнение 3: Асинхронная обработка исключений ===")
    
    # ЗАДАЧА: Реализуйте асинхронную систему обработки задач
    
    # РЕШЕНИЕ:
    
    from asyncio import Semaphore, Event, Queue
    from enum import Enum
    import uuid
    
    class TaskStatus(Enum):
        """Статусы задач"""
        PENDING = "pending"
        RUNNING = "running"
        COMPLETED = "completed"
        FAILED = "failed"
        CANCELLED = "cancelled"
        RETRYING = "retrying"
    
    class AsyncTaskManager:
        """Менеджер асинхронных задач с обработкой исключений"""
        
        def __init__(self, max_concurrent_tasks=5, default_timeout=30):
            self.max_concurrent_tasks = max_concurrent_tasks
            self.default_timeout = default_timeout
            self.semaphore = Semaphore(max_concurrent_tasks)
            self.shutdown_event = Event()
            self.task_queue = Queue()
            self.active_tasks = {}
            self.task_stats = {
                'total': 0,
                'completed': 0,
                'failed': 0,
                'cancelled': 0
            }
            self.logger = logging.getLogger(self.__class__.__name__)
        
        async def async_retry(self, coro_func, *args, max_attempts=3, 
                            base_delay=1, backoff_multiplier=2, 
                            exceptions=(Exception,), **kwargs):
            """Асинхронный retry с exponential backoff"""
            
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await coro_func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        break
                    
                    delay = base_delay * (backoff_multiplier ** attempt)
                    self.logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for "
                        f"{coro_func.__name__}: {e}. Retrying in {delay}s"
                    )
                    
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        async def execute_with_timeout(self, coro, timeout=None):
            """Выполнение корутины с таймаутом"""
            timeout = timeout or self.default_timeout
            
            try:
                return await asyncio.wait_for(coro, timeout=timeout)
            except asyncio.TimeoutError:
                raise TimeoutError(f"Task timed out after {timeout}s")
        
        async def submit_task(self, task_func, *args, task_id=None, 
                            timeout=None, max_retries=3, **kwargs):
            """Отправка задачи на выполнение"""
            
            if task_id is None:
                task_id = str(uuid.uuid4())
            
            task_info = {
                'id': task_id,
                'func': task_func,
                'args': args,
                'kwargs': kwargs,
                'timeout': timeout,
                'max_retries': max_retries,
                'status': TaskStatus.PENDING,
                'created_at': datetime.now(),
                'attempts': 0,
                'result': None,
                'error': None
            }
            
            self.active_tasks[task_id] = task_info
            await self.task_queue.put(task_info)
            self.task_stats['total'] += 1
            
            return task_id
        
        async def process_task(self, task_info):
            """Обработка одной задачи"""
            task_id = task_info['id']
            
            try:
                async with self.semaphore:  # Ограничиваем параллельность
                    if self.shutdown_event.is_set():
                        task_info['status'] = TaskStatus.CANCELLED
                        self.task_stats['cancelled'] += 1
                        return
                    
                    task_info['status'] = TaskStatus.RUNNING
                    task_info['started_at'] = datetime.now()
                    
                    self.logger.info(f"Starting task {task_id}")
                    
                    # Выполняем задачу с retry и timeout
                    result = await self.async_retry(
                        lambda: self.execute_with_timeout(
                            task_info['func'](*task_info['args'], **task_info['kwargs']),
                            task_info['timeout']
                        ),
                        max_attempts=task_info['max_retries'],
                        exceptions=(ConnectionError, TimeoutError, ValueError)
                    )
                    
                    task_info['result'] = result
                    task_info['status'] = TaskStatus.COMPLETED
                    task_info['completed_at'] = datetime.now()
                    self.task_stats['completed'] += 1
                    
                    self.logger.info(f"Task {task_id} completed successfully")
                    
            except Exception as e:
                task_info['error'] = str(e)
                task_info['status'] = TaskStatus.FAILED
                task_info['failed_at'] = datetime.now()
                self.task_stats['failed'] += 1
                
                self.logger.error(f"Task {task_id} failed: {e}")
                
                # Критические ошибки могут вызвать shutdown
                if isinstance(e, (MemoryError, SystemError)):
                    self.logger.critical(f"Critical error in task {task_id}: {e}")
                    await self.graceful_shutdown()
        
        async def worker(self, worker_id):
            """Рабочий процесс для обработки задач"""
            self.logger.info(f"Worker {worker_id} started")
            
            try:
                while not self.shutdown_event.is_set():
                    try:
                        # Ждем задачу с таймаутом
                        task_info = await asyncio.wait_for(
                            self.task_queue.get(), 
                            timeout=1.0
                        )
                        
                        await self.process_task(task_info)
                        self.task_queue.task_done()
                        
                    except asyncio.TimeoutError:
                        # Таймаут ожидания задачи - продолжаем
                        continue
                    except Exception as e:
                        self.logger.error(f"Worker {worker_id} error: {e}")
                        
            except asyncio.CancelledError:
                self.logger.info(f"Worker {worker_id} cancelled")
            finally:
                self.logger.info(f"Worker {worker_id} stopped")
        
        async def start_workers(self, num_workers=3):
            """Запуск рабочих процессов"""
            workers = []
            for i in range(num_workers):
                worker = asyncio.create_task(self.worker(f"worker-{i}"))
                workers.append(worker)
            
            return workers
        
        async def graceful_shutdown(self, timeout=10):
            """Graceful shutdown системы"""
            self.logger.info("Initiating graceful shutdown...")
            
            # Устанавливаем флаг shutdown
            self.shutdown_event.set()
            
            # Ждем завершения активных задач
            try:
                await asyncio.wait_for(self.task_queue.join(), timeout=timeout)
                self.logger.info("All tasks completed")
            except asyncio.TimeoutError:
                self.logger.warning(f"Shutdown timeout ({timeout}s) reached")
                
                # Отменяем оставшиеся задачи
                for task_id, task_info in self.active_tasks.items():
                    if task_info['status'] in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                        task_info['status'] = TaskStatus.CANCELLED
                        self.task_stats['cancelled'] += 1
        
        def get_task_status(self, task_id):
            """Получить статус задачи"""
            return self.active_tasks.get(task_id)
        
        def get_stats(self):
            """Получить статистику"""
            active_count = sum(
                1 for task in self.active_tasks.values()
                if task['status'] in [TaskStatus.PENDING, TaskStatus.RUNNING]
            )
            
            return {
                **self.task_stats,
                'active': active_count,
                'queue_size': self.task_queue.qsize()
            }
    
    # === ПРИМЕРЫ ЗАДАЧ ===
    
    async def simulate_api_call(api_name, delay=2, failure_rate=0.3):
        """Имитация API вызова"""
        await asyncio.sleep(delay)
        
        import random
        if random.random() < failure_rate:
            if random.random() < 0.5:
                raise ConnectionError(f"Failed to connect to {api_name}")
            else:
                raise TimeoutError(f"Timeout calling {api_name}")
        
        return {"api": api_name, "data": f"Response from {api_name}", "timestamp": datetime.now().isoformat()}
    
    async def simulate_database_operation(operation, delay=1, failure_rate=0.2):
        """Имитация операции с БД"""
        await asyncio.sleep(delay)
        
        import random
        if random.random() < failure_rate:
            raise ValueError(f"Database operation '{operation}' failed")
        
        return {"operation": operation, "rows_affected": random.randint(1, 100)}
    
    async def simulate_file_processing(filename, delay=3, failure_rate=0.1):
        """Имитация обработки файла"""
        await asyncio.sleep(delay)
        
        import random
        if random.random() < failure_rate:
            raise RuntimeError(f"Failed to process file {filename}")
        
        return {"filename": filename, "size": random.randint(1000, 10000), "processed": True}
    
    # === МОНИТОРИНГ ===
    
    async def monitor_system(task_manager, interval=5):
        """Мониторинг состояния системы"""
        while not task_manager.shutdown_event.is_set():
            stats = task_manager.get_stats()
            
            success_rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            
            print(f"\n📊 Статистика системы:")
            print(f"  Всего задач: {stats['total']}")
            print(f"  Активных: {stats['active']}")
            print(f"  В очереди: {stats['queue_size']}")
            print(f"  Завершено: {stats['completed']}")
            print(f"  Ошибок: {stats['failed']}")
            print(f"  Отменено: {stats['cancelled']}")
            print(f"  Успешность: {success_rate:.1f}%")
            
            await asyncio.sleep(interval)
    
    # === ГЛАВНАЯ ФУНКЦИЯ ТЕСТИРОВАНИЯ ===
    
    async def run_async_task_system():
        """Запуск и тестирование асинхронной системы"""
        
        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Создаем менеджер задач
        task_manager = AsyncTaskManager(max_concurrent_tasks=3, default_timeout=10)
        
        # Запускаем рабочие процессы
        workers = await task_manager.start_workers(num_workers=2)
        
        # Запускаем мониторинг
        monitor_task = asyncio.create_task(monitor_system(task_manager, interval=3))
        
        try:
            print("🚀 Запуск асинхронной системы обработки задач")
            
            # Отправляем различные типы задач
            task_ids = []
            
            # API вызовы
            for i in range(5):
                task_id = await task_manager.submit_task(
                    simulate_api_call, 
                    f"api-service-{i}", 
                    delay=2, 
                    failure_rate=0.4
                )
                task_ids.append(task_id)
            
            # Операции с БД
            for i in range(3):
                task_id = await task_manager.submit_task(
                    simulate_database_operation,
                    f"operation-{i}",
                    delay=1,
                    failure_rate=0.3
                )
                task_ids.append(task_id)
            
            # Обработка файлов
            for i in range(4):
                task_id = await task_manager.submit_task(
                    simulate_file_processing,
                    f"file-{i}.txt",
                    delay=3,
                    failure_rate=0.2,
                    max_retries=2
                )
                task_ids.append(task_id)
            
            print(f"Отправлено {len(task_ids)} задач")
            
            # Ждем некоторое время для обработки
            await asyncio.sleep(15)
            
            # Показываем статус задач
            print("\n📋 Статус задач:")
            for task_id in task_ids:
                task_info = task_manager.get_task_status(task_id)
                if task_info:
                    status = task_info['status'].value
                    func_name = task_info['func'].__name__
                    
                    if task_info['status'] == TaskStatus.COMPLETED:
                        print(f"  ✅ {task_id[:8]} ({func_name}): {status}")
                    elif task_info['status'] == TaskStatus.FAILED:
                        print(f"  ❌ {task_id[:8]} ({func_name}): {status} - {task_info['error']}")
                    else:
                        print(f"  🔄 {task_id[:8]} ({func_name}): {status}")
            
            # Graceful shutdown
            print("\n🛑 Инициация graceful shutdown...")
            await task_manager.graceful_shutdown(timeout=5)
            
        except KeyboardInterrupt:
            print("\n⚠️ Получен сигнал прерывания")
            await task_manager.graceful_shutdown()
        
        finally:
            # Отменяем мониторинг и рабочие процессы
            monitor_task.cancel()
            for worker in workers:
                worker.cancel()
            
            # Ждем их завершения
            await asyncio.gather(*workers, monitor_task, return_exceptions=True)
            
            # Финальная статистика
            final_stats = task_manager.get_stats()
            print(f"\n📈 Финальная статистика: {final_stats}")
    
    # Запуск асинхронной системы
    try:
        asyncio.run(run_async_task_system())
    except Exception as e:
        print(f"Критическая ошибка системы: {e}")
    
    print("\n✅ Упражнение 3 завершено!")


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Иерархия исключений для e-commerce", exercise_01_exception_hierarchy),
        ("Система декораторов для обработки ошибок", exercise_02_decorator_error_handling),
        ("Асинхронная обработка исключений", exercise_03_async_exception_handling),
    ]
    
    print("🔥 Упражнения: Исключения в Python")
    print("=" * 50)
    print("Эти упражнения помогут вам освоить:")
    print("- Создание иерархий пользовательских исключений")
    print("- Разработку декораторов для обработки ошибок")
    print("- Асинхронную обработку исключений")
    print("- Мониторинг и восстановление после сбоев")
    print("=" * 50)
    
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
            input("\nНажмите Enter для продолжения к следующему упражнению...")


if __name__ == "__main__":
    main() 