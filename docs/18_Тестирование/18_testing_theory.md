# Теория: Тестирование в Python

## 🎯 Цель раздела

Этот раздел охватывает все аспекты тестирования в Python: от базовых unit-тестов до сложных интеграционных тестов, от TDD до автоматизации тестирования в CI/CD.

## 📋 Содержание

1. [Основы тестирования](#основы-тестирования)
2. [unittest - встроенный фреймворк](#unittest---встроенный-фреймворк)
3. [pytest - современное тестирование](#pytest---современное-тестирование)
4. [Типы тестов](#типы-тестов)
5. [Моки и фикстуры](#моки-и-фикстуры)
6. [TDD и BDD](#tdd-и-bdd)
7. [Покрытие кода и метрики](#покрытие-кода-и-метрики)

---

## 🧪 Основы тестирования

### Принципы качественного тестирования

```python
"""
Принципы тестирования:

1. FAST - Быстрые тесты
2. INDEPENDENT - Независимые тесты
3. REPEATABLE - Повторяемые результаты
4. SELF-VALIDATING - Четкий результат pass/fail
5. TIMELY - Написаны своевременно

Пирамида тестирования:
- Unit Tests (70%) - Тестирование отдельных функций/классов
- Integration Tests (20%) - Тестирование взаимодействия компонентов
- E2E Tests (10%) - Тестирование полного пользовательского пути
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import functools

# Базовые концепции тестирования
@dataclass
class TestResult:
    """Результат выполнения теста"""
    name: str
    passed: bool
    message: str
    execution_time: float
    timestamp: datetime

class TestCase(ABC):
    """Абстрактный базовый класс для тест-кейсов"""
    
    def __init__(self, name: str):
        self.name = name
        self.setup_done = False
        self.teardown_done = False
    
    def setUp(self):
        """Подготовка к тесту"""
        self.setup_done = True
    
    def tearDown(self):
        """Очистка после теста"""
        self.teardown_done = True
    
    @abstractmethod
    def run_test(self) -> TestResult:
        """Выполнение теста"""
        pass
    
    def assert_equal(self, actual: Any, expected: Any, message: str = ""):
        """Проверка равенства"""
        if actual != expected:
            raise AssertionError(f"Expected {expected}, got {actual}. {message}")
    
    def assert_true(self, condition: bool, message: str = ""):
        """Проверка истинности"""
        if not condition:
            raise AssertionError(f"Expected True, got False. {message}")
    
    def assert_raises(self, exception_type: type, callable_obj: Callable, *args, **kwargs):
        """Проверка выброса исключения"""
        try:
            callable_obj(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} to be raised")
        except exception_type:
            pass  # Ожидаемое исключение
        except Exception as e:
            raise AssertionError(f"Expected {exception_type.__name__}, got {type(e).__name__}")

# Простой test runner
class SimpleTestRunner:
    """Простой запускатель тестов"""
    
    def __init__(self):
        self.results: List[TestResult] = []
    
    def run_test(self, test_case: TestCase) -> TestResult:
        """Запуск одного теста"""
        start_time = datetime.now()
        
        try:
            test_case.setUp()
            result = test_case.run_test()
            test_case.tearDown()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            
            self.results.append(result)
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            result = TestResult(
                name=test_case.name,
                passed=False,
                message=str(e),
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            self.results.append(result)
            return result
    
    def run_suite(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        """Запуск набора тестов"""
        results = []
        for test_case in test_cases:
            result = self.run_test(test_case)
            results.append(result)
        
        passed_count = sum(1 for r in results if r.passed)
        total_time = sum(r.execution_time for r in results)
        
        return {
            'total_tests': len(results),
            'passed': passed_count,
            'failed': len(results) - passed_count,
            'success_rate': passed_count / len(results) * 100,
            'total_time': total_time,
            'results': results
        }

# Декораторы для тестирования
def test_method(func):
    """Декоратор для маркировки тестовых методов"""
    func._is_test = True
    return func

def skip_test(reason: str):
    """Декоратор для пропуска тестов"""
    def decorator(func):
        func._skip = True
        func._skip_reason = reason
        return func
    return decorator

def timeout(seconds: int):
    """Декоратор для ограничения времени выполнения теста"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Test timed out after {seconds} seconds")
            
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            
            try:
                result = func(*args, **kwargs)
                signal.alarm(0)  # Отменяем таймер
                return result
            except TimeoutError:
                signal.alarm(0)
                raise
        
        return wrapper
    return decorator

def parametrize(params: List[tuple]):
    """Декоратор для параметризованных тестов"""
    def decorator(func):
        func._parametrized = True
        func._params = params
        return func
    return decorator

# Пример использования базовых концепций
class CalculatorTestCase(TestCase):
    """Пример тест-кейса для калькулятора"""
    
    def setUp(self):
        super().setUp()
        self.calculator = Calculator()
    
    def run_test(self) -> TestResult:
        try:
            # Тест сложения
            result = self.calculator.add(2, 3)
            self.assert_equal(result, 5, "Addition test failed")
            
            # Тест деления на ноль
            self.assert_raises(ZeroDivisionError, self.calculator.divide, 5, 0)
            
            return TestResult(
                name=self.name,
                passed=True,
                message="All assertions passed",
                execution_time=0.0,  # Будет установлено runner'ом
                timestamp=datetime.now()
            )
            
        except AssertionError as e:
            return TestResult(
                name=self.name,
                passed=False,
                message=str(e),
                execution_time=0.0,
                timestamp=datetime.now()
            )

class Calculator:
    """Простой калькулятор для демонстрации тестов"""
    
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
```

---

## 🔬 unittest - встроенный фреймворк

unittest - стандартный модуль Python для тестирования, основанный на JUnit.

### Основы unittest

```python
import unittest
from unittest.mock import Mock, patch, MagicMock, call
from unittest import TestCase, TestSuite, TextTestRunner
import sys
import io
from typing import List, Dict, Any

class MathOperations:
    """Класс для демонстрации тестирования"""
    
    def __init__(self):
        self.history: List[str] = []
    
    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base: float, exponent: float) -> float:
        if base == 0 and exponent < 0:
            raise ValueError("Cannot raise zero to negative power")
        result = base ** exponent
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def get_history(self) -> List[str]:
        return self.history.copy()
    
    def clear_history(self):
        self.history.clear()

class TestMathOperations(unittest.TestCase):
    """Комплексные тесты для MathOperations"""
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.math_ops = MathOperations()
        self.test_data = [
            (2, 3, 5),
            (0, 5, 5),
            (-1, 1, 0),
            (10.5, 2.5, 13.0)
        ]
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.math_ops.clear_history()
    
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел"""
        result = self.math_ops.add(5, 3)
        self.assertEqual(result, 8)
        self.assertIn("5 + 3 = 8", self.math_ops.get_history())
    
    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел"""
        result = self.math_ops.add(-5, -3)
        self.assertEqual(result, -8)
    
    def test_add_mixed_numbers(self):
        """Тест сложения смешанных чисел"""
        result = self.math_ops.add(-5, 3)
        self.assertEqual(result, -2)
    
    def test_add_with_zero(self):
        """Тест сложения с нулем"""
        result = self.math_ops.add(5, 0)
        self.assertEqual(result, 5)
    
    def test_divide_normal_case(self):
        """Тест обычного деления"""
        result = self.math_ops.divide(10, 2)
        self.assertEqual(result, 5.0)
    
    def test_divide_by_zero(self):
        """Тест деления на ноль"""
        with self.assertRaises(ValueError) as context:
            self.math_ops.divide(5, 0)
        
        self.assertEqual(str(context.exception), "Cannot divide by zero")
    
    def test_divide_negative_numbers(self):
        """Тест деления отрицательных чисел"""
        result = self.math_ops.divide(-10, -2)
        self.assertEqual(result, 5.0)
    
    def test_power_positive_base(self):
        """Тест возведения в степень положительного основания"""
        result = self.math_ops.power(2, 3)
        self.assertEqual(result, 8)
    
    def test_power_zero_base_positive_exponent(self):
        """Тест возведения нуля в положительную степень"""
        result = self.math_ops.power(0, 5)
        self.assertEqual(result, 0)
    
    def test_power_zero_base_negative_exponent(self):
        """Тест возведения нуля в отрицательную степень"""
        with self.assertRaises(ValueError):
            self.math_ops.power(0, -1)
    
    def test_history_tracking(self):
        """Тест отслеживания истории операций"""
        self.math_ops.add(1, 2)
        self.math_ops.divide(6, 2)
        self.math_ops.power(2, 3)
        
        history = self.math_ops.get_history()
        self.assertEqual(len(history), 3)
        self.assertIn("1 + 2 = 3", history)
        self.assertIn("6 / 2 = 3.0", history)
        self.assertIn("2 ^ 3 = 8", history)
    
    def test_clear_history(self):
        """Тест очистки истории"""
        self.math_ops.add(1, 2)
        self.assertEqual(len(self.math_ops.get_history()), 1)
        
        self.math_ops.clear_history()
        self.assertEqual(len(self.math_ops.get_history()), 0)
    
    @unittest.skip("Пропускаем этот тест для демонстрации")
    def test_skipped_example(self):
        """Пример пропущенного теста"""
        pass
    
    @unittest.skipIf(sys.version_info < (3, 8), "Требует Python 3.8+")
    def test_conditional_skip(self):
        """Тест с условным пропуском"""
        self.assertTrue(True)
    
    def test_with_subtest(self):
        """Тест с подтестами"""
        for a, b, expected in self.test_data:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.math_ops.add(a, b)
                self.assertEqual(result, expected)

# Тесты с моками
class DatabaseService:
    """Сервис для работы с базой данных"""
    
    def __init__(self, connection):
        self.connection = connection
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        return result if result else None
    
    def create_user(self, username: str, email: str) -> int:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        self.connection.commit()
        return cursor.lastrowid
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        
        set_clause = ", ".join(f"{key} = ?" for key in kwargs.keys())
        query = f"UPDATE users SET {set_clause} WHERE id = ?"
        
        cursor = self.connection.cursor()
        cursor.execute(query, list(kwargs.values()) + [user_id])
        self.connection.commit()
        
        return cursor.rowcount > 0

class TestDatabaseService(unittest.TestCase):
    """Тесты для DatabaseService с моками"""
    
    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.db_service = DatabaseService(self.mock_connection)
    
    def test_get_user_found(self):
        """Тест получения существующего пользователя"""
        # Настройка мока
        expected_user = {"id": 1, "username": "john", "email": "john@example.com"}
        self.mock_cursor.fetchone.return_value = expected_user
        
        # Выполнение
        result = self.db_service.get_user(1)
        
        # Проверки
        self.assertEqual(result, expected_user)
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM users WHERE id = ?", (1,)
        )
    
    def test_get_user_not_found(self):
        """Тест получения несуществующего пользователя"""
        self.mock_cursor.fetchone.return_value = None
        
        result = self.db_service.get_user(999)
        
        self.assertIsNone(result)
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM users WHERE id = ?", (999,)
        )
    
    def test_create_user(self):
        """Тест создания пользователя"""
        self.mock_cursor.lastrowid = 123
        
        result = self.db_service.create_user("alice", "alice@example.com")
        
        self.assertEqual(result, 123)
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            ("alice", "alice@example.com")
        )
        self.mock_connection.commit.assert_called_once()
    
    def test_update_user_success(self):
        """Тест успешного обновления пользователя"""
        self.mock_cursor.rowcount = 1
        
        result = self.db_service.update_user(1, username="bob", email="bob@example.com")
        
        self.assertTrue(result)
        self.mock_connection.commit.assert_called_once()
    
    def test_update_user_no_changes(self):
        """Тест обновления без изменений"""
        result = self.db_service.update_user(1)
        
        self.assertFalse(result)
        self.mock_cursor.execute.assert_not_called()

# Тесты с патчингом
class FileProcessor:
    """Процессор файлов для демонстрации патчинга"""
    
    def read_config(self, filename: str) -> Dict[str, Any]:
        import json
        with open(filename, 'r') as file:
            return json.load(file)
    
    def save_data(self, data: Dict[str, Any], filename: str) -> bool:
        import json
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=2)
            return True
        except Exception:
            return False
    
    def process_file(self, input_file: str, output_file: str) -> bool:
        try:
            config = self.read_config(input_file)
            processed_data = {
                'processed_at': str(datetime.now()),
                'original_data': config,
                'processed': True
            }
            return self.save_data(processed_data, output_file)
        except Exception:
            return False

class TestFileProcessor(unittest.TestCase):
    """Тесты для FileProcessor с патчингом"""
    
    def setUp(self):
        self.processor = FileProcessor()
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, 
           read_data='{"key": "value", "number": 42}')
    @patch('json.load')
    def test_read_config(self, mock_json_load, mock_open):
        """Тест чтения конфигурации"""
        expected_config = {"key": "value", "number": 42}
        mock_json_load.return_value = expected_config
        
        result = self.processor.read_config("config.json")
        
        self.assertEqual(result, expected_config)
        mock_open.assert_called_once_with("config.json", 'r')
        mock_json_load.assert_called_once()
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_save_data_success(self, mock_json_dump, mock_open):
        """Тест успешного сохранения данных"""
        test_data = {"test": "data"}
        
        result = self.processor.save_data(test_data, "output.json")
        
        self.assertTrue(result)
        mock_open.assert_called_once_with("output.json", 'w')
        mock_json_dump.assert_called_once_with(test_data, mock_open.return_value, indent=2)
    
    @patch('builtins.open')
    def test_save_data_failure(self, mock_open):
        """Тест неудачного сохранения данных"""
        mock_open.side_effect = IOError("Permission denied")
        
        result = self.processor.save_data({"test": "data"}, "readonly.json")
        
        self.assertFalse(result)
    
    @patch.object(FileProcessor, 'save_data')
    @patch.object(FileProcessor, 'read_config')
    def test_process_file_success(self, mock_read_config, mock_save_data):
        """Тест успешной обработки файла"""
        mock_read_config.return_value = {"original": "data"}
        mock_save_data.return_value = True
        
        result = self.processor.process_file("input.json", "output.json")
        
        self.assertTrue(result)
        mock_read_config.assert_called_once_with("input.json")
        mock_save_data.assert_called_once()
        
        # Проверяем аргументы вызова save_data
        args, kwargs = mock_save_data.call_args
        processed_data = args[0]
        self.assertIn('processed_at', processed_data)
        self.assertIn('original_data', processed_data)
        self.assertTrue(processed_data['processed'])

# Кастомные assert методы
class CustomAssertions:
    """Кастомные методы для проверок"""
    
    def assertDictContainsSubset(self, subset: Dict[str, Any], dictionary: Dict[str, Any]):
        """Проверка, что словарь содержит подмножество"""
        for key, value in subset.items():
            if key not in dictionary:
                raise AssertionError(f"Key '{key}' not found in dictionary")
            if dictionary[key] != value:
                raise AssertionError(f"Value for key '{key}': expected {value}, got {dictionary[key]}")
    
    def assertAlmostEqualList(self, list1: List[float], list2: List[float], delta: float = 0.001):
        """Проверка приблизительного равенства списков чисел"""
        if len(list1) != len(list2):
            raise AssertionError(f"Lists have different lengths: {len(list1)} vs {len(list2)}")
        
        for i, (a, b) in enumerate(zip(list1, list2)):
            if abs(a - b) > delta:
                raise AssertionError(f"Lists differ at index {i}: {a} vs {b} (delta: {abs(a-b)})")

class TestWithCustomAssertions(unittest.TestCase, CustomAssertions):
    """Тест с кастомными проверками"""
    
    def test_dict_subset(self):
        """Тест проверки подмножества словаря"""
        full_dict = {"a": 1, "b": 2, "c": 3, "d": 4}
        subset = {"a": 1, "c": 3}
        
        self.assertDictContainsSubset(subset, full_dict)
    
    def test_almost_equal_lists(self):
        """Тест приблизительного равенства списков"""
        list1 = [1.001, 2.002, 3.003]
        list2 = [1.000, 2.000, 3.000]
        
        self.assertAlmostEqualList(list1, list2, delta=0.01)

# Параметризованные тесты в unittest
class ParametrizedTestCase(unittest.TestCase):
    """Параметризованные тесты в unittest"""
    
    def _test_add_operation(self, a, b, expected):
        """Базовый тест для операции сложения"""
        calc = Calculator()
        result = calc.add(a, b)
        self.assertEqual(result, expected, f"Failed for {a} + {b}")
    
    def test_add_operations(self):
        """Тест множественных операций сложения"""
        test_cases = [
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (10.5, 2.5, 13.0),
            (-5, -3, -8)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self._test_add_operation(a, b, expected)

# Test Suite и Runner
def create_test_suite():
    """Создание набора тестов"""
    suite = unittest.TestSuite()
    
    # Добавляем тесты
    suite.addTest(TestMathOperations('test_add_positive_numbers'))
    suite.addTest(TestMathOperations('test_divide_by_zero'))
    suite.addTest(TestDatabaseService('test_get_user_found'))
    suite.addTest(TestFileProcessor('test_read_config'))
    
    return suite

class VerboseTestResult(unittest.TextTestResult):
    """Кастомный результат теста с подробным выводом"""
    
    def startTest(self, test):
        super().startTest(test)
        print(f"\n🧪 Запуск теста: {test._testMethodName}")
    
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"✅ Успех: {test._testMethodName}")
    
    def addError(self, test, err):
        super().addError(test, err)
        print(f"❌ Ошибка: {test._testMethodName}")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"💥 Провал: {test._testMethodName}")

if __name__ == '__main__':
    # Запуск конкретного теста
    unittest.main(verbosity=2)
    
    # Или запуск custom suite
    # suite = create_test_suite()
    # runner = unittest.TextTestRunner(resultclass=VerboseTestResult, verbosity=2)
    # result = runner.run(suite)
```

---

## 🚀 pytest - современное тестирование

pytest - мощный и гибкий фреймворк тестирования с множеством возможностей.

### Основы pytest

```python
import pytest
from typing import List, Dict, Any, Generator
from unittest.mock import Mock, patch
import tempfile
import os
import json
from dataclasses import dataclass
from datetime import datetime, timedelta

# Простые тесты pytest
def test_simple_addition():
    """Простой тест сложения"""
    assert 2 + 2 == 4

def test_string_operations():
    """Тест строковых операций"""
    text = "Hello, World!"
    assert "Hello" in text
    assert text.startswith("Hello")
    assert text.endswith("!")
    assert len(text) == 13

def test_list_operations():
    """Тест операций со списками"""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert 3 in numbers
    assert max(numbers) == 5
    assert sum(numbers) == 15

# Классы для тестирования
@dataclass
class Product:
    """Продукт в интернет-магазине"""
    id: int
    name: str
    price: float
    category: str
    in_stock: bool = True
    quantity: int = 0
    
    def calculate_total(self, qty: int) -> float:
        if not self.in_stock or qty > self.quantity:
            raise ValueError("Product not available")
        return self.price * qty
    
    def apply_discount(self, discount_percent: float) -> float:
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        return self.price * (1 - discount_percent / 100)

class ShoppingCart:
    """Корзина покупок"""
    
    def __init__(self):
        self.items: List[Dict[str, Any]] = []
        self.discount_code: str = None
        self.discount_percent: float = 0
    
    def add_item(self, product: Product, quantity: int = 1):
        """Добавление товара в корзину"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if not product.in_stock or quantity > product.quantity:
            raise ValueError("Insufficient stock")
        
        # Проверяем, есть ли уже такой товар
        for item in self.items:
            if item['product'].id == product.id:
                item['quantity'] += quantity
                return
        
        self.items.append({
            'product': product,
            'quantity': quantity
        })
    
    def remove_item(self, product_id: int) -> bool:
        """Удаление товара из корзины"""
        for i, item in enumerate(self.items):
            if item['product'].id == product_id:
                del self.items[i]
                return True
        return False
    
    def update_quantity(self, product_id: int, new_quantity: int) -> bool:
        """Обновление количества товара"""
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        for item in self.items:
            if item['product'].id == product_id:
                if new_quantity == 0:
                    return self.remove_item(product_id)
                
                if new_quantity > item['product'].quantity:
                    raise ValueError("Insufficient stock")
                
                item['quantity'] = new_quantity
                return True
        return False
    
    def apply_discount_code(self, code: str) -> bool:
        """Применение промо-кода"""
        discount_codes = {
            'SAVE10': 10,
            'SAVE20': 20,
            'WELCOME5': 5
        }
        
        if code in discount_codes:
            self.discount_code = code
            self.discount_percent = discount_codes[code]
            return True
        return False
    
    def calculate_subtotal(self) -> float:
        """Расчет промежуточной суммы"""
        return sum(
            item['product'].price * item['quantity']
            for item in self.items
        )
    
    def calculate_total(self) -> float:
        """Расчет итоговой суммы с учетом скидки"""
        subtotal = self.calculate_subtotal()
        if self.discount_percent > 0:
            return subtotal * (1 - self.discount_percent / 100)
        return subtotal
    
    def get_item_count(self) -> int:
        """Общее количество товаров в корзине"""
        return sum(item['quantity'] for item in self.items)
    
    def clear(self):
        """Очистка корзины"""
        self.items.clear()
        self.discount_code = None
        self.discount_percent = 0

# Фикстуры pytest
@pytest.fixture
def sample_product():
    """Фикстура с образцом продукта"""
    return Product(
        id=1,
        name="Laptop",
        price=999.99,
        category="Electronics",
        in_stock=True,
        quantity=10
    )

@pytest.fixture
def multiple_products():
    """Фикстура с несколькими продуктами"""
    return [
        Product(1, "Laptop", 999.99, "Electronics", True, 5),
        Product(2, "Mouse", 29.99, "Electronics", True, 20),
        Product(3, "Keyboard", 79.99, "Electronics", True, 15),
        Product(4, "Monitor", 299.99, "Electronics", False, 0),
        Product(5, "Headphones", 149.99, "Electronics", True, 8)
    ]

@pytest.fixture
def empty_cart():
    """Фикстура с пустой корзиной"""
    return ShoppingCart()

@pytest.fixture
def cart_with_items(multiple_products):
    """Фикстура с корзиной, содержащей товары"""
    cart = ShoppingCart()
    cart.add_item(multiple_products[0], 1)  # Laptop
    cart.add_item(multiple_products[1], 2)  # Mouse x2
    return cart

@pytest.fixture(scope="session")
def test_database():
    """Фикстура базы данных для всей сессии"""
    # Создаем временную базу данных
    db_file = tempfile.NamedTemporaryFile(delete=False)
    db_path = db_file.name
    db_file.close()
    
    # Инициализация базы данных
    yield db_path
    
    # Очистка после тестов
    os.unlink(db_path)

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Автоматическая фикстура для настройки окружения"""
    # Настройка перед тестом
    original_env = os.environ.get('TEST_MODE')
    os.environ['TEST_MODE'] = 'true'
    
    yield
    
    # Очистка после теста
    if original_env is None:
        os.environ.pop('TEST_MODE', None)
    else:
        os.environ['TEST_MODE'] = original_env

# Тесты с фикстурами
class TestProduct:
    """Тесты для класса Product"""
    
    def test_product_creation(self, sample_product):
        """Тест создания продукта"""
        assert sample_product.id == 1
        assert sample_product.name == "Laptop"
        assert sample_product.price == 999.99
        assert sample_product.in_stock is True
    
    def test_calculate_total_valid(self, sample_product):
        """Тест расчета общей стоимости"""
        total = sample_product.calculate_total(2)
        assert total == 1999.98
    
    def test_calculate_total_insufficient_stock(self, sample_product):
        """Тест расчета при недостатке товара"""
        with pytest.raises(ValueError, match="Product not available"):
            sample_product.calculate_total(20)
    
    def test_calculate_total_out_of_stock(self):
        """Тест расчета для товара не в наличии"""
        product = Product(1, "Test", 100.0, "Test", False, 0)
        with pytest.raises(ValueError, match="Product not available"):
            product.calculate_total(1)
    
    def test_apply_discount_valid(self, sample_product):
        """Тест применения валидной скидки"""
        discounted_price = sample_product.apply_discount(10)
        assert discounted_price == 899.991  # 999.99 * 0.9
    
    def test_apply_discount_invalid(self, sample_product):
        """Тест применения невалидной скидки"""
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            sample_product.apply_discount(150)
        
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            sample_product.apply_discount(-10)

class TestShoppingCart:
    """Тесты для класса ShoppingCart"""
    
    def test_empty_cart_initialization(self, empty_cart):
        """Тест инициализации пустой корзины"""
        assert len(empty_cart.items) == 0
        assert empty_cart.calculate_total() == 0
        assert empty_cart.get_item_count() == 0
    
    def test_add_single_item(self, empty_cart, sample_product):
        """Тест добавления одного товара"""
        empty_cart.add_item(sample_product, 1)
        
        assert len(empty_cart.items) == 1
        assert empty_cart.items[0]['product'] == sample_product
        assert empty_cart.items[0]['quantity'] == 1
        assert empty_cart.get_item_count() == 1
    
    def test_add_multiple_same_items(self, empty_cart, sample_product):
        """Тест добавления нескольких одинаковых товаров"""
        empty_cart.add_item(sample_product, 2)
        empty_cart.add_item(sample_product, 3)
        
        assert len(empty_cart.items) == 1
        assert empty_cart.items[0]['quantity'] == 5
        assert empty_cart.get_item_count() == 5
    
    def test_add_different_items(self, empty_cart, multiple_products):
        """Тест добавления разных товаров"""
        empty_cart.add_item(multiple_products[0], 1)
        empty_cart.add_item(multiple_products[1], 2)
        
        assert len(empty_cart.items) == 2
        assert empty_cart.get_item_count() == 3
    
    def test_add_item_invalid_quantity(self, empty_cart, sample_product):
        """Тест добавления товара с невалидным количеством"""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            empty_cart.add_item(sample_product, 0)
        
        with pytest.raises(ValueError, match="Quantity must be positive"):
            empty_cart.add_item(sample_product, -1)
    
    def test_add_item_insufficient_stock(self, empty_cart, sample_product):
        """Тест добавления товара при недостатке на складе"""
        with pytest.raises(ValueError, match="Insufficient stock"):
            empty_cart.add_item(sample_product, 20)
    
    def test_remove_item_existing(self, cart_with_items):
        """Тест удаления существующего товара"""
        initial_count = len(cart_with_items.items)
        result = cart_with_items.remove_item(1)  # Laptop
        
        assert result is True
        assert len(cart_with_items.items) == initial_count - 1
    
    def test_remove_item_nonexistent(self, cart_with_items):
        """Тест удаления несуществующего товара"""
        result = cart_with_items.remove_item(999)
        assert result is False
    
    def test_update_quantity_valid(self, cart_with_items):
        """Тест обновления количества товара"""
        result = cart_with_items.update_quantity(1, 3)  # Laptop
        assert result is True
        
        laptop_item = next(item for item in cart_with_items.items 
                          if item['product'].id == 1)
        assert laptop_item['quantity'] == 3
    
    def test_update_quantity_to_zero(self, cart_with_items):
        """Тест обновления количества до нуля (удаление)"""
        initial_count = len(cart_with_items.items)
        result = cart_with_items.update_quantity(1, 0)
        
        assert result is True
        assert len(cart_with_items.items) == initial_count - 1
    
    def test_update_quantity_negative(self, cart_with_items):
        """Тест обновления количества на отрицательное значение"""
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            cart_with_items.update_quantity(1, -1)
    
    def test_apply_valid_discount_code(self, empty_cart):
        """Тест применения валидного промо-кода"""
        result = empty_cart.apply_discount_code('SAVE10')
        
        assert result is True
        assert empty_cart.discount_code == 'SAVE10'
        assert empty_cart.discount_percent == 10
    
    def test_apply_invalid_discount_code(self, empty_cart):
        """Тест применения невалидного промо-кода"""
        result = empty_cart.apply_discount_code('INVALID')
        
        assert result is False
        assert empty_cart.discount_code is None
        assert empty_cart.discount_percent == 0
    
    def test_calculate_subtotal(self, cart_with_items):
        """Тест расчета промежуточной суммы"""
        # Laptop (999.99 * 1) + Mouse (29.99 * 2) = 1059.97
        expected_subtotal = 999.99 + (29.99 * 2)
        assert cart_with_items.calculate_subtotal() == expected_subtotal
    
    def test_calculate_total_with_discount(self, cart_with_items):
        """Тест расчета итоговой суммы со скидкой"""
        cart_with_items.apply_discount_code('SAVE10')
        
        subtotal = cart_with_items.calculate_subtotal()
        expected_total = subtotal * 0.9  # 10% скидка
        
        assert cart_with_items.calculate_total() == expected_total
    
    def test_clear_cart(self, cart_with_items):
        """Тест очистки корзины"""
        cart_with_items.clear()
        
        assert len(cart_with_items.items) == 0
        assert cart_with_items.discount_code is None
        assert cart_with_items.discount_percent == 0
        assert cart_with_items.calculate_total() == 0

# Параметризованные тесты
@pytest.mark.parametrize("price,discount,expected", [
    (100.0, 10, 90.0),
    (50.0, 20, 40.0),
    (999.99, 5, 949.9905),
    (25.0, 0, 25.0),
    (200.0, 50, 100.0)
])
def test_discount_calculation(price, discount, expected):
    """Параметризованный тест расчета скидки"""
    product = Product(1, "Test", price, "Test", True, 10)
    result = product.apply_discount(discount)
    assert abs(result - expected) < 0.001

@pytest.mark.parametrize("code,expected_discount", [
    ('SAVE10', 10),
    ('SAVE20', 20),
    ('WELCOME5', 5),
    ('INVALID', 0)
])
def test_discount_codes(empty_cart, code, expected_discount):
    """Параметризованный тест промо-кодов"""
    result = empty_cart.apply_discount_code(code)
    
    if expected_discount > 0:
        assert result is True
        assert empty_cart.discount_percent == expected_discount
    else:
        assert result is False
        assert empty_cart.discount_percent == 0

# Маркеры и группировка тестов
@pytest.mark.slow
def test_expensive_operation():
    """Тест медленной операции"""
    import time
    time.sleep(0.1)  # Имитация медленной операции
    assert True

@pytest.mark.integration
def test_database_integration(test_database):
    """Интеграционный тест с базой данных"""
    # Имитация работы с базой данных
    assert os.path.exists(test_database)

@pytest.mark.unit
def test_unit_functionality():
    """Юнит-тест функциональности"""
    assert 2 + 2 == 4

@pytest.mark.skip(reason="Функция еще не реализована")
def test_future_feature():
    """Тест будущей функциональности"""
    pass

@pytest.mark.skipif(os.name == "nt", reason="Не запускается на Windows")
def test_unix_specific():
    """Тест специфичный для Unix систем"""
    assert True

# Тесты с исключениями
def test_exception_with_match():
    """Тест исключения с проверкой сообщения"""
    with pytest.raises(ValueError, match=r"Discount must be between.*"):
        product = Product(1, "Test", 100, "Test")
        product.apply_discount(150)

def test_exception_info():
    """Тест с получением информации об исключении"""
    with pytest.raises(ValueError) as exc_info:
        product = Product(1, "Test", 100, "Test")
        product.apply_discount(-10)
    
    assert "between 0 and 100" in str(exc_info.value)

# Моки в pytest
@patch('requests.get')
def test_api_call_mock(mock_get):
    """Тест API вызова с моком"""
    # Настройка мока
    mock_response = Mock()
    mock_response.json.return_value = {'status': 'success', 'data': 'test'}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    # Код, который тестируем
    import requests
    response = requests.get('https://api.example.com/data')
    data = response.json()
    
    # Проверки
    assert data['status'] == 'success'
    mock_get.assert_called_once_with('https://api.example.com/data')

# Временные файлы в тестах
def test_file_operations():
    """Тест операций с файлами"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('{"test": "data"}')
        tmp_path = tmp_file.name
    
    try:
        with open(tmp_path, 'r') as f:
            data = json.load(f)
        
        assert data['test'] == 'data'
    finally:
        os.unlink(tmp_path)

# Конфигурация pytest в conftest.py стиле
@pytest.fixture(autouse=True)
def reset_environment():
    """Сброс окружения перед каждым тестом"""
    # Сохраняем текущее состояние
    original_cwd = os.getcwd()
    
    yield
    
    # Восстанавливаем состояние
    os.chdir(original_cwd)

# Хуки pytest (обычно в conftest.py)
def pytest_runtest_setup(item):
    """Хук, выполняемый перед каждым тестом"""
    print(f"\n🏃 Подготовка к выполнению: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """Хук, выполняемый после каждого теста"""
    print(f"🧹 Очистка после: {item.name}")

# Кастомные маркеры
pytestmark = pytest.mark.shopping_cart  # Маркер для всего модуля

if __name__ == "__main__":
    # Запуск pytest программно
    pytest.main(["-v", "--tb=short", __file__])
```

Эта документация охватывает все основные аспекты тестирования в Python от базовых принципов до продвинутых техник с unittest и pytest. 