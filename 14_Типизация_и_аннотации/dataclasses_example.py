# Dataclasses в Python
from dataclasses import dataclass, field, asdict, astuple
from typing import List, Optional, ClassVar
import json

# Простой dataclass
@dataclass
class Point:
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

# Dataclass с значениями по умолчанию
@dataclass
class Person:
    name: str
    age: int
    email: str = ""
    is_active: bool = True
    
    def __post_init__(self):
        """Вызывается после __init__"""
        if not self.email:
            self.email = f"{self.name.lower().replace(' ', '.')}@example.com"

# Dataclass с field()
@dataclass
class Student:
    name: str
    student_id: int
    courses: List[str] = field(default_factory=list)
    grades: dict = field(default_factory=dict)
    _private_notes: str = field(default="", repr=False)  # Не показывается в repr
    
    def add_course(self, course: str, grade: Optional[float] = None):
        if course not in self.courses:
            self.courses.append(course)
        if grade is not None:
            self.grades[course] = grade
    
    def get_average_grade(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

# Неизменяемый dataclass (frozen)
@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int
    
    def __post_init__(self):
        """Проверка значений"""
        for value in [self.red, self.green, self.blue]:
            if not 0 <= value <= 255:
                raise ValueError("RGB значения должны быть от 0 до 255")
    
    def to_hex(self) -> str:
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"

# Dataclass с классовыми переменными
@dataclass
class BankAccount:
    account_number: str
    balance: float = 0.0
    
    # Классовая переменная (не является полем экземпляра)
    bank_name: ClassVar[str] = "Python Bank"
    interest_rate: ClassVar[float] = 0.02
    
    def deposit(self, amount: float):
        if amount > 0:
            self.balance += amount
    
    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False
    
    def apply_interest(self):
        self.balance *= (1 + self.interest_rate)

# Dataclass с сортировкой
@dataclass(order=True)
class Task:
    priority: int
    name: str = field(compare=False)  # Не участвует в сравнении
    description: str = field(default="", compare=False)
    completed: bool = field(default=False, compare=False)

# Наследование dataclasses
@dataclass
class Vehicle:
    make: str
    model: str
    year: int

@dataclass
class Car(Vehicle):
    doors: int = 4
    fuel_type: str = "petrol"
    
    def __post_init__(self):
        if self.doors not in [2, 4, 5]:
            raise ValueError("Количество дверей должно быть 2, 4 или 5")

# Сравнение с обычным классом
class RegularPerson:
    def __init__(self, name: str, age: int, email: str = ""):
        self.name = name
        self.age = age
        self.email = email or f"{name.lower().replace(' ', '.')}@example.com"
    
    def __repr__(self):
        return f"RegularPerson(name='{self.name}', age={self.age}, email='{self.email}')"
    
    def __eq__(self, other):
        if not isinstance(other, RegularPerson):
            return False
        return (self.name, self.age, self.email) == (other.name, other.age, other.email)

# Демонстрация использования
if __name__ == "__main__":
    print("=== Простой dataclass ===")
    p1 = Point(3.0, 4.0)
    p2 = Point(0.0, 0.0)
    print(f"Точка: {p1}")
    print(f"Расстояние от начала координат: {p1.distance_from_origin()}")
    print(f"Равны ли точки: {p1 == p2}")
    
    print("\n=== Person с post_init ===")
    person1 = Person("Анна Иванова", 25)
    person2 = Person("Иван Петров", 30, "ivan@company.com")
    print(f"Человек 1: {person1}")
    print(f"Человек 2: {person2}")
    
    print("\n=== Student с field() ===")
    student = Student("Мария Сидорова", 12345)
    student.add_course("Математика", 4.5)
    student.add_course("Физика", 4.0)
    student.add_course("Программирование")
    print(f"Студент: {student}")
    print(f"Средний балл: {student.get_average_grade()}")
    
    print("\n=== Frozen dataclass ===")
    red = Color(255, 0, 0)
    print(f"Красный цвет: {red}")
    print(f"Hex: {red.to_hex()}")
    
    # Попытка изменить frozen объект вызовет ошибку
    try:
        red.red = 200  # type: ignore
    except Exception as e:
        print(f"Ошибка изменения frozen объекта: {type(e).__name__}")
    
    print("\n=== Bank Account ===")
    account = BankAccount("12345678", 1000.0)
    print(f"Счёт: {account}")
    print(f"Банк: {BankAccount.bank_name}")
    account.deposit(500)
    account.apply_interest()
    print(f"После пополнения и начисления процентов: {account}")
    
    print("\n=== Сортировка Task ===")
    tasks = [
        Task(3, "Низкий приоритет"),
        Task(1, "Высокий приоритет"),
        Task(2, "Средний приоритет"),
    ]
    print("Исходные задачи:")
    for task in tasks:
        print(f"  {task}")
    
    tasks.sort()
    print("Отсортированные задачи:")
    for task in tasks:
        print(f"  {task}")
    
    print("\n=== Наследование ===")
    car = Car("Toyota", "Camry", 2020, 4, "hybrid")
    print(f"Автомобиль: {car}")
    
    print("\n=== Преобразование в словарь и кортеж ===")
    person_dict = asdict(person1)
    person_tuple = astuple(person1)
    print(f"Словарь: {person_dict}")
    print(f"Кортеж: {person_tuple}")
    
    # Сериализация в JSON
    json_str = json.dumps(person_dict, ensure_ascii=False, indent=2)
    print(f"JSON:\n{json_str}")
    
    print("\n=== Сравнение с обычным классом ===")
    # Dataclass
    dp1 = Person("Тест", 25)
    dp2 = Person("Тест", 25)
    
    # Обычный класс
    rp1 = RegularPerson("Тест", 25)
    rp2 = RegularPerson("Тест", 25)
    
    print(f"Dataclass равенство: {dp1 == dp2}")
    print(f"Обычный класс равенство: {rp1 == rp2}")
    print(f"Dataclass repr: {dp1}")
    print(f"Обычный класс repr: {rp1}")
    
    # Количество строк кода
    print("\nDataclass требует гораздо меньше кода для:")
    print("- __init__")
    print("- __repr__") 
    print("- __eq__")
    print("- __hash__ (если frozen=True)")
    print("- И других магических методов") 