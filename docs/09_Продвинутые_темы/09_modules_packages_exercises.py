#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Модули и пакеты в Python

Этот файл содержит практические упражнения для закрепления знаний:
- Создание модулей и пакетов
- Различные способы импорта
- Динамический импорт
- Система плагинов
- Организация кода
"""

import sys
import os
import tempfile
import shutil
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


def exercise_01_calculator_package():
    """
    Упражнение 1: Создание пакета калькулятора
    
    Задача:
    Создайте пакет calculator с модулями для различных операций:
    1. basic.py - базовые операции (+, -, *, /)
    2. advanced.py - продвинутые операции (степень, корень, логарифм)
    3. statistics.py - статистические функции
    4. history.py - история вычислений
    5. Настройте правильные импорты в __init__.py
    """
    print("=== Упражнение 1: Создание пакета калькулятора ===")
    
    # ЗАДАЧА: Создайте полноценный пакет калькулятора
    
    # РЕШЕНИЕ:
    
    temp_dir = tempfile.mkdtemp()
    sys.path.insert(0, temp_dir)
    
    try:
        # Создаем структуру пакета calculator
        calc_dir = os.path.join(temp_dir, "calculator")
        os.makedirs(calc_dir)
        
        print("1. Создание пакета calculator...")
        
        # calculator/__init__.py
        init_code = '''
"""
Пакет калькулятора с различными математическими операциями
"""

__version__ = "1.0.0"
__author__ = "Python Developer"

# Импортируем основные компоненты для удобного доступа
from .basic import BasicCalculator
from .advanced import AdvancedCalculator
from .statistics import StatisticsCalculator
from .history import CalculatorHistory

# Создаем единый интерфейс калькулятора
class Calculator(BasicCalculator, AdvancedCalculator, StatisticsCalculator):
    """Полнофункциональный калькулятор"""
    
    def __init__(self):
        self.history = CalculatorHistory()
        self._last_result = 0
    
    def _record_operation(self, operation, result):
        """Записать операцию в историю"""
        self.history.add_record(operation, result)
        self._last_result = result
        return result
    
    @property
    def last_result(self):
        """Последний результат"""
        return self._last_result

__all__ = ['Calculator', 'BasicCalculator', 'AdvancedCalculator', 
           'StatisticsCalculator', 'CalculatorHistory']
'''
        
        with open(os.path.join(calc_dir, "__init__.py"), 'w') as f:
            f.write(init_code)
        
        # calculator/basic.py
        basic_code = '''
"""
Базовые математические операции
"""

class BasicCalculator:
    """Базовый калькулятор"""
    
    def add(self, a, b):
        """Сложение"""
        result = a + b
        return self._record_operation(f"{a} + {b}", result)
    
    def subtract(self, a, b):
        """Вычитание"""
        result = a - b
        return self._record_operation(f"{a} - {b}", result)
    
    def multiply(self, a, b):
        """Умножение"""
        result = a * b
        return self._record_operation(f"{a} * {b}", result)
    
    def divide(self, a, b):
        """Деление"""
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        result = a / b
        return self._record_operation(f"{a} / {b}", result)
    
    def modulo(self, a, b):
        """Остаток от деления"""
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        result = a % b
        return self._record_operation(f"{a} % {b}", result)
    
    def _record_operation(self, operation, result):
        """Заглушка для записи операции (переопределяется в Calculator)"""
        return result
'''
        
        with open(os.path.join(calc_dir, "basic.py"), 'w') as f:
            f.write(basic_code)
        
        # calculator/advanced.py
        advanced_code = '''
"""
Продвинутые математические операции
"""

import math

class AdvancedCalculator:
    """Продвинутый калькулятор"""
    
    def power(self, base, exponent):
        """Возведение в степень"""
        result = base ** exponent
        return self._record_operation(f"{base} ^ {exponent}", result)
    
    def square_root(self, x):
        """Квадратный корень"""
        if x < 0:
            raise ValueError("Квадратный корень из отрицательного числа")
        result = math.sqrt(x)
        return self._record_operation(f"sqrt({x})", result)
    
    def nth_root(self, x, n):
        """N-й корень"""
        if n == 0:
            raise ValueError("Корень нулевой степени не определен")
        if x < 0 and n % 2 == 0:
            raise ValueError("Четный корень из отрицательного числа")
        
        result = x ** (1/n)
        return self._record_operation(f"{n}-root({x})", result)
    
    def logarithm(self, x, base=math.e):
        """Логарифм"""
        if x <= 0:
            raise ValueError("Логарифм от неположительного числа")
        if base <= 0 or base == 1:
            raise ValueError("Недопустимое основание логарифма")
        
        if base == math.e:
            result = math.log(x)
            return self._record_operation(f"ln({x})", result)
        elif base == 10:
            result = math.log10(x)
            return self._record_operation(f"log10({x})", result)
        else:
            result = math.log(x, base)
            return self._record_operation(f"log_{base}({x})", result)
    
    def factorial(self, n):
        """Факториал"""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Факториал определен только для неотрицательных целых чисел")
        
        result = math.factorial(n)
        return self._record_operation(f"{n}!", result)
    
    def sin(self, x, degrees=False):
        """Синус"""
        if degrees:
            x = math.radians(x)
        result = math.sin(x)
        unit = "°" if degrees else "rad"
        return self._record_operation(f"sin({x}{unit})", result)
    
    def cos(self, x, degrees=False):
        """Косинус"""
        if degrees:
            x = math.radians(x)
        result = math.cos(x)
        unit = "°" if degrees else "rad"
        return self._record_operation(f"cos({x}{unit})", result)
    
    def tan(self, x, degrees=False):
        """Тангенс"""
        if degrees:
            x = math.radians(x)
        result = math.tan(x)
        unit = "°" if degrees else "rad"
        return self._record_operation(f"tan({x}{unit})", result)
    
    def _record_operation(self, operation, result):
        """Заглушка для записи операции"""
        return result
'''
        
        with open(os.path.join(calc_dir, "advanced.py"), 'w') as f:
            f.write(advanced_code)
        
        # calculator/statistics.py
        statistics_code = '''
"""
Статистические функции
"""

import statistics
import math

class StatisticsCalculator:
    """Калькулятор статистических функций"""
    
    def mean(self, data):
        """Среднее арифметическое"""
        if not data:
            raise ValueError("Список данных не может быть пустым")
        result = statistics.mean(data)
        return self._record_operation(f"mean({len(data)} elements)", result)
    
    def median(self, data):
        """Медиана"""
        if not data:
            raise ValueError("Список данных не может быть пустым")
        result = statistics.median(data)
        return self._record_operation(f"median({len(data)} elements)", result)
    
    def mode(self, data):
        """Мода"""
        if not data:
            raise ValueError("Список данных не может быть пустым")
        try:
            result = statistics.mode(data)
            return self._record_operation(f"mode({len(data)} elements)", result)
        except statistics.StatisticsError as e:
            raise ValueError(f"Не удалось вычислить моду: {e}")
    
    def variance(self, data, sample=True):
        """Дисперсия"""
        if not data:
            raise ValueError("Список данных не может быть пустым")
        
        if sample:
            result = statistics.variance(data)
            op_type = "sample variance"
        else:
            result = statistics.pvariance(data)
            op_type = "population variance"
        
        return self._record_operation(f"{op_type}({len(data)} elements)", result)
    
    def standard_deviation(self, data, sample=True):
        """Стандартное отклонение"""
        if not data:
            raise ValueError("Список данных не может быть пустым")
        
        if sample:
            result = statistics.stdev(data)
            op_type = "sample stdev"
        else:
            result = statistics.pstdev(data)
            op_type = "population stdev"
        
        return self._record_operation(f"{op_type}({len(data)} elements)", result)
    
    def range_value(self, data):
        """Размах (разность между max и min)"""
        if not data:
            raise ValueError("Список данных не может быть пустым")
        result = max(data) - min(data)
        return self._record_operation(f"range({len(data)} elements)", result)
    
    def percentile(self, data, p):
        """Процентиль"""
        if not data:
            raise ValueError("Список данных не может быть пустым")
        if not 0 <= p <= 100:
            raise ValueError("Процентиль должен быть от 0 до 100")
        
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * p / 100
        f = math.floor(k)
        c = math.ceil(k)
        
        if f == c:
            result = sorted_data[int(k)]
        else:
            result = sorted_data[int(f)] * (c - k) + sorted_data[int(c)] * (k - f)
        
        return self._record_operation(f"{p}th percentile({len(data)} elements)", result)
    
    def _record_operation(self, operation, result):
        """Заглушка для записи операции"""
        return result
'''
        
        with open(os.path.join(calc_dir, "statistics.py"), 'w') as f:
            f.write(statistics_code)
        
        # calculator/history.py
        history_code = '''
"""
История вычислений калькулятора
"""

from datetime import datetime
from typing import List, Dict, Any

class CalculatorHistory:
    """Управление историей вычислений"""
    
    def __init__(self, max_records=100):
        self.max_records = max_records
        self._records = []
    
    def add_record(self, operation: str, result: Any):
        """Добавить запись в историю"""
        record = {
            'timestamp': datetime.now(),
            'operation': operation,
            'result': result
        }
        
        self._records.append(record)
        
        # Ограничиваем размер истории
        if len(self._records) > self.max_records:
            self._records.pop(0)
    
    def get_history(self, limit: int = None) -> List[Dict]:
        """Получить историю операций"""
        if limit is None:
            return self._records.copy()
        return self._records[-limit:]
    
    def get_last_operation(self) -> Dict:
        """Получить последнюю операцию"""
        if self._records:
            return self._records[-1]
        return None
    
    def get_operations_by_type(self, operation_type: str) -> List[Dict]:
        """Получить операции определенного типа"""
        return [record for record in self._records 
                if operation_type.lower() in record['operation'].lower()]
    
    def clear_history(self):
        """Очистить историю"""
        self._records.clear()
    
    def export_history(self, format='text') -> str:
        """Экспортировать историю"""
        if format == 'text':
            lines = []
            for i, record in enumerate(self._records, 1):
                timestamp = record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                lines.append(f"{i}. [{timestamp}] {record['operation']} = {record['result']}")
            return '\\n'.join(lines)
        
        elif format == 'json':
            import json
            # Сериализуем с обработкой datetime
            serializable_records = []
            for record in self._records:
                serializable_record = record.copy()
                serializable_record['timestamp'] = record['timestamp'].isoformat()
                serializable_records.append(serializable_record)
            return json.dumps(serializable_records, indent=2, ensure_ascii=False)
        
        else:
            raise ValueError(f"Неподдерживаемый формат: {format}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику по истории"""
        if not self._records:
            return {'total_operations': 0}
        
        # Подсчет операций по типам
        operation_counts = {}
        numeric_results = []
        
        for record in self._records:
            # Определяем тип операции
            operation = record['operation']
            if '+' in operation:
                op_type = 'addition'
            elif '-' in operation:
                op_type = 'subtraction'
            elif '*' in operation:
                op_type = 'multiplication'
            elif '/' in operation:
                op_type = 'division'
            elif '^' in operation:
                op_type = 'power'
            elif 'sqrt' in operation:
                op_type = 'square_root'
            elif 'log' in operation:
                op_type = 'logarithm'
            elif 'sin' in operation or 'cos' in operation or 'tan' in operation:
                op_type = 'trigonometric'
            elif 'mean' in operation or 'median' in operation:
                op_type = 'statistics'
            else:
                op_type = 'other'
            
            operation_counts[op_type] = operation_counts.get(op_type, 0) + 1
            
            # Собираем численные результаты
            if isinstance(record['result'], (int, float)):
                numeric_results.append(record['result'])
        
        stats = {
            'total_operations': len(self._records),
            'operation_types': operation_counts,
            'first_operation': self._records[0]['timestamp'].isoformat(),
            'last_operation': self._records[-1]['timestamp'].isoformat()
        }
        
        if numeric_results:
            stats['result_statistics'] = {
                'min': min(numeric_results),
                'max': max(numeric_results),
                'average': sum(numeric_results) / len(numeric_results)
            }
        
        return stats
    
    def __len__(self):
        return len(self._records)
    
    def __bool__(self):
        return len(self._records) > 0
'''
        
        with open(os.path.join(calc_dir, "history.py"), 'w') as f:
            f.write(history_code)
        
        print("2. Тестирование пакета калькулятора:")
        
        # Импортируем созданный пакет
        import calculator
        
        print(f"Версия пакета: {calculator.__version__}")
        print(f"Автор: {calculator.__author__}")
        
        # Создаем экземпляр калькулятора
        calc = calculator.Calculator()
        
        print("\n3. Тестирование базовых операций:")
        print(f"10 + 5 = {calc.add(10, 5)}")
        print(f"10 - 3 = {calc.subtract(10, 3)}")
        print(f"6 * 7 = {calc.multiply(6, 7)}")
        print(f"15 / 3 = {calc.divide(15, 3)}")
        print(f"17 % 5 = {calc.modulo(17, 5)}")
        
        print("\n4. Тестирование продвинутых операций:")
        print(f"2^10 = {calc.power(2, 10)}")
        print(f"sqrt(64) = {calc.square_root(64)}")
        print(f"3-root(27) = {calc.nth_root(27, 3)}")
        print(f"ln(e) = {calc.logarithm(2.718281828)}")
        print(f"5! = {calc.factorial(5)}")
        print(f"sin(30°) = {calc.sin(30, degrees=True)}")
        
        print("\n5. Тестирование статистических функций:")
        test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        print(f"Данные: {test_data}")
        print(f"Среднее: {calc.mean(test_data)}")
        print(f"Медиана: {calc.median(test_data)}")
        print(f"Дисперсия: {calc.variance(test_data)}")
        print(f"Стандартное отклонение: {calc.standard_deviation(test_data)}")
        print(f"Размах: {calc.range_value(test_data)}")
        print(f"75-й процентиль: {calc.percentile(test_data, 75)}")
        
        print("\n6. История вычислений:")
        print(f"Всего операций: {len(calc.history)}")
        print(f"Последний результат: {calc.last_result}")
        
        # Последние 5 операций
        recent_history = calc.history.get_history(5)
        print("\nПоследние 5 операций:")
        for i, record in enumerate(recent_history, 1):
            timestamp = record['timestamp'].strftime('%H:%M:%S')
            print(f"  {i}. [{timestamp}] {record['operation']} = {record['result']}")
        
        # Статистика по истории
        hist_stats = calc.history.get_statistics()
        print(f"\nСтатистика истории:")
        print(f"  Всего операций: {hist_stats['total_operations']}")
        print(f"  Типы операций: {hist_stats['operation_types']}")
        if 'result_statistics' in hist_stats:
            result_stats = hist_stats['result_statistics']
            print(f"  Результаты: min={result_stats['min']}, max={result_stats['max']}, avg={result_stats['average']:.2f}")
        
        print("\n7. Экспорт истории:")
        print("Экспорт в текстовом формате:")
        text_export = calc.history.export_history('text')
        print(text_export[:200] + "..." if len(text_export) > 200 else text_export)
        
        print("\n✅ Упражнение 1 завершено!")
        
    finally:
        # Очищаем
        sys.path.remove(temp_dir)
        shutil.rmtree(temp_dir)


def exercise_02_config_manager():
    """
    Упражнение 2: Система управления конфигурацией
    
    Задача:
    Создайте систему управления конфигурацией с поддержкой:
    1. Загрузки конфигурации из разных источников (JSON, YAML, ENV)
    2. Валидации конфигурации
    3. Горячей перезагрузки
    4. Конфигурации по умолчанию
    5. Профилей конфигурации (dev, test, prod)
    """
    print("=== Упражнение 2: Система управления конфигурацией ===")
    
    # ЗАДАЧА: Создайте гибкую систему конфигурации
    
    # РЕШЕНИЕ:
    
    temp_dir = tempfile.mkdtemp()
    sys.path.insert(0, temp_dir)
    
    try:
        # Создаем структуру пакета config_manager
        config_dir = os.path.join(temp_dir, "config_manager")
        os.makedirs(config_dir)
        
        print("1. Создание системы управления конфигурацией...")
        
        # config_manager/__init__.py
        init_code = '''
"""
Система управления конфигурацией
"""

from .manager import ConfigManager
from .loaders import JSONLoader, EnvLoader
from .validators import ConfigValidator
from .exceptions import ConfigError, ValidationError

__version__ = "2.0.0"

# Глобальный экземпляр менеджера конфигурации
config = ConfigManager()

__all__ = ['ConfigManager', 'config', 'JSONLoader', 'EnvLoader', 
           'ConfigValidator', 'ConfigError', 'ValidationError']
'''
        
        with open(os.path.join(config_dir, "__init__.py"), 'w') as f:
            f.write(init_code)
        
        # config_manager/exceptions.py
        exceptions_code = '''
"""
Исключения для системы конфигурации
"""

class ConfigError(Exception):
    """Базовое исключение конфигурации"""
    pass

class ValidationError(ConfigError):
    """Ошибка валидации конфигурации"""
    pass

class LoaderError(ConfigError):
    """Ошибка загрузчика конфигурации"""
    pass
'''
        
        with open(os.path.join(config_dir, "exceptions.py"), 'w') as f:
            f.write(exceptions_code)
        
        # config_manager/loaders.py
        loaders_code = '''
"""
Загрузчики конфигурации из различных источников
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any
from .exceptions import LoaderError

class ConfigLoader(ABC):
    """Базовый класс загрузчика конфигурации"""
    
    @abstractmethod
    def load(self, source: str) -> Dict[str, Any]:
        """Загрузить конфигурацию из источника"""
        pass
    
    @abstractmethod
    def can_handle(self, source: str) -> bool:
        """Проверить, может ли загрузчик обработать источник"""
        pass

class JSONLoader(ConfigLoader):
    """Загрузчик JSON конфигурации"""
    
    def load(self, source: str) -> Dict[str, Any]:
        """Загрузить конфигурацию из JSON файла"""
        try:
            with open(source, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise LoaderError(f"Файл конфигурации не найден: {source}")
        except json.JSONDecodeError as e:
            raise LoaderError(f"Ошибка парсинга JSON: {e}")
        except Exception as e:
            raise LoaderError(f"Ошибка загрузки конфигурации: {e}")
    
    def can_handle(self, source: str) -> bool:
        """Проверить расширение файла"""
        return source.endswith('.json')

class EnvLoader(ConfigLoader):
    """Загрузчик конфигурации из переменных окружения"""
    
    def __init__(self, prefix="APP_"):
        self.prefix = prefix
    
    def load(self, source: str = None) -> Dict[str, Any]:
        """Загрузить конфигурацию из переменных окружения"""
        config = {}
        
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                # Убираем префикс и преобразуем в нижний регистр
                config_key = key[len(self.prefix):].lower()
                
                # Пытаемся преобразовать типы
                config[config_key] = self._convert_value(value)
        
        return config
    
    def _convert_value(self, value: str) -> Any:
        """Преобразовать строковое значение в подходящий тип"""
        # Булевые значения
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        # Числа
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # JSON массивы/объекты
        if value.startswith(('[', '{')):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        
        # Строки
        return value
    
    def can_handle(self, source: str) -> bool:
        """Загрузчик окружения всегда может обработать запрос"""
        return True

class DictLoader(ConfigLoader):
    """Загрузчик из словаря (для тестирования)"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
    
    def load(self, source: str = None) -> Dict[str, Any]:
        """Вернуть предустановленные данные"""
        return self.data.copy()
    
    def can_handle(self, source: str) -> bool:
        return True
'''
        
        with open(os.path.join(config_dir, "loaders.py"), 'w') as f:
            f.write(loaders_code)
        
        # config_manager/validators.py
        validators_code = '''
"""
Валидаторы конфигурации
"""

from typing import Dict, Any, List, Callable
from .exceptions import ValidationError

class ConfigValidator:
    """Валидатор конфигурации"""
    
    def __init__(self):
        self.rules = {}
    
    def add_rule(self, key: str, validator: Callable[[Any], bool], 
                 error_message: str = None):
        """Добавить правило валидации"""
        self.rules[key] = {
            'validator': validator,
            'error_message': error_message or f"Ошибка валидации для {key}"
        }
    
    def validate(self, config: Dict[str, Any]) -> List[str]:
        """Валидировать конфигурацию"""
        errors = []
        
        for key, rule in self.rules.items():
            if key in config:
                try:
                    if not rule['validator'](config[key]):
                        errors.append(rule['error_message'])
                except Exception as e:
                    errors.append(f"Ошибка валидации {key}: {e}")
        
        return errors
    
    def validate_required(self, config: Dict[str, Any], 
                         required_keys: List[str]) -> List[str]:
        """Проверить обязательные ключи"""
        errors = []
        
        for key in required_keys:
            if key not in config:
                errors.append(f"Отсутствует обязательный параметр: {key}")
            elif config[key] is None:
                errors.append(f"Параметр {key} не может быть None")
        
        return errors

# Предустановленные валидаторы
def is_positive_int(value):
    """Проверить, что значение - положительное целое число"""
    return isinstance(value, int) and value > 0

def is_valid_port(value):
    """Проверить, что значение - валидный порт"""
    return isinstance(value, int) and 1 <= value <= 65535

def is_non_empty_string(value):
    """Проверить, что значение - непустая строка"""
    return isinstance(value, str) and len(value.strip()) > 0

def is_valid_log_level(value):
    """Проверить, что значение - валидный уровень логирования"""
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    return isinstance(value, str) and value.upper() in valid_levels

def is_valid_email(value):
    """Простая проверка email"""
    return isinstance(value, str) and '@' in value and '.' in value
'''
        
        with open(os.path.join(config_dir, "validators.py"), 'w') as f:
            f.write(validators_code)
        
        # config_manager/manager.py
        manager_code = '''
"""
Основной менеджер конфигурации
"""

import os
import json
from typing import Dict, Any, List, Optional
from .loaders import ConfigLoader, JSONLoader, EnvLoader
from .validators import ConfigValidator
from .exceptions import ConfigError, ValidationError

class ConfigManager:
    """Менеджер конфигурации"""
    
    def __init__(self):
        self._config = {}
        self._loaders = []
        self._validator = ConfigValidator()
        self._profiles = {}
        self._current_profile = 'default'
        self._defaults = {}
        
        # Регистрируем стандартные загрузчики
        self.register_loader(JSONLoader())
        self.register_loader(EnvLoader())
    
    def register_loader(self, loader: ConfigLoader):
        """Зарегистрировать загрузчик"""
        self._loaders.append(loader)
    
    def set_defaults(self, defaults: Dict[str, Any]):
        """Установить конфигурацию по умолчанию"""
        self._defaults = defaults.copy()
        self._merge_config(defaults)
    
    def load_from_source(self, source: str, profile: str = 'default'):
        """Загрузить конфигурацию из источника"""
        # Найти подходящий загрузчик
        loader = None
        for l in self._loaders:
            if l.can_handle(source):
                loader = l
                break
        
        if not loader:
            raise ConfigError(f"Не найден загрузчик для источника: {source}")
        
        # Загрузить конфигурацию
        config_data = loader.load(source)
        
        # Сохранить профиль
        self._profiles[profile] = config_data
        
        # Если это текущий профиль, применить его
        if profile == self._current_profile:
            self._merge_config(config_data)
        
        return config_data
    
    def load_from_dict(self, data: Dict[str, Any], profile: str = 'default'):
        """Загрузить конфигурацию из словаря"""
        self._profiles[profile] = data.copy()
        
        if profile == self._current_profile:
            self._merge_config(data)
    
    def switch_profile(self, profile: str):
        """Переключить профиль конфигурации"""
        if profile not in self._profiles:
            raise ConfigError(f"Профиль не найден: {profile}")
        
        self._current_profile = profile
        
        # Пересобрать конфигурацию
        self._config = self._defaults.copy()
        self._merge_config(self._profiles[profile])
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """Объединить новую конфигурацию с существующей"""
        self._config.update(new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получить значение конфигурации"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Установить значение конфигурации"""
        keys = key.split('.')
        config = self._config
        
        # Навигация до предпоследнего ключа
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Установка значения
        config[keys[-1]] = value
    
    def validate_config(self, required_keys: List[str] = None) -> bool:
        """Валидировать текущую конфигурацию"""
        errors = []
        
        # Проверка обязательных ключей
        if required_keys:
            errors.extend(self._validator.validate_required(self._config, required_keys))
        
        # Проверка правил валидации
        errors.extend(self._validator.validate(self._config))
        
        if errors:
            raise ValidationError(f"Ошибки валидации: {', '.join(errors)}")
        
        return True
    
    def add_validation_rule(self, key: str, validator, error_message: str = None):
        """Добавить правило валидации"""
        self._validator.add_rule(key, validator, error_message)
    
    def reload(self):
        """Перезагрузить конфигурацию"""
        if self._current_profile in self._profiles:
            # Сброс до defaults
            self._config = self._defaults.copy()
            # Применение текущего профиля
            self._merge_config(self._profiles[self._current_profile])
    
    def export_config(self, format: str = 'json') -> str:
        """Экспортировать конфигурацию"""
        if format == 'json':
            return json.dumps(self._config, indent=2, ensure_ascii=False)
        elif format == 'env':
            lines = []
            for key, value in self._flatten_dict(self._config).items():
                env_key = f"APP_{key.upper()}"
                lines.append(f"{env_key}={value}")
            return '\\n'.join(lines)
        else:
            raise ValueError(f"Неподдерживаемый формат: {format}")
    
    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Преобразовать вложенный словарь в плоский"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def get_all_config(self) -> Dict[str, Any]:
        """Получить всю конфигурацию"""
        return self._config.copy()
    
    def get_profiles(self) -> List[str]:
        """Получить список профилей"""
        return list(self._profiles.keys())
    
    def get_current_profile(self) -> str:
        """Получить текущий профиль"""
        return self._current_profile
    
    def clear(self):
        """Очистить конфигурацию"""
        self._config.clear()
        self._profiles.clear()
        self._current_profile = 'default'
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)
    
    def __contains__(self, key):
        return self.get(key) is not None
'''
        
        with open(os.path.join(config_dir, "manager.py"), 'w') as f:
            f.write(manager_code)
        
        print("2. Создание тестовых конфигурационных файлов...")
        
        # Создаем тестовые конфигурации
        configs_dir = os.path.join(temp_dir, "configs")
        os.makedirs(configs_dir)
        
        # config_dev.json
        dev_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "myapp_dev",
                "user": "dev_user",
                "debug": True
            },
            "server": {
                "host": "127.0.0.1",
                "port": 8000,
                "debug": True
            },
            "logging": {
                "level": "DEBUG",
                "file": "app_dev.log"
            },
            "features": {
                "new_ui": True,
                "analytics": False
            }
        }
        
        with open(os.path.join(configs_dir, "config_dev.json"), 'w') as f:
            json.dump(dev_config, f, indent=2)
        
        # config_prod.json
        prod_config = {
            "database": {
                "host": "prod-db.example.com",
                "port": 5432,
                "name": "myapp_prod",
                "user": "prod_user",
                "debug": False
            },
            "server": {
                "host": "0.0.0.0",
                "port": 80,
                "debug": False
            },
            "logging": {
                "level": "ERROR",
                "file": "app_prod.log"
            },
            "features": {
                "new_ui": False,
                "analytics": True
            }
        }
        
        with open(os.path.join(configs_dir, "config_prod.json"), 'w') as f:
            json.dump(prod_config, f, indent=2)
        
        print("3. Тестирование системы конфигурации...")
        
        # Импортируем созданный пакет
        import config_manager
        from config_manager.validators import is_positive_int, is_valid_port, is_non_empty_string
        
        # Создаем менеджер конфигурации
        config = config_manager.ConfigManager()
        
        print(f"Версия пакета: {config_manager.__version__}")
        
        # Устанавливаем конфигурацию по умолчанию
        defaults = {
            "app_name": "MyApplication",
            "version": "1.0.0",
            "database": {
                "timeout": 30,
                "pool_size": 10
            },
            "server": {
                "workers": 4
            }
        }
        
        config.set_defaults(defaults)
        print("Конфигурация по умолчанию установлена")
        
        # Добавляем правила валидации
        config.add_validation_rule(
            "database.port", 
            is_valid_port, 
            "Порт базы данных должен быть от 1 до 65535"
        )
        config.add_validation_rule(
            "server.port", 
            is_valid_port, 
            "Порт сервера должен быть от 1 до 65535"
        )
        config.add_validation_rule(
            "database.name", 
            is_non_empty_string, 
            "Имя базы данных не может быть пустым"
        )
        
        print("Правила валидации добавлены")
        
        # Загружаем конфигурацию для разработки
        dev_config_path = os.path.join(configs_dir, "config_dev.json")
        config.load_from_source(dev_config_path, "development")
        
        print("\\n4. Тестирование конфигурации для разработки:")
        print(f"Имя приложения: {config.get('app_name')}")
        print(f"База данных: {config.get('database.host')}:{config.get('database.port')}")
        print(f"Сервер: {config.get('server.host')}:{config.get('server.port')}")
        print(f"Уровень логирования: {config.get('logging.level')}")
        print(f"Отладка включена: {config.get('database.debug')}")
        
        # Валидация
        try:
            config.validate_config(['database.host', 'server.port'])
            print("✅ Конфигурация валидна")
        except config_manager.ValidationError as e:
            print(f"❌ Ошибка валидации: {e}")
        
        # Загружаем производственную конфигурацию
        prod_config_path = os.path.join(configs_dir, "config_prod.json")
        config.load_from_source(prod_config_path, "production")
        
        print("\\n5. Переключение на производственную конфигурацию:")
        config.switch_profile("production")
        
        print(f"Текущий профиль: {config.get_current_profile()}")
        print(f"База данных: {config.get('database.host')}:{config.get('database.port')}")
        print(f"Сервер: {config.get('server.host')}:{config.get('server.port')}")
        print(f"Уровень логирования: {config.get('logging.level')}")
        print(f"Отладка включена: {config.get('database.debug')}")
        
        # Тестирование переменных окружения
        print("\\n6. Тестирование загрузки из переменных окружения:")
        
        # Симулируем переменные окружения
        test_env = {
            "APP_DATABASE_HOST": "env-db.example.com",
            "APP_DATABASE_PORT": "3306",
            "APP_SERVER_DEBUG": "false",
            "APP_FEATURES_BETA": "true"
        }
        
        # Временно устанавливаем переменные окружения
        original_env = {}
        for key, value in test_env.items():
            original_env[key] = os.environ.get(key)
            os.environ[key] = value
        
        try:
            config.load_from_source("", "environment")
            config.switch_profile("environment")
            
            print(f"Database host из ENV: {config.get('database_host')}")
            print(f"Database port из ENV: {config.get('database_port')}")
            print(f"Server debug из ENV: {config.get('server_debug')}")
            print(f"Features beta из ENV: {config.get('features_beta')}")
            
        finally:
            # Восстанавливаем переменные окружения
            for key, value in original_env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        
        print("\\n7. Экспорт конфигурации:")
        
        # Переключаемся обратно на dev
        config.switch_profile("development")
        
        # JSON экспорт
        json_export = config.export_config('json')
        print("JSON экспорт (первые 200 символов):")
        print(json_export[:200] + "..." if len(json_export) > 200 else json_export)
        
        print(f"\\nДоступные профили: {config.get_profiles()}")
        print(f"Текущий профиль: {config.get_current_profile()}")
        
        print("\\n✅ Упражнение 2 завершено!")
        
    finally:
        # Очищаем
        sys.path.remove(temp_dir)
        shutil.rmtree(temp_dir)


def exercise_03_plugin_framework():
    """
    Упражнение 3: Фреймворк плагинов для текстовой обработки
    
    Задача:
    Создайте фреймворк плагинов для обработки текста с:
    1. Базовым интерфейсом плагина
    2. Системой регистрации плагинов
    3. Цепочкой обработки (pipeline)
    4. Конфигурацией плагинов
    5. Горячей загрузкой/выгрузкой плагинов
    """
    print("=== Упражнение 3: Фреймворк плагинов для текстовой обработки ===")
    
    # ЗАДАЧА: Создайте гибкий фреймворк плагинов
    
    # РЕШЕНИЕ:
    
    temp_dir = tempfile.mkdtemp()
    plugins_dir = os.path.join(temp_dir, "plugins")
    os.makedirs(plugins_dir)
    sys.path.insert(0, temp_dir)
    
    try:
        print("1. Создание базового интерфейса плагина...")
        
        # Базовые интерфейсы
        base_code = '''
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class TextProcessor(ABC):
    """Базовый интерфейс для плагинов обработки текста"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Имя плагина"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Версия плагина"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Описание плагина"""
        pass
    
    @abstractmethod
    def process(self, text: str, **kwargs) -> str:
        """Обработать текст"""
        pass
    
    def configure(self, config: Dict[str, Any]):
        """Настроить плагин (опционально)"""
        pass
    
    def initialize(self):
        """Инициализация плагина (опционально)"""
        pass
    
    def cleanup(self):
        """Очистка ресурсов (опционально)"""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Получить информацию о плагине"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'type': self.__class__.__name__
        }

class PluginManager:
    """Менеджер плагинов"""
    
    def __init__(self):
        self.plugins = {}
        self.pipeline = []
        self.configurations = {}
    
    def register_plugin(self, plugin: TextProcessor, config: Dict = None):
        """Зарегистрировать плагин"""
        if config:
            plugin.configure(config)
            self.configurations[plugin.name] = config
        
        plugin.initialize()
        self.plugins[plugin.name] = plugin
        print(f"Плагин {plugin.name} зарегистрирован")
    
    def unregister_plugin(self, name: str):
        """Отменить регистрацию плагина"""
        if name in self.plugins:
            self.plugins[name].cleanup()
            del self.plugins[name]
            if name in self.configurations:
                del self.configurations[name]
            # Удаляем из pipeline
            self.pipeline = [p for p in self.pipeline if p != name]
            print(f"Плагин {name} удален")
    
    def get_plugin(self, name: str) -> Optional[TextProcessor]:
        """Получить плагин по имени"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[str]:
        """Список зарегистрированных плагинов"""
        return list(self.plugins.keys())
    
    def create_pipeline(self, plugin_names: List[str]):
        """Создать pipeline обработки"""
        # Проверяем, что все плагины существуют
        for name in plugin_names:
            if name not in self.plugins:
                raise ValueError(f"Плагин {name} не найден")
        
        self.pipeline = plugin_names
        print(f"Pipeline создан: {' -> '.join(plugin_names)}")
    
    def process_text(self, text: str, **kwargs) -> str:
        """Обработать текст через pipeline"""
        result = text
        
        for plugin_name in self.pipeline:
            plugin = self.plugins[plugin_name]
            result = plugin.process(result, **kwargs)
        
        return result
    
    def process_with_plugin(self, text: str, plugin_name: str, **kwargs) -> str:
        """Обработать текст конкретным плагином"""
        if plugin_name not in self.plugins:
            raise ValueError(f"Плагин {plugin_name} не найден")
        
        return self.plugins[plugin_name].process(text, **kwargs)
    
    def get_pipeline_info(self) -> List[Dict[str, Any]]:
        """Получить информацию о pipeline"""
        return [self.plugins[name].get_info() for name in self.pipeline]
'''
        
        base_path = os.path.join(temp_dir, "text_processing_framework.py")
        with open(base_path, 'w') as f:
            f.write(base_code)
        
        print("2. Создание плагинов...")
        
        # Плагин удаления лишних пробелов
        cleanup_plugin = '''
import re
import sys
sys.path.append('{}')
from text_processing_framework import TextProcessor

class WhitespaceCleanupPlugin(TextProcessor):
    """Плагин очистки пробелов"""
    
    def __init__(self):
        self.remove_multiple_spaces = True
        self.remove_trailing_spaces = True
        self.normalize_newlines = True
    
    @property
    def name(self) -> str:
        return "whitespace_cleanup"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Очищает лишние пробелы и нормализует текст"
    
    def configure(self, config):
        """Настройка плагина"""
        self.remove_multiple_spaces = config.get('remove_multiple_spaces', True)
        self.remove_trailing_spaces = config.get('remove_trailing_spaces', True)
        self.normalize_newlines = config.get('normalize_newlines', True)
    
    def process(self, text: str, **kwargs) -> str:
        """Очистить текст от лишних пробелов"""
        result = text
        
        if self.remove_multiple_spaces:
            # Заменяем множественные пробелы на одинарные
            result = re.sub(r'[ ]{{2,}}', ' ', result)
        
        if self.remove_trailing_spaces:
            # Удаляем пробелы в начале и конце строк
            lines = result.split('\\n')
            lines = [line.strip() for line in lines]
            result = '\\n'.join(lines)
        
        if self.normalize_newlines:
            # Заменяем множественные переносы строк
            result = re.sub(r'\\n{{3,}}', '\\n\\n', result)
        
        return result
'''.format(temp_dir)
        
        with open(os.path.join(plugins_dir, "cleanup_plugin.py"), 'w') as f:
            f.write(cleanup_plugin)
        
        # Плагин форматирования
        format_plugin = '''
import sys
sys.path.append('{}')
from text_processing_framework import TextProcessor

class TextFormatterPlugin(TextProcessor):
    """Плагин форматирования текста"""
    
    def __init__(self):
        self.case_transform = None  # 'upper', 'lower', 'title', 'capitalize'
        self.add_line_numbers = False
        self.wrap_width = None
    
    @property
    def name(self) -> str:
        return "text_formatter"
    
    @property
    def version(self) -> str:
        return "1.1.0"
    
    @property
    def description(self) -> str:
        return "Форматирует текст: регистр, нумерация строк, перенос"
    
    def configure(self, config):
        """Настройка плагина"""
        self.case_transform = config.get('case_transform')
        self.add_line_numbers = config.get('add_line_numbers', False)
        self.wrap_width = config.get('wrap_width')
    
    def process(self, text: str, **kwargs) -> str:
        """Форматировать текст"""
        result = text
        
        # Преобразование регистра
        if self.case_transform == 'upper':
            result = result.upper()
        elif self.case_transform == 'lower':
            result = result.lower()
        elif self.case_transform == 'title':
            result = result.title()
        elif self.case_transform == 'capitalize':
            result = result.capitalize()
        
        # Добавление номеров строк
        if self.add_line_numbers:
            lines = result.split('\\n')
            numbered_lines = []
            for i, line in enumerate(lines, 1):
                numbered_lines.append(f"{i:3d}: {line}")
            result = '\\n'.join(numbered_lines)
        
        # Перенос строк
        if self.wrap_width and self.wrap_width > 0:
            lines = result.split('\\n')
            wrapped_lines = []
            for line in lines:
                if len(line) <= self.wrap_width:
                    wrapped_lines.append(line)
                else:
                    # Простой перенос по словам
                    words = line.split(' ')
                    current_line = ''
                    for word in words:
                        if len(current_line + ' ' + word) <= self.wrap_width:
                            current_line += (' ' + word) if current_line else word
                        else:
                            if current_line:
                                wrapped_lines.append(current_line)
                            current_line = word
                    if current_line:
                        wrapped_lines.append(current_line)
            result = '\\n'.join(wrapped_lines)
        
        return result
'''.format(temp_dir)
        
        with open(os.path.join(plugins_dir, "format_plugin.py"), 'w') as f:
            f.write(format_plugin)
        
        # Плагин замены текста
        replace_plugin = '''
import re
import sys
sys.path.append('{}')
from text_processing_framework import TextProcessor

class TextReplacePlugin(TextProcessor):
    """Плагин замены текста"""
    
    def __init__(self):
        self.replacements = []  # List of (pattern, replacement, use_regex)
        self.case_sensitive = True
    
    @property
    def name(self) -> str:
        return "text_replace"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Заменяет текст по шаблонам и регулярным выражениям"
    
    def configure(self, config):
        """Настройка плагина"""
        self.replacements = config.get('replacements', [])
        self.case_sensitive = config.get('case_sensitive', True)
    
    def process(self, text: str, **kwargs) -> str:
        """Выполнить замены в тексте"""
        result = text
        
        for replacement in self.replacements:
            if len(replacement) >= 2:
                pattern = replacement[0]
                replacement_text = replacement[1]
                use_regex = replacement[2] if len(replacement) > 2 else False
                
                if use_regex:
                    flags = 0 if self.case_sensitive else re.IGNORECASE
                    result = re.sub(pattern, replacement_text, result, flags=flags)
                else:
                    if self.case_sensitive:
                        result = result.replace(pattern, replacement_text)
                    else:
                        # Замена без учета регистра
                        def replace_case_insensitive(text, old, new):
                            index = 0
                            while True:
                                index = text.lower().find(old.lower(), index)
                                if index == -1:
                                    break
                                text = text[:index] + new + text[index + len(old):]
                                index += len(new)
                            return text
                        
                        result = replace_case_insensitive(result, pattern, replacement_text)
        
        return result
'''.format(temp_dir)
        
        with open(os.path.join(plugins_dir, "replace_plugin.py"), 'w') as f:
            f.write(replace_plugin)
        
        print("3. Тестирование фреймворка плагинов...")
        
        # Импортируем фреймворк
        sys.path.append(temp_dir)
        from text_processing_framework import PluginManager
        
        # Загружаем плагины динамически
        def load_plugins_from_directory(plugin_dir, manager):
            """Загрузить плагины из директории"""
            for filename in os.listdir(plugin_dir):
                if filename.endswith('.py'):
                    plugin_path = os.path.join(plugin_dir, filename)
                    module_name = f"plugin_{filename[:-3]}"
                    
                    # Загружаем модуль
                    spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    
                    # Ищем классы плагинов
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            hasattr(attr, 'name') and 
                            hasattr(attr, 'process')):
                            try:
                                plugin_instance = attr()
                                manager.register_plugin(plugin_instance)
                            except Exception as e:
                                print(f"Ошибка создания плагина {attr_name}: {e}")
        
        # Создаем менеджер и загружаем плагины
        manager = PluginManager()
        load_plugins_from_directory(plugins_dir, manager)
        
        print(f"Загружено плагинов: {len(manager.list_plugins())}")
        print(f"Список плагинов: {manager.list_plugins()}")
        
        print("\\n4. Настройка плагинов...")
        
        # Настраиваем плагины
        cleanup_config = {
            'remove_multiple_spaces': True,
            'remove_trailing_spaces': True,
            'normalize_newlines': True
        }
        
        format_config = {
            'case_transform': 'title',
            'add_line_numbers': False,
            'wrap_width': 50
        }
        
        replace_config = {
            'replacements': [
                ('Python', 'Python 🐍', False),
                ('test', 'тест', False),
                (r'\\d+', '[ЧИСЛО]', True)  # Regex замена
            ],
            'case_sensitive': False
        }
        
        # Применяем конфигурации (перерегистрируем плагины)
        if 'whitespace_cleanup' in manager.plugins:
            cleanup_plugin = manager.get_plugin('whitespace_cleanup')
            cleanup_plugin.configure(cleanup_config)
        
        if 'text_formatter' in manager.plugins:
            format_plugin = manager.get_plugin('text_formatter')
            format_plugin.configure(format_config)
        
        if 'text_replace' in manager.plugins:
            replace_plugin = manager.get_plugin('text_replace')
            replace_plugin.configure(replace_config)
        
        print("Плагины настроены")
        
        print("\\n5. Создание pipeline обработки...")
        
        # Создаем pipeline
        pipeline_plugins = ['whitespace_cleanup', 'text_replace', 'text_formatter']
        available_plugins = [p for p in pipeline_plugins if p in manager.list_plugins()]
        
        if available_plugins:
            manager.create_pipeline(available_plugins)
            
            # Тестовый текст
            test_text = """
            This is a test    text with    multiple spaces.
            
            
            Python is great for    text processing.
            Numbers like 123 and 456 should be replaced.
            
                This line has trailing spaces.   
            """
            
            print("\\nИсходный текст:")
            print(repr(test_text))
            
            print("\\nОбработанный текст:")
            processed_text = manager.process_text(test_text)
            print(repr(processed_text))
            
            print("\\nОтображение обработанного текста:")
            print(processed_text)
            
            print("\\n6. Информация о pipeline:")
            pipeline_info = manager.get_pipeline_info()
            for i, info in enumerate(pipeline_info, 1):
                print(f"  {i}. {info['name']} v{info['version']}")
                print(f"     {info['description']}")
            
            print("\\n7. Тестирование отдельных плагинов:")
            
            # Тест только замены
            if 'text_replace' in manager.plugins:
                replace_result = manager.process_with_plugin(
                    "Python test with numbers 42 and 100", 
                    'text_replace'
                )
                print(f"Только замена: {replace_result}")
            
            # Тест только форматирования с номерами строк
            if 'text_formatter' in manager.plugins:
                format_plugin = manager.get_plugin('text_formatter')
                format_plugin.configure({'add_line_numbers': True, 'case_transform': 'upper'})
                
                format_result = manager.process_with_plugin(
                    "line one\\nline two\\nline three", 
                    'text_formatter'
                )
                print(f"Форматирование с номерами:\\n{format_result}")
        
        else:
            print("Не удалось создать pipeline - плагины не загружены")
        
        print("\\n✅ Упражнение 3 завершено!")
        
    finally:
        # Очищаем
        sys.path.remove(temp_dir)
        shutil.rmtree(temp_dir)


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Создание пакета калькулятора", exercise_01_calculator_package),
        ("Система управления конфигурацией", exercise_02_config_manager),
        ("Фреймворк плагинов для текстовой обработки", exercise_03_plugin_framework),
    ]
    
    print("📦 Упражнения: Модули и пакеты в Python")
    print("=" * 70)
    print("Эти упражнения помогут освоить:")
    print("- Создание структурированных пакетов")
    print("- Организацию кода в модули")
    print("- Динамический импорт")
    print("- Системы плагинов")
    print("- Управление конфигурацией")
    print("- Лучшие практики разработки")
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


if __name__ == "__main__":
    main() 