# Теория: Логирование и мониторинг в Python

## 🎯 Цель раздела

Этот раздел охватывает все аспекты логирования и мониторинга Python приложений: от базового логирования до продвинутых систем мониторинга, метрик и алертов.

## 📋 Содержание

1. [Основы логирования](#основы-логирования)
2. [Продвинутое логирование](#продвинутое-логирование)
3. [Структурированное логирование](#структурированное-логирование)
4. [Мониторинг и метрики](#мониторинг-и-метрики)
5. [Профилирование производительности](#профилирование-производительности)
6. [Система алертов](#система-алертов)
7. [Интеграция с внешними системами](#интеграция-с-внешними-системами)

---

## 📝 Основы логирования

Python предоставляет мощный встроенный модуль logging для записи событий приложения.

### Базовая настройка логирования

```python
import logging
import logging.handlers
import logging.config
from datetime import datetime
from typing import Any, Dict, Optional, List, Union
import json
import sys
import os
import traceback
from pathlib import Path
import threading
import queue
from dataclasses import dataclass, asdict
import time

class LoggingManager:
    """Менеджер для настройки логирования"""
    
    def __init__(self, app_name: str = "MyApp"):
        self.app_name = app_name
        self.loggers = {}
        self.handlers = {}
        self.formatters = {}
        
    def setup_basic_logging(self, level: str = "INFO", 
                          log_file: Optional[str] = None) -> logging.Logger:
        """Базовая настройка логирования"""
        
        # Настройка форматтера
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Создаем основной логгер
        logger = logging.getLogger(self.app_name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # Очищаем существующие обработчики
        logger.handlers.clear()
        
        # Консольный обработчик
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Файловый обработчик (если указан)
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Предотвращаем дублирование логов
        logger.propagate = False
        
        self.loggers['main'] = logger
        return logger
    
    def setup_advanced_logging(self, config: Dict[str, Any]) -> Dict[str, logging.Logger]:
        """Продвинутая настройка логирования"""
        
        loggers = {}
        
        # Создаем форматтеры
        for name, fmt_config in config.get('formatters', {}).items():
            formatter = logging.Formatter(
                fmt_config['format'],
                datefmt=fmt_config.get('datefmt', '%Y-%m-%d %H:%M:%S')
            )
            self.formatters[name] = formatter
        
        # Создаем обработчики
        for name, handler_config in config.get('handlers', {}).items():
            handler = self._create_handler(handler_config)
            
            if 'formatter' in handler_config:
                handler.setFormatter(self.formatters[handler_config['formatter']])
            
            if 'level' in handler_config:
                handler.setLevel(getattr(logging, handler_config['level'].upper()))
            
            self.handlers[name] = handler
        
        # Создаем логгеры
        for name, logger_config in config.get('loggers', {}).items():
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, logger_config['level'].upper()))
            
            # Очищаем существующие обработчики
            logger.handlers.clear()
            
            # Добавляем указанные обработчики
            for handler_name in logger_config.get('handlers', []):
                if handler_name in self.handlers:
                    logger.addHandler(self.handlers[handler_name])
            
            logger.propagate = logger_config.get('propagate', False)
            loggers[name] = logger
        
        self.loggers.update(loggers)
        return loggers
    
    def _create_handler(self, config: Dict[str, Any]) -> logging.Handler:
        """Создание обработчика логов"""
        handler_type = config['type']
        
        if handler_type == 'console':
            return logging.StreamHandler(sys.stdout)
        
        elif handler_type == 'file':
            return logging.FileHandler(config['filename'], encoding='utf-8')
        
        elif handler_type == 'rotating_file':
            return logging.handlers.RotatingFileHandler(
                config['filename'],
                maxBytes=config.get('maxBytes', 10 * 1024 * 1024),  # 10MB
                backupCount=config.get('backupCount', 5),
                encoding='utf-8'
            )
        
        elif handler_type == 'timed_rotating_file':
            return logging.handlers.TimedRotatingFileHandler(
                config['filename'],
                when=config.get('when', 'midnight'),
                interval=config.get('interval', 1),
                backupCount=config.get('backupCount', 30),
                encoding='utf-8'
            )
        
        elif handler_type == 'syslog':
            return logging.handlers.SysLogHandler(
                address=config.get('address', ('localhost', 514))
            )
        
        elif handler_type == 'smtp':
            return logging.handlers.SMTPHandler(
                mailhost=config['mailhost'],
                fromaddr=config['fromaddr'],
                toaddrs=config['toaddrs'],
                subject=config['subject'],
                credentials=config.get('credentials'),
                secure=config.get('secure')
            )
        
        else:
            raise ValueError(f"Неподдерживаемый тип обработчика: {handler_type}")
    
    def get_logger(self, name: str = 'main') -> logging.Logger:
        """Получение логгера по имени"""
        return self.loggers.get(name, logging.getLogger(name))
    
    def create_context_logger(self, context: Dict[str, Any]) -> 'ContextLogger':
        """Создание логгера с контекстом"""
        return ContextLogger(self.get_logger(), context)

class ContextLogger:
    """Логгер с автоматическим добавлением контекста"""
    
    def __init__(self, logger: logging.Logger, context: Dict[str, Any]):
        self.logger = logger
        self.context = context
    
    def _format_message(self, message: str) -> str:
        """Форматирование сообщения с контекстом"""
        context_str = " | ".join(f"{k}={v}" for k, v in self.context.items())
        return f"[{context_str}] {message}"
    
    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(self._format_message(message), *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        self.logger.info(self._format_message(message), *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(self._format_message(message), *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        self.logger.error(self._format_message(message), *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(self._format_message(message), *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        self.logger.exception(self._format_message(message), *args, **kwargs)

# Кастомные фильтры
class SensitiveDataFilter(logging.Filter):
    """Фильтр для скрытия чувствительных данных"""
    
    SENSITIVE_PATTERNS = [
        r'password["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
        r'token["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
        r'api_key["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
        r'secret["\']?\s*[:=]\s*["\']?([^"\'&\s]+)',
    ]
    
    def filter(self, record):
        """Фильтрация чувствительных данных"""
        import re
        
        # Обрабатываем сообщение
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            for pattern in self.SENSITIVE_PATTERNS:
                record.msg = re.sub(pattern, r'\1: ***HIDDEN***', record.msg, flags=re.IGNORECASE)
        
        # Обрабатываем аргументы
        if hasattr(record, 'args') and record.args:
            filtered_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    for pattern in self.SENSITIVE_PATTERNS:
                        arg = re.sub(pattern, r'\1: ***HIDDEN***', arg, flags=re.IGNORECASE)
                filtered_args.append(arg)
            record.args = tuple(filtered_args)
        
        return True

class PerformanceFilter(logging.Filter):
    """Фильтр для логирования производительности"""
    
    def __init__(self, min_duration: float = 0.1):
        super().__init__()
        self.min_duration = min_duration
    
    def filter(self, record):
        """Фильтрация по времени выполнения"""
        if hasattr(record, 'duration'):
            return record.duration >= self.min_duration
        return True

# Кастомные форматтеры
class JSONFormatter(logging.Formatter):
    """JSON форматтер для структурированного логирования"""
    
    def format(self, record):
        """Форматирование записи в JSON"""
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread': record.thread,
            'thread_name': record.threadName,
            'process': record.process,
        }
        
        # Добавляем exception info если есть
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Добавляем дополнительные поля
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'lineno', 'funcName', 'created', 
                          'msecs', 'relativeCreated', 'thread', 'threadName', 'processName',
                          'process', 'exc_info', 'exc_text', 'stack_info', 'getMessage']:
                log_entry[key] = value
        
        return json.dumps(log_entry, ensure_ascii=False)

class ColoredFormatter(logging.Formatter):
    """Цветной форматтер для консоли"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        """Цветное форматирование"""
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)

# Декораторы для логирования
def log_function_calls(logger: Optional[logging.Logger] = None, 
                      level: str = 'DEBUG',
                      include_args: bool = True,
                      include_result: bool = True):
    """Декоратор для логирования вызовов функций"""
    
    def decorator(func):
        nonlocal logger
        if logger is None:
            logger = logging.getLogger(func.__module__)
        
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__name__}"
            
            # Логируем вызов
            if include_args:
                args_str = ", ".join([repr(arg) for arg in args])
                kwargs_str = ", ".join([f"{k}={repr(v)}" for k, v in kwargs.items()])
                params_str = ", ".join(filter(None, [args_str, kwargs_str]))
                getattr(logger, level.lower())(f"Вызов {func_name}({params_str})")
            else:
                getattr(logger, level.lower())(f"Вызов {func_name}")
            
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Логируем результат
                if include_result:
                    getattr(logger, level.lower())(
                        f"Завершен {func_name}, результат: {repr(result)}, время: {duration:.3f}s"
                    )
                else:
                    getattr(logger, level.lower())(
                        f"Завершен {func_name}, время: {duration:.3f}s"
                    )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"Ошибка в {func_name}: {str(e)}, время: {duration:.3f}s",
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator

def log_exceptions(logger: Optional[logging.Logger] = None, 
                  reraise: bool = True):
    """Декоратор для логирования исключений"""
    
    def decorator(func):
        nonlocal logger
        if logger is None:
            logger = logging.getLogger(func.__module__)
        
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                func_name = f"{func.__module__}.{func.__name__}"
                logger.error(
                    f"Исключение в {func_name}: {type(e).__name__}: {str(e)}",
                    exc_info=True
                )
                
                if reraise:
                    raise
                return None
        
        return wrapper
    return decorator

class AsyncLogger:
    """Асинхронный логгер для высоконагруженных приложений"""
    
    def __init__(self, logger: logging.Logger, queue_size: int = 1000):
        self.logger = logger
        self.queue = queue.Queue(maxsize=queue_size)
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        self._shutdown = False
    
    def _worker(self):
        """Рабочий поток для обработки логов"""
        while not self._shutdown:
            try:
                record = self.queue.get(timeout=1)
                if record is None:  # Сигнал завершения
                    break
                self.logger.handle(record)
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Ошибка в AsyncLogger: {e}")
    
    def log(self, level: int, message: str, *args, **kwargs):
        """Асинхронная запись лога"""
        if not self._shutdown:
            record = self.logger.makeRecord(
                self.logger.name, level, "", 0, message, args, None, **kwargs
            )
            try:
                self.queue.put_nowait(record)
            except queue.Full:
                # Если очередь переполнена, логируем синхронно
                self.logger.handle(record)
    
    def debug(self, message: str, *args, **kwargs):
        self.log(logging.DEBUG, message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        self.log(logging.INFO, message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        self.log(logging.WARNING, message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        self.log(logging.ERROR, message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        self.log(logging.CRITICAL, message, *args, **kwargs)
    
    def shutdown(self):
        """Завершение работы асинхронного логгера"""
        self._shutdown = True
        self.queue.put(None)  # Сигнал завершения
        self.worker_thread.join(timeout=5)
```

---

## 📊 Структурированное логирование

Структурированное логирование обеспечивает машиночитаемый формат логов.

### Современное структурированное логирование

```python
import structlog
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
import json
import sys
import uuid
from contextvars import ContextVar
from dataclasses import dataclass
import traceback

# Контекстные переменные для отслеживания запросов
request_id: ContextVar[str] = ContextVar('request_id', default='')
user_id: ContextVar[str] = ContextVar('user_id', default='')
correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')

@dataclass
class LogContext:
    """Контекст логирования"""
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    correlation_id: Optional[str] = None
    component: Optional[str] = None
    operation: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {k: v for k, v in asdict(self).items() if v is not None}

class StructuredLoggingManager:
    """Менеджер структурированного логирования"""
    
    def __init__(self, app_name: str = "MyApp", environment: str = "production"):
        self.app_name = app_name
        self.environment = environment
        self.setup_structlog()
    
    def setup_structlog(self):
        """Настройка structlog"""
        
        # Процессоры для обработки событий лога
        processors = [
            # Добавляем timestamp
            structlog.processors.TimeStamper(fmt="ISO"),
            
            # Добавляем уровень лога
            structlog.stdlib.add_log_level,
            
            # Добавляем информацию о вызывающей функции
            structlog.processors.CallsiteParameterAdder(
                parameters=[structlog.processors.CallsiteParameter.FILENAME,
                           structlog.processors.CallsiteParameter.FUNC_NAME,
                           structlog.processors.CallsiteParameter.LINENO]
            ),
            
            # Добавляем контекст
            self._add_context_processor,
            
            # Добавляем метаданные приложения
            self._add_app_metadata_processor,
            
            # JSON сериализация
            structlog.processors.JSONRenderer(ensure_ascii=False)
        ]
        
        # Настраиваем structlog
        structlog.configure(
            processors=processors,
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    
    def _add_context_processor(self, logger, method_name, event_dict):
        """Процессор для добавления контекста"""
        # Добавляем контекстные переменные
        if request_id.get():
            event_dict['request_id'] = request_id.get()
        if user_id.get():
            event_dict['user_id'] = user_id.get()
        if correlation_id.get():
            event_dict['correlation_id'] = correlation_id.get()
        
        return event_dict
    
    def _add_app_metadata_processor(self, logger, method_name, event_dict):
        """Процессор для добавления метаданных приложения"""
        event_dict['app'] = self.app_name
        event_dict['environment'] = self.environment
        event_dict['level'] = method_name.upper()
        
        return event_dict
    
    def get_logger(self, name: str = None) -> structlog.BoundLogger:
        """Получение структурированного логгера"""
        if name:
            return structlog.get_logger(name)
        return structlog.get_logger()
    
    def create_request_logger(self, req_id: Optional[str] = None) -> 'RequestLogger':
        """Создание логгера для запроса"""
        if req_id is None:
            req_id = str(uuid.uuid4())
        
        return RequestLogger(self.get_logger(), req_id)

class RequestLogger:
    """Логгер для отслеживания запросов"""
    
    def __init__(self, logger: structlog.BoundLogger, req_id: str):
        self.logger = logger
        self.req_id = req_id
        self.start_time = datetime.now()
        
        # Устанавливаем контекст
        request_id.set(req_id)
    
    def info(self, event: str, **kwargs):
        """Информационное сообщение"""
        self.logger.info(event, **kwargs)
    
    def error(self, event: str, error: Optional[Exception] = None, **kwargs):
        """Сообщение об ошибке"""
        if error:
            kwargs['error_type'] = type(error).__name__
            kwargs['error_message'] = str(error)
            kwargs['traceback'] = traceback.format_exc()
        
        self.logger.error(event, **kwargs)
    
    def warning(self, event: str, **kwargs):
        """Предупреждение"""
        self.logger.warning(event, **kwargs)
    
    def debug(self, event: str, **kwargs):
        """Отладочное сообщение"""
        self.logger.debug(event, **kwargs)
    
    def log_request_start(self, method: str, url: str, **kwargs):
        """Логирование начала запроса"""
        self.logger.info(
            "request_started",
            method=method,
            url=url,
            **kwargs
        )
    
    def log_request_end(self, status_code: int, **kwargs):
        """Логирование завершения запроса"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        self.logger.info(
            "request_completed",
            status_code=status_code,
            duration=duration,
            **kwargs
        )
    
    def log_database_query(self, query: str, duration: float, **kwargs):
        """Логирование запроса к БД"""
        self.logger.info(
            "database_query",
            query=query[:200] + "..." if len(query) > 200 else query,
            duration=duration,
            **kwargs
        )
    
    def log_external_api_call(self, service: str, endpoint: str, 
                             status_code: int, duration: float, **kwargs):
        """Логирование вызова внешнего API"""
        self.logger.info(
            "external_api_call",
            service=service,
            endpoint=endpoint,
            status_code=status_code,
            duration=duration,
            **kwargs
        )

class MetricsLogger:
    """Логгер для метрик"""
    
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger
    
    def counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Логирование счетчика"""
        self.logger.info(
            "metric_counter",
            metric_name=name,
            metric_type="counter",
            value=value,
            tags=tags or {}
        )
    
    def gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Логирование калибра"""
        self.logger.info(
            "metric_gauge",
            metric_name=name,
            metric_type="gauge",
            value=value,
            tags=tags or {}
        )
    
    def histogram(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Логирование гистограммы"""
        self.logger.info(
            "metric_histogram",
            metric_name=name,
            metric_type="histogram",
            value=value,
            tags=tags or {}
        )
    
    def timing(self, name: str, duration: float, tags: Optional[Dict[str, str]] = None):
        """Логирование времени выполнения"""
        self.logger.info(
            "metric_timing",
            metric_name=name,
            metric_type="timing",
            duration=duration,
            tags=tags or {}
        )

class BusinessEventLogger:
    """Логгер для бизнес-событий"""
    
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger
    
    def user_action(self, action: str, user_id: str, **context):
        """Логирование действия пользователя"""
        self.logger.info(
            "user_action",
            event_type="user_action",
            action=action,
            user_id=user_id,
            **context
        )
    
    def business_process(self, process: str, status: str, **context):
        """Логирование бизнес-процесса"""
        self.logger.info(
            "business_process",
            event_type="business_process",
            process=process,
            status=status,
            **context
        )
    
    def security_event(self, event: str, severity: str, **context):
        """Логирование события безопасности"""
        self.logger.warning(
            "security_event",
            event_type="security",
            event=event,
            severity=severity,
            **context
        )
    
    def performance_event(self, component: str, metric: str, value: float, **context):
        """Логирование события производительности"""
        self.logger.info(
            "performance_event",
            event_type="performance",
            component=component,
            metric=metric,
            value=value,
            **context
        )

# Контекстный менеджер для логирования операций
class LoggedOperation:
    """Контекстный менеджер для логирования операций"""
    
    def __init__(self, logger: structlog.BoundLogger, operation: str, **context):
        self.logger = logger
        self.operation = operation
        self.context = context
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(
            "operation_started",
            operation=self.operation,
            **self.context
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(
                "operation_completed",
                operation=self.operation,
                duration=duration,
                status="success",
                **self.context
            )
        else:
            self.logger.error(
                "operation_failed",
                operation=self.operation,
                duration=duration,
                status="error",
                error_type=exc_type.__name__,
                error_message=str(exc_val),
                **self.context
            )

# Декораторы для структурированного логирования
def log_operation(operation: str, logger: Optional[structlog.BoundLogger] = None):
    """Декоратор для логирования операций"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = structlog.get_logger(func.__module__)
            
            with LoggedOperation(logger, operation):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

def log_performance(threshold: float = 1.0, logger: Optional[structlog.BoundLogger] = None):
    """Декоратор для логирования производительности"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = structlog.get_logger(func.__module__)
            
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                
                if duration > threshold:
                    logger.warning(
                        "slow_operation",
                        function=func.__name__,
                        duration=duration,
                        threshold=threshold
                    )
                
                return result
                
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                logger.error(
                    "operation_error",
                    function=func.__name__,
                    duration=duration,
                    error_type=type(e).__name__,
                    error_message=str(e)
                )
                raise
        
        return wrapper
    return decorator

def demonstrate_structured_logging():
    """Демонстрация структурированного логирования"""
    print("📊 Демонстрация структурированного логирования")
    print("=" * 50)
    
    # Настраиваем структурированное логирование
    logging_manager = StructuredLoggingManager("DemoApp", "development")
    
    # Создаем логгеры
    main_logger = logging_manager.get_logger("main")
    request_logger = logging_manager.create_request_logger()
    metrics_logger = MetricsLogger(main_logger)
    business_logger = BusinessEventLogger(main_logger)
    
    # Базовое логирование
    main_logger.info("Приложение запущено", version="1.0.0", pid=os.getpid())
    
    # Логирование запроса
    request_logger.log_request_start("GET", "/api/users")
    request_logger.log_database_query("SELECT * FROM users", 0.025)
    request_logger.log_request_end(200, response_size=1024)
    
    # Метрики
    metrics_logger.counter("requests_total", 1, {"method": "GET", "endpoint": "/api/users"})
    metrics_logger.timing("request_duration", 0.156, {"endpoint": "/api/users"})
    metrics_logger.gauge("active_connections", 42)
    
    # Бизнес-события
    business_logger.user_action("login", "user123", ip="192.168.1.1")
    business_logger.business_process("order_creation", "completed", order_id="order456")
    business_logger.security_event("failed_login_attempt", "medium", user="attacker", ip="10.0.0.1")
    
    # Использование контекстного менеджера
    with LoggedOperation(main_logger, "data_processing", batch_size=1000):
        time.sleep(0.1)  # Имитация обработки
    
    # Использование декораторов
    @log_operation("calculation")
    @log_performance(threshold=0.05)
    def complex_calculation(n: int) -> int:
        time.sleep(0.02)  # Имитация вычислений
        return sum(i * i for i in range(n))
    
    result = complex_calculation(100)
    
    print("✅ Структурированные логи созданы")
    return {
        'result': result,
        'logs_created': True
    }
```

---

## 📈 Мониторинг и метрики

Система мониторинга для отслеживания состояния приложения в реальном времени.

### Система метрик и мониторинга

```python
import time
import threading
import psutil
from collections import defaultdict, deque
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import statistics
import json
import asyncio
from abc import ABC, abstractmethod

@dataclass
class MetricPoint:
    """Точка метрики"""
    timestamp: datetime
    value: Union[int, float]
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class MetricSummary:
    """Сводка метрики"""
    name: str
    count: int
    min_value: float
    max_value: float
    mean: float
    median: float
    p95: float
    p99: float
    current: float
    tags: Dict[str, str] = field(default_factory=dict)

class MetricsCollector:
    """Коллектор метрик"""
    
    def __init__(self, max_points: int = 10000):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_points))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = defaultdict(float)
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()
        
        # Автоматический сбор системных метрик
        self.system_metrics_enabled = True
        self.system_metrics_thread = threading.Thread(target=self._collect_system_metrics, daemon=True)
        self.system_metrics_thread.start()
    
    def counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Увеличение счетчика"""
        with self.lock:
            key = self._make_key(name, tags)
            self.counters[key] += value
            self._add_point(name, self.counters[key], tags)
    
    def gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Установка значения калибра"""
        with self.lock:
            key = self._make_key(name, tags)
            self.gauges[key] = value
            self._add_point(name, value, tags)
    
    def histogram(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Добавление значения в гистограмму"""
        with self.lock:
            key = self._make_key(name, tags)
            self.histograms[key].append(value)
            # Ограничиваем размер гистограммы
            if len(self.histograms[key]) > 1000:
                self.histograms[key] = self.histograms[key][-1000:]
            self._add_point(name, value, tags)
    
    def timing(self, name: str, duration: float, tags: Optional[Dict[str, str]] = None):
        """Запись времени выполнения"""
        self.histogram(f"{name}_duration", duration, tags)
    
    def _make_key(self, name: str, tags: Optional[Dict[str, str]]) -> str:
        """Создание ключа метрики"""
        if not tags:
            return name
        
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}[{tag_str}]"
    
    def _add_point(self, name: str, value: Union[int, float], tags: Optional[Dict[str, str]]):
        """Добавление точки метрики"""
        point = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            tags=tags or {}
        )
        self.metrics[name].append(point)
    
    def _collect_system_metrics(self):
        """Сбор системных метрик"""
        while self.system_metrics_enabled:
            try:
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                self.gauge("system.cpu.usage", cpu_percent, {"unit": "percent"})
                
                # Память
                memory = psutil.virtual_memory()
                self.gauge("system.memory.usage", memory.percent, {"unit": "percent"})
                self.gauge("system.memory.available", memory.available, {"unit": "bytes"})
                self.gauge("system.memory.used", memory.used, {"unit": "bytes"})
                
                # Диск
                disk = psutil.disk_usage('/')
                self.gauge("system.disk.usage", (disk.used / disk.total) * 100, {"unit": "percent"})
                self.gauge("system.disk.free", disk.free, {"unit": "bytes"})
                
                # Сеть
                network = psutil.net_io_counters()
                self.counter("system.network.bytes_sent", network.bytes_sent, {"direction": "out"})
                self.counter("system.network.bytes_recv", network.bytes_recv, {"direction": "in"})
                
                # Процессы
                self.gauge("system.processes.count", len(psutil.pids()))
                
                time.sleep(10)  # Собираем системные метрики каждые 10 секунд
                
            except Exception as e:
                print(f"Ошибка сбора системных метрик: {e}")
                time.sleep(10)
    
    def get_metric_summary(self, name: str, tags: Optional[Dict[str, str]] = None) -> Optional[MetricSummary]:
        """Получение сводки метрики"""
        with self.lock:
            if name not in self.metrics:
                return None
            
            points = list(self.metrics[name])
            
            # Фильтруем по тегам если указаны
            if tags:
                points = [p for p in points if all(p.tags.get(k) == v for k, v in tags.items())]
            
            if not points:
                return None
            
            values = [p.value for p in points]
            
            return MetricSummary(
                name=name,
                count=len(values),
                min_value=min(values),
                max_value=max(values),
                mean=statistics.mean(values),
                median=statistics.median(values),
                p95=self._percentile(values, 95),
                p99=self._percentile(values, 99),
                current=values[-1],
                tags=tags or {}
            )
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Вычисление перцентиля"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        k = (len(sorted_values) - 1) * percentile / 100
        f = int(k)
        c = k - f
        
        if f == len(sorted_values) - 1:
            return sorted_values[f]
        
        return sorted_values[f] * (1 - c) + sorted_values[f + 1] * c
    
    def get_all_metrics(self) -> Dict[str, MetricSummary]:
        """Получение всех метрик"""
        summaries = {}
        
        for name in self.metrics.keys():
            summary = self.get_metric_summary(name)
            if summary:
                summaries[name] = summary
        
        return summaries
    
    def export_prometheus(self) -> str:
        """Экспорт метрик в формате Prometheus"""
        lines = []
        
        with self.lock:
            # Счетчики
            for key, value in self.counters.items():
                name, tags_str = self._parse_key(key)
                metric_name = f"{name}_total"
                if tags_str:
                    lines.append(f'{metric_name}{{{tags_str}}} {value}')
                else:
                    lines.append(f'{metric_name} {value}')
            
            # Калибры
            for key, value in self.gauges.items():
                name, tags_str = self._parse_key(key)
                if tags_str:
                    lines.append(f'{name}{{{tags_str}}} {value}')
                else:
                    lines.append(f'{name} {value}')
        
        return '\n'.join(lines)
    
    def _parse_key(self, key: str) -> tuple:
        """Парсинг ключа метрики"""
        if '[' in key:
            name, tags_part = key.split('[', 1)
            tags_str = tags_part.rstrip(']')
            return name, tags_str
        return key, ""

class HealthChecker:
    """Проверка здоровья системы"""
    
    def __init__(self):
        self.checks: Dict[str, Callable[[], bool]] = {}
        self.check_results: Dict[str, Dict[str, Any]] = {}
    
    def register_check(self, name: str, check_func: Callable[[], bool], 
                      description: str = "", timeout: float = 5.0):
        """Регистрация проверки здоровья"""
        self.checks[name] = {
            'func': check_func,
            'description': description,
            'timeout': timeout
        }
    
    def run_check(self, name: str) -> Dict[str, Any]:
        """Выполнение одной проверки"""
        if name not in self.checks:
            return {
                'name': name,
                'status': 'error',
                'message': 'Check not found',
                'timestamp': datetime.now().isoformat()
            }
        
        check_info = self.checks[name]
        start_time = time.time()
        
        try:
            # Выполняем проверку с таймаутом
            result = self._run_with_timeout(check_info['func'], check_info['timeout'])
            duration = time.time() - start_time
            
            return {
                'name': name,
                'status': 'healthy' if result else 'unhealthy',
                'message': check_info['description'],
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            duration = time.time() - start_time
            return {
                'name': name,
                'status': 'error',
                'message': str(e),
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            }
    
    def _run_with_timeout(self, func: Callable, timeout: float) -> bool:
        """Выполнение функции с таймаутом"""
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Health check timeout")
        
        # Устанавливаем таймаут только для Unix систем
        if hasattr(signal, 'alarm'):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(timeout))
        
        try:
            result = func()
            if hasattr(signal, 'alarm'):
                signal.alarm(0)  # Отменяем таймаут
            return result
        except TimeoutError:
            raise
        finally:
            if hasattr(signal, 'alarm'):
                signal.alarm(0)
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Выполнение всех проверок"""
        results = {}
        overall_status = 'healthy'
        
        for name in self.checks:
            result = self.run_check(name)
            results[name] = result
            
            if result['status'] != 'healthy':
                overall_status = 'unhealthy'
        
        return {
            'status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'checks': results
        }

class AlertManager:
    """Менеджер алертов"""
    
    def __init__(self):
        self.rules: List[Dict[str, Any]] = []
        self.active_alerts: Dict[str, Dict[str, Any]] = {}
        self.alert_handlers: List[Callable] = []
    
    def add_rule(self, name: str, condition: Callable[[Dict[str, Any]], bool], 
                severity: str = "warning", description: str = ""):
        """Добавление правила алерта"""
        self.rules.append({
            'name': name,
            'condition': condition,
            'severity': severity,
            'description': description
        })
    
    def add_alert_handler(self, handler: Callable[[Dict[str, Any]], None]):
        """Добавление обработчика алертов"""
        self.alert_handlers.append(handler)
    
    def check_alerts(self, metrics: Dict[str, MetricSummary]):
        """Проверка условий алертов"""
        current_time = datetime.now()
        
        for rule in self.rules:
            try:
                if rule['condition'](metrics):
                    # Алерт активен
                    if rule['name'] not in self.active_alerts:
                        # Новый алерт
                        alert = {
                            'name': rule['name'],
                            'severity': rule['severity'],
                            'description': rule['description'],
                            'started_at': current_time,
                            'last_seen': current_time,
                            'count': 1
                        }
                        
                        self.active_alerts[rule['name']] = alert
                        self._trigger_alert(alert)
                    else:
                        # Обновляем существующий алерт
                        self.active_alerts[rule['name']]['last_seen'] = current_time
                        self.active_alerts[rule['name']]['count'] += 1
                
                else:
                    # Алерт неактивен
                    if rule['name'] in self.active_alerts:
                        # Алерт разрешился
                        alert = self.active_alerts.pop(rule['name'])
                        alert['resolved_at'] = current_time
                        self._resolve_alert(alert)
                        
            except Exception as e:
                print(f"Ошибка проверки правила {rule['name']}: {e}")
    
    def _trigger_alert(self, alert: Dict[str, Any]):
        """Срабатывание алерта"""
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Ошибка обработчика алерта: {e}")
    
    def _resolve_alert(self, alert: Dict[str, Any]):
        """Разрешение алерта"""
        alert['action'] = 'resolved'
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Ошибка обработчика разрешения алерта: {e}")
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Получение активных алертов"""
        return list(self.active_alerts.values())

class MonitoringDashboard:
    """Простая панель мониторинга"""
    
    def __init__(self, metrics_collector: MetricsCollector, 
                 health_checker: HealthChecker, alert_manager: AlertManager):
        self.metrics_collector = metrics_collector
        self.health_checker = health_checker
        self.alert_manager = alert_manager
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Получение данных для панели"""
        metrics = self.metrics_collector.get_all_metrics()
        health = self.health_checker.run_all_checks()
        alerts = self.alert_manager.get_active_alerts()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'metrics': {name: asdict(summary) for name, summary in metrics.items()},
            'health': health,
            'alerts': alerts,
            'summary': {
                'total_metrics': len(metrics),
                'healthy_checks': sum(1 for check in health['checks'].values() 
                                    if check['status'] == 'healthy'),
                'total_checks': len(health['checks']),
                'active_alerts': len(alerts)
            }
        }
    
    def export_json(self) -> str:
        """Экспорт данных в JSON"""
        return json.dumps(self.get_dashboard_data(), ensure_ascii=False, indent=2)

def demonstrate_monitoring():
    """Демонстрация системы мониторинга"""
    print("📈 Демонстрация системы мониторинга")
    print("=" * 50)
    
    # Создаем компоненты мониторинга
    metrics = MetricsCollector()
    health = HealthChecker()
    alerts = AlertManager()
    dashboard = MonitoringDashboard(metrics, health, alerts)
    
    # Регистрируем проверки здоровья
    health.register_check("database", lambda: True, "Проверка БД")
    health.register_check("cache", lambda: True, "Проверка кэша")
    health.register_check("disk_space", lambda: psutil.disk_usage('/').percent < 90, "Проверка места на диске")
    
    # Добавляем правила алертов
    alerts.add_rule(
        "high_cpu",
        lambda m: 'system.cpu.usage' in m and m['system.cpu.usage'].current > 80,
        "critical",
        "Высокая загрузка CPU"
    )
    
    alerts.add_rule(
        "low_disk_space",
        lambda m: 'system.disk.usage' in m and m['system.disk.usage'].current > 85,
        "warning",
        "Мало места на диске"
    )
    
    # Добавляем обработчик алертов
    def alert_handler(alert):
        print(f"🚨 АЛЕРТ: {alert['name']} - {alert['description']}")
    
    alerts.add_alert_handler(alert_handler)
    
    # Генерируем тестовые метрики
    for i in range(10):
        metrics.counter("requests_total", 1, {"method": "GET"})
        metrics.timing("request_duration", 0.1 + i * 0.05)
        metrics.gauge("active_users", 100 + i * 10)
        time.sleep(0.1)
    
    # Проверяем алерты
    all_metrics = metrics.get_all_metrics()
    alerts.check_alerts(all_metrics)
    
    # Получаем данные панели
    dashboard_data = dashboard.get_dashboard_data()
    
    print(f"\n📊 Собрано метрик: {dashboard_data['summary']['total_metrics']}")
    print(f"🏥 Проверок здоровья: {dashboard_data['summary']['healthy_checks']}/{dashboard_data['summary']['total_checks']}")
    print(f"🚨 Активных алертов: {dashboard_data['summary']['active_alerts']}")
    
    # Показываем несколько ключевых метрик
    if 'requests_total' in all_metrics:
        req_metric = all_metrics['requests_total']
        print(f"📈 Запросы: {req_metric.count} (текущий: {req_metric.current})")
    
    if 'request_duration_duration' in all_metrics:
        dur_metric = all_metrics['request_duration_duration']
        print(f"⏱️  Время ответа: среднее={dur_metric.mean:.3f}s, p95={dur_metric.p95:.3f}s")
    
    return dashboard_data
```

Этот раздел представляет полную систему логирования и мониторинга, включая структурированное логирование, сбор метрик, проверки здоровья и систему алертов. 