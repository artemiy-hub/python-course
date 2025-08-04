"""
Примеры: Тестирование в Python

Этот файл содержит практические примеры тестирования Python приложений,
включая unit тесты, integration тесты, mocking, fixtures и различные
стратегии тестирования.
"""

import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock, call
import tempfile
import os
import json
import requests
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import sqlite3
from contextlib import contextmanager
import time
import threading

# =============================================================================
# Пример 1: Базовые unit тесты с unittest и pytest
# =============================================================================

class Calculator:
    """Простой калькулятор для демонстрации тестирования"""
    
    def add(self, a: float, b: float) -> float:
        """Сложение двух чисел"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Вычитание двух чисел"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Умножение двух чисел"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Деление двух чисел"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """Возведение в степень"""
        return base ** exponent

# Тесты с unittest
class TestCalculatorUnittest(unittest.TestCase):
    """Тесты калькулятора с использованием unittest"""
    
    def setUp(self):
        """Подготовка данных для каждого теста"""
        self.calc = Calculator()
    
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел"""
        result = self.calc.add(5, 3)
        self.assertEqual(result, 8)
    
    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел"""
        result = self.calc.add(-5, -3)
        self.assertEqual(result, -8)
    
    def test_divide_by_zero_raises_exception(self):
        """Тест деления на ноль"""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        
        self.assertEqual(str(context.exception), "Cannot divide by zero")
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.calc = None

# Тесты с pytest
class TestCalculatorPytest:
    """Тесты калькулятора с использованием pytest"""
    
    @pytest.fixture
    def calculator(self):
        """Fixture для создания экземпляра калькулятора"""
        return Calculator()
    
    def test_add(self, calculator):
        """Тест сложения"""
        assert calculator.add(2, 3) == 5
        assert calculator.add(-1, 1) == 0
        assert calculator.add(0, 0) == 0
    
    def test_subtract(self, calculator):
        """Тест вычитания"""
        assert calculator.subtract(5, 3) == 2
        assert calculator.subtract(0, 5) == -5
    
    def test_multiply(self, calculator):
        """Тест умножения"""
        assert calculator.multiply(4, 3) == 12
        assert calculator.multiply(-2, 3) == -6
        assert calculator.multiply(0, 100) == 0
    
    def test_divide(self, calculator):
        """Тест деления"""
        assert calculator.divide(10, 2) == 5
        assert calculator.divide(7, 2) == 3.5
    
    def test_divide_by_zero(self, calculator):
        """Тест деления на ноль"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)
    
    @pytest.mark.parametrize("base,exponent,expected", [
        (2, 3, 8),
        (5, 0, 1),
        (10, 1, 10),
        (3, 2, 9),
    ])
    def test_power_parametrized(self, calculator, base, exponent, expected):
        """Параметризованный тест возведения в степень"""
        assert calculator.power(base, exponent) == expected

# =============================================================================
# Пример 2: Fixtures и dependency injection
# =============================================================================

@dataclass
class User:
    """Модель пользователя"""
    id: int
    name: str
    email: str
    is_active: bool = True

class UserRepository:
    """Репозиторий для работы с пользователями"""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
    
    def create_user(self, name: str, email: str) -> User:
        """Создать нового пользователя"""
        user = User(id=self._next_id, name=name, email=email)
        self._users[user.id] = user
        self._next_id += 1
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        return self._users.get(user_id)
    
    def get_all_users(self) -> List[User]:
        """Получить всех пользователей"""
        return list(self._users.values())
    
    def update_user(self, user_id: int, name: str = None, email: str = None) -> Optional[User]:
        """Обновить пользователя"""
        user = self._users.get(user_id)
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Удалить пользователя"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def register_user(self, name: str, email: str) -> User:
        """Регистрация нового пользователя"""
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        
        # Проверка уникальности email
        existing_users = self.repository.get_all_users()
        if any(user.email == email for user in existing_users):
            raise ValueError("Email already exists")
        
        return self.repository.create_user(name, email)
    
    def get_active_users(self) -> List[User]:
        """Получить только активных пользователей"""
        all_users = self.repository.get_all_users()
        return [user for user in all_users if user.is_active]
    
    def deactivate_user(self, user_id: int) -> bool:
        """Деактивировать пользователя"""
        user = self.repository.get_user(user_id)
        if user:
            user.is_active = False
            return True
        return False
    
    def _is_valid_email(self, email: str) -> bool:
        """Простая валидация email"""
        return "@" in email and "." in email

# Pytest fixtures для тестирования сервисов
@pytest.fixture
def user_repository():
    """Fixture для репозитория пользователей"""
    return UserRepository()

@pytest.fixture
def user_service(user_repository):
    """Fixture для сервиса пользователей"""
    return UserService(user_repository)

@pytest.fixture
def sample_users(user_repository):
    """Fixture с предустановленными пользователями"""
    users = [
        user_repository.create_user("Alice", "alice@example.com"),
        user_repository.create_user("Bob", "bob@example.com"),
        user_repository.create_user("Charlie", "charlie@example.com"),
    ]
    return users

class TestUserService:
    """Тесты сервиса пользователей с fixtures"""
    
    def test_register_user_success(self, user_service):
        """Тест успешной регистрации пользователя"""
        user = user_service.register_user("John", "john@example.com")
        
        assert user.name == "John"
        assert user.email == "john@example.com"
        assert user.is_active is True
        assert user.id > 0
    
    def test_register_user_invalid_email(self, user_service):
        """Тест регистрации с невалидным email"""
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.register_user("John", "invalid-email")
    
    def test_register_user_duplicate_email(self, user_service, sample_users):
        """Тест регистрации с дублирующимся email"""
        with pytest.raises(ValueError, match="Email already exists"):
            user_service.register_user("NewUser", "alice@example.com")
    
    def test_get_active_users(self, user_service, sample_users):
        """Тест получения активных пользователей"""
        # Деактивируем одного пользователя
        user_service.deactivate_user(sample_users[1].id)
        
        active_users = user_service.get_active_users()
        assert len(active_users) == 2
        assert all(user.is_active for user in active_users)
    
    def test_deactivate_user(self, user_service, sample_users):
        """Тест деактивации пользователя"""
        user_id = sample_users[0].id
        result = user_service.deactivate_user(user_id)
        
        assert result is True
        
        user = user_service.repository.get_user(user_id)
        assert user.is_active is False

# =============================================================================
# Пример 3: Mocking и test doubles
# =============================================================================

class EmailService:
    """Сервис отправки email"""
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Отправить email (в реальности делал бы HTTP запрос)"""
        # В реальном коде здесь был бы запрос к SMTP серверу
        print(f"Sending email to {to}: {subject}")
        return True

class NotificationService:
    """Сервис уведомлений"""
    
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
    
    def notify_user_registration(self, user: User) -> bool:
        """Уведомить о регистрации пользователя"""
        subject = "Welcome to our service!"
        body = f"Hello {user.name}, welcome to our platform!"
        
        return self.email_service.send_email(user.email, subject, body)
    
    def notify_password_reset(self, user: User, reset_token: str) -> bool:
        """Уведомить о сбросе пароля"""
        subject = "Password Reset Request"
        body = f"Hello {user.name}, your reset token is: {reset_token}"
        
        return self.email_service.send_email(user.email, subject, body)

class ExternalAPIClient:
    """Клиент для внешнего API"""
    
    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Получить профиль пользователя из внешнего API"""
        # В реальности делал бы HTTP запрос
        response = requests.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()
    
    def update_user_status(self, user_id: int, status: str) -> bool:
        """Обновить статус пользователя во внешнем API"""
        data = {"status": status}
        response = requests.post(f"https://api.example.com/users/{user_id}/status", json=data)
        return response.status_code == 200

# Тесты с mocking
class TestNotificationService:
    """Тесты сервиса уведомлений с моками"""
    
    @pytest.fixture
    def mock_email_service(self):
        """Mock для email сервиса"""
        return Mock(spec=EmailService)
    
    @pytest.fixture
    def notification_service(self, mock_email_service):
        """Сервис уведомлений с мок email сервисом"""
        return NotificationService(mock_email_service)
    
    @pytest.fixture
    def sample_user(self):
        """Пример пользователя для тестов"""
        return User(id=1, name="John Doe", email="john@example.com")
    
    def test_notify_user_registration(self, notification_service, mock_email_service, sample_user):
        """Тест уведомления о регистрации"""
        # Настраиваем мок
        mock_email_service.send_email.return_value = True
        
        # Выполняем тест
        result = notification_service.notify_user_registration(sample_user)
        
        # Проверяем результат
        assert result is True
        
        # Проверяем, что мок был вызван с правильными параметрами
        mock_email_service.send_email.assert_called_once_with(
            "john@example.com",
            "Welcome to our service!",
            "Hello John Doe, welcome to our platform!"
        )
    
    def test_notify_password_reset(self, notification_service, mock_email_service, sample_user):
        """Тест уведомления о сбросе пароля"""
        mock_email_service.send_email.return_value = True
        reset_token = "abc123"
        
        result = notification_service.notify_password_reset(sample_user, reset_token)
        
        assert result is True
        mock_email_service.send_email.assert_called_once_with(
            "john@example.com",
            "Password Reset Request",
            "Hello John Doe, your reset token is: abc123"
        )
    
    def test_email_service_failure(self, notification_service, mock_email_service, sample_user):
        """Тест обработки ошибки email сервиса"""
        # Настраиваем мок для возврата False (ошибка отправки)
        mock_email_service.send_email.return_value = False
        
        result = notification_service.notify_user_registration(sample_user)
        
        assert result is False

class TestExternalAPIClient:
    """Тесты клиента внешнего API с patch декоратором"""
    
    @patch('requests.get')
    def test_get_user_profile_success(self, mock_get):
        """Тест успешного получения профиля пользователя"""
        # Настраиваем мок ответа
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "status": "active"
        }
        mock_get.return_value = mock_response
        
        client = ExternalAPIClient()
        profile = client.get_user_profile(1)
        
        assert profile["id"] == 1
        assert profile["name"] == "John Doe"
        mock_get.assert_called_once_with("https://api.example.com/users/1")
    
    @patch('requests.get')
    def test_get_user_profile_http_error(self, mock_get):
        """Тест обработки HTTP ошибки"""
        # Настраиваем мок для выброса исключения
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        client = ExternalAPIClient()
        
        with pytest.raises(requests.HTTPError):
            client.get_user_profile(999)
    
    @patch('requests.post')
    def test_update_user_status(self, mock_post):
        """Тест обновления статуса пользователя"""
        # Настраиваем мок ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        client = ExternalAPIClient()
        result = client.update_user_status(1, "inactive")
        
        assert result is True
        mock_post.assert_called_once_with(
            "https://api.example.com/users/1/status",
            json={"status": "inactive"}
        )

# =============================================================================
# Пример 4: Тестирование с базой данных
# =============================================================================

class DatabaseUserRepository:
    """Репозиторий пользователей с базой данных"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            conn.commit()
    
    def create_user(self, name: str, email: str) -> User:
        """Создать пользователя в базе данных"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return User(id=user_id, name=name, email=email)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, email, is_active FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return User(id=row[0], name=row[1], email=row[2], is_active=bool(row[3]))
            return None
    
    def get_all_users(self) -> List[User]:
        """Получить всех пользователей"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, name, email, is_active FROM users")
            rows = cursor.fetchall()
            return [User(id=row[0], name=row[1], email=row[2], is_active=bool(row[3])) 
                   for row in rows]

# Fixtures для тестирования с базой данных
@pytest.fixture
def temp_db():
    """Fixture для временной базы данных"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    yield db_path
    
    # Очистка после теста
    try:
        os.unlink(db_path)
    except OSError:
        pass

@pytest.fixture
def db_repository(temp_db):
    """Fixture для репозитория с временной БД"""
    return DatabaseUserRepository(temp_db)

class TestDatabaseUserRepository:
    """Тесты репозитория с базой данных"""
    
    def test_create_and_get_user(self, db_repository):
        """Тест создания и получения пользователя"""
        # Создаем пользователя
        user = db_repository.create_user("Alice", "alice@example.com")
        assert user.id is not None
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        
        # Получаем пользователя
        retrieved_user = db_repository.get_user(user.id)
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.name == user.name
        assert retrieved_user.email == user.email
    
    def test_get_nonexistent_user(self, db_repository):
        """Тест получения несуществующего пользователя"""
        user = db_repository.get_user(999)
        assert user is None
    
    def test_get_all_users(self, db_repository):
        """Тест получения всех пользователей"""
        # Создаем несколько пользователей
        user1 = db_repository.create_user("Alice", "alice@example.com")
        user2 = db_repository.create_user("Bob", "bob@example.com")
        
        # Получаем всех пользователей
        all_users = db_repository.get_all_users()
        assert len(all_users) == 2
        
        user_emails = {user.email for user in all_users}
        assert "alice@example.com" in user_emails
        assert "bob@example.com" in user_emails

# =============================================================================
# Пример 5: Performance тестирование
# =============================================================================

def fibonacci_recursive(n: int) -> int:
    """Рекурсивное вычисление чисел Фибоначчи (медленно)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_iterative(n: int) -> int:
    """Итеративное вычисление чисел Фибоначчи (быстро)"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

class TestPerformance:
    """Тесты производительности"""
    
    def test_fibonacci_recursive_performance(self):
        """Тест производительности рекурсивного алгоритма"""
        start_time = time.time()
        result = fibonacci_recursive(20)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Проверяем, что результат правильный
        assert result == 6765
        
        # Проверяем, что выполнение не слишком медленное (более 0.1 секунды)
        print(f"Recursive fibonacci(20) took {execution_time:.4f} seconds")
        # В реальных тестах можно установить лимит времени
        # assert execution_time < 1.0  # максимум 1 секунда
    
    def test_fibonacci_iterative_performance(self):
        """Тест производительности итеративного алгоритма"""
        start_time = time.time()
        result = fibonacci_iterative(20)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Проверяем, что результат правильный
        assert result == 6765
        
        # Итеративный алгоритм должен быть очень быстрым
        print(f"Iterative fibonacci(20) took {execution_time:.4f} seconds")
        assert execution_time < 0.001  # менее 1 миллисекунды
    
    @pytest.mark.parametrize("n,expected_max_time", [
        (10, 0.001),
        (20, 0.001),
        (30, 0.001),
    ])
    def test_fibonacci_iterative_scaling(self, n, expected_max_time):
        """Тест масштабируемости итеративного алгоритма"""
        start_time = time.time()
        fibonacci_iterative(n)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < expected_max_time

# =============================================================================
# Пример 6: Интеграционные тесты
# =============================================================================

class UserManagementSystem:
    """Система управления пользователями (интеграция компонентов)"""
    
    def __init__(self, repository: UserRepository, notification_service: NotificationService):
        self.repository = repository
        self.notification_service = notification_service
    
    def register_new_user(self, name: str, email: str) -> User:
        """Полная регистрация пользователя с уведомлением"""
        # Создаем пользователя
        user = self.repository.create_user(name, email)
        
        # Отправляем уведомление
        notification_sent = self.notification_service.notify_user_registration(user)
        
        if not notification_sent:
            # В реальной системе можно логировать ошибку
            print(f"Warning: Failed to send notification to {user.email}")
        
        return user

class TestUserManagementSystemIntegration:
    """Интеграционные тесты системы управления пользователями"""
    
    @pytest.fixture
    def system_components(self):
        """Fixture для создания всех компонентов системы"""
        repository = UserRepository()
        email_service = Mock(spec=EmailService)
        notification_service = NotificationService(email_service)
        system = UserManagementSystem(repository, notification_service)
        
        return {
            'system': system,
            'repository': repository,
            'email_service': email_service,
            'notification_service': notification_service
        }
    
    def test_complete_user_registration_flow(self, system_components):
        """Тест полного процесса регистрации пользователя"""
        components = system_components
        system = components['system']
        email_service = components['email_service']
        
        # Настраиваем мок email сервиса
        email_service.send_email.return_value = True
        
        # Выполняем регистрацию
        user = system.register_new_user("John Doe", "john@example.com")
        
        # Проверяем, что пользователь создан
        assert user.id is not None
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        
        # Проверяем, что пользователь сохранен в репозитории
        saved_user = system.repository.get_user(user.id)
        assert saved_user is not None
        assert saved_user.email == "john@example.com"
        
        # Проверяем, что уведомление отправлено
        email_service.send_email.assert_called_once()
        call_args = email_service.send_email.call_args
        assert call_args[0][0] == "john@example.com"  # to
        assert "Welcome" in call_args[0][1]  # subject
    
    def test_user_registration_with_notification_failure(self, system_components):
        """Тест регистрации с ошибкой отправки уведомления"""
        components = system_components
        system = components['system']
        email_service = components['email_service']
        
        # Настраиваем мок для возврата ошибки
        email_service.send_email.return_value = False
        
        # Выполняем регистрацию (должна пройти несмотря на ошибку уведомления)
        user = system.register_new_user("Jane Doe", "jane@example.com")
        
        # Проверяем, что пользователь все равно создан
        assert user.id is not None
        assert user.name == "Jane Doe"
        
        # Проверяем, что попытка отправить уведомление была
        email_service.send_email.assert_called_once()

# =============================================================================
# Пример 7: Тестирование асинхронного кода
# =============================================================================

import asyncio
from unittest.mock import AsyncMock

class AsyncUserService:
    """Асинхронный сервис пользователей"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def create_user_async(self, name: str, email: str) -> User:
        """Асинхронное создание пользователя"""
        # Симуляция асинхронной операции
        await asyncio.sleep(0.01)
        return self.repository.create_user(name, email)
    
    async def send_welcome_email_async(self, user: User) -> bool:
        """Асинхронная отправка приветственного email"""
        # Симуляция асинхронной отправки email
        await asyncio.sleep(0.05)
        print(f"Sending welcome email to {user.email}")
        return True
    
    async def register_user_with_welcome(self, name: str, email: str) -> User:
        """Регистрация пользователя с отправкой приветственного email"""
        user = await self.create_user_async(name, email)
        await self.send_welcome_email_async(user)
        return user

class TestAsyncUserService:
    """Тесты асинхронного сервиса пользователей"""
    
    @pytest.fixture
    def async_service(self):
        """Fixture для асинхронного сервиса"""
        repository = UserRepository()
        return AsyncUserService(repository)
    
    @pytest.mark.asyncio
    async def test_create_user_async(self, async_service):
        """Тест асинхронного создания пользователя"""
        user = await async_service.create_user_async("Alice", "alice@example.com")
        
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.id is not None
    
    @pytest.mark.asyncio
    async def test_send_welcome_email_async(self, async_service):
        """Тест асинхронной отправки email"""
        user = User(id=1, name="Bob", email="bob@example.com")
        
        result = await async_service.send_welcome_email_async(user)
        assert result is True
    
    @pytest.mark.asyncio
    async def test_register_user_with_welcome(self, async_service):
        """Тест полной асинхронной регистрации"""
        start_time = time.time()
        user = await async_service.register_user_with_welcome("Charlie", "charlie@example.com")
        end_time = time.time()
        
        # Проверяем результат
        assert user.name == "Charlie"
        assert user.email == "charlie@example.com"
        
        # Проверяем, что операция заняла ожидаемое время (около 0.06 секунды)
        execution_time = end_time - start_time
        assert 0.05 < execution_time < 0.1  # учитываем возможные задержки

# =============================================================================
# Пример 8: Тестирование с временными ограничениями
# =============================================================================

class TimeoutService:
    """Сервис с операциями, которые могут зависать"""
    
    def slow_operation(self, delay: float) -> str:
        """Медленная операция"""
        time.sleep(delay)
        return "completed"
    
    def network_request_simulation(self, timeout: float) -> Dict[str, Any]:
        """Симуляция сетевого запроса с таймаутом"""
        time.sleep(timeout)
        return {"status": "success", "data": "response"}

class TestTimeoutService:
    """Тесты с временными ограничениями"""
    
    @pytest.fixture
    def timeout_service(self):
        return TimeoutService()
    
    def test_fast_operation(self, timeout_service):
        """Тест быстрой операции"""
        result = timeout_service.slow_operation(0.01)
        assert result == "completed"
    
    @pytest.mark.timeout(1)  # тест должен завершиться за 1 секунду
    def test_operation_with_timeout(self, timeout_service):
        """Тест операции с ограничением времени"""
        result = timeout_service.slow_operation(0.5)
        assert result == "completed"
    
    def test_timeout_handling_with_threading(self, timeout_service):
        """Тест обработки таймаута с использованием threading"""
        result = None
        exception = None
        
        def run_operation():
            nonlocal result, exception
            try:
                result = timeout_service.network_request_simulation(0.1)
            except Exception as e:
                exception = e
        
        # Запускаем в отдельном потоке с таймаутом
        thread = threading.Thread(target=run_operation)
        thread.start()
        thread.join(timeout=0.5)  # ждем максимум 0.5 секунды
        
        if thread.is_alive():
            # Операция не завершилась в срок
            pytest.fail("Operation timed out")
        
        assert result is not None
        assert result["status"] == "success"
        assert exception is None

# =============================================================================
# Пример 9: Тестирование с внешними ресурсами
# =============================================================================

@contextmanager
def temp_config_file(config_data: Dict[str, Any]):
    """Context manager для создания временного конфигурационного файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
        json.dump(config_data, tmp_file)
        tmp_file_path = tmp_file.name
    
    try:
        yield tmp_file_path
    finally:
        try:
            os.unlink(tmp_file_path)
        except OSError:
            pass

class ConfigService:
    """Сервис для работы с конфигурацией"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config = None
    
    def load_config(self) -> Dict[str, Any]:
        """Загрузить конфигурацию из файла"""
        with open(self.config_path, 'r') as file:
            self._config = json.load(file)
        return self._config
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Получить настройку по ключу"""
        if self._config is None:
            self.load_config()
        return self._config.get(key, default)
    
    def has_setting(self, key: str) -> bool:
        """Проверить наличие настройки"""
        if self._config is None:
            self.load_config()
        return key in self._config

class TestConfigService:
    """Тесты сервиса конфигурации"""
    
    def test_load_config_success(self):
        """Тест успешной загрузки конфигурации"""
        config_data = {
            "database_url": "sqlite:///test.db",
            "debug": True,
            "max_connections": 100
        }
        
        with temp_config_file(config_data) as config_path:
            service = ConfigService(config_path)
            loaded_config = service.load_config()
            
            assert loaded_config == config_data
            assert service.get_setting("database_url") == "sqlite:///test.db"
            assert service.get_setting("debug") is True
            assert service.get_setting("max_connections") == 100
    
    def test_get_setting_with_default(self):
        """Тест получения настройки с значением по умолчанию"""
        config_data = {"existing_key": "value"}
        
        with temp_config_file(config_data) as config_path:
            service = ConfigService(config_path)
            
            # Существующая настройка
            assert service.get_setting("existing_key") == "value"
            
            # Несуществующая настройка с default
            assert service.get_setting("missing_key", "default_value") == "default_value"
            
            # Несуществующая настройка без default
            assert service.get_setting("missing_key") is None
    
    def test_has_setting(self):
        """Тест проверки наличия настройки"""
        config_data = {"key1": "value1", "key2": None}
        
        with temp_config_file(config_data) as config_path:
            service = ConfigService(config_path)
            
            assert service.has_setting("key1") is True
            assert service.has_setting("key2") is True  # None значение тоже считается
            assert service.has_setting("missing_key") is False

# =============================================================================
# Запуск примеров
# =============================================================================

def run_examples():
    """Запуск примеров тестирования"""
    print("=== Примеры тестирования в Python ===\n")
    
    print("1. Простые unit тесты:")
    calc = Calculator()
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"10 / 2 = {calc.divide(10, 2)}")
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"Ошибка деления на ноль: {e}")
    
    print("\n2. Работа с репозиторием:")
    repo = UserRepository()
    user1 = repo.create_user("Alice", "alice@example.com")
    user2 = repo.create_user("Bob", "bob@example.com")
    print(f"Создано пользователей: {len(repo.get_all_users())}")
    
    print("\n3. Сервис с валидацией:")
    service = UserService(repo)
    try:
        user3 = service.register_user("Charlie", "charlie@example.com")
        print(f"Зарегистрирован пользователь: {user3.name}")
    except ValueError as e:
        print(f"Ошибка регистрации: {e}")
    
    print("\n4. Mock пример:")
    mock_email = Mock(spec=EmailService)
    mock_email.send_email.return_value = True
    
    notification_service = NotificationService(mock_email)
    result = notification_service.notify_user_registration(user1)
    print(f"Уведомление отправлено: {result}")
    print(f"Mock был вызван: {mock_email.send_email.called}")
    
    print("\n5. Производительность:")
    start = time.time()
    fib_result = fibonacci_iterative(30)
    duration = time.time() - start
    print(f"fibonacci(30) = {fib_result} за {duration:.4f} секунд")

if __name__ == "__main__":
    run_examples() 