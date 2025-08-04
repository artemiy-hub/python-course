"""
Упражнения: Тестирование в Python

Этот файл содержит практические упражнения для изучения тестирования Python
приложений. Каждое упражнение включает задание, решение и тесты.
"""

import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import json
import sqlite3
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import time
import asyncio
from contextlib import contextmanager

# =============================================================================
# Упражнение 1: Базовое unit тестирование
# =============================================================================

"""
ЗАДАНИЕ 1: Shopping Cart

Создайте класс ShoppingCart со следующими методами:
1. add_item(name: str, price: float, quantity: int = 1)
2. remove_item(name: str)
3. get_total() -> float
4. get_items() -> List[Dict]
5. clear()

Требования:
- Цена не может быть отрицательной
- Количество должно быть положительным
- При добавлении существующего товара увеличивать количество
- Метод get_total() должен возвращать общую стоимость всех товаров
"""

# Ваш код здесь:
class ShoppingCart:
    """Корзина покупок"""
    
    def __init__(self):
        # TODO: Реализуйте инициализацию
        pass
    
    def add_item(self, name: str, price: float, quantity: int = 1):
        """Добавить товар в корзину"""
        # TODO: Реализуйте метод
        pass
    
    def remove_item(self, name: str):
        """Удалить товар из корзины"""
        # TODO: Реализуйте метод
        pass
    
    def get_total(self) -> float:
        """Получить общую стоимость"""
        # TODO: Реализуйте метод
        pass
    
    def get_items(self) -> List[Dict]:
        """Получить список товаров"""
        # TODO: Реализуйте метод
        pass
    
    def clear(self):
        """Очистить корзину"""
        # TODO: Реализуйте метод
        pass

# Решение:
class ShoppingCartSolution:
    """Решение: Корзина покупок"""
    
    def __init__(self):
        self._items = {}
    
    def add_item(self, name: str, price: float, quantity: int = 1):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if name in self._items:
            self._items[name]['quantity'] += quantity
        else:
            self._items[name] = {'price': price, 'quantity': quantity}
    
    def remove_item(self, name: str):
        if name not in self._items:
            raise KeyError(f"Item '{name}' not found in cart")
        del self._items[name]
    
    def get_total(self) -> float:
        return sum(item['price'] * item['quantity'] for item in self._items.values())
    
    def get_items(self) -> List[Dict]:
        return [
            {'name': name, 'price': item['price'], 'quantity': item['quantity']}
            for name, item in self._items.items()
        ]
    
    def clear(self):
        self._items.clear()

# Тесты для проверки решения:
class TestShoppingCart(unittest.TestCase):
    """Тесты корзины покупок"""
    
    def setUp(self):
        self.cart = ShoppingCartSolution()
    
    def test_add_item(self):
        """Тест добавления товара"""
        self.cart.add_item("Apple", 1.50, 3)
        items = self.cart.get_items()
        
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], "Apple")
        self.assertEqual(items[0]['price'], 1.50)
        self.assertEqual(items[0]['quantity'], 3)
    
    def test_add_existing_item(self):
        """Тест добавления существующего товара"""
        self.cart.add_item("Apple", 1.50, 2)
        self.cart.add_item("Apple", 1.50, 3)
        
        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['quantity'], 5)
    
    def test_negative_price_raises_error(self):
        """Тест отрицательной цены"""
        with self.assertRaises(ValueError):
            self.cart.add_item("Apple", -1.50)
    
    def test_zero_quantity_raises_error(self):
        """Тест нулевого количества"""
        with self.assertRaises(ValueError):
            self.cart.add_item("Apple", 1.50, 0)
    
    def test_remove_item(self):
        """Тест удаления товара"""
        self.cart.add_item("Apple", 1.50, 2)
        self.cart.remove_item("Apple")
        
        self.assertEqual(len(self.cart.get_items()), 0)
    
    def test_remove_nonexistent_item(self):
        """Тест удаления несуществующего товара"""
        with self.assertRaises(KeyError):
            self.cart.remove_item("NonExistent")
    
    def test_get_total(self):
        """Тест расчета общей стоимости"""
        self.cart.add_item("Apple", 1.50, 2)  # 3.00
        self.cart.add_item("Banana", 0.75, 4)  # 3.00
        
        self.assertEqual(self.cart.get_total(), 6.00)
    
    def test_clear(self):
        """Тест очистки корзины"""
        self.cart.add_item("Apple", 1.50, 2)
        self.cart.clear()
        
        self.assertEqual(len(self.cart.get_items()), 0)
        self.assertEqual(self.cart.get_total(), 0.0)

# =============================================================================
# Упражнение 2: Mocking и test doubles
# =============================================================================

"""
ЗАДАНИЕ 2: Order Processing System

Создайте систему обработки заказов:

1. PaymentProcessor - обрабатывает платежи
   - process_payment(amount: float, card_token: str) -> bool

2. InventoryService - управляет складом
   - check_availability(product_id: str, quantity: int) -> bool
   - reserve_items(product_id: str, quantity: int) -> bool

3. OrderService - обрабатывает заказы
   - place_order(product_id: str, quantity: int, card_token: str, price: float) -> Dict

Требования к OrderService.place_order():
- Проверить наличие товара
- Зарезервировать товары
- Обработать платеж
- Вернуть результат заказа
"""

# Ваши классы здесь:
class PaymentProcessor:
    """Процессор платежей"""
    
    def process_payment(self, amount: float, card_token: str) -> bool:
        """Обработать платеж"""
        # TODO: Реализуйте метод
        pass

class InventoryService:
    """Сервис управления складом"""
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Проверить наличие товара"""
        # TODO: Реализуйте метод
        pass
    
    def reserve_items(self, product_id: str, quantity: int) -> bool:
        """Зарезервировать товары"""
        # TODO: Реализуйте метод
        pass

class OrderService:
    """Сервис заказов"""
    
    def __init__(self, payment_processor: PaymentProcessor, inventory_service: InventoryService):
        # TODO: Реализуйте инициализацию
        pass
    
    def place_order(self, product_id: str, quantity: int, card_token: str, price: float) -> Dict:
        """Разместить заказ"""
        # TODO: Реализуйте метод
        pass

# Решение:
class PaymentProcessorSolution:
    """Решение: Процессор платежей"""
    
    def process_payment(self, amount: float, card_token: str) -> bool:
        # В реальности здесь был бы вызов платежной системы
        if amount <= 0:
            return False
        if not card_token:
            return False
        return True

class InventoryServiceSolution:
    """Решение: Сервис управления складом"""
    
    def __init__(self):
        self._inventory = {}
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        available = self._inventory.get(product_id, 0)
        return available >= quantity
    
    def reserve_items(self, product_id: str, quantity: int) -> bool:
        if self.check_availability(product_id, quantity):
            self._inventory[product_id] -= quantity
            return True
        return False
    
    def add_stock(self, product_id: str, quantity: int):
        """Добавить товар на склад (для тестов)"""
        self._inventory[product_id] = self._inventory.get(product_id, 0) + quantity

class OrderServiceSolution:
    """Решение: Сервис заказов"""
    
    def __init__(self, payment_processor: PaymentProcessorSolution, inventory_service: InventoryServiceSolution):
        self.payment_processor = payment_processor
        self.inventory_service = inventory_service
    
    def place_order(self, product_id: str, quantity: int, card_token: str, price: float) -> Dict:
        # Проверяем наличие товара
        if not self.inventory_service.check_availability(product_id, quantity):
            return {
                'success': False,
                'error': 'Insufficient inventory',
                'order_id': None
            }
        
        # Резервируем товары
        if not self.inventory_service.reserve_items(product_id, quantity):
            return {
                'success': False,
                'error': 'Failed to reserve items',
                'order_id': None
            }
        
        # Обрабатываем платеж
        total_amount = price * quantity
        if not self.payment_processor.process_payment(total_amount, card_token):
            # Возвращаем товары в случае неудачи платежа
            self.inventory_service.add_stock(product_id, quantity)
            return {
                'success': False,
                'error': 'Payment failed',
                'order_id': None
            }
        
        # Успешный заказ
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            'success': True,
            'error': None,
            'order_id': order_id,
            'total_amount': total_amount
        }

# Тесты с моками:
class TestOrderService:
    """Тесты сервиса заказов с моками"""
    
    @pytest.fixture
    def mock_payment_processor(self):
        """Mock процессора платежей"""
        return Mock(spec=PaymentProcessorSolution)
    
    @pytest.fixture
    def mock_inventory_service(self):
        """Mock сервиса склада"""
        return Mock(spec=InventoryServiceSolution)
    
    @pytest.fixture
    def order_service(self, mock_payment_processor, mock_inventory_service):
        """Сервис заказов с моками"""
        return OrderServiceSolution(mock_payment_processor, mock_inventory_service)
    
    def test_successful_order(self, order_service, mock_payment_processor, mock_inventory_service):
        """Тест успешного заказа"""
        # Настраиваем моки
        mock_inventory_service.check_availability.return_value = True
        mock_inventory_service.reserve_items.return_value = True
        mock_payment_processor.process_payment.return_value = True
        
        # Выполняем заказ
        result = order_service.place_order("PRODUCT-123", 2, "card_token", 10.0)
        
        # Проверяем результат
        assert result['success'] is True
        assert result['error'] is None
        assert result['order_id'] is not None
        assert result['total_amount'] == 20.0
        
        # Проверяем вызовы моков
        mock_inventory_service.check_availability.assert_called_once_with("PRODUCT-123", 2)
        mock_inventory_service.reserve_items.assert_called_once_with("PRODUCT-123", 2)
        mock_payment_processor.process_payment.assert_called_once_with(20.0, "card_token")
    
    def test_insufficient_inventory(self, order_service, mock_payment_processor, mock_inventory_service):
        """Тест недостаточного количества товара"""
        mock_inventory_service.check_availability.return_value = False
        
        result = order_service.place_order("PRODUCT-123", 10, "card_token", 10.0)
        
        assert result['success'] is False
        assert result['error'] == 'Insufficient inventory'
        assert result['order_id'] is None
        
        # Платеж не должен был быть вызван
        mock_payment_processor.process_payment.assert_not_called()
    
    def test_payment_failure(self, order_service, mock_payment_processor, mock_inventory_service):
        """Тест неудачного платежа"""
        mock_inventory_service.check_availability.return_value = True
        mock_inventory_service.reserve_items.return_value = True
        mock_payment_processor.process_payment.return_value = False
        
        result = order_service.place_order("PRODUCT-123", 2, "card_token", 10.0)
        
        assert result['success'] is False
        assert result['error'] == 'Payment failed'
        
        # Проверяем, что товары были возвращены
        mock_inventory_service.add_stock.assert_called_once_with("PRODUCT-123", 2)

# =============================================================================
# Упражнение 3: Fixtures и параметризация
# =============================================================================

"""
ЗАДАНИЕ 3: Task Management System

Создайте систему управления задачами:

1. Task (dataclass):
   - id: int
   - title: str
   - description: str
   - status: str (pending, in_progress, completed)
   - created_at: datetime

2. TaskManager:
   - create_task(title: str, description: str) -> Task
   - get_task(task_id: int) -> Optional[Task]
   - update_task_status(task_id: int, status: str) -> bool
   - get_tasks_by_status(status: str) -> List[Task]
   - delete_task(task_id: int) -> bool

Создайте fixtures и параметризованные тесты.
"""

# Ваш код здесь:
@dataclass
class Task:
    """Задача"""
    # TODO: Определите поля
    pass

class TaskManager:
    """Менеджер задач"""
    
    def __init__(self):
        # TODO: Реализуйте инициализацию
        pass
    
    def create_task(self, title: str, description: str):
        """Создать задачу"""
        # TODO: Реализуйте метод
        pass
    
    def get_task(self, task_id: int):
        """Получить задачу"""
        # TODO: Реализуйте метод
        pass
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        """Обновить статус задачи"""
        # TODO: Реализуйте метод
        pass
    
    def get_tasks_by_status(self, status: str):
        """Получить задачи по статусу"""
        # TODO: Реализуйте метод
        pass
    
    def delete_task(self, task_id: int) -> bool:
        """Удалить задачу"""
        # TODO: Реализуйте метод
        pass

# Решение:
@dataclass
class TaskSolution:
    """Решение: Задача"""
    id: int
    title: str
    description: str
    status: str = "pending"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class TaskManagerSolution:
    """Решение: Менеджер задач"""
    
    VALID_STATUSES = ["pending", "in_progress", "completed"]
    
    def __init__(self):
        self._tasks = {}
        self._next_id = 1
    
    def create_task(self, title: str, description: str) -> TaskSolution:
        if not title.strip():
            raise ValueError("Title cannot be empty")
        
        task = TaskSolution(
            id=self._next_id,
            title=title.strip(),
            description=description.strip()
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[TaskSolution]:
        return self._tasks.get(task_id)
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        
        task = self._tasks.get(task_id)
        if task:
            task.status = status
            return True
        return False
    
    def get_tasks_by_status(self, status: str) -> List[TaskSolution]:
        return [task for task in self._tasks.values() if task.status == status]
    
    def delete_task(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

# Fixtures для тестов:
@pytest.fixture
def task_manager():
    """Fixture для менеджера задач"""
    return TaskManagerSolution()

@pytest.fixture
def sample_tasks(task_manager):
    """Fixture с примерами задач"""
    tasks = [
        task_manager.create_task("Task 1", "Description 1"),
        task_manager.create_task("Task 2", "Description 2"),
        task_manager.create_task("Task 3", "Description 3"),
    ]
    
    # Обновляем статусы
    task_manager.update_task_status(tasks[1].id, "in_progress")
    task_manager.update_task_status(tasks[2].id, "completed")
    
    return tasks

# Параметризованные тесты:
class TestTaskManager:
    """Тесты менеджера задач"""
    
    def test_create_task(self, task_manager):
        """Тест создания задачи"""
        task = task_manager.create_task("Test Task", "Test Description")
        
        assert task.id > 0
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == "pending"
        assert task.created_at is not None
    
    def test_create_task_empty_title(self, task_manager):
        """Тест создания задачи с пустым заголовком"""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            task_manager.create_task("", "Description")
    
    @pytest.mark.parametrize("title,description,expected_title,expected_description", [
        ("  Task  ", "  Description  ", "Task", "Description"),
        ("Task", "", "Task", ""),
        ("Multi\nLine\nTask", "Multi\nLine\nDescription", "Multi\nLine\nTask", "Multi\nLine\nDescription"),
    ])
    def test_create_task_whitespace_handling(self, task_manager, title, description, expected_title, expected_description):
        """Параметризованный тест обработки пробелов"""
        task = task_manager.create_task(title, description)
        assert task.title == expected_title
        assert task.description == expected_description
    
    def test_get_task(self, task_manager, sample_tasks):
        """Тест получения задачи"""
        task_id = sample_tasks[0].id
        retrieved_task = task_manager.get_task(task_id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == task_id
        assert retrieved_task.title == "Task 1"
    
    def test_get_nonexistent_task(self, task_manager):
        """Тест получения несуществующей задачи"""
        task = task_manager.get_task(999)
        assert task is None
    
    @pytest.mark.parametrize("status", ["pending", "in_progress", "completed"])
    def test_update_task_status_valid(self, task_manager, sample_tasks, status):
        """Параметризованный тест обновления статуса"""
        task_id = sample_tasks[0].id
        result = task_manager.update_task_status(task_id, status)
        
        assert result is True
        
        updated_task = task_manager.get_task(task_id)
        assert updated_task.status == status
    
    def test_update_task_status_invalid(self, task_manager, sample_tasks):
        """Тест обновления статуса на невалидный"""
        task_id = sample_tasks[0].id
        
        with pytest.raises(ValueError, match="Invalid status"):
            task_manager.update_task_status(task_id, "invalid_status")
    
    @pytest.mark.parametrize("status,expected_count", [
        ("pending", 1),
        ("in_progress", 1),
        ("completed", 1),
        ("nonexistent", 0),
    ])
    def test_get_tasks_by_status(self, task_manager, sample_tasks, status, expected_count):
        """Параметризованный тест получения задач по статусу"""
        tasks = task_manager.get_tasks_by_status(status)
        assert len(tasks) == expected_count
        
        for task in tasks:
            assert task.status == status
    
    def test_delete_task(self, task_manager, sample_tasks):
        """Тест удаления задачи"""
        task_id = sample_tasks[0].id
        result = task_manager.delete_task(task_id)
        
        assert result is True
        assert task_manager.get_task(task_id) is None
    
    def test_delete_nonexistent_task(self, task_manager):
        """Тест удаления несуществующей задачи"""
        result = task_manager.delete_task(999)
        assert result is False

# =============================================================================
# Упражнение 4: Тестирование с базой данных
# =============================================================================

"""
ЗАДАНИЕ 4: User Profile Database

Создайте систему профилей пользователей с базой данных:

1. UserProfile (dataclass):
   - id: int
   - username: str
   - email: str
   - first_name: str
   - last_name: str
   - is_active: bool

2. UserProfileRepository:
   - create_profile(username: str, email: str, first_name: str, last_name: str) -> UserProfile
   - get_profile_by_id(profile_id: int) -> Optional[UserProfile]
   - get_profile_by_username(username: str) -> Optional[UserProfile]
   - update_profile(profile_id: int, **kwargs) -> bool
   - delete_profile(profile_id: int) -> bool
   - search_profiles(query: str) -> List[UserProfile]

Создайте тесты с временной базой данных.
"""

# Ваш код здесь:
@dataclass
class UserProfile:
    """Профиль пользователя"""
    # TODO: Определите поля
    pass

class UserProfileRepository:
    """Репозиторий профилей пользователей"""
    
    def __init__(self, db_path: str):
        # TODO: Реализуйте инициализацию
        pass
    
    def create_profile(self, username: str, email: str, first_name: str, last_name: str):
        """Создать профиль"""
        # TODO: Реализуйте метод
        pass
    
    def get_profile_by_id(self, profile_id: int):
        """Получить профиль по ID"""
        # TODO: Реализуйте метод
        pass

# Решение:
@dataclass
class UserProfileSolution:
    """Решение: Профиль пользователя"""
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool = True

class UserProfileRepositorySolution:
    """Решение: Репозиторий профилей пользователей"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            conn.commit()
    
    def create_profile(self, username: str, email: str, first_name: str, last_name: str) -> UserProfileSolution:
        """Создать профиль"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO user_profiles (username, email, first_name, last_name)
                   VALUES (?, ?, ?, ?)""",
                (username, email, first_name, last_name)
            )
            profile_id = cursor.lastrowid
            conn.commit()
            
            return UserProfileSolution(
                id=profile_id,
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
    
    def get_profile_by_id(self, profile_id: int) -> Optional[UserProfileSolution]:
        """Получить профиль по ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, username, email, first_name, last_name, is_active FROM user_profiles WHERE id = ?",
                (profile_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return UserProfileSolution(*row)
            return None
    
    def get_profile_by_username(self, username: str) -> Optional[UserProfileSolution]:
        """Получить профиль по имени пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, username, email, first_name, last_name, is_active FROM user_profiles WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            
            if row:
                return UserProfileSolution(*row)
            return None
    
    def update_profile(self, profile_id: int, **kwargs) -> bool:
        """Обновить профиль"""
        allowed_fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return False
        
        set_clause = ", ".join(f"{field} = ?" for field in update_fields.keys())
        query = f"UPDATE user_profiles SET {set_clause} WHERE id = ?"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, list(update_fields.values()) + [profile_id])
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_profile(self, profile_id: int) -> bool:
        """Удалить профиль"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM user_profiles WHERE id = ?", (profile_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_profiles(self, query: str) -> List[UserProfileSolution]:
        """Поиск профилей"""
        search_term = f"%{query}%"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT id, username, email, first_name, last_name, is_active 
                   FROM user_profiles 
                   WHERE username LIKE ? OR email LIKE ? OR first_name LIKE ? OR last_name LIKE ?""",
                (search_term, search_term, search_term, search_term)
            )
            rows = cursor.fetchall()
            return [UserProfileSolution(*row) for row in rows]

# Fixtures для тестов с БД:
@pytest.fixture
def temp_db():
    """Fixture для временной базы данных"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    yield db_path
    
    try:
        os.unlink(db_path)
    except OSError:
        pass

@pytest.fixture
def profile_repository(temp_db):
    """Fixture для репозитория профилей"""
    return UserProfileRepositorySolution(temp_db)

@pytest.fixture
def sample_profiles(profile_repository):
    """Fixture с примерами профилей"""
    profiles = [
        profile_repository.create_profile("alice", "alice@example.com", "Alice", "Smith"),
        profile_repository.create_profile("bob", "bob@example.com", "Bob", "Johnson"),
        profile_repository.create_profile("charlie", "charlie@example.com", "Charlie", "Brown"),
    ]
    return profiles

# Тесты с базой данных:
class TestUserProfileRepository:
    """Тесты репозитория профилей пользователей"""
    
    def test_create_and_get_profile(self, profile_repository):
        """Тест создания и получения профиля"""
        profile = profile_repository.create_profile("testuser", "test@example.com", "Test", "User")
        
        assert profile.id is not None
        assert profile.username == "testuser"
        assert profile.email == "test@example.com"
        assert profile.first_name == "Test"
        assert profile.last_name == "User"
        assert profile.is_active is True
        
        retrieved = profile_repository.get_profile_by_id(profile.id)
        assert retrieved is not None
        assert retrieved.username == "testuser"
    
    def test_get_profile_by_username(self, profile_repository, sample_profiles):
        """Тест получения профиля по имени пользователя"""
        profile = profile_repository.get_profile_by_username("alice")
        
        assert profile is not None
        assert profile.username == "alice"
        assert profile.email == "alice@example.com"
    
    def test_update_profile(self, profile_repository, sample_profiles):
        """Тест обновления профиля"""
        profile_id = sample_profiles[0].id
        
        result = profile_repository.update_profile(
            profile_id,
            first_name="Updated Alice",
            email="alice.updated@example.com"
        )
        
        assert result is True
        
        updated_profile = profile_repository.get_profile_by_id(profile_id)
        assert updated_profile.first_name == "Updated Alice"
        assert updated_profile.email == "alice.updated@example.com"
        assert updated_profile.last_name == "Smith"  # Unchanged
    
    def test_delete_profile(self, profile_repository, sample_profiles):
        """Тест удаления профиля"""
        profile_id = sample_profiles[0].id
        
        result = profile_repository.delete_profile(profile_id)
        assert result is True
        
        deleted_profile = profile_repository.get_profile_by_id(profile_id)
        assert deleted_profile is None
    
    def test_search_profiles(self, profile_repository, sample_profiles):
        """Тест поиска профилей"""
        # Поиск по имени
        results = profile_repository.search_profiles("Alice")
        assert len(results) == 1
        assert results[0].first_name == "Alice"
        
        # Поиск по email
        results = profile_repository.search_profiles("bob@example")
        assert len(results) == 1
        assert results[0].username == "bob"
        
        # Поиск без результатов
        results = profile_repository.search_profiles("nonexistent")
        assert len(results) == 0

# =============================================================================
# Упражнение 5: Асинхронное тестирование
# =============================================================================

"""
ЗАДАНИЕ 5: Async File Processor

Создайте асинхронный процессор файлов:

1. AsyncFileProcessor:
   - read_file_async(file_path: str) -> str
   - write_file_async(file_path: str, content: str) -> bool
   - process_files_batch(file_paths: List[str]) -> List[Dict]

Требования:
- Все операции должны быть асинхронными
- process_files_batch должен обрабатывать файлы параллельно
- Обрабатывать ошибки чтения/записи файлов

Создайте асинхронные тесты.
"""

# Ваш код здесь:
class AsyncFileProcessor:
    """Асинхронный процессор файлов"""
    
    async def read_file_async(self, file_path: str) -> str:
        """Асинхронное чтение файла"""
        # TODO: Реализуйте метод
        pass
    
    async def write_file_async(self, file_path: str, content: str) -> bool:
        """Асинхронная запись в файл"""
        # TODO: Реализуйте метод
        pass
    
    async def process_files_batch(self, file_paths: List[str]) -> List[Dict]:
        """Асинхронная обработка пакета файлов"""
        # TODO: Реализуйте метод
        pass

# Решение:
class AsyncFileProcessorSolution:
    """Решение: Асинхронный процессор файлов"""
    
    async def read_file_async(self, file_path: str) -> str:
        """Асинхронное чтение файла"""
        def read_file():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, read_file)
    
    async def write_file_async(self, file_path: str, content: str) -> bool:
        """Асинхронная запись в файл"""
        def write_file():
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            except Exception:
                return False
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, write_file)
    
    async def process_files_batch(self, file_paths: List[str]) -> List[Dict]:
        """Асинхронная обработка пакета файлов"""
        async def process_single_file(file_path: str) -> Dict:
            try:
                content = await self.read_file_async(file_path)
                word_count = len(content.split())
                char_count = len(content)
                
                return {
                    'file_path': file_path,
                    'success': True,
                    'word_count': word_count,
                    'char_count': char_count,
                    'error': None
                }
            except Exception as e:
                return {
                    'file_path': file_path,
                    'success': False,
                    'word_count': 0,
                    'char_count': 0,
                    'error': str(e)
                }
        
        tasks = [process_single_file(file_path) for file_path in file_paths]
        return await asyncio.gather(*tasks)

# Асинхронные тесты:
class TestAsyncFileProcessor:
    """Тесты асинхронного процессора файлов"""
    
    @pytest.fixture
    def processor(self):
        """Fixture для процессора файлов"""
        return AsyncFileProcessorSolution()
    
    @pytest.fixture
    def temp_files(self):
        """Fixture для временных файлов"""
        files = []
        file_contents = [
            ("Hello world", "hello.txt"),
            ("Python async testing", "python.txt"),
            ("Multiple\nlines\nof\ntext", "multiline.txt"),
        ]
        
        for content, filename in file_contents:
            with tempfile.NamedTemporaryFile(mode='w', suffix=filename, delete=False) as tmp_file:
                tmp_file.write(content)
                files.append(tmp_file.name)
        
        yield files
        
        # Cleanup
        for file_path in files:
            try:
                os.unlink(file_path)
            except OSError:
                pass
    
    @pytest.mark.asyncio
    async def test_read_file_async(self, processor, temp_files):
        """Тест асинхронного чтения файла"""
        content = await processor.read_file_async(temp_files[0])
        assert content == "Hello world"
    
    @pytest.mark.asyncio
    async def test_write_file_async(self, processor):
        """Тест асинхронной записи в файл"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file_path = tmp_file.name
        
        try:
            content = "Test content for async write"
            result = await processor.write_file_async(file_path, content)
            
            assert result is True
            
            # Проверяем, что файл записан правильно
            written_content = await processor.read_file_async(file_path)
            assert written_content == content
        
        finally:
            try:
                os.unlink(file_path)
            except OSError:
                pass
    
    @pytest.mark.asyncio
    async def test_process_files_batch(self, processor, temp_files):
        """Тест асинхронной обработки пакета файлов"""
        results = await processor.process_files_batch(temp_files)
        
        assert len(results) == 3
        
        # Проверяем первый файл
        result1 = results[0]
        assert result1['success'] is True
        assert result1['word_count'] == 2  # "Hello world"
        assert result1['char_count'] == 11
        assert result1['error'] is None
        
        # Проверяем второй файл
        result2 = results[1]
        assert result2['success'] is True
        assert result2['word_count'] == 3  # "Python async testing"
        
        # Все файлы должны быть обработаны успешно
        for result in results:
            assert result['success'] is True
    
    @pytest.mark.asyncio
    async def test_process_nonexistent_files(self, processor):
        """Тест обработки несуществующих файлов"""
        file_paths = ["nonexistent1.txt", "nonexistent2.txt"]
        results = await processor.process_files_batch(file_paths)
        
        assert len(results) == 2
        
        for result in results:
            assert result['success'] is False
            assert result['error'] is not None
            assert "No such file" in result['error']

# =============================================================================
# Запуск тестов
# =============================================================================

def run_tests():
    """Запуск всех тестов"""
    print("=== Упражнения: Тестирование ===\n")
    print("Запуск тестов для проверки решений...\n")
    
    # Тестируем Shopping Cart
    print("1. Тестирование Shopping Cart...")
    cart = ShoppingCartSolution()
    cart.add_item("Apple", 1.50, 3)
    cart.add_item("Banana", 0.75, 2)
    print(f"   Товаров в корзине: {len(cart.get_items())}")
    print(f"   Общая стоимость: ${cart.get_total():.2f}")
    
    # Тестируем Task Manager
    print("\n2. Тестирование Task Manager...")
    manager = TaskManagerSolution()
    task1 = manager.create_task("Test Task 1", "Description 1")
    task2 = manager.create_task("Test Task 2", "Description 2")
    manager.update_task_status(task1.id, "completed")
    completed_tasks = manager.get_tasks_by_status("completed")
    print(f"   Создано задач: 2")
    print(f"   Завершенных задач: {len(completed_tasks)}")
    
    # Тестируем Order Service с моками
    print("\n3. Тестирование Order Service с моками...")
    mock_payment = Mock()
    mock_inventory = Mock()
    mock_payment.process_payment.return_value = True
    mock_inventory.check_availability.return_value = True
    mock_inventory.reserve_items.return_value = True
    
    order_service = OrderServiceSolution(mock_payment, mock_inventory)
    result = order_service.place_order("PRODUCT-123", 2, "token", 10.0)
    print(f"   Заказ размещен: {result['success']}")
    print(f"   ID заказа: {result.get('order_id', 'N/A')}")
    
    print("\nВсе примеры работают корректно! ✅")

if __name__ == "__main__":
    run_tests() 