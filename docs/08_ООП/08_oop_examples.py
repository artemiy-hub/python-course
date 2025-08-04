#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Объектно-ориентированное программирование в Python

Этот файл содержит подробные примеры для изучения:
- Основ ООП (классы, объекты, атрибуты, методы)
- Инкапсуляции (public, protected, private, properties)
- Наследования (одиночное, множественное, MRO)
- Полиморфизма (duck typing, протоколы)
- Абстракции (ABC, интерфейсы)
- Специальных методов (magic methods)
- Метаклассов и дескрипторов
- Паттернов проектирования
"""

import abc
import functools
import weakref
from typing import Protocol, runtime_checkable, Any, Optional, List, Dict
from datetime import datetime, timedelta
import json


def example_01_basic_classes():
    """
    Пример 1: Основы классов и объектов
    
    Демонстрирует создание классов, атрибуты класса и экземпляра,
    методы экземпляра, класса и статические методы.
    """
    print("=== Пример 1: Основы классов и объектов ===")
    
    class Book:
        """Класс для представления книги"""
        
        # Атрибут класса - общий для всех экземпляров
        library_name = "Центральная библиотека"
        total_books = 0
        
        def __init__(self, title, author, isbn, pages):
            """Конструктор - инициализация экземпляра"""
            # Атрибуты экземпляра - уникальные для каждого объекта
            self.title = title
            self.author = author
            self.isbn = isbn
            self.pages = pages
            self.is_available = True
            self.borrowed_by = None
            self.created_at = datetime.now()
            
            # Увеличиваем счетчик книг
            Book.total_books += 1
        
        def __del__(self):
            """Деструктор - вызывается при удалении объекта"""
            Book.total_books -= 1
            print(f"Книга '{self.title}' удалена из памяти")
        
        # Методы экземпляра - работают с конкретным объектом
        def borrow(self, borrower_name):
            """Взять книгу в аренду"""
            if self.is_available:
                self.is_available = False
                self.borrowed_by = borrower_name
                return f"Книга '{self.title}' выдана пользователю {borrower_name}"
            else:
                return f"Книга '{self.title}' уже занята пользователем {self.borrowed_by}"
        
        def return_book(self):
            """Вернуть книгу"""
            if not self.is_available:
                borrower = self.borrowed_by
                self.is_available = True
                self.borrowed_by = None
                return f"Книга '{self.title}' возвращена пользователем {borrower}"
            else:
                return f"Книга '{self.title}' уже доступна"
        
        def get_info(self):
            """Получить информацию о книге"""
            status = "Доступна" if self.is_available else f"Занята ({self.borrowed_by})"
            return f"'{self.title}' - {self.author} ({self.pages} стр.) - {status}"
        
        # Методы класса - работают с классом, а не с экземпляром
        @classmethod
        def get_library_info(cls):
            """Получить информацию о библиотеке"""
            return f"Библиотека: {cls.library_name}, всего книг: {cls.total_books}"
        
        @classmethod
        def create_from_string(cls, book_string):
            """Создать книгу из строки (альтернативный конструктор)"""
            parts = book_string.split(';')
            if len(parts) != 4:
                raise ValueError("Неправильный формат строки")
            
            title, author, isbn, pages = parts
            return cls(title.strip(), author.strip(), isbn.strip(), int(pages.strip()))
        
        # Статические методы - не связаны ни с классом, ни с экземпляром
        @staticmethod
        def is_valid_isbn(isbn):
            """Проверить корректность ISBN"""
            # Упрощенная проверка
            return len(isbn.replace('-', '')) in [10, 13] and isbn.replace('-', '').isdigit()
        
        @staticmethod
        def calculate_reading_time(pages, reading_speed=250):
            """Рассчитать время чтения (слов в минуту)"""
            words_per_page = 250
            total_words = pages * words_per_page
            minutes = total_words / reading_speed
            hours = minutes / 60
            return f"Примерное время чтения: {hours:.1f} часов"
        
        # Специальные методы
        def __str__(self):
            """Строковое представление для пользователей"""
            return f"Книга: {self.title} - {self.author}"
        
        def __repr__(self):
            """Формальное представление для разработчиков"""
            return f"Book('{self.title}', '{self.author}', '{self.isbn}', {self.pages})"
        
        def __eq__(self, other):
            """Сравнение книг по ISBN"""
            if isinstance(other, Book):
                return self.isbn == other.isbn
            return False
        
        def __len__(self):
            """Длина книги в страницах"""
            return self.pages
    
    # Тестирование класса Book
    print("1. Создание книг:")
    
    # Создание объектов
    book1 = Book("1984", "Джордж Оруэлл", "978-0-452-28423-4", 328)
    book2 = Book("Мастер и Маргарита", "Михаил Булгаков", "978-5-17-123456-7", 480)
    
    print(f"Книга 1: {book1}")
    print(f"Книга 2: {book2}")
    print(f"Repr книги 1: {repr(book1)}")
    
    print("\n2. Информация о библиотеке:")
    print(Book.get_library_info())
    
    print("\n3. Операции с книгами:")
    print(book1.borrow("Алиса"))
    print(book1.borrow("Боб"))  # Книга уже занята
    print(book1.return_book())
    
    print("\n4. Статические методы:")
    print(f"ISBN корректен: {Book.is_valid_isbn('978-0-452-28423-4')}")
    print(f"ISBN некорректен: {Book.is_valid_isbn('123')}")
    print(Book.calculate_reading_time(328))
    
    print("\n5. Альтернативный конструктор:")
    book3 = Book.create_from_string("Война и мир; Лев Толстой; 978-5-17-654321-0; 1225")
    print(f"Книга из строки: {book3}")
    
    print("\n6. Специальные методы:")
    print(f"Длина книги 1: {len(book1)} страниц")
    print(f"Книги равны: {book1 == book2}")
    
    print("\n7. Информация о всех книгах:")
    books = [book1, book2, book3]
    for book in books:
        print(f"  {book.get_info()}")
    
    print(f"\nОбщая статистика: {Book.get_library_info()}")


def example_02_encapsulation():
    """
    Пример 2: Инкапсуляция и уровни доступа
    
    Демонстрирует публичные, защищенные и приватные атрибуты,
    свойства (properties) и дескрипторы для контроля доступа.
    """
    print("=== Пример 2: Инкапсуляция и уровни доступа ===")
    
    # Дескриптор для валидации
    class ValidatedAttribute:
        """Дескриптор для валидации атрибутов"""
        
        def __init__(self, validator, name=None):
            self.validator = validator
            self.name = name
        
        def __set_name__(self, owner, name):
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
        return isinstance(value, str) and '@' in value and '.' in value
    
    class BankAccount:
        """Банковский счет с различными уровнями инкапсуляции"""
        
        # Дескрипторы для валидации
        initial_balance = ValidatedAttribute(positive_number)
        
        def __init__(self, account_number, owner_name, initial_balance=0):
            # Публичные атрибуты
            self.account_number = account_number
            self.owner_name = owner_name
            
            # Защищенный атрибут (конвенция)
            self._balance = 0
            
            # Приватные атрибуты (name mangling)
            self.__pin = "1234"
            self.__transaction_history = []
            
            # Инициализация баланса через дескриптор
            self.initial_balance = initial_balance
            self._balance = initial_balance
        
        # Свойство (property) для контролируемого доступа к балансу
        @property
        def balance(self):
            """Получить баланс счета"""
            return self._balance
        
        @balance.setter
        def balance(self, value):
            """Установить баланс (с валидацией)"""
            if value < 0:
                raise ValueError("Баланс не может быть отрицательным")
            self._balance = value
        
        # Свойство только для чтения
        @property
        def transaction_count(self):
            """Количество транзакций (только чтение)"""
            return len(self.__transaction_history)
        
        # Свойство с getter, setter и deleter
        @property
        def pin(self):
            """PIN код (защищенный доступ)"""
            return "****"  # Никогда не возвращаем реальный PIN
        
        @pin.setter
        def pin(self, new_pin):
            """Установить новый PIN"""
            if not isinstance(new_pin, str) or len(new_pin) != 4 or not new_pin.isdigit():
                raise ValueError("PIN должен состоять из 4 цифр")
            self.__pin = new_pin
        
        @pin.deleter
        def pin(self):
            """Удалить PIN (сбросить на значение по умолчанию)"""
            self.__pin = "0000"
        
        # Приватные методы
        def __validate_pin(self, pin):
            """Проверить PIN код"""
            return pin == self.__pin
        
        def __log_transaction(self, transaction_type, amount, description=""):
            """Записать транзакцию в историю"""
            transaction = {
                'type': transaction_type,
                'amount': amount,
                'description': description,
                'timestamp': datetime.now(),
                'balance_after': self._balance
            }
            self.__transaction_history.append(transaction)
        
        # Защищенные методы (конвенция)
        def _calculate_interest(self, rate=0.02, days=30):
            """Рассчитать проценты (внутренний метод)"""
            return self._balance * rate * (days / 365)
        
        # Публичные методы
        def deposit(self, amount, description="Пополнение"):
            """Внести деньги на счет"""
            if amount <= 0:
                raise ValueError("Сумма депозита должна быть положительной")
            
            self._balance += amount
            self.__log_transaction("deposit", amount, description)
            return f"Депозит {amount} успешно внесен. Баланс: {self._balance}"
        
        def withdraw(self, amount, pin, description="Снятие"):
            """Снять деньги со счета"""
            if not self.__validate_pin(pin):
                raise ValueError("Неверный PIN код")
            
            if amount <= 0:
                raise ValueError("Сумма снятия должна быть положительной")
            
            if amount > self._balance:
                raise ValueError("Недостаточно средств на счете")
            
            self._balance -= amount
            self.__log_transaction("withdrawal", amount, description)
            return f"Снятие {amount} успешно выполнено. Баланс: {self._balance}"
        
        def transfer(self, amount, recipient_account, pin, description="Перевод"):
            """Перевести деньги на другой счет"""
            if not self.__validate_pin(pin):
                raise ValueError("Неверный PIN код")
            
            # Снимаем с текущего счета
            self.withdraw(amount, pin, f"Перевод на счет {recipient_account.account_number}")
            
            # Пополняем получателя
            recipient_account.deposit(amount, f"Перевод со счета {self.account_number}")
            
            return f"Перевод {amount} на счет {recipient_account.account_number} выполнен"
        
        def get_transaction_history(self, pin, limit=10):
            """Получить историю транзакций"""
            if not self.__validate_pin(pin):
                raise ValueError("Неверный PIN код")
            
            return self.__transaction_history[-limit:]
        
        def apply_interest(self):
            """Начислить проценты"""
            interest = self._calculate_interest()
            if interest > 0:
                self._balance += interest
                self.__log_transaction("interest", interest, "Начисление процентов")
                return f"Начислены проценты: {interest:.2f}. Баланс: {self._balance:.2f}"
            return "Проценты не начислены"
        
        # Специальные методы
        def __str__(self):
            return f"Счет {self.account_number} ({self.owner_name}): {self._balance:.2f}"
        
        def __repr__(self):
            return f"BankAccount('{self.account_number}', '{self.owner_name}', {self._balance})"
    
    # Тестирование инкапсуляции
    print("1. Создание банковских счетов:")
    
    account1 = BankAccount("123456789", "Алиса Иванова", 1000)
    account2 = BankAccount("987654321", "Боб Петров", 500)
    
    print(f"Счет 1: {account1}")
    print(f"Счет 2: {account2}")
    
    print("\n2. Работа со свойствами:")
    print(f"Баланс счета 1: {account1.balance}")
    print(f"Количество транзакций: {account1.transaction_count}")
    print(f"PIN код: {account1.pin}")  # Показывает ****
    
    print("\n3. Операции со счетом:")
    print(account1.deposit(500, "Зарплата"))
    print(account1.withdraw(200, "1234", "Покупки"))
    print(account1.apply_interest())
    
    print("\n4. Перевод между счетами:")
    print(account1.transfer(100, account2, "1234", "Долг"))
    print(f"Баланс после перевода - Счет 1: {account1.balance}, Счет 2: {account2.balance}")
    
    print("\n5. Работа с приватными методами:")
    # Попытка доступа к приватным атрибутам
    try:
        print(account1.__pin)  # Вызовет AttributeError
    except AttributeError as e:
        print(f"Ошибка доступа к приватному атрибуту: {e}")
    
    # Доступ через name mangling (не рекомендуется!)
    print(f"PIN через name mangling: {account1._BankAccount__pin}")
    
    print("\n6. Валидация через свойства:")
    try:
        account1.balance = -100  # Вызовет ValueError
    except ValueError as e:
        print(f"Ошибка валидации баланса: {e}")
    
    try:
        account1.pin = "123"  # Неправильный PIN
    except ValueError as e:
        print(f"Ошибка валидации PIN: {e}")
    
    print("\n7. История транзакций:")
    history = account1.get_transaction_history("1234", 5)
    for i, transaction in enumerate(history, 1):
        print(f"  {i}. {transaction['type']}: {transaction['amount']} "
              f"({transaction['timestamp'].strftime('%H:%M:%S')})")


def example_03_inheritance():
    """
    Пример 3: Наследование и полиморфизм
    
    Демонстрирует одиночное и множественное наследование,
    переопределение методов, super(), MRO и полиморфизм.
    """
    print("=== Пример 3: Наследование и полиморфизм ===")
    
    # Базовый класс
    class Vehicle:
        """Базовый класс транспортного средства"""
        
        def __init__(self, make, model, year, max_speed):
            self.make = make
            self.model = model
            self.year = year
            self.max_speed = max_speed
            self.current_speed = 0
            self.is_engine_on = False
        
        def start_engine(self):
            """Запустить двигатель"""
            self.is_engine_on = True
            return f"{self.make} {self.model}: двигатель запущен"
        
        def stop_engine(self):
            """Заглушить двигатель"""
            if self.current_speed == 0:
                self.is_engine_on = False
                return f"{self.make} {self.model}: двигатель заглушен"
            else:
                return "Остановите транспорт перед выключением двигателя"
        
        def accelerate(self, increment):
            """Ускориться"""
            if not self.is_engine_on:
                return "Сначала запустите двигатель"
            
            new_speed = min(self.current_speed + increment, self.max_speed)
            self.current_speed = new_speed
            return f"Скорость: {self.current_speed} км/ч"
        
        def brake(self, decrement):
            """Затормозить"""
            self.current_speed = max(0, self.current_speed - decrement)
            return f"Скорость: {self.current_speed} км/ч"
        
        def get_info(self):
            """Получить информацию о транспорте"""
            return f"{self.year} {self.make} {self.model} (макс. {self.max_speed} км/ч)"
        
        def __str__(self):
            return f"{self.make} {self.model} ({self.year})"
    
    # Одиночное наследование
    class Car(Vehicle):
        """Автомобиль"""
        
        def __init__(self, make, model, year, max_speed, doors, fuel_type):
            # Вызов конструктора родительского класса
            super().__init__(make, model, year, max_speed)
            self.doors = doors
            self.fuel_type = fuel_type
            self.fuel_level = 100  # Полный бак
        
        def accelerate(self, increment):
            """Переопределение метода ускорения с расходом топлива"""
            if self.fuel_level <= 0:
                return "Нет топлива!"
            
            result = super().accelerate(increment)
            self.fuel_level -= increment * 0.1  # Расход топлива
            self.fuel_level = max(0, self.fuel_level)
            return f"{result}, топливо: {self.fuel_level:.1f}%"
        
        def refuel(self, amount=100):
            """Заправиться"""
            self.fuel_level = min(100, self.fuel_level + amount)
            return f"Заправка завершена. Уровень топлива: {self.fuel_level:.1f}%"
        
        def get_info(self):
            """Расширенная информация об автомобиле"""
            base_info = super().get_info()
            return f"{base_info}, {self.doors} дверей, топливо: {self.fuel_type}"
    
    class Motorcycle(Vehicle):
        """Мотоцикл"""
        
        def __init__(self, make, model, year, max_speed, engine_volume):
            super().__init__(make, model, year, max_speed)
            self.engine_volume = engine_volume
            self.has_sidecar = False
        
        def wheelie(self):
            """Езда на заднем колесе"""
            if self.current_speed > 20:
                return f"{self.make} {self.model} делает wheelie!"
            else:
                return "Наберите скорость для wheelie"
        
        def add_sidecar(self):
            """Добавить коляску"""
            self.has_sidecar = True
            self.max_speed = int(self.max_speed * 0.8)  # Снижение максимальной скорости
            return "Коляска установлена"
        
        def get_info(self):
            base_info = super().get_info()
            sidecar_info = " с коляской" if self.has_sidecar else ""
            return f"{base_info}, объем двигателя: {self.engine_volume}л{sidecar_info}"
    
    # Миксины для множественного наследования
    class ElectricMixin:
        """Миксин для электрических транспортных средств"""
        
        def __init__(self, *args, battery_capacity=100, **kwargs):
            super().__init__(*args, **kwargs)
            self.battery_capacity = battery_capacity
            self.current_charge = battery_capacity
        
        def charge_battery(self, amount=None):
            """Зарядить батарею"""
            if amount is None:
                amount = self.battery_capacity - self.current_charge
            
            self.current_charge = min(self.battery_capacity, self.current_charge + amount)
            return f"Заряд батареи: {self.current_charge}/{self.battery_capacity}"
        
        def get_range(self):
            """Получить дальность поездки"""
            return self.current_charge * 3  # 3 км на единицу заряда
    
    class AutopilotMixin:
        """Миксин для автопилота"""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.autopilot_enabled = False
            self.autopilot_level = 1  # Уровень автопилота
        
        def enable_autopilot(self):
            """Включить автопилот"""
            if self.current_speed > 30:
                self.autopilot_enabled = True
                return f"Автопилот уровня {self.autopilot_level} включен"
            else:
                return "Наберите скорость выше 30 км/ч для включения автопилота"
        
        def disable_autopilot(self):
            """Выключить автопилот"""
            self.autopilot_enabled = False
            return "Автопилот выключен"
    
    class GPSMixin:
        """Миксин для GPS навигации"""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.current_location = "Неизвестно"
            self.destination = None
        
        def set_destination(self, destination):
            """Установить пункт назначения"""
            self.destination = destination
            return f"Маршрут построен до: {destination}"
        
        def get_navigation_info(self):
            """Получить навигационную информацию"""
            if self.destination:
                return f"Текущее местоположение: {self.current_location}, едем в: {self.destination}"
            return f"Текущее местоположение: {self.current_location}"
    
    # Множественное наследование
    class ElectricCar(Car, ElectricMixin, AutopilotMixin, GPSMixin):
        """Электрический автомобиль с множественным наследованием"""
        
        def __init__(self, make, model, year, max_speed, doors, battery_capacity=100):
            # Инициализация всех родительских классов
            super().__init__(
                make=make, 
                model=model, 
                year=year, 
                max_speed=max_speed, 
                doors=doors, 
                fuel_type="электричество",
                battery_capacity=battery_capacity
            )
            self.autopilot_level = 3  # Продвинутый автопилот
        
        def accelerate(self, increment):
            """Переопределение для электрического ускорения"""
            if self.current_charge <= 0:
                return "Батарея разряжена!"
            
            if not self.is_engine_on:
                return "Сначала запустите систему"
            
            new_speed = min(self.current_speed + increment, self.max_speed)
            self.current_speed = new_speed
            
            # Расход заряда
            self.current_charge -= increment * 0.05
            self.current_charge = max(0, self.current_charge)
            
            return f"Скорость: {self.current_speed} км/ч, заряд: {self.current_charge:.1f}%"
        
        def get_info(self):
            """Полная информация об электрокаре"""
            base_info = super(Car, self).get_info()  # Пропускаем Car.get_info()
            return (f"{base_info}, {self.doors} дверей, "
                   f"батарея: {self.battery_capacity}кВт·ч, "
                   f"автопилот: уровень {self.autopilot_level}")
    
    # Проверка MRO (Method Resolution Order)
    print("1. Method Resolution Order для ElectricCar:")
    for i, cls in enumerate(ElectricCar.__mro__):
        print(f"  {i + 1}. {cls.__name__}")
    
    print("\n2. Создание транспортных средств:")
    
    # Обычный автомобиль
    regular_car = Car("Toyota", "Camry", 2020, 200, 4, "бензин")
    print(f"Обычный автомобиль: {regular_car.get_info()}")
    
    # Мотоцикл
    motorcycle = Motorcycle("Harley-Davidson", "Sportster", 2021, 180, 1.2)
    print(f"Мотоцикл: {motorcycle.get_info()}")
    
    # Электрический автомобиль
    tesla = ElectricCar("Tesla", "Model S", 2022, 250, 4, 100)
    print(f"Электрокар: {tesla.get_info()}")
    
    print("\n3. Полиморфное использование:")
    
    vehicles = [regular_car, motorcycle, tesla]
    
    # Запуск всех транспортных средств
    print("Запуск транспорта:")
    for vehicle in vehicles:
        print(f"  {vehicle.start_engine()}")
    
    # Ускорение (полиморфный вызов)
    print("\nУскорение:")
    for vehicle in vehicles:
        print(f"  {vehicle}: {vehicle.accelerate(50)}")
    
    print("\n4. Специфичные возможности:")
    
    # Мотоцикл - wheelie
    print(motorcycle.wheelie())
    
    # Электрокар - зарядка и автопилот
    print(tesla.charge_battery(20))
    print(tesla.enable_autopilot())
    print(tesla.set_destination("Москва"))
    print(tesla.get_navigation_info())
    
    print("\n5. Переопределение методов:")
    print("Сравнение ускорения обычного и электрического автомобиля:")
    regular_car.start_engine()
    tesla.start_engine()
    
    print(f"  Обычный: {regular_car.accelerate(30)}")
    print(f"  Электрический: {tesla.accelerate(30)}")


def example_04_special_methods():
    """
    Пример 4: Специальные методы (Magic Methods)
    
    Демонстрирует основные специальные методы Python
    для настройки поведения объектов.
    """
    print("=== Пример 4: Специальные методы (Magic Methods) ===")
    
    class Money:
        """Класс для работы с деньгами"""
        
        # Поддерживаемые валюты
        EXCHANGE_RATES = {
            'USD': 1.0,
            'EUR': 0.85,
            'RUB': 75.0,
            'GBP': 0.73
        }
        
        def __init__(self, amount, currency='USD'):
            if currency not in self.EXCHANGE_RATES:
                raise ValueError(f"Неподдерживаемая валюта: {currency}")
            
            self.amount = float(amount)
            self.currency = currency
        
        # Строковое представление
        def __str__(self):
            """Пользовательское строковое представление"""
            return f"{self.amount:.2f} {self.currency}"
        
        def __repr__(self):
            """Формальное представление для отладки"""
            return f"Money({self.amount}, '{self.currency}')"
        
        # Арифметические операторы
        def __add__(self, other):
            """Сложение денег"""
            if isinstance(other, Money):
                # Конвертируем в USD, складываем, возвращаем в исходной валюте
                other_in_usd = other.to_usd()
                self_in_usd = self.to_usd()
                result_usd = self_in_usd + other_in_usd
                return Money(result_usd, 'USD').to_currency(self.currency)
            elif isinstance(other, (int, float)):
                return Money(self.amount + other, self.currency)
            else:
                return NotImplemented
        
        def __radd__(self, other):
            """Правостороннее сложение (для sum() и других функций)"""
            return self.__add__(other)
        
        def __sub__(self, other):
            """Вычитание денег"""
            if isinstance(other, Money):
                other_in_usd = other.to_usd()
                self_in_usd = self.to_usd()
                result_usd = self_in_usd - other_in_usd
                return Money(result_usd, 'USD').to_currency(self.currency)
            elif isinstance(other, (int, float)):
                return Money(self.amount - other, self.currency)
            else:
                return NotImplemented
        
        def __mul__(self, other):
            """Умножение на число"""
            if isinstance(other, (int, float)):
                return Money(self.amount * other, self.currency)
            else:
                return NotImplemented
        
        def __rmul__(self, other):
            """Правостороннее умножение"""
            return self.__mul__(other)
        
        def __truediv__(self, other):
            """Деление на число"""
            if isinstance(other, (int, float)):
                if other == 0:
                    raise ZeroDivisionError("Деление на ноль")
                return Money(self.amount / other, self.currency)
            else:
                return NotImplemented
        
        # Операторы сравнения
        def __eq__(self, other):
            """Равенство"""
            if isinstance(other, Money):
                return abs(self.to_usd() - other.to_usd()) < 0.01
            return False
        
        def __lt__(self, other):
            """Меньше"""
            if isinstance(other, Money):
                return self.to_usd() < other.to_usd()
            return NotImplemented
        
        def __le__(self, other):
            """Меньше или равно"""
            return self < other or self == other
        
        def __gt__(self, other):
            """Больше"""
            if isinstance(other, Money):
                return self.to_usd() > other.to_usd()
            return NotImplemented
        
        def __ge__(self, other):
            """Больше или равно"""
            return self > other or self == other
        
        def __ne__(self, other):
            """Не равно"""
            return not self == other
        
        # Хеширование
        def __hash__(self):
            """Хеш для использования в множествах и словарях"""
            return hash((round(self.to_usd(), 2), 'USD'))
        
        # Логические операции
        def __bool__(self):
            """Логическое значение (True если сумма > 0)"""
            return self.amount > 0
        
        # Длина
        def __len__(self):
            """Длина (количество символов в строковом представлении)"""
            return len(str(self))
        
        # Итерирование
        def __iter__(self):
            """Итерирование по цифрам суммы"""
            return iter(str(int(self.amount)))
        
        # Индексирование
        def __getitem__(self, index):
            """Получение цифры по индексу"""
            amount_str = str(int(self.amount))
            return amount_str[index]
        
        # Контекстный менеджер
        def __enter__(self):
            """Вход в контекстный менеджер"""
            print(f"Начало операции с {self}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            """Выход из контекстного менеджера"""
            if exc_type is None:
                print(f"Операция с {self} завершена успешно")
            else:
                print(f"Операция с {self} завершена с ошибкой: {exc_val}")
            return False
        
        # Вызов как функции
        def __call__(self, currency):
            """Конвертация валюты при вызове объекта как функции"""
            return self.to_currency(currency)
        
        # Дополнительные методы
        def to_usd(self):
            """Конвертировать в USD"""
            return self.amount / self.EXCHANGE_RATES[self.currency]
        
        def to_currency(self, target_currency):
            """Конвертировать в указанную валюту"""
            if target_currency not in self.EXCHANGE_RATES:
                raise ValueError(f"Неподдерживаемая валюта: {target_currency}")
            
            usd_amount = self.to_usd()
            target_amount = usd_amount * self.EXCHANGE_RATES[target_currency]
            return Money(target_amount, target_currency)
    
    # Тестирование специальных методов
    print("1. Создание объектов Money:")
    
    money1 = Money(100, 'USD')
    money2 = Money(85, 'EUR')
    money3 = Money(7500, 'RUB')
    
    print(f"Деньги 1: {money1}")
    print(f"Деньги 2: {money2}")
    print(f"Деньги 3: {money3}")
    print(f"Repr: {repr(money1)}")
    
    print("\n2. Арифметические операции:")
    
    # Сложение
    total = money1 + money2
    print(f"{money1} + {money2} = {total}")
    
    # Вычитание
    difference = money1 - Money(25, 'USD')
    print(f"{money1} - 25.00 USD = {difference}")
    
    # Умножение
    doubled = money1 * 2
    print(f"{money1} * 2 = {doubled}")
    
    # Деление
    half = money1 / 2
    print(f"{money1} / 2 = {half}")
    
    # Сумма списка
    money_list = [money1, money2, money3]
    total_sum = sum(money_list, Money(0))
    print(f"Сумма всех денег: {total_sum}")
    
    print("\n3. Операторы сравнения:")
    
    print(f"{money1} == {money2}: {money1 == money2}")
    print(f"{money1} > {money2}: {money1 > money2}")
    print(f"{money1} < {money3}: {money1 < money3}")
    
    # Сортировка
    sorted_money = sorted([money3, money1, money2])
    print(f"Отсортированные деньги: {[str(m) for m in sorted_money]}")
    
    print("\n4. Логические операции:")
    
    print(f"bool({money1}): {bool(money1)}")
    print(f"bool(Money(0)): {bool(Money(0))}")
    
    # Условие
    if money1:
        print(f"{money1} - положительная сумма")
    
    print("\n5. Длина и итерирование:")
    
    print(f"Длина {money1}: {len(money1)} символов")
    print(f"Цифры в {money1}: {list(money1)}")
    print(f"Первая цифра: {money1[0]}")
    
    print("\n6. Хеширование (для словарей и множеств):")
    
    money_set = {money1, money2, money3, Money(100, 'USD')}  # Дубликат
    print(f"Уникальные суммы: {len(money_set)}")
    
    money_dict = {money1: "Первые деньги", money2: "Вторые деньги"}
    print(f"Словарь с Money ключами: {len(money_dict)} элементов")
    
    print("\n7. Контекстный менеджер:")
    
    with money1 as m:
        result = m * 1.5
        print(f"Результат операции: {result}")
    
    print("\n8. Вызов как функции:")
    
    money_in_eur = money1('EUR')
    print(f"{money1} в евро: {money_in_eur}")
    
    money_in_rub = money1('RUB')
    print(f"{money1} в рублях: {money_in_rub}")
    
    print("\n9. Цепочка операций:")
    
    result = (money1 + money2) * 1.1 / 2
    print(f"({money1} + {money2}) * 1.1 / 2 = {result}")


def example_05_metaclasses():
    """
    Пример 5: Метаклассы и продвинутые техники
    
    Демонстрирует создание и использование метаклассов,
    синглтоны, ORM-подобные модели и автоматическую регистрацию.
    """
    print("=== Пример 5: Метаклассы и продвинутые техники ===")
    
    # Простой метакласс
    class DebugMeta(type):
        """Метакласс для отладки создания классов"""
        
        def __new__(mcs, name, bases, namespace, **kwargs):
            print(f"Создается класс: {name}")
            print(f"  Базовые классы: {[base.__name__ for base in bases]}")
            print(f"  Атрибуты: {list(namespace.keys())}")
            
            # Добавляем дополнительные атрибуты
            namespace['_created_at'] = datetime.now()
            namespace['_debug_info'] = f"Класс {name} создан метаклассом DebugMeta"
            
            return super().__new__(mcs, name, bases, namespace)
        
        def __init__(cls, name, bases, namespace, **kwargs):
            super().__init__(name, bases, namespace)
            print(f"Класс {name} инициализирован")
    
    # Метакласс для Singleton
    class SingletonMeta(type):
        """Метакласс для создания синглтонов"""
        
        _instances = {}
        
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
                print(f"Создан новый экземпляр {cls.__name__}")
            else:
                print(f"Возвращен существующий экземпляр {cls.__name__}")
            return cls._instances[cls]
    
    # Метакласс для автоматической регистрации
    class RegistryMeta(type):
        """Метакласс для автоматической регистрации классов"""
        
        registry = {}
        
        def __new__(mcs, name, bases, namespace, **kwargs):
            cls = super().__new__(mcs, name, bases, namespace)
            
            # Автоматическая регистрация
            if name != 'BaseModel':  # Не регистрируем базовый класс
                mcs.registry[name.lower()] = cls
                print(f"Класс {name} автоматически зарегистрирован")
            
            return cls
        
        @classmethod
        def get_class(mcs, name):
            """Получить класс по имени"""
            return mcs.registry.get(name.lower())
        
        @classmethod
        def list_classes(mcs):
            """Список всех зарегистрированных классов"""
            return list(mcs.registry.keys())
    
    # ORM-подобный метакласс
    class ORMMeta(type):
        """Метакласс для создания ORM-подобных моделей"""
        
        def __new__(mcs, name, bases, namespace, **kwargs):
            # Собираем поля модели
            fields = {}
            for key, value in list(namespace.items()):
                if isinstance(value, Field):
                    fields[key] = value
                    value.name = key
                    # Заменяем дескрипторы поля на дескрипторы модели
                    namespace[key] = ModelAttribute(key, value)
            
            namespace['_fields'] = fields
            namespace['_table_name'] = kwargs.get('table_name', name.lower())
            
            cls = super().__new__(mcs, name, bases, namespace)
            return cls
    
    # Дескрипторы для ORM
    class Field:
        """Базовый класс поля модели"""
        
        def __init__(self, field_type, required=True, default=None):
            self.field_type = field_type
            self.required = required
            self.default = default
            self.name = None
    
    class ModelAttribute:
        """Дескриптор для атрибутов модели"""
        
        def __init__(self, name, field):
            self.name = name
            self.field = field
        
        def __get__(self, instance, owner):
            if instance is None:
                return self.field
            return instance._data.get(self.name, self.field.default)
        
        def __set__(self, instance, value):
            # Валидация типа
            if not isinstance(value, self.field.field_type) and value is not None:
                raise TypeError(f"Поле {self.name} должно быть типа {self.field.field_type.__name__}")
            instance._data[self.name] = value
    
    # Классы с метаклассами
    class DebugClass(metaclass=DebugMeta):
        """Класс с отладочным метаклассом"""
        
        def __init__(self, value):
            self.value = value
        
        def get_debug_info(self):
            return self._debug_info
    
    class DatabaseConnection(metaclass=SingletonMeta):
        """Подключение к базе данных (синглтон)"""
        
        def __init__(self, host='localhost', port=5432):
            if hasattr(self, 'initialized'):
                return
            
            self.host = host
            self.port = port
            self.initialized = True
            print(f"Подключение к {host}:{port} инициализировано")
        
        def query(self, sql):
            return f"Выполнен запрос: {sql} на {self.host}:{self.port}"
    
    class BaseModel(metaclass=RegistryMeta):
        """Базовая модель для автоматической регистрации"""
        
        def __init__(self, **kwargs):
            self.data = kwargs
        
        def __str__(self):
            return f"{self.__class__.__name__}({self.data})"
    
    class User(BaseModel):
        """Пользователь"""
        
        def __init__(self, name, email, **kwargs):
            super().__init__(name=name, email=email, **kwargs)
    
    class Product(BaseModel):
        """Продукт"""
        
        def __init__(self, title, price, **kwargs):
            super().__init__(title=title, price=price, **kwargs)
    
    # ORM модель
    class ORMModel(metaclass=ORMMeta):
        """Базовая ORM модель"""
        
        def __init__(self, **kwargs):
            self._data = {}
            
            # Инициализация полей
            for name, field in self._fields.items():
                if name in kwargs:
                    setattr(self, name, kwargs[name])
                elif field.required and field.default is None:
                    raise ValueError(f"Поле {name} обязательно")
                else:
                    setattr(self, name, field.default)
        
        def to_dict(self):
            """Преобразовать в словарь"""
            return self._data.copy()
        
        def __str__(self):
            return f"{self.__class__.__name__}({self.to_dict()})"
    
    class Person(ORMModel, table_name='people'):
        """Модель человека"""
        
        name = Field(str, required=True)
        age = Field(int, required=True)
        email = Field(str, required=False, default="")
        salary = Field(float, required=False, default=0.0)
    
    # Тестирование метаклассов
    print("1. Отладочный метакласс:")
    
    debug_obj = DebugClass("test")
    print(f"Отладочная информация: {debug_obj.get_debug_info()}")
    print(f"Время создания класса: {debug_obj._created_at}")
    
    print("\n2. Singleton метакласс:")
    
    # Первое создание
    db1 = DatabaseConnection("server1", 5432)
    
    # Второе создание - вернется тот же объект
    db2 = DatabaseConnection("server2", 3306)  # Параметры игнорируются
    
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1 host: {db1.host}, db2 host: {db2.host}")
    
    print("\n3. Автоматическая регистрация:")
    
    print(f"Зарегистрированные классы: {RegistryMeta.list_classes()}")
    
    # Получение класса по имени
    UserClass = RegistryMeta.get_class('user')
    ProductClass = RegistryMeta.get_class('product')
    
    if UserClass:
        user = UserClass("Алиса", "alice@example.com")
        print(f"Созданный пользователь: {user}")
    
    if ProductClass:
        product = ProductClass("Laptop", 1000)
        print(f"Созданный продукт: {product}")
    
    print("\n4. ORM метакласс:")
    
    # Создание модели
    person = Person(name="Боб", age=30, email="bob@example.com", salary=50000.0)
    print(f"Созданная персона: {person}")
    print(f"Данные персоны: {person.to_dict()}")
    print(f"Имя таблицы: {Person._table_name}")
    print(f"Поля модели: {list(Person._fields.keys())}")
    
    # Валидация типов
    try:
        person.age = "тридцать"  # Неправильный тип
    except TypeError as e:
        print(f"Ошибка валидации: {e}")
    
    # Доступ к полям
    print(f"Имя: {person.name}")
    print(f"Возраст: {person.age}")
    
    print("\n5. Создание метакласса на лету:")
    
    # Создание метакласса с помощью type()
    def add_methods(cls):
        """Функция для добавления методов в класс"""
        def get_description(self):
            return f"Это экземпляр класса {self.__class__.__name__}"
        
        cls.get_description = get_description
        return cls
    
    # Метакласс, добавляющий методы
    DynamicMeta = type('DynamicMeta', (type,), {
        '__new__': lambda mcs, name, bases, namespace: add_methods(
            super(DynamicMeta, mcs).__new__(mcs, name, bases, namespace)
        )
    })
    
    # Класс с динамическим метаклассом
    class DynamicClass(metaclass=DynamicMeta):
        def __init__(self, value):
            self.value = value
    
    dynamic_obj = DynamicClass("test")
    print(f"Динамический метод: {dynamic_obj.get_description()}")
    
    print("\n6. Проверка атрибутов метакласса:")
    
    print(f"Тип Person: {type(Person)}")
    print(f"MRO Person: {[cls.__name__ for cls in Person.__mro__]}")
    print(f"Атрибуты Person: {[attr for attr in dir(Person) if not attr.startswith('__')]}")


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Основы классов и объектов", example_01_basic_classes),
        ("Инкапсуляция и уровни доступа", example_02_encapsulation),
        ("Наследование и полиморфизм", example_03_inheritance),
        ("Специальные методы", example_04_special_methods),
        ("Метаклассы и продвинутые техники", example_05_metaclasses),
    ]
    
    print("🏗️ Примеры: Объектно-ориентированное программирование в Python")
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