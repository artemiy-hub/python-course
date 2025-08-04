# Основы тестирования с unittest
import unittest
import sys
import os
from io import StringIO

# Код для тестирования
class Calculator:
    """Простой калькулятор для демонстрации тестирования"""
    
    def add(self, a, b):
        """Сложение двух чисел"""
        return a + b
    
    def subtract(self, a, b):
        """Вычитание"""
        return a - b
    
    def multiply(self, a, b):
        """Умножение"""
        return a * b
    
    def divide(self, a, b):
        """Деление"""
        if b == 0:
            raise ValueError("Деление на ноль запрещено")
        return a / b
    
    def power(self, base, exp):
        """Возведение в степень"""
        return base ** exp

class StringProcessor:
    """Класс для обработки строк"""
    
    def reverse(self, text):
        """Переворот строки"""
        if not isinstance(text, str):
            raise TypeError("Ожидается строка")
        return text[::-1]
    
    def capitalize_words(self, text):
        """Капитализация слов"""
        return ' '.join(word.capitalize() for word in text.split())
    
    def count_words(self, text):
        """Подсчёт слов"""
        if not text.strip():
            return 0
        return len(text.split())

# Базовые тесты с unittest
class TestCalculator(unittest.TestCase):
    """Тесты для класса Calculator"""
    
    def setUp(self):
        """Метод вызывается перед каждым тестом"""
        self.calc = Calculator()
        print(f"Запуск теста: {self._testMethodName}")
    
    def tearDown(self):
        """Метод вызывается после каждого теста"""
        print(f"Завершение теста: {self._testMethodName}")
    
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел"""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел"""
        result = self.calc.add(-2, -3)
        self.assertEqual(result, -5)
    
    def test_add_zero(self):
        """Тест сложения с нулём"""
        result = self.calc.add(5, 0)
        self.assertEqual(result, 5)
    
    def test_subtract(self):
        """Тест вычитания"""
        result = self.calc.subtract(10, 3)
        self.assertEqual(result, 7)
    
    def test_multiply(self):
        """Тест умножения"""
        result = self.calc.multiply(4, 5)
        self.assertEqual(result, 20)
    
    def test_divide(self):
        """Тест деления"""
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5.0)
    
    def test_divide_by_zero(self):
        """Тест деления на ноль (должно вызвать исключение)"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_power(self):
        """Тест возведения в степень"""
        result = self.calc.power(2, 3)
        self.assertEqual(result, 8)

class TestStringProcessor(unittest.TestCase):
    """Тесты для класса StringProcessor"""
    
    @classmethod
    def setUpClass(cls):
        """Метод вызывается один раз перед всеми тестами класса"""
        print("Инициализация тестов StringProcessor")
        cls.processor = StringProcessor()
    
    @classmethod
    def tearDownClass(cls):
        """Метод вызывается один раз после всех тестов класса"""
        print("Завершение тестов StringProcessor")
    
    def test_reverse_string(self):
        """Тест переворота строки"""
        result = self.processor.reverse("hello")
        self.assertEqual(result, "olleh")
    
    def test_reverse_empty_string(self):
        """Тест переворота пустой строки"""
        result = self.processor.reverse("")
        self.assertEqual(result, "")
    
    def test_reverse_invalid_input(self):
        """Тест переворота с неверным типом данных"""
        with self.assertRaises(TypeError):
            self.processor.reverse(123)
    
    def test_capitalize_words(self):
        """Тест капитализации слов"""
        result = self.processor.capitalize_words("hello world python")
        self.assertEqual(result, "Hello World Python")
    
    def test_count_words(self):
        """Тест подсчёта слов"""
        result = self.processor.count_words("hello world python")
        self.assertEqual(result, 3)
    
    def test_count_words_empty(self):
        """Тест подсчёта слов в пустой строке"""
        result = self.processor.count_words("")
        self.assertEqual(result, 0)
    
    def test_count_words_whitespace(self):
        """Тест подсчёта слов в строке с пробелами"""
        result = self.processor.count_words("   ")
        self.assertEqual(result, 0)

# Демонстрация различных assert методов
class TestAssertMethods(unittest.TestCase):
    """Демонстрация различных assert методов"""
    
    def test_equality_assertions(self):
        """Тесты на равенство"""
        self.assertEqual(1, 1)
        self.assertNotEqual(1, 2)
        self.assertAlmostEqual(1.1, 1.15, places=1)
        self.assertNotAlmostEqual(1.1, 1.2, places=1)
    
    def test_boolean_assertions(self):
        """Тесты булевых значений"""
        self.assertTrue(True)
        self.assertFalse(False)
        self.assertIsNone(None)
        self.assertIsNotNone("not none")
    
    def test_membership_assertions(self):
        """Тесты принадлежности"""
        self.assertIn(1, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])
    
    def test_type_assertions(self):
        """Тесты типов"""
        self.assertIsInstance(1, int)
        self.assertNotIsInstance("1", int)
    
    def test_regex_assertions(self):
        """Тесты регулярных выражений"""
        self.assertRegex("hello123", r"\w+\d+")
        self.assertNotRegex("hello", r"\d+")
    
    def test_collection_assertions(self):
        """Тесты коллекций"""
        list1 = [1, 2, 3]
        list2 = [3, 2, 1]
        self.assertListEqual(list1, [1, 2, 3])
        self.assertCountEqual(list1, list2)  # Порядок не важен
    
    def test_exception_assertions(self):
        """Тесты исключений"""
        with self.assertRaises(ZeroDivisionError):
            1 / 0
        
        with self.assertRaisesRegex(ValueError, "invalid literal"):
            int("not_a_number")

# Пропуск тестов
class TestSkippingExamples(unittest.TestCase):
    """Примеры пропуска тестов"""
    
    @unittest.skip("Этот тест пропускается")
    def test_skip_unconditional(self):
        """Безусловный пропуск теста"""
        self.fail("Этот тест не должен выполняться")
    
    @unittest.skipIf(sys.platform == "win32", "Не для Windows")
    def test_skip_if_windows(self):
        """Пропуск на Windows"""
        pass
    
    @unittest.skipUnless(sys.platform.startswith("linux"), "Только для Linux")
    def test_skip_unless_linux(self):
        """Выполнение только на Linux"""
        pass
    
    @unittest.expectedFailure
    def test_expected_failure(self):
        """Тест, который ожидаемо падает"""
        self.assertEqual(1, 2)

# Подтесты (subtests)
class TestSubtests(unittest.TestCase):
    """Демонстрация подтестов"""
    
    def test_even_numbers(self):
        """Тест чётных чисел с подтестами"""
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0, f"{i} не является чётным")

# Создание тестового набора
def create_test_suite():
    """Создание набора тестов"""
    suite = unittest.TestSuite()
    
    # Добавление отдельных тестов
    suite.addTest(TestCalculator('test_add_positive_numbers'))
    suite.addTest(TestCalculator('test_divide_by_zero'))
    
    # Добавление всех тестов из класса
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStringProcessor))
    
    return suite

# Кастомный TestResult для демонстрации
class CustomTestResult(unittest.TextTestResult):
    """Кастомный результат тестов"""
    
    def startTest(self, test):
        super().startTest(test)
        print(f"🟡 Начинаем: {test}")
    
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"✅ Успех: {test}")
    
    def addError(self, test, err):
        super().addError(test, err)
        print(f"❌ Ошибка: {test}")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"❌ Провал: {test}")

# Мок для демонстрации
class TestWithMocks(unittest.TestCase):
    """Простые примеры с моками"""
    
    def test_with_patch(self):
        """Тест с патчингом"""
        from unittest.mock import patch
        
        # Патчим встроенную функцию
        with patch('builtins.len') as mock_len:
            mock_len.return_value = 5
            result = len([1, 2, 3])
            self.assertEqual(result, 5)
            mock_len.assert_called_once_with([1, 2, 3])

# Запуск тестов программно
def run_tests_programmatically():
    """Программный запуск тестов"""
    print("=== Программный запуск тестов ===")
    
    # Создание тестового набора
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавление тестов
    suite.addTests(loader.loadTestsFromTestCase(TestCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestAssertMethods))
    
    # Запуск с кастомным результатом
    runner = unittest.TextTestRunner(verbosity=2, resultclass=CustomTestResult)
    result = runner.run(suite)
    
    # Статистика
    print(f"\nВыполнено тестов: {result.testsRun}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Провалов: {len(result.failures)}")
    print(f"Пропущено: {len(result.skipped)}")

# Демонстрация захвата вывода
class TestOutputCapture(unittest.TestCase):
    """Тестирование функций с выводом"""
    
    def test_print_function(self):
        """Тест функции с print"""
        from unittest.mock import patch
        
        def greeting(name):
            print(f"Привет, {name}!")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            greeting("Мир")
            self.assertEqual(fake_out.getvalue().strip(), "Привет, Мир!")

if __name__ == '__main__':
    print("Демонстрация unittest")
    print("=" * 50)
    
    # Разные способы запуска тестов
    
    # 1. Простой запуск всех тестов
    print("1. Запуск всех тестов:")
    # unittest.main(verbosity=2, exit=False)
    
    # 2. Программный запуск
    run_tests_programmatically()
    
    # 3. Запуск конкретного набора
    print("\n=== Запуск конкретного набора тестов ===")
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 4. Обнаружение тестов
    print("\n=== Автоматическое обнаружение тестов ===")
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir, pattern='*unittest_basics.py')
    
    print("\n=== Лучшие практики unittest ===")
    best_practices = [
        "1. Один assert на тест (когда возможно)",
        "2. Описательные имена тестов",
        "3. Использование setUp и tearDown для подготовки",
        "4. Тестирование граничных случаев",
        "5. Тестирование исключений",
        "6. Использование подтестов для параметризации",
        "7. Пропуск тестов при определённых условиях",
        "8. Изоляция тестов друг от друга"
    ]
    
    for practice in best_practices:
        print(f"   {practice}")
    
    print("\n=== Команды запуска ===")
    print("   python -m unittest test_module.py")
    print("   python -m unittest test_module.TestClass")
    print("   python -m unittest test_module.TestClass.test_method")
    print("   python -m unittest discover -s tests -p '*test*.py'")
    print("   python -m unittest -v  # подробный вывод") 