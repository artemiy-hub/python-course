"""
Примеры: Логирование и мониторинг

Этот файл содержит практические примеры настройки логирования, мониторинга
производительности, метрик и системы оповещений в Python приложениях.
"""

import logging
import logging.handlers
import sys
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import traceback
import functools
import inspect
import psutil
import queue
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import sqlite3
from contextlib import contextmanager
import tempfile
import warnings
from collections import defaultdict, deque
import asyncio
import aiohttp
import weakref

# =============================================================================
# Пример 1: Структурированное логирование
# =============================================================================

class StructuredLogger:
    """Структурированный логгер с JSON форматом"""
    
    def __init__(self, name: str, log_file: str = None, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Удаляем существующие обработчики
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # JSON форматтер
        self.formatter = JsonFormatter()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=10*1024*1024, backupCount=5
            )
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
    
    def log(self, level: str, message: str, **kwargs):
        """Логирование с дополнительными полями"""
        extra = {
            'custom_fields': kwargs,
            'timestamp_iso': datetime.utcnow().isoformat(),
            'process_id': psutil.Process().pid,
            'thread_id': threading.get_ident()
        }
        
        getattr(self.logger, level.lower())(message, extra=extra)
    
    def info(self, message: str, **kwargs):
        self.log('INFO', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log('ERROR', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log('WARNING', message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self.log('DEBUG', message, **kwargs)

class JsonFormatter(logging.Formatter):
    """JSON форматтер для логов"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Добавляем дополнительные поля
        if hasattr(record, 'custom_fields'):
            log_entry.update(record.custom_fields)
        
        if hasattr(record, 'timestamp_iso'):
            log_entry['timestamp_iso'] = record.timestamp_iso
        
        if hasattr(record, 'process_id'):
            log_entry['process_id'] = record.process_id
        
        if hasattr(record, 'thread_id'):
            log_entry['thread_id'] = record.thread_id
        
        # Добавляем exception info если есть
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_entry)

def structured_logging_demo():
    """Демонстрация структурированного логирования"""
    print("=== Structured Logging Demo ===")
    
    # Создание логгера
    logger = StructuredLogger('demo_app', 'demo.log', 'DEBUG')
    
    # Примеры логирования
    logger.info("Application started", 
                version="1.0.0", 
                environment="development")
    
    logger.debug("Processing user request", 
                 user_id=12345, 
                 endpoint="/api/users",
                 method="GET")
    
    logger.warning("Rate limit approaching", 
                   current_requests=95, 
                   limit=100,
                   user_ip="192.168.1.100")
    
    # Логирование с exception
    try:
        result = 10 / 0
    except Exception as e:
        logger.error("Mathematical error occurred", 
                     operation="division",
                     operands=[10, 0],
                     error_type=type(e).__name__)
    
    return logger

# =============================================================================
# Пример 2: Декораторы для логирования
# =============================================================================

def log_function_calls(logger: StructuredLogger = None, 
                      log_args: bool = True, 
                      log_result: bool = True,
                      log_performance: bool = True):
    """Декоратор для логирования вызовов функций"""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if logger is None:
                return func(*args, **kwargs)
            
            function_name = func.__name__
            start_time = time.time()
            
            # Логируем вызов
            log_data = {
                'function': function_name,
                'module': func.__module__,
            }
            
            if log_args:
                log_data.update({
                    'args': [str(arg) for arg in args],
                    'kwargs': {k: str(v) for k, v in kwargs.items()}
                })
            
            logger.debug(f"Calling function {function_name}", **log_data)
            
            try:
                result = func(*args, **kwargs)
                
                # Логируем успешное выполнение
                end_time = time.time()
                execution_time = end_time - start_time
                
                success_data = {
                    'function': function_name,
                    'status': 'success',
                }
                
                if log_performance:
                    success_data['execution_time_seconds'] = execution_time
                
                if log_result and result is not None:
                    success_data['result_type'] = type(result).__name__
                    success_data['result_length'] = len(str(result))
                
                logger.info(f"Function {function_name} completed successfully", **success_data)
                
                return result
                
            except Exception as e:
                # Логируем ошибку
                end_time = time.time()
                execution_time = end_time - start_time
                
                error_data = {
                    'function': function_name,
                    'status': 'error',
                    'error_type': type(e).__name__,
                    'error_message': str(e),
                    'execution_time_seconds': execution_time
                }
                
                logger.error(f"Function {function_name} failed", **error_data)
                raise
        
        return wrapper
    return decorator

def log_class_methods(logger: StructuredLogger = None):
    """Декоратор для логирования методов класса"""
    
    def class_decorator(cls):
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not attr_name.startswith('_'):
                setattr(cls, attr_name, log_function_calls(logger)(attr))
        return cls
    
    return class_decorator

@dataclass
class UserService:
    """Пример сервиса с логированием"""
    
    def __init__(self):
        self.users = {}
        self.logger = StructuredLogger('user_service')
    
    @log_function_calls()
    def create_user(self, username: str, email: str) -> Dict[str, Any]:
        """Создание пользователя"""
        if username in self.users:
            raise ValueError(f"User {username} already exists")
        
        user = {
            'username': username,
            'email': email,
            'created_at': datetime.utcnow().isoformat(),
            'id': len(self.users) + 1
        }
        
        self.users[username] = user
        return user
    
    @log_function_calls()
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя"""
        return self.users.get(username)
    
    @log_function_calls()
    def delete_user(self, username: str) -> bool:
        """Удаление пользователя"""
        if username in self.users:
            del self.users[username]
            return True
        return False

def logging_decorators_demo():
    """Демонстрация декораторов логирования"""
    print("\n=== Logging Decorators Demo ===")
    
    # Создание сервиса
    service = UserService()
    
    # Операции с пользователями
    try:
        user1 = service.create_user("alice", "alice@example.com")
        print(f"Created user: {user1}")
        
        user2 = service.get_user("alice")
        print(f"Retrieved user: {user2}")
        
        # Попытка создать дублирующегося пользователя (вызовет ошибку)
        service.create_user("alice", "alice2@example.com")
        
    except Exception as e:
        print(f"Expected error caught: {e}")
    
    return service

# =============================================================================
# Пример 3: Мониторинг производительности
# =============================================================================

class PerformanceMonitor:
    """Монитор производительности приложения"""
    
    def __init__(self, collection_interval: float = 10.0):
        self.collection_interval = collection_interval
        self.metrics = defaultdict(list)
        self.running = False
        self.thread = None
        self.logger = StructuredLogger('performance_monitor')
    
    def start_monitoring(self):
        """Запуск мониторинга"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._collect_metrics, daemon=True)
        self.thread.start()
        
        self.logger.info("Performance monitoring started", 
                        interval=self.collection_interval)
    
    def stop_monitoring(self):
        """Остановка мониторинга"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        
        self.logger.info("Performance monitoring stopped")
    
    def _collect_metrics(self):
        """Сбор метрик производительности"""
        while self.running:
            try:
                timestamp = datetime.utcnow()
                
                # Системные метрики
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Метрики процесса
                process = psutil.Process()
                process_memory = process.memory_info()
                process_cpu = process.cpu_percent()
                
                metrics = {
                    'timestamp': timestamp.isoformat(),
                    'system': {
                        'cpu_percent': cpu_percent,
                        'memory_percent': memory.percent,
                        'memory_available_gb': memory.available / (1024**3),
                        'disk_percent': (disk.used / disk.total) * 100,
                        'disk_free_gb': disk.free / (1024**3)
                    },
                    'process': {
                        'cpu_percent': process_cpu,
                        'memory_rss_mb': process_memory.rss / (1024**2),
                        'memory_vms_mb': process_memory.vms / (1024**2),
                        'threads_count': process.num_threads()
                    }
                }
                
                # Сохраняем метрики
                self.metrics['system_metrics'].append(metrics)
                
                # Логируем если есть проблемы
                if cpu_percent > 80:
                    self.logger.warning("High CPU usage detected", 
                                      cpu_percent=cpu_percent)
                
                if memory.percent > 85:
                    self.logger.warning("High memory usage detected", 
                                      memory_percent=memory.percent)
                
                # Ограничиваем размер истории метрик
                if len(self.metrics['system_metrics']) > 100:
                    self.metrics['system_metrics'] = self.metrics['system_metrics'][-50:]
                
                time.sleep(self.collection_interval)
                
            except Exception as e:
                self.logger.error("Error collecting performance metrics", 
                                error=str(e))
                time.sleep(self.collection_interval)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Получение текущих метрик"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            process = psutil.Process()
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'process_memory_mb': process.memory_info().rss / (1024**2),
                'process_cpu_percent': process.cpu_percent()
            }
        except Exception as e:
            self.logger.error("Error getting current metrics", error=str(e))
            return {}
    
    def get_metrics_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Получение сводки метрик за период"""
        if not self.metrics['system_metrics']:
            return {'error': 'No metrics available'}
        
        # Фильтруем метрики за указанный период
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_metrics = [
            m for m in self.metrics['system_metrics']
            if datetime.fromisoformat(m['timestamp']) > cutoff_time
        ]
        
        if not recent_metrics:
            return {'error': 'No recent metrics available'}
        
        # Вычисляем статистику
        cpu_values = [m['system']['cpu_percent'] for m in recent_metrics]
        memory_values = [m['system']['memory_percent'] for m in recent_metrics]
        
        return {
            'period_hours': hours,
            'metrics_count': len(recent_metrics),
            'cpu': {
                'avg': sum(cpu_values) / len(cpu_values),
                'max': max(cpu_values),
                'min': min(cpu_values)
            },
            'memory': {
                'avg': sum(memory_values) / len(memory_values),
                'max': max(memory_values),
                'min': min(memory_values)
            }
        }

class RequestTracker:
    """Трекер HTTP запросов"""
    
    def __init__(self):
        self.requests = deque(maxlen=1000)  # Последние 1000 запросов
        self.logger = StructuredLogger('request_tracker')
    
    def track_request(self, method: str, path: str, status_code: int, 
                     duration: float, user_id: str = None, 
                     ip_address: str = None):
        """Трекинг HTTP запроса"""
        request_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'method': method,
            'path': path,
            'status_code': status_code,
            'duration_ms': duration * 1000,
            'user_id': user_id,
            'ip_address': ip_address
        }
        
        self.requests.append(request_data)
        
        # Логируем запрос
        self.logger.info(f"{method} {path} - {status_code}", **request_data)
        
        # Предупреждения о медленных запросах
        if duration > 2.0:  # Более 2 секунд
            self.logger.warning("Slow request detected", **request_data)
    
    def get_request_stats(self, minutes: int = 10) -> Dict[str, Any]:
        """Статистика запросов за период"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        
        recent_requests = [
            req for req in self.requests
            if datetime.fromisoformat(req['timestamp']) > cutoff_time
        ]
        
        if not recent_requests:
            return {'total_requests': 0}
        
        # Статистика по статус кодам
        status_codes = defaultdict(int)
        durations = []
        methods = defaultdict(int)
        
        for req in recent_requests:
            status_codes[req['status_code']] += 1
            durations.append(req['duration_ms'])
            methods[req['method']] += 1
        
        return {
            'period_minutes': minutes,
            'total_requests': len(recent_requests),
            'status_codes': dict(status_codes),
            'methods': dict(methods),
            'duration_stats': {
                'avg_ms': sum(durations) / len(durations),
                'max_ms': max(durations),
                'min_ms': min(durations)
            },
            'error_rate': (status_codes.get(500, 0) + status_codes.get(400, 0)) / len(recent_requests)
        }

def performance_monitoring_demo():
    """Демонстрация мониторинга производительности"""
    print("\n=== Performance Monitoring Demo ===")
    
    # Запуск мониторинга
    monitor = PerformanceMonitor(collection_interval=2.0)
    monitor.start_monitoring()
    
    # Симуляция работы приложения
    request_tracker = RequestTracker()
    
    print("Симуляция HTTP запросов...")
    for i in range(10):
        # Симуляция запроса
        start_time = time.time()
        time.sleep(0.1)  # Симуляция обработки
        duration = time.time() - start_time
        
        method = 'GET' if i % 2 == 0 else 'POST'
        path = f'/api/endpoint/{i}'
        status_code = 200 if i < 8 else 500  # Несколько ошибок
        
        request_tracker.track_request(method, path, status_code, duration, 
                                    user_id=f"user_{i % 3}",
                                    ip_address=f"192.168.1.{i + 100}")
    
    # Получение метрик
    current_metrics = monitor.get_current_metrics()
    print(f"Текущие метрики: {json.dumps(current_metrics, indent=2)}")
    
    request_stats = request_tracker.get_request_stats(minutes=1)
    print(f"Статистика запросов: {json.dumps(request_stats, indent=2)}")
    
    # Остановка мониторинга
    monitor.stop_monitoring()
    
    return monitor, request_tracker

# =============================================================================
# Пример 4: Система оповещений
# =============================================================================

@dataclass
class Alert:
    """Модель оповещения"""
    id: str
    level: str  # INFO, WARNING, ERROR, CRITICAL
    title: str
    message: str
    source: str
    timestamp: datetime
    tags: Dict[str, str]
    resolved: bool = False

class AlertManager:
    """Менеджер системы оповещений"""
    
    def __init__(self):
        self.alerts = {}
        self.handlers = []
        self.rules = []
        self.logger = StructuredLogger('alert_manager')
    
    def add_handler(self, handler):
        """Добавление обработчика оповещений"""
        self.handlers.append(handler)
    
    def add_rule(self, rule):
        """Добавление правила для генерации оповещений"""
        self.rules.append(rule)
    
    def create_alert(self, level: str, title: str, message: str, 
                    source: str, tags: Dict[str, str] = None) -> Alert:
        """Создание оповещения"""
        alert = Alert(
            id=f"alert_{int(time.time())}_{len(self.alerts)}",
            level=level,
            title=title,
            message=message,
            source=source,
            timestamp=datetime.utcnow(),
            tags=tags or {}
        )
        
        self.alerts[alert.id] = alert
        
        # Логируем создание оповещения
        self.logger.info(f"Alert created: {alert.title}", 
                        alert_id=alert.id,
                        level=alert.level,
                        source=alert.source,
                        tags=alert.tags)
        
        # Отправляем оповещение всем обработчикам
        for handler in self.handlers:
            try:
                handler.handle_alert(alert)
            except Exception as e:
                self.logger.error(f"Alert handler failed: {handler.__class__.__name__}", 
                                error=str(e))
        
        return alert
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Разрешение оповещения"""
        if alert_id in self.alerts:
            self.alerts[alert_id].resolved = True
            self.logger.info(f"Alert resolved", alert_id=alert_id)
            return True
        return False
    
    def get_active_alerts(self, level: str = None) -> List[Alert]:
        """Получение активных оповещений"""
        active_alerts = [
            alert for alert in self.alerts.values()
            if not alert.resolved
        ]
        
        if level:
            active_alerts = [
                alert for alert in active_alerts
                if alert.level == level
            ]
        
        return sorted(active_alerts, key=lambda a: a.timestamp, reverse=True)
    
    def check_metrics_for_alerts(self, metrics: Dict[str, Any]):
        """Проверка метрик на соответствие правилам оповещений"""
        for rule in self.rules:
            try:
                if rule.should_trigger(metrics):
                    alert = rule.create_alert(metrics)
                    self.create_alert(**alert)
            except Exception as e:
                self.logger.error(f"Error checking alert rule: {rule.__class__.__name__}", 
                                error=str(e))

class AlertRule:
    """Базовый класс для правил оповещений"""
    
    def should_trigger(self, metrics: Dict[str, Any]) -> bool:
        """Проверка, должно ли сработать правило"""
        raise NotImplementedError
    
    def create_alert(self, metrics: Dict[str, Any]) -> Dict[str, str]:
        """Создание данных для оповещения"""
        raise NotImplementedError

class HighCPURule(AlertRule):
    """Правило для высокой загрузки CPU"""
    
    def __init__(self, threshold: float = 80.0):
        self.threshold = threshold
    
    def should_trigger(self, metrics: Dict[str, Any]) -> bool:
        cpu_percent = metrics.get('cpu_percent', 0)
        return cpu_percent > self.threshold
    
    def create_alert(self, metrics: Dict[str, Any]) -> Dict[str, str]:
        cpu_percent = metrics.get('cpu_percent', 0)
        return {
            'level': 'WARNING',
            'title': 'High CPU Usage',
            'message': f'CPU usage is at {cpu_percent:.1f}%, exceeding threshold of {self.threshold}%',
            'source': 'system_monitor',
            'tags': {'metric': 'cpu_usage', 'threshold': str(self.threshold)}
        }

class HighMemoryRule(AlertRule):
    """Правило для высокого использования памяти"""
    
    def __init__(self, threshold: float = 85.0):
        self.threshold = threshold
    
    def should_trigger(self, metrics: Dict[str, Any]) -> bool:
        memory_percent = metrics.get('memory_percent', 0)
        return memory_percent > self.threshold
    
    def create_alert(self, metrics: Dict[str, Any]) -> Dict[str, str]:
        memory_percent = metrics.get('memory_percent', 0)
        return {
            'level': 'ERROR',
            'title': 'High Memory Usage',
            'message': f'Memory usage is at {memory_percent:.1f}%, exceeding threshold of {self.threshold}%',
            'source': 'system_monitor',
            'tags': {'metric': 'memory_usage', 'threshold': str(self.threshold)}
        }

class ConsoleAlertHandler:
    """Обработчик оповещений для консоли"""
    
    def handle_alert(self, alert: Alert):
        """Обработка оповещения"""
        print(f"🚨 ALERT [{alert.level}]: {alert.title}")
        print(f"   Message: {alert.message}")
        print(f"   Source: {alert.source}")
        print(f"   Time: {alert.timestamp}")
        if alert.tags:
            print(f"   Tags: {alert.tags}")
        print()

class LogAlertHandler:
    """Обработчик оповещений для логирования"""
    
    def __init__(self):
        self.logger = StructuredLogger('alert_handler')
    
    def handle_alert(self, alert: Alert):
        """Обработка оповещения через логирование"""
        self.logger.info(f"Alert notification: {alert.title}",
                        alert_id=alert.id,
                        level=alert.level,
                        message=alert.message,
                        source=alert.source,
                        tags=alert.tags)

class EmailAlertHandler:
    """Обработчик оповещений для email (демонстрационный)"""
    
    def __init__(self, smtp_server: str, port: int, username: str, password: str, recipients: List[str]):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
        self.recipients = recipients
        self.logger = StructuredLogger('email_alert_handler')
    
    def handle_alert(self, alert: Alert):
        """Обработка оповещения через email"""
        # В демонстрационном режиме просто логируем
        self.logger.info(f"Would send email alert: {alert.title}",
                        recipients=self.recipients,
                        alert_level=alert.level)
        
        # Реальная отправка email (закомментировано для демо)
        # try:
        #     self._send_email(alert)
        # except Exception as e:
        #     self.logger.error(f"Failed to send email alert", error=str(e))
    
    def _send_email(self, alert: Alert):
        """Отправка email (реальная реализация)"""
        msg = MimeMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = f"[{alert.level}] {alert.title}"
        
        body = f"""
        Alert Details:
        
        Level: {alert.level}
        Title: {alert.title}
        Message: {alert.message}
        Source: {alert.source}
        Time: {alert.timestamp}
        Tags: {alert.tags}
        
        Alert ID: {alert.id}
        """
        
        msg.attach(MimeText(body, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)

def alerting_system_demo():
    """Демонстрация системы оповещений"""
    print("\n=== Alerting System Demo ===")
    
    # Создание менеджера оповещений
    alert_manager = AlertManager()
    
    # Добавление обработчиков
    alert_manager.add_handler(ConsoleAlertHandler())
    alert_manager.add_handler(LogAlertHandler())
    
    # Добавление правил
    alert_manager.add_rule(HighCPURule(threshold=75.0))
    alert_manager.add_rule(HighMemoryRule(threshold=80.0))
    
    # Симуляция метрик, которые вызовут оповещения
    test_metrics = [
        {'cpu_percent': 85.0, 'memory_percent': 70.0},  # Высокий CPU
        {'cpu_percent': 60.0, 'memory_percent': 90.0},  # Высокая память
        {'cpu_percent': 95.0, 'memory_percent': 95.0},  # Оба высокие
        {'cpu_percent': 50.0, 'memory_percent': 60.0},  # Нормальные значения
    ]
    
    print("Проверка метрик на оповещения...")
    for i, metrics in enumerate(test_metrics):
        print(f"\nТест {i+1}: CPU={metrics['cpu_percent']}%, Memory={metrics['memory_percent']}%")
        alert_manager.check_metrics_for_alerts(metrics)
    
    # Создание ручного оповещения
    manual_alert = alert_manager.create_alert(
        level='CRITICAL',
        title='Database Connection Lost',
        message='Unable to connect to primary database server',
        source='database_monitor',
        tags={'database': 'primary', 'service': 'user_api'}
    )
    
    # Получение активных оповещений
    active_alerts = alert_manager.get_active_alerts()
    print(f"\nВсего активных оповещений: {len(active_alerts)}")
    
    for alert in active_alerts:
        print(f"  - [{alert.level}] {alert.title} (ID: {alert.id})")
    
    # Разрешение оповещения
    if active_alerts:
        alert_manager.resolve_alert(active_alerts[0].id)
        print(f"\nРазрешено оповещение: {active_alerts[0].id}")
    
    return alert_manager

# =============================================================================
# Пример 5: Мониторинг базы данных и запросов
# =============================================================================

class DatabaseMonitor:
    """Монитор базы данных"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = None
        self.query_stats = defaultdict(list)
        self.logger = StructuredLogger('database_monitor')
        self._setup_database()
    
    def _setup_database(self):
        """Настройка базы данных"""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        
        # Создание таблиц для мониторинга
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS query_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_hash TEXT NOT NULL,
                query_text TEXT NOT NULL,
                execution_time_ms REAL NOT NULL,
                rows_affected INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL
            )
        ''')
        self.connection.commit()
    
    @contextmanager
    def monitored_query(self, query: str, params: tuple = None):
        """Context manager для мониторинга SQL запросов"""
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]
        start_time = time.time()
        
        cursor = self.connection.cursor()
        
        try:
            # Выполнение запроса
            if params:
                result = cursor.execute(query, params)
            else:
                result = cursor.execute(query)
            
            execution_time = (time.time() - start_time) * 1000  # в миллисекундах
            rows_affected = cursor.rowcount
            
            # Логирование успешного запроса
            self._log_query(query_hash, query, execution_time, rows_affected, 'SUCCESS')
            
            yield result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            
            # Логирование неудачного запроса
            self._log_query(query_hash, query, execution_time, 0, 'ERROR')
            
            self.logger.error("Database query failed", 
                            query_hash=query_hash,
                            error=str(e),
                            execution_time_ms=execution_time)
            raise
        
        finally:
            cursor.close()
    
    def _log_query(self, query_hash: str, query: str, execution_time: float, 
                   rows_affected: int, status: str):
        """Логирование запроса"""
        try:
            # Сохранение в БД
            log_cursor = self.connection.cursor()
            log_cursor.execute('''
                INSERT INTO query_log (query_hash, query_text, execution_time_ms, rows_affected, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (query_hash, query, execution_time, rows_affected, status))
            self.connection.commit()
            log_cursor.close()
            
            # Сохранение в памяти для анализа
            self.query_stats[query_hash].append({
                'execution_time_ms': execution_time,
                'rows_affected': rows_affected,
                'timestamp': datetime.utcnow(),
                'status': status
            })
            
            # Логирование медленных запросов
            if execution_time > 1000:  # Более 1 секунды
                self.logger.warning("Slow query detected",
                                  query_hash=query_hash,
                                  execution_time_ms=execution_time,
                                  rows_affected=rows_affected)
            
        except Exception as e:
            self.logger.error("Failed to log query", error=str(e))
    
    def get_query_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """Получение статистики запросов"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_queries,
                    AVG(execution_time_ms) as avg_execution_time,
                    MAX(execution_time_ms) as max_execution_time,
                    SUM(CASE WHEN status = 'ERROR' THEN 1 ELSE 0 END) as error_count,
                    SUM(CASE WHEN execution_time_ms > 1000 THEN 1 ELSE 0 END) as slow_query_count
                FROM query_log
                WHERE timestamp > datetime('now', '-{} hours')
            '''.format(hours))
            
            stats = cursor.fetchone()
            cursor.close()
            
            return {
                'period_hours': hours,
                'total_queries': stats[0] or 0,
                'avg_execution_time_ms': stats[1] or 0,
                'max_execution_time_ms': stats[2] or 0,
                'error_count': stats[3] or 0,
                'slow_query_count': stats[4] or 0,
                'error_rate': (stats[3] or 0) / max(stats[0] or 1, 1) * 100
            }
            
        except Exception as e:
            self.logger.error("Failed to get query statistics", error=str(e))
            return {'error': 'Failed to get statistics'}
    
    def get_slowest_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получение самых медленных запросов"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT query_hash, query_text, MAX(execution_time_ms) as max_time,
                       AVG(execution_time_ms) as avg_time, COUNT(*) as count
                FROM query_log
                WHERE timestamp > datetime('now', '-24 hours')
                GROUP BY query_hash
                ORDER BY max_time DESC
                LIMIT ?
            ''', (limit,))
            
            queries = []
            for row in cursor.fetchall():
                queries.append({
                    'query_hash': row[0],
                    'query_text': row[1][:100] + '...' if len(row[1]) > 100 else row[1],
                    'max_execution_time_ms': row[2],
                    'avg_execution_time_ms': row[3],
                    'execution_count': row[4]
                })
            
            cursor.close()
            return queries
            
        except Exception as e:
            self.logger.error("Failed to get slowest queries", error=str(e))
            return []

import hashlib

def database_monitoring_demo():
    """Демонстрация мониторинга базы данных"""
    print("\n=== Database Monitoring Demo ===")
    
    # Создание монитора БД
    db_monitor = DatabaseMonitor()
    
    # Создание тестовой таблицы
    with db_monitor.monitored_query('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    '''):
        pass
    
    print("Выполнение тестовых запросов...")
    
    # Быстрые запросы
    for i in range(5):
        with db_monitor.monitored_query(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (f'User {i}', f'user{i}@example.com')
        ):
            pass
    
    # Запрос на чтение
    with db_monitor.monitored_query('SELECT * FROM users') as cursor:
        users = cursor.fetchall()
        print(f"Найдено пользователей: {len(users)}")
    
    # Имитация медленного запроса
    with db_monitor.monitored_query('SELECT * FROM users WHERE name LIKE ?', ('%User%',)) as cursor:
        time.sleep(0.01)  # Имитация медленной обработки
        results = cursor.fetchall()
    
    # Имитация ошибочного запроса
    try:
        with db_monitor.monitored_query('SELECT * FROM nonexistent_table'):
            pass
    except Exception:
        pass  # Ожидаемая ошибка
    
    # Получение статистики
    stats = db_monitor.get_query_statistics(hours=1)
    print(f"\nСтатистика запросов: {json.dumps(stats, indent=2)}")
    
    slowest_queries = db_monitor.get_slowest_queries(limit=3)
    print(f"\nСамые медленные запросы:")
    for query in slowest_queries:
        print(f"  - {query['query_text']} (max: {query['max_execution_time_ms']:.2f}ms)")
    
    return db_monitor

# =============================================================================
# Главная функция для демонстрации всех примеров
# =============================================================================

def main():
    """Запуск всех примеров логирования и мониторинга"""
    print("=== Логирование и мониторинг в Python ===\n")
    
    # 1. Структурированное логирование
    logger = structured_logging_demo()
    
    # 2. Декораторы для логирования
    service = logging_decorators_demo()
    
    # 3. Мониторинг производительности
    monitor, request_tracker = performance_monitoring_demo()
    
    # 4. Система оповещений
    alert_manager = alerting_system_demo()
    
    # 5. Мониторинг базы данных
    db_monitor = database_monitoring_demo()
    
    print("\n=== Сводка ===")
    print("✅ Структурированное логирование с JSON форматом")
    print("✅ Декораторы для автоматического логирования функций")
    print("✅ Мониторинг производительности системы и приложения")
    print("✅ Трекинг HTTP запросов и метрик")
    print("✅ Система оповещений с правилами и обработчиками")
    print("✅ Мониторинг базы данных и SQL запросов")
    print("✅ Сбор и анализ метрик в реальном времени")
    print("✅ Интеграция с системами уведомлений")
    
    print("\nВсе примеры демонстрируют современные подходы к логированию и мониторингу! 📊📈")

if __name__ == "__main__":
    main() 