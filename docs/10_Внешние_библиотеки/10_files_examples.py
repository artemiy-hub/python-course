#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Работа с файлами в Python

Этот файл содержит подробные примеры для изучения:
- Основных операций с файлами
- Различных режимов открытия
- Работы с кодировками
- Обработки больших файлов
- Файловых форматов
- Безопасности файловых операций
"""

import os
import sys
import json
import csv
import tempfile
import shutil
import time
from pathlib import Path
from contextlib import contextmanager
from typing import List, Dict, Any, Generator, Optional


def example_01_basic_file_operations():
    """
    Пример 1: Основные операции с файлами
    
    Демонстрирует базовые операции чтения, записи,
    различные режимы открытия файлов и их особенности.
    """
    print("=== Пример 1: Основные операции с файлами ===")
    
    # Создаем тестовые данные
    sample_data = """Первая строка файла
Вторая строка с числами: 42, 3.14, 100
Третья строка содержит специальные символы: @#$%^&*()
Четвертая строка на русском языке: Привет, мир!
Пятая и последняя строка"""
    
    test_file = "basic_operations_test.txt"
    
    try:
        print("1. Запись в файл (режим 'w'):")
        
        # Запись с перезаписью
        with open(test_file, 'w', encoding='utf-8') as file:
            file.write(sample_data)
        
        print(f"   Записано {len(sample_data)} символов в файл {test_file}")
        
        print("\n2. Чтение всего файла:")
        
        # Чтение всего содержимого
        with open(test_file, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"   Прочитано {len(content)} символов")
            print(f"   Количество строк: {content.count(chr(10)) + 1}")
        
        print("\n3. Построчное чтение:")
        
        # Чтение по строкам
        with open(test_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                print(f"   Строка {line_num}: {line.strip()}")
        
        print("\n4. Чтение в список:")
        
        # Чтение всех строк в список
        with open(test_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"   Получен список из {len(lines)} строк")
            print(f"   Первая строка: {repr(lines[0])}")
            print(f"   Последняя строка: {repr(lines[-1])}")
        
        print("\n5. Добавление в файл (режим 'a'):")
        
        # Добавление новых строк
        additional_data = "\nШестая строка (добавлена)\nСедьмая строка (добавлена)"
        
        with open(test_file, 'a', encoding='utf-8') as file:
            file.write(additional_data)
        
        print(f"   Добавлено {len(additional_data)} символов")
        
        # Проверяем результат
        with open(test_file, 'r', encoding='utf-8') as file:
            updated_content = file.read()
            line_count = updated_content.count('\n') + 1
            print(f"   Теперь в файле {line_count} строк")
        
        print("\n6. Чтение и запись одновременно (режим 'r+'):")
        
        with open(test_file, 'r+', encoding='utf-8') as file:
            # Читаем содержимое
            original = file.read()
            print(f"   Прочитано: {len(original)} символов")
            
            # Возвращаемся в начало
            file.seek(0)
            
            # Перезаписываем первые несколько символов
            file.write("ИЗМЕНЕНО: ")
            
            # Переходим в конец
            file.seek(0, 2)  # 2 = SEEK_END
            file.write("\nВосьмая строка (добавлена через r+)")
        
        print("   Файл изменен в режиме 'r+'")
        
        print("\n7. Позиционирование в файле:")
        
        with open(test_file, 'r', encoding='utf-8') as file:
            print(f"   Начальная позиция: {file.tell()}")
            
            # Читаем первые 10 символов
            chunk = file.read(10)
            print(f"   Прочитано: {repr(chunk)}")
            print(f"   Текущая позиция: {file.tell()}")
            
            # Переходим к позиции 50
            file.seek(50)
            print(f"   После seek(50): {file.tell()}")
            
            # Читаем следующие 20 символов
            chunk = file.read(20)
            print(f"   Прочитано с позиции 50: {repr(chunk)}")
        
        print("\n8. Информация о файле:")
        
        file_path = Path(test_file)
        if file_path.exists():
            stat = file_path.stat()
            print(f"   Размер файла: {stat.st_size} байт")
            print(f"   Время создания: {time.ctime(stat.st_ctime)}")
            print(f"   Время изменения: {time.ctime(stat.st_mtime)}")
        
        # Показываем итоговое содержимое
        print("\n9. Итоговое содержимое файла:")
        with open(test_file, 'r', encoding='utf-8') as file:
            final_content = file.read()
            print("   ---")
            print(final_content)
            print("   ---")
        
    finally:
        # Очистка
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\nФайл {test_file} удален")


def example_02_encoding_handling():
    """
    Пример 2: Работа с кодировками
    
    Демонстрирует работу с различными кодировками,
    обработку ошибок декодирования и автоматическое
    определение кодировки.
    """
    print("=== Пример 2: Работа с кодировками ===")
    
    # Тестовый текст с различными символами
    test_texts = {
        'ascii_text': "Hello, World!",
        'latin_text': "Café, naïve, résumé",
        'cyrillic_text': "Привет, мир! Как дела?",
        'mixed_text': "Mixed: Hello, Привет, Café 🌍",
        'emoji_text': "Python 🐍 is awesome! ❤️✨"
    }
    
    print("1. Создание файлов с разными кодировками:")
    
    # Создаем файлы с различными кодировками
    encodings = ['utf-8', 'cp1251', 'iso-8859-1']
    created_files = []
    
    for text_name, text in test_texts.items():
        for encoding in encodings:
            filename = f"{text_name}_{encoding.replace('-', '_')}.txt"
            
            try:
                with open(filename, 'w', encoding=encoding) as file:
                    file.write(text)
                
                created_files.append((filename, encoding, text))
                print(f"   ✅ {filename} создан с кодировкой {encoding}")
                
            except UnicodeEncodeError as e:
                print(f"   ❌ {filename}: Ошибка кодирования {encoding} - {e}")
    
    print(f"\n2. Анализ созданных файлов ({len(created_files)} файлов):")
    
    def analyze_file_encoding(filename):
        """Анализ кодировки файла"""
        print(f"\n   Анализ файла: {filename}")
        
        # Читаем в бинарном режиме
        with open(filename, 'rb') as file:
            raw_bytes = file.read()
        
        print(f"     Размер: {len(raw_bytes)} байт")
        print(f"     Первые байты: {raw_bytes[:20]}")
        
        # Пробуем различные кодировки
        test_encodings = ['utf-8', 'cp1251', 'iso-8859-1', 'ascii']
        
        for encoding in test_encodings:
            try:
                decoded = raw_bytes.decode(encoding)
                print(f"     {encoding:>12}: ✅ {decoded}")
            except UnicodeDecodeError as e:
                print(f"     {encoding:>12}: ❌ {str(e)[:50]}...")
    
    # Анализируем несколько файлов
    for filename, original_encoding, original_text in created_files[:3]:
        analyze_file_encoding(filename)
    
    print("\n3. Безопасное чтение с обработкой ошибок:")
    
    def safe_read_file(filename, target_encoding='utf-8'):
        """Безопасное чтение файла с обработкой ошибок декодирования"""
        
        error_strategies = ['strict', 'ignore', 'replace', 'xmlcharrefreplace']
        
        print(f"\n   Чтение файла: {filename}")
        
        for strategy in error_strategies:
            try:
                with open(filename, 'r', encoding=target_encoding, errors=strategy) as file:
                    content = file.read()
                
                print(f"     {strategy:>18}: {repr(content[:50])}...")
                
            except UnicodeDecodeError as e:
                print(f"     {strategy:>18}: ❌ {e}")
    
    # Тестируем на файле с потенциальными проблемами
    problematic_files = [f for f, e, t in created_files if 'cyrillic' in f and 'iso' in f]
    
    if problematic_files:
        safe_read_file(problematic_files[0])
    
    print("\n4. Автоматическое определение кодировки:")
    
    def detect_encoding_simple(filename):
        """Простое определение кодировки методом попыток"""
        
        common_encodings = ['utf-8', 'cp1251', 'iso-8859-1', 'ascii']
        
        with open(filename, 'rb') as file:
            sample = file.read(1024)  # Читаем образец
        
        print(f"\n   Определение кодировки для: {filename}")
        
        for encoding in common_encodings:
            try:
                decoded = sample.decode(encoding)
                
                # Простая эвристика: проверяем наличие русских символов
                has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in decoded)
                has_extended = any(ord(char) > 127 for char in decoded)
                
                confidence = "высокая" if not has_extended else "средняя"
                if has_cyrillic and encoding == 'cp1251':
                    confidence = "высокая"
                
                print(f"     {encoding:>12}: ✅ {confidence} - {repr(decoded[:30])}...")
                return encoding
                
            except UnicodeDecodeError:
                print(f"     {encoding:>12}: ❌")
        
        return 'utf-8'  # Fallback
    
    # Определяем кодировку для нескольких файлов
    for filename, original_encoding, _ in created_files[::3]:  # Каждый третий
        detected = detect_encoding_simple(filename)
        match = "✅" if detected == original_encoding else "❌"
        print(f"     Исходная: {original_encoding}, определена: {detected} {match}")
    
    print("\n5. Конвертация между кодировками:")
    
    def convert_file_encoding(source_file, target_file, from_encoding, to_encoding):
        """Конвертация файла из одной кодировки в другую"""
        
        try:
            # Читаем в исходной кодировке
            with open(source_file, 'r', encoding=from_encoding) as src:
                content = src.read()
            
            # Записываем в целевой кодировке
            with open(target_file, 'w', encoding=to_encoding) as dst:
                dst.write(content)
            
            print(f"   ✅ {source_file} → {target_file}: {from_encoding} → {to_encoding}")
            
            # Проверяем размеры
            src_size = os.path.getsize(source_file)
            dst_size = os.path.getsize(target_file)
            print(f"      Размеры: {src_size} → {dst_size} байт")
            
        except (UnicodeDecodeError, UnicodeEncodeError) as e:
            print(f"   ❌ Ошибка конвертации: {e}")
    
    # Конвертируем несколько файлов
    conversions = [
        ('utf_8', 'cp1251'),
        ('cp1251', 'utf_8'),
        ('iso_8859_1', 'utf_8')
    ]
    
    for from_enc, to_enc in conversions:
        source_files = [f for f, e, t in created_files if from_enc in f]
        if source_files:
            source = source_files[0]
            target = source.replace(from_enc, f"{from_enc}_to_{to_enc}")
            
            orig_encoding = from_enc.replace('_', '-')
            target_encoding = to_enc.replace('_', '-')
            
            convert_file_encoding(source, target, orig_encoding, target_encoding)
    
    print("\n6. Работа с BOM (Byte Order Mark):")
    
    def create_file_with_bom():
        """Создание файла с BOM"""
        
        text = "Файл с BOM: Привет, мир!"
        
        # UTF-8 с BOM
        with open('utf8_with_bom.txt', 'wb') as file:
            file.write('\ufeff'.encode('utf-8'))  # BOM
            file.write(text.encode('utf-8'))
        
        # UTF-16 (автоматически добавляет BOM)
        with open('utf16_with_bom.txt', 'w', encoding='utf-16') as file:
            file.write(text)
        
        print("   Файлы с BOM созданы")
        
        # Анализируем BOM
        bom_files = ['utf8_with_bom.txt', 'utf16_with_bom.txt']
        
        for filename in bom_files:
            with open(filename, 'rb') as file:
                first_bytes = file.read(4)
            
            print(f"   {filename}: первые байты {first_bytes}")
            
            # Определяем тип BOM
            if first_bytes.startswith(b'\xef\xbb\xbf'):
                print("     Обнаружен UTF-8 BOM")
            elif first_bytes.startswith(b'\xff\xfe'):
                print("     Обнаружен UTF-16 LE BOM")
            elif first_bytes.startswith(b'\xfe\xff'):
                print("     Обнаружен UTF-16 BE BOM")
    
    create_file_with_bom()
    
    # Очистка
    print("\n7. Очистка созданных файлов:")
    
    all_test_files = [f[0] for f in created_files]
    all_test_files.extend([
        'utf8_with_bom.txt', 'utf16_with_bom.txt'
    ])
    
    # Добавляем конвертированные файлы
    all_test_files.extend([
        f for f in os.listdir('.') 
        if f.endswith('.txt') and '_to_' in f
    ])
    
    removed_count = 0
    for filename in all_test_files:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                removed_count += 1
        except OSError:
            pass
    
    print(f"   Удалено {removed_count} тестовых файлов")


def example_03_large_file_processing():
    """
    Пример 3: Обработка больших файлов
    
    Демонстрирует эффективные техники работы с большими файлами:
    потоковое чтение, генераторы, обработка по частям.
    """
    print("=== Пример 3: Обработка больших файлов ===")
    
    print("1. Создание большого тестового файла:")
    
    large_file = "large_test_file.txt"
    
    # Создаем файл размером около 1MB
    def create_large_file(filename, target_size_mb=1):
        """Создание большого файла для тестирования"""
        
        target_size = target_size_mb * 1024 * 1024  # Размер в байтах
        
        with open(filename, 'w', encoding='utf-8') as file:
            line_template = "Строка номер {num:06d}: Это тестовая строка с данными для демонстрации обработки больших файлов. Timestamp: {timestamp}\n"
            
            current_size = 0
            line_num = 1
            
            while current_size < target_size:
                line = line_template.format(
                    num=line_num, 
                    timestamp=time.time()
                )
                
                file.write(line)
                current_size += len(line.encode('utf-8'))
                line_num += 1
                
                # Показываем прогресс
                if line_num % 1000 == 0:
                    progress = (current_size / target_size) * 100
                    print(f"\r   Создано: {progress:.1f}% ({current_size:,} байт)", end='', flush=True)
        
        print(f"\n   Файл создан: {current_size:,} байт, {line_num-1:,} строк")
        return line_num - 1
    
    total_lines = create_large_file(large_file)
    
    print("\n2. Сравнение методов чтения:")
    
    def measure_time(func):
        """Декоратор для измерения времени выполнения"""
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            print(f"   Время выполнения: {execution_time:.3f} секунд")
            return result
        return wrapper
    
    @measure_time
    def read_entire_file(filename):
        """Чтение всего файла в память"""
        print("\n   Метод 1: read() - весь файл в память")
        
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        lines = content.count('\n')
        size_mb = len(content) / (1024 * 1024)
        
        print(f"   Прочитано: {size_mb:.2f} MB, {lines:,} строк")
        return lines
    
    @measure_time
    def read_by_chunks(filename, chunk_size=8192):
        """Чтение файла по частям"""
        print(f"\n   Метод 2: read({chunk_size}) - по частям")
        
        total_chars = 0
        total_lines = 0
        
        with open(filename, 'r', encoding='utf-8') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                
                total_chars += len(chunk)
                total_lines += chunk.count('\n')
        
        size_mb = total_chars / (1024 * 1024)
        print(f"   Прочитано: {size_mb:.2f} MB, {total_lines:,} строк")
        return total_lines
    
    @measure_time
    def read_line_by_line(filename):
        """Построчное чтение"""
        print("\n   Метод 3: построчное чтение")
        
        line_count = 0
        total_chars = 0
        
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line_count += 1
                total_chars += len(line)
        
        size_mb = total_chars / (1024 * 1024)
        print(f"   Прочитано: {size_mb:.2f} MB, {line_count:,} строк")
        return line_count
    
    # Сравниваем производительность
    methods = [read_entire_file, read_by_chunks, read_line_by_line]
    
    for method in methods:
        method(large_file)
    
    print("\n3. Обработка файла с генераторами:")
    
    def process_file_generator(filename):
        """Генератор для обработки файла построчно"""
        
        def file_processor():
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    # Обработка строки
                    processed_line = {
                        'line_number': line_num,
                        'length': len(line),
                        'words': len(line.split()),
                        'has_numbers': any(char.isdigit() for char in line),
                        'content_preview': line.strip()[:50]
                    }
                    
                    yield processed_line
        
        return file_processor()
    
    # Используем генератор
    print("   Обработка первых 10 строк через генератор:")
    
    processor = process_file_generator(large_file)
    
    for i, processed_line in enumerate(processor):
        if i >= 10:  # Показываем только первые 10
            break
        
        print(f"   Строка {processed_line['line_number']}: "
              f"{processed_line['words']} слов, "
              f"{processed_line['length']} символов")
    
    print("\n4. Фильтрация и поиск в большом файле:")
    
    def search_in_file(filename, search_term, max_results=5):
        """Поиск строк содержащих определенный термин"""
        
        print(f"   Поиск строк содержащих '{search_term}':")
        
        found_count = 0
        total_lines = 0
        
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                total_lines += 1
                
                if search_term.lower() in line.lower():
                    found_count += 1
                    
                    if found_count <= max_results:
                        print(f"     {line_num:6d}: {line.strip()[:80]}...")
                
                # Показываем прогресс каждые 10000 строк
                if line_num % 10000 == 0:
                    print(f"\r   Обработано: {line_num:,} строк", end='', flush=True)
        
        print(f"\n   Найдено {found_count} строк из {total_lines:,} (показано {min(found_count, max_results)})")
    
    # Ищем строки с определенными номерами
    search_in_file(large_file, "001000")  # Строки с номерами вида 001000
    
    print("\n5. Статистика файла:")
    
    def analyze_file_stats(filename):
        """Сбор статистики по файлу"""
        
        stats = {
            'total_lines': 0,
            'total_chars': 0,
            'total_words': 0,
            'min_line_length': float('inf'),
            'max_line_length': 0,
            'empty_lines': 0,
            'lines_with_numbers': 0
        }
        
        print("   Сбор статистики...")
        
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line_length = len(line.strip())
                word_count = len(line.split())
                
                stats['total_lines'] += 1
                stats['total_chars'] += len(line)
                stats['total_words'] += word_count
                
                if line_length == 0:
                    stats['empty_lines'] += 1
                else:
                    stats['min_line_length'] = min(stats['min_line_length'], line_length)
                    stats['max_line_length'] = max(stats['max_line_length'], line_length)
                
                if any(char.isdigit() for char in line):
                    stats['lines_with_numbers'] += 1
                
                # Прогресс
                if line_num % 5000 == 0:
                    print(f"\r   Обработано: {line_num:,} строк", end='', flush=True)
        
        print(f"\n   Статистика файла:")
        print(f"     Всего строк: {stats['total_lines']:,}")
        print(f"     Всего символов: {stats['total_chars']:,}")
        print(f"     Всего слов: {stats['total_words']:,}")
        print(f"     Средняя длина строки: {stats['total_chars']/stats['total_lines']:.1f}")
        print(f"     Мин. длина строки: {stats['min_line_length']}")
        print(f"     Макс. длина строки: {stats['max_line_length']}")
        print(f"     Пустых строк: {stats['empty_lines']}")
        print(f"     Строк с числами: {stats['lines_with_numbers']}")
    
    analyze_file_stats(large_file)
    
    print("\n6. Чтение файла в обратном порядке:")
    
    def read_file_reverse(filename, num_lines=5):
        """Чтение последних N строк файла (аналог tail)"""
        
        print(f"   Последние {num_lines} строк файла:")
        
        with open(filename, 'rb') as file:
            # Переходим в конец файла
            file.seek(0, 2)
            file_size = file.tell()
            
            lines = []
            buffer = b''
            position = file_size
            
            # Читаем файл блоками с конца
            while position > 0 and len(lines) < num_lines:
                # Определяем размер блока для чтения
                read_size = min(4096, position)
                position -= read_size
                
                file.seek(position)
                chunk = file.read(read_size)
                buffer = chunk + buffer
                
                # Извлекаем строки из буфера
                while b'\n' in buffer and len(lines) < num_lines:
                    line, buffer = buffer.rsplit(b'\n', 1)
                    if line:  # Пропускаем пустые строки
                        try:
                            decoded_line = line.decode('utf-8')
                            lines.append(decoded_line)
                        except UnicodeDecodeError:
                            pass
            
            # Показываем строки в правильном порядке
            for i, line in enumerate(reversed(lines), 1):
                line_from_end = i
                print(f"     -{line_from_end:2d}: {line[:80]}...")
    
    read_file_reverse(large_file)
    
    # Очистка
    print("\n7. Очистка:")
    if os.path.exists(large_file):
        file_size = os.path.getsize(large_file)
        os.remove(large_file)
        print(f"   Удален файл {large_file} ({file_size:,} байт)")


def example_04_structured_data_formats():
    """
    Пример 4: Работа со структурированными форматами данных
    
    Демонстрирует работу с JSON, CSV, XML, INI и другими
    популярными форматами файлов.
    """
    print("=== Пример 4: Работа со структурированными форматами данных ===")
    
    # Тестовые данные
    sample_data = {
        'users': [
            {
                'id': 1,
                'name': 'Алиса Иванова',
                'email': 'alice@example.com',
                'age': 28,
                'city': 'Москва',
                'skills': ['Python', 'JavaScript', 'SQL'],
                'active': True,
                'salary': 95000.50
            },
            {
                'id': 2,
                'name': 'Боб Петров',
                'email': 'bob@example.com',
                'age': 32,
                'city': 'Санкт-Петербург',
                'skills': ['Java', 'Spring', 'Docker'],
                'active': True,
                'salary': 105000.00
            },
            {
                'id': 3,
                'name': 'Чарли Сидоров',
                'email': 'charlie@example.com',
                'age': 26,
                'city': 'Новосибирск',
                'skills': ['C++', 'Python', 'Machine Learning'],
                'active': False,
                'salary': 85000.25
            }
        ],
        'metadata': {
            'version': '1.0.0',
            'created': '2024-01-15',
            'source': 'HR Database',
            'total_records': 3
        }
    }
    
    print("1. Работа с JSON:")
    
    def json_operations():
        """Операции с JSON файлами"""
        
        json_file = 'users.json'
        
        # Запись JSON
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(sample_data, file, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Данные сохранены в {json_file}")
        
        # Чтение JSON
        with open(json_file, 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)
        
        print(f"   ✅ Загружено {len(loaded_data['users'])} пользователей")
        
        # Обработка данных
        active_users = [user for user in loaded_data['users'] if user['active']]
        avg_salary = sum(user['salary'] for user in active_users) / len(active_users)
        
        print(f"   📊 Активных пользователей: {len(active_users)}")
        print(f"   💰 Средняя зарплата: {avg_salary:,.2f}")
        
        # Модификация и сохранение
        loaded_data['metadata']['processed'] = time.strftime('%Y-%m-%d %H:%M:%S')
        loaded_data['metadata']['avg_salary'] = avg_salary
        
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(loaded_data, file, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Данные обновлены")
        
        return json_file
    
    json_file = json_operations()
    
    print("\n2. Работа с CSV:")
    
    def csv_operations():
        """Операции с CSV файлами"""
        
        csv_file = 'users.csv'
        
        # Запись CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'id', 'name', 'email', 'age', 'city', 'skills', 'active', 'salary'
            ])
            
            writer.writeheader()
            
            for user in sample_data['users']:
                # Преобразуем список навыков в строку
                user_row = user.copy()
                user_row['skills'] = '; '.join(user['skills'])
                writer.writerow(user_row)
        
        print(f"   ✅ CSV данные сохранены в {csv_file}")
        
        # Чтение CSV
        users_from_csv = []
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Преобразуем типы данных
                user = {
                    'id': int(row['id']),
                    'name': row['name'],
                    'email': row['email'],
                    'age': int(row['age']),
                    'city': row['city'],
                    'skills': row['skills'].split('; '),
                    'active': row['active'].lower() == 'true',
                    'salary': float(row['salary'])
                }
                users_from_csv.append(user)
        
        print(f"   ✅ Загружено {len(users_from_csv)} пользователей из CSV")
        
        # Статистика по городам
        cities = {}
        for user in users_from_csv:
            city = user['city']
            if city not in cities:
                cities[city] = {'count': 0, 'total_salary': 0}
            
            cities[city]['count'] += 1
            cities[city]['total_salary'] += user['salary']
        
        print("   📊 Статистика по городам:")
        for city, stats in cities.items():
            avg_salary = stats['total_salary'] / stats['count']
            print(f"     {city}: {stats['count']} чел., средняя ЗП: {avg_salary:,.0f}")
        
        return csv_file
    
    csv_file = csv_operations()
    
    print("\n3. Работа с XML:")
    
    def xml_operations():
        """Операции с XML файлами"""
        
        import xml.etree.ElementTree as ET
        
        xml_file = 'users.xml'
        
        # Создание XML структуры
        root = ET.Element('database')
        
        # Метаданные
        metadata_elem = ET.SubElement(root, 'metadata')
        for key, value in sample_data['metadata'].items():
            meta_elem = ET.SubElement(metadata_elem, key)
            meta_elem.text = str(value)
        
        # Пользователи
        users_elem = ET.SubElement(root, 'users')
        
        for user in sample_data['users']:
            user_elem = ET.SubElement(users_elem, 'user', {'id': str(user['id'])})
            
            for key, value in user.items():
                if key == 'id':
                    continue
                
                elem = ET.SubElement(user_elem, key)
                
                if key == 'skills':
                    for skill in value:
                        skill_elem = ET.SubElement(elem, 'skill')
                        skill_elem.text = skill
                else:
                    elem.text = str(value)
        
        # Запись XML
        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
        
        print(f"   ✅ XML данные сохранены в {xml_file}")
        
        # Чтение XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Извлечение пользователей
        users_from_xml = []
        
        for user_elem in root.find('users').findall('user'):
            user = {
                'id': int(user_elem.get('id')),
                'name': user_elem.find('name').text,
                'email': user_elem.find('email').text,
                'age': int(user_elem.find('age').text),
                'city': user_elem.find('city').text,
                'active': user_elem.find('active').text.lower() == 'true',
                'salary': float(user_elem.find('salary').text),
                'skills': [skill.text for skill in user_elem.find('skills').findall('skill')]
            }
            users_from_xml.append(user)
        
        print(f"   ✅ Загружено {len(users_from_xml)} пользователей из XML")
        
        # Поиск пользователей с определенными навыками
        python_users = [
            user for user in users_from_xml 
            if 'Python' in user['skills']
        ]
        
        print(f"   🐍 Пользователей со знанием Python: {len(python_users)}")
        for user in python_users:
            print(f"     - {user['name']} ({user['city']})")
        
        return xml_file
    
    xml_file = xml_operations()
    
    print("\n4. Работа с INI конфигурацией:")
    
    def ini_operations():
        """Операции с INI файлами"""
        
        import configparser
        
        ini_file = 'config.ini'
        
        # Создание конфигурации
        config = configparser.ConfigParser()
        
        # Секции конфигурации
        config['DATABASE'] = {
            'host': 'localhost',
            'port': '5432',
            'name': 'users_db',
            'user': 'admin',
            'password': 'secret123',
            'pool_size': '10'
        }
        
        config['SERVER'] = {
            'host': '0.0.0.0',
            'port': '8000',
            'debug': 'true',
            'workers': '4'
        }
        
        config['LOGGING'] = {
            'level': 'INFO',
            'file': 'app.log',
            'max_size': '10MB',
            'backup_count': '5'
        }
        
        # Запись INI
        with open(ini_file, 'w', encoding='utf-8') as file:
            config.write(file)
        
        print(f"   ✅ INI конфигурация сохранена в {ini_file}")
        
        # Чтение INI
        loaded_config = configparser.ConfigParser()
        loaded_config.read(ini_file, encoding='utf-8')
        
        print(f"   ✅ Загружена конфигурация с {len(loaded_config.sections())} секциями")
        
        # Вывод конфигурации
        for section_name in loaded_config.sections():
            print(f"   📂 Секция [{section_name}]:")
            
            for key, value in loaded_config[section_name].items():
                print(f"     {key} = {value}")
        
        # Модификация конфигурации
        loaded_config['SERVER']['port'] = '8080'
        loaded_config['SERVER']['ssl_enabled'] = 'true'
        
        # Новая секция
        loaded_config['CACHE'] = {
            'type': 'redis',
            'host': 'localhost',
            'port': '6379',
            'db': '0'
        }
        
        # Сохранение изменений
        with open(ini_file, 'w', encoding='utf-8') as file:
            loaded_config.write(file)
        
        print(f"   ✅ Конфигурация обновлена")
        
        return ini_file
    
    ini_file = ini_operations()
    
    print("\n5. Работа с текстовыми логами:")
    
    def log_operations():
        """Операции с лог файлами"""
        
        log_file = 'application.log'
        
        # Создание лог записей
        log_entries = [
            "2024-01-15 10:30:15 INFO Application started",
            "2024-01-15 10:30:16 INFO Database connection established",
            "2024-01-15 10:32:22 DEBUG User 'alice@example.com' logged in",
            "2024-01-15 10:35:18 WARNING High memory usage detected: 85%",
            "2024-01-15 10:38:45 ERROR Failed to connect to external API: timeout",
            "2024-01-15 10:40:12 INFO User 'bob@example.com' logged in",
            "2024-01-15 10:45:33 DEBUG Processing batch job #1234",
            "2024-01-15 10:47:28 ERROR Database query failed: connection lost",
            "2024-01-15 10:48:15 INFO Database connection restored",
            "2024-01-15 10:50:42 INFO Batch job #1234 completed successfully"
        ]
        
        # Запись логов
        with open(log_file, 'w', encoding='utf-8') as file:
            for entry in log_entries:
                file.write(entry + '\n')
        
        print(f"   ✅ Лог файл создан с {len(log_entries)} записями")
        
        # Анализ логов
        log_stats = {'INFO': 0, 'DEBUG': 0, 'WARNING': 0, 'ERROR': 0}
        error_entries = []
        
        with open(log_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                for level in log_stats:
                    if f' {level} ' in line:
                        log_stats[level] += 1
                        
                        if level == 'ERROR':
                            error_entries.append((line_num, line))
                        break
        
        print("   📊 Статистика по уровням логирования:")
        for level, count in log_stats.items():
            print(f"     {level:>7}: {count} записей")
        
        print("   🚨 Ошибки в логах:")
        for line_num, entry in error_entries:
            timestamp = entry.split(' ')[0:2]
            message = ' '.join(entry.split(' ')[3:])
            print(f"     Строка {line_num}: {' '.join(timestamp)} - {message}")
        
        return log_file
    
    log_file = log_operations()
    
    print("\n6. Конвертация между форматами:")
    
    def format_conversion():
        """Конвертация данных между форматами"""
        
        print("   Конвертация JSON → CSV:")
        
        # Читаем JSON
        with open(json_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        # Сохраняем как CSV (только пользователей)
        converted_csv = 'converted_users.csv'
        
        with open(converted_csv, 'w', newline='', encoding='utf-8') as file:
            if json_data['users']:
                writer = csv.DictWriter(file, fieldnames=json_data['users'][0].keys())
                writer.writeheader()
                
                for user in json_data['users']:
                    # Преобразуем список в строку
                    user_copy = user.copy()
                    user_copy['skills'] = '|'.join(user['skills'])
                    writer.writerow(user_copy)
        
        print(f"     ✅ Создан {converted_csv}")
        
        # Проверяем размеры файлов
        json_size = os.path.getsize(json_file)
        csv_size = os.path.getsize(converted_csv)
        
        print(f"     📏 JSON: {json_size} байт, CSV: {csv_size} байт")
        print(f"     📊 CSV составляет {(csv_size/json_size)*100:.1f}% от размера JSON")
        
        return converted_csv
    
    converted_file = format_conversion()
    
    # Очистка
    print("\n7. Созданные файлы:")
    created_files = [json_file, csv_file, xml_file, ini_file, log_file, converted_file]
    
    total_size = 0
    for filename in created_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            total_size += size
            print(f"   📄 {filename}: {size} байт")
    
    print(f"   📦 Общий размер: {total_size} байт")
    
    # Удаляем файлы
    print("\n8. Очистка:")
    for filename in created_files:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"   🗑️ Удален {filename}")


def example_05_secure_file_operations():
    """
    Пример 5: Безопасные файловые операции
    
    Демонстрирует безопасные техники работы с файлами:
    валидация путей, атомарные операции, обработка ошибок.
    """
    print("=== Пример 5: Безопасные файловые операции ===")
    
    print("1. Валидация и санитизация путей:")
    
    def validate_file_path(filepath, allowed_dirs=None):
        """Валидация пути к файлу"""
        
        if allowed_dirs is None:
            allowed_dirs = ['.', './data', './temp']
        
        try:
            # Нормализация пути
            normalized_path = os.path.normpath(filepath)
            absolute_path = os.path.abspath(normalized_path)
            
            print(f"   🔍 Проверка пути: {filepath}")
            print(f"     Нормализован: {normalized_path}")
            print(f"     Абсолютный: {absolute_path}")
            
            # Проверка на path traversal
            if '..' in normalized_path:
                print("     ❌ Обнаружен path traversal (..)")
                return False
            
            # Проверка разрешенных директорий
            path_obj = Path(absolute_path)
            current_dir = Path.cwd()
            
            is_in_allowed_dir = False
            for allowed_dir in allowed_dirs:
                allowed_path = current_dir / allowed_dir
                try:
                    path_obj.relative_to(allowed_path.resolve())
                    is_in_allowed_dir = True
                    print(f"     ✅ Путь в разрешенной директории: {allowed_dir}")
                    break
                except ValueError:
                    continue
            
            if not is_in_allowed_dir:
                print(f"     ❌ Путь не в разрешенных директориях: {allowed_dirs}")
                return False
            
            # Проверка длины имени файла
            filename = os.path.basename(filepath)
            if len(filename) > 255:
                print("     ❌ Слишком длинное имя файла")
                return False
            
            # Проверка на недопустимые символы
            invalid_chars = '<>:"|?*'
            if any(char in filename for char in invalid_chars):
                print(f"     ❌ Недопустимые символы в имени файла: {invalid_chars}")
                return False
            
            print("     ✅ Путь прошел все проверки")
            return True
            
        except Exception as e:
            print(f"     ❌ Ошибка валидации: {e}")
            return False
    
    # Тестируем различные пути
    test_paths = [
        "safe_file.txt",           # Безопасный
        "./data/config.json",      # Безопасный
        "../../../etc/passwd",     # Path traversal
        "normal_file_name.txt",    # Безопасный
        "file<with>invalid:chars.txt",  # Недопустимые символы
        "a" * 300 + ".txt"         # Слишком длинное имя
    ]
    
    for test_path in test_paths:
        validate_file_path(test_path)
        print()
    
    print("2. Атомарные операции с файлами:")
    
    @contextmanager
    def atomic_write(filepath, mode='w', encoding='utf-8', **kwargs):
        """Контекстный менеджер для атомарной записи"""
        
        # Создаем временный файл в той же директории
        dir_path = os.path.dirname(filepath) or '.'
        
        with tempfile.NamedTemporaryFile(
            mode=mode,
            encoding=encoding if 'b' not in mode else None,
            dir=dir_path,
            delete=False,
            **kwargs
        ) as temp_file:
            
            temp_filepath = temp_file.name
            
            try:
                print(f"   📝 Атомарная запись в {filepath}")
                print(f"     Временный файл: {temp_filepath}")
                
                yield temp_file
                
                # Принудительная запись на диск
                temp_file.flush()
                os.fsync(temp_file.fileno())
                
            except Exception:
                # При ошибке удаляем временный файл
                if os.path.exists(temp_filepath):
                    os.unlink(temp_filepath)
                raise
        
        # Атомарное перемещение временного файла
        try:
            if os.name == 'nt':  # Windows
                if os.path.exists(filepath):
                    os.unlink(filepath)
            
            shutil.move(temp_filepath, filepath)
            print(f"     ✅ Файл атомарно записан")
            
        except Exception as e:
            if os.path.exists(temp_filepath):
                os.unlink(temp_filepath)
            raise e
    
    # Тестируем атомарную запись
    def test_atomic_write():
        test_file = "atomic_test.txt"
        
        try:
            with atomic_write(test_file) as f:
                f.write("Первая строка\n")
                f.write("Вторая строка\n")
                # Симулируем задержку
                time.sleep(0.1)
                f.write("Третья строка\n")
            
            # Проверяем результат
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.strip().split('\n')
                print(f"     📖 Записано {len(lines)} строк")
            
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)
    
    test_atomic_write()
    
    print("\n3. Безопасная работа с временными файлами:")
    
    def secure_temp_operations():
        """Безопасные операции с временными файлами"""
        
        print("   🔒 Создание безопасных временных файлов:")
        
        # Безопасный временный файл
        with tempfile.NamedTemporaryFile(
            mode='w+',
            encoding='utf-8',
            prefix='secure_',
            suffix='.tmp',
            delete=True
        ) as temp_file:
            
            print(f"     Временный файл: {temp_file.name}")
            
            # Проверяем права доступа
            stat_info = os.stat(temp_file.name)
            permissions = oct(stat_info.st_mode)[-3:]
            print(f"     Права доступа: {permissions}")
            
            # Записываем конфиденциальные данные
            sensitive_data = """
            Конфиденциальная информация:
            - Пароль базы данных: secret123
            - API ключ: abc-def-ghi-jkl
            - Токен доступа: xyz789
            """
            
            temp_file.write(sensitive_data)
            temp_file.flush()
            
            # Читаем обратно
            temp_file.seek(0)
            read_data = temp_file.read()
            
            print(f"     Записано {len(read_data)} символов")
            print("     ✅ Файл будет автоматически удален")
        
        print("     ✅ Временный файл удален")
        
        # Безопасная временная директория
        with tempfile.TemporaryDirectory(prefix='secure_dir_') as temp_dir:
            print(f"   📁 Временная директория: {temp_dir}")
            
            # Создаем файлы в временной директории
            for i in range(3):
                file_path = os.path.join(temp_dir, f"temp_file_{i}.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Временный файл номер {i}")
            
            # Показываем содержимое
            files = os.listdir(temp_dir)
            print(f"     Создано файлов: {len(files)}")
            
        print("     ✅ Временная директория удалена")
    
    secure_temp_operations()
    
    print("\n4. Обработка ошибок доступа к файлам:")
    
    def handle_file_errors():
        """Обработка различных ошибок при работе с файлами"""
        
        error_scenarios = [
            ("nonexistent_file.txt", "r", "Файл не существует"),
            ("/root/protected_file.txt", "w", "Нет прав доступа"),
            ("", "w", "Пустое имя файла"),
            ("con", "w", "Зарезервированное имя (Windows)")
        ]
        
        for filepath, mode, description in error_scenarios:
            print(f"   🧪 Тест: {description}")
            
            try:
                with open(filepath, mode, encoding='utf-8') as f:
                    f.write("test data")
                
                print("     ✅ Операция успешна")
                
                # Удаляем файл если он был создан
                if os.path.exists(filepath):
                    os.remove(filepath)
                
            except FileNotFoundError:
                print("     📁 FileNotFoundError: Файл или директория не найдены")
            except PermissionError:
                print("     🔒 PermissionError: Недостаточно прав доступа")
            except OSError as e:
                print(f"     💥 OSError: {e}")
            except Exception as e:
                print(f"     ❌ Неожиданная ошибка: {type(e).__name__}: {e}")
    
    handle_file_errors()
    
    print("\n5. Мониторинг файловых операций:")
    
    class FileOperationMonitor:
        """Монитор файловых операций"""
        
        def __init__(self):
            self.operations = []
        
        @contextmanager
        def monitor_operation(self, operation_type, filepath):
            """Мониторинг файловой операции"""
            
            start_time = time.perf_counter()
            operation_id = len(self.operations) + 1
            
            print(f"   🔍 [{operation_id}] Начало: {operation_type} {filepath}")
            
            try:
                yield
                
                end_time = time.perf_counter()
                duration = end_time - start_time
                
                self.operations.append({
                    'id': operation_id,
                    'type': operation_type,
                    'filepath': filepath,
                    'duration': duration,
                    'success': True,
                    'timestamp': time.time()
                })
                
                print(f"   ✅ [{operation_id}] Успех: {duration:.3f}s")
                
            except Exception as e:
                end_time = time.perf_counter()
                duration = end_time - start_time
                
                self.operations.append({
                    'id': operation_id,
                    'type': operation_type,
                    'filepath': filepath,
                    'duration': duration,
                    'success': False,
                    'error': str(e),
                    'timestamp': time.time()
                })
                
                print(f"   ❌ [{operation_id}] Ошибка: {e} ({duration:.3f}s)")
                raise
        
        def get_stats(self):
            """Получить статистику операций"""
            if not self.operations:
                return {}
            
            successful = [op for op in self.operations if op['success']]
            failed = [op for op in self.operations if not op['success']]
            
            total_duration = sum(op['duration'] for op in self.operations)
            avg_duration = total_duration / len(self.operations)
            
            return {
                'total_operations': len(self.operations),
                'successful': len(successful),
                'failed': len(failed),
                'success_rate': len(successful) / len(self.operations) * 100,
                'total_duration': total_duration,
                'average_duration': avg_duration
            }
    
    # Тестируем мониторинг
    monitor = FileOperationMonitor()
    
    # Успешные операции
    with monitor.monitor_operation("CREATE", "monitored_file.txt"):
        with open("monitored_file.txt", 'w', encoding='utf-8') as f:
            f.write("Мониторируемая операция записи")
    
    with monitor.monitor_operation("READ", "monitored_file.txt"):
        with open("monitored_file.txt", 'r', encoding='utf-8') as f:
            content = f.read()
    
    # Операция с ошибкой
    try:
        with monitor.monitor_operation("READ", "nonexistent.txt"):
            with open("nonexistent.txt", 'r', encoding='utf-8') as f:
                content = f.read()
    except FileNotFoundError:
        pass  # Ожидаемая ошибка
    
    # Статистика
    stats = monitor.get_stats()
    print(f"\n   📊 Статистика файловых операций:")
    print(f"     Всего операций: {stats['total_operations']}")
    print(f"     Успешных: {stats['successful']}")
    print(f"     С ошибками: {stats['failed']}")
    print(f"     Процент успеха: {stats['success_rate']:.1f}%")
    print(f"     Общее время: {stats['total_duration']:.3f}s")
    print(f"     Среднее время: {stats['average_duration']:.3f}s")
    
    # Очистка
    print("\n6. Очистка:")
    test_files = ["monitored_file.txt"]
    
    for filepath in test_files:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"   🗑️ Удален {filepath}")


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Основные операции с файлами", example_01_basic_file_operations),
        ("Работа с кодировками", example_02_encoding_handling),
        ("Обработка больших файлов", example_03_large_file_processing),
        ("Структурированные форматы данных", example_04_structured_data_formats),
        ("Безопасные файловые операции", example_05_secure_file_operations),
    ]
    
    print("📁 Примеры: Работа с файлами в Python")
    print("=" * 70)
    print("Эти примеры демонстрируют:")
    print("- Основные операции чтения и записи")
    print("- Работу с различными кодировками")
    print("- Эффективную обработку больших файлов")
    print("- Работу со структурированными форматами")
    print("- Безопасные техники работы с файлами")
    print("=" * 70)
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")
        print("-" * (len(name) + 3))
        try:
            func()
        except Exception as e:
            print(f"Ошибка при выполнении примера: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(examples):
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main() 