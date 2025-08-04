# Теория: Архитектура и CS фундамент в Python

## 🎯 Цель раздела

Этот раздел охватывает фундаментальные принципы Computer Science и архитектурные паттерны применительно к Python разработке. Мы изучим алгоритмы, структуры данных, паттерны проектирования и принципы построения масштабируемых систем.

## 📋 Содержание

1. [Алгоритмы и сложность](#алгоритмы-и-сложность)
2. [Структуры данных](#структуры-данных)
3. [Паттерны проектирования](#паттерны-проектирования)
4. [Архитектурные принципы](#архитектурные-принципы)
5. [Параллелизм и асинхронность](#параллелизм-и-асинхронность)
6. [Производительность и оптимизация](#производительность-и-оптимизация)
7. [Системное проектирование](#системное-проектирование)

---

## 🧮 Алгоритмы и сложность

### Анализ сложности алгоритмов

**Big O нотация** — это математический способ описания поведения алгоритма при увеличении размера входных данных.

#### Основные классы сложности:

```python
# O(1) - Константная сложность
def get_first_element(arr):
    """Доступ к элементу по индексу"""
    return arr[0] if arr else None

# O(log n) - Логарифмическая сложность
def binary_search(arr, target):
    """Бинарный поиск в отсортированном массиве"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# O(n) - Линейная сложность
def linear_search(arr, target):
    """Линейный поиск"""
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1

# O(n log n) - Логарифмически-линейная сложность
def merge_sort(arr):
    """Сортировка слиянием"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Слияние двух отсортированных массивов"""
    result = []
    i, j = 0, 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# O(n²) - Квадратичная сложность
def bubble_sort(arr):
    """Пузырьковая сортировка"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

### Рекурсия и динамическое программирование

```python
from functools import lru_cache
from typing import Dict, List

# Наивная рекурсия - O(2^n)
def fibonacci_naive(n: int) -> int:
    """Наивное вычисление числа Фибоначчи"""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

# Мемоизация - O(n)
@lru_cache(maxsize=None)
def fibonacci_memo(n: int) -> int:
    """Фибоначчи с мемоизацией"""
    if n <= 1:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)

# Динамическое программирование (снизу вверх) - O(n)
def fibonacci_dp(n: int) -> int:
    """Фибоначчи с динамическим программированием"""
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

# Оптимизированная версия - O(n) времени, O(1) памяти
def fibonacci_optimized(n: int) -> int:
    """Оптимизированное вычисление Фибоначчи"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b

# Задача о рюкзаке (0/1 Knapsack)
def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """Решение задачи о рюкзаке методом динамического программирования"""
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w],  # Не берем предмет
                    values[i - 1] + dp[i - 1][w - weights[i - 1]]  # Берем предмет
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]
```

### Алгоритмы на графах

```python
from collections import deque, defaultdict
from typing import List, Dict, Set, Tuple
import heapq

class Graph:
    """Класс для представления графа"""
    
    def __init__(self):
        self.adjacency_list: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
    
    def add_edge(self, from_vertex: str, to_vertex: str, weight: int = 1):
        """Добавить ребро в граф"""
        self.adjacency_list[from_vertex].append((to_vertex, weight))
    
    def bfs(self, start: str) -> List[str]:
        """Обход в ширину (BFS)"""
        visited = set()
        queue = deque([start])
        result = []
        
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                for neighbor, _ in self.adjacency_list[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    def dfs(self, start: str, visited: Set[str] = None) -> List[str]:
        """Обход в глубину (DFS)"""
        if visited is None:
            visited = set()
        
        result = []
        if start not in visited:
            visited.add(start)
            result.append(start)
            
            for neighbor, _ in self.adjacency_list[start]:
                result.extend(self.dfs(neighbor, visited))
        
        return result
    
    def dijkstra(self, start: str) -> Dict[str, int]:
        """Алгоритм Дейкстры для поиска кратчайших путей"""
        distances = {vertex: float('infinity') for vertex in self.adjacency_list}
        distances[start] = 0
        
        priority_queue = [(0, start)]
        visited = set()
        
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            
            if current_vertex in visited:
                continue
            
            visited.add(current_vertex)
            
            for neighbor, weight in self.adjacency_list[current_vertex]:
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances
    
    def has_cycle(self) -> bool:
        """Проверка наличия цикла в направленном графе"""
        color = {}  # 0 - белый, 1 - серый, 2 - черный
        
        def dfs_cycle(vertex):
            if vertex in color:
                return color[vertex] == 1  # Серый = цикл
            
            color[vertex] = 1  # Серый
            
            for neighbor, _ in self.adjacency_list[vertex]:
                if dfs_cycle(neighbor):
                    return True
            
            color[vertex] = 2  # Черный
            return False
        
        for vertex in self.adjacency_list:
            if vertex not in color:
                if dfs_cycle(vertex):
                    return True
        
        return False
```

---

## 📊 Структуры данных

### Продвинутые структуры данных

```python
from typing import Optional, Any, List
import bisect

class TreeNode:
    """Узел бинарного дерева"""
    
    def __init__(self, value: Any):
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

class BinarySearchTree:
    """Бинарное дерево поиска"""
    
    def __init__(self):
        self.root: Optional[TreeNode] = None
    
    def insert(self, value: Any) -> None:
        """Вставка значения"""
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: TreeNode, value: Any) -> None:
        """Рекурсивная вставка"""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value: Any) -> bool:
        """Поиск значения"""
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[TreeNode], value: Any) -> bool:
        """Рекурсивный поиск"""
        if node is None:
            return False
        
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def inorder_traversal(self) -> List[Any]:
        """Обход дерева в порядке возрастания"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Рекурсивный обход"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

class TrieNode:
    """Узел префиксного дерева"""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word = False

class Trie:
    """Префиксное дерево (Trie)"""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Вставка слова"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Поиск слова"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """Проверка наличия слов с префиксом"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def find_words_with_prefix(self, prefix: str) -> List[str]:
        """Найти все слова с заданным префиксом"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        words = []
        self._collect_words(node, prefix, words)
        return words
    
    def _collect_words(self, node: TrieNode, current_word: str, words: List[str]) -> None:
        """Сбор всех слов из поддерева"""
        if node.is_end_of_word:
            words.append(current_word)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current_word + char, words)

class MinHeap:
    """Минимальная куча (Min Heap)"""
    
    def __init__(self):
        self.heap: List[Any] = []
    
    def parent(self, i: int) -> int:
        """Индекс родителя"""
        return (i - 1) // 2
    
    def left_child(self, i: int) -> int:
        """Индекс левого ребенка"""
        return 2 * i + 1
    
    def right_child(self, i: int) -> int:
        """Индекс правого ребенка"""
        return 2 * i + 2
    
    def swap(self, i: int, j: int) -> None:
        """Обмен элементов"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def insert(self, value: Any) -> None:
        """Вставка элемента"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
    
    def _heapify_up(self, i: int) -> None:
        """Восстановление свойства кучи вверх"""
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.swap(i, self.parent(i))
            i = self.parent(i)
    
    def extract_min(self) -> Optional[Any]:
        """Извлечение минимального элемента"""
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        
        return min_val
    
    def _heapify_down(self, i: int) -> None:
        """Восстановление свойства кучи вниз"""
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left
        
        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right
        
        if i != min_index:
            self.swap(i, min_index)
            self._heapify_down(min_index)
    
    def peek(self) -> Optional[Any]:
        """Просмотр минимального элемента без извлечения"""
        return self.heap[0] if self.heap else None
    
    def size(self) -> int:
        """Размер кучи"""
        return len(self.heap)
```

---

## 🎨 Паттерны проектирования

### Порождающие паттерны

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum

# Singleton
class DatabaseConnection:
    """Паттерн Singleton для подключения к БД"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_string = "database://localhost:5432"
            self.is_connected = False
            DatabaseConnection._initialized = True
    
    def connect(self):
        """Подключение к базе данных"""
        if not self.is_connected:
            print(f"Подключение к {self.connection_string}")
            self.is_connected = True
    
    def disconnect(self):
        """Отключение от базы данных"""
        if self.is_connected:
            print("Отключение от базы данных")
            self.is_connected = False

# Factory Method
class Document(ABC):
    """Абстрактный документ"""
    
    @abstractmethod
    def create(self) -> str:
        pass

class PDFDocument(Document):
    """PDF документ"""
    
    def create(self) -> str:
        return "Создан PDF документ"

class WordDocument(Document):
    """Word документ"""
    
    def create(self) -> str:
        return "Создан Word документ"

class DocumentFactory(ABC):
    """Абстрактная фабрика документов"""
    
    @abstractmethod
    def create_document(self) -> Document:
        pass

class PDFFactory(DocumentFactory):
    """Фабрика PDF документов"""
    
    def create_document(self) -> Document:
        return PDFDocument()

class WordFactory(DocumentFactory):
    """Фабрика Word документов"""
    
    def create_document(self) -> Document:
        return WordDocument()

# Builder
class Computer:
    """Компьютер"""
    
    def __init__(self):
        self.cpu: str = ""
        self.memory: str = ""
        self.storage: str = ""
        self.gpu: str = ""
        self.case: str = ""
    
    def __str__(self) -> str:
        return f"Компьютер: CPU={self.cpu}, RAM={self.memory}, Storage={self.storage}, GPU={self.gpu}, Case={self.case}"

class ComputerBuilder:
    """Строитель компьютера"""
    
    def __init__(self):
        self.computer = Computer()
    
    def add_cpu(self, cpu: str) -> 'ComputerBuilder':
        """Добавить процессор"""
        self.computer.cpu = cpu
        return self
    
    def add_memory(self, memory: str) -> 'ComputerBuilder':
        """Добавить память"""
        self.computer.memory = memory
        return self
    
    def add_storage(self, storage: str) -> 'ComputerBuilder':
        """Добавить накопитель"""
        self.computer.storage = storage
        return self
    
    def add_gpu(self, gpu: str) -> 'ComputerBuilder':
        """Добавить видеокарту"""
        self.computer.gpu = gpu
        return self
    
    def add_case(self, case: str) -> 'ComputerBuilder':
        """Добавить корпус"""
        self.computer.case = case
        return self
    
    def build(self) -> Computer:
        """Собрать компьютер"""
        return self.computer

class ComputerDirector:
    """Директор сборки компьютера"""
    
    @staticmethod
    def build_gaming_computer() -> Computer:
        """Собрать игровой компьютер"""
        return (ComputerBuilder()
                .add_cpu("Intel i9-13900K")
                .add_memory("32GB DDR5")
                .add_storage("2TB NVMe SSD")
                .add_gpu("RTX 4080")
                .add_case("Gaming Tower")
                .build())
    
    @staticmethod
    def build_office_computer() -> Computer:
        """Собрать офисный компьютер"""
        return (ComputerBuilder()
                .add_cpu("Intel i5-13400")
                .add_memory("16GB DDR4")
                .add_storage("512GB SSD")
                .add_gpu("Integrated")
                .add_case("Mini ITX")
                .build())
```

### Структурные паттерны

```python
# Adapter
class LegacyPrinter:
    """Старый принтер с устаревшим интерфейсом"""
    
    def old_print(self, text: str) -> None:
        print(f"Старый принтер: {text}")

class ModernPrinter:
    """Современный принтер"""
    
    def print_document(self, document: str) -> None:
        print(f"Современный принтер: {document}")

class PrinterAdapter:
    """Адаптер для старого принтера"""
    
    def __init__(self, legacy_printer: LegacyPrinter):
        self.legacy_printer = legacy_printer
    
    def print_document(self, document: str) -> None:
        """Адаптированный метод печати"""
        self.legacy_printer.old_print(document)

# Decorator
class Coffee(ABC):
    """Абстрактный кофе"""
    
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass

class SimpleCoffee(Coffee):
    """Простой кофе"""
    
    def cost(self) -> float:
        return 50.0
    
    def description(self) -> str:
        return "Простой кофе"

class CoffeeDecorator(Coffee):
    """Базовый декоратор кофе"""
    
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()
    
    def description(self) -> str:
        return self._coffee.description()

class MilkDecorator(CoffeeDecorator):
    """Декоратор молока"""
    
    def cost(self) -> float:
        return self._coffee.cost() + 10.0
    
    def description(self) -> str:
        return self._coffee.description() + ", молоко"

class SugarDecorator(CoffeeDecorator):
    """Декоратор сахара"""
    
    def cost(self) -> float:
        return self._coffee.cost() + 5.0
    
    def description(self) -> str:
        return self._coffee.description() + ", сахар"

# Facade
class CPU:
    """Процессор"""
    
    def freeze(self):
        print("CPU: Заморозка")
    
    def jump(self, position: int):
        print(f"CPU: Переход к позиции {position}")
    
    def execute(self):
        print("CPU: Выполнение команд")

class Memory:
    """Память"""
    
    def load(self, position: int, data: str):
        print(f"Memory: Загрузка '{data}' в позицию {position}")

class HardDrive:
    """Жесткий диск"""
    
    def read(self, lba: int, size: int) -> str:
        print(f"HDD: Чтение {size} байт с позиции {lba}")
        return "boot_data"

class ComputerFacade:
    """Фасад компьютера"""
    
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
    
    def start(self):
        """Запуск компьютера"""
        print("Запуск компьютера...")
        self.cpu.freeze()
        boot_data = self.hard_drive.read(0, 1024)
        self.memory.load(0, boot_data)
        self.cpu.jump(0)
        self.cpu.execute()
        print("Компьютер запущен!")
```

### Поведенческие паттерны

```python
# Observer
from typing import List

class Observer(ABC):
    """Абстрактный наблюдатель"""
    
    @abstractmethod
    def update(self, subject: 'Subject') -> None:
        pass

class Subject(ABC):
    """Абстрактный субъект"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Подписать наблюдателя"""
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Отписать наблюдателя"""
        self._observers.remove(observer)
    
    def notify(self) -> None:
        """Уведомить всех наблюдателей"""
        for observer in self._observers:
            observer.update(self)

class StockPrice(Subject):
    """Цена акции"""
    
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self._symbol = symbol
        self._price = price
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, value: float) -> None:
        self._price = value
        self.notify()
    
    @property
    def symbol(self) -> str:
        return self._symbol

class StockDisplay(Observer):
    """Отображение цены акции"""
    
    def __init__(self, name: str):
        self.name = name
    
    def update(self, subject: Subject) -> None:
        if isinstance(subject, StockPrice):
            print(f"{self.name}: {subject.symbol} = ${subject.price:.2f}")

# Strategy
class SortStrategy(ABC):
    """Абстрактная стратегия сортировки"""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

class BubbleSortStrategy(SortStrategy):
    """Стратегия пузырьковой сортировки"""
    
    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

class QuickSortStrategy(SortStrategy):
    """Стратегия быстрой сортировки"""
    
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        
        return self.sort(left) + middle + self.sort(right)

class SortContext:
    """Контекст сортировки"""
    
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy) -> None:
        """Изменить стратегию"""
        self._strategy = strategy
    
    def sort_data(self, data: List[int]) -> List[int]:
        """Сортировать данные используя текущую стратегию"""
        return self._strategy.sort(data)

# Command
class Command(ABC):
    """Абстрактная команда"""
    
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass

class Light:
    """Лампочка"""
    
    def __init__(self, location: str):
        self.location = location
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"Свет в {self.location} включен")
    
    def turn_off(self):
        self.is_on = False
        print(f"Свет в {self.location} выключен")

class LightOnCommand(Command):
    """Команда включения света"""
    
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self) -> None:
        self.light.turn_on()
    
    def undo(self) -> None:
        self.light.turn_off()

class LightOffCommand(Command):
    """Команда выключения света"""
    
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self) -> None:
        self.light.turn_off()
    
    def undo(self) -> None:
        self.light.turn_on()

class RemoteControl:
    """Пульт управления"""
    
    def __init__(self):
        self._commands: Dict[int, Command] = {}
        self._last_command: Optional[Command] = None
    
    def set_command(self, slot: int, command: Command) -> None:
        """Установить команду на слот"""
        self._commands[slot] = command
    
    def press_button(self, slot: int) -> None:
        """Нажать кнопку"""
        if slot in self._commands:
            command = self._commands[slot]
            command.execute()
            self._last_command = command
    
    def press_undo(self) -> None:
        """Нажать кнопку отмены"""
        if self._last_command:
            self._last_command.undo()
```

---

## 🏗️ Архитектурные принципы

### SOLID принципы

```python
# Single Responsibility Principle (SRP)
class EmailService:
    """Сервис отправки email - одна ответственность"""
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Отправить email"""
        print(f"Отправка email на {to}: {subject}")
        return True

class User:
    """Пользователь - только данные и базовая логика"""
    
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def get_display_name(self) -> str:
        """Получить отображаемое имя"""
        return self.name

class UserNotificationService:
    """Сервис уведомлений пользователей - отдельная ответственность"""
    
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
    
    def notify_user(self, user: User, message: str) -> bool:
        """Уведомить пользователя"""
        return self.email_service.send_email(
            user.email, 
            "Уведомление", 
            message
        )

# Open/Closed Principle (OCP)
class Shape(ABC):
    """Базовая фигура"""
    
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    """Прямоугольник"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Circle(Shape):
    """Круг"""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

class AreaCalculator:
    """Калькулятор площади - закрыт для модификации, открыт для расширения"""
    
    def calculate_total_area(self, shapes: List[Shape]) -> float:
        """Вычислить общую площадь"""
        return sum(shape.area() for shape in shapes)

# Liskov Substitution Principle (LSP)
class Bird(ABC):
    """Базовая птица"""
    
    @abstractmethod
    def move(self) -> str:
        pass

class FlyingBird(Bird):
    """Летающая птица"""
    
    @abstractmethod
    def fly(self) -> str:
        pass
    
    def move(self) -> str:
        return self.fly()

class WalkingBird(Bird):
    """Ходящая птица"""
    
    @abstractmethod
    def walk(self) -> str:
        pass
    
    def move(self) -> str:
        return self.walk()

class Eagle(FlyingBird):
    """Орел"""
    
    def fly(self) -> str:
        return "Орел летит высоко"

class Penguin(WalkingBird):
    """Пингвин"""
    
    def walk(self) -> str:
        return "Пингвин идет вперевалку"

# Interface Segregation Principle (ISP)
class Readable(Protocol):
    """Интерфейс для чтения"""
    
    def read(self) -> str:
        pass

class Writable(Protocol):
    """Интерфейс для записи"""
    
    def write(self, data: str) -> None:
        pass

class Printable(Protocol):
    """Интерфейс для печати"""
    
    def print_document(self) -> None:
        pass

class SimpleDocument:
    """Простой документ - только чтение и запись"""
    
    def __init__(self, content: str = ""):
        self._content = content
    
    def read(self) -> str:
        return self._content
    
    def write(self, data: str) -> None:
        self._content = data

class PrintableDocument:
    """Документ с возможностью печати"""
    
    def __init__(self, content: str = ""):
        self._content = content
    
    def read(self) -> str:
        return self._content
    
    def write(self, data: str) -> None:
        self._content = data
    
    def print_document(self) -> None:
        print(f"Печать: {self._content}")

# Dependency Inversion Principle (DIP)
class Database(ABC):
    """Абстракция базы данных"""
    
    @abstractmethod
    def save(self, data: Any) -> bool:
        pass
    
    @abstractmethod
    def load(self, key: str) -> Optional[Any]:
        pass

class MySQLDatabase(Database):
    """MySQL реализация"""
    
    def save(self, data: Any) -> bool:
        print(f"Сохранение в MySQL: {data}")
        return True
    
    def load(self, key: str) -> Optional[Any]:
        print(f"Загрузка из MySQL: {key}")
        return f"data_for_{key}"

class MongoDatabase(Database):
    """MongoDB реализация"""
    
    def save(self, data: Any) -> bool:
        print(f"Сохранение в MongoDB: {data}")
        return True
    
    def load(self, key: str) -> Optional[Any]:
        print(f"Загрузка из MongoDB: {key}")
        return f"data_for_{key}"

class UserRepository:
    """Репозиторий пользователей - зависит от абстракции"""
    
    def __init__(self, database: Database):
        self.database = database
    
    def save_user(self, user: User) -> bool:
        """Сохранить пользователя"""
        user_data = {"name": user.name, "email": user.email}
        return self.database.save(user_data)
    
    def load_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Загрузить пользователя"""
        return self.database.load(user_id)
```

---

## ⚡ Параллелизм и асинхронность

### Многопоточность (Threading)

```python
import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Any

class ThreadSafeCounter:
    """Потокобезопасный счетчик"""
    
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        """Увеличить счетчик"""
        with self._lock:
            self._value += 1
    
    def decrement(self):
        """Уменьшить счетчик"""
        with self._lock:
            self._value -= 1
    
    @property
    def value(self) -> int:
        """Получить значение"""
        with self._lock:
            return self._value

class ProducerConsumer:
    """Паттерн Производитель-Потребитель"""
    
    def __init__(self, max_size: int = 10):
        self.queue = queue.Queue(maxsize=max_size)
        self.is_producing = True
    
    def producer(self, items: List[Any]) -> None:
        """Производитель"""
        for item in items:
            self.queue.put(item)
            print(f"Произведено: {item}")
            time.sleep(0.1)
        
        # Сигнал завершения
        self.queue.put(None)
        self.is_producing = False
    
    def consumer(self, consumer_id: int) -> None:
        """Потребитель"""
        while self.is_producing or not self.queue.empty():
            try:
                item = self.queue.get(timeout=1)
                if item is None:
                    break
                
                print(f"Потребитель {consumer_id} обработал: {item}")
                time.sleep(0.2)
                self.queue.task_done()
            
            except queue.Empty:
                continue
    
    def start(self, items: List[Any], num_consumers: int = 2) -> None:
        """Запустить производство и потребление"""
        threads = []
        
        # Запускаем производителя
        producer_thread = threading.Thread(
            target=self.producer, 
            args=(items,)
        )
        threads.append(producer_thread)
        producer_thread.start()
        
        # Запускаем потребителей
        for i in range(num_consumers):
            consumer_thread = threading.Thread(
                target=self.consumer, 
                args=(i + 1,)
            )
            threads.append(consumer_thread)
            consumer_thread.start()
        
        # Ждем завершения всех потоков
        for thread in threads:
            thread.join()

def parallel_processing_example():
    """Пример параллельной обработки"""
    
    def heavy_task(n: int) -> int:
        """Тяжелая задача"""
        time.sleep(1)  # Имитация долгой работы
        return n * n
    
    numbers = list(range(1, 11))
    
    # Последовательная обработка
    start_time = time.time()
    sequential_results = [heavy_task(n) for n in numbers]
    sequential_time = time.time() - start_time
    
    # Параллельная обработка
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        parallel_results = list(executor.map(heavy_task, numbers))
    parallel_time = time.time() - start_time
    
    print(f"Последовательно: {sequential_time:.2f}с")
    print(f"Параллельно: {parallel_time:.2f}с")
    print(f"Ускорение: {sequential_time / parallel_time:.2f}x")
```

### Асинхронное программирование

```python
import asyncio
import aiohttp
import time
from typing import List, Dict, Any

async def async_task(name: str, duration: int) -> str:
    """Асинхронная задача"""
    print(f"Задача {name} началась")
    await asyncio.sleep(duration)
    print(f"Задача {name} завершилась")
    return f"Результат {name}"

async def run_concurrent_tasks():
    """Запуск нескольких асинхронных задач"""
    tasks = [
        async_task("A", 2),
        async_task("B", 1),
        async_task("C", 3)
    ]
    
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    execution_time = time.time() - start_time
    
    print(f"Все задачи завершены за {execution_time:.2f}с")
    return results

class AsyncWebScraper:
    """Асинхронный веб-скрапер"""
    
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Получить содержимое URL"""
        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    content = await response.text()
                    return {
                        "url": url,
                        "status": response.status,
                        "length": len(content),
                        "success": True
                    }
            except Exception as e:
                return {
                    "url": url,
                    "error": str(e),
                    "success": False
                }
    
    async def scrape_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Скрапинг нескольких URL"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_url(session, url) for url in urls]
            return await asyncio.gather(*tasks)

class AsyncProducerConsumer:
    """Асинхронный производитель-потребитель"""
    
    def __init__(self, max_size: int = 10):
        self.queue = asyncio.Queue(maxsize=max_size)
    
    async def producer(self, items: List[Any]) -> None:
        """Асинхронный производитель"""
        for item in items:
            await self.queue.put(item)
            print(f"Произведено: {item}")
            await asyncio.sleep(0.1)
        
        # Сигнал завершения
        await self.queue.put(None)
    
    async def consumer(self, consumer_id: int) -> None:
        """Асинхронный потребитель"""
        while True:
            item = await self.queue.get()
            if item is None:
                await self.queue.put(None)  # Передаем сигнал другим потребителям
                break
            
            print(f"Потребитель {consumer_id} обработал: {item}")
            await asyncio.sleep(0.2)
            self.queue.task_done()
    
    async def start(self, items: List[Any], num_consumers: int = 2) -> None:
        """Запустить асинхронное производство и потребление"""
        tasks = []
        
        # Создаем задачи
        tasks.append(asyncio.create_task(self.producer(items)))
        
        for i in range(num_consumers):
            tasks.append(asyncio.create_task(self.consumer(i + 1)))
        
        # Ждем завершения всех задач
        await asyncio.gather(*tasks)
```

---

## 🚀 Производительность и оптимизация

### Профилирование кода

```python
import cProfile
import pstats
import functools
import time
from typing import Callable, Any
from memory_profiler import profile
import tracemalloc

def timing_decorator(func: Callable) -> Callable:
    """Декоратор для измерения времени выполнения"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        print(f"{func.__name__} выполнилась за {execution_time:.4f}с")
        
        return result
    
    return wrapper

class PerformanceProfiler:
    """Профилировщик производительности"""
    
    def __init__(self):
        self.profiler = cProfile.Profile()
    
    def start_profiling(self):
        """Начать профилирование"""
        self.profiler.enable()
    
    def stop_profiling(self):
        """Остановить профилирование"""
        self.profiler.disable()
    
    def print_stats(self, sort_by: str = 'cumulative', lines: int = 10):
        """Вывести статистику"""
        stats = pstats.Stats(self.profiler)
        stats.sort_stats(sort_by)
        stats.print_stats(lines)
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Any:
        """Профилировать конкретную функцию"""
        self.start_profiling()
        result = func(*args, **kwargs)
        self.stop_profiling()
        return result

class MemoryProfiler:
    """Профилировщик памяти"""
    
    @staticmethod
    def trace_memory_usage(func: Callable) -> Callable:
        """Декоратор для отслеживания использования памяти"""
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            tracemalloc.start()
            
            result = func(*args, **kwargs)
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            print(f"{func.__name__}:")
            print(f"  Текущее использование памяти: {current / 1024 / 1024:.2f} MB")
            print(f"  Пиковое использование памяти: {peak / 1024 / 1024:.2f} MB")
            
            return result
        
        return wrapper

# Примеры оптимизации
class OptimizationExamples:
    """Примеры оптимизации кода"""
    
    @staticmethod
    @timing_decorator
    def inefficient_string_concatenation(strings: List[str]) -> str:
        """Неэффективная конкатенация строк"""
        result = ""
        for s in strings:
            result += s
        return result
    
    @staticmethod
    @timing_decorator
    def efficient_string_concatenation(strings: List[str]) -> str:
        """Эффективная конкатенация строк"""
        return "".join(strings)
    
    @staticmethod
    @timing_decorator
    def inefficient_list_search(data: List[int], target: int) -> bool:
        """Неэффективный поиск в списке"""
        for item in data:
            if item == target:
                return True
        return False
    
    @staticmethod
    @timing_decorator
    def efficient_set_search(data: set, target: int) -> bool:
        """Эффективный поиск в множестве"""
        return target in data
    
    @staticmethod
    @functools.lru_cache(maxsize=None)
    def cached_fibonacci(n: int) -> int:
        """Кэшированное вычисление Фибоначчи"""
        if n <= 1:
            return n
        return OptimizationExamples.cached_fibonacci(n - 1) + OptimizationExamples.cached_fibonacci(n - 2)
    
    @staticmethod
    def benchmark_data_structures():
        """Бенчмарк структур данных"""
        import random
        
        # Подготовка данных
        data_size = 100000
        random_data = [random.randint(1, 1000000) for _ in range(data_size)]
        target = random.choice(random_data)
        
        # Список vs Множество
        data_list = random_data
        data_set = set(random_data)
        
        print("Сравнение поиска в списке и множестве:")
        OptimizationExamples.inefficient_list_search(data_list, target)
        OptimizationExamples.efficient_set_search(data_set, target)
        
        # Строки
        strings = ["строка" + str(i) for i in range(1000)]
        
        print("\nСравнение конкатенации строк:")
        OptimizationExamples.inefficient_string_concatenation(strings)
        OptimizationExamples.efficient_string_concatenation(strings)
```

Этот раздел представляет собой комплексное введение в архитектурные принципы и фундаментальные концепции Computer Science применительно к Python. Он охватывает как теоретические аспекты (алгоритмы, структуры данных), так и практические навыки (паттерны проектирования, оптимизация производительности). 