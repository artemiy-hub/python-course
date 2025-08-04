#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Объектно-ориентированное программирование в Python

Этот файл содержит практические упражнения для закрепления знаний:
- Создание классов и объектов
- Инкапсуляция и уровни доступа
- Наследование и полиморфизм
- Абстракция и интерфейсы
- Специальные методы
- Метаклассы и дескрипторы

Каждое упражнение включает:
- Подробное описание задачи
- Примеры использования
- Решение с комментариями
"""

import abc
import json
import uuid
from datetime import datetime, timedelta
from typing import Protocol, List, Dict, Optional, Any, Type, runtime_checkable
from collections import defaultdict
import weakref
import functools


def exercise_01_library_management_system():
    """
    Упражнение 1: Система управления библиотекой
    
    Задача:
    Создайте полную систему управления библиотекой с использованием ООП:
    1. Базовый класс Item (книги, журналы, DVD)
    2. Классы Book, Magazine, DVD с наследованием
    3. Класс Member для читателей
    4. Класс Library для управления
    5. Инкапсуляция с защищенными/приватными атрибутами
    6. Специальные методы (__str__, __eq__, __hash__)
    7. Валидация данных через properties
    """
    print("=== Упражнение 1: Система управления библиотекой ===")
    
    # ЗАДАЧА: Реализуйте систему управления библиотекой
    
    # РЕШЕНИЕ:
    
    from enum import Enum
    from abc import ABC, abstractmethod
    
    class ItemStatus(Enum):
        """Статус элементов библиотеки"""
        AVAILABLE = "available"
        BORROWED = "borrowed"
        RESERVED = "reserved"
        MAINTENANCE = "maintenance"
        LOST = "lost"
    
    class Item(ABC):
        """Абстрактный базовый класс для элементов библиотеки"""
        
        def __init__(self, item_id: str, title: str, publisher: str, year: int):
            self._item_id = item_id
            self._title = title
            self._publisher = publisher
            self._year = year
            self._status = ItemStatus.AVAILABLE
            self._borrowed_by = None
            self._borrowed_date = None
            self._due_date = None
        
        # Properties для контролируемого доступа
        @property
        def item_id(self):
            return self._item_id
        
        @property
        def title(self):
            return self._title
        
        @title.setter
        def title(self, value):
            if not isinstance(value, str) or len(value.strip()) == 0:
                raise ValueError("Название не может быть пустым")
            self._title = value.strip()
        
        @property
        def year(self):
            return self._year
        
        @year.setter
        def year(self, value):
            current_year = datetime.now().year
            if not isinstance(value, int) or value < 1000 or value > current_year + 5:
                raise ValueError(f"Год должен быть между 1000 и {current_year + 5}")
            self._year = value
        
        @property
        def status(self):
            return self._status
        
        @property
        def is_available(self):
            return self._status == ItemStatus.AVAILABLE
        
        def borrow(self, member, days=14):
            """Выдать элемент читателю"""
            if not self.is_available:
                raise ValueError(f"Элемент недоступен для выдачи: {self._status.value}")
            
            self._status = ItemStatus.BORROWED
            self._borrowed_by = member
            self._borrowed_date = datetime.now()
            self._due_date = self._borrowed_date + timedelta(days=days)
            
            return f"Элемент '{self.title}' выдан {member.name} до {self._due_date.strftime('%d.%m.%Y')}"
        
        def return_item(self):
            """Вернуть элемент"""
            if self._status != ItemStatus.BORROWED:
                raise ValueError("Элемент не был выдан")
            
            member = self._borrowed_by
            self._status = ItemStatus.AVAILABLE
            self._borrowed_by = None
            self._borrowed_date = None
            self._due_date = None
            
            return f"Элемент '{self.title}' возвращен от {member.name}"
        
        def is_overdue(self):
            """Проверить просрочку"""
            if self._status == ItemStatus.BORROWED and self._due_date:
                return datetime.now() > self._due_date
            return False
        
        @abstractmethod
        def get_loan_period(self):
            """Абстрактный метод для получения срока выдачи"""
            pass
        
        @abstractmethod
        def get_category(self):
            """Абстрактный метод для получения категории"""
            pass
        
        def __str__(self):
            return f"{self.get_category()}: {self.title} ({self.year})"
        
        def __repr__(self):
            return f"{self.__class__.__name__}('{self._item_id}', '{self.title}', {self.year})"
        
        def __eq__(self, other):
            if isinstance(other, Item):
                return self._item_id == other._item_id
            return False
        
        def __hash__(self):
            return hash(self._item_id)
    
    class Book(Item):
        """Книга"""
        
        def __init__(self, item_id: str, title: str, author: str, publisher: str, 
                     year: int, isbn: str, pages: int):
            super().__init__(item_id, title, publisher, year)
            self.author = author
            self.isbn = isbn
            self.pages = pages
        
        def get_loan_period(self):
            return 21  # 3 недели для книг
        
        def get_category(self):
            return "Книга"
        
        def __str__(self):
            return f"Книга: {self.title} - {self.author} ({self.year})"
    
    class Magazine(Item):
        """Журнал"""
        
        def __init__(self, item_id: str, title: str, publisher: str, 
                     year: int, issue_number: int, month: str):
            super().__init__(item_id, title, publisher, year)
            self.issue_number = issue_number
            self.month = month
        
        def get_loan_period(self):
            return 7  # 1 неделя для журналов
        
        def get_category(self):
            return "Журнал"
        
        def __str__(self):
            return f"Журнал: {self.title} №{self.issue_number} ({self.month} {self.year})"
    
    class DVD(Item):
        """DVD диск"""
        
        def __init__(self, item_id: str, title: str, director: str, publisher: str,
                     year: int, duration: int, genre: str):
            super().__init__(item_id, title, publisher, year)
            self.director = director
            self.duration = duration
            self.genre = genre
        
        def get_loan_period(self):
            return 3  # 3 дня для DVD
        
        def get_category(self):
            return "DVD"
        
        def __str__(self):
            return f"DVD: {self.title} - {self.director} ({self.year}, {self.genre})"
    
    class Member:
        """Читатель библиотеки"""
        
        def __init__(self, member_id: str, name: str, email: str, phone: str):
            self.member_id = member_id
            self._name = name
            self._email = email
            self._phone = phone
            self._borrowed_items = []
            self._registration_date = datetime.now()
            self._fine_amount = 0.0
        
        @property
        def name(self):
            return self._name
        
        @name.setter
        def name(self, value):
            if not isinstance(value, str) or len(value.strip()) < 2:
                raise ValueError("Имя должно содержать минимум 2 символа")
            self._name = value.strip()
        
        @property
        def email(self):
            return self._email
        
        @email.setter
        def email(self, value):
            if not isinstance(value, str) or '@' not in value:
                raise ValueError("Некорректный email адрес")
            self._email = value
        
        @property
        def borrowed_items(self):
            return self._borrowed_items.copy()
        
        @property
        def fine_amount(self):
            return self._fine_amount
        
        def add_borrowed_item(self, item):
            """Добавить взятый элемент"""
            if item not in self._borrowed_items:
                self._borrowed_items.append(item)
        
        def remove_borrowed_item(self, item):
            """Удалить возвращенный элемент"""
            if item in self._borrowed_items:
                self._borrowed_items.remove(item)
        
        def add_fine(self, amount):
            """Добавить штраф"""
            self._fine_amount += amount
        
        def pay_fine(self, amount):
            """Оплатить штраф"""
            if amount > self._fine_amount:
                raise ValueError("Сумма оплаты превышает размер штрафа")
            self._fine_amount -= amount
            return f"Оплачен штраф: {amount}. Остаток: {self._fine_amount}"
        
        def can_borrow(self, max_items=5):
            """Проверить возможность взять еще книги"""
            return len(self._borrowed_items) < max_items and self._fine_amount == 0
        
        def __str__(self):
            return f"Читатель: {self.name} (ID: {self.member_id})"
        
        def __repr__(self):
            return f"Member('{self.member_id}', '{self.name}')"
        
        def __eq__(self, other):
            if isinstance(other, Member):
                return self.member_id == other.member_id
            return False
        
        def __hash__(self):
            return hash(self.member_id)
    
    class Library:
        """Система управления библиотекой"""
        
        def __init__(self, name: str):
            self.name = name
            self._items = {}  # item_id -> Item
            self._members = {}  # member_id -> Member
            self._transactions = []  # История операций
            self._fine_rate = 1.0  # Штраф за день просрочки
        
        def add_item(self, item: Item):
            """Добавить элемент в библиотеку"""
            if item.item_id in self._items:
                raise ValueError(f"Элемент с ID {item.item_id} уже существует")
            
            self._items[item.item_id] = item
            self._log_transaction("ADD_ITEM", f"Добавлен {item}")
            return f"Элемент добавлен: {item}"
        
        def add_member(self, member: Member):
            """Добавить читателя"""
            if member.member_id in self._members:
                raise ValueError(f"Читатель с ID {member.member_id} уже существует")
            
            self._members[member.member_id] = member
            self._log_transaction("ADD_MEMBER", f"Зарегистрирован {member}")
            return f"Читатель зарегистрирован: {member}"
        
        def borrow_item(self, item_id: str, member_id: str):
            """Выдать элемент читателю"""
            item = self._items.get(item_id)
            member = self._members.get(member_id)
            
            if not item:
                raise ValueError(f"Элемент с ID {item_id} не найден")
            if not member:
                raise ValueError(f"Читатель с ID {member_id} не найден")
            
            if not member.can_borrow():
                raise ValueError(f"Читатель {member.name} не может взять книги (превышен лимит или есть штрафы)")
            
            result = item.borrow(member, item.get_loan_period())
            member.add_borrowed_item(item)
            
            self._log_transaction("BORROW", f"{member.name} взял {item.title}")
            return result
        
        def return_item(self, item_id: str):
            """Вернуть элемент"""
            item = self._items.get(item_id)
            if not item:
                raise ValueError(f"Элемент с ID {item_id} не найден")
            
            if item.status != ItemStatus.BORROWED:
                raise ValueError("Элемент не был выдан")
            
            member = item._borrowed_by
            
            # Проверяем просрочку
            if item.is_overdue():
                overdue_days = (datetime.now() - item._due_date).days
                fine = overdue_days * self._fine_rate
                member.add_fine(fine)
                self._log_transaction("FINE", f"Штраф {fine} для {member.name} за просрочку {overdue_days} дней")
            
            result = item.return_item()
            member.remove_borrowed_item(item)
            
            self._log_transaction("RETURN", f"{member.name} вернул {item.title}")
            return result
        
        def search_items(self, query: str, category: str = None):
            """Поиск элементов"""
            results = []
            query_lower = query.lower()
            
            for item in self._items.values():
                if category and item.get_category() != category:
                    continue
                
                if (query_lower in item.title.lower() or 
                    (hasattr(item, 'author') and query_lower in item.author.lower()) or
                    (hasattr(item, 'director') and query_lower in item.director.lower())):
                    results.append(item)
            
            return results
        
        def get_overdue_items(self):
            """Получить просроченные элементы"""
            overdue = []
            for item in self._items.values():
                if item.is_overdue():
                    overdue.append(item)
            return overdue
        
        def get_member_info(self, member_id: str):
            """Получить информацию о читателе"""
            member = self._members.get(member_id)
            if not member:
                raise ValueError(f"Читатель с ID {member_id} не найден")
            
            info = {
                'member': member,
                'borrowed_count': len(member.borrowed_items),
                'borrowed_items': member.borrowed_items,
                'fine_amount': member.fine_amount,
                'can_borrow': member.can_borrow()
            }
            return info
        
        def get_statistics(self):
            """Получить статистику библиотеки"""
            total_items = len(self._items)
            available_items = sum(1 for item in self._items.values() if item.is_available)
            borrowed_items = total_items - available_items
            total_members = len(self._members)
            overdue_items = len(self.get_overdue_items())
            
            return {
                'total_items': total_items,
                'available_items': available_items,
                'borrowed_items': borrowed_items,
                'total_members': total_members,
                'overdue_items': overdue_items,
                'transactions_count': len(self._transactions)
            }
        
        def _log_transaction(self, transaction_type: str, description: str):
            """Записать транзакцию"""
            transaction = {
                'timestamp': datetime.now(),
                'type': transaction_type,
                'description': description
            }
            self._transactions.append(transaction)
        
        def __str__(self):
            stats = self.get_statistics()
            return (f"Библиотека '{self.name}': {stats['total_items']} элементов, "
                   f"{stats['total_members']} читателей")
    
    # Тестирование системы библиотеки
    print("1. Создание библиотеки и добавление элементов:")
    
    library = Library("Центральная библиотека")
    
    # Добавляем книги
    book1 = Book("B001", "1984", "Джордж Оруэлл", "Прогресс", 1949, "978-0-452-28423-4", 328)
    book2 = Book("B002", "Мастер и Маргарита", "Михаил Булгаков", "АСТ", 1967, "978-5-17-123456-7", 480)
    
    # Добавляем журналы
    magazine1 = Magazine("M001", "National Geographic", "National Geographic Society", 2023, 5, "Май")
    
    # Добавляем DVD
    dvd1 = DVD("D001", "Матрица", "Вачовски", "Warner Bros", 1999, 136, "Фантастика")
    
    for item in [book1, book2, magazine1, dvd1]:
        print(library.add_item(item))
    
    print("\n2. Регистрация читателей:")
    
    member1 = Member("M001", "Алиса Иванова", "alice@example.com", "+7-900-123-4567")
    member2 = Member("M002", "Боб Петров", "bob@example.com", "+7-900-987-6543")
    
    for member in [member1, member2]:
        print(library.add_member(member))
    
    print("\n3. Выдача книг:")
    
    print(library.borrow_item("B001", "M001"))
    print(library.borrow_item("M001", "M001"))
    print(library.borrow_item("D001", "M002"))
    
    print("\n4. Информация о читателях:")
    
    for member_id in ["M001", "M002"]:
        info = library.get_member_info(member_id)
        print(f"\nЧитатель: {info['member'].name}")
        print(f"  Взято книг: {info['borrowed_count']}")
        print(f"  Штрафы: {info['fine_amount']}")
        print(f"  Может брать книги: {info['can_borrow']}")
    
    print("\n5. Поиск элементов:")
    
    search_results = library.search_items("Матрица")
    print(f"Результаты поиска 'Матрица': {len(search_results)} элементов")
    for item in search_results:
        print(f"  {item}")
    
    print("\n6. Возврат книг:")
    
    print(library.return_item("B001"))
    print(library.return_item("M001"))
    
    print("\n7. Статистика библиотеки:")
    
    stats = library.get_statistics()
    print(f"Библиотека: {library}")
    print(f"Доступно элементов: {stats['available_items']}")
    print(f"Выдано элементов: {stats['borrowed_items']}")
    print(f"Просроченных: {stats['overdue_items']}")
    
    print("\n✅ Упражнение 1 завершено!")


def exercise_02_game_development_framework():
    """
    Упражнение 2: Фреймворк для разработки игр
    
    Задача:
    Создайте объектно-ориентированный фреймворк для простых игр:
    1. Абстрактные классы GameObject, Component
    2. Систему компонентов (ECS pattern)
    3. Множественное наследование и миксины
    4. Метаклассы для автоматической регистрации
    5. Специальные методы для сравнения и итерации
    6. Протоколы для различных интерфейсов
    """
    print("=== Упражнение 2: Фреймворк для разработки игр ===")
    
    # ЗАДАЧА: Реализуйте игровой фреймворк
    
    # РЕШЕНИЕ:
    
    from typing import Protocol, Set, Type
    import weakref
    import math
    
    # Метакласс для автоматической регистрации компонентов
    class ComponentMeta(type):
        """Метакласс для автоматической регистрации компонентов"""
        
        registry: Dict[str, Type] = {}
        
        def __new__(mcs, name, bases, namespace, **kwargs):
            cls = super().__new__(mcs, name, bases, namespace)
            
            # Регистрируем только не абстрактные компоненты
            if not getattr(cls, '__abstract__', False) and name != 'Component':
                mcs.registry[name.lower()] = cls
                print(f"Компонент {name} автоматически зарегистрирован")
            
            return cls
        
        @classmethod
        def get_component_type(mcs, name: str):
            """Получить тип компонента по имени"""
            return mcs.registry.get(name.lower())
        
        @classmethod
        def list_components(mcs):
            """Список всех зарегистрированных компонентов"""
            return list(mcs.registry.keys())
    
    # Протоколы для различных интерфейсов
    @runtime_checkable
    class Drawable(Protocol):
        """Протокол для объектов, которые можно нарисовать"""
        
        def draw(self) -> str:
            ...
        
        def get_render_info(self) -> Dict[str, Any]:
            ...
    
    @runtime_checkable
    class Updatable(Protocol):
        """Протокол для объектов, которые можно обновлять"""
        
        def update(self, delta_time: float) -> None:
            ...
    
    @runtime_checkable
    class Collidable(Protocol):
        """Протокол для объектов с коллизией"""
        
        def get_bounds(self) -> Dict[str, float]:
            ...
        
        def check_collision(self, other: 'Collidable') -> bool:
            ...
    
    # Базовые классы
    class Vector2D:
        """Двумерный вектор"""
        
        def __init__(self, x: float = 0, y: float = 0):
            self.x = x
            self.y = y
        
        def __add__(self, other):
            if isinstance(other, Vector2D):
                return Vector2D(self.x + other.x, self.y + other.y)
            return NotImplemented
        
        def __sub__(self, other):
            if isinstance(other, Vector2D):
                return Vector2D(self.x - other.x, self.y - other.y)
            return NotImplemented
        
        def __mul__(self, scalar):
            if isinstance(scalar, (int, float)):
                return Vector2D(self.x * scalar, self.y * scalar)
            return NotImplemented
        
        def __rmul__(self, scalar):
            return self.__mul__(scalar)
        
        def __truediv__(self, scalar):
            if isinstance(scalar, (int, float)) and scalar != 0:
                return Vector2D(self.x / scalar, self.y / scalar)
            return NotImplemented
        
        def magnitude(self):
            """Длина вектора"""
            return math.sqrt(self.x ** 2 + self.y ** 2)
        
        def normalize(self):
            """Нормализованный вектор"""
            mag = self.magnitude()
            if mag > 0:
                return self / mag
            return Vector2D(0, 0)
        
        def distance_to(self, other):
            """Расстояние до другого вектора"""
            return (self - other).magnitude()
        
        def __str__(self):
            return f"Vector2D({self.x:.2f}, {self.y:.2f})"
        
        def __repr__(self):
            return f"Vector2D({self.x}, {self.y})"
        
        def __eq__(self, other):
            if isinstance(other, Vector2D):
                return abs(self.x - other.x) < 0.001 and abs(self.y - other.y) < 0.001
            return False
        
        def __hash__(self):
            return hash((round(self.x, 3), round(self.y, 3)))
    
    class Component(ABC, metaclass=ComponentMeta):
        """Абстрактный базовый класс компонента"""
        
        __abstract__ = True
        
        def __init__(self):
            self.game_object = None
            self.enabled = True
        
        def attach_to(self, game_object):
            """Прикрепить к игровому объекту"""
            self.game_object = game_object
        
        def detach(self):
            """Открепить от игрового объекта"""
            self.game_object = None
        
        @abstractmethod
        def initialize(self):
            """Инициализация компонента"""
            pass
        
        def __str__(self):
            return f"{self.__class__.__name__}(enabled={self.enabled})"
    
    # Конкретные компоненты
    class Transform(Component):
        """Компонент позиции и трансформации"""
        
        def __init__(self, position: Vector2D = None, rotation: float = 0, scale: Vector2D = None):
            super().__init__()
            self.position = position or Vector2D(0, 0)
            self.rotation = rotation
            self.scale = scale or Vector2D(1, 1)
        
        def initialize(self):
            pass
        
        def move(self, direction: Vector2D):
            """Переместить объект"""
            self.position += direction
        
        def rotate(self, angle: float):
            """Повернуть объект"""
            self.rotation += angle
            self.rotation %= 360
        
        def __str__(self):
            return f"Transform(pos={self.position}, rot={self.rotation:.1f}°)"
    
    class Renderer(Component):
        """Компонент отрисовки"""
        
        def __init__(self, sprite: str, color: str = "white", layer: int = 0):
            super().__init__()
            self.sprite = sprite
            self.color = color
            self.layer = layer
            self.visible = True
        
        def initialize(self):
            pass
        
        def draw(self) -> str:
            """Отрисовать объект"""
            if not self.visible or not self.enabled:
                return ""
            
            transform = self.game_object.get_component(Transform)
            if transform:
                return (f"Рисуем {self.sprite} ({self.color}) в позиции {transform.position} "
                       f"с поворотом {transform.rotation}° на слое {self.layer}")
            return f"Рисуем {self.sprite} ({self.color})"
        
        def get_render_info(self) -> Dict[str, Any]:
            """Информация для отрисовки"""
            transform = self.game_object.get_component(Transform)
            return {
                'sprite': self.sprite,
                'color': self.color,
                'layer': self.layer,
                'visible': self.visible,
                'position': transform.position if transform else Vector2D(0, 0),
                'rotation': transform.rotation if transform else 0
            }
    
    class Rigidbody(Component):
        """Компонент физики"""
        
        def __init__(self, mass: float = 1.0, drag: float = 0.1):
            super().__init__()
            self.mass = mass
            self.velocity = Vector2D(0, 0)
            self.acceleration = Vector2D(0, 0)
            self.drag = drag
            self.gravity_scale = 1.0
        
        def initialize(self):
            pass
        
        def add_force(self, force: Vector2D):
            """Добавить силу"""
            self.acceleration += force / self.mass
        
        def update(self, delta_time: float):
            """Обновить физику"""
            if not self.enabled:
                return
            
            # Применяем гравитацию
            gravity = Vector2D(0, -9.81 * self.gravity_scale)
            self.acceleration += gravity
            
            # Обновляем скорость
            self.velocity += self.acceleration * delta_time
            
            # Применяем сопротивление
            self.velocity *= (1.0 - self.drag * delta_time)
            
            # Обновляем позицию
            transform = self.game_object.get_component(Transform)
            if transform:
                transform.move(self.velocity * delta_time)
            
            # Сбрасываем ускорение
            self.acceleration = Vector2D(0, 0)
    
    class Collider(Component):
        """Компонент коллизии"""
        
        def __init__(self, width: float, height: float, is_trigger: bool = False):
            super().__init__()
            self.width = width
            self.height = height
            self.is_trigger = is_trigger
            self.collision_callbacks = []
        
        def initialize(self):
            pass
        
        def get_bounds(self) -> Dict[str, float]:
            """Получить границы коллайдера"""
            transform = self.game_object.get_component(Transform)
            if transform:
                pos = transform.position
                return {
                    'left': pos.x - self.width / 2,
                    'right': pos.x + self.width / 2,
                    'top': pos.y + self.height / 2,
                    'bottom': pos.y - self.height / 2
                }
            return {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
        
        def check_collision(self, other: 'Collider') -> bool:
            """Проверить коллизию с другим коллайдером"""
            bounds1 = self.get_bounds()
            bounds2 = other.get_bounds()
            
            return (bounds1['left'] < bounds2['right'] and
                    bounds1['right'] > bounds2['left'] and
                    bounds1['bottom'] < bounds2['top'] and
                    bounds1['top'] > bounds2['bottom'])
        
        def add_collision_callback(self, callback):
            """Добавить callback для коллизии"""
            self.collision_callbacks.append(callback)
    
    # Миксины для дополнительной функциональности
    class HealthMixin:
        """Миксин для здоровья"""
        
        def __init__(self, *args, max_health: float = 100, **kwargs):
            super().__init__(*args, **kwargs)
            self.max_health = max_health
            self.current_health = max_health
            self.is_alive = True
        
        def take_damage(self, damage: float):
            """Получить урон"""
            self.current_health = max(0, self.current_health - damage)
            if self.current_health <= 0:
                self.is_alive = False
                self.on_death()
        
        def heal(self, amount: float):
            """Восстановить здоровье"""
            self.current_health = min(self.max_health, self.current_health + amount)
        
        def get_health_percentage(self) -> float:
            """Процент здоровья"""
            return self.current_health / self.max_health
        
        def on_death(self):
            """Обработка смерти"""
            print(f"{self} умер!")
    
    class InventoryMixin:
        """Миксин для инвентаря"""
        
        def __init__(self, *args, inventory_size: int = 10, **kwargs):
            super().__init__(*args, **kwargs)
            self.inventory_size = inventory_size
            self.inventory = []
        
        def add_item(self, item):
            """Добавить предмет"""
            if len(self.inventory) < self.inventory_size:
                self.inventory.append(item)
                return True
            return False
        
        def remove_item(self, item):
            """Удалить предмет"""
            if item in self.inventory:
                self.inventory.remove(item)
                return True
            return False
        
        def has_item(self, item) -> bool:
            """Проверить наличие предмета"""
            return item in self.inventory
        
        def get_inventory_info(self):
            """Информация об инвентаре"""
            return {
                'items': self.inventory.copy(),
                'count': len(self.inventory),
                'free_slots': self.inventory_size - len(self.inventory)
            }
    
    # Главный класс игрового объекта
    class GameObject:
        """Игровой объект"""
        
        _id_counter = 0
        
        def __init__(self, name: str):
            GameObject._id_counter += 1
            self.id = GameObject._id_counter
            self.name = name
            self.active = True
            self.tag = ""
            self._components = {}
            self._component_instances = []
        
        def add_component(self, component: Component):
            """Добавить компонент"""
            component_type = type(component)
            
            if component_type in self._components:
                raise ValueError(f"Компонент {component_type.__name__} уже добавлен")
            
            self._components[component_type] = component
            self._component_instances.append(component)
            component.attach_to(self)
            component.initialize()
            
            return component
        
        def remove_component(self, component_type: Type[Component]):
            """Удалить компонент"""
            component = self._components.get(component_type)
            if component:
                component.detach()
                del self._components[component_type]
                self._component_instances.remove(component)
                return component
            return None
        
        def get_component(self, component_type: Type[Component]):
            """Получить компонент"""
            return self._components.get(component_type)
        
        def has_component(self, component_type: Type[Component]) -> bool:
            """Проверить наличие компонента"""
            return component_type in self._components
        
        def get_all_components(self):
            """Получить все компоненты"""
            return self._component_instances.copy()
        
        def update(self, delta_time: float):
            """Обновить объект"""
            if not self.active:
                return
            
            for component in self._component_instances:
                if isinstance(component, Updatable) and component.enabled:
                    component.update(delta_time)
        
        def draw(self) -> str:
            """Нарисовать объект"""
            if not self.active:
                return ""
            
            renderer = self.get_component(Renderer)
            if renderer and isinstance(renderer, Drawable):
                return renderer.draw()
            return f"GameObject '{self.name}' (без рендерера)"
        
        def __str__(self):
            return f"GameObject(id={self.id}, name='{self.name}', components={len(self._components)})"
        
        def __repr__(self):
            return f"GameObject({self.id}, '{self.name}')"
        
        def __eq__(self, other):
            if isinstance(other, GameObject):
                return self.id == other.id
            return False
        
        def __hash__(self):
            return hash(self.id)
        
        def __iter__(self):
            """Итерация по компонентам"""
            return iter(self._component_instances)
        
        def __len__(self):
            """Количество компонентов"""
            return len(self._component_instances)
    
    # Специализированные игровые объекты
    class Player(GameObject, HealthMixin, InventoryMixin):
        """Игрок"""
        
        def __init__(self, name: str):
            super().__init__(name, max_health=100, inventory_size=20)
            self.score = 0
            self.level = 1
            
            # Добавляем базовые компоненты
            self.add_component(Transform(Vector2D(0, 0)))
            self.add_component(Renderer("player_sprite", "blue"))
            self.add_component(Rigidbody(mass=70, drag=0.2))
            self.add_component(Collider(32, 48))
        
        def move_player(self, direction: Vector2D, speed: float = 100):
            """Управление игроком"""
            rigidbody = self.get_component(Rigidbody)
            if rigidbody:
                force = direction.normalize() * speed
                rigidbody.add_force(force)
        
        def add_score(self, points: int):
            """Добавить очки"""
            self.score += points
            if self.score >= self.level * 1000:
                self.level_up()
        
        def level_up(self):
            """Повышение уровня"""
            self.level += 1
            self.max_health += 10
            self.heal(self.max_health)  # Полное восстановление при повышении уровня
            print(f"Уровень повышен до {self.level}!")
    
    class Enemy(GameObject, HealthMixin):
        """Враг"""
        
        def __init__(self, name: str, enemy_type: str = "basic"):
            super().__init__(name, max_health=50)
            self.enemy_type = enemy_type
            self.damage = 10
            self.speed = 50
            
            # Добавляем компоненты
            self.add_component(Transform())
            self.add_component(Renderer("enemy_sprite", "red"))
            self.add_component(Rigidbody(mass=60, drag=0.3))
            self.add_component(Collider(24, 24))
        
        def attack(self, target):
            """Атака цели"""
            if hasattr(target, 'take_damage'):
                target.take_damage(self.damage)
                return f"{self.name} атакует {target.name} на {self.damage} урона"
            return f"{self.name} не может атаковать {target.name}"
        
        def ai_update(self, delta_time: float, player_position: Vector2D):
            """ИИ врага"""
            transform = self.get_component(Transform)
            rigidbody = self.get_component(Rigidbody)
            
            if transform and rigidbody:
                # Движение к игроку
                direction = (player_position - transform.position).normalize()
                force = direction * self.speed
                rigidbody.add_force(force)
    
    # Система управления игрой
    class GameSystem:
        """Система управления игрой"""
        
        def __init__(self):
            self.game_objects = []
            self._colliders = []
            self.running = False
        
        def add_game_object(self, game_object: GameObject):
            """Добавить игровой объект"""
            self.game_objects.append(game_object)
            
            # Регистрируем коллайдеры
            collider = game_object.get_component(Collider)
            if collider:
                self._colliders.append(collider)
        
        def remove_game_object(self, game_object: GameObject):
            """Удалить игровой объект"""
            if game_object in self.game_objects:
                self.game_objects.remove(game_object)
                
                collider = game_object.get_component(Collider)
                if collider in self._colliders:
                    self._colliders.remove(collider)
        
        def update(self, delta_time: float):
            """Обновить все объекты"""
            # Обновляем объекты
            for obj in self.game_objects:
                obj.update(delta_time)
                
                # Специальная логика для врагов
                if isinstance(obj, Enemy) and obj.is_alive:
                    player = self.find_object_by_type(Player)
                    if player:
                        player_transform = player.get_component(Transform)
                        if player_transform:
                            obj.ai_update(delta_time, player_transform.position)
            
            # Проверяем коллизии
            self.check_collisions()
        
        def check_collisions(self):
            """Проверить коллизии"""
            for i, collider1 in enumerate(self._colliders):
                for collider2 in self._colliders[i + 1:]:
                    if collider1.check_collision(collider2):
                        self.handle_collision(collider1, collider2)
        
        def handle_collision(self, collider1: Collider, collider2: Collider):
            """Обработать коллизию"""
            obj1 = collider1.game_object
            obj2 = collider2.game_object
            
            # Вызываем callbacks
            for callback in collider1.collision_callbacks:
                callback(obj2)
            for callback in collider2.collision_callbacks:
                callback(obj1)
        
        def render(self):
            """Отрисовать все объекты"""
            drawable_objects = []
            
            for obj in self.game_objects:
                if isinstance(obj, Drawable) or obj.has_component(Renderer):
                    drawable_objects.append(obj)
            
            # Сортируем по слоям
            drawable_objects.sort(key=lambda obj: (
                obj.get_component(Renderer).layer 
                if obj.has_component(Renderer) 
                else 0
            ))
            
            print("=== Кадр отрисовки ===")
            for obj in drawable_objects:
                result = obj.draw()
                if result:
                    print(result)
        
        def find_object_by_name(self, name: str):
            """Найти объект по имени"""
            for obj in self.game_objects:
                if obj.name == name:
                    return obj
            return None
        
        def find_object_by_type(self, object_type: Type):
            """Найти объект по типу"""
            for obj in self.game_objects:
                if isinstance(obj, object_type):
                    return obj
            return None
        
        def find_objects_by_tag(self, tag: str):
            """Найти объекты по тегу"""
            return [obj for obj in self.game_objects if obj.tag == tag]
        
        def get_statistics(self):
            """Статистика игры"""
            total_objects = len(self.game_objects)
            active_objects = sum(1 for obj in self.game_objects if obj.active)
            components_count = sum(len(obj) for obj in self.game_objects)
            
            return {
                'total_objects': total_objects,
                'active_objects': active_objects,
                'components_count': components_count,
                'colliders_count': len(self._colliders)
            }
    
    # Тестирование игрового фреймворка
    print("1. Зарегистрированные компоненты:")
    print(f"Компоненты: {ComponentMeta.list_components()}")
    
    print("\n2. Создание игровых объектов:")
    
    game_system = GameSystem()
    
    # Создаем игрока
    player = Player("Герой")
    player.tag = "player"
    game_system.add_game_object(player)
    print(f"Создан игрок: {player}")
    print(f"Здоровье: {player.current_health}/{player.max_health}")
    print(f"Инвентарь: {player.get_inventory_info()}")
    
    # Создаем врагов
    enemy1 = Enemy("Орк", "orc")
    enemy1.tag = "enemy"
    enemy1_transform = enemy1.get_component(Transform)
    enemy1_transform.position = Vector2D(100, 50)
    game_system.add_game_object(enemy1)
    
    enemy2 = Enemy("Гоблин", "goblin")
    enemy2.tag = "enemy"
    enemy2_transform = enemy2.get_component(Transform)
    enemy2_transform.position = Vector2D(-80, 30)
    game_system.add_game_object(enemy2)
    
    print(f"Создан враг 1: {enemy1}")
    print(f"Создан враг 2: {enemy2}")
    
    print("\n3. Тестирование компонентов:")
    
    # Проверяем протоколы
    renderer = player.get_component(Renderer)
    print(f"Player имеет Drawable: {isinstance(renderer, Drawable)}")
    print(f"Player имеет Updatable: {isinstance(player.get_component(Rigidbody), Updatable)}")
    
    # Добавляем предметы в инвентарь
    player.add_item("Меч")
    player.add_item("Щит")
    player.add_item("Зелье здоровья")
    print(f"Инвентарь игрока: {player.get_inventory_info()}")
    
    print("\n4. Симуляция игры:")
    
    # Перемещаем игрока
    player.move_player(Vector2D(1, 0), 150)
    print("Игрок движется вправо")
    
    # Обновляем систему
    delta_time = 0.016  # 60 FPS
    for frame in range(3):
        print(f"\nКадр {frame + 1}:")
        game_system.update(delta_time)
        
        # Показываем позиции
        player_transform = player.get_component(Transform)
        print(f"Позиция игрока: {player_transform.position}")
        
        for i, enemy in enumerate([enemy1, enemy2]):
            enemy_transform = enemy.get_component(Transform)
            print(f"Позиция врага {i+1}: {enemy_transform.position}")
    
    print("\n5. Боевая система:")
    
    # Враг атакует игрока
    print(enemy1.attack(player))
    print(f"Здоровье игрока: {player.current_health}/{player.max_health}")
    
    # Игрок получает очки
    player.add_score(500)
    print(f"Очки игрока: {player.score}, уровень: {player.level}")
    
    print("\n6. Отрисовка:")
    game_system.render()
    
    print("\n7. Статистика системы:")
    stats = game_system.get_statistics()
    print(f"Всего объектов: {stats['total_objects']}")
    print(f"Активных объектов: {stats['active_objects']}")
    print(f"Компонентов: {stats['components_count']}")
    print(f"Коллайдеров: {stats['colliders_count']}")
    
    print("\n✅ Упражнение 2 завершено!")


def exercise_03_design_patterns_showcase():
    """
    Упражнение 3: Демонстрация паттернов проектирования
    
    Задача:
    Реализуйте несколько ключевых паттернов проектирования:
    1. Singleton (метакласс)
    2. Factory Method
    3. Observer
    4. Strategy
    5. Command
    6. Adapter
    7. Decorator
    8. State
    
    Используйте ООП принципы и современные возможности Python.
    """
    print("=== Упражнение 3: Демонстрация паттернов проектирования ===")
    
    # ЗАДАЧА: Реализуйте паттерны проектирования
    
    # РЕШЕНИЕ:
    
    from enum import Enum
    from collections import deque
    import threading
    
    # 1. Singleton (метакласс)
    class SingletonMeta(type):
        """Метакласс для создания синглтонов"""
        
        _instances = {}
        _lock = threading.Lock()
        
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                with cls._lock:
                    if cls not in cls._instances:
                        cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]
    
    class Logger(metaclass=SingletonMeta):
        """Логгер как синглтон"""
        
        def __init__(self):
            if hasattr(self, 'initialized'):
                return
            
            self.logs = []
            self.level = "INFO"
            self.initialized = True
        
        def log(self, level: str, message: str):
            """Записать лог"""
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {level}: {message}"
            self.logs.append(log_entry)
            print(log_entry)
        
        def get_logs(self):
            """Получить все логи"""
            return self.logs.copy()
    
    # 2. Factory Method
    class Animal(ABC):
        """Абстрактное животное"""
        
        @abstractmethod
        def make_sound(self) -> str:
            pass
        
        @abstractmethod
        def get_type(self) -> str:
            pass
    
    class Dog(Animal):
        def make_sound(self) -> str:
            return "Гав!"
        
        def get_type(self) -> str:
            return "Собака"
    
    class Cat(Animal):
        def make_sound(self) -> str:
            return "Мяу!"
        
        def get_type(self) -> str:
            return "Кошка"
    
    class Bird(Animal):
        def make_sound(self) -> str:
            return "Чирик!"
        
        def get_type(self) -> str:
            return "Птица"
    
    class AnimalFactory:
        """Фабрика животных"""
        
        _animals = {
            'dog': Dog,
            'cat': Cat,
            'bird': Bird
        }
        
        @classmethod
        def create_animal(cls, animal_type: str) -> Animal:
            """Создать животное по типу"""
            animal_class = cls._animals.get(animal_type.lower())
            if animal_class:
                return animal_class()
            raise ValueError(f"Неизвестный тип животного: {animal_type}")
        
        @classmethod
        def register_animal(cls, animal_type: str, animal_class: type):
            """Зарегистрировать новый тип животного"""
            cls._animals[animal_type.lower()] = animal_class
        
        @classmethod
        def get_available_types(cls):
            """Получить доступные типы"""
            return list(cls._animals.keys())
    
    # 3. Observer
    class Observer(ABC):
        """Абстрактный наблюдатель"""
        
        @abstractmethod
        def update(self, subject, event_type: str, data: Any):
            pass
    
    class Subject:
        """Субъект для наблюдения"""
        
        def __init__(self):
            self._observers = []
        
        def attach(self, observer: Observer):
            """Подписать наблюдателя"""
            if observer not in self._observers:
                self._observers.append(observer)
        
        def detach(self, observer: Observer):
            """Отписать наблюдателя"""
            if observer in self._observers:
                self._observers.remove(observer)
        
        def notify(self, event_type: str, data: Any = None):
            """Уведомить всех наблюдателей"""
            for observer in self._observers:
                observer.update(self, event_type, data)
    
    class NewsAgency(Subject):
        """Новостное агентство"""
        
        def __init__(self, name: str):
            super().__init__()
            self.name = name
            self.latest_news = ""
        
        def publish_news(self, news: str):
            """Опубликовать новость"""
            self.latest_news = news
            self.notify("news_published", news)
    
    class NewsSubscriber(Observer):
        """Подписчик новостей"""
        
        def __init__(self, name: str):
            self.name = name
            self.received_news = []
        
        def update(self, subject, event_type: str, data: Any):
            """Получить уведомление"""
            if event_type == "news_published":
                self.received_news.append(data)
                print(f"{self.name} получил новость: {data}")
    
    # 4. Strategy
    class PaymentStrategy(ABC):
        """Абстрактная стратегия оплаты"""
        
        @abstractmethod
        def pay(self, amount: float) -> str:
            pass
        
        @abstractmethod
        def get_fees(self, amount: float) -> float:
            pass
    
    class CreditCardPayment(PaymentStrategy):
        """Оплата кредитной картой"""
        
        def __init__(self, card_number: str):
            self.card_number = card_number[-4:]  # Показываем только последние 4 цифры
        
        def pay(self, amount: float) -> str:
            fees = self.get_fees(amount)
            total = amount + fees
            return f"Оплачено {total:.2f} (включая комиссию {fees:.2f}) картой ****{self.card_number}"
        
        def get_fees(self, amount: float) -> float:
            return amount * 0.03  # 3% комиссия
    
    class PayPalPayment(PaymentStrategy):
        """Оплата через PayPal"""
        
        def __init__(self, email: str):
            self.email = email
        
        def pay(self, amount: float) -> str:
            fees = self.get_fees(amount)
            total = amount + fees
            return f"Оплачено {total:.2f} (включая комиссию {fees:.2f}) через PayPal ({self.email})"
        
        def get_fees(self, amount: float) -> float:
            return 2.5  # Фиксированная комиссия
    
    class CryptoPayment(PaymentStrategy):
        """Оплата криптовалютой"""
        
        def __init__(self, wallet_address: str):
            self.wallet_address = wallet_address[:8] + "..."
        
        def pay(self, amount: float) -> str:
            fees = self.get_fees(amount)
            total = amount + fees
            return f"Оплачено {total:.2f} (включая комиссию {fees:.2f}) Bitcoin на {self.wallet_address}"
        
        def get_fees(self, amount: float) -> float:
            return 5.0  # Фиксированная комиссия за транзакцию
    
    class PaymentProcessor:
        """Процессор платежей с выбором стратегии"""
        
        def __init__(self):
            self.strategy = None
        
        def set_strategy(self, strategy: PaymentStrategy):
            """Установить стратегию оплаты"""
            self.strategy = strategy
        
        def process_payment(self, amount: float) -> str:
            """Обработать платеж"""
            if not self.strategy:
                raise ValueError("Стратегия оплаты не установлена")
            
            return self.strategy.pay(amount)
    
    # 5. Command
    class Command(ABC):
        """Абстрактная команда"""
        
        @abstractmethod
        def execute(self):
            pass
        
        @abstractmethod
        def undo(self):
            pass
    
    class LightReceiver:
        """Получатель команд - лампочка"""
        
        def __init__(self, location: str):
            self.location = location
            self.is_on = False
        
        def turn_on(self):
            self.is_on = True
            return f"Лампочка в {self.location} включена"
        
        def turn_off(self):
            self.is_on = False
            return f"Лампочка в {self.location} выключена"
    
    class LightOnCommand(Command):
        """Команда включения света"""
        
        def __init__(self, light: LightReceiver):
            self.light = light
        
        def execute(self):
            return self.light.turn_on()
        
        def undo(self):
            return self.light.turn_off()
    
    class LightOffCommand(Command):
        """Команда выключения света"""
        
        def __init__(self, light: LightReceiver):
            self.light = light
        
        def execute(self):
            return self.light.turn_off()
        
        def undo(self):
            return self.light.turn_on()
    
    class MacroCommand(Command):
        """Макрокоманда - выполняет несколько команд"""
        
        def __init__(self, commands: List[Command]):
            self.commands = commands
        
        def execute(self):
            results = []
            for command in self.commands:
                results.append(command.execute())
            return "; ".join(results)
        
        def undo(self):
            results = []
            # Отменяем в обратном порядке
            for command in reversed(self.commands):
                results.append(command.undo())
            return "; ".join(results)
    
    class RemoteControl:
        """Пульт управления"""
        
        def __init__(self):
            self.commands = {}
            self.last_command = None
            self.command_history = deque(maxlen=10)
        
        def set_command(self, slot: str, command: Command):
            """Установить команду на слот"""
            self.commands[slot] = command
        
        def press_button(self, slot: str):
            """Нажать кнопку"""
            command = self.commands.get(slot)
            if command:
                result = command.execute()
                self.last_command = command
                self.command_history.append(command)
                return result
            return f"Команда для слота {slot} не найдена"
        
        def press_undo(self):
            """Нажать кнопку отмены"""
            if self.last_command:
                result = self.last_command.undo()
                self.last_command = None
                return result
            return "Нет команды для отмены"
    
    # 6. Adapter
    class LegacyPrinter:
        """Старый принтер с несовместимым интерфейсом"""
        
        def print_old_format(self, text: str):
            return f"[LEGACY PRINTER] {text.upper()}"
    
    class ModernPrinter:
        """Современный принтер"""
        
        def print_document(self, document: str, format_type: str = "normal"):
            if format_type == "bold":
                return f"**{document}**"
            elif format_type == "italic":
                return f"*{document}*"
            else:
                return document
    
    class PrinterAdapter:
        """Адаптер для старого принтера"""
        
        def __init__(self, legacy_printer: LegacyPrinter):
            self.legacy_printer = legacy_printer
        
        def print_document(self, document: str, format_type: str = "normal"):
            """Адаптирует интерфейс к современному"""
            # Преобразуем формат
            if format_type == "bold":
                document = f"BOLD: {document}"
            elif format_type == "italic":
                document = f"ITALIC: {document}"
            
            return self.legacy_printer.print_old_format(document)
    
    # 7. Decorator (функциональный)
    def timing_decorator(func):
        """Декоратор для измерения времени выполнения"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() * 1000
            print(f"Функция {func.__name__} выполнилась за {duration:.2f}мс")
            return result
        return wrapper
    
    def logging_decorator(func):
        """Декоратор для логирования"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = Logger()
            logger.log("INFO", f"Вызов функции {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.log("INFO", f"Функция {func.__name__} завершилась успешно")
                return result
            except Exception as e:
                logger.log("ERROR", f"Ошибка в функции {func.__name__}: {e}")
                raise
        return wrapper
    
    # 8. State
    class State(ABC):
        """Абстрактное состояние"""
        
        @abstractmethod
        def handle_request(self, context):
            pass
        
        @abstractmethod
        def get_state_name(self) -> str:
            pass
    
    class IdleState(State):
        """Состояние ожидания"""
        
        def handle_request(self, context):
            context.set_state(WorkingState())
            return "Переход из ожидания в работу"
        
        def get_state_name(self) -> str:
            return "Ожидание"
    
    class WorkingState(State):
        """Состояние работы"""
        
        def handle_request(self, context):
            context.set_state(IdleState())
            return "Переход из работы в ожидание"
        
        def get_state_name(self) -> str:
            return "Работа"
    
    class StateMachine:
        """Конечный автомат"""
        
        def __init__(self):
            self._state = IdleState()
        
        def set_state(self, state: State):
            """Установить состояние"""
            self._state = state
        
        def get_current_state(self) -> str:
            """Получить текущее состояние"""
            return self._state.get_state_name()
        
        def request(self):
            """Обработать запрос"""
            return self._state.handle_request(self)
    
    # Тестирование паттернов
    print("1. Singleton Pattern:")
    
    logger1 = Logger()
    logger2 = Logger()
    
    print(f"logger1 is logger2: {logger1 is logger2}")
    logger1.log("INFO", "Тест синглтона")
    print(f"Количество логов в logger2: {len(logger2.get_logs())}")
    
    print("\n2. Factory Method Pattern:")
    
    factory = AnimalFactory()
    print(f"Доступные типы: {factory.get_available_types()}")
    
    animals = []
    for animal_type in ['dog', 'cat', 'bird']:
        animal = factory.create_animal(animal_type)
        animals.append(animal)
        print(f"Создано {animal.get_type()}: {animal.make_sound()}")
    
    print("\n3. Observer Pattern:")
    
    news_agency = NewsAgency("CNN")
    
    subscriber1 = NewsSubscriber("Алиса")
    subscriber2 = NewsSubscriber("Боб")
    
    news_agency.attach(subscriber1)
    news_agency.attach(subscriber2)
    
    news_agency.publish_news("Python 3.12 выпущен!")
    news_agency.publish_news("Новый паттерн проектирования открыт!")
    
    print(f"Алиса получила {len(subscriber1.received_news)} новостей")
    print(f"Боб получил {len(subscriber2.received_news)} новостей")
    
    print("\n4. Strategy Pattern:")
    
    processor = PaymentProcessor()
    
    # Тестируем разные стратегии оплаты
    strategies = [
        CreditCardPayment("1234567890123456"),
        PayPalPayment("user@example.com"),
        CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    ]
    
    amount = 100.0
    for strategy in strategies:
        processor.set_strategy(strategy)
        result = processor.process_payment(amount)
        print(result)
    
    print("\n5. Command Pattern:")
    
    # Создаем получателей
    living_room_light = LightReceiver("гостиная")
    bedroom_light = LightReceiver("спальня")
    
    # Создаем команды
    living_room_on = LightOnCommand(living_room_light)
    living_room_off = LightOffCommand(living_room_light)
    bedroom_on = LightOnCommand(bedroom_light)
    bedroom_off = LightOffCommand(bedroom_light)
    
    # Макрокоманда - включить все лампы
    all_lights_on = MacroCommand([living_room_on, bedroom_on])
    all_lights_off = MacroCommand([living_room_off, bedroom_off])
    
    # Настраиваем пульт
    remote = RemoteControl()
    remote.set_command("living_room_on", living_room_on)
    remote.set_command("living_room_off", living_room_off)
    remote.set_command("all_on", all_lights_on)
    remote.set_command("all_off", all_lights_off)
    
    # Тестируем команды
    print(remote.press_button("living_room_on"))
    print(remote.press_button("all_on"))
    print(remote.press_undo())  # Отменяем последнюю команду
    
    print("\n6. Adapter Pattern:")
    
    # Современный принтер
    modern_printer = ModernPrinter()
    print("Современный принтер:", modern_printer.print_document("Тест", "bold"))
    
    # Старый принтер через адаптер
    legacy_printer = LegacyPrinter()
    adapter = PrinterAdapter(legacy_printer)
    print("Старый принтер через адаптер:", adapter.print_document("Тест", "bold"))
    
    print("\n7. Decorator Pattern:")
    
    @timing_decorator
    @logging_decorator
    def slow_function():
        """Медленная функция для демонстрации декораторов"""
        import time
        time.sleep(0.01)  # Имитация работы
        return "Результат работы"
    
    result = slow_function()
    print(f"Результат: {result}")
    
    print("\n8. State Pattern:")
    
    machine = StateMachine()
    
    for i in range(4):
        print(f"Текущее состояние: {machine.get_current_state()}")
        result = machine.request()
        print(f"Результат запроса: {result}")
    
    print(f"Финальное состояние: {machine.get_current_state()}")
    
    print("\n✅ Упражнение 3 завершено!")


def main():
    """
    Главная функция для запуска всех упражнений
    """
    exercises = [
        ("Система управления библиотекой", exercise_01_library_management_system),
        ("Фреймворк для разработки игр", exercise_02_game_development_framework),
        ("Демонстрация паттернов проектирования", exercise_03_design_patterns_showcase),
    ]
    
    print("🏗️ Упражнения: Объектно-ориентированное программирование в Python")
    print("=" * 70)
    print("Эти упражнения помогут вам освоить:")
    print("- Принципы ООП (инкапсуляция, наследование, полиморфизм, абстракция)")
    print("- Проектирование классов и их взаимодействий")
    print("- Специальные методы и метаклассы")
    print("- Паттерны проектирования")
    print("- Современные возможности Python для ООП")
    print("=" * 70)
    
    for i, (name, func) in enumerate(exercises, 1):
        print(f"\n{i}. {name}")
        print("-" * (len(name) + 3))
        try:
            func()
        except Exception as e:
            print(f"Ошибка при выполнении упражнения: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(exercises):
            input("\nНажмите Enter для продолжения к следующему упражнению...")


if __name__ == "__main__":
    main() 