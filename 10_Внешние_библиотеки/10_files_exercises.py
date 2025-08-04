#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Работа с файлами в Python

Этот файл содержит практические упражнения для закрепления знаний:
- Основные операции с файлами
- Обработка больших данных
- Система логирования
- Конвертация форматов
- Резервное копирование
"""

import os
import json
import csv
import time
import shutil
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Generator
import hashlib


def exercise_01_log_analyzer():
    """
    Упражнение 1: Анализатор лог-файлов
    
    Задача:
    Создайте систему анализа лог-файлов веб-сервера с возможностями:
    1. Парсинг различных форматов логов
    2. Фильтрация по времени, IP, статус-кодам
    3. Генерация статистики и отчетов
    4. Обработка больших файлов (>100MB)
    5. Экспорт результатов в различные форматы
    """
    print("=== Упражнение 1: Анализатор лог-файлов ===")
    
    # ЗАДАЧА: Создайте полнофункциональный анализатор логов
    
    # РЕШЕНИЕ:
    
    import re
    from collections import defaultdict, Counter
    
    class LogEntry:
        """Класс для представления записи лога"""
        
        def __init__(self, ip, timestamp, method, url, status, size, user_agent, referer=""):
            self.ip = ip
            self.timestamp = timestamp
            self.method = method
            self.url = url
            self.status = int(status)
            self.size = int(size) if size != '-' else 0
            self.user_agent = user_agent
            self.referer = referer
        
        def __str__(self):
            return f"{self.ip} [{self.timestamp}] {self.method} {self.url} {self.status} {self.size}"
    
    class LogParser:
        """Парсер лог-файлов"""
        
        def __init__(self):
            # Регулярные выражения для различных форматов
            self.patterns = {
                'common': re.compile(
                    r'^(\S+) \S+ \S+ \[([^]]+)\] "(\S+) (\S+) \S+" (\d+) (\S+)$'
                ),
                'combined': re.compile(
                    r'^(\S+) \S+ \S+ \[([^]]+)\] "(\S+) (\S+) \S+" (\d+) (\S+) "([^"]*)" "([^"]*)"$'
                ),
                'custom': re.compile(
                    r'^(\S+) - - \[([^]]+)\] "(\S+) ([^"]+)" (\d+) (\S+) "([^"]*)" "([^"]*)"$'
                )
            }
        
        def parse_line(self, line):
            """Парсинг одной строки лога"""
            line = line.strip()
            if not line or line.startswith('#'):
                return None
            
            # Пробуем различные форматы
            for format_name, pattern in self.patterns.items():
                match = pattern.match(line)
                if match:
                    groups = match.groups()
                    
                    if format_name == 'common':
                        ip, timestamp, method, url, status, size = groups
                        return LogEntry(ip, timestamp, method, url, status, size, "")
                    
                    elif format_name in ['combined', 'custom']:
                        ip, timestamp, method, url, status, size, referer, user_agent = groups
                        return LogEntry(ip, timestamp, method, url, status, size, user_agent, referer)
            
            return None
        
        def parse_file(self, filename):
            """Генератор для парсинга файла"""
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                    for line_num, line in enumerate(file, 1):
                        entry = self.parse_line(line)
                        if entry:
                            yield entry
                        elif line.strip():  # Не пустая строка, но не распознана
                            print(f"Не удалось распарсить строку {line_num}: {line[:50]}...")
            except FileNotFoundError:
                print(f"Файл не найден: {filename}")
            except Exception as e:
                print(f"Ошибка чтения файла: {e}")
    
    class LogAnalyzer:
        """Анализатор логов"""
        
        def __init__(self):
            self.parser = LogParser()
            self.stats = defaultdict(int)
            self.ip_stats = Counter()
            self.status_stats = Counter()
            self.url_stats = Counter()
            self.hourly_stats = defaultdict(int)
            self.error_entries = []
        
        def analyze_file(self, filename):
            """Анализ лог-файла"""
            print(f"Анализируем файл: {filename}")
            
            start_time = time.time()
            processed_lines = 0
            
            for entry in self.parser.parse_file(filename):
                self._process_entry(entry)
                processed_lines += 1
                
                if processed_lines % 10000 == 0:
                    elapsed = time.time() - start_time
                    rate = processed_lines / elapsed
                    print(f"Обработано: {processed_lines:,} строк ({rate:.0f} строк/сек)")
            
            elapsed = time.time() - start_time
            print(f"Анализ завершен: {processed_lines:,} строк за {elapsed:.2f}с")
        
        def _process_entry(self, entry):
            """Обработка одной записи"""
            # Общая статистика
            self.stats['total_requests'] += 1
            self.stats['total_bytes'] += entry.size
            
            # Статистика по IP
            self.ip_stats[entry.ip] += 1
            
            # Статистика по статус-кодам
            self.status_stats[entry.status] += 1
            
            # Статистика по URL
            self.url_stats[entry.url] += 1
            
            # Почасовая статистика
            try:
                # Парсим timestamp (формат: dd/mmm/yyyy:HH:MM:SS +0000)
                date_part = entry.timestamp.split(':')[1]  # Берем час
                self.hourly_stats[date_part] += 1
            except:
                pass
            
            # Собираем ошибки (4xx, 5xx)
            if entry.status >= 400:
                self.error_entries.append(entry)
                if entry.status >= 500:
                    self.stats['server_errors'] += 1
                elif entry.status >= 400:
                    self.stats['client_errors'] += 1
        
        def generate_report(self):
            """Генерация отчета"""
            report = {
                'summary': dict(self.stats),
                'top_ips': self.ip_stats.most_common(10),
                'status_codes': dict(self.status_stats),
                'top_urls': self.url_stats.most_common(20),
                'hourly_distribution': dict(self.hourly_stats),
                'error_rate': (self.stats['client_errors'] + self.stats['server_errors']) / max(self.stats['total_requests'], 1) * 100
            }
            
            return report
        
        def print_report(self):
            """Вывод отчета на экран"""
            report = self.generate_report()
            
            print("\n" + "="*50)
            print("ОТЧЕТ ПО АНАЛИЗУ ЛОГОВ")
            print("="*50)
            
            # Общая статистика
            print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
            print(f"  Всего запросов: {report['summary']['total_requests']:,}")
            print(f"  Передано данных: {report['summary']['total_bytes']:,} байт")
            print(f"  Клиентские ошибки (4xx): {report['summary'].get('client_errors', 0):,}")
            print(f"  Серверные ошибки (5xx): {report['summary'].get('server_errors', 0):,}")
            print(f"  Процент ошибок: {report['error_rate']:.2f}%")
            
            # Топ IP-адресов
            print(f"\n🌐 ТОП-10 IP АДРЕСОВ:")
            for ip, count in report['top_ips']:
                percentage = (count / report['summary']['total_requests']) * 100
                print(f"  {ip:15} - {count:6,} запросов ({percentage:.1f}%)")
            
            # Статус-коды
            print(f"\n📈 СТАТУС-КОДЫ:")
            for status, count in sorted(report['status_codes'].items()):
                percentage = (count / report['summary']['total_requests']) * 100
                print(f"  {status}: {count:6,} ({percentage:.1f}%)")
            
            # Топ URL
            print(f"\n🔗 ТОП-10 URL:")
            for url, count in report['top_urls'][:10]:
                percentage = (count / report['summary']['total_requests']) * 100
                print(f"  {count:6,} ({percentage:.1f}%) - {url[:60]}")
        
        def export_report(self, format='json', filename=None):
            """Экспорт отчета в файл"""
            report = self.generate_report()
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"log_report_{timestamp}.{format}"
            
            if format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            elif format == 'csv':
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Топ IP
                    writer.writerow(['Top IPs'])
                    writer.writerow(['IP', 'Requests', 'Percentage'])
                    for ip, count in report['top_ips']:
                        pct = (count / report['summary']['total_requests']) * 100
                        writer.writerow([ip, count, f"{pct:.2f}%"])
                    
                    writer.writerow([])  # Пустая строка
                    
                    # Статус коды
                    writer.writerow(['Status Codes'])
                    writer.writerow(['Status', 'Count', 'Percentage'])
                    for status, count in sorted(report['status_codes'].items()):
                        pct = (count / report['summary']['total_requests']) * 100
                        writer.writerow([status, count, f"{pct:.2f}%"])
            
            print(f"Отчет экспортирован в {filename}")
            return filename
    
    print("1. Создание тестового лог-файла:")
    
    def create_test_log_file():
        """Создание тестового лог-файла"""
        
        log_file = "test_access.log"
        
        # Шаблоны для генерации реалистичных логов
        ips = ['192.168.1.10', '10.0.0.5', '203.0.113.15', '198.51.100.25', '172.16.0.8']
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        urls = [
            '/', '/index.html', '/about', '/contact', '/products',
            '/api/users', '/api/orders', '/login', '/logout', '/search',
            '/static/css/style.css', '/static/js/app.js', '/images/logo.png'
        ]
        status_codes = [200, 200, 200, 200, 301, 302, 404, 500, 503]  # Больше успешных
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
        import random
        
        with open(log_file, 'w', encoding='utf-8') as f:
            # Генерируем записи за последние 24 часа
            base_time = datetime.now() - timedelta(days=1)
            
            for i in range(50000):  # 50k записей
                # Случайные данные
                ip = random.choice(ips)
                timestamp_dt = base_time + timedelta(seconds=random.randint(0, 86400))
                timestamp = timestamp_dt.strftime('%d/%b/%Y:%H:%M:%S +0000')
                method = random.choice(methods)
                url = random.choice(urls)
                status = random.choice(status_codes)
                size = random.randint(100, 50000)
                user_agent = random.choice(user_agents)
                
                # Формат Combined Log Format
                line = f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size} "-" "{user_agent}"\n'
                f.write(line)
        
        file_size = os.path.getsize(log_file)
        print(f"Создан тестовый лог-файл: {log_file} ({file_size:,} байт)")
        
        return log_file
    
    log_file = create_test_log_file()
    
    print("\n2. Анализ лог-файла:")
    
    analyzer = LogAnalyzer()
    analyzer.analyze_file(log_file)
    
    print("\n3. Генерация отчета:")
    analyzer.print_report()
    
    print("\n4. Экспорт отчетов:")
    json_report = analyzer.export_report('json')
    csv_report = analyzer.export_report('csv')
    
    print("\n5. Фильтрация по критериям:")
    
    class LogFilter:
        """Фильтр для логов"""
        
        def __init__(self, analyzer):
            self.analyzer = analyzer
        
        def filter_by_status(self, filename, status_codes):
            """Фильтрация по статус-кодам"""
            filtered_file = f"filtered_status_{'-'.join(map(str, status_codes))}.log"
            
            count = 0
            with open(filtered_file, 'w', encoding='utf-8') as out_file:
                for entry in self.analyzer.parser.parse_file(filename):
                    if entry.status in status_codes:
                        out_file.write(str(entry) + '\n')
                        count += 1
            
            print(f"Отфильтровано по статус-кодам {status_codes}: {count} записей → {filtered_file}")
            return filtered_file
        
        def filter_by_ip(self, filename, ip_addresses):
            """Фильтрация по IP-адресам"""
            filtered_file = f"filtered_ip.log"
            
            count = 0
            with open(filtered_file, 'w', encoding='utf-8') as out_file:
                for entry in self.analyzer.parser.parse_file(filename):
                    if entry.ip in ip_addresses:
                        out_file.write(str(entry) + '\n')
                        count += 1
            
            print(f"Отфильтровано по IP {ip_addresses}: {count} записей → {filtered_file}")
            return filtered_file
    
    # Применяем фильтры
    log_filter = LogFilter(analyzer)
    
    # Фильтр ошибок
    error_file = log_filter.filter_by_status(log_file, [404, 500, 503])
    
    # Фильтр по топ IP
    top_ips = [ip for ip, count in analyzer.ip_stats.most_common(3)]
    top_ip_file = log_filter.filter_by_ip(log_file, top_ips)
    
    print("\n6. Очистка файлов:")
    
    # Список созданных файлов
    created_files = [log_file, json_report, csv_report, error_file, top_ip_file]
    
    total_size = 0
    for filename in created_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            total_size += size
            print(f"📄 {filename}: {size:,} байт")
    
    print(f"📦 Общий размер файлов: {total_size:,} байт")
    
    # Удаляем файлы
    for filename in created_files:
        if os.path.exists(filename):
            os.remove(filename)
    
    print("✅ Все тестовые файлы удалены")


def exercise_02_data_converter():
    """
    Упражнение 2: Универсальный конвертер данных
    
    Задача:
    Создайте систему конвертации данных между форматами:
    1. Поддержка JSON, CSV, XML, YAML
    2. Автоматическое определение формата
    3. Валидация данных при конвертации
    4. Обработка больших файлов по частям
    5. Настройка параметров конвертации
    """
    print("=== Упражнение 2: Универсальный конвертер данных ===")
    
    # ЗАДАЧА: Создайте универсальный конвертер форматов данных
    
    # РЕШЕНИЕ:
    
    import xml.etree.ElementTree as ET
    from abc import ABC, abstractmethod
    
    class DataFormat(ABC):
        """Базовый класс для форматов данных"""
        
        @abstractmethod
        def can_read(self, filename):
            """Может ли формат прочитать файл"""
            pass
        
        @abstractmethod
        def read(self, filename):
            """Чтение данных из файла"""
            pass
        
        @abstractmethod
        def write(self, data, filename):
            """Запись данных в файл"""
            pass
        
        @property
        @abstractmethod
        def extension(self):
            """Расширение файла"""
            pass
    
    class JSONFormat(DataFormat):
        """Формат JSON"""
        
        def can_read(self, filename):
            return filename.lower().endswith('.json')
        
        def read(self, filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        def write(self, data, filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        @property
        def extension(self):
            return '.json'
    
    class CSVFormat(DataFormat):
        """Формат CSV"""
        
        def can_read(self, filename):
            return filename.lower().endswith('.csv')
        
        def read(self, filename):
            data = []
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(dict(row))
            return data
        
        def write(self, data, filename):
            if not data:
                return
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if isinstance(data[0], dict):
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    writer = csv.writer(f)
                    writer.writerows(data)
        
        @property
        def extension(self):
            return '.csv'
    
    class XMLFormat(DataFormat):
        """Формат XML"""
        
        def can_read(self, filename):
            return filename.lower().endswith('.xml')
        
        def read(self, filename):
            tree = ET.parse(filename)
            root = tree.getroot()
            return self._xml_to_dict(root)
        
        def write(self, data, filename):
            root = self._dict_to_xml(data, 'root')
            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
        
        def _xml_to_dict(self, element):
            """Преобразование XML элемента в словарь"""
            result = {}
            
            # Атрибуты элемента
            if element.attrib:
                result['@attributes'] = element.attrib
            
            # Текст элемента
            if element.text and element.text.strip():
                if len(element) == 0:
                    return element.text.strip()
                result['#text'] = element.text.strip()
            
            # Дочерние элементы
            children = {}
            for child in element:
                child_data = self._xml_to_dict(child)
                
                if child.tag in children:
                    if not isinstance(children[child.tag], list):
                        children[child.tag] = [children[child.tag]]
                    children[child.tag].append(child_data)
                else:
                    children[child.tag] = child_data
            
            result.update(children)
            
            # Если только текст, возвращаем его
            if len(result) == 1 and '#text' in result:
                return result['#text']
            
            return result if result else None
        
        def _dict_to_xml(self, data, root_tag):
            """Преобразование словаря в XML элемент"""
            element = ET.Element(root_tag)
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if key == '@attributes':
                        element.attrib.update(value)
                    elif key == '#text':
                        element.text = str(value)
                    else:
                        if isinstance(value, list):
                            for item in value:
                                sub_elem = self._dict_to_xml(item, key)
                                element.append(sub_elem)
                        else:
                            sub_elem = self._dict_to_xml(value, key)
                            element.append(sub_elem)
            else:
                element.text = str(data)
            
            return element
        
        @property
        def extension(self):
            return '.xml'
    
    class DataConverter:
        """Универсальный конвертер данных"""
        
        def __init__(self):
            self.formats = {
                'json': JSONFormat(),
                'csv': CSVFormat(),
                'xml': XMLFormat()
            }
        
        def detect_format(self, filename):
            """Автоматическое определение формата"""
            for name, format_handler in self.formats.items():
                if format_handler.can_read(filename):
                    return name, format_handler
            
            raise ValueError(f"Неподдерживаемый формат файла: {filename}")
        
        def convert(self, input_file, output_format, output_file=None):
            """Конвертация файла в другой формат"""
            
            # Определяем входной формат
            input_format_name, input_format = self.detect_format(input_file)
            print(f"Входной формат: {input_format_name}")
            
            # Проверяем выходной формат
            if output_format not in self.formats:
                raise ValueError(f"Неподдерживаемый выходной формат: {output_format}")
            
            output_format_handler = self.formats[output_format]
            
            # Генерируем имя выходного файла
            if output_file is None:
                base_name = os.path.splitext(input_file)[0]
                output_file = base_name + output_format_handler.extension
            
            print(f"Выходной формат: {output_format}")
            print(f"Выходной файл: {output_file}")
            
            # Конвертация
            print("Чтение данных...")
            start_time = time.time()
            
            try:
                data = input_format.read(input_file)
                read_time = time.time() - start_time
                
                print(f"Данные прочитаны за {read_time:.3f}с")
                
                if isinstance(data, list):
                    print(f"Записей в данных: {len(data)}")
                elif isinstance(data, dict):
                    print(f"Ключей в данных: {len(data)}")
                
                print("Запись данных...")
                write_start = time.time()
                
                output_format_handler.write(data, output_file)
                write_time = time.time() - write_start
                
                print(f"Данные записаны за {write_time:.3f}с")
                
                # Сравниваем размеры файлов
                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                
                print(f"Размер входного файла: {input_size:,} байт")
                print(f"Размер выходного файла: {output_size:,} байт")
                print(f"Изменение размера: {(output_size/input_size-1)*100:+.1f}%")
                
                return output_file
                
            except Exception as e:
                print(f"Ошибка конвертации: {e}")
                raise
        
        def batch_convert(self, input_dir, output_format, output_dir=None):
            """Пакетная конвертация файлов в директории"""
            
            if output_dir is None:
                output_dir = input_dir + f"_converted_to_{output_format}"
            
            os.makedirs(output_dir, exist_ok=True)
            
            converted_files = []
            
            for filename in os.listdir(input_dir):
                input_file = os.path.join(input_dir, filename)
                
                if os.path.isfile(input_file):
                    try:
                        # Пытаемся определить формат
                        self.detect_format(input_file)
                        
                        # Конвертируем
                        base_name = os.path.splitext(filename)[0]
                        output_ext = self.formats[output_format].extension
                        output_file = os.path.join(output_dir, base_name + output_ext)
                        
                        print(f"\nКонвертация: {filename}")
                        self.convert(input_file, output_format, output_file)
                        converted_files.append(output_file)
                        
                    except ValueError:
                        print(f"Пропускаем файл неподдерживаемого формата: {filename}")
                    except Exception as e:
                        print(f"Ошибка конвертации {filename}: {e}")
            
            print(f"\nПакетная конвертация завершена: {len(converted_files)} файлов")
            return converted_files
    
    print("1. Создание тестовых данных:")
    
    def create_test_data():
        """Создание тестовых данных в разных форматах"""
        
        # Образец данных
        test_data = [
            {
                "id": 1,
                "name": "Иван Петров",
                "email": "ivan@example.com",
                "age": 28,
                "city": "Москва",
                "skills": ["Python", "JavaScript", "SQL"],
                "active": True,
                "salary": 95000
            },
            {
                "id": 2,
                "name": "Мария Сидорова",
                "email": "maria@example.com",
                "age": 25,
                "city": "Санкт-Петербург",
                "skills": ["Java", "Spring", "Docker"],
                "active": True,
                "salary": 85000
            },
            {
                "id": 3,
                "name": "Александр Козлов",
                "email": "alex@example.com",
                "age": 32,
                "city": "Новосибирск",
                "skills": ["C++", "Python", "Machine Learning"],
                "active": False,
                "salary": 105000
            }
        ]
        
        # Создаем JSON файл
        json_file = "test_data.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        # Создаем CSV файл
        csv_file = "test_data.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            # Упрощаем данные для CSV (без списков)
            csv_data = []
            for item in test_data:
                csv_item = item.copy()
                csv_item['skills'] = '|'.join(item['skills'])
                csv_data.append(csv_item)
            
            fieldnames = csv_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        
        print(f"Созданы тестовые файлы: {json_file}, {csv_file}")
        return json_file, csv_file, test_data
    
    json_file, csv_file, original_data = create_test_data()
    
    print("\n2. Тестирование конвертера:")
    
    converter = DataConverter()
    
    # JSON → XML
    print("\nКонвертация JSON → XML:")
    xml_file = converter.convert(json_file, 'xml')
    
    # CSV → JSON
    print("\nКонвертация CSV → JSON:")
    json_from_csv = converter.convert(csv_file, 'json', 'converted_from_csv.json')
    
    # XML → CSV
    print("\nКонвертация XML → CSV:")
    csv_from_xml = converter.convert(xml_file, 'csv', 'converted_from_xml.csv')
    
    print("\n3. Проверка целостности данных:")
    
    def verify_conversion(original_file, converted_file):
        """Проверка целостности после конвертации"""
        
        try:
            orig_format_name, orig_format = converter.detect_format(original_file)
            conv_format_name, conv_format = converter.detect_format(converted_file)
            
            orig_data = orig_format.read(original_file)
            conv_data = conv_format.read(converted_file)
            
            print(f"Проверка: {orig_format_name} → {conv_format_name}")
            
            if isinstance(orig_data, list) and isinstance(conv_data, list):
                print(f"  Записей в оригинале: {len(orig_data)}")
                print(f"  Записей в конвертированном: {len(conv_data)}")
                
                if len(orig_data) == len(conv_data):
                    print("  ✅ Количество записей совпадает")
                else:
                    print("  ❌ Количество записей не совпадает")
            
            # Проверяем наличие ключевых полей
            if (isinstance(orig_data, list) and orig_data and 
                isinstance(conv_data, list) and conv_data):
                
                orig_keys = set(orig_data[0].keys()) if isinstance(orig_data[0], dict) else set()
                conv_keys = set(conv_data[0].keys()) if isinstance(conv_data[0], dict) else set()
                
                if orig_keys and conv_keys:
                    common_keys = orig_keys.intersection(conv_keys)
                    print(f"  Общих полей: {len(common_keys)} из {len(orig_keys)}")
                    
                    if len(common_keys) >= len(orig_keys) * 0.8:  # 80% полей сохранено
                        print("  ✅ Структура данных сохранена")
                    else:
                        print("  ⚠️ Некоторые поля потеряны при конвертации")
        
        except Exception as e:
            print(f"  ❌ Ошибка проверки: {e}")
    
    # Проверяем все конвертации
    verify_conversion(json_file, xml_file)
    verify_conversion(csv_file, json_from_csv)
    verify_conversion(xml_file, csv_from_xml)
    
    print("\n4. Пакетная конвертация:")
    
    # Создаем директорию с несколькими файлами
    test_dir = "batch_test_data"
    os.makedirs(test_dir, exist_ok=True)
    
    # Копируем тестовые файлы
    shutil.copy(json_file, os.path.join(test_dir, "users.json"))
    shutil.copy(csv_file, os.path.join(test_dir, "employees.csv"))
    shutil.copy(xml_file, os.path.join(test_dir, "data.xml"))
    
    # Пакетная конвертация в JSON
    converted_files = converter.batch_convert(test_dir, 'json')
    
    print("\n5. Статистика конвертации:")
    
    all_files = [json_file, csv_file, xml_file, json_from_csv, csv_from_xml] + converted_files
    
    formats_count = {}
    total_size = 0
    
    for filename in all_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            total_size += size
            
            ext = os.path.splitext(filename)[1].lower()
            formats_count[ext] = formats_count.get(ext, 0) + 1
            
            print(f"📄 {filename}: {size:,} байт")
    
    print(f"\n📊 Статистика файлов:")
    for ext, count in formats_count.items():
        print(f"  {ext}: {count} файлов")
    print(f"📦 Общий размер: {total_size:,} байт")
    
    print("\n6. Очистка:")
    
    # Удаляем все созданные файлы
    cleanup_files = all_files + [test_dir]
    
    for item in cleanup_files:
        try:
            if os.path.isfile(item):
                os.remove(item)
            elif os.path.isdir(item):
                shutil.rmtree(item)
        except:
            pass
    
    print("✅ Все тестовые файлы и директории удалены")


def exercise_03_backup_system():
    """
    Упражнение 3: Система резервного копирования
    
    Задача:
    Создайте систему резервного копирования файлов с функциями:
    1. Полное и инкрементальное копирование
    2. Сжатие архивов
    3. Проверка целостности данных (хеши)
    4. Планирование копирования
    5. Восстановление из резервных копий
    """
    print("=== Упражнение 3: Система резервного копирования ===")
    
    # ЗАДАЧА: Создайте полнофункциональную систему резервного копирования
    
    # РЕШЕНИЕ:
    
    import zipfile
    import tarfile
    from datetime import datetime, timedelta
    
    class BackupSystem:
        """Система резервного копирования"""
        
        def __init__(self, backup_dir="backups"):
            self.backup_dir = Path(backup_dir)
            self.backup_dir.mkdir(exist_ok=True)
            self.metadata_file = self.backup_dir / "backup_metadata.json"
            self.metadata = self._load_metadata()
        
        def _load_metadata(self):
            """Загрузка метаданных о резервных копиях"""
            if self.metadata_file.exists():
                try:
                    with open(self.metadata_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    pass
            
            return {
                'backups': [],
                'last_full_backup': None,
                'total_backups': 0
            }
        
        def _save_metadata(self):
            """Сохранение метаданных"""
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        
        def _calculate_file_hash(self, filepath):
            """Вычисление хеша файла"""
            hash_md5 = hashlib.md5()
            
            try:
                with open(filepath, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                return hash_md5.hexdigest()
            except:
                return None
        
        def _scan_directory(self, source_dir):
            """Сканирование директории и создание индекса файлов"""
            file_index = {}
            
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    relative_path = os.path.relpath(filepath, source_dir)
                    
                    try:
                        stat = os.stat(filepath)
                        file_hash = self._calculate_file_hash(filepath)
                        
                        file_index[relative_path] = {
                            'size': stat.st_size,
                            'mtime': stat.st_mtime,
                            'hash': file_hash,
                            'full_path': filepath
                        }
                    except OSError:
                        continue
            
            return file_index
        
        def create_full_backup(self, source_dir, backup_name=None):
            """Создание полной резервной копии"""
            
            if backup_name is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f"full_backup_{timestamp}"
            
            print(f"Создание полной резервной копии: {backup_name}")
            
            # Сканируем исходную директорию
            print("Сканирование файлов...")
            file_index = self._scan_directory(source_dir)
            
            total_files = len(file_index)
            total_size = sum(info['size'] for info in file_index.values())
            
            print(f"Найдено файлов: {total_files:,}")
            print(f"Общий размер: {total_size:,} байт")
            
            # Создаем архив
            backup_file = self.backup_dir / f"{backup_name}.tar.gz"
            
            with tarfile.open(backup_file, 'w:gz') as tar:
                for relative_path, info in file_index.items():
                    try:
                        tar.add(info['full_path'], arcname=relative_path)
                    except OSError as e:
                        print(f"Ошибка добавления файла {relative_path}: {e}")
            
            # Сохраняем метаданные
            backup_info = {
                'name': backup_name,
                'type': 'full',
                'timestamp': datetime.now().isoformat(),
                'source_dir': str(source_dir),
                'backup_file': str(backup_file),
                'files_count': total_files,
                'total_size': total_size,
                'file_index': file_index
            }
            
            self.metadata['backups'].append(backup_info)
            self.metadata['last_full_backup'] = backup_name
            self.metadata['total_backups'] += 1
            self._save_metadata()
            
            backup_size = backup_file.stat().st_size
            compression_ratio = (1 - backup_size / total_size) * 100
            
            print(f"Резервная копия создана: {backup_file}")
            print(f"Размер архива: {backup_size:,} байт")
            print(f"Степень сжатия: {compression_ratio:.1f}%")
            
            return backup_name
        
        def create_incremental_backup(self, source_dir, backup_name=None):
            """Создание инкрементальной резервной копии"""
            
            if not self.metadata['last_full_backup']:
                print("Нет полной резервной копии. Создаем полную копию...")
                return self.create_full_backup(source_dir, backup_name)
            
            if backup_name is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f"incremental_backup_{timestamp}"
            
            print(f"Создание инкрементальной резервной копии: {backup_name}")
            
            # Находим последнюю резервную копию
            last_backup = None
            for backup in reversed(self.metadata['backups']):
                if backup['source_dir'] == str(source_dir):
                    last_backup = backup
                    break
            
            if not last_backup:
                print("Не найдена предыдущая резервная копия. Создаем полную...")
                return self.create_full_backup(source_dir, backup_name)
            
            # Сканируем текущее состояние
            print("Сканирование файлов...")
            current_index = self._scan_directory(source_dir)
            last_index = last_backup['file_index']
            
            # Находим изменения
            new_files = []
            modified_files = []
            deleted_files = []
            
            # Новые и измененные файлы
            for path, info in current_index.items():
                if path not in last_index:
                    new_files.append(path)
                elif (info['hash'] != last_index[path]['hash'] or 
                      info['mtime'] != last_index[path]['mtime']):
                    modified_files.append(path)
            
            # Удаленные файлы
            for path in last_index:
                if path not in current_index:
                    deleted_files.append(path)
            
            changed_files = new_files + modified_files
            
            print(f"Новых файлов: {len(new_files)}")
            print(f"Измененных файлов: {len(modified_files)}")
            print(f"Удаленных файлов: {len(deleted_files)}")
            
            if not changed_files and not deleted_files:
                print("Изменений не обнаружено. Резервная копия не создана.")
                return None
            
            # Создаем архив только с измененными файлами
            backup_file = self.backup_dir / f"{backup_name}.tar.gz"
            
            with tarfile.open(backup_file, 'w:gz') as tar:
                for relative_path in changed_files:
                    info = current_index[relative_path]
                    try:
                        tar.add(info['full_path'], arcname=relative_path)
                    except OSError as e:
                        print(f"Ошибка добавления файла {relative_path}: {e}")
            
            # Сохраняем метаданные
            backup_info = {
                'name': backup_name,
                'type': 'incremental',
                'timestamp': datetime.now().isoformat(),
                'source_dir': str(source_dir),
                'backup_file': str(backup_file),
                'base_backup': last_backup['name'],
                'new_files': new_files,
                'modified_files': modified_files,
                'deleted_files': deleted_files,
                'files_count': len(changed_files),
                'total_size': sum(current_index[f]['size'] for f in changed_files),
                'file_index': {f: current_index[f] for f in changed_files}
            }
            
            self.metadata['backups'].append(backup_info)
            self.metadata['total_backups'] += 1
            self._save_metadata()
            
            backup_size = backup_file.stat().st_size
            
            print(f"Инкрементальная копия создана: {backup_file}")
            print(f"Размер архива: {backup_size:,} байт")
            
            return backup_name
        
        def list_backups(self):
            """Список всех резервных копий"""
            
            print(f"Всего резервных копий: {len(self.metadata['backups'])}")
            print("-" * 80)
            
            for backup in self.metadata['backups']:
                timestamp = datetime.fromisoformat(backup['timestamp'])
                
                print(f"Имя: {backup['name']}")
                print(f"Тип: {backup['type']}")
                print(f"Дата: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Исходная папка: {backup['source_dir']}")
                print(f"Файлов: {backup['files_count']:,}")
                print(f"Размер: {backup['total_size']:,} байт")
                
                if backup['type'] == 'incremental':
                    print(f"Базовая копия: {backup['base_backup']}")
                
                print("-" * 80)
        
        def restore_backup(self, backup_name, restore_dir):
            """Восстановление из резервной копии"""
            
            print(f"Восстановление резервной копии: {backup_name}")
            
            # Находим резервную копию
            backup_info = None
            for backup in self.metadata['backups']:
                if backup['name'] == backup_name:
                    backup_info = backup
                    break
            
            if not backup_info:
                print(f"Резервная копия {backup_name} не найдена")
                return False
            
            restore_path = Path(restore_dir)
            restore_path.mkdir(parents=True, exist_ok=True)
            
            if backup_info['type'] == 'full':
                # Восстановление полной копии
                backup_file = Path(backup_info['backup_file'])
                
                if not backup_file.exists():
                    print(f"Файл резервной копии не найден: {backup_file}")
                    return False
                
                print("Восстановление полной резервной копии...")
                
                with tarfile.open(backup_file, 'r:gz') as tar:
                    tar.extractall(restore_path)
                
                print(f"Восстановлено {backup_info['files_count']} файлов")
            
            else:
                # Восстановление инкрементальной копии
                print("Восстановление инкрементальной копии требует базовую копию...")
                
                # Находим цепочку резервных копий
                backup_chain = self._build_backup_chain(backup_name)
                
                if not backup_chain:
                    print("Не удалось построить цепочку резервных копий")
                    return False
                
                print(f"Цепочка восстановления: {' → '.join(backup_chain)}")
                
                # Восстанавливаем в порядке от полной копии к инкрементальной
                for chain_backup_name in backup_chain:
                    chain_backup = next(b for b in self.metadata['backups'] 
                                      if b['name'] == chain_backup_name)
                    
                    backup_file = Path(chain_backup['backup_file'])
                    
                    if not backup_file.exists():
                        print(f"Файл резервной копии не найден: {backup_file}")
                        return False
                    
                    print(f"Восстановление: {chain_backup_name}")
                    
                    with tarfile.open(backup_file, 'r:gz') as tar:
                        tar.extractall(restore_path)
            
            print(f"Восстановление завершено в: {restore_path}")
            return True
        
        def _build_backup_chain(self, backup_name):
            """Построение цепочки резервных копий"""
            
            chain = []
            current_backup_name = backup_name
            
            while current_backup_name:
                backup = next((b for b in self.metadata['backups'] 
                             if b['name'] == current_backup_name), None)
                
                if not backup:
                    break
                
                chain.insert(0, current_backup_name)
                
                if backup['type'] == 'full':
                    break
                
                current_backup_name = backup.get('base_backup')
            
            return chain
        
        def verify_backup(self, backup_name):
            """Проверка целостности резервной копии"""
            
            print(f"Проверка целостности: {backup_name}")
            
            backup_info = next((b for b in self.metadata['backups'] 
                              if b['name'] == backup_name), None)
            
            if not backup_info:
                print(f"Резервная копия {backup_name} не найдена")
                return False
            
            backup_file = Path(backup_info['backup_file'])
            
            if not backup_file.exists():
                print(f"Файл резервной копии не найден: {backup_file}")
                return False
            
            # Проверяем архив
            try:
                with tarfile.open(backup_file, 'r:gz') as tar:
                    members = tar.getmembers()
                
                print(f"Архив содержит {len(members)} файлов")
                
                # Проверяем соответствие метаданным
                expected_count = backup_info['files_count']
                
                if len(members) == expected_count:
                    print("✅ Количество файлов соответствует метаданным")
                else:
                    print(f"❌ Ожидалось {expected_count} файлов, найдено {len(members)}")
                    return False
                
                print("✅ Резервная копия прошла проверку целостности")
                return True
                
            except Exception as e:
                print(f"❌ Ошибка проверки архива: {e}")
                return False
        
        def cleanup_old_backups(self, keep_days=30):
            """Очистка старых резервных копий"""
            
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            
            removed_backups = []
            
            for backup in self.metadata['backups'][:]:  # Копия списка для безопасного удаления
                backup_date = datetime.fromisoformat(backup['timestamp'])
                
                if backup_date < cutoff_date:
                    # Удаляем файл резервной копии
                    backup_file = Path(backup['backup_file'])
                    
                    if backup_file.exists():
                        backup_file.unlink()
                    
                    # Удаляем из метаданных
                    self.metadata['backups'].remove(backup)
                    removed_backups.append(backup['name'])
            
            if removed_backups:
                self._save_metadata()
                print(f"Удалено старых резервных копий: {len(removed_backups)}")
                for name in removed_backups:
                    print(f"  - {name}")
            else:
                print("Старых резервных копий для удаления не найдено")
    
    print("1. Создание тестовой структуры файлов:")
    
    def create_test_structure():
        """Создание тестовой структуры для резервного копирования"""
        
        test_dir = Path("test_source")
        test_dir.mkdir(exist_ok=True)
        
        # Создаем файлы и поддиректории
        (test_dir / "documents").mkdir(exist_ok=True)
        (test_dir / "images").mkdir(exist_ok=True)
        (test_dir / "projects").mkdir(exist_ok=True)
        
        # Создаем файлы с различным содержимым
        files_to_create = [
            ("readme.txt", "Это главный файл проекта\n" * 100),
            ("config.json", json.dumps({"setting1": "value1", "setting2": 42}, indent=2)),
            ("documents/letter.txt", "Важное письмо\n" * 50),
            ("documents/report.csv", "name,value\nItem1,100\nItem2,200\n"),
            ("images/placeholder.txt", "Файл-заглушка для изображения"),
            ("projects/main.py", "#!/usr/bin/env python3\nprint('Hello, World!')\n" * 20),
        ]
        
        total_size = 0
        for filepath, content in files_to_create:
            full_path = test_dir / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            total_size += len(content.encode('utf-8'))
        
        print(f"Создана тестовая структура в {test_dir}")
        print(f"Файлов: {len(files_to_create)}")
        print(f"Общий размер: {total_size:,} байт")
        
        return test_dir
    
    test_source = create_test_structure()
    
    print("\n2. Инициализация системы резервного копирования:")
    
    backup_system = BackupSystem("test_backups")
    
    print("\n3. Создание полной резервной копии:")
    
    full_backup_name = backup_system.create_full_backup(test_source)
    
    print("\n4. Модификация файлов:")
    
    # Изменяем некоторые файлы
    time.sleep(1)  # Чтобы время изменения отличалось
    
    # Изменяем существующий файл
    with open(test_source / "readme.txt", 'a', encoding='utf-8') as f:
        f.write("\nДобавлена новая строка для тестирования инкрементального копирования")
    
    # Создаем новый файл
    with open(test_source / "new_file.txt", 'w', encoding='utf-8') as f:
        f.write("Это новый файл, созданный после полной резервной копии")
    
    # Удаляем файл
    (test_source / "images" / "placeholder.txt").unlink()
    
    print("Файлы модифицированы для тестирования инкрементального копирования")
    
    print("\n5. Создание инкрементальной резервной копии:")
    
    incremental_backup_name = backup_system.create_incremental_backup(test_source)
    
    print("\n6. Список резервных копий:")
    
    backup_system.list_backups()
    
    print("\n7. Проверка целостности:")
    
    backup_system.verify_backup(full_backup_name)
    if incremental_backup_name:
        backup_system.verify_backup(incremental_backup_name)
    
    print("\n8. Восстановление из резервной копии:")
    
    # Восстанавливаем полную копию
    restore_dir_full = "restored_full"
    backup_system.restore_backup(full_backup_name, restore_dir_full)
    
    # Восстанавливаем инкрементальную копию
    if incremental_backup_name:
        restore_dir_incremental = "restored_incremental"
        backup_system.restore_backup(incremental_backup_name, restore_dir_incremental)
    
    print("\n9. Статистика системы:")
    
    backup_dir_size = sum(f.stat().st_size for f in Path("test_backups").rglob("*") if f.is_file())
    
    print(f"📊 Статистика резервного копирования:")
    print(f"  Всего резервных копий: {len(backup_system.metadata['backups'])}")
    print(f"  Размер директории резервных копий: {backup_dir_size:,} байт")
    print(f"  Последняя полная копия: {backup_system.metadata['last_full_backup']}")
    
    print("\n10. Очистка:")
    
    # Удаляем созданные директории и файлы
    cleanup_dirs = [test_source, "test_backups", restore_dir_full]
    if incremental_backup_name:
        cleanup_dirs.append("restored_incremental")
    
    for directory in cleanup_dirs:
        if Path(directory).exists():
            shutil.rmtree(directory)
            print(f"🗑️ Удалена директория: {directory}")
    
    print("✅ Очистка завершена")


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Анализатор лог-файлов", exercise_01_log_analyzer),
        ("Универсальный конвертер данных", exercise_02_data_converter),
        ("Система резервного копирования", exercise_03_backup_system),
    ]
    
    print("📁 Упражнения: Работа с файлами в Python")
    print("=" * 70)
    print("Эти упражнения помогут освоить:")
    print("- Обработку больших файлов")
    print("- Анализ и парсинг данных")
    print("- Конвертацию между форматами")
    print("- Системы резервного копирования")
    print("- Работу с архивами и сжатием")
    print("- Проверку целостности данных")
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