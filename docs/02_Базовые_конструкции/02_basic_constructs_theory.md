# Теория: Базовые конструкции Python

## 🎯 Цели раздела

После изучения этого раздела вы будете:
- Понимать все основные типы данных Python
- Уметь работать с переменными и операторами
- Знать условные конструкции и циклы
- Понимать область видимости переменных
- Уметь обрабатывать пользовательский ввод

## 📊 Переменные и присваивание

### Что такое переменная?

Переменная в Python — это имя, которое ссылается на объект в памяти. Python использует **динамическую типизацию**, что означает, что тип переменной определяется автоматически во время выполнения.

```python
# Python автоматически определяет тип
name = "Alice"      # str
age = 25           # int
height = 175.5     # float
is_student = True  # bool
```

### Правила именования переменных

| ✅ Правильно | ❌ Неправильно | Причина |
|-------------|---------------|---------|
| `user_name` | `userName` | Python предпочитает snake_case |
| `total_sum` | `2total` | Нельзя начинать с цифры |
| `is_active` | `is-active` | Дефисы запрещены |
| `MAX_SIZE` | `max size` | Пробелы запрещены |
| `_private` | `class` | `class` — зарезервированное слово |

### Множественное присваивание

```python
# Одновременное присваивание
x, y, z = 1, 2, 3

# Обмен значениями
a, b = 10, 20
a, b = b, a  # Теперь a=20, b=10

# Распаковка
coordinates = (5, 10)
x, y = coordinates
```

## 🔢 Типы данных в деталях

### Числовые типы

#### 1. Целые числа (int)

```python
# Различные способы записи
decimal = 42
binary = 0b101010      # Двоичная система (42)
octal = 0o52          # Восьмеричная система (42)
hexadecimal = 0x2A    # Шестнадцатеричная система (42)

# Большие числа
big_number = 123_456_789  # Подчёркивания для читаемости
very_big = 10**100       # Python поддерживает числа любого размера
```

#### 2. Числа с плавающей точкой (float)

```python
# Обычная запись
price = 19.99

# Научная нотация
speed_of_light = 3.0e8  # 300,000,000
planck_constant = 6.626e-34

# Специальные значения
infinity = float('inf')
negative_infinity = float('-inf')
not_a_number = float('nan')
```

#### 3. Комплексные числа (complex)

```python
# Создание комплексных чисел
z1 = 3 + 4j
z2 = complex(3, 4)

# Операции с комплексными числами
real_part = z1.real      # 3.0
imaginary_part = z1.imag # 4.0
absolute_value = abs(z1)  # 5.0
```

### Строки (str)

#### Способы создания строк

```python
# Одинарные кавычки
single_quotes = 'Hello, World!'

# Двойные кавычки
double_quotes = "Hello, World!"

# Тройные кавычки (многострочные)
multiline = """
Это многострочная
строка
"""

# Raw строки (без обработки escape-последовательностей)
raw_string = r"C:\Users\Name\Documents"

# Строки Unicode
unicode_string = "Привет, мир! 🐍"
```

#### Escape-последовательности

| Последовательность | Значение |
|-------------------|----------|
| `\n` | Новая строка |
| `\t` | Табуляция |
| `\\` | Обратная косая черта |
| `\"` | Двойная кавычка |
| `\'` | Одинарная кавычка |
| `\r` | Возврат каретки |
| `\0` | Нулевой символ |

```python
print("Первая строка\nВторая строка")
print("Колонка1\tКолонка2")
print("Путь: C:\\Users\\Name")
print("Он сказал: \"Привет!\"")
```

#### Методы строк

```python
text = "Python Programming"

# Регистр
text.upper()        # "PYTHON PROGRAMMING"
text.lower()        # "python programming"
text.title()        # "Python Programming"
text.capitalize()   # "Python programming"
text.swapcase()     # "pYTHON pROGRAMMING"

# Поиск и замена
text.find("gram")         # 10 (индекс первого вхождения)
text.replace("Python", "Java")  # "Java Programming"
text.count("m")          # 2 (количество вхождений)

# Проверки
text.startswith("Py")    # True
text.endswith("ing")     # True
text.isalpha()          # False (есть пробел)
text.isdigit()          # False
text.isalnum()          # False

# Разделение и объединение
words = text.split()     # ["Python", "Programming"]
"-".join(words)         # "Python-Programming"

# Очистка
"  Python  ".strip()    # "Python"
"...Python...".strip(".")  # "Python"
```

### Логические значения (bool)

```python
# Создание булевых значений
is_active = True
is_disabled = False

# Преобразование в bool
bool(1)        # True
bool(0)        # False
bool("")       # False (пустая строка)
bool("text")   # True (непустая строка)
bool([])       # False (пустой список)
bool([1, 2])   # True (непустой список)
bool(None)     # False
```

#### Таблица истинности для логических операторов

| A | B | A and B | A or B | not A |
|---|---|---------|--------|-------|
| True | True | True | True | False |
| True | False | False | True | False |
| False | True | False | True | True |
| False | False | False | False | True |

## 🔧 Операторы

### Арифметические операторы

```python
a = 10
b = 3

print(a + b)   # 13 (сложение)
print(a - b)   # 7  (вычитание)
print(a * b)   # 30 (умножение)
print(a / b)   # 3.333... (деление)
print(a // b)  # 3  (целочисленное деление)
print(a % b)   # 1  (остаток от деления)
print(a ** b)  # 1000 (возведение в степень)
```

### Операторы сравнения

```python
x = 5
y = 10

print(x == y)  # False (равно)
print(x != y)  # True  (не равно)
print(x < y)   # True  (меньше)
print(x <= y)  # True  (меньше или равно)
print(x > y)   # False (больше)
print(x >= y)  # False (больше или равно)

# Цепочки сравнений
print(1 < x < 10)  # True (эквивалентно: 1 < x and x < 10)
```

### Логические операторы

```python
# and - И (все условия должны быть True)
age = 25
has_license = True
can_drive = age >= 18 and has_license  # True

# or - ИЛИ (хотя бы одно условие должно быть True)
is_weekend = True
is_holiday = False
can_rest = is_weekend or is_holiday    # True

# not - НЕ (инвертирует значение)
is_working = not can_rest              # False
```

### Операторы присваивания

```python
x = 10

x += 5   # x = x + 5  → 15
x -= 3   # x = x - 3  → 12
x *= 2   # x = x * 2  → 24
x /= 4   # x = x / 4  → 6.0
x //= 2  # x = x // 2 → 3.0
x %= 2   # x = x % 2  → 1.0
x **= 3  # x = x ** 3 → 1.0
```

### Операторы принадлежности

```python
text = "Python Programming"

# in - проверка принадлежности
print("Python" in text)     # True
print("Java" in text)       # False

# not in - проверка отсутствия
print("Java" not in text)   # True

# Работает с любыми последовательностями
numbers = [1, 2, 3, 4, 5]
print(3 in numbers)         # True
print(6 not in numbers)     # True
```

### Операторы тождественности

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  (одинаковое содержимое)
print(a is b)   # False (разные объекты в памяти)
print(a is c)   # True  (один и тот же объект)

# Особые случаи
x = None
print(x is None)     # True (правильный способ проверки None)
print(x == None)     # True (работает, но не рекомендуется)
```

## 🎯 Условные конструкции

### Базовый синтаксис if

```python
age = 18

if age >= 18:
    print("Вы совершеннолетний")
    print("Можете голосовать")
```

### Полная конструкция if-elif-else

```python
score = 85

if score >= 90:
    grade = "A"
    print("Отлично!")
elif score >= 80:
    grade = "B"
    print("Хорошо!")
elif score >= 70:
    grade = "C"
    print("Удовлетворительно")
elif score >= 60:
    grade = "D"
    print("Плохо")
else:
    grade = "F"
    print("Провал")

print(f"Ваша оценка: {grade}")
```

### Тернарный оператор

```python
age = 20

# Полная запись
if age >= 18:
    status = "взрослый"
else:
    status = "ребёнок"

# Тернарный оператор (краткая запись)
status = "взрослый" if age >= 18 else "ребёнок"

# Более сложный пример
max_value = a if a > b else b
```

### Вложенные условия

```python
weather = "sunny"
temperature = 25

if weather == "sunny":
    if temperature > 20:
        print("Отличная погода для прогулки!")
    else:
        print("Солнечно, но прохладно")
else:
    if temperature > 20:
        print("Тепло, но не солнечно")
    else:
        print("Плохая погода")
```

### Множественные условия

```python
username = "admin"
password = "secret123"
is_active = True

# Сложное условие
if username == "admin" and password == "secret123" and is_active:
    print("Доступ разрешён")
elif username == "admin" and password == "secret123":
    print("Аккаунт заблокирован")
elif username == "admin":
    print("Неверный пароль")
else:
    print("Пользователь не найден")
```

## 🔄 Циклы

### Цикл for

#### Итерация по последовательностям

```python
# Цикл по строке
for char in "Python":
    print(char)  # P, y, t, h, o, n

# Цикл по списку
fruits = ["яблоко", "банан", "апельсин"]
for fruit in fruits:
    print(f"Фрукт: {fruit}")

# Цикл с индексами
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

#### Функция range()

```python
# range(stop)
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop)
for i in range(2, 8):
    print(i)  # 2, 3, 4, 5, 6, 7

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Обратный порядок
for i in range(10, 0, -1):
    print(i)  # 10, 9, 8, ..., 1
```

#### Вложенные циклы

```python
# Таблица умножения
for i in range(1, 4):
    for j in range(1, 4):
        product = i * j
        print(f"{i} x {j} = {product}")
    print("---")
```

### Цикл while

```python
# Базовый while
count = 0
while count < 5:
    print(f"Счётчик: {count}")
    count += 1

# While с условием
password = ""
while password != "secret":
    password = input("Введите пароль: ")
    if password != "secret":
        print("Неверный пароль!")

print("Доступ разрешён!")
```

#### Бесконечные циклы

```python
# Бесконечный цикл (осторожно!)
while True:
    user_input = input("Введите команду (exit для выхода): ")
    if user_input == "exit":
        break
    print(f"Вы ввели: {user_input}")
```

### Управление циклами

#### break - прерывание цикла

```python
# Поиск числа в списке
numbers = [1, 3, 7, 9, 12, 15]
target = 9

for num in numbers:
    if num == target:
        print(f"Число {target} найдено!")
        break
    print(f"Проверяем {num}")
else:
    print(f"Число {target} не найдено")
```

#### continue - пропуск итерации

```python
# Печать только нечётных чисел
for i in range(10):
    if i % 2 == 0:  # Если число чётное
        continue    # Пропускаем остальную часть итерации
    print(f"Нечётное число: {i}")
```

#### Блок else в циклах

```python
# else выполняется, если цикл завершился нормально (без break)
for i in range(5):
    print(i)
else:
    print("Цикл завершён нормально")

# else не выполняется при break
for i in range(5):
    if i == 3:
        break
    print(i)
else:
    print("Этот блок не выполнится")
```

## 📥 Ввод и вывод данных

### Функция input()

```python
# Базовый ввод (всегда возвращает строку)
name = input("Введите ваше имя: ")
print(f"Привет, {name}!")

# Ввод чисел (требует преобразования)
age_str = input("Введите ваш возраст: ")
age = int(age_str)

# Краткая запись
age = int(input("Введите ваш возраст: "))

# Ввод с обработкой ошибок
try:
    number = float(input("Введите число: "))
    print(f"Вы ввели: {number}")
except ValueError:
    print("Ошибка: введено не число!")
```

### Функция print()

```python
# Базовый вывод
print("Hello, World!")

# Множественные аргументы
print("Значения:", 10, 20, 30)

# Параметр sep (разделитель)
print("A", "B", "C", sep="-")  # A-B-C

# Параметр end (окончание)
print("Первая строка", end=" ")
print("Вторая строка")  # Первая строка Вторая строка

# Вывод в файл
with open("output.txt", "w") as file:
    print("Текст в файл", file=file)
```

### Форматирование вывода

```python
name = "Alice"
age = 25
salary = 50000.75

# f-строки (рекомендуемый способ)
print(f"Имя: {name}, Возраст: {age}, Зарплата: {salary:.2f}")

# Метод format()
print("Имя: {}, Возраст: {}, Зарплата: {:.2f}".format(name, age, salary))

# % форматирование (устаревший)
print("Имя: %s, Возраст: %d, Зарплата: %.2f" % (name, age, salary))
```

## 🎯 Область видимости переменных

### Локальные и глобальные переменные

```python
# Глобальная переменная
global_var = "Я глобальная"

def my_function():
    # Локальная переменная
    local_var = "Я локальная"
    print(global_var)  # Доступ к глобальной переменной
    print(local_var)   # Доступ к локальной переменной

my_function()
print(global_var)   # Работает
# print(local_var)  # Ошибка! Переменная не существует в глобальной области
```

### Ключевое слово global

```python
counter = 0  # Глобальная переменная

def increment():
    global counter  # Объявляем, что будем изменять глобальную переменную
    counter += 1

def increment_local():
    counter = 1  # Создаём новую локальную переменную
    counter += 1
    print(f"Локальный counter: {counter}")

print(f"Начальное значение: {counter}")
increment()
print(f"После increment(): {counter}")
increment_local()
print(f"После increment_local(): {counter}")
```

### Правило LEGB

Python ищет переменные в следующем порядке:
1. **L**ocal - локальная область
2. **E**nclosing - объемлющая область
3. **G**lobal - глобальная область  
4. **B**uilt-in - встроенная область

```python
x = "глобальная"

def outer():
    x = "объемлющая"
    
    def inner():
        x = "локальная"
        print(f"В inner(): {x}")
    
    inner()
    print(f"В outer(): {x}")

outer()
print(f"В глобальной области: {x}")
```

## 🎨 Лучшие практики

### 1. Именование переменных

```python
# ✅ Хорошо
user_name = "John"
total_price = 199.99
is_valid = True
MAX_RETRIES = 3

# ❌ Плохо
n = "John"
tp = 199.99
flag = True
max_retries = 3  # константы должны быть ЗАГЛАВНЫМИ
```

### 2. Структура кода

```python
# ✅ Хорошо структурированный код
def calculate_total_price(items, discount=0):
    """Вычисляет общую стоимость товаров с учётом скидки."""
    subtotal = sum(item.price for item in items)
    discount_amount = subtotal * discount / 100
    total = subtotal - discount_amount
    return total

# ❌ Плохо структурированный код
def calc(items, d=0):
    s = 0
    for i in items:
        s += i.price
    return s - s * d / 100
```

### 3. Обработка ошибок

```python
# ✅ Хорошо
try:
    age = int(input("Введите возраст: "))
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")
except ValueError as e:
    print(f"Ошибка ввода: {e}")

# ❌ Плохо
age = int(input("Введите возраст: "))  # Может вызвать ошибку
```

### 4. Использование констант

```python
# ✅ Хорошо
SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24

def seconds_to_days(seconds):
    return seconds / (SECONDS_IN_MINUTE * MINUTES_IN_HOUR * HOURS_IN_DAY)

# ❌ Плохо
def seconds_to_days(seconds):
    return seconds / 86400  # Магическое число
```

## 📝 Итоги

Базовые конструкции Python включают:

1. **Переменные** - контейнеры для данных
2. **Типы данных** - int, float, str, bool
3. **Операторы** - арифметические, логические, сравнения
4. **Условия** - if, elif, else
5. **Циклы** - for, while
6. **Ввод/вывод** - input(), print()
7. **Область видимости** - local, global

Эти конструкции — фундамент для создания любых программ на Python. Освоив их, вы сможете решать широкий круг задач и переходить к изучению более сложных тем.

---

**Следующий шаг:** Изучение структур данных (списки, кортежи, словари, множества) 