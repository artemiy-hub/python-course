#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Работа с файлами Python

Этот файл содержит подробные примеры для изучения:
- Основ чтения и записи файлов
- Работы с различными кодировками
- Использования контекстных менеджеров
- Работы с путями и директориями
- Обработки различных форматов файлов
- Работы с архивами и временными файлами
- Оптимизации для больших файлов
"""

import os
import json
import csv
import xml.etree.ElementTree as ET
import zipfile
import tarfile
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import time
import mmap


def example_01_basic_file_operations():
    """
    Пример 1: Основные операции с файлами
    
    Демонстрирует базовые операции чтения и записи файлов,
    различные режимы открытия и методы работы.
    """
    print("=== Пример 1: Основные операции с файлами ===")
    
    # Создаем тестовые данные
    test_content = """Привет, мир!
Это тестовый файл для демонстрации.
Строка номер три.
И еще одна строка с числом: 42"""
    
    filename = "test_file.txt"
    
    print("1. Запись файла:")
    
    # Запись файла (режим 'w' - перезапись)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(test_content)
    print(f"Файл '{filename}' создан и записан")
    
    # Добавление к файлу (режим 'a' - добавление)
    with open(filename, 'a', encoding='utf-8') as f:
        f.write("\nДобавленная строка")
    print("Добавлена новая строка")
    
    print("\n2. Чтение файла различными способами:")
    
    # Способ 1: read() - весь файл
    with open(filename, 'r', encoding='utf-8') as f:
        full_content = f.read()
        print("Полное содержимое файла:")
        print(repr(full_content[:50]) + "..." if len(full_content) > 50 else repr(full_content))
    
    # Способ 2: readlines() - все строки в список
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"\nВсего строк: {len(lines)}")
        for i, line in enumerate(lines[:3], 1):
            print(f"Строка {i}: {repr(line)}")
    
    # Способ 3: readline() - построчно
    with open(filename, 'r', encoding='utf-8') as f:
        print("\nЧтение построчно:")
        line_num = 1
        while True:
            line = f.readline()
            if not line:
                break
            print(f"Строка {line_num}: {line.strip()}")
            line_num += 1
            if line_num > 3:  # Ограничиваем вывод
                print("...")
                break
    
    # Способ 4: итерация (рекомендуется)
    print("\nИтерация по файлу (эффективный способ):")
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            print(f"Строка {i}: {line.strip()}")
            if i >= 3:
                print("...")
                break
    
    print("\n3. Позиционирование в файле:")
    
    with open(filename, 'r', encoding='utf-8') as f:
        print(f"Начальная позиция: {f.tell()}")
        
        # Читаем первые 10 символов
        chunk = f.read(10)
        print(f"Прочитано: {repr(chunk)}")
        print(f"Текущая позиция: {f.tell()}")
        
        # Возвращаемся в начало
        f.seek(0)
        print(f"После seek(0): {f.tell()}")
        
        # Переходим в конец файла
        f.seek(0, 2)  # 2 = конец файла
        print(f"Размер файла: {f.tell()} байт")
    
    print("\n4. Различные режимы файлов:")
    
    binary_file = "test_binary.bin"
    
    # Бинарная запись
    with open(binary_file, 'wb') as f:
        binary_data = "Тест бинарных данных".encode('utf-8')
        f.write(binary_data)
    
    # Бинарное чтение
    with open(binary_file, 'rb') as f:
        binary_content = f.read()
        print(f"Бинарные данные: {binary_content}")
        print(f"Декодированные: {binary_content.decode('utf-8')}")
    
    # Режим r+ (чтение и запись)
    with open(filename, 'r+', encoding='utf-8') as f:
        f.seek(0, 2)  # В конец файла
        f.write("\nДобавлено в режиме r+")
    
    print("Файлы созданы и обработаны успешно!")
    
    # Очистка
    try:
        os.unlink(filename)
        os.unlink(binary_file)
        print("Тестовые файлы удалены")
    except FileNotFoundError:
        pass


def example_02_encoding_handling():
    """
    Пример 2: Работа с кодировками
    
    Демонстрирует работу с различными кодировками,
    обработку ошибок и определение кодировки файлов.
    """
    print("=== Пример 2: Работа с кодировками ===")
    
    # Тестовый текст с различными символами
    test_texts = {
        'utf-8': "Привет, мир! 🌍 Hello, world! こんにちは",
        'cp1251': "Привет, мир! Тест кириллицы",
        'ascii': "Hello, world! ASCII only"
    }
    
    print("1. Создание файлов с различными кодировками:")
    
    for encoding, text in test_texts.items():
        filename = f"test_{encoding.replace('-', '_')}.txt"
        try:
            with open(filename, 'w', encoding=encoding) as f:
                f.write(text)
            print(f"✓ Файл {filename} создан с кодировкой {encoding}")
        except UnicodeEncodeError as e:
            print(f"✗ Ошибка записи в {encoding}: {e}")
    
    print("\n2. Чтение файлов с указанием кодировки:")
    
    for encoding in test_texts.keys():
        filename = f"test_{encoding.replace('-', '_')}.txt"
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"✓ {encoding}: {content}")
            except UnicodeDecodeError as e:
                print(f"✗ Ошибка чтения {encoding}: {e}")
    
    print("\n3. Демонстрация ошибок кодировки:")
    
    # Создаем файл в UTF-8
    utf8_file = "test_utf8_demo.txt"
    with open(utf8_file, 'w', encoding='utf-8') as f:
        f.write("Тест UTF-8: 🐍 Python")
    
    # Пытаемся прочитать как ASCII
    error_strategies = ['strict', 'ignore', 'replace', 'backslashreplace']
    
    for strategy in error_strategies:
        try:
            with open(utf8_file, 'r', encoding='ascii', errors=strategy) as f:
                content = f.read()
            print(f"Стратегия '{strategy}': {repr(content)}")
        except UnicodeDecodeError as e:
            print(f"Стратегия '{strategy}': ОШИБКА - {e}")
    
    print("\n4. Определение кодировки файла:")
    
    def simple_encoding_detection(filename):
        """Простое определение кодировки"""
        encodings_to_try = ['utf-8', 'cp1251', 'ascii', 'utf-16']
        
        for encoding in encodings_to_try:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                continue
        return None
    
    for encoding in ['utf_8', 'cp1251']:
        filename = f"test_{encoding}.txt"
        if os.path.exists(filename):
            detected = simple_encoding_detection(filename)
            print(f"Файл {filename}: обнаружена кодировка {detected}")
    
    print("\n5. Работа с BOM (Byte Order Mark):")
    
    # Создание файла с BOM
    bom_file = "test_bom.txt"
    with open(bom_file, 'w', encoding='utf-8-sig') as f:  # -sig добавляет BOM
        f.write("Файл с BOM")
    
    # Чтение без учета BOM
    with open(bom_file, 'rb') as f:
        raw_data = f.read()
        print(f"Сырые данные: {raw_data}")
    
    # Чтение с учетом BOM
    with open(bom_file, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        print(f"Содержимое: {repr(content)}")
    
    # Очистка
    test_files = ['test_utf_8.txt', 'test_cp1251.txt', 'test_ascii.txt', 
                  utf8_file, bom_file]
    for filename in test_files:
        try:
            os.unlink(filename)
        except FileNotFoundError:
            pass
    
    print("Демонстрация кодировок завершена")


def example_03_context_managers():
    """
    Пример 3: Контекстные менеджеры
    
    Демонстрирует использование контекстных менеджеров
    для безопасной работы с файлами и создание собственных.
    """
    print("=== Пример 3: Контекстные менеджеры ===")
    
    print("1. Стандартный контекстный менеджер:")
    
    filename = "context_test.txt"
    
    # Правильный способ с with
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Тест контекстного менеджера")
        print(f"Файл открыт: {not f.closed}")
    
    print(f"После выхода из контекста файл закрыт: {f.closed}")
    
    print("\n2. Множественные файлы:")
    
    input_file = "input.txt"
    output_file = "output.txt"
    
    # Создаем входной файл
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write("строка 1\nстрока 2\nстрока 3\n")
    
    # Обработка с двумя файлами одновременно
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line_num, line in enumerate(infile, 1):
            outfile.write(f"{line_num}: {line}")
    
    # Проверяем результат
    with open(output_file, 'r', encoding='utf-8') as f:
        print("Результат обработки:")
        print(f.read())
    
    print("\n3. Собственный контекстный менеджер:")
    
    class FileManager:
        """Собственный контекстный менеджер для файлов"""
        
        def __init__(self, filename, mode, encoding='utf-8'):
            self.filename = filename
            self.mode = mode
            self.encoding = encoding
            self.file = None
            self.start_time = None
        
        def __enter__(self):
            print(f"📂 Открываем файл: {self.filename}")
            self.start_time = time.time()
            self.file = open(self.filename, self.mode, encoding=self.encoding)
            return self.file
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.file:
                self.file.close()
            
            duration = time.time() - self.start_time
            print(f"📁 Файл {self.filename} закрыт через {duration:.3f}s")
            
            if exc_type:
                print(f"⚠️ Произошла ошибка: {exc_type.__name__}: {exc_val}")
                return False  # Не подавляем исключение
            
            return True
    
    # Использование собственного менеджера
    test_file = "custom_manager_test.txt"
    
    with FileManager(test_file, 'w') as f:
        f.write("Тест собственного контекстного менеджера\n")
        f.write("Время работы отслеживается\n")
        time.sleep(0.1)  # Имитируем работу
    
    print("\n4. Контекстный менеджер с обработкой ошибок:")
    
    class SafeFileManager:
        """Безопасный файловый менеджер с обработкой ошибок"""
        
        def __init__(self, filename, mode, encoding='utf-8', backup=True):
            self.filename = filename
            self.mode = mode
            self.encoding = encoding
            self.backup = backup
            self.file = None
            self.backup_file = None
        
        def __enter__(self):
            # Создаем резервную копию при записи
            if self.backup and 'w' in self.mode and os.path.exists(self.filename):
                self.backup_file = self.filename + '.backup'
                shutil.copy2(self.filename, self.backup_file)
                print(f"💾 Создана резервная копия: {self.backup_file}")
            
            try:
                self.file = open(self.filename, self.mode, encoding=self.encoding)
                return self.file
            except Exception as e:
                print(f"❌ Ошибка открытия файла: {e}")
                raise
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.file:
                self.file.close()
            
            if exc_type:
                print(f"❌ Ошибка во время работы с файлом: {exc_val}")
                
                # Восстанавливаем из резервной копии
                if self.backup_file and os.path.exists(self.backup_file):
                    shutil.move(self.backup_file, self.filename)
                    print(f"🔄 Файл восстановлен из резервной копии")
                
                return False
            else:
                # Удаляем резервную копию при успешном завершении
                if self.backup_file and os.path.exists(self.backup_file):
                    os.unlink(self.backup_file)
                    print(f"🗑️ Резервная копия удалена")
                
                return True
    
    # Тестируем безопасный менеджер
    safe_test_file = "safe_test.txt"
    
    # Создаем исходный файл
    with open(safe_test_file, 'w', encoding='utf-8') as f:
        f.write("Исходное содержимое\n")
    
    # Успешная операция
    print("Тест успешной операции:")
    with SafeFileManager(safe_test_file, 'w') as f:
        f.write("Новое содержимое\n")
        f.write("Операция прошла успешно\n")
    
    # Проверяем результат
    with open(safe_test_file, 'r', encoding='utf-8') as f:
        print(f"Результат: {f.read().strip()}")
    
    print("\n5. Контекстный менеджер для временных файлов:")
    
    class TempFileManager:
        """Менеджер временных файлов"""
        
        def __init__(self, suffix='.tmp', prefix='temp_', dir=None):
            self.suffix = suffix
            self.prefix = prefix
            self.dir = dir
            self.temp_file = None
            self.temp_path = None
        
        def __enter__(self):
            self.temp_file = tempfile.NamedTemporaryFile(
                mode='w+', 
                suffix=self.suffix,
                prefix=self.prefix,
                dir=self.dir,
                delete=False,
                encoding='utf-8'
            )
            self.temp_path = self.temp_file.name
            print(f"🔧 Создан временный файл: {self.temp_path}")
            return self.temp_file
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.temp_file:
                self.temp_file.close()
            
            if self.temp_path and os.path.exists(self.temp_path):
                os.unlink(self.temp_path)
                print(f"🧹 Временный файл удален: {self.temp_path}")
    
    # Использование временного файла
    with TempFileManager(suffix='.txt', prefix='demo_') as temp_f:
        temp_f.write("Временные данные\n")
        temp_f.write("Автоматически удалятся\n")
        temp_f.seek(0)
        content = temp_f.read()
        print(f"Содержимое временного файла: {content.strip()}")
    
    # Очистка
    test_files = [filename, input_file, output_file, test_file, safe_test_file]
    for f in test_files:
        try:
            os.unlink(f)
        except FileNotFoundError:
            pass
    
    print("Демонстрация контекстных менеджеров завершена")


def example_04_path_operations():
    """
    Пример 4: Работа с путями и директориями
    
    Демонстрирует современные способы работы с файловыми путями
    используя pathlib и классические методы os.path.
    """
    print("=== Пример 4: Работа с путями и директориями ===")
    
    print("1. Основы pathlib:")
    
    # Создание путей
    current_dir = Path('.')
    file_path = Path('documents') / 'projects' / 'python' / 'main.py'
    abs_path = Path.home() / 'documents' / 'file.txt'
    
    print(f"Текущая директория: {current_dir}")
    print(f"Относительный путь: {file_path}")
    print(f"Абсолютный путь: {abs_path}")
    
    # Компоненты пути
    demo_path = Path('/home/user/documents/project/main.py')
    print(f"\nКомпоненты пути {demo_path}:")
    print(f"  name: {demo_path.name}")
    print(f"  stem: {demo_path.stem}")
    print(f"  suffix: {demo_path.suffix}")
    print(f"  suffixes: {demo_path.suffixes}")
    print(f"  parent: {demo_path.parent}")
    print(f"  parents: {list(demo_path.parents)}")
    print(f"  parts: {demo_path.parts}")
    print(f"  anchor: {demo_path.anchor}")
    
    print("\n2. Создание и управление директориями:")
    
    # Создаем тестовую структуру директорий
    test_dir = Path('test_directory_structure')
    sub_dirs = [
        test_dir / 'documents',
        test_dir / 'projects' / 'python',
        test_dir / 'projects' / 'web',
        test_dir / 'downloads',
        test_dir / 'temp'
    ]
    
    for directory in sub_dirs:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"📁 Создана директория: {directory}")
    
    # Создаем файлы в директориях
    test_files = [
        test_dir / 'documents' / 'readme.txt',
        test_dir / 'projects' / 'python' / 'main.py',
        test_dir / 'projects' / 'web' / 'index.html',
        test_dir / 'downloads' / 'file.zip',
        test_dir / 'temp' / 'cache.tmp'
    ]
    
    for file_path in test_files:
        file_path.write_text(f"Содержимое файла {file_path.name}", encoding='utf-8')
        print(f"📄 Создан файл: {file_path}")
    
    print("\n3. Обход директорий:")
    
    # Метод 1: iterdir() - содержимое директории
    print("Содержимое test_directory_structure:")
    for item in test_dir.iterdir():
        if item.is_dir():
            print(f"📁 {item.name}/")
        else:
            print(f"📄 {item.name}")
    
    # Метод 2: glob() - поиск по паттерну
    print("\nПоиск файлов .py:")
    for py_file in test_dir.glob('**/*.py'):
        print(f"🐍 {py_file}")
    
    # Метод 3: rglob() - рекурсивный поиск
    print("\nВсе файлы (рекурсивно):")
    for file_path in test_dir.rglob('*'):
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"📄 {file_path.relative_to(test_dir)} ({size} байт)")
    
    print("\n4. Информация о файлах и директориях:")
    
    for file_path in test_files[:3]:
        if file_path.exists():
            stat = file_path.stat()
            print(f"\nИнформация о {file_path.name}:")
            print(f"  Размер: {stat.st_size} байт")
            print(f"  Изменен: {datetime.fromtimestamp(stat.st_mtime)}")
            print(f"  Права доступа: {oct(stat.st_mode)[-3:]}")
            print(f"  Это файл: {file_path.is_file()}")
            print(f"  Это директория: {file_path.is_dir()}")
    
    print("\n5. Фильтрация файлов:")
    
    def find_files_by_criteria(directory, **criteria):
        """Находит файлы по различным критериям"""
        results = []
        
        for file_path in Path(directory).rglob('*'):
            if not file_path.is_file():
                continue
            
            # Фильтр по расширению
            if 'extension' in criteria:
                if file_path.suffix.lower() != criteria['extension'].lower():
                    continue
            
            # Фильтр по размеру
            if 'min_size' in criteria:
                if file_path.stat().st_size < criteria['min_size']:
                    continue
            
            # Фильтр по имени
            if 'name_contains' in criteria:
                if criteria['name_contains'].lower() not in file_path.name.lower():
                    continue
            
            results.append(file_path)
        
        return results
    
    # Примеры фильтрации
    python_files = find_files_by_criteria(test_dir, extension='.py')
    print(f"Python файлы: {[f.name for f in python_files]}")
    
    files_with_main = find_files_by_criteria(test_dir, name_contains='main')
    print(f"Файлы с 'main' в имени: {[f.name for f in files_with_main]}")
    
    print("\n6. Операции с файлами:")
    
    # Копирование
    source_file = test_dir / 'documents' / 'readme.txt'
    backup_file = test_dir / 'documents' / 'readme_backup.txt'
    shutil.copy2(source_file, backup_file)
    print(f"📋 Скопирован файл: {source_file.name} -> {backup_file.name}")
    
    # Перемещение
    temp_file = test_dir / 'temp' / 'moved_file.txt'
    backup_file.replace(temp_file)
    print(f"🔄 Перемещен файл: {backup_file.name} -> {temp_file.name}")
    
    # Переименование
    old_name = temp_file
    new_name = test_dir / 'temp' / 'renamed_file.txt'
    old_name.rename(new_name)
    print(f"✏️ Переименован файл: {old_name.name} -> {new_name.name}")
    
    print("\n7. Сравнение pathlib и os.path:")
    
    sample_path = "/home/user/documents/project/main.py"
    
    print("pathlib:")
    p = Path(sample_path)
    print(f"  Родительская директория: {p.parent}")
    print(f"  Имя файла: {p.name}")
    print(f"  Расширение: {p.suffix}")
    
    print("os.path:")
    print(f"  Родительская директория: {os.path.dirname(sample_path)}")
    print(f"  Имя файла: {os.path.basename(sample_path)}")
    print(f"  Расширение: {os.path.splitext(sample_path)[1]}")
    
    # Очистка
    shutil.rmtree(test_dir)
    print(f"\n🧹 Тестовая структура директорий удалена")


def example_05_file_formats():
    """
    Пример 5: Работа с различными форматами файлов
    
    Демонстрирует работу с CSV, JSON, XML и другими
    популярными форматами файлов.
    """
    print("=== Пример 5: Работа с различными форматами файлов ===")
    
    # Тестовые данные
    test_data = [
        {"name": "Алиса", "age": 25, "city": "Москва", "skills": ["Python", "SQL"]},
        {"name": "Боб", "age": 30, "city": "СПб", "skills": ["JavaScript", "React"]},
        {"name": "Чарли", "age": 28, "city": "Казань", "skills": ["Java", "Spring"]},
        {"name": "Диана", "age": 26, "city": "Екатеринбург", "skills": ["C#", ".NET"]}
    ]
    
    print("1. Работа с CSV файлами:")
    
    csv_file = "employees.csv"
    
    # Запись CSV с помощью writer
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Заголовки
        writer.writerow(['Имя', 'Возраст', 'Город', 'Навыки'])
        
        # Данные
        for person in test_data:
            writer.writerow([
                person['name'], 
                person['age'], 
                person['city'],
                ', '.join(person['skills'])
            ])
    
    print(f"CSV файл '{csv_file}' создан")
    
    # Чтение CSV
    print("Содержимое CSV файла:")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row_num, row in enumerate(reader):
            print(f"  Строка {row_num}: {row}")
    
    # Работа с CSV через DictWriter/DictReader
    csv_dict_file = "employees_dict.csv"
    
    with open(csv_dict_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'age', 'city', 'skills']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for person in test_data:
            # Преобразуем навыки в строку для CSV
            person_copy = person.copy()
            person_copy['skills'] = ', '.join(person['skills'])
            writer.writerow(person_copy)
    
    print("Чтение CSV как словарей:")
    with open(csv_dict_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for person in reader:
            print(f"  {person['name']}, {person['age']} лет, {person['city']}")
    
    print("\n2. Работа с JSON файлами:")
    
    json_file = "employees.json"
    
    # Запись JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON файл '{json_file}' создан")
    
    # Чтение JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    
    print("Данные из JSON:")
    for person in loaded_data:
        skills = ', '.join(person['skills'])
        print(f"  {person['name']}: {skills}")
    
    # JSON с дополнительными опциями
    json_formatted_file = "employees_formatted.json"
    
    # Добавляем метаданные
    json_data_with_meta = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "1.0",
            "total_records": len(test_data)
        },
        "employees": test_data
    }
    
    with open(json_formatted_file, 'w', encoding='utf-8') as f:
        json.dump(json_data_with_meta, f, 
                 ensure_ascii=False, 
                 indent=4, 
                 sort_keys=True)
    
    print(f"Форматированный JSON файл создан")
    
    print("\n3. Работа с XML файлами:")
    
    xml_file = "employees.xml"
    
    # Создание XML
    root = ET.Element("employees")
    
    for person in test_data:
        employee = ET.SubElement(root, "employee", id=str(person['age']))
        
        name_elem = ET.SubElement(employee, "name")
        name_elem.text = person['name']
        
        age_elem = ET.SubElement(employee, "age")
        age_elem.text = str(person['age'])
        
        city_elem = ET.SubElement(employee, "city")
        city_elem.text = person['city']
        
        skills_elem = ET.SubElement(employee, "skills")
        for skill in person['skills']:
            skill_elem = ET.SubElement(skills_elem, "skill")
            skill_elem.text = skill
    
    # Сохранение XML
    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    
    print(f"XML файл '{xml_file}' создан")
    
    # Чтение XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    print("Данные из XML:")
    for employee in root.findall('employee'):
        name = employee.find('name').text
        age = employee.find('age').text
        city = employee.find('city').text
        
        skills = []
        skills_elem = employee.find('skills')
        if skills_elem is not None:
            for skill in skills_elem.findall('skill'):
                skills.append(skill.text)
        
        print(f"  {name}, {age} лет, {city} - {', '.join(skills)}")
    
    print("\n4. Работа с INI файлами:")
    
    import configparser
    
    ini_file = "config.ini"
    
    # Создание INI файла
    config = configparser.ConfigParser()
    
    config['DEFAULT'] = {
        'debug': 'false',
        'log_level': 'info'
    }
    
    config['database'] = {
        'host': 'localhost',
        'port': '5432',
        'name': 'myapp',
        'user': 'admin'
    }
    
    config['api'] = {
        'base_url': 'https://api.example.com',
        'timeout': '30',
        'retries': '3'
    }
    
    with open(ini_file, 'w') as f:
        config.write(f)
    
    print(f"INI файл '{ini_file}' создан")
    
    # Чтение INI файла
    config_read = configparser.ConfigParser()
    config_read.read(ini_file)
    
    print("Конфигурация из INI файла:")
    for section_name in config_read.sections():
        print(f"  [{section_name}]")
        for key, value in config_read.items(section_name):
            print(f"    {key} = {value}")
    
    print("\n5. Универсальный обработчик файлов:")
    
    class FileFormatHandler:
        """Универсальный обработчик различных форматов файлов"""
        
        @staticmethod
        def save_data(data, filename, format_type='auto'):
            """Сохраняет данные в указанном формате"""
            if format_type == 'auto':
                format_type = Path(filename).suffix.lower()[1:]  # без точки
            
            if format_type == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            elif format_type == 'csv':
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                else:
                    raise ValueError("CSV требует список словарей")
            
            else:
                raise ValueError(f"Неподдерживаемый формат: {format_type}")
        
        @staticmethod
        def load_data(filename, format_type='auto'):
            """Загружает данные из файла"""
            if format_type == 'auto':
                format_type = Path(filename).suffix.lower()[1:]
            
            if format_type == 'json':
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            elif format_type == 'csv':
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    return list(reader)
            
            else:
                raise ValueError(f"Неподдерживаемый формат: {format_type}")
    
    # Тестируем универсальный обработчик
    handler = FileFormatHandler()
    
    # Сохраняем в разных форматах
    handler.save_data(test_data, "test_data.json")
    handler.save_data(test_data, "test_data.csv")
    
    # Загружаем обратно
    loaded_json = handler.load_data("test_data.json")
    loaded_csv = handler.load_data("test_data.csv")
    
    print("Данные загружены через универсальный обработчик:")
    print(f"  JSON: {len(loaded_json)} записей")
    print(f"  CSV: {len(loaded_csv)} записей")
    
    # Очистка
    test_files = [csv_file, csv_dict_file, json_file, json_formatted_file, 
                  xml_file, ini_file, "test_data.json", "test_data.csv"]
    for filename in test_files:
        try:
            os.unlink(filename)
        except FileNotFoundError:
            pass
    
    print("Демонстрация форматов файлов завершена")


def example_06_archives_and_compression():
    """
    Пример 6: Работа с архивами и сжатием
    
    Демонстрирует создание и извлечение ZIP и TAR архивов,
    работу с различными методами сжатия.
    """
    print("=== Пример 6: Работа с архивами и сжатием ===")
    
    # Создаем тестовые файлы для архивирования
    test_dir = Path('archive_test')
    test_dir.mkdir(exist_ok=True)
    
    test_files = {
        'readme.txt': 'Это файл readme с описанием проекта.\nВторая строка файла.',
        'data.json': '{"users": [{"name": "Alice", "age": 25}], "version": "1.0"}',
        'config.ini': '[database]\nhost=localhost\nport=5432\n\n[app]\ndebug=true',
        'script.py': '#!/usr/bin/env python3\nprint("Hello, World!")\n',
        'subdir/nested.txt': 'Файл во вложенной директории'
    }
    
    # Создаем файлы
    for filepath, content in test_files.items():
        full_path = test_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
    
    print(f"Создана тестовая структура в {test_dir}")
    
    print("\n1. Создание ZIP архива:")
    
    zip_file = 'test_archive.zip'
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Добавляем файлы в архив
        for file_path in test_dir.rglob('*'):
            if file_path.is_file():
                # Относительный путь в архиве
                arcname = file_path.relative_to(test_dir)
                zipf.write(file_path, arcname)
                print(f"  📄 Добавлен: {arcname}")
    
    print(f"ZIP архив '{zip_file}' создан")
    
    # Информация об архиве
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        info = zipf.infolist()
        total_size = sum(f.file_size for f in info)
        compressed_size = sum(f.compress_size for f in info)
        compression_ratio = (1 - compressed_size / total_size) * 100
        
        print(f"Файлов в архиве: {len(info)}")
        print(f"Исходный размер: {total_size} байт")
        print(f"Сжатый размер: {compressed_size} байт")
        print(f"Степень сжатия: {compression_ratio:.1f}%")
    
    print("\n2. Извлечение из ZIP архива:")
    
    extract_dir = Path('extracted_zip')
    extract_dir.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        # Список файлов в архиве
        file_list = zipf.namelist()
        print("Файлы в архиве:")
        for filename in file_list:
            print(f"  📄 {filename}")
        
        # Извлечение всех файлов
        zipf.extractall(extract_dir)
        print(f"Файлы извлечены в {extract_dir}")
        
        # Извлечение конкретного файла
        if 'readme.txt' in file_list:
            zipf.extract('readme.txt', extract_dir / 'specific')
            print("Файл readme.txt извлечен отдельно")
    
    print("\n3. Чтение файлов из архива без извлечения:")
    
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        # Читаем файл прямо из архива
        if 'data.json' in zipf.namelist():
            with zipf.open('data.json') as f:
                content = f.read().decode('utf-8')
                print(f"Содержимое data.json из архива: {content}")
    
    print("\n4. Создание TAR архива:")
    
    tar_file = 'test_archive.tar.gz'
    
    with tarfile.open(tar_file, 'w:gz') as tar:
        # Добавляем всю директорию
        tar.add(test_dir, arcname='test_data')
        print(f"Директория {test_dir} добавлена в TAR архив")
    
    # Информация о TAR архиве
    with tarfile.open(tar_file, 'r:gz') as tar:
        members = tar.getmembers()
        print(f"TAR архив содержит {len(members)} элементов:")
        for member in members:
            type_char = 'd' if member.isdir() else 'f'
            print(f"  {type_char} {member.name} ({member.size} байт)")
    
    print("\n5. Извлечение из TAR архива:")
    
    extract_tar_dir = Path('extracted_tar')
    extract_tar_dir.mkdir(exist_ok=True)
    
    with tarfile.open(tar_file, 'r:gz') as tar:
        tar.extractall(extract_tar_dir)
        print(f"TAR архив извлечен в {extract_tar_dir}")
    
    print("\n6. Различные типы сжатия:")
    
    compression_types = [
        ('test_none.tar', 'w'),           # Без сжатия
        ('test_gzip.tar.gz', 'w:gz'),     # GZIP
        ('test_bzip2.tar.bz2', 'w:bz2'),  # BZIP2
    ]
    
    # Добавляем LZMA если доступен
    try:
        import lzma
        compression_types.append(('test_lzma.tar.xz', 'w:xz'))
    except ImportError:
        pass
    
    print("Сравнение методов сжатия:")
    
    for archive_name, mode in compression_types:
        try:
            with tarfile.open(archive_name, mode) as tar:
                tar.add(test_dir, arcname='data')
            
            size = os.path.getsize(archive_name)
            print(f"  {archive_name}: {size} байт")
            
        except Exception as e:
            print(f"  {archive_name}: Ошибка - {e}")
    
    print("\n7. Архивация с фильтрацией:")
    
    def create_filtered_archive(source_dir, archive_name, extensions=None):
        """Создает архив только с файлами определенных расширений"""
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if not file_path.is_file():
                    continue
                
                if extensions and file_path.suffix.lower() not in extensions:
                    continue
                
                arcname = file_path.relative_to(source_dir)
                zipf.write(file_path, arcname)
                print(f"  ✓ {arcname}")
    
    # Архивируем только текстовые файлы
    filtered_archive = 'text_files_only.zip'
    print(f"Создание архива только с текстовыми файлами:")
    create_filtered_archive(test_dir, filtered_archive, ['.txt', '.py', '.ini'])
    
    print("\n8. Класс для работы с архивами:")
    
    class ArchiveManager:
        """Универсальный менеджер архивов"""
        
        @staticmethod
        def create_archive(source_path, archive_path, compression='auto'):
            """Создает архив из директории или файла"""
            source = Path(source_path)
            archive = Path(archive_path)
            
            if compression == 'auto':
                if archive.suffix.lower() == '.zip':
                    return ArchiveManager._create_zip(source, archive)
                elif archive.suffix.lower() in ['.tar', '.gz', '.bz2', '.xz']:
                    return ArchiveManager._create_tar(source, archive)
                else:
                    raise ValueError(f"Неизвестный тип архива: {archive.suffix}")
        
        @staticmethod
        def _create_zip(source, archive):
            """Создает ZIP архив"""
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if source.is_file():
                    zipf.write(source, source.name)
                else:
                    for file_path in source.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(source.parent)
                            zipf.write(file_path, arcname)
        
        @staticmethod
        def _create_tar(source, archive):
            """Создает TAR архив"""
            if archive.suffix == '.gz':
                mode = 'w:gz'
            elif archive.suffix == '.bz2':
                mode = 'w:bz2'
            elif archive.suffix == '.xz':
                mode = 'w:xz'
            else:
                mode = 'w'
            
            with tarfile.open(archive, mode) as tar:
                tar.add(source, arcname=source.name)
        
        @staticmethod
        def extract_archive(archive_path, extract_path):
            """Извлекает архив"""
            archive = Path(archive_path)
            extract_dir = Path(extract_path)
            extract_dir.mkdir(parents=True, exist_ok=True)
            
            if archive.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive, 'r') as zipf:
                    zipf.extractall(extract_dir)
            else:
                with tarfile.open(archive, 'r') as tar:
                    tar.extractall(extract_dir)
    
    # Тестируем архивный менеджер
    manager = ArchiveManager()
    
    test_archive = 'manager_test.zip'
    manager.create_archive(test_dir, test_archive)
    print(f"Архив {test_archive} создан через менеджер")
    
    extract_manager_dir = Path('extracted_manager')
    manager.extract_archive(test_archive, extract_manager_dir)
    print(f"Архив извлечен в {extract_manager_dir}")
    
    # Очистка
    cleanup_items = [
        test_dir, extract_dir, extract_tar_dir, extract_manager_dir,
        zip_file, tar_file, filtered_archive, test_archive
    ]
    
    for archive_name, _ in compression_types:
        cleanup_items.append(archive_name)
    
    for item in cleanup_items:
        try:
            if Path(item).is_dir():
                shutil.rmtree(item)
            else:
                os.unlink(item)
        except (FileNotFoundError, OSError):
            pass
    
    print("Демонстрация архивов завершена")


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Основные операции с файлами", example_01_basic_file_operations),
        ("Работа с кодировками", example_02_encoding_handling),
        ("Контекстные менеджеры", example_03_context_managers),
        ("Работа с путями и директориями", example_04_path_operations),
        ("Форматы файлов", example_05_file_formats),
        ("Архивы и сжатие", example_06_archives_and_compression),
    ]
    
    print("📁 Примеры: Работа с файлами Python")
    print("=" * 50)
    
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