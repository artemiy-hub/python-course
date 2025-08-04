"""
Упражнения: Логирование и мониторинг

Этот файл содержит практические упражнения для изучения логирования,
мониторинга производительности и системы оповещений в Python.
"""

import logging
import logging.handlers
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import traceback
import functools
import psutil
import queue
import sqlite3
from contextlib import contextmanager
import tempfile
from collections import defaultdict, deque
import pytest
import asyncio
import weakref

# =============================================================================
# Упражнение 1: Advanced Logging System
# =============================================================================

"""
ЗАДАНИЕ 1: Advanced Logging System

Создайте продвинутую систему логирования:

1. Класс AdvancedLogger с функциями:
   - Структурированное логирование (JSON)
   - Ротация логов по размеру и времени
   - Фильтрация логов по уровням и тегам
   - Асинхронное логирование
   - Интеграция с внешними системами

2. Middleware для веб-приложений:
   - Логирование HTTP запросов
   - Трассировка запросов (request tracing)
   - Корреляционные ID
   - Performance logging

3. Система метрик:
   - Счетчики событий
   - Гистограммы времени выполнения
   - Пользовательские метрики
   - Экспорт метрик в различные форматы
"""

# Ваш код здесь:
class AdvancedLogger:
    """Продвинутая система логирования"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        # TODO: Реализуйте инициализацию
        pass
    
    def log_with_context(self, level: str, message: str, **context):
        """Логирование с контекстом"""
        # TODO: Реализуйте метод
        pass
    
    def start_trace(self, operation: str) -> str:
        """Начало трассировки операции"""
        # TODO: Реализуйте метод
        pass
    
    def end_trace(self, trace_id: str, success: bool = True, **metadata):
        """Завершение трассировки"""
        # TODO: Реализуйте метод
        pass
    
    def add_filter(self, filter_func: Callable):
        """Добавление фильтра логов"""
        # TODO: Реализуйте метод
        pass

# Решение:
import uuid
import asyncio
from threading import local

class LogContext:
    """Контекст логирования для хранения данных запроса"""
    
    def __init__(self):
        self.data = local()
    
    def set(self, key: str, value: Any):
        """Установка значения в контекст"""
        if not hasattr(self.data, 'context'):
            self.data.context = {}
        self.data.context[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получение значения из контекста"""
        if not hasattr(self.data, 'context'):
            return default
        return self.data.context.get(key, default)
    
    def clear(self):
        """Очистка контекста"""
        if hasattr(self.data, 'context'):
            self.data.context.clear()
    
    def get_all(self) -> Dict[str, Any]:
        """Получение всего контекста"""
        if not hasattr(self.data, 'context'):
            return {}
        return self.data.context.copy()

class TraceManager:
    """Менеджер трассировки операций"""
    
    def __init__(self):
        self.active_traces = {}
        self.completed_traces = deque(maxlen=1000)
    
    def start_trace(self, operation: str, parent_trace_id: str = None) -> str:
        """Начало новой трассировки"""
        trace_id = str(uuid.uuid4())
        
        trace_data = {
            'trace_id': trace_id,
            'operation': operation,
            'parent_trace_id': parent_trace_id,
            'start_time': datetime.utcnow(),
            'end_time': None,
            'duration_ms': None,
            'success': None,
            'metadata': {},
            'logs': []
        }
        
        self.active_traces[trace_id] = trace_data
        return trace_id
    
    def end_trace(self, trace_id: str, success: bool = True, **metadata):
        """Завершение трассировки"""
        if trace_id not in self.active_traces:
            return False
        
        trace = self.active_traces[trace_id]
        trace['end_time'] = datetime.utcnow()
        trace['duration_ms'] = (trace['end_time'] - trace['start_time']).total_seconds() * 1000
        trace['success'] = success
        trace['metadata'].update(metadata)
        
        # Перемещаем в завершенные
        self.completed_traces.append(trace)
        del self.active_traces[trace_id]
        
        return True
    
    def add_log_to_trace(self, trace_id: str, log_record: Dict[str, Any]):
        """Добавление лога к трассировке"""
        if trace_id in self.active_traces:
            self.active_traces[trace_id]['logs'].append(log_record)
    
    def get_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """Получение трассировки"""
        if trace_id in self.active_traces:
            return self.active_traces[trace_id].copy()
        
        for trace in self.completed_traces:
            if trace['trace_id'] == trace_id:
                return trace.copy()
        
        return None

class MetricsCollector:
    """Сборщик метрик"""
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.histograms = defaultdict(list)
        self.gauges = {}
        self.last_reset = datetime.utcnow()
    
    def increment_counter(self, name: str, value: int = 1, tags: Dict[str, str] = None):
        """Увеличение счетчика"""
        key = self._make_key(name, tags)
        self.counters[key] += value
    
    def record_histogram(self, name: str, value: float, tags: Dict[str, str] = None):
        """Запись значения в гистограмму"""
        key = self._make_key(name, tags)
        self.histograms[key].append(value)
        
        # Ограничиваем размер гистограммы
        if len(self.histograms[key]) > 1000:
            self.histograms[key] = self.histograms[key][-500:]
    
    def set_gauge(self, name: str, value: float, tags: Dict[str, str] = None):
        """Установка значения gauge"""
        key = self._make_key(name, tags)
        self.gauges[key] = value
    
    def _make_key(self, name: str, tags: Dict[str, str] = None) -> str:
        """Создание ключа метрики"""
        if not tags:
            return name
        
        tag_str = ','.join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}[{tag_str}]"
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Получение сводки метрик"""
        summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'counters': dict(self.counters),
            'gauges': dict(self.gauges),
            'histograms': {}
        }
        
        # Статистика по гистограммам
        for key, values in self.histograms.items():
            if values:
                summary['histograms'][key] = {
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'avg': sum(values) / len(values),
                    'p50': self._percentile(values, 0.5),
                    'p95': self._percentile(values, 0.95),
                    'p99': self._percentile(values, 0.99)
                }
        
        return summary
    
    def _percentile(self, values: List[float], p: float) -> float:
        """Вычисление процентиля"""
        sorted_values = sorted(values)
        index = int(len(sorted_values) * p)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def reset_counters(self):
        """Сброс счетчиков"""
        self.counters.clear()
        self.last_reset = datetime.utcnow()

class AsyncLogHandler:
    """Асинхронный обработчик логов"""
    
    def __init__(self, max_queue_size: int = 10000):
        self.queue = asyncio.Queue(maxsize=max_queue_size)
        self.handlers = []
        self.running = False
        self.task = None
    
    def add_handler(self, handler):
        """Добавление обработчика"""
        self.handlers.append(handler)
    
    async def start(self):
        """Запуск асинхронной обработки"""
        self.running = True
        self.task = asyncio.create_task(self._process_logs())
    
    async def stop(self):
        """Остановка обработки"""
        self.running = False
        if self.task:
            await self.task
    
    async def log_async(self, log_record: Dict[str, Any]):
        """Асинхронное логирование"""
        try:
            await self.queue.put(log_record)
        except asyncio.QueueFull:
            # В реальном приложении можно сбросить старые записи
            pass
    
    async def _process_logs(self):
        """Обработка логов из очереди"""
        while self.running or not self.queue.empty():
            try:
                log_record = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                
                for handler in self.handlers:
                    try:
                        if asyncio.iscoroutinefunction(handler.handle):
                            await handler.handle(log_record)
                        else:
                            handler.handle(log_record)
                    except Exception as e:
                        print(f"Log handler error: {e}")
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                        print(f"Log processing error: {e}")

class AdvancedLoggerSolution:
    """Решение: Продвинутая система логирования"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        
        # Компоненты системы
        self.context = LogContext()
        self.trace_manager = TraceManager()
        self.metrics = MetricsCollector()
        self.async_handler = AsyncLogHandler()
        
        # Фильтры и обработчики
        self.filters = []
        self.handlers = []
        
        # Настройка базового логгера
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Настройка по умолчанию
        self._setup_default_handlers()
    
    def _setup_default_handlers(self):
        """Настройка обработчиков по умолчанию"""
        # JSON formatter
        formatter = JsonLogFormatter(self)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler с ротацией
        if self.config.get('log_file'):
            file_handler = logging.handlers.RotatingFileHandler(
                self.config['log_file'],
                maxBytes=self.config.get('max_bytes', 10*1024*1024),
                backupCount=self.config.get('backup_count', 5)
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def set_context(self, **kwargs):
        """Установка контекста"""
        for key, value in kwargs.items():
            self.context.set(key, value)
    
    def clear_context(self):
        """Очистка контекста"""
        self.context.clear()
    
    def log_with_context(self, level: str, message: str, **context):
        """Логирование с контекстом"""
        # Объединяем контекст
        full_context = self.context.get_all()
        full_context.update(context)
        
        # Создаем запись лога
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level.upper(),
            'logger': self.name,
            'message': message,
            'context': full_context
        }
        
        # Применяем фильтры
        for filter_func in self.filters:
            if not filter_func(log_record):
                return  # Лог отфильтрован
        
        # Обновляем метрики
        self.metrics.increment_counter('logs_total', tags={'level': level.upper()})
        
        # Добавляем к трассировке
        trace_id = self.context.get('trace_id')
        if trace_id:
            self.trace_manager.add_log_to_trace(trace_id, log_record)
        
        # Логируем через стандартный logger
        getattr(self.logger, level.lower())(message, extra={'structured_data': log_record})
    
    def start_trace(self, operation: str) -> str:
        """Начало трассировки операции"""
        parent_trace_id = self.context.get('trace_id')
        trace_id = self.trace_manager.start_trace(operation, parent_trace_id)
        
        # Устанавливаем trace_id в контекст
        self.context.set('trace_id', trace_id)
        
        self.log_with_context('info', f"Started operation: {operation}", 
                             trace_id=trace_id, operation=operation)
        
        return trace_id
    
    def end_trace(self, trace_id: str, success: bool = True, **metadata):
        """Завершение трассировки"""
        result = self.trace_manager.end_trace(trace_id, success, **metadata)
        
        if result:
            trace = self.trace_manager.get_trace(trace_id)
            if trace:
                self.log_with_context(
                    'info' if success else 'error',
                    f"Completed operation: {trace['operation']}",
                    trace_id=trace_id,
                    operation=trace['operation'],
                    duration_ms=trace['duration_ms'],
                    success=success,
                    **metadata
                )
                
                # Записываем метрику времени выполнения
                self.metrics.record_histogram(
                    'operation_duration_ms',
                    trace['duration_ms'],
                    tags={'operation': trace['operation'], 'success': str(success)}
                )
        
        return result
    
    def add_filter(self, filter_func: Callable):
        """Добавление фильтра логов"""
        self.filters.append(filter_func)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Получение метрик"""
        return self.metrics.get_metrics_summary()
    
    def info(self, message: str, **context):
        self.log_with_context('info', message, **context)
    
    def error(self, message: str, **context):
        self.log_with_context('error', message, **context)
    
    def warning(self, message: str, **context):
        self.log_with_context('warning', message, **context)
    
    def debug(self, message: str, **context):
        self.log_with_context('debug', message, **context)

class JsonLogFormatter(logging.Formatter):
    """JSON форматтер с поддержкой структурированных данных"""
    
    def __init__(self, advanced_logger):
        super().__init__()
        self.advanced_logger = advanced_logger
    
    def format(self, record):
        if hasattr(record, 'structured_data'):
            return json.dumps(record.structured_data)
        
        # Стандартное форматирование
        log_entry = {
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        return json.dumps(log_entry)

# Декораторы для трассировки
def trace_function(logger: AdvancedLoggerSolution, operation: str = None):
    """Декоратор для трассировки выполнения функций"""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation or f"{func.__module__}.{func.__name__}"
            trace_id = logger.start_trace(op_name)
            
            try:
                result = func(*args, **kwargs)
                logger.end_trace(trace_id, success=True)
                return result
            except Exception as e:
                logger.end_trace(trace_id, success=False, error=str(e))
                raise
        
        return wrapper
    return decorator

# Тесты для AdvancedLogger
class TestAdvancedLogger:
    """Тесты продвинутой системы логирования"""
    
    @pytest.fixture
    def logger(self):
        """Fixture логгера"""
        return AdvancedLoggerSolution('test_logger')
    
    def test_context_logging(self, logger):
        """Тест логирования с контекстом"""
        logger.set_context(user_id=123, session_id='abc-def')
        logger.info("User action", action='login')
        
        # Проверяем, что контекст сохранился
        assert logger.context.get('user_id') == 123
        assert logger.context.get('session_id') == 'abc-def'
    
    def test_tracing(self, logger):
        """Тест трассировки операций"""
        trace_id = logger.start_trace('test_operation')
        
        assert trace_id is not None
        assert logger.context.get('trace_id') == trace_id
        
        # Завершение трассировки
        result = logger.end_trace(trace_id, success=True)
        assert result is True
        
        # Проверяем, что трассировка сохранена
        trace = logger.trace_manager.get_trace(trace_id)
        assert trace is not None
        assert trace['operation'] == 'test_operation'
        assert trace['success'] is True
    
    def test_metrics_collection(self, logger):
        """Тест сбора метрик"""
        # Логируем несколько событий
        for i in range(5):
            logger.info(f"Test message {i}")
        
        metrics = logger.get_metrics()
        
        assert 'counters' in metrics
        assert 'logs_total[level=INFO]' in metrics['counters']
        assert metrics['counters']['logs_total[level=INFO]'] == 5
    
    def test_filtering(self, logger):
        """Тест фильтрации логов"""
        # Добавляем фильтр, который пропускает только ERROR
        def error_only_filter(log_record):
            return log_record['level'] == 'ERROR'
        
        logger.add_filter(error_only_filter)
        
        # Эти логи должны быть отфильтрованы
        logger.info("Info message")
        logger.debug("Debug message")
        
        # Этот лог должен пройти
        logger.error("Error message")
        
        metrics = logger.get_metrics()
        # Должен быть только один лог (ERROR)
        total_logs = sum(v for k, v in metrics['counters'].items() if k.startswith('logs_total'))
        assert total_logs == 1

# =============================================================================
# Упражнение 2: Application Performance Monitoring (APM)
# =============================================================================

"""
ЗАДАНИЕ 2: Application Performance Monitoring

Создайте систему мониторинга производительности приложения:

1. APMTracker для отслеживания:
   - Время выполнения операций
   - Использование памяти
   - Количество активных соединений
   - Throughput и latency

2. Интеграция с веб-фреймворками:
   - Middleware для Flask/FastAPI
   - Автоматическое отслеживание HTTP запросов
   - Database query monitoring

3. Dashboards и отчеты:
   - Real-time метрики
   - Исторические данные
   - Alerts при превышении порогов
"""

# Ваш код здесь:
class APMTracker:
    """Трекер производительности приложения"""
    
    def __init__(self):
        # TODO: Реализуйте инициализацию
        pass
    
    def track_operation(self, operation_name: str):
        """Трекинг операции"""
        # TODO: Реализуйте context manager
        pass
    
    def track_database_query(self, query: str, duration: float):
        """Трекинг запроса к БД"""
        # TODO: Реализуйте метод
        pass
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Получение отчета о производительности"""
        # TODO: Реализуйте метод
        pass

# Решение (краткая версия):
@contextmanager
def performance_tracker(operation_name: str, apm_tracker):
    """Context manager для трекинга производительности"""
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss
    
    try:
        yield
    finally:
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        duration = end_time - start_time
        memory_delta = end_memory - start_memory
        
        apm_tracker.record_operation(operation_name, duration, memory_delta)

class APMTrackerSolution:
    """Решение: Трекер производительности приложения"""
    
    def __init__(self):
        self.operations = defaultdict(list)
        self.db_queries = []
        self.http_requests = []
        self.system_metrics = deque(maxlen=1000)
        self.start_time = datetime.utcnow()
        self.logger = AdvancedLoggerSolution('apm_tracker')
        
        # Запуск сбора системных метрик
        self._start_system_monitoring()
    
    def _start_system_monitoring(self):
        """Запуск мониторинга системных метрик"""
        def collect_system_metrics():
            while True:
                try:
                    metrics = {
                        'timestamp': datetime.utcnow().isoformat(),
                        'cpu_percent': psutil.cpu_percent(),
                        'memory_percent': psutil.virtual_memory().percent,
                        'disk_io': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
                        'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
                    }
                    self.system_metrics.append(metrics)
                    time.sleep(5)  # Собираем каждые 5 секунд
                except Exception as e:
                    self.logger.error("System metrics collection failed", error=str(e))
                    time.sleep(5)
        
        thread = threading.Thread(target=collect_system_metrics, daemon=True)
        thread.start()
    
    @contextmanager
    def track_operation(self, operation_name: str):
        """Трекинг операции"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        self.logger.debug(f"Starting operation: {operation_name}")
        
        try:
            yield
            success = True
        except Exception as e:
            success = False
            self.logger.error(f"Operation failed: {operation_name}", error=str(e))
            raise
        finally:
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss
            
            duration = end_time - start_time
            memory_delta = end_memory - start_memory
            
            self.record_operation(operation_name, duration, memory_delta, success)
    
    def record_operation(self, operation_name: str, duration: float, 
                        memory_delta: int, success: bool = True):
        """Запись операции"""
        operation_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'operation': operation_name,
            'duration_ms': duration * 1000,
            'memory_delta_mb': memory_delta / (1024 * 1024),
            'success': success
        }
        
        self.operations[operation_name].append(operation_data)
        
        # Ограничиваем историю
        if len(self.operations[operation_name]) > 100:
            self.operations[operation_name] = self.operations[operation_name][-50:]
        
        self.logger.info(f"Operation completed: {operation_name}",
                        duration_ms=operation_data['duration_ms'],
                        memory_delta_mb=operation_data['memory_delta_mb'],
                        success=success)
    
    def track_http_request(self, method: str, path: str, status_code: int, 
                          duration: float, size: int = 0):
        """Трекинг HTTP запроса"""
        request_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'method': method,
            'path': path,
            'status_code': status_code,
            'duration_ms': duration * 1000,
            'response_size_bytes': size
        }
        
        self.http_requests.append(request_data)
        
        # Ограничиваем размер
        if len(self.http_requests) > 1000:
            self.http_requests = self.http_requests[-500:]
        
        self.logger.info(f"HTTP {method} {path} - {status_code}",
                        duration_ms=request_data['duration_ms'],
                        response_size=size)
    
    def track_database_query(self, query: str, duration: float, rows_affected: int = 0):
        """Трекинг запроса к БД"""
        query_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'query_hash': hash(query) % 10000,
            'query_preview': query[:100] + '...' if len(query) > 100 else query,
            'duration_ms': duration * 1000,
            'rows_affected': rows_affected
        }
        
        self.db_queries.append(query_data)
        
        # Ограничиваем размер
        if len(self.db_queries) > 1000:
            self.db_queries = self.db_queries[-500:]
        
        if duration > 1.0:  # Медленный запрос
            self.logger.warning("Slow database query detected",
                              duration_ms=query_data['duration_ms'],
                              query_preview=query_data['query_preview'])
    
    def get_performance_report(self, hours: int = 1) -> Dict[str, Any]:
        """Получение отчета о производительности"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Фильтруем данные за период
        recent_ops = []
        for op_name, ops in self.operations.items():
            for op in ops:
                if datetime.fromisoformat(op['timestamp']) > cutoff_time:
                    recent_ops.append(op)
        
        recent_requests = [
            req for req in self.http_requests
            if datetime.fromisoformat(req['timestamp']) > cutoff_time
        ]
        
        recent_queries = [
            query for query in self.db_queries
            if datetime.fromisoformat(query['timestamp']) > cutoff_time
        ]
        
        # Вычисляем статистику
        report = {
            'period_hours': hours,
            'uptime_hours': (datetime.utcnow() - self.start_time).total_seconds() / 3600,
            'operations': self._analyze_operations(recent_ops),
            'http_requests': self._analyze_http_requests(recent_requests),
            'database_queries': self._analyze_db_queries(recent_queries),
            'system_metrics': self._get_latest_system_metrics()
        }
        
        return report
    
    def _analyze_operations(self, operations: List[Dict]) -> Dict[str, Any]:
        """Анализ операций"""
        if not operations:
            return {'total': 0}
        
        durations = [op['duration_ms'] for op in operations]
        success_count = sum(1 for op in operations if op['success'])
        
        return {
            'total': len(operations),
            'success_rate': success_count / len(operations),
            'avg_duration_ms': sum(durations) / len(durations),
            'max_duration_ms': max(durations),
            'min_duration_ms': min(durations)
        }
    
    def _analyze_http_requests(self, requests: List[Dict]) -> Dict[str, Any]:
        """Анализ HTTP запросов"""
        if not requests:
            return {'total': 0}
        
        status_codes = defaultdict(int)
        durations = [req['duration_ms'] for req in requests]
        
        for req in requests:
            status_codes[req['status_code']] += 1
        
        return {
            'total': len(requests),
            'status_codes': dict(status_codes),
            'avg_duration_ms': sum(durations) / len(durations),
            'throughput_per_minute': len(requests) / (self.get_performance_report.__defaults__[0] * 60),
            'error_rate': sum(v for k, v in status_codes.items() if k >= 400) / len(requests)
        }
    
    def _analyze_db_queries(self, queries: List[Dict]) -> Dict[str, Any]:
        """Анализ запросов к БД"""
        if not queries:
            return {'total': 0}
        
        durations = [q['duration_ms'] for q in queries]
        slow_queries = [q for q in queries if q['duration_ms'] > 1000]
        
        return {
            'total': len(queries),
            'slow_queries_count': len(slow_queries),
            'avg_duration_ms': sum(durations) / len(durations),
            'queries_per_minute': len(queries) / (self.get_performance_report.__defaults__[0] * 60)
        }
    
    def _get_latest_system_metrics(self) -> Dict[str, Any]:
        """Получение последних системных метрик"""
        if not self.system_metrics:
            return {}
        
        latest = self.system_metrics[-1]
        return {
            'timestamp': latest['timestamp'],
            'cpu_percent': latest['cpu_percent'],
            'memory_percent': latest['memory_percent']
        }

# =============================================================================
# Упражнение 3: Real-time Monitoring Dashboard
# =============================================================================

"""
ЗАДАНИЕ 3: Real-time Monitoring Dashboard

Создайте систему real-time мониторинга:

1. DashboardServer:
   - WebSocket подключения для real-time данных
   - REST API для исторических данных
   - Интеграция с метриками

2. AlertSystem:
   - Правила для автоматических оповещений
   - Интеграция с различными каналами (email, Slack)
   - Escalation policies

3. DataRetention:
   - Агрегация метрик по времени
   - Сжатие старых данных
   - Cleanup policies
"""

# Ваш код здесь (краткое решение):
class MonitoringDashboard:
    """Система мониторинга с dashboard"""
    
    def __init__(self):
        self.apm_tracker = APMTrackerSolution()
        self.alert_rules = []
        self.subscribers = []
        self.logger = AdvancedLoggerSolution('dashboard')
    
    def add_alert_rule(self, rule):
        """Добавление правила оповещения"""
        self.alert_rules.append(rule)
    
    def check_alerts(self):
        """Проверка правил оповещений"""
        metrics = self.apm_tracker.get_performance_report()
        
        for rule in self.alert_rules:
            try:
                if rule.should_trigger(metrics):
                    alert = rule.create_alert(metrics)
                    self._send_alert(alert)
            except Exception as e:
                self.logger.error(f"Alert rule check failed: {rule.__class__.__name__}", 
                                error=str(e))
    
    def _send_alert(self, alert: Dict[str, Any]):
        """Отправка оповещения"""
        self.logger.warning(f"ALERT: {alert['title']}", **alert)
        
        # Уведомление подписчиков
        for subscriber in self.subscribers:
            try:
                subscriber.notify(alert)
            except Exception as e:
                self.logger.error("Failed to notify subscriber", error=str(e))

# =============================================================================
# Запуск упражнений
# =============================================================================

def run_exercises():
    """Запуск всех упражнений"""
    print("=== Упражнения: Логирование и мониторинг ===\n")
    
    # 1. Advanced Logging System
    print("1. Advanced Logging System...")
    logger = AdvancedLoggerSolution('demo_app')
    
    # Установка контекста
    logger.set_context(user_id=123, session_id='abc-def-ghi')
    
    # Трассировка операции
    trace_id = logger.start_trace('user_authentication')
    logger.info("User login attempt", username='alice')
    time.sleep(0.1)  # Симуляция работы
    logger.end_trace(trace_id, success=True)
    
    # Получение метрик
    metrics = logger.get_metrics()
    print(f"   Метрики логирования: {len(metrics['counters'])} счетчиков")
    
    # 2. APM Tracker
    print("\n2. Application Performance Monitoring...")
    apm = APMTrackerSolution()
    
    # Трекинг операций
    with apm.track_operation('data_processing'):
        time.sleep(0.05)  # Симуляция работы
    
    # Трекинг HTTP запросов
    apm.track_http_request('GET', '/api/users', 200, 0.1, 1024)
    apm.track_http_request('POST', '/api/orders', 500, 0.5, 512)
    
    # Трекинг DB запросов
    apm.track_database_query('SELECT * FROM users WHERE id = ?', 0.02, 1)
    
    # Отчет о производительности
    report = apm.get_performance_report()
    print(f"   HTTP запросов: {report['http_requests']['total']}")
    print(f"   Операций: {report['operations']['total']}")
    
    # 3. Monitoring Dashboard
    print("\n3. Real-time Monitoring Dashboard...")
    dashboard = MonitoringDashboard()
    
    # Добавление простого правила оповещения
    class HighErrorRateRule:
        def should_trigger(self, metrics):
            http_metrics = metrics.get('http_requests', {})
            error_rate = http_metrics.get('error_rate', 0)
            return error_rate > 0.1  # Более 10% ошибок
        
        def create_alert(self, metrics):
            return {
                'title': 'High Error Rate',
                'message': f"Error rate: {metrics['http_requests']['error_rate']:.1%}",
                'severity': 'WARNING'
            }
    
    dashboard.add_alert_rule(HighErrorRateRule())
    dashboard.check_alerts()
    
    print("\n✅ Все упражнения выполнены успешно!")
    print("📊 Теперь вы можете создавать продвинутые системы логирования и мониторинга!")

if __name__ == "__main__":
    run_exercises() 