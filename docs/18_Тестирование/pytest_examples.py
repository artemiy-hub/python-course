# Тестирование с pytest - современный подход
try:
    import pytest
except ImportError:
    print("pytest не установлен. Установите: pip install pytest")
    exit()

import sys
from typing import List
import tempfile
import os

# Код для тестирования
class BankAccount:
    """Банковский счёт для демонстрации тестирования"""
    
    def __init__(self, initial_balance: float = 0):
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self._balance = initial_balance
        self._transactions = []
    
    @property
    def balance(self) -> float:
        return self._balance
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма депозита должна быть положительной")
        self._balance += amount
        self._transactions.append(f"Депозит: +{amount}")
    
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
        self._transactions.append(f"Снятие: -{amount}")
    
    def get_transactions(self) -> List[str]:
        return self._transactions.copy()

class MathUtils:
    """Математические утилиты"""
    
    @staticmethod
    def factorial(n: int) -> int:
        if n < 0:
            raise ValueError("Факториал отрицательного числа не определён")
        if n == 0 or n == 1:
            return 1
        return n * MathUtils.factorial(n - 1)
    
    @staticmethod
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

# Базовые тесты с pytest
def test_bank_account_creation():
    """Тест создания банковского счёта"""
    account = BankAccount(100)
    assert account.balance == 100

def test_bank_account_default_balance():
    """Тест создания счёта с балансом по умолчанию"""
    account = BankAccount()
    assert account.balance == 0

def test_bank_account_negative_initial_balance():
    """Тест создания счёта с отрицательным балансом"""
    with pytest.raises(ValueError, match="Начальный баланс не может быть отрицательным"):
        BankAccount(-100)

def test_deposit():
    """Тест депозита"""
    account = BankAccount(100)
    account.deposit(50)
    assert account.balance == 150

def test_deposit_invalid_amount():
    """Тест депозита с неверной суммой"""
    account = BankAccount()
    with pytest.raises(ValueError):
        account.deposit(-10)
    with pytest.raises(ValueError):
        account.deposit(0)

def test_withdraw():
    """Тест снятия средств"""
    account = BankAccount(100)
    account.withdraw(30)
    assert account.balance == 70

def test_withdraw_insufficient_funds():
    """Тест снятия при недостатке средств"""
    account = BankAccount(50)
    with pytest.raises(ValueError, match="Недостаточно средств"):
        account.withdraw(100)

def test_transactions_tracking():
    """Тест отслеживания транзакций"""
    account = BankAccount(100)
    account.deposit(50)
    account.withdraw(20)
    
    transactions = account.get_transactions()
    assert len(transactions) == 2
    assert "Депозит: +50" in transactions
    assert "Снятие: -20" in transactions

# Параметризованные тесты
@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120)
])
def test_factorial(n, expected):
    """Параметризованный тест факториала"""
    assert MathUtils.factorial(n) == expected

@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (6, False),
    (7, True),
    (8, False),
    (9, False),
    (10, False),
    (11, True)
])
def test_is_prime(n, expected):
    """Параметризованный тест проверки простых чисел"""
    assert MathUtils.is_prime(n) == expected

@pytest.mark.parametrize("invalid_input", [-1, -5, -10])
def test_factorial_negative_input(invalid_input):
    """Тест факториала с отрицательными числами"""
    with pytest.raises(ValueError):
        MathUtils.factorial(invalid_input)

# Фикстуры
@pytest.fixture
def empty_account():
    """Фикстура пустого банковского счёта"""
    return BankAccount()

@pytest.fixture
def account_with_balance():
    """Фикстура счёта с начальным балансом"""
    return BankAccount(1000)

@pytest.fixture
def temp_file():
    """Фикстура временного файла"""
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)

# Тесты с фикстурами
def test_deposit_with_fixture(empty_account):
    """Тест депозита с использованием фикстуры"""
    empty_account.deposit(100)
    assert empty_account.balance == 100

def test_withdraw_with_fixture(account_with_balance):
    """Тест снятия с использованием фикстуры"""
    account_with_balance.withdraw(200)
    assert account_with_balance.balance == 800

def test_file_operations(temp_file):
    """Тест файловых операций с временным файлом"""
    with open(temp_file, 'w') as f:
        f.write("test content")
    
    with open(temp_file, 'r') as f:
        content = f.read()
    
    assert content == "test content"

# Фикстуры с областями видимости
@pytest.fixture(scope="session")
def session_data():
    """Фикстура уровня сессии"""
    print("Создание данных сессии")
    return {"session_id": "12345"}

@pytest.fixture(scope="module")
def module_data():
    """Фикстура уровня модуля"""
    print("Создание данных модуля")
    return {"module_name": "test_module"}

@pytest.fixture(scope="class")
def class_data():
    """Фикстура уровня класса"""
    print("Создание данных класса")
    return {"class_name": "TestClass"}

# Автоиспользуемые фикстуры
@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Автоматически используемая фикстура"""
    print("Настройка перед тестом")
    yield
    print("Очистка после теста")

# Классы тестов
class TestBankAccountClass:
    """Группировка тестов в класс"""
    
    def test_account_creation(self):
        account = BankAccount(500)
        assert account.balance == 500
    
    def test_multiple_operations(self):
        account = BankAccount(1000)
        account.deposit(200)
        account.withdraw(150)
        assert account.balance == 1050

# Маркировки тестов
@pytest.mark.slow
def test_time_consuming_operation():
    """Медленный тест"""
    import time
    time.sleep(0.1)  # Имитация медленной операции
    assert True

@pytest.mark.integration
def test_integration_example():
    """Интеграционный тест"""
    # Тест взаимодействия компонентов
    account1 = BankAccount(1000)
    account2 = BankAccount(500)
    
    # Перевод средств
    transfer_amount = 200
    account1.withdraw(transfer_amount)
    account2.deposit(transfer_amount)
    
    assert account1.balance == 800
    assert account2.balance == 700

@pytest.mark.skip(reason="Функция ещё не реализована")
def test_future_feature():
    """Тест будущей функции"""
    assert False

@pytest.mark.skipif(sys.platform == "win32", reason="Не для Windows")
def test_unix_specific():
    """Тест только для Unix систем"""
    assert True

@pytest.mark.xfail(reason="Известная ошибка")
def test_known_bug():
    """Тест с известной ошибкой"""
    assert 1 == 2

# Параметризация фикстур
@pytest.fixture(params=[0, 100, 1000])
def account_with_different_balances(request):
    """Фикстура с разными начальными балансами"""
    return BankAccount(request.param)

def test_account_creation_parameterized(account_with_different_balances):
    """Тест с параметризованной фикстурой"""
    account = account_with_different_balances
    assert account.balance >= 0

# Мониторинг и фикстуры для настройки
@pytest.fixture
def capture_stdout():
    """Фикстура для захвата stdout"""
    import io
    import contextlib
    
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        yield f

def test_print_output(capture_stdout):
    """Тест вывода print"""
    print("Hello, pytest!")
    output = capture_stdout.getvalue()
    assert "Hello, pytest!" in output

# Кастомные ассерты
def assert_account_balance_positive(account):
    """Кастомный ассерт для проверки положительного баланса"""
    assert account.balance >= 0, f"Баланс {account.balance} не может быть отрицательным"

def test_custom_assert():
    """Тест с кастомным ассертом"""
    account = BankAccount(100)
    assert_account_balance_positive(account)

# Тестирование исключений с дополнительной информацией
def test_exception_details():
    """Тест деталей исключения"""
    account = BankAccount()
    
    with pytest.raises(ValueError) as exc_info:
        account.withdraw(100)
    
    assert "Недостаточно средств" in str(exc_info.value)
    assert exc_info.type is ValueError

# Приблизительные сравнения
def test_approximate_values():
    """Тест приблизительных значений"""
    result = 0.1 + 0.2
    assert result == pytest.approx(0.3)
    
    # С допуском
    assert 1.001 == pytest.approx(1.0, abs=0.01)

# Условные фикстуры
@pytest.fixture
def database_connection():
    """Фикстура подключения к базе данных"""
    # Имитация подключения
    connection = {"connected": True, "db": "test_db"}
    yield connection
    # Очистка
    connection["connected"] = False

@pytest.mark.database
def test_with_database(database_connection):
    """Тест с базой данных"""
    assert database_connection["connected"] is True

# Конфигурация pytest через conftest.py (пример)
def pytest_configure(config):
    """Конфигурация pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "database: marks tests that require database"
    )

# Хуки pytest
def pytest_runtest_setup(item):
    """Хук вызывается перед каждым тестом"""
    print(f"Настройка для теста: {item.name}")

def pytest_runtest_teardown(item):
    """Хук вызывается после каждого теста"""
    print(f"Очистка после теста: {item.name}")

if __name__ == "__main__":
    # Программный запуск pytest
    print("Для запуска тестов используйте:")
    print("pytest pytest_examples.py")
    print("pytest -v  # подробный вывод")
    print("pytest -m slow  # только медленные тесты")
    print("pytest -k 'deposit'  # тесты содержащие 'deposit'")
    print("pytest --tb=short  # короткий traceback")
    print("pytest -x  # остановка на первой ошибке")
    print("pytest --pdb  # запуск отладчика при ошибке")
    
    print("\n=== Преимущества pytest ===")
    advantages = [
        "1. Простой синтаксис assert",
        "2. Мощные фикстуры",
        "3. Параметризация тестов",
        "4. Плагины и расширения",
        "5. Автоматическое обнаружение тестов",
        "6. Подробные сообщения об ошибках",
        "7. Маркировка и фильтрация тестов",
        "8. Лёгкая интеграция с CI/CD"
    ]
    
    for advantage in advantages:
        print(f"   {advantage}")
    
    # Запуск тестов программно (не рекомендуется в реальных проектах)
    pytest.main([__file__, "-v"]) 