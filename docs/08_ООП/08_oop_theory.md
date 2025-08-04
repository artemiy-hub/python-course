# Теория: Объектно-ориентированное программирование в Python

## 🎯 Цель раздела

Объектно-ориентированное программирование (ООП) - это парадигма программирования, основанная на концепции "объектов", которые содержат данные (атрибуты) и код (методы). Python полностью поддерживает ООП и предоставляет мощные инструменты для создания элегантных и эффективных объектно-ориентированных решений.

## 📋 Содержание

1. [Основы ООП](#основы-ооп)
2. [Классы и объекты](#классы-и-объекты)
3. [Атрибуты и методы](#атрибуты-и-методы)
4. [Инкапсуляция](#инкапсуляция)
5. [Наследование](#наследование)
6. [Полиморфизм](#полиморфизм)
7. [Абстракция](#абстракция)
8. [Специальные методы](#специальные-методы)
9. [Метаклассы](#метаклассы)
10. [Дескрипторы](#дескрипторы)
11. [Лучшие практики](#лучшие-практики)

---

## 🏗️ Основы ООП

### Четыре столпа ООП

**1. Инкапсуляция** - объединение данных и методов в одном объекте, сокрытие внутренней реализации.

**2. Наследование** - возможность создавать новые классы на основе существующих, наследуя их свойства и методы.

**3. Полиморфизм** - способность объектов разных типов отвечать на одни и те же сообщения.

**4. Абстракция** - выделение существенных характеристик объекта, игнорируя несущественные детали.

### Преимущества ООП

```python
# Модульность - код разбит на логические блоки
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance
    
    def deposit(self, amount):
        self._balance += amount
    
    def withdraw(self, amount):
        if self._balance >= amount:
            self._balance -= amount
            return True
        return False

# Повторное использование - наследование
class SavingsAccount(BankAccount):
    def __init__(self, balance=0, interest_rate=0.02):
        super().__init__(balance)
        self.interest_rate = interest_rate
    
    def add_interest(self):
        self._balance *= (1 + self.interest_rate)

# Масштабируемость - легко добавлять новый функционал
class CheckingAccount(BankAccount):
    def __init__(self, balance=0, overdraft_limit=100):
        super().__init__(balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if self._balance + self.overdraft_limit >= amount:
            self._balance -= amount
            return True
        return False
```

### Концепции объектного мышления

```python
# Объект = Данные + Поведение
class Car:
    """Автомобиль как объект"""
    
    # Данные (атрибуты)
    def __init__(self, make, model, year):
        self.make = make        # Марка
        self.model = model      # Модель
        self.year = year        # Год
        self.speed = 0          # Текущая скорость
        self.engine_on = False  # Состояние двигателя
    
    # Поведение (методы)
    def start_engine(self):
        """Запустить двигатель"""
        self.engine_on = True
        print(f"{self.make} {self.model}: двигатель запущен")
    
    def accelerate(self, increment):
        """Ускориться"""
        if self.engine_on:
            self.speed += increment
            print(f"Скорость: {self.speed} км/ч")
        else:
            print("Сначала запустите двигатель!")
    
    def brake(self, decrement):
        """Затормозить"""
        self.speed = max(0, self.speed - decrement)
        print(f"Скорость: {self.speed} км/ч")
    
    def stop_engine(self):
        """Заглушить двигатель"""
        if self.speed == 0:
            self.engine_on = False
            print("Двигатель заглушен")
        else:
            print("Остановите автомобиль перед глушением двигателя!")

# Использование
my_car = Car("Toyota", "Camry", 2022)
my_car.start_engine()
my_car.accelerate(50)
my_car.brake(20)
my_car.brake(30)
my_car.stop_engine()
```

---

## 🏭 Классы и объекты

### Определение классов

```python
# Базовое определение класса
class Person:
    """Класс для представления человека"""
    
    # Атрибут класса (общий для всех экземпляров)
    species = "Homo sapiens"
    population = 0
    
    def __init__(self, name, age):
        """Конструктор - инициализация объекта"""
        # Атрибуты экземпляра (уникальные для каждого объекта)
        self.name = name
        self.age = age
        self.email = None
        
        # Увеличиваем счетчик популяции
        Person.population += 1
    
    def __del__(self):
        """Деструктор - вызывается при удалении объекта"""
        Person.population -= 1
        print(f"Объект {self.name} удален")
    
    def introduce(self):
        """Метод экземпляра"""
        return f"Привет, меня зовут {self.name}, мне {self.age} лет"
    
    def have_birthday(self):
        """Увеличить возраст на год"""
        self.age += 1
        print(f"С днем рождения, {self.name}! Теперь вам {self.age} лет")
    
    @classmethod
    def get_population(cls):
        """Метод класса - работает с атрибутами класса"""
        return f"Популяция: {cls.population} человек"
    
    @staticmethod
    def is_adult(age):
        """Статический метод - не связан с экземпляром или классом"""
        return age >= 18
    
    def __str__(self):
        """Строковое представление объекта"""
        return f"Person(name='{self.name}', age={self.age})"
    
    def __repr__(self):
        """Формальное представление объекта"""
        return f"Person('{self.name}', {self.age})"

# Создание объектов
person1 = Person("Алиса", 25)
person2 = Person("Боб", 30)

print(person1.introduce())  # Привет, меня зовут Алиса, мне 25 лет
print(Person.get_population())  # Популяция: 2 человек
print(Person.is_adult(person1.age))  # True
```

### Атрибуты класса vs атрибуты экземпляра

```python
class Counter:
    """Демонстрация различий между атрибутами класса и экземпляра"""
    
    # Атрибут класса - общий для всех экземпляров
    total_count = 0
    instances = []
    
    def __init__(self, name):
        # Атрибут экземпляра - уникальный для каждого объекта
        self.name = name
        self.count = 0
        
        # Изменяем атрибуты класса
        Counter.total_count += 1
        Counter.instances.append(self)
    
    def increment(self):
        """Увеличить счетчик экземпляра"""
        self.count += 1
    
    @classmethod
    def get_total_count(cls):
        """Получить общий счетчик"""
        return cls.total_count
    
    @classmethod
    def reset_all(cls):
        """Сбросить все счетчики"""
        for instance in cls.instances:
            instance.count = 0
        print("Все счетчики сброшены")

# Тестирование
counter1 = Counter("Первый")
counter2 = Counter("Второй")

counter1.increment()
counter1.increment()
counter2.increment()

print(f"Счетчик 1: {counter1.count}")  # 2
print(f"Счетчик 2: {counter2.count}")  # 1
print(f"Общий счетчик: {Counter.get_total_count()}")  # 2

# Изменение атрибута класса влияет на все экземпляры
print(f"Всего экземпляров: {len(Counter.instances)}")  # 2

Counter.reset_all()
print(f"После сброса - Счетчик 1: {counter1.count}")  # 0
```

### Пространства имен и область видимости

```python
class NamespaceDemo:
    """Демонстрация пространств имен в классах"""
    
    class_var = "Переменная класса"
    
    def __init__(self, value):
        self.instance_var = value
        
        # Локальная переменная в методе
        local_var = "Локальная переменная"
        print(f"В __init__: {local_var}")
    
    def method_demo(self):
        """Демонстрация доступа к различным переменным"""
        # Доступ к переменной экземпляра
        print(f"Instance var: {self.instance_var}")
        
        # Доступ к переменной класса через экземпляр
        print(f"Class var (через self): {self.class_var}")
        
        # Доступ к переменной класса через класс
        print(f"Class var (через класс): {NamespaceDemo.class_var}")
        
        # Локальная переменная метода
        method_local = "Локальная переменная метода"
        print(f"Method local: {method_local}")
    
    def modify_attributes(self):
        """Изменение атрибутов"""
        # Изменение атрибута экземпляра
        self.instance_var = "Измененная переменная экземпляра"
        
        # Это создаст новый атрибут экземпляра, не изменив атрибут класса
        self.class_var = "Переменная экземпляра (маскирует переменную класса)"
        
        print(f"После изменения self.class_var: {self.class_var}")
        print(f"Переменная класса осталась: {NamespaceDemo.class_var}")

# Тестирование
obj = NamespaceDemo("Значение экземпляра")
obj.method_demo()
print("\n--- После изменений ---")
obj.modify_attributes()
```

---

## 🔒 Инкапсуляция

### Уровни доступа в Python

```python
class BankAccount:
    """Демонстрация инкапсуляции в Python"""
    
    def __init__(self, account_number, initial_balance=0):
        # Публичный атрибут (public) - доступен везде
        self.account_number = account_number
        
        # Защищенный атрибут (protected) - конвенция: не использовать вне класса
        self._balance = initial_balance
        
        # Приватный атрибут (private) - name mangling
        self.__pin = "1234"
        
        # Публичный атрибут для хранения истории
        self.transaction_history = []
    
    # Публичный метод
    def get_balance(self):
        """Получить баланс счета"""
        return self._balance
    
    # Защищенный метод (конвенция)
    def _log_transaction(self, transaction_type, amount):
        """Записать транзакцию в историю"""
        from datetime import datetime
        self.transaction_history.append({
            'type': transaction_type,
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self._balance
        })
    
    # Приватный метод
    def __validate_pin(self, pin):
        """Проверить PIN код"""
        return pin == self.__pin
    
    def deposit(self, amount):
        """Внести деньги на счет"""
        if amount > 0:
            self._balance += amount
            self._log_transaction("deposit", amount)
            return True
        return False
    
    def withdraw(self, amount, pin):
        """Снять деньги со счета"""
        if not self.__validate_pin(pin):
            raise ValueError("Неверный PIN код")
        
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            self._log_transaction("withdrawal", amount)
            return True
        return False
    
    def change_pin(self, old_pin, new_pin):
        """Изменить PIN код"""
        if self.__validate_pin(old_pin):
            self.__pin = new_pin
            return True
        return False
    
    # Демонстрация доступа к приватному атрибуту изнутри класса
    def get_pin_length(self):
        """Получить длину PIN кода (для демонстрации)"""
        return len(self.__pin)

# Тестирование инкапсуляции
account = BankAccount("12345", 1000)

# Публичный доступ
print(f"Номер счета: {account.account_number}")
print(f"Баланс: {account.get_balance()}")

# Защищенный атрибут (можно, но не рекомендуется)
print(f"Прямой доступ к балансу: {account._balance}")

# Попытка доступа к приватному атрибуту
try:
    print(account.__pin)  # Вызовет AttributeError
except AttributeError as e:
    print(f"Ошибка доступа: {e}")

# Доступ через name mangling (не рекомендуется!)
print(f"PIN через name mangling: {account._BankAccount__pin}")

# Использование методов
account.deposit(500)
account.withdraw(200, "1234")
print(f"Баланс после операций: {account.get_balance()}")
```

### Свойства (Properties)

```python
class Temperature:
    """Класс для работы с температурой с валидацией"""
    
    def __init__(self, celsius=0):
        self._celsius = 0
        self.celsius = celsius  # Используем setter для валидации
    
    @property
    def celsius(self):
        """Getter для температуры в Цельсиях"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Setter для температуры в Цельсиях с валидацией"""
        if value < -273.15:
            raise ValueError("Температура не может быть ниже абсолютного нуля")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """Температура в Фаренгейтах (только чтение)"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """Setter для температуры в Фаренгейтах"""
        celsius_value = (value - 32) * 5/9
        self.celsius = celsius_value  # Используем setter для валидации
    
    @property
    def kelvin(self):
        """Температура в Кельвинах (только чтение)"""
        return self._celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value):
        """Setter для температуры в Кельвинах"""
        if value < 0:
            raise ValueError("Температура в Кельвинах не может быть отрицательной")
        self.celsius = value - 273.15
    
    def __str__(self):
        return f"{self._celsius:.2f}°C ({self.fahrenheit:.2f}°F, {self.kelvin:.2f}K)"

# Использование свойств
temp = Temperature(25)
print(temp)  # 25.00°C (77.00°F, 298.15K)

# Изменение через свойство
temp.fahrenheit = 100
print(temp)  # 37.78°C (100.00°F, 310.93K)

temp.kelvin = 300
print(temp)  # 26.85°C (80.33°F, 300.00K)

# Валидация работает
try:
    temp.celsius = -300  # Ниже абсолютного нуля
except ValueError as e:
    print(f"Ошибка: {e}")
```

### Дескрипторы данных

```python
class ValidatedAttribute:
    """Дескриптор для валидации атрибутов"""
    
    def __init__(self, validator, name=None):
        self.validator = validator
        self.name = name
    
    def __set_name__(self, owner, name):
        """Автоматически устанавливается имя атрибута (Python 3.6+)"""
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not self.validator(value):
            raise ValueError(f"Недопустимое значение для {self.name}: {value}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        del instance.__dict__[self.name]

# Валидаторы
def positive_number(value):
    return isinstance(value, (int, float)) and value > 0

def non_empty_string(value):
    return isinstance(value, str) and len(value.strip()) > 0

def valid_email(value):
    return isinstance(value, str) and "@" in value and "." in value

class Product:
    """Продукт с валидированными атрибутами"""
    
    # Использование дескрипторов
    price = ValidatedAttribute(positive_number)
    name = ValidatedAttribute(non_empty_string)
    email = ValidatedAttribute(valid_email)
    
    def __init__(self, name, price, email):
        self.name = name
        self.price = price
        self.email = email
    
    def __str__(self):
        return f"Product(name='{self.name}', price={self.price}, email='{self.email}')"

# Тестирование
try:
    product = Product("Laptop", 1000, "sales@company.com")
    print(product)
    
    # Валидация сработает
    product.price = -100  # Ошибка: отрицательная цена
except ValueError as e:
    print(f"Ошибка валидации: {e}")
```

---

## 🧬 Наследование

### Базовое наследование

```python
# Базовый класс (родительский)
class Animal:
    """Базовый класс для всех животных"""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.energy = 100
    
    def eat(self, food_energy=20):
        """Животное ест и восстанавливает энергию"""
        self.energy += food_energy
        print(f"{self.name} поел и восстановил энергию. Энергия: {self.energy}")
    
    def sleep(self, hours=8):
        """Животное спит"""
        energy_restored = hours * 5
        self.energy += energy_restored
        print(f"{self.name} спал {hours} часов. Энергия: {self.energy}")
    
    def move(self):
        """Базовое движение"""
        if self.energy > 10:
            self.energy -= 10
            print(f"{self.name} движется. Энергия: {self.energy}")
        else:
            print(f"{self.name} слишком устал для движения")
    
    def make_sound(self):
        """Базовый звук (будет переопределен в подклассах)"""
        print(f"{self.name} издает звук")
    
    def __str__(self):
        return f"{self.species} по имени {self.name} (энергия: {self.energy})"

# Производный класс (наследник)
class Dog(Animal):
    """Класс собаки, наследующий от Animal"""
    
    def __init__(self, name, breed):
        # Вызов конструктора родительского класса
        super().__init__(name, "Собака")
        self.breed = breed
        self.loyalty = 100
    
    def make_sound(self):
        """Переопределение метода родительского класса"""
        print(f"{self.name} гавкает: Гав-гав!")
    
    def fetch(self, item="мяч"):
        """Специфичный для собаки метод"""
        if self.energy > 15:
            self.energy -= 15
            self.loyalty += 5
            print(f"{self.name} принес {item}! Лояльность: {self.loyalty}")
        else:
            print(f"{self.name} слишком устал, чтобы принести {item}")
    
    def guard(self):
        """Охрана территории"""
        if self.energy > 20:
            self.energy -= 20
            print(f"{self.name} охраняет дом")
        else:
            print(f"{self.name} слишком устал для охраны")

class Cat(Animal):
    """Класс кошки, наследующий от Animal"""
    
    def __init__(self, name, color):
        super().__init__(name, "Кошка")
        self.color = color
        self.independence = 80
    
    def make_sound(self):
        """Переопределение метода"""
        print(f"{self.name} мяукает: Мяу-мяу!")
    
    def purr(self):
        """Специфичный для кошки метод"""
        self.energy += 5
        print(f"{self.name} мурлычет. Энергия: {self.energy}")
    
    def hunt(self, prey="мышь"):
        """Охота"""
        if self.energy > 25:
            self.energy -= 25
            self.independence += 3
            print(f"{self.name} поймал {prey}! Независимость: {self.independence}")
        else:
            print(f"{self.name} слишком устал для охоты")

# Использование наследования
dog = Dog("Рекс", "Немецкая овчарка")
cat = Cat("Мурка", "Рыжий")

print(dog)  # Собака по имени Рекс (энергия: 100)
print(cat)  # Кошка по имени Мурка (энергия: 100)

# Использование методов родительского класса
dog.eat()
cat.sleep(6)

# Использование переопределенных методов
dog.make_sound()  # Рекс гавкает: Гав-гав!
cat.make_sound()  # Мурка мяукает: Мяу-мяу!

# Использование специфичных методов
dog.fetch("палка")
cat.hunt("птичка")
```

### Множественное наследование

```python
# Миксины - классы, предоставляющие функциональность
class LoggerMixin:
    """Миксин для логирования действий"""
    
    def log_action(self, action):
        """Записать действие в лог"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.__class__.__name__}: {action}")

class SerializableMixin:
    """Миксин для сериализации объектов"""
    
    def to_dict(self):
        """Преобразовать объект в словарь"""
        return {key: value for key, value in self.__dict__.items() 
                if not key.startswith('_')}
    
    def from_dict(self, data):
        """Восстановить объект из словаря"""
        for key, value in data.items():
            setattr(self, key, value)

class ValidationMixin:
    """Миксин для валидации данных"""
    
    def validate(self):
        """Базовая валидация (переопределяется в подклассах)"""
        return True
    
    def is_valid(self):
        """Проверить валидность объекта"""
        try:
            return self.validate()
        except Exception as e:
            print(f"Ошибка валидации: {e}")
            return False

# Основные классы
class Vehicle:
    """Базовый класс транспортного средства"""
    
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.speed = 0
    
    def start(self):
        """Запустить транспорт"""
        print(f"{self.make} {self.model} запущен")
    
    def accelerate(self, increment):
        """Ускориться"""
        self.speed += increment
        print(f"Скорость: {self.speed} км/ч")

class Electric:
    """Класс для электрических транспортных средств"""
    
    def __init__(self, battery_capacity=100):
        self.battery_capacity = battery_capacity
        self.current_charge = battery_capacity
    
    def charge(self, amount=None):
        """Зарядить батарею"""
        if amount is None:
            amount = self.battery_capacity - self.current_charge
        
        self.current_charge = min(self.battery_capacity, self.current_charge + amount)
        print(f"Заряд батареи: {self.current_charge}/{self.battery_capacity}")
    
    def get_range(self):
        """Получить дальность поездки"""
        return self.current_charge * 5  # 5 км на единицу заряда

# Класс с множественным наследованием
class ElectricCar(Vehicle, Electric, LoggerMixin, SerializableMixin, ValidationMixin):
    """Электрический автомобиль с множественным наследованием"""
    
    def __init__(self, make, model, year, battery_capacity=100):
        # Инициализация родительских классов
        Vehicle.__init__(self, make, model, year)
        Electric.__init__(self, battery_capacity)
        
        self.autopilot = False
        self.log_action("Создан электрический автомобиль")
    
    def start(self):
        """Переопределение метода запуска"""
        if self.current_charge > 0:
            super().start()  # Вызов метода родительского класса
            self.log_action("Автомобиль запущен")
        else:
            print("Недостаточно заряда для запуска")
            self.log_action("Попытка запуска с пустой батареей")
    
    def accelerate(self, increment):
        """Переопределение ускорения с расходом энергии"""
        if self.current_charge > increment * 0.1:
            super().accelerate(increment)
            self.current_charge -= increment * 0.1
            self.log_action(f"Ускорение на {increment} км/ч")
        else:
            print("Недостаточно заряда для ускорения")
    
    def enable_autopilot(self):
        """Включить автопилот"""
        if self.speed > 0:
            self.autopilot = True
            self.log_action("Автопилот включен")
        else:
            print("Для включения автопилота нужно начать движение")
    
    def validate(self):
        """Валидация электрического автомобиля"""
        if self.year < 1990:
            raise ValueError("Год выпуска слишком старый для электромобиля")
        if self.battery_capacity <= 0:
            raise ValueError("Емкость батареи должна быть положительной")
        return True

# Проверка порядка разрешения методов (MRO)
print("MRO для ElectricCar:")
for cls in ElectricCar.__mro__:
    print(f"  {cls}")

# Использование
tesla = ElectricCar("Tesla", "Model S", 2022, 100)

# Проверка валидности
if tesla.is_valid():
    print("Автомобиль прошел валидацию")

# Использование методов из разных родительских классов
tesla.charge(50)  # От Electric
tesla.start()     # Переопределенный метод
tesla.accelerate(60)  # Переопределенный метод
tesla.enable_autopilot()  # Собственный метод

# Сериализация
car_data = tesla.to_dict()
print(f"Сериализованные данные: {car_data}")
```

### Композиция vs Наследование

```python
# Пример композиции (предпочтительный подход во многих случаях)
class Engine:
    """Двигатель как отдельный компонент"""
    
    def __init__(self, power, fuel_type):
        self.power = power
        self.fuel_type = fuel_type
        self.running = False
    
    def start(self):
        self.running = True
        return f"Двигатель {self.power} л.с. запущен"
    
    def stop(self):
        self.running = False
        return "Двигатель остановлен"

class GPS:
    """GPS навигация как отдельный компонент"""
    
    def __init__(self):
        self.current_location = "Неизвестно"
        self.destination = None
    
    def set_destination(self, destination):
        self.destination = destination
        return f"Маршрут построен до: {destination}"
    
    def get_directions(self):
        if self.destination:
            return f"Следуйте по маршруту до {self.destination}"
        return "Пункт назначения не задан"

class Radio:
    """Радио как отдельный компонент"""
    
    def __init__(self):
        self.station = 100.0
        self.volume = 5
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        return f"Радио включено, станция {self.station} FM"
    
    def change_station(self, station):
        self.station = station
        return f"Переключено на {station} FM"

# Композиция - автомобиль СОДЕРЖИТ компоненты
class ModernCar:
    """Современный автомобиль, использующий композицию"""
    
    def __init__(self, make, model, engine_power=150):
        self.make = make
        self.model = model
        
        # Композиция - создаем компоненты
        self.engine = Engine(engine_power, "бензин")
        self.gps = GPS()
        self.radio = Radio()
        
        self.speed = 0
    
    def start_car(self):
        """Запуск автомобиля"""
        result = self.engine.start()
        print(f"{self.make} {self.model}: {result}")
    
    def drive_to(self, destination):
        """Поехать к пункту назначения"""
        if self.engine.running:
            directions = self.gps.set_destination(destination)
            print(directions)
            self.speed = 60
            print(f"Едем со скоростью {self.speed} км/ч")
        else:
            print("Сначала запустите двигатель")
    
    def listen_to_music(self, station=None):
        """Включить музыку"""
        music = self.radio.turn_on()
        if station:
            music = self.radio.change_station(station)
        print(music)
    
    def get_car_info(self):
        """Получить информацию об автомобиле"""
        return {
            'make': self.make,
            'model': self.model,
            'engine_running': self.engine.running,
            'engine_power': self.engine.power,
            'speed': self.speed,
            'gps_destination': self.gps.destination,
            'radio_station': self.radio.station if self.radio.is_on else None
        }

# Использование композиции
car = ModernCar("BMW", "X5", 300)
car.start_car()
car.drive_to("Москва")
car.listen_to_music(101.2)

print("\nИнформация об автомобиле:")
info = car.get_car_info()
for key, value in info.items():
    print(f"  {key}: {value}")

# Преимущества композиции:
# 1. Гибкость - можно легко заменить компоненты
car.engine = Engine(400, "электричество")  # Заменили двигатель
print(f"\nНовый двигатель: {car.engine.power} л.с., тип: {car.engine.fuel_type}")

# 2. Повторное использование - компоненты можно использовать в других классах
class Motorcycle:
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.engine = Engine(100, "бензин")  # Тот же компонент

# 3. Более четкое разделение ответственности
```

---

## 🎭 Полиморфизм

### Полиморфизм через наследование

```python
from abc import ABC, abstractmethod
import math

# Абстрактный базовый класс
class Shape(ABC):
    """Абстрактный класс геометрической фигуры"""
    
    def __init__(self, color="white"):
        self.color = color
    
    @abstractmethod
    def area(self):
        """Абстрактный метод для вычисления площади"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Абстрактный метод для вычисления периметра"""
        pass
    
    def describe(self):
        """Общий метод описания фигуры"""
        return f"{self.color} {self.__class__.__name__}"
    
    # Полиморфный метод
    def scale(self, factor):
        """Масштабирование фигуры (переопределяется в подклассах)"""
        print(f"Масштабирование {self.__class__.__name__} в {factor} раз")

class Rectangle(Shape):
    """Прямоугольник"""
    
    def __init__(self, width, height, color="white"):
        super().__init__(color)
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def scale(self, factor):
        super().scale(factor)
        self.width *= factor
        self.height *= factor
    
    def __str__(self):
        return f"Rectangle({self.width}x{self.height}, {self.color})"

class Circle(Shape):
    """Круг"""
    
    def __init__(self, radius, color="white"):
        super().__init__(color)
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius
    
    def scale(self, factor):
        super().scale(factor)
        self.radius *= factor
    
    def __str__(self):
        return f"Circle(radius={self.radius}, {self.color})"

class Triangle(Shape):
    """Треугольник"""
    
    def __init__(self, side_a, side_b, side_c, color="white"):
        super().__init__(color)
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
    
    def area(self):
        # Формула Герона
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))
    
    def perimeter(self):
        return self.side_a + self.side_b + self.side_c
    
    def scale(self, factor):
        super().scale(factor)
        self.side_a *= factor
        self.side_b *= factor
        self.side_c *= factor
    
    def __str__(self):
        return f"Triangle({self.side_a}, {self.side_b}, {self.side_c}, {self.color})"

# Полиморфное использование
def print_shape_info(shape):
    """Функция, работающая с любой фигурой полиморфно"""
    print(f"Фигура: {shape}")
    print(f"Описание: {shape.describe()}")
    print(f"Площадь: {shape.area():.2f}")
    print(f"Периметр: {shape.perimeter():.2f}")
    print("-" * 40)

# Создание различных фигур
shapes = [
    Rectangle(5, 3, "красный"),
    Circle(4, "синий"),
    Triangle(3, 4, 5, "зеленый")
]

# Полиморфное использование - одна функция работает с разными типами
for shape in shapes:
    print_shape_info(shape)

# Полиморфное масштабирование
print("Масштабирование всех фигур в 2 раза:")
for shape in shapes:
    shape.scale(2)
    print(f"После масштабирования: {shape}")
```

### Duck Typing

```python
# Duck Typing - "Если это выглядит как утка, плавает как утка и крякает как утка, то это утка"

class Duck:
    """Настоящая утка"""
    
    def quack(self):
        return "Кря-кря!"
    
    def swim(self):
        return "Плаваю как утка"
    
    def fly(self):
        return "Лечу как утка"

class Person:
    """Человек, который может имитировать утку"""
    
    def __init__(self, name):
        self.name = name
    
    def quack(self):
        return f"{self.name} говорит: Кря-кря!"
    
    def swim(self):
        return f"{self.name} плавает как утка"
    
    def fly(self):
        return f"{self.name} машет руками, пытаясь лететь"

class Robot:
    """Робот-утка"""
    
    def __init__(self, model):
        self.model = model
    
    def quack(self):
        return f"Робот {self.model}: КРЯК-КРЯК.EXE"
    
    def swim(self):
        return f"Робот {self.model}: Активирован режим плавания"
    
    def fly(self):
        return f"Робот {self.model}: Включены винты для полета"

# Полиморфная функция, использующая Duck Typing
def make_it_quack(duck_like_object):
    """Функция, которая работает с любым объектом, имеющим метод quack"""
    try:
        print(duck_like_object.quack())
    except AttributeError:
        print(f"{duck_like_object} не умеет крякать")

def duck_activities(duck_like_object):
    """Полный набор утиных активностей"""
    print(f"=== Активности для {duck_like_object.__class__.__name__} ===")
    
    # Используем hasattr для проверки наличия методов
    if hasattr(duck_like_object, 'quack'):
        print(duck_like_object.quack())
    
    if hasattr(duck_like_object, 'swim'):
        print(duck_like_object.swim())
    
    if hasattr(duck_like_object, 'fly'):
        print(duck_like_object.fly())
    
    print()

# Создание объектов разных типов
duck = Duck()
person = Person("Алиса")
robot = Robot("DuckBot-3000")

# Duck Typing в действии - все объекты обрабатываются одинаково
duck_like_objects = [duck, person, robot]

for obj in duck_like_objects:
    duck_activities(obj)

# Демонстрация того, что важно поведение, а не тип
class FakeString:
    """Класс, который ведет себя как строка"""
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
    def upper(self):
        return self.value.upper()
    
    def lower(self):
        return self.value.lower()
    
    def __len__(self):
        return len(str(self.value))

def string_operations(string_like):
    """Функция, работающая с объектами, похожими на строки"""
    print(f"Объект: {string_like}")
    print(f"Верхний регистр: {string_like.upper()}")
    print(f"Нижний регистр: {string_like.lower()}")
    print(f"Длина: {len(string_like)}")
    print()

# Работает и со строкой, и с объектом, похожим на строку
regular_string = "Hello World"
fake_string = FakeString("Hello World")

print("=== Операции со строкой ===")
string_operations(regular_string)

print("=== Операции с объектом, похожим на строку ===")
string_operations(fake_string)
```

### Протоколы и типизация

```python
from typing import Protocol, runtime_checkable

# Определение протоколов для типизации
@runtime_checkable
class Drawable(Protocol):
    """Протокол для объектов, которые можно нарисовать"""
    
    def draw(self) -> str:
        ...
    
    def get_area(self) -> float:
        ...

@runtime_checkable
class Movable(Protocol):
    """Протокол для объектов, которые можно перемещать"""
    
    def move(self, x: float, y: float) -> None:
        ...
    
    def get_position(self) -> tuple[float, float]:
        ...

# Классы, реализующие протоколы
class GameRectangle:
    """Прямоугольник в игре"""
    
    def __init__(self, width: float, height: float, x: float = 0, y: float = 0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
    
    def draw(self) -> str:
        return f"Рисуем прямоугольник {self.width}x{self.height} в позиции ({self.x}, {self.y})"
    
    def get_area(self) -> float:
        return self.width * self.height
    
    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def get_position(self) -> tuple[float, float]:
        return (self.x, self.y)

class GameCircle:
    """Круг в игре"""
    
    def __init__(self, radius: float, x: float = 0, y: float = 0):
        self.radius = radius
        self.x = x
        self.y = y
    
    def draw(self) -> str:
        return f"Рисуем круг радиусом {self.radius} в позиции ({self.x}, {self.y})"
    
    def get_area(self) -> float:
        return math.pi * self.radius ** 2
    
    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def get_position(self) -> tuple[float, float]:
        return (self.x, self.y)

class Text:
    """Текст (только рисуемый, но не перемещаемый)"""
    
    def __init__(self, content: str):
        self.content = content
    
    def draw(self) -> str:
        return f"Рисуем текст: '{self.content}'"
    
    def get_area(self) -> float:
        return len(self.content) * 8.0  # Примерная площадь

# Функции, использующие протоколы
def render_drawable(drawable: Drawable) -> None:
    """Отрендерить объект, который можно нарисовать"""
    print(drawable.draw())
    print(f"Площадь: {drawable.get_area():.2f}")

def move_object(movable: Movable, new_x: float, new_y: float) -> None:
    """Переместить объект"""
    old_pos = movable.get_position()
    movable.move(new_x, new_y)
    new_pos = movable.get_position()
    print(f"Объект перемещен с {old_pos} в {new_pos}")

def process_game_object(obj) -> None:
    """Обработать игровой объект в зависимости от его возможностей"""
    print(f"=== Обработка {obj.__class__.__name__} ===")
    
    # Проверяем, реализует ли объект протокол Drawable
    if isinstance(obj, Drawable):
        render_drawable(obj)
    
    # Проверяем, реализует ли объект протокол Movable
    if isinstance(obj, Movable):
        print("Объект можно перемещать")
        move_object(obj, 10, 15)
    else:
        print("Объект нельзя перемещать")
    
    print()

# Тестирование протоколов
game_objects = [
    GameRectangle(5, 3),
    GameCircle(2.5),
    Text("Hello, World!")
]

for obj in game_objects:
    process_game_object(obj)

# Проверка соответствия протоколам
print("=== Проверка соответствия протоколам ===")
rect = GameRectangle(10, 5)
text = Text("Test")

print(f"Rectangle поддерживает Drawable: {isinstance(rect, Drawable)}")
print(f"Rectangle поддерживает Movable: {isinstance(rect, Movable)}")
print(f"Text поддерживает Drawable: {isinstance(text, Drawable)}")
print(f"Text поддерживает Movable: {isinstance(text, Movable)}")
```

---

## 🔮 Абстракция

### Абстрактные базовые классы

```python
from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod

class DatabaseConnection(ABC):
    """Абстрактный класс для подключения к базе данных"""
    
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port
        self.database = database
        self._connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """Абстрактный метод подключения"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Абстрактный метод отключения"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> list:
        """Абстрактный метод выполнения запроса"""
        pass
    
    @abstractmethod
    def execute_transaction(self, queries: list) -> bool:
        """Абстрактный метод выполнения транзакции"""
        pass
    
    @property
    @abstractmethod
    def connection_string(self) -> str:
        """Абстрактное свойство строки подключения"""
        pass
    
    @classmethod
    @abstractmethod
    def from_url(cls, url: str):
        """Абстрактный метод класса для создания из URL"""
        pass
    
    @staticmethod
    @abstractmethod
    def validate_query(query: str) -> bool:
        """Абстрактный статический метод валидации запроса"""
        pass
    
    # Конкретный метод (общий для всех реализаций)
    def is_connected(self) -> bool:
        """Проверить статус подключения"""
        return self._connected
    
    def safe_execute(self, query: str) -> list:
        """Безопасное выполнение запроса с проверками"""
        if not self.is_connected():
            raise RuntimeError("Нет подключения к базе данных")
        
        if not self.validate_query(query):
            raise ValueError("Недопустимый запрос")
        
        return self.execute_query(query)

# Конкретная реализация для PostgreSQL
class PostgreSQLConnection(DatabaseConnection):
    """Реализация подключения к PostgreSQL"""
    
    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        super().__init__(host, port, database)
        self.username = username
        self.password = password
    
    def connect(self) -> bool:
        """Подключение к PostgreSQL"""
        print(f"Подключение к PostgreSQL: {self.connection_string}")
        # Здесь была бы реальная логика подключения
        self._connected = True
        return True
    
    def disconnect(self) -> None:
        """Отключение от PostgreSQL"""
        print("Отключение от PostgreSQL")
        self._connected = False
    
    def execute_query(self, query: str) -> list:
        """Выполнение запроса в PostgreSQL"""
        print(f"Выполнение запроса PostgreSQL: {query}")
        # Здесь была бы реальная логика выполнения запроса
        return [{"result": "mock_data"}]
    
    def execute_transaction(self, queries: list) -> bool:
        """Выполнение транзакции в PostgreSQL"""
        print(f"Выполнение транзакции PostgreSQL с {len(queries)} запросами")
        try:
            for query in queries:
                self.execute_query(query)
            print("Транзакция зафиксирована")
            return True
        except Exception as e:
            print(f"Откат транзакции: {e}")
            return False
    
    @property
    def connection_string(self) -> str:
        """Строка подключения PostgreSQL"""
        return f"postgresql://{self.username}@{self.host}:{self.port}/{self.database}"
    
    @classmethod
    def from_url(cls, url: str):
        """Создание подключения из URL"""
        # Упрощенный парсинг URL
        parts = url.replace("postgresql://", "").split("@")
        username = parts[0]
        host_part = parts[1].split(":")
        host = host_part[0]
        port_db = host_part[1].split("/")
        port = int(port_db[0])
        database = port_db[1]
        
        return cls(host, port, database, username, "password")
    
    @staticmethod
    def validate_query(query: str) -> bool:
        """Валидация запроса PostgreSQL"""
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE"]
        return not any(keyword in query.upper() for keyword in dangerous_keywords)

# Конкретная реализация для MongoDB
class MongoDBConnection(DatabaseConnection):
    """Реализация подключения к MongoDB"""
    
    def __init__(self, host: str, port: int, database: str):
        super().__init__(host, port, database)
    
    def connect(self) -> bool:
        """Подключение к MongoDB"""
        print(f"Подключение к MongoDB: {self.connection_string}")
        self._connected = True
        return True
    
    def disconnect(self) -> None:
        """Отключение от MongoDB"""
        print("Отключение от MongoDB")
        self._connected = False
    
    def execute_query(self, query: str) -> list:
        """Выполнение запроса в MongoDB"""
        print(f"Выполнение запроса MongoDB: {query}")
        return [{"_id": "mock_id", "data": "mock_data"}]
    
    def execute_transaction(self, queries: list) -> bool:
        """Выполнение транзакции в MongoDB"""
        print(f"Выполнение транзакции MongoDB с {len(queries)} запросами")
        # MongoDB транзакции работают по-другому
        return True
    
    @property
    def connection_string(self) -> str:
        """Строка подключения MongoDB"""
        return f"mongodb://{self.host}:{self.port}/{self.database}"
    
    @classmethod
    def from_url(cls, url: str):
        """Создание подключения из URL"""
        parts = url.replace("mongodb://", "").split("/")
        host_port = parts[0].split(":")
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 27017
        database = parts[1] if len(parts) > 1 else "test"
        
        return cls(host, port, database)
    
    @staticmethod
    def validate_query(query: str) -> bool:
        """Валидация запроса MongoDB"""
        # Простая валидация для MongoDB
        return len(query) > 0 and query.startswith("{")

# Класс для работы с базами данных (использует абстракцию)
class DatabaseManager:
    """Менеджер баз данных, работающий с абстракцией"""
    
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection
    
    def initialize(self) -> bool:
        """Инициализация подключения"""
        return self.connection.connect()
    
    def cleanup(self) -> None:
        """Очистка ресурсов"""
        if self.connection.is_connected():
            self.connection.disconnect()
    
    def run_report(self, report_queries: list) -> dict:
        """Запуск отчета с несколькими запросами"""
        if not self.connection.is_connected():
            raise RuntimeError("Нет подключения к базе данных")
        
        results = {}
        for i, query in enumerate(report_queries):
            try:
                result = self.connection.safe_execute(query)
                results[f"query_{i+1}"] = result
            except Exception as e:
                results[f"query_{i+1}"] = {"error": str(e)}
        
        return results

# Использование абстракции
def demo_database_abstraction():
    """Демонстрация работы с абстракцией базы данных"""
    
    # Создание различных типов подключений
    postgres_conn = PostgreSQLConnection("localhost", 5432, "myapp", "user", "pass")
    mongo_conn = MongoDBConnection("localhost", 27017, "myapp")
    
    # Создание из URL
    postgres_from_url = PostgreSQLConnection.from_url("postgresql://user@localhost:5432/myapp")
    mongo_from_url = MongoDBConnection.from_url("mongodb://localhost:27017/myapp")
    
    connections = [postgres_conn, mongo_conn, postgres_from_url, mongo_from_url]
    
    for conn in connections:
        print(f"\n=== Тестирование {conn.__class__.__name__} ===")
        
        # Создание менеджера с абстрактным интерфейсом
        manager = DatabaseManager(conn)
        
        try:
            # Инициализация
            manager.initialize()
            
            # Выполнение запросов через абстракцию
            queries = [
                "SELECT * FROM users",
                "{find: 'users'}"
            ]
            
            results = manager.run_report(queries)
            print(f"Результаты отчета: {results}")
            
        finally:
            # Очистка
            manager.cleanup()

demo_database_abstraction()
```

### Интерфейсы через Protocol

```python
from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod

# Определение интерфейсов через Protocol
@runtime_checkable
class Serializable(Protocol):
    """Интерфейс для сериализуемых объектов"""
    
    def serialize(self) -> dict:
        """Сериализовать объект в словарь"""
        ...
    
    def deserialize(self, data: dict) -> None:
        """Десериализовать объект из словаря"""
        ...

@runtime_checkable
class Cacheable(Protocol):
    """Интерфейс для кешируемых объектов"""
    
    def get_cache_key(self) -> str:
        """Получить ключ для кеширования"""
        ...
    
    def get_cache_ttl(self) -> int:
        """Получить время жизни в кеше (секунды)"""
        ...

@runtime_checkable
class Validatable(Protocol):
    """Интерфейс для валидируемых объектов"""
    
    def validate(self) -> bool:
        """Провалидировать объект"""
        ...
    
    def get_validation_errors(self) -> list[str]:
        """Получить список ошибок валидации"""
        ...

# Базовый класс пользователя
class User:
    """Пользователь системы"""
    
    def __init__(self, user_id: str, username: str, email: str, age: int):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.age = age
        self._validation_errors = []
    
    def serialize(self) -> dict:
        """Реализация интерфейса Serializable"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'age': self.age
        }
    
    def deserialize(self, data: dict) -> None:
        """Реализация интерфейса Serializable"""
        self.user_id = data.get('user_id', '')
        self.username = data.get('username', '')
        self.email = data.get('email', '')
        self.age = data.get('age', 0)
    
    def get_cache_key(self) -> str:
        """Реализация интерфейса Cacheable"""
        return f"user:{self.user_id}"
    
    def get_cache_ttl(self) -> int:
        """Реализация интерфейса Cacheable"""
        return 3600  # 1 час
    
    def validate(self) -> bool:
        """Реализация интерфейса Validatable"""
        self._validation_errors = []
        
        if not self.username or len(self.username) < 3:
            self._validation_errors.append("Имя пользователя должно содержать минимум 3 символа")
        
        if not self.email or '@' not in self.email:
            self._validation_errors.append("Некорректный email адрес")
        
        if self.age < 0 or self.age > 150:
            self._validation_errors.append("Возраст должен быть от 0 до 150 лет")
        
        return len(self._validation_errors) == 0
    
    def get_validation_errors(self) -> list[str]:
        """Реализация интерфейса Validatable"""
        return self._validation_errors.copy()

# Продукт
class Product:
    """Продукт в системе"""
    
    def __init__(self, product_id: str, name: str, price: float, category: str):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self._validation_errors = []
    
    def serialize(self) -> dict:
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'category': self.category
        }
    
    def deserialize(self, data: dict) -> None:
        self.product_id = data.get('product_id', '')
        self.name = data.get('name', '')
        self.price = data.get('price', 0.0)
        self.category = data.get('category', '')
    
    def get_cache_key(self) -> str:
        return f"product:{self.product_id}"
    
    def get_cache_ttl(self) -> int:
        return 7200  # 2 часа
    
    def validate(self) -> bool:
        self._validation_errors = []
        
        if not self.name or len(self.name) < 2:
            self._validation_errors.append("Название продукта должно содержать минимум 2 символа")
        
        if self.price <= 0:
            self._validation_errors.append("Цена должна быть положительной")
        
        if not self.category:
            self._validation_errors.append("Категория обязательна")
        
        return len(self._validation_errors) == 0
    
    def get_validation_errors(self) -> list[str]:
        return self._validation_errors.copy()

# Сервисы, работающие с интерфейсами
class SerializationService:
    """Сервис сериализации"""
    
    @staticmethod
    def serialize_object(obj: Serializable) -> dict:
        """Сериализовать любой объект, реализующий интерфейс Serializable"""
        if not isinstance(obj, Serializable):
            raise TypeError("Объект должен реализовывать интерфейс Serializable")
        
        return obj.serialize()
    
    @staticmethod
    def serialize_list(objects: list[Serializable]) -> list[dict]:
        """Сериализовать список объектов"""
        return [obj.serialize() for obj in objects if isinstance(obj, Serializable)]

class CacheService:
    """Сервис кеширования"""
    
    def __init__(self):
        self._cache = {}
    
    def cache_object(self, obj: Cacheable) -> None:
        """Закешировать объект"""
        if not isinstance(obj, Cacheable):
            raise TypeError("Объект должен реализовывать интерфейс Cacheable")
        
        key = obj.get_cache_key()
        ttl = obj.get_cache_ttl()
        
        # Если объект также сериализуемый, сохраняем сериализованную версию
        if isinstance(obj, Serializable):
            self._cache[key] = {
                'data': obj.serialize(),
                'ttl': ttl,
                'cached_at': time.time()
            }
        else:
            self._cache[key] = {
                'data': obj,
                'ttl': ttl,
                'cached_at': time.time()
            }
        
        print(f"Объект закеширован с ключом: {key}, TTL: {ttl}s")
    
    def get_cached_object(self, cache_key: str) -> dict:
        """Получить объект из кеша"""
        return self._cache.get(cache_key)

class ValidationService:
    """Сервис валидации"""
    
    @staticmethod
    def validate_object(obj: Validatable) -> tuple[bool, list[str]]:
        """Валидировать объект"""
        if not isinstance(obj, Validatable):
            raise TypeError("Объект должен реализовывать интерфейс Validatable")
        
        is_valid = obj.validate()
        errors = obj.get_validation_errors()
        
        return is_valid, errors
    
    @staticmethod
    def validate_batch(objects: list[Validatable]) -> dict:
        """Валидировать список объектов"""
        results = {}
        
        for i, obj in enumerate(objects):
            if isinstance(obj, Validatable):
                is_valid, errors = ValidationService.validate_object(obj)
                results[i] = {
                    'valid': is_valid,
                    'errors': errors,
                    'object_type': obj.__class__.__name__
                }
        
        return results

# Демонстрация работы с интерфейсами
def demo_interfaces():
    """Демонстрация работы с интерфейсами"""
    import time
    
    # Создание объектов
    user = User("u001", "alice", "alice@example.com", 25)
    product = Product("p001", "Laptop", 1000.0, "Electronics")
    invalid_user = User("u002", "ab", "invalid-email", -5)  # Невалидный пользователь
    
    objects = [user, product, invalid_user]
    
    print("=== Сериализация ===")
    serialization_service = SerializationService()
    
    for obj in objects:
        try:
            serialized = serialization_service.serialize_object(obj)
            print(f"{obj.__class__.__name__}: {serialized}")
        except TypeError as e:
            print(f"Ошибка сериализации: {e}")
    
    print("\n=== Кеширование ===")
    cache_service = CacheService()
    
    for obj in objects:
        try:
            cache_service.cache_object(obj)
        except TypeError as e:
            print(f"Ошибка кеширования: {e}")
    
    print("\n=== Валидация ===")
    validation_service = ValidationService()
    
    validation_results = validation_service.validate_batch(objects)
    for idx, result in validation_results.items():
        print(f"Объект {idx} ({result['object_type']}):")
        print(f"  Валиден: {result['valid']}")
        if result['errors']:
            print(f"  Ошибки: {result['errors']}")
    
    print("\n=== Проверка соответствия интерфейсам ===")
    for obj in objects:
        print(f"{obj.__class__.__name__}:")
        print(f"  Serializable: {isinstance(obj, Serializable)}")
        print(f"  Cacheable: {isinstance(obj, Cacheable)}")
        print(f"  Validatable: {isinstance(obj, Validatable)}")

demo_interfaces()
```

Этот раздел демонстрирует принципы абстракции в Python, включая абстрактные базовые классы и современные протоколы для определения интерфейсов. Абстракция помогает создавать гибкие и расширяемые системы. 