#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Работа с файлами Python

Этот файл содержит практические упражнения для закрепления знаний:
- Основные операции с файлами
- Работа с различными кодировками
- Использование контекстных менеджеров
- Работа с путями и директориями
- Обработка различных форматов файлов
- Создание архивов и работа с ними
- Оптимизация для больших файлов

Каждое упражнение включает:
- Подробное описание задачи
- Примеры входных и выходных данных
- Решение с комментариями
"""

import os
import json
import csv
import zipfile
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import time


def exercise_01_file_log_analyzer():
    """
    Упражнение 1: Анализатор лог-файлов
    
    Задача:
    Создайте систему для анализа лог-файлов веб-сервера.
    Система должна:
    1. Читать лог-файл построчно (для больших файлов)
    2. Парсить каждую строку лога
    3. Собирать статистику (IP адреса, коды ответов, популярные страницы)
    4. Сохранять результаты в JSON и CSV форматах
    5. Обрабатывать ошибки кодировки
    
    Формат лога: IP - - [дата] "метод URL версия" код размер
    Пример: 192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
    """
    print("=== Упражнение 1: Анализатор лог-файлов ===")
    
    # Создаем тестовый лог-файл
    sample_log = """192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
192.168.1.2 - - [10/Oct/2023:13:55:37 +0000] "GET /about.html HTTP/1.1" 200 1024
192.168.1.1 - - [10/Oct/2023:13:55:38 +0000] "POST /login HTTP/1.1" 200 512
192.168.1.3 - - [10/Oct/2023:13:55:39 +0000] "GET /nonexistent.html HTTP/1.1" 404 196
192.168.1.2 - - [10/Oct/2023:13:55:40 +0000] "GET /index.html HTTP/1.1" 200 2326
192.168.1.4 - - [10/Oct/2023:13:55:41 +0000] "GET /api/users HTTP/1.1" 500 89
192.168.1.1 - - [10/Oct/2023:13:55:42 +0000] "GET /about.html HTTP/1.1" 200 1024"""
    
    log_file = "access.log"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(sample_log)
    
    print("Тестовый лог-файл создан")
    
    # ЗАДАЧА: Реализуйте LogAnalyzer
    
    """
    # РЕШЕНИЕ:
    
    import re
    from collections import defaultdict, Counter
    
    class LogAnalyzer:
        def __init__(self):
            self.ip_stats = Counter()
            self.status_stats = Counter()
            self.url_stats = Counter()
            self.method_stats = Counter()
            self.total_requests = 0
            self.total_bytes = 0
            self.errors = []
        
        def parse_log_line(self, line):
            # Регулярное выражение для парсинга лога
            pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(\w+) (.*?) HTTP/1\.\d" (\d+) (\d+)'
            match = re.match(pattern, line.strip())
            
            if match:
                ip, timestamp, method, url, status, size = match.groups()
                return {
                    'ip': ip,
                    'timestamp': timestamp,
                    'method': method,
                    'url': url,
                    'status': int(status),
                    'size': int(size)
                }
            return None
        
        def analyze_file(self, filename):
            try:
                with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                    for line_num, line in enumerate(f, 1):
                        try:
                            parsed = self.parse_log_line(line)
                            if parsed:
                                self.ip_stats[parsed['ip']] += 1
                                self.status_stats[parsed['status']] += 1
                                self.url_stats[parsed['url']] += 1
                                self.method_stats[parsed['method']] += 1
                                self.total_requests += 1
                                self.total_bytes += parsed['size']
                            else:
                                self.errors.append(f"Строка {line_num}: не удалось распарсить")
                        except Exception as e:
                            self.errors.append(f"Строка {line_num}: {e}")
            except Exception as e:
                self.errors.append(f"Ошибка чтения файла: {e}")
        
        def get_statistics(self):
            return {
                'total_requests': self.total_requests,
                'total_bytes': self.total_bytes,
                'unique_ips': len(self.ip_stats),
                'top_ips': dict(self.ip_stats.most_common(10)),
                'status_codes': dict(self.status_stats),
                'top_urls': dict(self.url_stats.most_common(10)),
                'methods': dict(self.method_stats),
                'errors': self.errors
            }
        
        def save_results(self, json_file, csv_file):
            stats = self.get_statistics()
            
            # Сохранение в JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            # Сохранение в CSV (топ IP адреса)
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['IP', 'Requests'])
                for ip, count in self.ip_stats.most_common():
                    writer.writerow([ip, count])
    
    # Использование
    analyzer = LogAnalyzer()
    analyzer.analyze_file(log_file)
    stats = analyzer.get_statistics()
    
    print(f"Обработано запросов: {stats['total_requests']}")
    print(f"Уникальных IP: {stats['unique_ips']}")
    print(f"Топ IP адреса: {stats['top_ips']}")
    
    analyzer.save_results('log_stats.json', 'top_ips.csv')
    print("Результаты сохранены в log_stats.json и top_ips.csv")
    """
    
    # Очистка
    try:
        os.unlink(log_file)
        os.unlink('log_stats.json')
        os.unlink('top_ips.csv')
    except FileNotFoundError:
        pass


def exercise_02_config_manager():
    """
    Упражнение 2: Менеджер конфигураций
    
    Задача:
    Создайте универсальный менеджер конфигураций, который:
    1. Поддерживает JSON, INI и YAML форматы
    2. Автоматически определяет формат по расширению файла
    3. Валидирует конфигурацию по схеме
    4. Создает резервные копии при изменении
    5. Отслеживает изменения файлов конфигурации
    6. Поддерживает переменные окружения в значениях
    """
    print("=== Упражнение 2: Менеджер конфигураций ===")
    
    # Создаем тестовые конфигурации
    test_configs = {
        'app.json': {
            "database": {
                "host": "${DB_HOST:localhost}",
                "port": 5432,
                "name": "myapp"
            },
            "api": {
                "debug": True,
                "timeout": 30
            }
        },
        'app.ini': """[database]
host = ${DB_HOST:localhost}
port = 5432
name = myapp

[api]
debug = true
timeout = 30"""
    }
    
    # Создаем файлы
    with open('app.json', 'w') as f:
        json.dump(test_configs['app.json'], f, indent=2)
    
    with open('app.ini', 'w') as f:
        f.write(test_configs['app.ini'])
    
    print("Тестовые конфигурации созданы")
    
    # ЗАДАЧА: Реализуйте ConfigManager
    
    """
    # РЕШЕНИЕ:
    
    import configparser
    import re
    import threading
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    
    class ConfigManager:
        def __init__(self):
            self.configs = {}
            self.schemas = {}
            self.observers = {}
            self.lock = threading.Lock()
        
        def load_config(self, filename, schema=None):
            path = Path(filename)
            
            if not path.exists():
                raise FileNotFoundError(f"Конфигурация {filename} не найдена")
            
            # Создаем резервную копию
            backup_path = path.with_suffix(path.suffix + '.backup')
            if path.exists():
                shutil.copy2(path, backup_path)
            
            # Загружаем в зависимости от формата
            if path.suffix.lower() == '.json':
                config = self._load_json(path)
            elif path.suffix.lower() == '.ini':
                config = self._load_ini(path)
            elif path.suffix.lower() in ['.yml', '.yaml']:
                config = self._load_yaml(path)
            else:
                raise ValueError(f"Неподдерживаемый формат: {path.suffix}")
            
            # Обрабатываем переменные окружения
            config = self._process_env_vars(config)
            
            # Валидируем если есть схема
            if schema:
                self._validate_config(config, schema)
                self.schemas[filename] = schema
            
            with self.lock:
                self.configs[filename] = config
            
            return config
        
        def _load_json(self, path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        def _load_ini(self, path):
            config = configparser.ConfigParser()
            config.read(path, encoding='utf-8')
            
            # Преобразуем в обычный словарь
            result = {}
            for section in config.sections():
                result[section] = dict(config[section])
            return result
        
        def _process_env_vars(self, obj):
            if isinstance(obj, dict):
                return {k: self._process_env_vars(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [self._process_env_vars(item) for item in obj]
            elif isinstance(obj, str):
                # Ищем паттерн ${VAR:default}
                pattern = r'\$\{([^:}]+)(?::([^}]*))?\}'
                
                def replacer(match):
                    var_name = match.group(1)
                    default_value = match.group(2) or ''
                    return os.environ.get(var_name, default_value)
                
                return re.sub(pattern, replacer, obj)
            else:
                return obj
        
        def _validate_config(self, config, schema):
            # Простая валидация по схеме
            def validate_dict(data, schema_dict):
                for key, expected_type in schema_dict.items():
                    if key not in data:
                        raise ValueError(f"Отсутствует обязательный ключ: {key}")
                    if not isinstance(data[key], expected_type):
                        raise TypeError(f"Неверный тип для {key}: ожидается {expected_type}")
            
            if isinstance(schema, dict):
                validate_dict(config, schema)
        
        def save_config(self, filename, config=None):
            if config is None:
                config = self.configs.get(filename)
                if config is None:
                    raise ValueError(f"Конфигурация {filename} не загружена")
            
            path = Path(filename)
            
            # Создаем резервную копию
            if path.exists():
                backup_path = path.with_suffix(path.suffix + '.backup')
                shutil.copy2(path, backup_path)
            
            # Сохраняем в зависимости от формата
            if path.suffix.lower() == '.json':
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
            elif path.suffix.lower() == '.ini':
                self._save_ini(path, config)
            else:
                raise ValueError(f"Неподдерживаемый формат для сохранения: {path.suffix}")
            
            with self.lock:
                self.configs[filename] = config
        
        def _save_ini(self, path, config):
            parser = configparser.ConfigParser()
            
            for section, values in config.items():
                parser.add_section(section)
                for key, value in values.items():
                    parser.set(section, key, str(value))
            
            with open(path, 'w', encoding='utf-8') as f:
                parser.write(f)
        
        def get_value(self, filename, key_path, default=None):
            config = self.configs.get(filename)
            if config is None:
                return default
            
            # Поддержка вложенных ключей: "database.host"
            keys = key_path.split('.')
            value = config
            
            try:
                for key in keys:
                    value = value[key]
                return value
            except (KeyError, TypeError):
                return default
        
        def set_value(self, filename, key_path, value):
            config = self.configs.get(filename)
            if config is None:
                raise ValueError(f"Конфигурация {filename} не загружена")
            
            keys = key_path.split('.')
            current = config
            
            # Создаем вложенную структуру если нужно
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            current[keys[-1]] = value
            
            # Автоматически сохраняем
            self.save_config(filename, config)
        
        def watch_config(self, filename, callback=None):
            # Настройка мониторинга изменений файла
            class ConfigHandler(FileSystemEventHandler):
                def __init__(self, manager, filename, callback):
                    self.manager = manager
                    self.filename = filename
                    self.callback = callback
                
                def on_modified(self, event):
                    if event.src_path.endswith(self.filename):
                        print(f"Конфигурация {self.filename} изменена, перезагружаем...")
                        try:
                            schema = self.manager.schemas.get(self.filename)
                            self.manager.load_config(self.filename, schema)
                            if self.callback:
                                self.callback(self.filename)
                        except Exception as e:
                            print(f"Ошибка перезагрузки конфигурации: {e}")
            
            observer = Observer()
            event_handler = ConfigHandler(self, filename, callback)
            observer.schedule(event_handler, str(Path(filename).parent), recursive=False)
            observer.start()
            
            self.observers[filename] = observer
            return observer
    
    # Пример использования
    manager = ConfigManager()
    
    # Схема валидации
    schema = {
        'database': dict,
        'api': dict
    }
    
    # Загружаем конфигурации
    config = manager.load_config('app.json', schema)
    print("JSON конфигурация загружена:", config)
    
    ini_config = manager.load_config('app.ini')
    print("INI конфигурация загружена:", ini_config)
    
    # Получаем значения
    db_host = manager.get_value('app.json', 'database.host')
    print(f"DB Host: {db_host}")
    
    # Изменяем значение
    manager.set_value('app.json', 'api.timeout', 60)
    print("Timeout изменен на 60")
    """
    
    # Очистка
    test_files = ['app.json', 'app.ini', 'app.json.backup', 'app.ini.backup']
    for filename in test_files:
        try:
            os.unlink(filename)
        except FileNotFoundError:
            pass


def exercise_03_file_synchronizer():
    """
    Упражнение 3: Синхронизатор файлов
    
    Задача:
    Создайте систему синхронизации файлов между двумя директориями:
    1. Сравнивает файлы по содержимому (хеш) и времени изменения
    2. Синхронизирует в обоих направлениях
    3. Создает инкрементальные резервные копии
    4. Ведет лог всех операций
    5. Поддерживает исключения (паттерны файлов)
    6. Может работать с архивами
    """
    print("=== Упражнение 3: Синхронизатор файлов ===")
    
    # Создаем тестовые директории
    source_dir = Path('sync_source')
    target_dir = Path('sync_target')
    
    source_dir.mkdir(exist_ok=True)
    target_dir.mkdir(exist_ok=True)
    
    # Создаем тестовые файлы
    (source_dir / 'file1.txt').write_text('Содержимое файла 1', encoding='utf-8')
    (source_dir / 'file2.txt').write_text('Содержимое файла 2', encoding='utf-8')
    (source_dir / 'subdir').mkdir(exist_ok=True)
    (source_dir / 'subdir' / 'nested.txt').write_text('Вложенный файл', encoding='utf-8')
    
    (target_dir / 'file2.txt').write_text('Изменённое содержимое файла 2', encoding='utf-8')
    (target_dir / 'file3.txt').write_text('Содержимое файла 3', encoding='utf-8')
    
    print("Тестовые директории созданы")
    
    # ЗАДАЧА: Реализуйте FileSynchronizer
    
    """
    # РЕШЕНИЕ:
    
    import hashlib
    import fnmatch
    from typing import List, Set, Tuple
    
    class FileSynchronizer:
        def __init__(self, log_file='sync.log'):
            self.log_file = log_file
            self.exclude_patterns = []
        
        def add_exclude_pattern(self, pattern):
            self.exclude_patterns.append(pattern)
        
        def _should_exclude(self, path):
            for pattern in self.exclude_patterns:
                if fnmatch.fnmatch(str(path), pattern):
                    return True
            return False
        
        def _calculate_hash(self, file_path):
            hash_obj = hashlib.md5()
            try:
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        hash_obj.update(chunk)
                return hash_obj.hexdigest()
            except Exception:
                return None
        
        def _log_operation(self, operation, source, target=None):
            timestamp = datetime.now().isoformat()
            message = f"[{timestamp}] {operation}: {source}"
            if target:
                message += f" -> {target}"
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
            print(message)
        
        def _get_file_info(self, directory):
            file_info = {}
            
            for file_path in Path(directory).rglob('*'):
                if file_path.is_file() and not self._should_exclude(file_path):
                    relative_path = file_path.relative_to(directory)
                    stat = file_path.stat()
                    
                    file_info[str(relative_path)] = {
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'hash': self._calculate_hash(file_path),
                        'full_path': file_path
                    }
            
            return file_info
        
        def _copy_file(self, source_path, target_path):
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
        
        def _create_backup(self, file_path, backup_dir):
            backup_dir = Path(backup_dir)
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = backup_dir / backup_name
            
            shutil.copy2(file_path, backup_path)
            return backup_path
        
        def sync_directories(self, source_dir, target_dir, bidirectional=False, backup_dir=None):
            source_dir = Path(source_dir)
            target_dir = Path(target_dir)
            
            self._log_operation("SYNC_START", f"{source_dir} -> {target_dir}")
            
            # Получаем информацию о файлах
            source_files = self._get_file_info(source_dir)
            target_files = self._get_file_info(target_dir)
            
            # Файлы только в источнике (нужно копировать)
            source_only = set(source_files.keys()) - set(target_files.keys())
            
            # Файлы только в цели (нужно удалить или скопировать обратно)
            target_only = set(target_files.keys()) - set(source_files.keys())
            
            # Общие файлы (нужно сравнить)
            common_files = set(source_files.keys()) & set(target_files.keys())
            
            # Копируем новые файлы из источника
            for rel_path in source_only:
                source_path = source_files[rel_path]['full_path']
                target_path = target_dir / rel_path
                
                self._copy_file(source_path, target_path)
                self._log_operation("COPY", source_path, target_path)
            
            # Обрабатываем общие файлы
            for rel_path in common_files:
                source_info = source_files[rel_path]
                target_info = target_files[rel_path]
                
                # Сравниваем по хешу
                if source_info['hash'] != target_info['hash']:
                    # Создаем резервную копию если нужно
                    if backup_dir:
                        backup_path = self._create_backup(
                            target_info['full_path'], 
                            Path(backup_dir) / 'target'
                        )
                        self._log_operation("BACKUP", target_info['full_path'], backup_path)
                    
                    # Копируем более новую версию
                    if source_info['mtime'] > target_info['mtime']:
                        self._copy_file(source_info['full_path'], target_info['full_path'])
                        self._log_operation("UPDATE", source_info['full_path'], target_info['full_path'])
                    elif bidirectional and target_info['mtime'] > source_info['mtime']:
                        self._copy_file(target_info['full_path'], source_info['full_path'])
                        self._log_operation("UPDATE_BACK", target_info['full_path'], source_info['full_path'])
            
            # Обрабатываем файлы только в цели
            if bidirectional:
                for rel_path in target_only:
                    target_path = target_files[rel_path]['full_path']
                    source_path = source_dir / rel_path
                    
                    self._copy_file(target_path, source_path)
                    self._log_operation("COPY_BACK", target_path, source_path)
            
            self._log_operation("SYNC_COMPLETE", f"{source_dir} -> {target_dir}")
            
            return {
                'copied': len(source_only),
                'updated': len([f for f in common_files 
                               if source_files[f]['hash'] != target_files[f]['hash']]),
                'copied_back': len(target_only) if bidirectional else 0
            }
        
        def create_archive_backup(self, directory, archive_path):
            directory = Path(directory)
            archive_path = Path(archive_path)
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in directory.rglob('*'):
                    if file_path.is_file() and not self._should_exclude(file_path):
                        arcname = file_path.relative_to(directory)
                        zipf.write(file_path, arcname)
            
            self._log_operation("ARCHIVE_CREATED", directory, archive_path)
            return archive_path
    
    # Пример использования
    synchronizer = FileSynchronizer()
    
    # Добавляем исключения
    synchronizer.add_exclude_pattern('*.tmp')
    synchronizer.add_exclude_pattern('*.log')
    
    # Синхронизируем
    result = synchronizer.sync_directories(
        source_dir, 
        target_dir, 
        bidirectional=True,
        backup_dir='sync_backups'
    )
    
    print(f"Результат синхронизации: {result}")
    
    # Создаем архивную копию
    archive_path = synchronizer.create_archive_backup(source_dir, 'source_backup.zip')
    print(f"Архив создан: {archive_path}")
    """
    
    # Очистка
    cleanup_items = [source_dir, target_dir, 'sync_backups', 'sync.log', 'source_backup.zip']
    for item in cleanup_items:
        try:
            if Path(item).is_dir():
                shutil.rmtree(item)
            else:
                os.unlink(item)
        except (FileNotFoundError, OSError):
            pass


def exercise_04_data_processor():
    """
    Упражнение 4: Обработчик больших данных
    
    Задача:
    Создайте систему для обработки больших CSV файлов:
    1. Читает файл порциями (chunk-based processing)
    2. Применяет фильтры и трансформации
    3. Агрегирует данные (сумма, среднее, группировка)
    4. Сохраняет результаты в различных форматах
    5. Показывает прогресс обработки
    6. Обрабатывает ошибки в данных
    """
    print("=== Упражнение 4: Обработчик больших данных ===")
    
    # Создаем большой тестовый CSV файл
    import random
    
    csv_file = "large_sales_data.csv"
    
    # Генерируем тестовые данные
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Tablet']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Product', 'Region', 'Sales', 'Quantity', 'Price'])
        
        # Генерируем 10000 записей
        for i in range(10000):
            date = f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            product = random.choice(products)
            region = random.choice(regions)
            quantity = random.randint(1, 100)
            price = round(random.uniform(10, 1000), 2)
            sales = round(quantity * price, 2)
            
            writer.writerow([date, product, region, sales, quantity, price])
    
    print(f"Создан тестовый файл {csv_file} с 10000 записями")
    
    # ЗАДАЧА: Реализуйте DataProcessor
    
    """
    # РЕШЕНИЕ:
    
    from typing import Iterator, Dict, Any, Callable
    import pandas as pd  # Для более эффективной обработки
    
    class DataProcessor:
        def __init__(self, chunk_size=1000):
            self.chunk_size = chunk_size
            self.filters = []
            self.transformations = []
            self.aggregations = {}
        
        def add_filter(self, condition: Callable[[Dict], bool]):
            self.filters.append(condition)
        
        def add_transformation(self, field: str, transform_func: Callable):
            self.transformations.append((field, transform_func))
        
        def add_aggregation(self, field: str, agg_type: str, group_by=None):
            if group_by not in self.aggregations:
                self.aggregations[group_by] = {}
            self.aggregations[group_by][field] = agg_type
        
        def read_csv_chunks(self, filename: str) -> Iterator[List[Dict]]:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                chunk = []
                for row in reader:
                    try:
                        # Преобразуем числовые поля
                        for field in ['Sales', 'Quantity', 'Price']:
                            if field in row:
                                row[field] = float(row[field])
                        
                        chunk.append(row)
                        
                        if len(chunk) >= self.chunk_size:
                            yield chunk
                            chunk = []
                    
                    except ValueError as e:
                        print(f"Ошибка в строке: {row}, пропускаем: {e}")
                        continue
                
                if chunk:
                    yield chunk
        
        def process_chunk(self, chunk: List[Dict]) -> List[Dict]:
            processed = []
            
            for row in chunk:
                # Применяем фильтры
                if all(filter_func(row) for filter_func in self.filters):
                    # Применяем трансформации
                    for field, transform_func in self.transformations:
                        if field in row:
                            try:
                                row[field] = transform_func(row[field])
                            except Exception as e:
                                print(f"Ошибка трансформации {field}: {e}")
                    
                    processed.append(row)
            
            return processed
        
        def process_file(self, input_file: str, output_file: str = None):
            results = []
            total_rows = 0
            processed_rows = 0
            
            # Подсчитываем общее количество строк для прогресса
            with open(input_file, 'r', encoding='utf-8') as f:
                total_rows = sum(1 for _ in f) - 1  # -1 для заголовка
            
            print(f"Обрабатываем {total_rows} строк...")
            
            # Обрабатываем по частям
            for chunk_num, chunk in enumerate(self.read_csv_chunks(input_file)):
                processed_chunk = self.process_chunk(chunk)
                results.extend(processed_chunk)
                
                processed_rows += len(chunk)
                progress = (processed_rows / total_rows) * 100
                print(f"Прогресс: {progress:.1f}% ({processed_rows}/{total_rows})")
            
            print(f"Обработано {len(results)} строк из {total_rows}")
            
            # Сохраняем результаты если указан файл
            if output_file:
                self.save_results(results, output_file)
            
            return results
        
        def calculate_aggregations(self, data: List[Dict]):
            from collections import defaultdict
            
            aggregated = {}
            
            for group_field, aggs in self.aggregations.items():
                if group_field is None:
                    # Глобальная агрегация
                    result = {}
                    for field, agg_type in aggs.items():
                        values = [float(row[field]) for row in data if field in row]
                        
                        if agg_type == 'sum':
                            result[f"{field}_sum"] = sum(values)
                        elif agg_type == 'avg':
                            result[f"{field}_avg"] = sum(values) / len(values) if values else 0
                        elif agg_type == 'count':
                            result[f"{field}_count"] = len(values)
                        elif agg_type == 'min':
                            result[f"{field}_min"] = min(values) if values else 0
                        elif agg_type == 'max':
                            result[f"{field}_max"] = max(values) if values else 0
                    
                    aggregated['global'] = result
                
                else:
                    # Группировка
                    groups = defaultdict(list)
                    for row in data:
                        group_value = row.get(group_field, 'Unknown')
                        groups[group_value].append(row)
                    
                    group_results = {}
                    for group_value, group_data in groups.items():
                        result = {}
                        for field, agg_type in aggs.items():
                            values = [float(row[field]) for row in group_data if field in row]
                            
                            if agg_type == 'sum':
                                result[f"{field}_sum"] = sum(values)
                            elif agg_type == 'avg':
                                result[f"{field}_avg"] = sum(values) / len(values) if values else 0
                            elif agg_type == 'count':
                                result[f"{field}_count"] = len(values)
                        
                        group_results[group_value] = result
                    
                    aggregated[f'by_{group_field}'] = group_results
            
            return aggregated
        
        def save_results(self, data: List[Dict], filename: str):
            path = Path(filename)
            
            if path.suffix.lower() == '.json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            elif path.suffix.lower() == '.csv':
                if data:
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
            
            print(f"Результаты сохранены в {filename}")
    
    # Пример использования
    processor = DataProcessor(chunk_size=500)
    
    # Добавляем фильтры
    processor.add_filter(lambda row: row['Sales'] > 100)  # Продажи больше 100
    processor.add_filter(lambda row: row['Region'] in ['North', 'South'])  # Только север и юг
    
    # Добавляем трансформации
    processor.add_transformation('Product', lambda x: x.upper())  # Продукты в верхнем регистре
    processor.add_transformation('Sales', lambda x: round(x, 0))  # Округляем продажи
    
    # Добавляем агрегации
    processor.add_aggregation('Sales', 'sum')
    processor.add_aggregation('Sales', 'avg')
    processor.add_aggregation('Quantity', 'sum')
    
    processor.add_aggregation('Sales', 'sum', group_by='Region')
    processor.add_aggregation('Sales', 'avg', group_by='Product')
    
    # Обрабатываем файл
    filtered_data = processor.process_file(csv_file, 'filtered_sales.csv')
    
    # Вычисляем агрегации
    aggregations = processor.calculate_aggregations(filtered_data)
    
    # Сохраняем агрегации
    with open('sales_aggregations.json', 'w', encoding='utf-8') as f:
        json.dump(aggregations, f, ensure_ascii=False, indent=2)
    
    print("Агрегации:")
    for key, value in aggregations.items():
        print(f"  {key}: {value}")
    """
    
    # Очистка
    cleanup_files = [csv_file, 'filtered_sales.csv', 'sales_aggregations.json']
    for filename in cleanup_files:
        try:
            os.unlink(filename)
        except FileNotFoundError:
            pass


def exercise_05_backup_system():
    """
    Упражнение 5: Система резервного копирования
    
    Задача:
    Создайте полнофункциональную систему резервного копирования:
    1. Поддерживает полные и инкрементальные копии
    2. Сжимает архивы с различными алгоритмами
    3. Шифрует важные данные
    4. Проверяет целостность архивов
    5. Ведет базу данных резервных копий
    6. Автоматически удаляет старые копии по политике
    """
    print("=== Упражнение 5: Система резервного копирования ===")
    
    # Создаем тестовую структуру для бэкапа
    test_dir = Path('backup_test_data')
    test_dir.mkdir(exist_ok=True)
    
    # Создаем файлы разных типов
    (test_dir / 'documents').mkdir(exist_ok=True)
    (test_dir / 'documents' / 'report.txt').write_text('Важный отчет', encoding='utf-8')
    (test_dir / 'documents' / 'data.json').write_text('{"key": "value"}', encoding='utf-8')
    
    (test_dir / 'images').mkdir(exist_ok=True)
    (test_dir / 'images' / 'photo.jpg').write_bytes(b'fake_image_data' * 100)
    
    (test_dir / 'config.ini').write_text('[app]\nkey=value', encoding='utf-8')
    
    print("Тестовые данные для бэкапа созданы")
    
    # ЗАДАЧА: Реализуйте BackupSystem
    
    """
    # РЕШЕНИЕ:
    
    import sqlite3
    from cryptography.fernet import Fernet
    import tarfile
    import gzip
    
    class BackupSystem:
        def __init__(self, backup_dir='backups', db_file='backups.db'):
            self.backup_dir = Path(backup_dir)
            self.backup_dir.mkdir(exist_ok=True)
            self.db_file = db_file
            self.encryption_key = None
            
            self._init_database()
        
        def _init_database(self):
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backups (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    type TEXT,
                    source_path TEXT,
                    archive_path TEXT,
                    compression TEXT,
                    encrypted BOOLEAN,
                    checksum TEXT,
                    size INTEGER,
                    files_count INTEGER
                )
            ''')
            
            conn.commit()
            conn.close()
        
        def generate_encryption_key(self):
            self.encryption_key = Fernet.generate_key()
            
            # Сохраняем ключ в файл
            key_file = self.backup_dir / 'encryption.key'
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            
            return self.encryption_key
        
        def load_encryption_key(self, key_file=None):
            if key_file is None:
                key_file = self.backup_dir / 'encryption.key'
            
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
            
            return self.encryption_key
        
        def _calculate_checksum(self, file_path):
            import hashlib
            hash_obj = hashlib.sha256()
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
        
        def _get_directory_files(self, directory):
            files = []
            for file_path in Path(directory).rglob('*'):
                if file_path.is_file():
                    files.append(file_path)
            return files
        
        def create_full_backup(self, source_path, compression='gzip', encrypt=False):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            source_name = Path(source_path).name
            
            # Имя архива
            if compression == 'gzip':
                archive_name = f"{source_name}_full_{timestamp}.tar.gz"
            elif compression == 'bzip2':
                archive_name = f"{source_name}_full_{timestamp}.tar.bz2"
            else:
                archive_name = f"{source_name}_full_{timestamp}.tar"
            
            archive_path = self.backup_dir / archive_name
            
            # Создаем архив
            if compression == 'gzip':
                mode = 'w:gz'
            elif compression == 'bzip2':
                mode = 'w:bz2'
            else:
                mode = 'w'
            
            files_count = 0
            
            with tarfile.open(archive_path, mode) as tar:
                for file_path in self._get_directory_files(source_path):
                    arcname = file_path.relative_to(source_path)
                    tar.add(file_path, arcname)
                    files_count += 1
            
            # Шифрование если нужно
            if encrypt:
                if self.encryption_key is None:
                    self.generate_encryption_key()
                
                encrypted_path = archive_path.with_suffix(archive_path.suffix + '.enc')
                
                fernet = Fernet(self.encryption_key)
                
                with open(archive_path, 'rb') as f:
                    data = f.read()
                
                encrypted_data = fernet.encrypt(data)
                
                with open(encrypted_path, 'wb') as f:
                    f.write(encrypted_data)
                
                # Удаляем незашифрованный файл
                archive_path.unlink()
                archive_path = encrypted_path
            
            # Вычисляем контрольную сумму
            checksum = self._calculate_checksum(archive_path)
            size = archive_path.stat().st_size
            
            # Записываем в базу данных
            self._record_backup(
                timestamp, 'full', source_path, str(archive_path),
                compression, encrypt, checksum, size, files_count
            )
            
            print(f"Полный бэкап создан: {archive_path} ({size} байт, {files_count} файлов)")
            return archive_path
        
        def create_incremental_backup(self, source_path, base_backup_id=None, compression='gzip', encrypt=False):
            # Находим последний полный бэкап если не указан
            if base_backup_id is None:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                
                cursor.execute(
                    'SELECT id FROM backups WHERE source_path = ? AND type = "full" ORDER BY timestamp DESC LIMIT 1',
                    (str(source_path),)
                )
                result = cursor.fetchone()
                conn.close()
                
                if not result:
                    raise ValueError("Не найден базовый полный бэкап")
                
                base_backup_id = result[0]
            
            # Получаем время последнего бэкапа
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT timestamp FROM backups WHERE id = ?', (base_backup_id,))
            base_timestamp = cursor.fetchone()[0]
            conn.close()
            
            base_time = datetime.fromisoformat(base_timestamp)
            
            # Находим измененные файлы
            changed_files = []
            for file_path in self._get_directory_files(source_path):
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_mtime > base_time:
                    changed_files.append(file_path)
            
            if not changed_files:
                print("Нет измененных файлов для инкрементального бэкапа")
                return None
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            source_name = Path(source_path).name
            
            # Создаем инкрементальный архив
            if compression == 'gzip':
                archive_name = f"{source_name}_inc_{timestamp}.tar.gz"
                mode = 'w:gz'
            elif compression == 'bzip2':
                archive_name = f"{source_name}_inc_{timestamp}.tar.bz2"
                mode = 'w:bz2'
            else:
                archive_name = f"{source_name}_inc_{timestamp}.tar"
                mode = 'w'
            
            archive_path = self.backup_dir / archive_name
            
            with tarfile.open(archive_path, mode) as tar:
                for file_path in changed_files:
                    arcname = file_path.relative_to(source_path)
                    tar.add(file_path, arcname)
            
            # Шифрование если нужно
            if encrypt:
                if self.encryption_key is None:
                    raise ValueError("Ключ шифрования не загружен")
                
                encrypted_path = archive_path.with_suffix(archive_path.suffix + '.enc')
                
                fernet = Fernet(self.encryption_key)
                
                with open(archive_path, 'rb') as f:
                    encrypted_data = fernet.encrypt(f.read())
                
                with open(encrypted_path, 'wb') as f:
                    f.write(encrypted_data)
                
                archive_path.unlink()
                archive_path = encrypted_path
            
            # Записываем в базу
            checksum = self._calculate_checksum(archive_path)
            size = archive_path.stat().st_size
            
            self._record_backup(
                timestamp, 'incremental', source_path, str(archive_path),
                compression, encrypt, checksum, size, len(changed_files)
            )
            
            print(f"Инкрементальный бэкап создан: {archive_path} ({len(changed_files)} измененных файлов)")
            return archive_path
        
        def _record_backup(self, timestamp, backup_type, source_path, archive_path, 
                          compression, encrypted, checksum, size, files_count):
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO backups (timestamp, type, source_path, archive_path, 
                                   compression, encrypted, checksum, size, files_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), backup_type, str(source_path), 
                  archive_path, compression, encrypted, checksum, size, files_count))
            
            conn.commit()
            conn.close()
        
        def verify_backup(self, backup_id):
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM backups WHERE id = ?', (backup_id,))
            backup = cursor.fetchone()
            conn.close()
            
            if not backup:
                return False, "Бэкап не найден"
            
            archive_path = Path(backup[4])  # archive_path
            stored_checksum = backup[7]     # checksum
            
            if not archive_path.exists():
                return False, f"Файл архива не найден: {archive_path}"
            
            # Проверяем контрольную сумму
            current_checksum = self._calculate_checksum(archive_path)
            
            if current_checksum != stored_checksum:
                return False, f"Контрольная сумма не совпадает"
            
            return True, "Бэкап корректен"
        
        def list_backups(self, source_path=None):
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            if source_path:
                cursor.execute('SELECT * FROM backups WHERE source_path = ? ORDER BY timestamp DESC',
                             (str(source_path),))
            else:
                cursor.execute('SELECT * FROM backups ORDER BY timestamp DESC')
            
            backups = cursor.fetchall()
            conn.close()
            
            return backups
        
        def cleanup_old_backups(self, keep_days=30, keep_count=10):
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Находим старые бэкапы
            cursor.execute('''
                SELECT id, archive_path FROM backups 
                WHERE timestamp < ? 
                ORDER BY timestamp DESC 
                OFFSET ?
            ''', (cutoff_date.isoformat(), keep_count))
            
            old_backups = cursor.fetchall()
            
            for backup_id, archive_path in old_backups:
                # Удаляем файл
                try:
                    Path(archive_path).unlink()
                except FileNotFoundError:
                    pass
                
                # Удаляем запись из БД
                cursor.execute('DELETE FROM backups WHERE id = ?', (backup_id,))
            
            conn.commit()
            conn.close()
            
            print(f"Удалено {len(old_backups)} старых бэкапов")
            return len(old_backups)
    
    # Пример использования
    backup_system = BackupSystem()
    
    # Создаем полный бэкап
    archive1 = backup_system.create_full_backup(
        test_dir, 
        compression='gzip', 
        encrypt=True
    )
    
    # Имитируем изменения
    time.sleep(1)
    (test_dir / 'documents' / 'new_file.txt').write_text('Новый файл', encoding='utf-8')
    
    # Создаем инкрементальный бэкап
    archive2 = backup_system.create_incremental_backup(
        test_dir,
        compression='gzip',
        encrypt=True
    )
    
    # Список бэкапов
    backups = backup_system.list_backups(test_dir)
    print("\nСписок бэкапов:")
    for backup in backups:
        print(f"  ID: {backup[0]}, Тип: {backup[2]}, Время: {backup[1]}, Файлов: {backup[9]}")
    
    # Проверяем целостность
    for backup in backups:
        valid, message = backup_system.verify_backup(backup[0])
        print(f"  Бэкап {backup[0]}: {'✓' if valid else '✗'} {message}")
    """
    
    # Очистка
    cleanup_items = [test_dir, 'backups', 'backups.db']
    for item in cleanup_items:
        try:
            if Path(item).is_dir():
                shutil.rmtree(item)
            else:
                os.unlink(item)
        except (FileNotFoundError, OSError):
            pass


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Анализатор лог-файлов", exercise_01_file_log_analyzer),
        ("Менеджер конфигураций", exercise_02_config_manager),
        ("Синхронизатор файлов", exercise_03_file_synchronizer),
        ("Обработчик больших данных", exercise_04_data_processor),
        ("Система резервного копирования", exercise_05_backup_system),
    ]
    
    print("📝 Упражнения: Работа с файлами Python")
    print("=" * 50)
    print("В каждом упражнении есть подробное описание задачи и решение.")
    print("Изучите код, попробуйте реализовать самостоятельно, затем сравните с решением.")
    print("=" * 50)
    
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
            input("\nНажмите Enter для продолжения к следующему упражнению...")


if __name__ == "__main__":
    main() 