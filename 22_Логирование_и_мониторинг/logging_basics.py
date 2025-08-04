# Основы логирования в Python
import logging
import logging.config
import os
import sys
from datetime import datetime
from pathlib import Path

def demonstrate_basic_logging():
    """Демонстрация базового логирования"""
    print("=== Базовое логирование ===")
    
    # Базовая конфигурация
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Создание логгера
    logger = logging.getLogger(__name__)
    
    # Различные уровни логирования
    logger.debug("Это debug сообщение (не будет показано)")
    logger.info("Информационное сообщение")
    logger.warning("Предупреждение")
    logger.error("Ошибка")
    logger.critical("Критическая ошибка")
    
    print("\nУровни логирования по убыванию важности:")
    levels = [
        "CRITICAL (50) - Критические ошибки",
        "ERROR (40) - Ошибки",
        "WARNING (30) - Предупреждения", 
        "INFO (20) - Информационные сообщения",
        "DEBUG (10) - Отладочная информация"
    ]
    for level in levels:
        print(f"   {level}")

def demonstrate_logger_hierarchy():
    """Демонстрация иерархии логгеров"""
    print("\n=== Иерархия логгеров ===")
    
    # Корневой логгер
    root_logger = logging.getLogger()
    print(f"Корневой логгер: {root_logger.name}")
    
    # Дочерние логгеры
    app_logger = logging.getLogger('myapp')
    db_logger = logging.getLogger('myapp.database')
    api_logger = logging.getLogger('myapp.api')
    
    print(f"Приложение: {app_logger.name}")
    print(f"База данных: {db_logger.name}")
    print(f"API: {api_logger.name}")
    
    # Настройка уровней
    app_logger.setLevel(logging.INFO)
    db_logger.setLevel(logging.DEBUG)
    api_logger.setLevel(logging.WARNING)
    
    # Логирование с разных уровней
    app_logger.info("Приложение запущено")
    db_logger.debug("Подключение к базе данных")
    api_logger.warning("Медленный API запрос")
    
    print(f"\nИерархическое наследование:")
    print(f"   db_logger является дочерним для app_logger: {db_logger.parent == app_logger}")
    print(f"   app_logger является дочерним для root: {app_logger.parent == root_logger}")

def demonstrate_handlers():
    """Демонстрация различных обработчиков"""
    print("\n=== Обработчики (Handlers) ===")
    
    # Создаём логгер
    logger = logging.getLogger('handlers_demo')
    logger.setLevel(logging.DEBUG)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # 1. StreamHandler (консоль)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 2. FileHandler (файл)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(log_dir / "application.log")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # 3. RotatingFileHandler (ротация по размеру)
    from logging.handlers import RotatingFileHandler
    rotating_handler = RotatingFileHandler(
        log_dir / "rotating.log",
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    rotating_handler.setLevel(logging.ERROR)
    rotating_handler.setFormatter(file_formatter)
    logger.addHandler(rotating_handler)
    
    # Тестируем логирование
    logger.debug("Debug сообщение (только в файл)")
    logger.info("Info сообщение (консоль и файл)")
    logger.error("Error сообщение (консоль, файл и ротируемый файл)")
    
    print(f"Логи сохранены в папке: {log_dir.absolute()}")
    
    # Показываем информацию об обработчиках
    print(f"\nОбработчики для {logger.name}:")
    for i, handler in enumerate(logger.handlers, 1):
        print(f"   {i}. {type(handler).__name__} - уровень {handler.level}")

def demonstrate_formatters():
    """Демонстрация форматирования логов"""
    print("\n=== Форматирование логов ===")
    
    logger = logging.getLogger('formatter_demo')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # Различные форматы
    formats = {
        'simple': '%(levelname)s: %(message)s',
        'standard': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'detailed': '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
        'json_like': '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    }
    
    for format_name, format_string in formats.items():
        print(f"\n{format_name.upper()} формат:")
        
        # Создаём обработчик с форматом
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        
        # Временно добавляем обработчик
        logger.addHandler(handler)
        logger.info(f"Пример сообщения в {format_name} формате")
        logger.removeHandler(handler)

def demonstrate_configuration():
    """Демонстрация конфигурации через словарь"""
    print("\n=== Конфигурация через словарь ===")
    
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'error': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(filename)s:%(lineno)d)'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'error',
                'filename': 'logs/config_demo.log',
                'mode': 'a',
            }
        },
        'loggers': {
            'config_demo': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    }
    
    # Применяем конфигурацию
    logging.config.dictConfig(config)
    
    # Используем сконфигурированный логгер
    logger = logging.getLogger('config_demo')
    logger.debug("Отладочное сообщение")
    logger.info("Информационное сообщение")
    logger.error("Сообщение об ошибке")
    
    print("Логгер настроен через конфигурационный словарь")

def demonstrate_context_logging():
    """Демонстрация контекстного логирования"""
    print("\n=== Контекстное логирование ===")
    
    # Создаём кастомный фильтр для добавления контекста
    class ContextFilter(logging.Filter):
        def filter(self, record):
            record.user_id = getattr(self, 'user_id', 'anonymous')
            record.request_id = getattr(self, 'request_id', 'no-request')
            return True
    
    # Настраиваем логгер с контекстом
    logger = logging.getLogger('context_demo')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] [User:%(user_id)s] [Req:%(request_id)s] %(message)s'
    )
    handler.setFormatter(formatter)
    
    context_filter = ContextFilter()
    handler.addFilter(context_filter)
    logger.addHandler(handler)
    
    # Логирование без контекста
    logger.info("Сообщение без контекста")
    
    # Логирование с контекстом
    context_filter.user_id = "user123"
    context_filter.request_id = "req-456"
    logger.info("Сообщение с контекстом")
    logger.error("Ошибка в контексте пользователя")

def demonstrate_exception_logging():
    """Демонстрация логирования исключений"""
    print("\n=== Логирование исключений ===")
    
    logger = logging.getLogger('exception_demo')
    logger.setLevel(logging.DEBUG)
    
    # Убираем существующие обработчики
    logger.handlers.clear()
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    def divide_numbers(a, b):
        try:
            result = a / b
            logger.info(f"Деление {a} на {b} = {result}")
            return result
        except ZeroDivisionError:
            logger.error(f"Попытка деления на ноль: {a} / {b}", exc_info=True)
            raise
        except Exception as e:
            logger.exception(f"Неожиданная ошибка при делении {a} на {b}")
            raise
    
    # Тестируем логирование исключений
    try:
        divide_numbers(10, 2)  # Успешно
        divide_numbers(10, 0)  # Ошибка деления на ноль
    except ZeroDivisionError:
        logger.warning("Обработана ошибка деления на ноль")

def demonstrate_performance_logging():
    """Демонстрация логирования производительности"""
    print("\n=== Логирование производительности ===")
    
    import time
    import functools
    
    logger = logging.getLogger('performance')
    
    def log_execution_time(func):
        """Декоратор для логирования времени выполнения"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                logger.info(f"{func.__name__} выполнена за {execution_time:.4f} сек")
                return result
            except Exception as e:
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                logger.error(f"{func.__name__} завершилась с ошибкой за {execution_time:.4f} сек: {e}")
                raise
        return wrapper
    
    @log_execution_time
    def slow_function():
        """Медленная функция для демонстрации"""
        time.sleep(0.1)
        return "Результат"
    
    @log_execution_time 
    def fast_function():
        """Быстрая функция"""
        return sum(range(1000))
    
    # Тестируем
    slow_function()
    fast_function()

def demonstrate_log_levels_in_practice():
    """Демонстрация практического использования уровней логирования"""
    print("\n=== Практическое использование уровней ===")
    
    logger = logging.getLogger('practice')
    logger.setLevel(logging.DEBUG)
    
    def simulate_user_login(username, password):
        logger.debug(f"Попытка входа пользователя: {username}")
        
        if not username:
            logger.error("Пустое имя пользователя")
            return False
        
        if not password:
            logger.warning(f"Пустой пароль для пользователя {username}")
            return False
        
        # Имитация проверки пароля
        if password == "correct":
            logger.info(f"Успешный вход пользователя {username}")
            return True
        else:
            logger.warning(f"Неверный пароль для пользователя {username}")
            return False
    
    def simulate_critical_error():
        logger.critical("Критическая ошибка: база данных недоступна!")
    
    # Тестируем различные сценарии
    simulate_user_login("john", "correct")
    simulate_user_login("", "password")
    simulate_user_login("jane", "")
    simulate_user_login("bob", "wrong")
    simulate_critical_error()

def demonstrate_cleanup():
    """Очистка созданных файлов"""
    print("\n=== Очистка ===")
    
    log_dir = Path("logs")
    if log_dir.exists():
        for log_file in log_dir.glob("*.log*"):
            try:
                log_file.unlink()
                print(f"Удален файл: {log_file}")
            except Exception as e:
                print(f"Не удалось удалить {log_file}: {e}")
        
        try:
            log_dir.rmdir()
            print(f"Удалена папка: {log_dir}")
        except Exception as e:
            print(f"Не удалось удалить папку {log_dir}: {e}")

if __name__ == "__main__":
    print("Основы логирования в Python")
    print("=" * 50)
    
    demonstrate_basic_logging()
    demonstrate_logger_hierarchy()
    demonstrate_handlers()
    demonstrate_formatters()
    demonstrate_configuration()
    demonstrate_context_logging()
    demonstrate_exception_logging()
    demonstrate_performance_logging()
    demonstrate_log_levels_in_practice()
    
    print("\n=== Лучшие практики логирования ===")
    best_practices = [
        "1. Используйте правильные уровни логирования",
        "2. Включайте контекстную информацию",
        "3. Логируйте исключения с трассировкой",
        "4. Используйте структурированное логирование",
        "5. Настройте ротацию логов",
        "6. Не логируйте конфиденциальную информацию",
        "7. Используйте асинхронное логирование для высоконагруженных приложений",
        "8. Настройте централизованный сбор логов",
        "9. Мониторьте и анализируйте логи",
        "10. Тестируйте логирование в тестах"
    ]
    
    for practice in best_practices:
        print(f"   {practice}")
    
    print("\n=== Уровни логирования: когда использовать ===")
    when_to_use = {
        "DEBUG": "Детальная отладочная информация, обычно только в разработке",
        "INFO": "Общая информация о работе приложения",
        "WARNING": "Что-то неожиданное произошло, но приложение работает",
        "ERROR": "Серьёзная проблема, некоторая функциональность не работает",
        "CRITICAL": "Критическая ошибка, приложение может не работать"
    }
    
    for level, description in when_to_use.items():
        print(f"   {level}: {description}")
    
    # Очистка (раскомментируйте для удаления файлов)
    # demonstrate_cleanup()
    print(f"\nФайлы логов сохранены в папке logs/ для изучения")
    print("Для очистки запустите функцию demonstrate_cleanup()") 