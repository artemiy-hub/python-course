# Основы аннотаций типов в Python
from typing import List, Dict, Optional, Union, Tuple, Callable

# Простые типы
def greet(name: str) -> str:
    """Функция с аннотациями типов"""
    return f"Привет, {name}!"

def add_numbers(a: int, b: int) -> int:
    """Сложение двух чисел"""
    return a + b

def calculate_average(numbers: List[float]) -> float:
    """Вычисление среднего значения"""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

# Переменные с аннотациями
age: int = 25
name: str = "Анна"
scores: List[int] = [95, 87, 92, 88]
person_info: Dict[str, Union[str, int]] = {
    "name": "Иван", 
    "age": 30,
    "city": "Москва"
}

# Optional и Union
def find_user(user_id: int) -> Optional[str]:
    """Поиск пользователя по ID"""
    users = {1: "Анна", 2: "Иван", 3: "Мария"}
    return users.get(user_id)

def process_data(data: Union[str, int, float]) -> str:
    """Обработка данных разных типов"""
    if isinstance(data, str):
        return data.upper()
    else:
        return str(data)

# Кортежи с типизацией
def get_coordinates() -> Tuple[float, float]:
    """Получение координат"""
    return 55.7558, 37.6176

def get_name_age() -> Tuple[str, int]:
    """Получение имени и возраста"""
    return "Петр", 28

# Функции как типы
def apply_operation(x: int, y: int, operation: Callable[[int, int], int]) -> int:
    """Применение операции к двум числам"""
    return operation(x, y)

def multiply(a: int, b: int) -> int:
    return a * b

# Списки и словари
def process_names(names: List[str]) -> List[str]:
    """Обработка списка имён"""
    return [name.title() for name in names]

def count_words(text: str) -> Dict[str, int]:
    """Подсчёт слов в тексте"""
    words = text.lower().split()
    word_count: Dict[str, int] = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

# Классы с аннотациями
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age
    
    def get_info(self) -> str:
        return f"{self.name}, {self.age} лет"
    
    def is_adult(self) -> bool:
        return self.age >= 18

class Calculator:
    def __init__(self) -> None:
        self.history: List[str] = []
    
    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_history(self) -> List[str]:
        return self.history.copy()

# Демонстрация использования
if __name__ == "__main__":
    # Основные функции
    print(greet("Мир"))
    print(add_numbers(5, 3))
    print(calculate_average([1.5, 2.5, 3.5]))
    
    # Optional
    user = find_user(1)
    if user:
        print(f"Найден пользователь: {user}")
    
    # Union
    print(process_data("hello"))
    print(process_data(42))
    print(process_data(3.14))
    
    # Кортежи
    lat, lon = get_coordinates()
    print(f"Координаты: {lat}, {lon}")
    
    # Функции высшего порядка
    result = apply_operation(4, 5, multiply)
    print(f"Результат: {result}")
    
    # Работа с коллекциями
    names = ["анна", "иван", "мария"]
    processed_names = process_names(names)
    print(f"Обработанные имена: {processed_names}")
    
    word_counts = count_words("hello world hello python world")
    print(f"Подсчёт слов: {word_counts}")
    
    # Классы
    person = Person("Алексей", 25)
    print(person.get_info())
    print(f"Совершеннолетний: {person.is_adult()}")
    
    calc = Calculator()
    calc.add(10, 5)
    calc.add(3.14, 2.86)
    print("История вычислений:")
    for entry in calc.get_history():
        print(f"  {entry}")
    
    # Проверка типов во время выполнения
    print(f"\nТипы переменных:")
    print(f"age: {type(age)}")
    print(f"name: {type(name)}")
    print(f"scores: {type(scores)}")
    print(f"person_info: {type(person_info)}")
    
    # Аннотации не влияют на выполнение
    # Это будет работать, несмотря на неправильные типы
    wrong_result = add_numbers("5", "3")  # type: ignore
    print(f"Неправильные типы всё равно работают: {wrong_result}") 