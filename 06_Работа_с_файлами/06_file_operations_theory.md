# Теория: Работа с файлами в Python

## 🎯 Цели раздела

После изучения этого раздела вы будете:
- Понимать принципы работы с файлами в Python
- Уметь читать и записывать файлы различными способами
- Знать особенности работы с разными кодировками
- Понимать контекстные менеджеры и их применение
- Уметь работать с путями файлов и директориями
- Знать современные инструменты для работы с файловой системой

## 📁 Основы работы с файлами

### Что такое файл в Python

**Файл** — это именованная область хранения данных на диске. В Python файлы представлены файловыми объектами, которые предоставляют интерфейс для чтения и записи данных.

### Типы файлов

1. **Текстовые файлы** — содержат читаемый текст в определенной кодировке
2. **Бинарные файлы** — содержат данные в двоичном формате
3. **Специальные файлы** — CSV, JSON, XML и другие структурированные форматы

## 📖 Открытие файлов

### Функция open()

Основная функция для работы с файлами в Python:

```python
file_object = open(filename, mode='r', encoding=None, **kwargs)
```

#### Параметры функции open():

- **filename** — путь к файлу (строка или Path объект)
- **mode** — режим открытия файла
- **encoding** — кодировка для текстовых файлов
- **buffering** — размер буфера
- **errors** — стратегия обработки ошибок кодировки
- **newline** — обработка символов новой строки

### Режимы открытия файлов

#### Основные режимы:

| Режим | Описание | Позиция | Создание |
|-------|----------|---------|----------|
| `'r'` | Чтение (по умолчанию) | Начало | ❌ |
| `'w'` | Запись (перезапись) | Начало | ✅ |
| `'a'` | Добавление | Конец | ✅ |
| `'x'` | Эксклюзивное создание | Начало | ✅ |

#### Модификаторы режимов:

| Модификатор | Описание |
|-------------|----------|
| `'+'` | Чтение + запись |
| `'b'` | Бинарный режим |
| `'t'` | Текстовый режим (по умолчанию) |

#### Комбинированные режимы:

```python
# Примеры различных режимов
file1 = open('file.txt', 'r')        # Только чтение
file2 = open('file.txt', 'w')        # Только запись
file3 = open('file.txt', 'a')        # Добавление
file4 = open('file.txt', 'r+')       # Чтение и запись
file5 = open('file.txt', 'w+')       # Запись и чтение (очищает файл)
file6 = open('file.bin', 'rb')       # Бинарное чтение
file7 = open('file.bin', 'wb')       # Бинарная запись
file8 = open('file.txt', 'x')        # Создание нового файла
```

## 📝 Чтение файлов

### Методы чтения

#### 1. read() — чтение всего файла или N символов

```python
# Чтение всего файла
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()  # Вся содержимое в виде строки

# Чтение N символов
with open('file.txt', 'r', encoding='utf-8') as f:
    chunk = f.read(100)  # Первые 100 символов
```

#### 2. readline() — чтение одной строки

```python
with open('file.txt', 'r', encoding='utf-8') as f:
    first_line = f.readline()   # Первая строка
    second_line = f.readline()  # Вторая строка
```

#### 3. readlines() — чтение всех строк в список

```python
with open('file.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()  # Список всех строк
    
# Каждая строка содержит символ новой строки \n
for line in lines:
    print(repr(line))  # 'Hello\n', 'World\n', etc.
```

#### 4. Итерация по файлу (рекомендуется)

```python
# Самый эффективный способ для больших файлов
with open('file.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())  # Убираем \n в конце
```

### Позиционирование в файле

#### Методы работы с позицией:

```python
with open('file.txt', 'r', encoding='utf-8') as f:
    # Узнать текущую позицию
    position = f.tell()
    
    # Переместиться в начало файла
    f.seek(0)
    
    # Переместиться на 10 байт от начала
    f.seek(10, 0)  # 0 - от начала файла
    
    # Переместиться на 5 байт от текущей позиции
    f.seek(5, 1)   # 1 - от текущей позиции
    
    # Переместиться на 10 байт от конца файла
    f.seek(-10, 2) # 2 - от конца файла
```

## ✏️ Запись файлов

### Методы записи

#### 1. write() — запись строки

```python
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write("Привет, мир!")
    f.write("\nВторая строка")
    
# Запись возвращает количество записанных символов
bytes_written = f.write("Текст")
```

#### 2. writelines() — запись списка строк

```python
lines = ["Первая строка\n", "Вторая строка\n", "Третья строка\n"]

with open('file.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Внимание: writelines() НЕ добавляет символы новой строки автоматически!
```

#### 3. print() в файл

```python
with open('file.txt', 'w', encoding='utf-8') as f:
    print("Первая строка", file=f)
    print("Вторая строка", file=f)
    print("Число:", 42, file=f)
```

### Добавление в файл

```python
# Режим 'a' - добавление в конец файла
with open('file.txt', 'a', encoding='utf-8') as f:
    f.write("\nДобавленная строка")
```

## 🔐 Контекстные менеджеры

### Проблема управления ресурсами

```python
# ❌ Плохой способ - файл может не закрыться при ошибке
f = open('file.txt', 'r')
try:
    content = f.read()
    # Если здесь произойдет ошибка, файл не закроется
finally:
    f.close()
```

### Оператор with

```python
# ✅ Правильный способ - файл автоматически закроется
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    # Файл автоматически закроется даже при ошибке
```

### Множественные файлы

```python
# Открытие нескольких файлов одновременно
with open('input.txt', 'r') as infile, \
     open('output.txt', 'w') as outfile:
    data = infile.read()
    outfile.write(data.upper())
```

### Создание собственного контекстного менеджера

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Открываем файл {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Закрываем файл {self.filename}")
        if self.file:
            self.file.close()

# Использование
with FileManager('test.txt', 'w') as f:
    f.write("Тест")
```

## 🌍 Кодировки текста

### Основные кодировки

| Кодировка | Описание | Байт на символ |
|-----------|----------|----------------|
| ASCII | Базовая латиница | 1 |
| UTF-8 | Универсальная (рекомендуется) | 1-4 |
| UTF-16 | Широко используется в Windows | 2-4 |
| CP1251 | Кириллица в Windows | 1 |
| KOI8-R | Старая кириллица | 1 |

### Указание кодировки

```python
# Явное указание кодировки (рекомендуется)
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Автоопределение (может быть ненадежно)
with open('file.txt', 'r') as f:  # Использует locale.getpreferredencoding()
    content = f.read()
```

### Обработка ошибок кодировки

```python
# Различные стратегии обработки ошибок
strategies = [
    'strict',    # Выбросить исключение (по умолчанию)
    'ignore',    # Игнорировать проблемные символы
    'replace',   # Заменить на символ замещения (?)
    'backslashreplace',  # Заменить на \xNN или \uNNNN
    'xmlcharrefreplace', # Заменить на XML-ссылки &#NNNN;
]

for strategy in strategies:
    try:
        with open('file.txt', 'r', encoding='utf-8', errors=strategy) as f:
            content = f.read()
            print(f"Стратегия {strategy}: OK")
    except UnicodeDecodeError as e:
        print(f"Стратегия {strategy}: {e}")
```

### Определение кодировки файла

```python
import chardet

def detect_encoding(filename):
    """Определяет кодировку файла"""
    with open(filename, 'rb') as f:
        raw_data = f.read()
    
    result = chardet.detect(raw_data)
    return result['encoding'], result['confidence']

# Использование
encoding, confidence = detect_encoding('unknown_file.txt')
print(f"Кодировка: {encoding}, уверенность: {confidence:.2%}")

# Чтение с определенной кодировкой
with open('unknown_file.txt', 'r', encoding=encoding) as f:
    content = f.read()
```

## 🗂️ Работа с путями

### Модуль os.path (устаревший способ)

```python
import os

# Работа с путями
filename = "/home/user/documents/file.txt"

# Получение компонентов пути
directory = os.path.dirname(filename)   # "/home/user/documents"
basename = os.path.basename(filename)   # "file.txt"
name, ext = os.path.splitext(basename)  # ("file", ".txt")

# Построение путей
path = os.path.join("home", "user", "file.txt")  # "home/user/file.txt"

# Проверка существования
exists = os.path.exists(filename)
is_file = os.path.isfile(filename)
is_dir = os.path.isdir(filename)

# Абсолютный путь
abs_path = os.path.abspath("file.txt")
```

### Модуль pathlib (современный способ)

```python
from pathlib import Path

# Создание объекта пути
path = Path("documents/file.txt")
abs_path = Path("/home/user/documents/file.txt")

# Получение компонентов
print(path.name)         # "file.txt"
print(path.stem)         # "file"
print(path.suffix)       # ".txt"
print(path.suffixes)     # [".txt"]
print(path.parent)       # Path("documents")
print(path.parents)      # Все родительские директории
print(path.anchor)       # Корень пути ("/" или "C:\")

# Построение путей
new_path = path / "subfolder" / "newfile.txt"
config_path = Path.home() / ".config" / "app.conf"

# Проверка существования и типа
if path.exists():
    if path.is_file():
        print("Это файл")
    elif path.is_dir():
        print("Это директория")

# Абсолютный и относительный пути
abs_path = path.absolute()
resolved = path.resolve()  # Разрешает символические ссылки

# Получение информации о файле
stat = path.stat()
size = stat.st_size
mtime = stat.st_mtime
```

### Операции с путями

```python
from pathlib import Path
import shutil
import os

path = Path("documents/file.txt")

# Создание файла
path.touch()                    # Создает пустой файл
path.write_text("content")      # Создает файл с содержимым
path.write_bytes(b"binary")     # Создает бинарный файл

# Чтение файла
content = path.read_text(encoding='utf-8')
binary = path.read_bytes()

# Создание директорий
path.parent.mkdir(parents=True, exist_ok=True)

# Удаление
path.unlink()                   # Удаляет файл
path.rmdir()                    # Удаляет пустую директорию
shutil.rmtree(path)            # Удаляет директорию с содержимым

# Копирование и перемещение
shutil.copy2(src, dst)         # Копирует файл с метаданными
shutil.copytree(src_dir, dst_dir)  # Копирует директорию
shutil.move(src, dst)          # Перемещает файл/директорию

# Переименование
path.rename("new_name.txt")
path.replace("new_name.txt")   # Принудительное переименование
```

## 📂 Работа с директориями

### Листинг директорий

```python
from pathlib import Path
import os
import glob

# Способ 1: os.listdir()
files = os.listdir('.')
for filename in files:
    print(filename)

# Способ 2: pathlib (рекомендуется)
path = Path('.')
for item in path.iterdir():
    if item.is_file():
        print(f"Файл: {item.name}")
    elif item.is_dir():
        print(f"Директория: {item.name}")

# Способ 3: os.walk() для рекурсивного обхода
for root, dirs, files in os.walk('.'):
    for filename in files:
        filepath = os.path.join(root, filename)
        print(filepath)

# Способ 4: pathlib с glob
path = Path('.')
for txt_file in path.glob('*.txt'):
    print(txt_file)

# Рекурсивный поиск
for py_file in path.rglob('*.py'):
    print(py_file)
```

### Фильтрация файлов

```python
from pathlib import Path

def find_files(directory, pattern="*", recursive=True):
    """Находит файлы по паттерну"""
    path = Path(directory)
    
    if recursive:
        return list(path.rglob(pattern))
    else:
        return list(path.glob(pattern))

# Примеры использования
python_files = find_files('.', '*.py')
all_files = find_files('.', '*', recursive=False)
config_files = find_files('.', '*.conf')

# Фильтрация по размеру и времени
large_files = []
for file_path in Path('.').rglob('*'):
    if file_path.is_file():
        size = file_path.stat().st_size
        if size > 1024 * 1024:  # Больше 1 МБ
            large_files.append(file_path)
```

## 🔄 Работа с временными файлами

### Модуль tempfile

```python
import tempfile
import os

# Временный файл (автоматически удаляется)
with tempfile.NamedTemporaryFile(mode='w+t', encoding='utf-8', delete=True) as f:
    f.write("Временные данные")
    f.seek(0)
    content = f.read()
    print(f"Временный файл: {f.name}")

# Временный файл (не удаляется автоматически)
with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as f:
    f.write("Данные")
    temp_filename = f.name

# Нужно удалить вручную
os.unlink(temp_filename)

# Временная директория
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    temp_file = temp_path / "test.txt"
    temp_file.write_text("test")
    print(f"Временная директория: {temp_dir}")
# Директория автоматически удаляется

# Получение системной временной директории
temp_dir = tempfile.gettempdir()
print(f"Системная временная директория: {temp_dir}")

# Создание уникального имени файла
temp_name = tempfile.mktemp(suffix='.txt', prefix='myapp_')
print(f"Уникальное имя: {temp_name}")
```

## 📊 Форматы файлов

### CSV файлы

```python
import csv
from pathlib import Path

# Запись CSV
data = [
    ['Имя', 'Возраст', 'Город'],
    ['Алиса', 25, 'Москва'],
    ['Боб', 30, 'СПб'],
    ['Чарли', 35, 'Казань']
]

# Запись
with open('people.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Чтение
with open('people.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# Работа со словарями
with open('people.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['name', 'age', 'city']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerow({'name': 'Алиса', 'age': 25, 'city': 'Москва'})
    writer.writerow({'name': 'Боб', 'age': 30, 'city': 'СПб'})

# Чтение словарей
with open('people.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']} из {row['city']}, возраст {row['age']}")
```

### JSON файлы

```python
import json
from pathlib import Path

# Данные для записи
data = {
    'name': 'Иван Иванов',
    'age': 30,
    'skills': ['Python', 'JavaScript', 'SQL'],
    'active': True,
    'salary': None
}

# Запись JSON
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Альтернативный способ записи
json_string = json.dumps(data, ensure_ascii=False, indent=2)
Path('data2.json').write_text(json_string, encoding='utf-8')

# Чтение JSON
with open('data.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)
    print(loaded_data)

# Альтернативный способ чтения
json_string = Path('data.json').read_text(encoding='utf-8')
loaded_data = json.loads(json_string)

# Обработка ошибок JSON
try:
    with open('invalid.json', 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Ошибка JSON: {e}")
    print(f"Строка {e.lineno}, позиция {e.colno}")
```

### XML файлы

```python
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Создание XML
root = ET.Element("library")

book1 = ET.SubElement(root, "book", id="1")
ET.SubElement(book1, "title").text = "Python Programming"
ET.SubElement(book1, "author").text = "John Doe"
ET.SubElement(book1, "year").text = "2023"

book2 = ET.SubElement(root, "book", id="2")
ET.SubElement(book2, "title").text = "Web Development"
ET.SubElement(book2, "author").text = "Jane Smith"
ET.SubElement(book2, "year").text = "2022"

# Красивое форматирование
def prettify_xml(element):
    rough_string = ET.tostring(element, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Запись XML
xml_string = prettify_xml(root)
with open('library.xml', 'w', encoding='utf-8') as f:
    f.write(xml_string)

# Чтение XML
tree = ET.parse('library.xml')
root = tree.getroot()

for book in root.findall('book'):
    book_id = book.get('id')
    title = book.find('title').text
    author = book.find('author').text
    year = book.find('year').text
    
    print(f"Книга {book_id}: {title} - {author} ({year})")
```

## 📁 Архивы и сжатие

### ZIP архивы

```python
import zipfile
from pathlib import Path

# Создание ZIP архива
with zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Добавление файлов
    zipf.write('file1.txt')
    zipf.write('file2.txt', 'renamed_file2.txt')  # С переименованием
    
    # Добавление директории рекурсивно
    for file_path in Path('.').rglob('*.py'):
        zipf.write(file_path)

# Чтение ZIP архива
with zipfile.ZipFile('archive.zip', 'r') as zipf:
    # Список файлов
    file_list = zipf.namelist()
    print("Файлы в архиве:", file_list)
    
    # Информация о файлах
    for info in zipf.infolist():
        print(f"{info.filename}: {info.file_size} байт")
    
    # Извлечение всех файлов
    zipf.extractall('extracted/')
    
    # Извлечение конкретного файла
    zipf.extract('file1.txt', 'extracted/')
    
    # Чтение файла без извлечения
    with zipf.open('file1.txt') as f:
        content = f.read().decode('utf-8')
        print(content)
```

### TAR архивы

```python
import tarfile

# Создание TAR архива
with tarfile.open('archive.tar.gz', 'w:gz') as tar:
    tar.add('file1.txt')
    tar.add('directory/', recursive=True)

# Чтение TAR архива
with tarfile.open('archive.tar.gz', 'r:gz') as tar:
    # Список файлов
    members = tar.getmembers()
    for member in members:
        print(f"{member.name}: {member.size} байт")
    
    # Извлечение
    tar.extractall('extracted/')
    
    # Извлечение конкретного файла
    tar.extract('file1.txt', 'extracted/')
```

## 🔍 Мониторинг файловой системы

### Модуль watchdog

```python
# pip install watchdog

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"Файл изменен: {event.src_path}")
    
    def on_created(self, event):
        if not event.is_directory:
            print(f"Файл создан: {event.src_path}")
    
    def on_deleted(self, event):
        if not event.is_directory:
            print(f"Файл удален: {event.src_path}")
    
    def on_moved(self, event):
        if not event.is_directory:
            print(f"Файл перемещен: {event.src_path} -> {event.dest_path}")

# Настройка мониторинга
event_handler = FileChangeHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=True)

# Запуск мониторинга
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

## 🚀 Производительность и оптимизация

### Буферизация

```python
# Размер буфера влияет на производительность
# По умолчанию Python использует оптимальный размер

# Отключение буферизации (медленно)
with open('file.txt', 'w', buffering=0) as f:  # Только для бинарных
    pass

# Линейная буферизация (для терминалов)
with open('file.txt', 'w', buffering=1) as f:
    pass

# Кастомный размер буфера
with open('file.txt', 'w', buffering=8192) as f:  # 8KB буфер
    pass

# Системный буфер по умолчанию (рекомендуется)
with open('file.txt', 'w') as f:  # buffering=-1
    pass
```

### Чтение больших файлов

```python
def process_large_file(filename):
    """Эффективная обработка больших файлов"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Обрабатываем по одной строке
            process_line(line.strip())
            
            if line_num % 10000 == 0:
                print(f"Обработано {line_num} строк")

def read_in_chunks(filename, chunk_size=8192):
    """Чтение файла блоками"""
    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Использование
for chunk in read_in_chunks('large_file.txt'):
    process_chunk(chunk)
```

### Использование mmap для больших файлов

```python
import mmap

def search_in_large_file(filename, search_term):
    """Поиск в большом файле с помощью mmap"""
    with open(filename, 'r', encoding='utf-8') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            # Поиск подстроки
            position = mmapped_file.find(search_term.encode('utf-8'))
            if position != -1:
                # Найдено на позиции position
                return position
    return -1
```

## 🔒 Безопасность работы с файлами

### Безопасные пути

```python
from pathlib import Path
import os

def safe_path_join(base_dir, user_path):
    """Безопасное объединение путей"""
    base = Path(base_dir).resolve()
    target = (base / user_path).resolve()
    
    # Проверяем, что результирующий путь находится в базовой директории
    try:
        target.relative_to(base)
        return target
    except ValueError:
        raise ValueError("Небезопасный путь")

# Использование
try:
    safe_file = safe_path_join('/safe/directory', 'user/file.txt')
    # Безопасно: /safe/directory/user/file.txt
    
    unsafe_file = safe_path_join('/safe/directory', '../../../etc/passwd')
    # Выбросит ValueError
except ValueError as e:
    print(f"Ошибка безопасности: {e}")
```

### Проверка разрешений

```python
import os
import stat

def check_file_permissions(filename):
    """Проверяет разрешения файла"""
    try:
        file_stat = os.stat(filename)
        mode = file_stat.st_mode
        
        permissions = {
            'readable': os.access(filename, os.R_OK),
            'writable': os.access(filename, os.W_OK),
            'executable': os.access(filename, os.X_OK),
            'owner_read': bool(mode & stat.S_IRUSR),
            'owner_write': bool(mode & stat.S_IWUSR),
            'owner_exec': bool(mode & stat.S_IXUSR),
            'group_read': bool(mode & stat.S_IRGRP),
            'group_write': bool(mode & stat.S_IWGRP),
            'group_exec': bool(mode & stat.S_IXGRP),
            'other_read': bool(mode & stat.S_IROTH),
            'other_write': bool(mode & stat.S_IWOTH),
            'other_exec': bool(mode & stat.S_IXOTH),
        }
        
        return permissions
    except OSError:
        return None
```

### Атомарная запись

```python
import tempfile
import os
from pathlib import Path

def atomic_write(filename, content, encoding='utf-8'):
    """Атомарная запись в файл"""
    path = Path(filename)
    
    # Создаем временный файл в той же директории
    with tempfile.NamedTemporaryFile(
        mode='w',
        encoding=encoding,
        dir=path.parent,
        delete=False
    ) as tmp_file:
        tmp_file.write(content)
        tmp_name = tmp_file.name
    
    # Атомарно заменяем оригинальный файл
    os.replace(tmp_name, filename)

# Использование
atomic_write('important.txt', 'Критически важные данные')
```

## 🛠️ Лучшие практики

### 1. Всегда используйте контекстные менеджеры

```python
# ✅ Правильно
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# ❌ Неправильно
f = open('file.txt', 'r')
content = f.read()
f.close()  # Может не выполниться при ошибке
```

### 2. Явно указывайте кодировку

```python
# ✅ Правильно
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# ❌ Может привести к проблемам
with open('file.txt', 'r') as f:  # Кодировка по умолчанию
    content = f.read()
```

### 3. Используйте pathlib вместо os.path

```python
from pathlib import Path

# ✅ Современный способ
path = Path('documents') / 'files' / 'data.txt'
if path.exists():
    content = path.read_text(encoding='utf-8')

# ❌ Устаревший способ
import os
filepath = os.path.join('documents', 'files', 'data.txt')
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
```

### 4. Обрабатывайте исключения

```python
from pathlib import Path

def safe_read_file(filename):
    """Безопасное чтение файла"""
    try:
        path = Path(filename)
        return path.read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except PermissionError:
        print(f"Нет прав для чтения {filename}")
        return None
    except UnicodeDecodeError:
        print(f"Ошибка кодировки в файле {filename}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None
```

### 5. Используйте генераторы для больших файлов

```python
def read_large_file(filename):
    """Генератор для чтения больших файлов"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()

# Использование
for line in read_large_file('huge_file.txt'):
    if 'important' in line:
        process_line(line)
```

### 6. Проверяйте существование и тип

```python
from pathlib import Path

def process_path(path_str):
    """Обработка пути с проверками"""
    path = Path(path_str)
    
    if not path.exists():
        raise FileNotFoundError(f"Путь {path} не существует")
    
    if path.is_file():
        return f"Файл: {path.name}, размер: {path.stat().st_size} байт"
    elif path.is_dir():
        file_count = len(list(path.iterdir()))
        return f"Директория: {path.name}, файлов: {file_count}"
    else:
        return f"Специальный файл: {path}"
```

## 🚀 Заключение

Работа с файлами — это fundamental навык в Python программировании. Ключевые принципы:

### Основные принципы:
1. **Всегда используйте контекстные менеджеры (`with`)**
2. **Явно указывайте кодировку для текстовых файлов**
3. **Используйте pathlib для работы с путями**
4. **Обрабатывайте исключения файловых операций**
5. **Используйте генераторы для больших файлов**
6. **Проверяйте безопасность путей**

### Современные инструменты:
- **pathlib** для работы с путями
- **contextlib** для создания контекстных менеджеров
- **tempfile** для временных файлов
- **watchdog** для мониторинга файловой системы
- **chardet** для определения кодировок

### Форматы данных:
- **CSV** для табличных данных
- **JSON** для структурированных данных
- **XML** для сложных иерархических данных
- **Архивы** для сжатия и группировки файлов

Правильная работа с файлами обеспечивает надежность, производительность и безопасность ваших Python приложений! 