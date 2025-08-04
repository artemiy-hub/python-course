# Structural Pattern Matching (match/case) в Python 3.10+
import sys

# Проверяем версию Python
if sys.version_info < (3, 10):
    print("Этот код требует Python 3.10 или новее")
    print(f"Текущая версия: {sys.version}")
    exit()

print("=== Основы match/case ===")

def handle_value(value):
    match value:
        case 0:
            return "Ноль"
        case 1:
            return "Один"
        case 2:
            return "Два"
        case _:  # default case
            return f"Другое число: {value}"

# Тестирование
for num in [0, 1, 2, 5]:
    print(f"{num} -> {handle_value(num)}")

print("\n=== Сопоставление с типами ===")

def process_data(data):
    match data:
        case int() if data > 0:
            return f"Положительное число: {data}"
        case int() if data < 0:
            return f"Отрицательное число: {data}"
        case int():
            return "Ноль"
        case str() if len(data) > 10:
            return f"Длинная строка: {data[:10]}..."
        case str():
            return f"Строка: {data}"
        case list() if len(data) == 0:
            return "Пустой список"
        case list():
            return f"Список из {len(data)} элементов"
        case dict():
            return f"Словарь с ключами: {list(data.keys())}"
        case _:
            return f"Неизвестный тип: {type(data)}"

# Тестирование
test_data = [42, -10, 0, "hello", "это очень длинная строка", [], [1, 2, 3], {"a": 1, "b": 2}]
for item in test_data:
    print(f"{item} -> {process_data(item)}")

print("\n=== Распаковка последовательностей ===")

def analyze_list(items):
    match items:
        case []:
            return "Пустой список"
        case [x]:
            return f"Один элемент: {x}"
        case [x, y]:
            return f"Два элемента: {x}, {y}"
        case [x, y, z]:
            return f"Три элемента: {x}, {y}, {z}"
        case [first, *middle, last]:
            return f"Первый: {first}, последний: {last}, средних: {len(middle)}"

# Тестирование
test_lists = [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4, 5]]
for lst in test_lists:
    print(f"{lst} -> {analyze_list(lst)}")

print("\n=== Сопоставление словарей ===")

def handle_request(request):
    match request:
        case {"action": "get", "resource": resource}:
            return f"Получение ресурса: {resource}"
        case {"action": "post", "resource": resource, "data": data}:
            return f"Создание {resource} с данными: {data}"
        case {"action": "put", "resource": resource, "id": obj_id, "data": data}:
            return f"Обновление {resource} #{obj_id}: {data}"
        case {"action": "delete", "resource": resource, "id": obj_id}:
            return f"Удаление {resource} #{obj_id}"
        case {"action": action}:
            return f"Неизвестное действие: {action}"
        case _:
            return "Неверный формат запроса"

# Тестирование
requests = [
    {"action": "get", "resource": "users"},
    {"action": "post", "resource": "posts", "data": {"title": "Новый пост"}},
    {"action": "put", "resource": "users", "id": 123, "data": {"name": "Иван"}},
    {"action": "delete", "resource": "posts", "id": 456},
    {"action": "unknown"},
    {"invalid": "request"}
]

for req in requests:
    print(f"{req} -> {handle_request(req)}")

print("\n=== Работа с классами ===")

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def __repr__(self):
        return f"Circle({self.center}, {self.radius})"

def describe_shape(shape):
    match shape:
        case Point(x=0, y=0):
            return "Точка в начале координат"
        case Point(x=0, y=y):
            return f"Точка на оси Y: {y}"
        case Point(x=x, y=0):
            return f"Точка на оси X: {x}"
        case Point(x=x, y=y) if x == y:
            return f"Точка на диагонали: ({x}, {y})"
        case Point(x=x, y=y):
            return f"Точка: ({x}, {y})"
        case Circle(center=Point(x=0, y=0), radius=r):
            return f"Круг в центре с радиусом {r}"
        case Circle(center=center, radius=r):
            return f"Круг с центром {center} и радиусом {r}"
        case _:
            return "Неизвестная фигура"

# Тестирование
shapes = [
    Point(0, 0),
    Point(0, 5),
    Point(3, 0),
    Point(2, 2),
    Point(1, 3),
    Circle(Point(0, 0), 5),
    Circle(Point(1, 2), 3)
]

for shape in shapes:
    print(f"{shape} -> {describe_shape(shape)}")

print("\n=== HTTP статус-коды ===")

def handle_http_response(status_code):
    match status_code:
        case 200:
            return "OK - Успешный запрос"
        case 201:
            return "Created - Ресурс создан"
        case 400:
            return "Bad Request - Неверный запрос"
        case 401:
            return "Unauthorized - Не авторизован"
        case 403:
            return "Forbidden - Доступ запрещён"
        case 404:
            return "Not Found - Ресурс не найден"
        case 500:
            return "Internal Server Error - Ошибка сервера"
        case code if 200 <= code < 300:
            return f"Успешный запрос: {code}"
        case code if 300 <= code < 400:
            return f"Перенаправление: {code}"
        case code if 400 <= code < 500:
            return f"Ошибка клиента: {code}"
        case code if 500 <= code < 600:
            return f"Ошибка сервера: {code}"
        case _:
            return f"Неизвестный код: {status_code}"

# Тестирование
status_codes = [200, 201, 404, 500, 302, 418, 600]
for code in status_codes:
    print(f"{code} -> {handle_http_response(code)}")

print("\n=== Парсер выражений ===")

# Простой парсер арифметических выражений
class Expr:
    pass

class Number(Expr):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinOp({self.left}, '{self.op}', {self.right})"

def evaluate(expr):
    match expr:
        case Number(value):
            return value
        case BinOp(left, '+', right):
            return evaluate(left) + evaluate(right)
        case BinOp(left, '-', right):
            return evaluate(left) - evaluate(right)
        case BinOp(left, '*', right):
            return evaluate(left) * evaluate(right)
        case BinOp(left, '/', right):
            right_val = evaluate(right)
            if right_val == 0:
                raise ValueError("Деление на ноль")
            return evaluate(left) / right_val
        case _:
            raise ValueError(f"Неизвестное выражение: {expr}")

# Тестирование парсера
expressions = [
    Number(42),
    BinOp(Number(10), '+', Number(5)),
    BinOp(Number(20), '-', Number(8)),
    BinOp(Number(6), '*', Number(7)),
    BinOp(Number(15), '/', Number(3)),
    BinOp(BinOp(Number(2), '+', Number(3)), '*', Number(4))  # (2 + 3) * 4
]

for expr in expressions:
    try:
        result = evaluate(expr)
        print(f"{expr} = {result}")
    except ValueError as e:
        print(f"{expr} -> Ошибка: {e}")

print("\n=== Сравнение с if/elif ===")

# Старый способ с if/elif
def old_way_handler(data):
    if isinstance(data, int) and data > 0:
        return f"Positive: {data}"
    elif isinstance(data, int) and data < 0:
        return f"Negative: {data}"
    elif isinstance(data, int):
        return "Zero"
    elif isinstance(data, str):
        return f"String: {data}"
    elif isinstance(data, list) and len(data) == 0:
        return "Empty list"
    elif isinstance(data, list):
        return f"List with {len(data)} items"
    else:
        return "Unknown"

# Новый способ с match/case более читаемый и мощный
def new_way_handler(data):
    match data:
        case int() if data > 0:
            return f"Positive: {data}"
        case int() if data < 0:
            return f"Negative: {data}"
        case int():
            return "Zero"
        case str():
            return f"String: {data}"
        case []:
            return "Empty list"
        case list():
            return f"List with {len(data)} items"
        case _:
            return "Unknown"

print("Match/case обеспечивает:")
print("- Более читаемый код")
print("- Мощные возможности сопоставления")
print("- Распаковку структур данных")
print("- Проверку типов и условий")
print("- Работу с пользовательскими классами") 