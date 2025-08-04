# Теория: Работа с файлами в Python

## 🎯 Цель раздела

Работа с файлами - одна из основных задач в программировании. Python предоставляет мощные и гибкие инструменты для работы с файлами различных типов. Этот раздел охватывает все аспекты файловых операций в Python.

## 📋 Содержание

1. [Основы работы с файлами](#основы-работы-с-файлами)
2. [Режимы открытия файлов](#режимы-открытия-файлов)
3. [Чтение файлов](#чтение-файлов)
4. [Запись файлов](#запись-файлов)
5. [Контекстные менеджеры](#контекстные-менеджеры)
6. [Кодировки и Unicode](#кодировки-и-unicode)
7. [Работа с путями](#работа-с-путями)
8. [Файловые операции](#файловые-операции)
9. [Форматы файлов](#форматы-файлов)
10. [Продвинутые техники](#продвинутые-техники)

---

## 📁 Основы работы с файлами

### Что такое файл?

**Файл** - это именованная область данных на носителе информации. В Python файлы представлены как объекты, с которыми можно выполнять различные операции.

```python
# Основная функция для работы с файлами
file_object = open('filename.txt', 'mode', encoding='utf-8')

# Основные операции
content = file_object.read()    # Чтение
file_object.write('data')       # Запись
file_object.close()             # Закрытие

# Безопасная работа с файлами
with open('filename.txt', 'r', encoding='utf-8') as file:
    content = file.read()
# Файл автоматически закрывается
```

### Жизненный цикл файла

```python
# 1. Открытие файла
with open('example.txt', 'w', encoding='utf-8') as file:
    # 2. Работа с файлом
    file.write('Hello, World!')
    file.flush()  # Принудительная запись в файл
    
    # 3. Позиционирование
    file.seek(0)  # Переход в начало файла
    current_position = file.tell()  # Текущая позиция
    
# 4. Автоматическое закрытие при выходе из контекста
```

### Атрибуты файлового объекта

```python
with open('example.txt', 'r', encoding='utf-8') as file:
    print(f"Имя файла: {file.name}")
    print(f"Режим: {file.mode}")
    print(f"Кодировка: {file.encoding}")
    print(f"Закрыт ли файл: {file.closed}")
    print(f"Доступен ли для чтения: {file.readable()}")
    print(f"Доступен ли для записи: {file.writable()}")
    print(f"Поддерживает ли поиск: {file.seekable()}")
```

---

## 🔧 Режимы открытия файлов

### Основные режимы

```python
# Режимы чтения
'r'   # Чтение (по умолчанию)
'rb'  # Чтение в бинарном режиме
'rt'  # Чтение в текстовом режиме (явно)

# Режимы записи
'w'   # Запись (перезаписывает файл)
'wb'  # Запись в бинарном режиме
'wt'  # Запись в текстовом режиме

# Режимы добавления
'a'   # Добавление в конец файла
'ab'  # Добавление в бинарном режиме
'at'  # Добавление в текстовом режиме

# Режимы чтения и записи
'r+'  # Чтение и запись
'w+'  # Запись и чтение (создает новый файл)
'a+'  # Добавление и чтение

# Эксклюзивное создание
'x'   # Эксклюзивное создание (ошибка если файл существует)
'xb'  # Эксклюзивное создание в бинарном режиме
```

### Подробное описание режимов

```python
import os

def demonstrate_file_modes():
    """Демонстрация различных режимов открытия файлов"""
    
    # Создаем тестовый файл
    test_file = 'test_modes.txt'
    
    # 1. Режим 'w' - запись (перезапись)
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write('Первая строка\n')
        f.write('Вторая строка\n')
    
    print("После записи в режиме 'w':")
    with open(test_file, 'r', encoding='utf-8') as f:
        print(f.read())
    
    # 2. Режим 'a' - добавление
    with open(test_file, 'a', encoding='utf-8') as f:
        f.write('Третья строка\n')
        f.write('Четвертая строка\n')
    
    print("После добавления в режиме 'a':")
    with open(test_file, 'r', encoding='utf-8') as f:
        print(f.read())
    
    # 3. Режим 'r+' - чтение и запись
    with open(test_file, 'r+', encoding='utf-8') as f:
        content = f.read()
        print(f"Прочитано: {len(content)} символов")
        
        # Перейти в начало и перезаписать
        f.seek(0)
        f.write('ПЕРЕЗАПИСАНО\n')
    
    print("После частичной перезаписи в режиме 'r+':")
    with open(test_file, 'r', encoding='utf-8') as f:
        print(f.read())
    
    # 4. Режим 'x' - эксклюзивное создание
    exclusive_file = 'exclusive_test.txt'
    try:
        with open(exclusive_file, 'x', encoding='utf-8') as f:
            f.write('Файл создан в режиме x')
        print("Файл успешно создан в режиме 'x'")
        
        # Попытка создать еще раз - ошибка
        with open(exclusive_file, 'x', encoding='utf-8') as f:
            f.write('Это не выполнится')
    except FileExistsError:
        print("Ошибка: файл уже существует (режим 'x')")
    
    # Очистка
    for filename in [test_file, exclusive_file]:
        if os.path.exists(filename):
            os.remove(filename)

# Вызов демонстрации
# demonstrate_file_modes()
```

### Бинарный vs текстовый режим

```python
# Текстовый режим (по умолчанию)
with open('text_file.txt', 'w', encoding='utf-8') as f:
    f.write('Привет, мир! 🐍')  # Автоматическое преобразование в байты

with open('text_file.txt', 'r', encoding='utf-8') as f:
    text = f.read()  # Получаем строку
    print(f"Тип: {type(text)}, содержимое: {text}")

# Бинарный режим
with open('binary_file.bin', 'wb') as f:
    data = 'Привет, мир! 🐍'.encode('utf-8')
    f.write(data)  # Записываем байты

with open('binary_file.bin', 'rb') as f:
    binary_data = f.read()  # Получаем bytes
    print(f"Тип: {type(binary_data)}")
    text = binary_data.decode('utf-8')
    print(f"Декодировано: {text}")

# Смешанный режим для изображений, видео и других бинарных данных
def copy_binary_file(source, destination):
    """Копирование бинарного файла"""
    with open(source, 'rb') as src:
        with open(destination, 'wb') as dst:
            # Копируем по частям для больших файлов
            while True:
                chunk = src.read(8192)  # 8KB за раз
                if not chunk:
                    break
                dst.write(chunk)
```

---

## 📖 Чтение файлов

### Методы чтения

```python
# Различные способы чтения файла
def demonstrate_reading_methods():
    """Демонстрация методов чтения файлов"""
    
    # Создаем тестовый файл
    test_content = """Первая строка
Вторая строка с числами: 123
Третья строка с символами: @#$%
Четвертая строка
Пятая и последняя строка"""
    
    with open('read_test.txt', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("=== Методы чтения файлов ===")
    
    # 1. read() - читает весь файл
    with open('read_test.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"1. read() - весь файл ({len(content)} символов):")
        print(repr(content[:50]) + "...")
    
    # 2. read(size) - читает указанное количество символов
    with open('read_test.txt', 'r', encoding='utf-8') as f:
        chunk1 = f.read(10)
        chunk2 = f.read(10)
        print(f"\n2. read(size) - по частям:")
        print(f"   Первые 10: {repr(chunk1)}")
        print(f"   Следующие 10: {repr(chunk2)}")
    
    # 3. readline() - читает одну строку
    with open('read_test.txt', 'r', encoding='utf-8') as f:
        line1 = f.readline()
        line2 = f.readline()
        print(f"\n3. readline() - по строкам:")
        print(f"   Строка 1: {repr(line1)}")
        print(f"   Строка 2: {repr(line2)}")
    
    # 4. readlines() - читает все строки в список
    with open('read_test.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"\n4. readlines() - все строки в список:")
        print(f"   Количество строк: {len(lines)}")
        print(f"   Первая строка: {repr(lines[0])}")
    
    # 5. Итерация по файлу
    print(f"\n5. Итерация по файлу:")
    with open('read_test.txt', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            print(f"   Строка {i}: {line.strip()}")
    
    # 6. Чтение с позиционированием
    print(f"\n6. Позиционирование:")
    with open('read_test.txt', 'r', encoding='utf-8') as f:
        print(f"   Начальная позиция: {f.tell()}")
        
        first_10 = f.read(10)
        print(f"   После чтения 10 символов: {f.tell()}")
        
        f.seek(0)  # Возврат в начало
        print(f"   После seek(0): {f.tell()}")
        
        f.seek(5)  # Переход к 5-му символу
        next_5 = f.read(5)
        print(f"   С 5-го символа прочитано: {repr(next_5)}")
    
    # Очистка
    import os
    os.remove('read_test.txt')

# demonstrate_reading_methods()
```

### Обработка больших файлов

```python
def read_large_file_efficiently(filename, chunk_size=8192):
    """Эффективное чтение больших файлов по частям"""
    
    total_size = 0
    line_count = 0
    
    with open(filename, 'r', encoding='utf-8') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            
            total_size += len(chunk)
            line_count += chunk.count('\n')
    
    return total_size, line_count

def read_file_by_lines_generator(filename):
    """Генератор для построчного чтения файла"""
    with open(filename, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, 1):
            yield line_number, line.rstrip('\n\r')

# Пример использования генератора
def process_large_file(filename):
    """Обработка большого файла без загрузки в память"""
    for line_num, line in read_file_by_lines_generator(filename):
        # Обработка строки
        if line_num % 10000 == 0:  # Прогресс каждые 10000 строк
            print(f"Обработано {line_num} строк")
        
        # Поиск или обработка данных
        if 'error' in line.lower():
            print(f"Ошибка в строке {line_num}: {line}")

# Чтение файла в обратном порядке
def read_file_reverse(filename, buf_size=8192):
    """Чтение файла с конца (для логов)"""
    with open(filename, 'rb') as f:
        # Переходим в конец файла
        f.seek(0, 2)
        file_size = f.tell()
        
        lines = []
        buffer = b''
        position = file_size
        
        while position > 0:
            # Читаем блок
            read_size = min(buf_size, position)
            position -= read_size
            f.seek(position)
            
            chunk = f.read(read_size)
            buffer = chunk + buffer
            
            # Разбиваем на строки
            while b'\n' in buffer:
                line, buffer = buffer.rsplit(b'\n', 1)
                lines.append(line.decode('utf-8'))
        
        # Добавляем оставшуюся часть
        if buffer:
            lines.append(buffer.decode('utf-8'))
        
        return lines

# Пример использования
def tail_file(filename, num_lines=10):
    """Аналог команды tail - последние N строк"""
    lines = read_file_reverse(filename)
    return lines[:num_lines]
```

### Безопасное чтение

```python
import os
from pathlib import Path

def safe_read_file(filename, encoding='utf-8', fallback_encoding='latin-1'):
    """Безопасное чтение файла с обработкой ошибок"""
    
    # Проверка существования файла
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл не найден: {filename}")
    
    # Проверка разрешений
    if not os.access(filename, os.R_OK):
        raise PermissionError(f"Нет прав на чтение файла: {filename}")
    
    # Попытка чтения с основной кодировкой
    try:
        with open(filename, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        print(f"Ошибка декодирования с {encoding}, пробуем {fallback_encoding}")
        
        # Fallback кодировка
        try:
            with open(filename, 'r', encoding=fallback_encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            # Чтение с игнорированием ошибок
            with open(filename, 'r', encoding=encoding, errors='ignore') as file:
                return file.read()

def read_with_progress(filename, callback=None):
    """Чтение файла с индикацией прогресса"""
    
    # Получаем размер файла
    file_size = Path(filename).stat().st_size
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = []
        bytes_read = 0
        
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            
            content.append(chunk)
            bytes_read += len(chunk.encode('utf-8'))
            
            # Вызываем callback с прогрессом
            if callback:
                progress = (bytes_read / file_size) * 100
                callback(progress)
        
        return ''.join(content)

# Пример callback для прогресса
def progress_callback(progress):
    """Отображение прогресса чтения"""
    bar_length = 30
    filled_length = int(bar_length * progress / 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f'\rПрогресс: |{bar}| {progress:.1f}%', end='', flush=True)
```

---

## ✍️ Запись файлов

### Методы записи

```python
def demonstrate_writing_methods():
    """Демонстрация методов записи в файлы"""
    
    print("=== Методы записи в файлы ===")
    
    # 1. write() - запись строки
    with open('write_test.txt', 'w', encoding='utf-8') as f:
        chars_written = f.write('Первая строка\n')
        print(f"1. write() записал {chars_written} символов")
        
        f.write('Вторая строка\n')
        f.write('Третья строка без переноса')
    
    # 2. writelines() - запись списка строк
    lines = [
        'Четвертая строка\n',
        'Пятая строка\n',
        'Шестая строка\n'
    ]
    
    with open('write_test.txt', 'a', encoding='utf-8') as f:
        f.writelines(lines)
        print("2. writelines() добавил список строк")
    
    # 3. print() в файл
    with open('write_test.txt', 'a', encoding='utf-8') as f:
        print('Седьмая строка через print()', file=f)
        print('Восьмая строка', 'с несколькими', 'аргументами', file=f)
        print('Девятая строка', end=' (без переноса)\n', file=f)
        print("3. print() добавил форматированные строки")
    
    # 4. Запись с форматированием
    data = {'name': 'Python', 'version': 3.12, 'year': 2023}
    
    with open('write_test.txt', 'a', encoding='utf-8') as f:
        # Различные способы форматирования
        f.write(f"f-string: {data['name']} версии {data['version']}\n")
        f.write("format(): {} версии {}\n".format(data['name'], data['version']))
        f.write("%-форматирование: %s версии %.1f\n" % (data['name'], data['version']))
    
    print("4. Записаны форматированные строки")
    
    # 5. Запись числовых данных
    numbers = [1, 2, 3, 4, 5, 3.14, 2.71]
    
    with open('numbers.txt', 'w', encoding='utf-8') as f:
        # Каждое число на отдельной строке
        for num in numbers:
            f.write(f"{num}\n")
        
        # Числа через запятую
        f.write(','.join(map(str, numbers)) + '\n')
        
        # Форматированные числа
        for num in numbers:
            if isinstance(num, float):
                f.write(f"{num:.2f}\n")
            else:
                f.write(f"{num:04d}\n")
    
    print("5. Записаны числовые данные")
    
    # Чтение результатов
    print("\n=== Результат записи ===")
    with open('write_test.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print("write_test.txt:")
        print(content)
    
    with open('numbers.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print("numbers.txt:")
        print(content)
    
    # Очистка
    import os
    for filename in ['write_test.txt', 'numbers.txt']:
        if os.path.exists(filename):
            os.remove(filename)

# demonstrate_writing_methods()
```

### Атомарная запись

```python
import os
import tempfile
import shutil

def atomic_write(filename, content, encoding='utf-8'):
    """Атомарная запись в файл (все или ничего)"""
    
    # Создаем временный файл в той же директории
    dir_name = os.path.dirname(filename) or '.'
    
    with tempfile.NamedTemporaryFile(
        mode='w', 
        encoding=encoding, 
        dir=dir_name, 
        delete=False
    ) as temp_file:
        
        temp_filename = temp_file.name
        
        try:
            # Записываем содержимое во временный файл
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())  # Принудительная запись на диск
            
        except Exception:
            # Если произошла ошибка, удаляем временный файл
            os.unlink(temp_filename)
            raise
    
    # Атомарно перемещаем временный файл на место целевого
    if os.name == 'nt':  # Windows
        # На Windows нужно удалить целевой файл перед перемещением
        if os.path.exists(filename):
            os.unlink(filename)
    
    shutil.move(temp_filename, filename)

# Пример использования
def save_config_atomically(config_data, filename):
    """Атомарное сохранение конфигурации"""
    import json
    
    config_json = json.dumps(config_data, indent=2, ensure_ascii=False)
    atomic_write(filename, config_json)
    print(f"Конфигурация атомарно сохранена в {filename}")

# Тест атомарной записи
config = {
    'database': {'host': 'localhost', 'port': 5432},
    'server': {'host': '0.0.0.0', 'port': 8000},
    'debug': True
}

# save_config_atomically(config, 'config.json')
```

### Буферизация записи

```python
def demonstrate_buffering():
    """Демонстрация буферизации при записи"""
    
    import time
    
    print("=== Буферизация записи ===")
    
    # 1. Стандартная буферизация
    with open('buffered_test.txt', 'w', encoding='utf-8') as f:
        print("Записываем данные с обычной буферизацией...")
        
        for i in range(5):
            f.write(f"Строка {i}\n")
            print(f"Записали строку {i}")
            time.sleep(0.5)  # Пауза для демонстрации
            
            # Данные могут быть еще в буфере!
    
    # 2. Принудительная запись
    with open('flushed_test.txt', 'w', encoding='utf-8') as f:
        print("\nЗаписываем данные с принудительным сбросом буфера...")
        
        for i in range(5):
            f.write(f"Строка {i}\n")
            f.flush()  # Принудительный сброс буфера
            print(f"Записали и сбросили строку {i}")
            time.sleep(0.5)
    
    # 3. Небуферизованная запись
    with open('unbuffered_test.txt', 'w', encoding='utf-8', buffering=1) as f:
        print("\nЗаписываем данные с построчной буферизацией...")
        
        for i in range(5):
            f.write(f"Строка {i}\n")  # Автоматический flush после \n
            print(f"Записали строку {i} (автоматический flush)")
            time.sleep(0.5)
    
    # 4. Полностью небуферизованная запись (только для бинарных файлов)
    with open('binary_unbuffered.bin', 'wb', buffering=0) as f:
        print("\nБинарная запись без буферизации...")
        
        for i in range(5):
            data = f"Строка {i}\n".encode('utf-8')
            f.write(data)  # Немедленная запись
            print(f"Записали байты строки {i}")
            time.sleep(0.5)
    
    # Очистка
    import os
    for filename in ['buffered_test.txt', 'flushed_test.txt', 
                     'unbuffered_test.txt', 'binary_unbuffered.bin']:
        if os.path.exists(filename):
            os.remove(filename)

# demonstrate_buffering()
```

### Запись структурированных данных

```python
def write_structured_data():
    """Запись структурированных данных в различных форматах"""
    
    # Тестовые данные
    data = {
        'users': [
            {'id': 1, 'name': 'Алиса', 'email': 'alice@example.com', 'age': 25},
            {'id': 2, 'name': 'Боб', 'email': 'bob@example.com', 'age': 30},
            {'id': 3, 'name': 'Чарли', 'email': 'charlie@example.com', 'age': 35}
        ],
        'settings': {
            'theme': 'dark',
            'language': 'ru',
            'notifications': True
        },
        'metadata': {
            'version': '1.0.0',
            'created': '2024-01-01',
            'updated': '2024-01-15'
        }
    }
    
    # 1. CSV формат
    import csv
    
    with open('users.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'email', 'age'])
        writer.writeheader()
        writer.writerows(data['users'])
    
    print("1. Данные сохранены в CSV")
    
    # 2. JSON формат
    import json
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("2. Данные сохранены в JSON")
    
    # 3. XML формат (простой)
    def dict_to_xml(data, root_name='root'):
        """Простое преобразование словаря в XML"""
        def _dict_to_xml(d, parent_name):
            if isinstance(d, dict):
                result = []
                for key, value in d.items():
                    result.append(f"<{key}>{_dict_to_xml(value, key)}</{key}>")
                return ''.join(result)
            elif isinstance(d, list):
                result = []
                for item in d:
                    result.append(f"<item>{_dict_to_xml(item, 'item')}</item>")
                return ''.join(result)
            else:
                return str(d)
        
        return f"<?xml version='1.0' encoding='UTF-8'?>\n<{root_name}>{_dict_to_xml(data, root_name)}</{root_name}>"
    
    xml_content = dict_to_xml(data, 'application_data')
    
    with open('data.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print("3. Данные сохранены в XML")
    
    # 4. INI формат
    import configparser
    
    config = configparser.ConfigParser()
    config['settings'] = data['settings']
    config['metadata'] = data['metadata']
    
    with open('config.ini', 'w', encoding='utf-8') as f:
        config.write(f)
    
    print("4. Настройки сохранены в INI")
    
    # 5. Собственный формат
    with open('custom_format.txt', 'w', encoding='utf-8') as f:
        f.write("# Пользователи\n")
        for user in data['users']:
            f.write(f"USER:{user['id']}:{user['name']}:{user['email']}:{user['age']}\n")
        
        f.write("\n# Настройки\n")
        for key, value in data['settings'].items():
            f.write(f"SETTING:{key}={value}\n")
        
        f.write("\n# Метаданные\n")
        for key, value in data['metadata'].items():
            f.write(f"META:{key}={value}\n")
    
    print("5. Данные сохранены в собственном формате")
    
    # Проверяем созданные файлы
    import os
    created_files = ['users.csv', 'data.json', 'data.xml', 'config.ini', 'custom_format.txt']
    
    print(f"\nСозданные файлы:")
    for filename in created_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  {filename}: {size} байт")
    
    # Читаем для проверки
    print(f"\nПример содержимого custom_format.txt:")
    with open('custom_format.txt', 'r', encoding='utf-8') as f:
        print(f.read())

# write_structured_data()
```

---

## 🔒 Контекстные менеджеры

### Стандартные контекстные менеджеры

```python
# Базовое использование with
with open('example.txt', 'w', encoding='utf-8') as file:
    file.write('Содержимое файла')
# Файл автоматически закрывается

# Эквивалентно следующему коду:
file = open('example.txt', 'w', encoding='utf-8')
try:
    file.write('Содержимое файла')
finally:
    file.close()
```

### Множественные файлы

```python
# Работа с несколькими файлами одновременно
def copy_file_with_context(source, destination):
    """Копирование файла с использованием контекстных менеджеров"""
    
    with open(source, 'r', encoding='utf-8') as src, \
         open(destination, 'w', encoding='utf-8') as dst:
        
        # Копируем содержимое
        for line in src:
            dst.write(line)
    
    print(f"Файл скопирован из {source} в {destination}")

# Альтернативный синтаксис
def copy_file_alternative(source, destination):
    """Альтернативный способ работы с несколькими файлами"""
    
    with open(source, 'r', encoding='utf-8') as src:
        with open(destination, 'w', encoding='utf-8') as dst:
            content = src.read()
            dst.write(content)
```

### Собственные контекстные менеджеры

```python
from contextlib import contextmanager
import time
import os

# Способ 1: Декоратор @contextmanager
@contextmanager
def timed_file_operation(filename, mode='r'):
    """Контекстный менеджер с измерением времени операции"""
    print(f"Открываем файл {filename} в режиме {mode}")
    start_time = time.time()
    
    try:
        file = open(filename, mode, encoding='utf-8')
        yield file
    finally:
        if not file.closed:
            file.close()
        
        end_time = time.time()
        print(f"Операция с файлом заняла {end_time - start_time:.3f} секунд")

# Использование
with timed_file_operation('test.txt', 'w') as f:
    f.write('Тестовое содержимое')
    time.sleep(0.1)  # Симуляция работы

# Способ 2: Класс с __enter__ и __exit__
class FileManager:
    """Продвинутый менеджер файлов"""
    
    def __init__(self, filename, mode='r', encoding='utf-8', backup=False):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.backup = backup
        self.file = None
        self.backup_filename = None
    
    def __enter__(self):
        print(f"Открываем файл: {self.filename}")
        
        # Создаем резервную копию перед записью
        if self.backup and 'w' in self.mode and os.path.exists(self.filename):
            self.backup_filename = f"{self.filename}.backup"
            with open(self.filename, 'r', encoding=self.encoding) as src:
                with open(self.backup_filename, 'w', encoding=self.encoding) as dst:
                    dst.write(src.read())
            print(f"Создана резервная копия: {self.backup_filename}")
        
        self.file = open(self.filename, self.mode, encoding=self.encoding)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file and not self.file.closed:
            self.file.close()
            print(f"Файл закрыт: {self.filename}")
        
        if exc_type is not None:
            print(f"Произошла ошибка: {exc_type.__name__}: {exc_val}")
            
            # Восстанавливаем из резервной копии при ошибке
            if self.backup_filename and os.path.exists(self.backup_filename):
                print(f"Восстанавливаем из резервной копии...")
                with open(self.backup_filename, 'r', encoding=self.encoding) as src:
                    with open(self.filename, 'w', encoding=self.encoding) as dst:
                        dst.write(src.read())
        
        # Удаляем резервную копию при успешном завершении
        if exc_type is None and self.backup_filename and os.path.exists(self.backup_filename):
            os.remove(self.backup_filename)
            print(f"Резервная копия удалена")
        
        # Возвращаем False, чтобы исключение не подавлялось
        return False

# Использование собственного менеджера
def test_file_manager():
    # Создаем тестовый файл
    with open('original.txt', 'w') as f:
        f.write('Исходное содержимое файла')
    
    # Безопасная перезапись с резервным копированием
    try:
        with FileManager('original.txt', 'w', backup=True) as f:
            f.write('Новое содержимое файла')
            # Искусственная ошибка для демонстрации восстановления
            # raise ValueError("Тестовая ошибка")
    except ValueError as e:
        print(f"Обработана ошибка: {e}")
    
    # Проверяем содержимое
    with open('original.txt', 'r') as f:
        print(f"Итоговое содержимое: {f.read()}")

# test_file_manager()
```

### Контекстные менеджеры для различных операций

```python
import fcntl  # Только для Unix-систем
import tempfile
from contextlib import contextmanager

@contextmanager
def locked_file(filename, mode='r'):
    """Контекстный менеджер с блокировкой файла (Unix)"""
    file = open(filename, mode)
    try:
        # Блокируем файл (только для Unix)
        if hasattr(fcntl, 'flock'):
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        yield file
    finally:
        file.close()

@contextmanager
def temporary_file(suffix='', prefix='tmp', dir=None):
    """Контекстный менеджер для временного файла"""
    temp_file = tempfile.NamedTemporaryFile(
        mode='w+', 
        suffix=suffix, 
        prefix=prefix, 
        dir=dir, 
        delete=False
    )
    
    try:
        yield temp_file
    finally:
        temp_file.close()
        # Удаляем временный файл
        try:
            os.unlink(temp_file.name)
        except OSError:
            pass

@contextmanager
def chdir(path):
    """Контекстный менеджер для временной смены директории"""
    old_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(old_cwd)

# Пример использования
def demonstrate_custom_managers():
    # Временный файл
    with temporary_file(suffix='.txt', prefix='test_') as temp:
        temp.write('Временные данные')
        temp.flush()
        print(f"Временный файл создан: {temp.name}")
        
        # Файл будет автоматически удален после выхода из контекста
    
    # Временная смена директории
    print(f"Текущая директория: {os.getcwd()}")
    
    with chdir('/tmp' if os.name != 'nt' else 'C:\\'):
        print(f"Внутри контекста: {os.getcwd()}")
        # Можно работать в другой директории
    
    print(f"После контекста: {os.getcwd()}")

# demonstrate_custom_managers()
```

---

## 🌐 Кодировки и Unicode

### Основы кодировок

```python
# Кодировка определяет, как символы преобразуются в байты
text = "Привет, мир! 🐍"

# Различные кодировки
encodings = ['utf-8', 'utf-16', 'cp1251', 'ascii']

for encoding in encodings:
    try:
        encoded = text.encode(encoding)
        print(f"{encoding:>8}: {len(encoded)} байт - {encoded[:20]}...")
        
        # Декодирование обратно
        decoded = encoded.decode(encoding)
        print(f"         Декодировано: {decoded == text}")
        
    except UnicodeEncodeError as e:
        print(f"{encoding:>8}: Ошибка кодирования - {e}")
    except UnicodeDecodeError as e:
        print(f"{encoding:>8}: Ошибка декодирования - {e}")
    
    print()
```

### Работа с различными кодировками

```python
def demonstrate_encodings():
    """Демонстрация работы с различными кодировками"""
    
    # Текст с различными символами
    texts = {
        'ascii': "Hello, World!",
        'latin': "Café, naïve, résumé",
        'cyrillic': "Привет, мир!",
        'mixed': "Hello, мир! 🌍🐍",
        'special': "Math: ∑, ∆, ∞, ≈"
    }
    
    print("=== Работа с кодировками ===")
    
    for name, text in texts.items():
        print(f"\nТекст '{name}': {text}")
        
        # Пробуем различные кодировки
        encodings = ['utf-8', 'utf-16', 'cp1251', 'iso-8859-1', 'ascii']
        
        for encoding in encodings:
            try:
                # Кодируем
                encoded = text.encode(encoding)
                size = len(encoded)
                
                # Декодируем обратно
                decoded = encoded.decode(encoding)
                
                status = "✅" if decoded == text else "❌"
                print(f"  {encoding:>12}: {size:3d} байт {status}")
                
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                print(f"  {encoding:>12}: ❌ {type(e).__name__}")

# demonstrate_encodings()
```

### Автоматическое определение кодировки

```python
def detect_file_encoding(filename, sample_size=10000):
    """Автоматическое определение кодировки файла"""
    
    try:
        import chardet
        chardet_available = True
    except ImportError:
        chardet_available = False
        print("Модуль chardet не установлен, используем простое определение")
    
    # Читаем образец файла в бинарном режиме
    with open(filename, 'rb') as file:
        sample = file.read(sample_size)
    
    if chardet_available:
        # Используем chardet для точного определения
        result = chardet.detect(sample)
        encoding = result['encoding']
        confidence = result['confidence']
        
        print(f"Определена кодировка: {encoding} (уверенность: {confidence:.2%})")
        return encoding
    
    else:
        # Простое определение методом попыток
        common_encodings = ['utf-8', 'cp1251', 'iso-8859-1', 'utf-16']
        
        for encoding in common_encodings:
            try:
                sample.decode(encoding)
                print(f"Вероятная кодировка: {encoding}")
                return encoding
            except UnicodeDecodeError:
                continue
        
        print("Не удалось определить кодировку")
        return 'utf-8'  # Fallback

def safe_read_any_encoding(filename):
    """Безопасное чтение файла с любой кодировкой"""
    
    # Определяем кодировку
    encoding = detect_file_encoding(filename)
    
    # Читаем файл с определенной кодировкой
    try:
        with open(filename, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        # Если все же ошибка, читаем с игнорированием ошибок
        print(f"Ошибка чтения с {encoding}, читаем с errors='replace'")
        
        with open(filename, 'r', encoding=encoding, errors='replace') as file:
            return file.read()

# Создаем тестовые файлы с разными кодировками
def create_test_files():
    """Создание тестовых файлов с различными кодировками"""
    
    test_text = "Тестовый текст: ASCII, Русский, émoji 🎉"
    
    encodings = {
        'utf8_test.txt': 'utf-8',
        'cp1251_test.txt': 'cp1251',
        'utf16_test.txt': 'utf-16'
    }
    
    for filename, encoding in encodings.items():
        try:
            with open(filename, 'w', encoding=encoding) as file:
                file.write(test_text)
            print(f"Создан файл {filename} с кодировкой {encoding}")
        except UnicodeEncodeError:
            print(f"Не удалось создать файл с кодировкой {encoding}")

# create_test_files()
```

### Обработка ошибок кодирования

```python
def demonstrate_encoding_errors():
    """Демонстрация различных способов обработки ошибок кодирования"""
    
    # Текст, который нельзя закодировать в ASCII
    problematic_text = "Текст с émoji 🐍 и спецсимволами ∑∆"
    
    print("=== Обработка ошибок кодирования ===")
    print(f"Исходный текст: {problematic_text}")
    
    # Различные стратегии обработки ошибок
    error_handlers = {
        'strict': 'Строгий режим (по умолчанию)',
        'ignore': 'Игнорировать проблемные символы',
        'replace': 'Заменить на символ замещения',
        'xmlcharrefreplace': 'XML числовые ссылки',
        'backslashreplace': 'Escape-последовательности'
    }
    
    target_encoding = 'ascii'
    
    for handler, description in error_handlers.items():
        print(f"\n{handler} ({description}):")
        
        try:
            # Кодирование с обработкой ошибок
            encoded = problematic_text.encode(target_encoding, errors=handler)
            print(f"  Закодировано: {encoded}")
            
            # Декодирование обратно
            if handler != 'ignore':  # ignore может создать невалидные последовательности
                decoded = encoded.decode(target_encoding, errors=handler)
                print(f"  Декодировано: {decoded}")
            
        except UnicodeEncodeError as e:
            print(f"  Ошибка: {e}")
        except UnicodeDecodeError as e:
            print(f"  Ошибка декодирования: {e}")

# demonstrate_encoding_errors()
```

### Практические примеры с кодировками

```python
def convert_file_encoding(input_file, output_file, from_encoding, to_encoding):
    """Конвертация файла из одной кодировки в другую"""
    
    try:
        # Читаем в исходной кодировке
        with open(input_file, 'r', encoding=from_encoding) as f:
            content = f.read()
        
        # Записываем в целевой кодировке
        with open(output_file, 'w', encoding=to_encoding) as f:
            f.write(content)
        
        print(f"Файл сконвертирован: {from_encoding} → {to_encoding}")
        
    except UnicodeDecodeError as e:
        print(f"Ошибка чтения ({from_encoding}): {e}")
    except UnicodeEncodeError as e:
        print(f"Ошибка записи ({to_encoding}): {e}")

def fix_mojibake(filename, suspected_encoding, target_encoding='utf-8'):
    """Исправление 'мojibake' - неправильно декодированного текста"""
    
    with open(filename, 'r', encoding=target_encoding, errors='replace') as f:
        broken_text = f.read()
    
    print(f"Сломанный текст: {broken_text[:100]}...")
    
    try:
        # Пытаемся восстановить, кодируя обратно и декодируя правильно
        original_bytes = broken_text.encode('latin1')  # Часто помогает
        fixed_text = original_bytes.decode(suspected_encoding)
        
        # Сохраняем исправленный текст
        fixed_filename = filename.replace('.txt', '_fixed.txt')
        with open(fixed_filename, 'w', encoding=target_encoding) as f:
            f.write(fixed_text)
        
        print(f"Исправленный текст сохранен в {fixed_filename}")
        print(f"Исправленный текст: {fixed_text[:100]}...")
        
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        print(f"Не удалось исправить: {e}")

def analyze_file_encoding(filename):
    """Анализ кодировки файла и его содержимого"""
    
    print(f"=== Анализ файла {filename} ===")
    
    # Читаем файл в бинарном режиме
    with open(filename, 'rb') as f:
        raw_bytes = f.read()
    
    print(f"Размер файла: {len(raw_bytes)} байт")
    print(f"Первые 50 байт: {raw_bytes[:50]}")
    
    # Анализируем BOM (Byte Order Mark)
    bom_signatures = {
        b'\xef\xbb\xbf': 'UTF-8 BOM',
        b'\xff\xfe': 'UTF-16 LE BOM',
        b'\xfe\xff': 'UTF-16 BE BOM',
        b'\xff\xfe\x00\x00': 'UTF-32 LE BOM',
        b'\x00\x00\xfe\xff': 'UTF-32 BE BOM'
    }
    
    for bom, description in bom_signatures.items():
        if raw_bytes.startswith(bom):
            print(f"Обнаружен BOM: {description}")
            break
    else:
        print("BOM не обнаружен")
    
    # Пробуем различные кодировки
    common_encodings = ['utf-8', 'cp1251', 'iso-8859-1', 'utf-16']
    
    for encoding in common_encodings:
        try:
            decoded = raw_bytes.decode(encoding)
            print(f"\n{encoding}: Успешно декодировано")
            print(f"  Длина текста: {len(decoded)} символов")
            print(f"  Первые 100 символов: {decoded[:100]}")
            
        except UnicodeDecodeError as e:
            print(f"\n{encoding}: Ошибка декодирования")
            print(f"  {e}")

# Пример создания и анализа файлов
def encoding_examples():
    """Примеры работы с кодировками"""
    
    # Создаем файл с проблемной кодировкой
    problematic_text = "Файл с кириллицей: Привет, мир!"
    
    # Сохраняем в CP1251
    with open('cp1251_file.txt', 'w', encoding='cp1251') as f:
        f.write(problematic_text)
    
    # Конвертируем в UTF-8
    convert_file_encoding('cp1251_file.txt', 'utf8_file.txt', 'cp1251', 'utf-8')
    
    # Анализируем файлы
    for filename in ['cp1251_file.txt', 'utf8_file.txt']:
        if os.path.exists(filename):
            analyze_file_encoding(filename)

# encoding_examples()
```

Эта первая часть теории охватывает основные концепции работы с файлами. Продолжить с остальными разделами? 