# Walrus Operator (:=) в Python 3.8+
import re
import math

print("=== Основы Walrus Operator ===")

# Обычный способ
numbers = [1, 2, 3, 4, 5]
length = len(numbers)
if length > 3:
    print(f"Список длинный: {length} элементов")

# С walrus operator
if (length := len(numbers)) > 3:
    print(f"Список длинный: {length} элементов")

print("\n=== Обработка списков ===")

# Фильтрация с сохранением результата
data = [1, 4, 9, 16, 25, 36]

# Старый способ
squares = []
for x in data:
    sqrt_x = math.sqrt(x)
    if sqrt_x > 3:
        squares.append(sqrt_x)
print(f"Старый способ: {squares}")

# С walrus operator
squares_new = [sqrt_x for x in data if (sqrt_x := math.sqrt(x)) > 3]
print(f"С walrus: {squares_new}")

print("\n=== Работа с циклами while ===")

# Чтение файла построчно (имитация)
lines = ["line 1", "line 2", "", "line 4", ""]

# Обычный способ
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line:
        print(f"Обработка: {line}")
    i += 1

print("---")

# С walrus operator (имитация readline)
def get_next_line():
    """Имитация чтения следующей строки"""
    if not hasattr(get_next_line, 'index'):
        get_next_line.index = 0
    
    if get_next_line.index < len(lines):
        line = lines[get_next_line.index]
        get_next_line.index += 1
        return line
    return ""

# Сброс счётчика
get_next_line.index = 0

while (line := get_next_line().strip()):
    print(f"Обработка с walrus: {line}")

print("\n=== Регулярные выражения ===")

text = "Телефон: +7-123-456-78-90, Email: user@example.com"
phone_pattern = r'\+7-\d{3}-\d{3}-\d{2}-\d{2}'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Обычный способ
phone_match = re.search(phone_pattern, text)
if phone_match:
    print(f"Найден телефон: {phone_match.group()}")

email_match = re.search(email_pattern, text)
if email_match:
    print(f"Найден email: {email_match.group()}")

# С walrus operator
if (phone_match := re.search(phone_pattern, text)):
    print(f"Найден телефон (walrus): {phone_match.group()}")

if (email_match := re.search(email_pattern, text)):
    print(f"Найден email (walrus): {email_match.group()}")

print("\n=== Словари и вычисления ===")

# Подсчёт частоты слов
text = "python is great python is powerful python is fun"
words = text.split()

# Обычный способ
word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1
print(f"Обычный подсчёт: {word_count}")

# С walrus operator и get
word_count_walrus = {}
for word in words:
    word_count_walrus[word] = (current := word_count_walrus.get(word, 0)) + 1
print(f"С walrus: {word_count_walrus}")

print("\n=== Проверка условий ===")

# Проверка результата функции
def expensive_computation(x):
    """Имитация дорогой операции"""
    print(f"Вычисляю для {x}...")
    return x ** 2 + 2 * x + 1

values = [1, 2, 3, 4, 5]

# Обычный способ (двойной вызов функции)
results = []
for x in values:
    if expensive_computation(x) > 10:
        results.append(expensive_computation(x))  # Двойной вызов!

print("---")

# С walrus operator (один вызов)
results_walrus = []
for x in values:
    if (result := expensive_computation(x)) > 10:
        results_walrus.append(result)  # Используем сохранённый результат

print(f"Результаты: {results_walrus}")

print("\n=== Обработка исключений ===")

def divide_numbers(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

# С walrus operator в условии
pairs = [(10, 2), (15, 3), (20, 0), (25, 5)]

for a, b in pairs:
    if (result := divide_numbers(a, b)) is not None:
        print(f"{a} / {b} = {result}")
    else:
        print(f"{a} / {b} = деление на ноль!")

print("\n=== Списочные включения ===")

# Фильтрация с преобразованием
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Обычный способ (неэффективно)
squares_gt_25 = [x**2 for x in numbers if x**2 > 25]

# С walrus operator (эффективно)
squares_gt_25_walrus = [square for x in numbers if (square := x**2) > 25]

print(f"Квадраты > 25: {squares_gt_25_walrus}")

print("\n=== Практический пример: парсинг данных ===")

# Парсинг логов
log_entries = [
    "2023-01-01 10:00:00 INFO User login",
    "2023-01-01 10:05:00 ERROR Database connection failed",
    "2023-01-01 10:10:00 WARNING High memory usage",
    "2023-01-01 10:15:00 INFO User logout"
]

error_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ERROR (.+)'

# С walrus operator
errors = []
for entry in log_entries:
    if (match := re.match(error_pattern, entry)):
        timestamp, error_msg = match.groups()
        errors.append({
            'timestamp': timestamp,
            'message': error_msg
        })

print("Найденные ошибки:")
for error in errors:
    print(f"  {error['timestamp']}: {error['message']}")

# Важное примечание
print("\n=== Важные замечания ===")
print("1. Walrus operator нельзя использовать в lambda")
print("2. Скобки обязательны в большинстве случаев")
print("3. Читаемость кода должна быть приоритетом")
print("4. Не злоупотребляйте - используйте там, где это улучшает код") 