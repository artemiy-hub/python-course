#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Архитектура и CS фундамент в Python

Этот файл содержит примеры для изучения:
- Алгоритмов и структур данных
- Паттернов проектирования
- Архитектурных принципов
- Оптимизации производительности
"""

import time
import threading
import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Callable, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum
import heapq
from collections import defaultdict, deque
import functools


def example_01_algorithms_and_complexity():
    """
    Пример 1: Алгоритмы и анализ сложности
    
    Демонстрирует различные алгоритмы и их временную сложность
    на практических задачах.
    """
    print("=== Пример 1: Алгоритмы и анализ сложности ===")
    
    def measure_time(func):
        """Декоратор для измерения времени выполнения"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"   {func.__name__}: {(end - start) * 1000:.2f}ms")
            return result
        return wrapper
    
    # Алгоритмы поиска
    @measure_time
    def linear_search(arr: List[int], target: int) -> int:
        """Линейный поиск O(n)"""
        for i, value in enumerate(arr):
            if value == target:
                return i
        return -1
    
    @measure_time
    def binary_search(arr: List[int], target: int) -> int:
        """Бинарный поиск O(log n)"""
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
    
    # Алгоритмы сортировки
    @measure_time
    def bubble_sort(arr: List[int]) -> List[int]:
        """Пузырьковая сортировка O(n²)"""
        arr = arr.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        
        return arr
    
    @measure_time
    def quick_sort(arr: List[int]) -> List[int]:
        """Быстрая сортировка O(n log n) в среднем"""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return quick_sort(left) + middle + quick_sort(right)
    
    @measure_time
    def merge_sort(arr: List[int]) -> List[int]:
        """Сортировка слиянием O(n log n)"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        
        return merge(left, right)
    
    def merge(left: List[int], right: List[int]) -> List[int]:
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
    
    # Алгоритм Дейкстры
    def dijkstra(graph: Dict[str, List[tuple]], start: str) -> Dict[str, int]:
        """Алгоритм Дейкстры для поиска кратчайших путей"""
        distances = {vertex: float('infinity') for vertex in graph}
        distances[start] = 0
        
        priority_queue = [(0, start)]
        visited = set()
        
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            
            if current_vertex in visited:
                continue
            
            visited.add(current_vertex)
            
            for neighbor, weight in graph[current_vertex]:
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances
    
    # Демонстрация
    print("1. Сравнение алгоритмов поиска:")
    
    # Подготовка данных
    data_size = 10000
    sorted_data = list(range(data_size))
    target = data_size // 2
    
    # Поиск
    linear_result = linear_search(sorted_data, target)
    binary_result = binary_search(sorted_data, target)
    
    print(f"   Линейный поиск нашел элемент на позиции: {linear_result}")
    print(f"   Бинарный поиск нашел элемент на позиции: {binary_result}")
    
    print("\n2. Сравнение алгоритмов сортировки:")
    
    # Небольшой массив для демонстрации
    import random
    small_data = [random.randint(1, 100) for _ in range(100)]
    
    print(f"   Исходный массив (первые 10): {small_data[:10]}")
    
    bubble_result = bubble_sort(small_data)
    quick_result = quick_sort(small_data)
    merge_result = merge_sort(small_data)
    
    print(f"   Результат сортировки (первые 10): {merge_result[:10]}")
    
    print("\n3. Алгоритм Дейкстры:")
    
    # Граф для демонстрации
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 1), ('D', 5)],
        'C': [('D', 8), ('E', 10)],
        'D': [('E', 2), ('F', 6)],
        'E': [('F', 3)],
        'F': []
    }
    
    distances = dijkstra(graph, 'A')
    print("   Кратчайшие расстояния от A:")
    for vertex, distance in distances.items():
        print(f"     До {vertex}: {distance}")
    
    print("✅ Пример 1 завершен")


def example_02_data_structures():
    """
    Пример 2: Продвинутые структуры данных
    
    Реализация и использование различных структур данных
    с анализом их производительности.
    """
    print("=== Пример 2: Продвинутые структуры данных ===")
    
    # Бинарное дерево поиска
    class TreeNode:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None
    
    class BinarySearchTree:
        """Бинарное дерево поиска"""
        
        def __init__(self):
            self.root = None
        
        def insert(self, value):
            """Вставка значения"""
            if not self.root:
                self.root = TreeNode(value)
            else:
                self._insert_recursive(self.root, value)
        
        def _insert_recursive(self, node, value):
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
        
        def search(self, value):
            """Поиск значения"""
            return self._search_recursive(self.root, value)
        
        def _search_recursive(self, node, value):
            if node is None:
                return False
            
            if value == node.value:
                return True
            elif value < node.value:
                return self._search_recursive(node.left, value)
            else:
                return self._search_recursive(node.right, value)
        
        def inorder_traversal(self):
            """Обход в порядке возрастания"""
            result = []
            self._inorder_recursive(self.root, result)
            return result
        
        def _inorder_recursive(self, node, result):
            if node:
                self._inorder_recursive(node.left, result)
                result.append(node.value)
                self._inorder_recursive(node.right, result)
    
    # Префиксное дерево (Trie)
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end_of_word = False
    
    class Trie:
        """Префиксное дерево для работы со строками"""
        
        def __init__(self):
            self.root = TrieNode()
        
        def insert(self, word):
            """Вставка слова"""
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end_of_word = True
        
        def search(self, word):
            """Поиск слова"""
            node = self.root
            for char in word:
                if char not in node.children:
                    return False
                node = node.children[char]
            return node.is_end_of_word
        
        def starts_with(self, prefix):
            """Проверка наличия слов с префиксом"""
            node = self.root
            for char in prefix:
                if char not in node.children:
                    return False
                node = node.children[char]
            return True
        
        def find_words_with_prefix(self, prefix):
            """Найти все слова с заданным префиксом"""
            node = self.root
            for char in prefix:
                if char not in node.children:
                    return []
                node = node.children[char]
            
            words = []
            self._collect_words(node, prefix, words)
            return words
        
        def _collect_words(self, node, current_word, words):
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child_node in node.children.items():
                self._collect_words(child_node, current_word + char, words)
    
    # Минимальная куча
    class MinHeap:
        """Минимальная куча"""
        
        def __init__(self):
            self.heap = []
        
        def parent(self, i):
            return (i - 1) // 2
        
        def left_child(self, i):
            return 2 * i + 1
        
        def right_child(self, i):
            return 2 * i + 2
        
        def swap(self, i, j):
            self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
        def insert(self, value):
            """Вставка элемента"""
            self.heap.append(value)
            self._heapify_up(len(self.heap) - 1)
        
        def _heapify_up(self, i):
            while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
                self.swap(i, self.parent(i))
                i = self.parent(i)
        
        def extract_min(self):
            """Извлечение минимального элемента"""
            if not self.heap:
                return None
            
            if len(self.heap) == 1:
                return self.heap.pop()
            
            min_val = self.heap[0]
            self.heap[0] = self.heap.pop()
            self._heapify_down(0)
            
            return min_val
        
        def _heapify_down(self, i):
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
        
        def peek(self):
            return self.heap[0] if self.heap else None
    
    # Демонстрация
    print("1. Бинарное дерево поиска:")
    
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    
    for value in values:
        bst.insert(value)
    
    print(f"   Вставлены значения: {values}")
    print(f"   Обход в порядке возрастания: {bst.inorder_traversal()}")
    print(f"   Поиск 40: {bst.search(40)}")
    print(f"   Поиск 90: {bst.search(90)}")
    
    print("\n2. Префиксное дерево (Trie):")
    
    trie = Trie()
    words = ["программирование", "программа", "программист", "код", "кодирование"]
    
    for word in words:
        trie.insert(word)
    
    print(f"   Вставлены слова: {words}")
    print(f"   Поиск 'программа': {trie.search('программа')}")
    print(f"   Поиск 'программ': {trie.search('программ')}")
    print(f"   Есть слова с префиксом 'программ': {trie.starts_with('программ')}")
    
    prefix_words = trie.find_words_with_prefix("програм")
    print(f"   Слова с префиксом 'програм': {prefix_words}")
    
    print("\n3. Минимальная куча:")
    
    heap = MinHeap()
    values = [10, 4, 15, 20, 25, 30]
    
    for value in values:
        heap.insert(value)
    
    print(f"   Вставлены значения: {values}")
    print(f"   Минимальный элемент: {heap.peek()}")
    
    extracted = []
    while heap.heap:
        extracted.append(heap.extract_min())
    
    print(f"   Извлечение в порядке возрастания: {extracted}")
    
    print("✅ Пример 2 завершен")


def example_03_design_patterns():
    """
    Пример 3: Паттерны проектирования
    
    Реализация основных паттернов проектирования
    с практическими примерами использования.
    """
    print("=== Пример 3: Паттерны проектирования ===")
    
    # Singleton
    class DatabaseConnection:
        """Паттерн Singleton"""
        
        _instance = None
        _initialized = False
        
        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
        
        def __init__(self):
            if not DatabaseConnection._initialized:
                self.connection_string = "database://localhost:5432"
                self.is_connected = False
                DatabaseConnection._initialized = True
        
        def connect(self):
            if not self.is_connected:
                print(f"   Подключение к {self.connection_string}")
                self.is_connected = True
                return True
            return False
        
        def disconnect(self):
            if self.is_connected:
                print("   Отключение от базы данных")
                self.is_connected = False
                return True
            return False
    
    # Factory Method
    class Document(ABC):
        @abstractmethod
        def create(self) -> str:
            pass
    
    class PDFDocument(Document):
        def create(self) -> str:
            return "PDF документ создан"
    
    class WordDocument(Document):
        def create(self) -> str:
            return "Word документ создан"
    
    class DocumentFactory:
        @staticmethod
        def create_document(doc_type: str) -> Document:
            if doc_type.lower() == "pdf":
                return PDFDocument()
            elif doc_type.lower() == "word":
                return WordDocument()
            else:
                raise ValueError(f"Неизвестный тип документа: {doc_type}")
    
    # Observer
    class Observer(ABC):
        @abstractmethod
        def update(self, subject) -> None:
            pass
    
    class Subject(ABC):
        def __init__(self):
            self._observers = []
        
        def attach(self, observer: Observer) -> None:
            self._observers.append(observer)
        
        def detach(self, observer: Observer) -> None:
            self._observers.remove(observer)
        
        def notify(self) -> None:
            for observer in self._observers:
                observer.update(self)
    
    class StockPrice(Subject):
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
        def __init__(self, name: str):
            self.name = name
        
        def update(self, subject) -> None:
            if isinstance(subject, StockPrice):
                print(f"   {self.name}: {subject.symbol} = ${subject.price:.2f}")
    
    # Strategy
    class SortStrategy(ABC):
        @abstractmethod
        def sort(self, data: List[int]) -> List[int]:
            pass
    
    class BubbleSortStrategy(SortStrategy):
        def sort(self, data: List[int]) -> List[int]:
            arr = data.copy()
            n = len(arr)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return arr
    
    class QuickSortStrategy(SortStrategy):
        def sort(self, data: List[int]) -> List[int]:
            if len(data) <= 1:
                return data
            
            pivot = data[len(data) // 2]
            left = [x for x in data if x < pivot]
            middle = [x for x in data if x == pivot]
            right = [x for x in data if x > pivot]
            
            return self.sort(left) + middle + self.sort(right)
    
    class SortContext:
        def __init__(self, strategy: SortStrategy):
            self._strategy = strategy
        
        def set_strategy(self, strategy: SortStrategy) -> None:
            self._strategy = strategy
        
        def sort_data(self, data: List[int]) -> List[int]:
            return self._strategy.sort(data)
    
    # Decorator
    class Coffee(ABC):
        @abstractmethod
        def cost(self) -> float:
            pass
        
        @abstractmethod
        def description(self) -> str:
            pass
    
    class SimpleCoffee(Coffee):
        def cost(self) -> float:
            return 50.0
        
        def description(self) -> str:
            return "Простой кофе"
    
    class CoffeeDecorator(Coffee):
        def __init__(self, coffee: Coffee):
            self._coffee = coffee
        
        def cost(self) -> float:
            return self._coffee.cost()
        
        def description(self) -> str:
            return self._coffee.description()
    
    class MilkDecorator(CoffeeDecorator):
        def cost(self) -> float:
            return self._coffee.cost() + 10.0
        
        def description(self) -> str:
            return self._coffee.description() + ", молоко"
    
    class SugarDecorator(CoffeeDecorator):
        def cost(self) -> float:
            return self._coffee.cost() + 5.0
        
        def description(self) -> str:
            return self._coffee.description() + ", сахар"
    
    # Демонстрация
    print("1. Паттерн Singleton:")
    
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"   db1 и db2 один объект: {db1 is db2}")
    db1.connect()
    print(f"   db2 подключена: {db2.is_connected}")
    
    print("\n2. Паттерн Factory Method:")
    
    pdf_doc = DocumentFactory.create_document("pdf")
    word_doc = DocumentFactory.create_document("word")
    
    print(f"   {pdf_doc.create()}")
    print(f"   {word_doc.create()}")
    
    print("\n3. Паттерн Observer:")
    
    apple_stock = StockPrice("AAPL", 150.0)
    
    mobile_display = StockDisplay("Мобильное приложение")
    web_display = StockDisplay("Веб-сайт")
    terminal_display = StockDisplay("Терминал")
    
    apple_stock.attach(mobile_display)
    apple_stock.attach(web_display)
    apple_stock.attach(terminal_display)
    
    print("   Изменение цены акции:")
    apple_stock.price = 155.0
    apple_stock.price = 148.5
    
    print("\n4. Паттерн Strategy:")
    
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Исходные данные: {data}")
    
    context = SortContext(BubbleSortStrategy())
    bubble_result = context.sort_data(data)
    print(f"   Пузырьковая сортировка: {bubble_result}")
    
    context.set_strategy(QuickSortStrategy())
    quick_result = context.sort_data(data)
    print(f"   Быстрая сортировка: {quick_result}")
    
    print("\n5. Паттерн Decorator:")
    
    # Простой кофе
    coffee = SimpleCoffee()
    print(f"   {coffee.description()}: {coffee.cost()}₽")
    
    # Кофе с молоком
    coffee_with_milk = MilkDecorator(coffee)
    print(f"   {coffee_with_milk.description()}: {coffee_with_milk.cost()}₽")
    
    # Кофе с молоком и сахаром
    coffee_with_milk_and_sugar = SugarDecorator(coffee_with_milk)
    print(f"   {coffee_with_milk_and_sugar.description()}: {coffee_with_milk_and_sugar.cost()}₽")
    
    print("✅ Пример 3 завершен")


def example_04_concurrency_and_async():
    """
    Пример 4: Параллелизм и асинхронность
    
    Демонстрация различных подходов к параллельному
    и асинхронному программированию в Python.
    """
    print("=== Пример 4: Параллелизм и асинхронность ===")
    
    # Многопоточность
    class ThreadSafeCounter:
        """Потокобезопасный счетчик"""
        
        def __init__(self):
            self._value = 0
            self._lock = threading.Lock()
        
        def increment(self):
            with self._lock:
                self._value += 1
        
        def decrement(self):
            with self._lock:
                self._value -= 1
        
        @property
        def value(self):
            with self._lock:
                return self._value
    
    def worker_thread(counter: ThreadSafeCounter, increments: int, thread_id: int):
        """Рабочий поток"""
        for _ in range(increments):
            counter.increment()
            time.sleep(0.001)  # Имитация работы
        print(f"   Поток {thread_id} завершен")
    
    # Асинхронные функции
    async def async_task(name: str, duration: float) -> str:
        """Асинхронная задача"""
        print(f"   Задача {name} началась")
        await asyncio.sleep(duration)
        print(f"   Задача {name} завершилась")
        return f"Результат {name}"
    
    async def async_web_request(url: str, delay: float) -> dict:
        """Имитация асинхронного веб-запроса"""
        print(f"   Запрос к {url} начат")
        await asyncio.sleep(delay)  # Имитация сетевой задержки
        print(f"   Запрос к {url} завершен")
        return {
            "url": url,
            "status": 200,
            "data": f"Данные от {url}"
        }
    
    async def run_concurrent_requests():
        """Запуск нескольких асинхронных запросов"""
        urls = [
            ("api.example1.com", 1.0),
            ("api.example2.com", 0.5),
            ("api.example3.com", 1.5),
            ("api.example4.com", 0.8)
        ]
        
        tasks = [async_web_request(url, delay) for url, delay in urls]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        execution_time = time.time() - start_time
        
        print(f"   Все запросы завершены за {execution_time:.2f}с")
        return results
    
    # Producer-Consumer с asyncio
    class AsyncProducerConsumer:
        """Асинхронный Producer-Consumer"""
        
        def __init__(self, max_size: int = 5):
            self.queue = asyncio.Queue(maxsize=max_size)
        
        async def producer(self, items: List[str]) -> None:
            """Производитель"""
            for item in items:
                await self.queue.put(item)
                print(f"   Произведено: {item}")
                await asyncio.sleep(0.1)
            
            # Сигнал завершения
            await self.queue.put(None)
        
        async def consumer(self, consumer_id: int) -> None:
            """Потребитель"""
            while True:
                item = await self.queue.get()
                if item is None:
                    await self.queue.put(None)  # Передаем сигнал другим
                    break
                
                print(f"   Потребитель {consumer_id} обработал: {item}")
                await asyncio.sleep(0.2)
                self.queue.task_done()
        
        async def start(self, items: List[str], num_consumers: int = 2) -> None:
            """Запуск производства и потребления"""
            tasks = []
            
            # Создаем задачи
            tasks.append(asyncio.create_task(self.producer(items)))
            
            for i in range(num_consumers):
                tasks.append(asyncio.create_task(self.consumer(i + 1)))
            
            # Ждем завершения всех задач
            await asyncio.gather(*tasks)
    
    # Демонстрация многопоточности
    def demo_threading():
        """Демонстрация многопоточности"""
        print("1. Многопоточность:")
        
        counter = ThreadSafeCounter()
        threads = []
        
        # Создаем и запускаем потоки
        for i in range(3):
            thread = threading.Thread(
                target=worker_thread,
                args=(counter, 100, i + 1)
            )
            threads.append(thread)
            thread.start()
        
        # Ждем завершения всех потоков
        for thread in threads:
            thread.join()
        
        print(f"   Финальное значение счетчика: {counter.value}")
    
    # Демонстрация асинхронности
    async def demo_async():
        """Демонстрация асинхронности"""
        print("\n2. Асинхронное программирование:")
        
        # Последовательное выполнение
        print("   Последовательное выполнение:")
        start_time = time.time()
        
        await async_task("A", 1.0)
        await async_task("B", 0.5)
        await async_task("C", 1.5)
        
        sequential_time = time.time() - start_time
        print(f"   Общее время: {sequential_time:.2f}с")
        
        # Параллельное выполнение
        print("\n   Параллельное выполнение:")
        start_time = time.time()
        
        tasks = [
            async_task("X", 1.0),
            async_task("Y", 0.5),
            async_task("Z", 1.5)
        ]
        
        results = await asyncio.gather(*tasks)
        parallel_time = time.time() - start_time
        
        print(f"   Общее время: {parallel_time:.2f}с")
        print(f"   Ускорение: {sequential_time / parallel_time:.2f}x")
        
        # Веб-запросы
        print("\n3. Асинхронные веб-запросы:")
        await run_concurrent_requests()
        
        # Producer-Consumer
        print("\n4. Асинхронный Producer-Consumer:")
        pc = AsyncProducerConsumer()
        items = [f"item_{i}" for i in range(10)]
        await pc.start(items, 2)
    
    # Запуск демонстраций
    demo_threading()
    
    # Запуск асинхронной демонстрации
    try:
        asyncio.run(demo_async())
    except Exception as e:
        print(f"   Ошибка в асинхронном коде: {e}")
    
    print("✅ Пример 4 завершен")


def example_05_performance_optimization():
    """
    Пример 5: Оптимизация производительности
    
    Практические техники оптимизации Python кода
    с измерением производительности.
    """
    print("=== Пример 5: Оптимизация производительности ===")
    
    import cProfile
    import functools
    from collections import defaultdict
    
    def timing_decorator(func):
        """Декоратор для измерения времени выполнения"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            print(f"   {func.__name__}: {execution_time:.4f}с")
            return result
        return wrapper
    
    # Оптимизация строк
    @timing_decorator
    def inefficient_string_concatenation(strings: List[str]) -> str:
        """Неэффективная конкатенация строк"""
        result = ""
        for s in strings:
            result += s
        return result
    
    @timing_decorator
    def efficient_string_concatenation(strings: List[str]) -> str:
        """Эффективная конкатенация строк"""
        return "".join(strings)
    
    # Оптимизация поиска
    @timing_decorator
    def inefficient_list_search(data: List[int], targets: List[int]) -> List[bool]:
        """Неэффективный поиск в списке"""
        results = []
        for target in targets:
            found = False
            for item in data:
                if item == target:
                    found = True
                    break
            results.append(found)
        return results
    
    @timing_decorator
    def efficient_set_search(data: set, targets: List[int]) -> List[bool]:
        """Эффективный поиск в множестве"""
        return [target in data for target in targets]
    
    # Кэширование
    def fibonacci_no_cache(n: int) -> int:
        """Фибоначчи без кэширования"""
        if n <= 1:
            return n
        return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)
    
    @functools.lru_cache(maxsize=None)
    def fibonacci_with_cache(n: int) -> int:
        """Фибоначчи с кэшированием"""
        if n <= 1:
            return n
        return fibonacci_with_cache(n - 1) + fibonacci_with_cache(n - 2)
    
    # Оптимизация циклов
    @timing_decorator
    def inefficient_loop(data: List[dict]) -> int:
        """Неэффективный цикл с многократными вычислениями"""
        total = 0
        for item in data:
            if len(item.keys()) > 2:  # Пересчет на каждой итерации
                if 'value' in item.keys():  # Еще один пересчет
                    total += item['value']
        return total
    
    @timing_decorator
    def efficient_loop(data: List[dict]) -> int:
        """Эффективный цикл с предварительными вычислениями"""
        total = 0
        for item in data:
            keys = item.keys()  # Вычисляем один раз
            if len(keys) > 2:
                if 'value' in item:  # Используем оптимизированную проверку
                    total += item['value']
        return total
    
    # List comprehension vs циклы
    @timing_decorator
    def traditional_loop(numbers: List[int]) -> List[int]:
        """Традиционный цикл"""
        result = []
        for num in numbers:
            if num % 2 == 0:
                result.append(num * num)
        return result
    
    @timing_decorator
    def list_comprehension(numbers: List[int]) -> List[int]:
        """List comprehension"""
        return [num * num for num in numbers if num % 2 == 0]
    
    # Генераторы vs списки
    @timing_decorator
    def memory_intensive_list(n: int) -> List[int]:
        """Создание большого списка в памяти"""
        return [x * x for x in range(n)]
    
    def memory_efficient_generator(n: int):
        """Генератор для экономии памяти"""
        for x in range(n):
            yield x * x
    
    @timing_decorator
    def process_with_generator(n: int) -> int:
        """Обработка данных через генератор"""
        total = 0
        gen = memory_efficient_generator(n)
        for value in gen:
            total += value
            if total > 1000000:  # Можем остановиться досрочно
                break
        return total
    
    # Профилирование функции
    def profile_function():
        """Функция для профилирования"""
        
        def slow_function():
            """Медленная функция для анализа"""
            total = 0
            for i in range(100000):
                total += i ** 2
                if i % 1000 == 0:
                    time.sleep(0.001)  # Имитация I/O операции
            return total
        
        # Профилирование
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = slow_function()
        
        profiler.disable()
        
        print("   Результаты профилирования:")
        profiler.print_stats(sort='cumulative')
        
        return result
    
    # Демонстрация
    print("1. Оптимизация конкатенации строк:")
    
    strings = ["строка" + str(i) for i in range(1000)]
    
    inefficient_string_concatenation(strings)
    efficient_string_concatenation(strings)
    
    print("\n2. Оптимизация поиска:")
    
    data_list = list(range(10000))
    data_set = set(data_list)
    targets = [100, 500, 1000, 5000, 9999]
    
    inefficient_list_search(data_list, targets)
    efficient_set_search(data_set, targets)
    
    print("\n3. Эффект кэширования (Фибоначчи):")
    
    n = 30
    
    start_time = time.perf_counter()
    result_no_cache = fibonacci_no_cache(n)
    time_no_cache = time.perf_counter() - start_time
    
    start_time = time.perf_counter()
    result_with_cache = fibonacci_with_cache(n)
    time_with_cache = time.perf_counter() - start_time
    
    print(f"   Без кэша: {time_no_cache:.4f}с, результат: {result_no_cache}")
    print(f"   С кэшем: {time_with_cache:.4f}с, результат: {result_with_cache}")
    print(f"   Ускорение: {time_no_cache / time_with_cache:.2f}x")
    
    print("\n4. Оптимизация циклов:")
    
    test_data = [
        {'name': f'item_{i}', 'value': i, 'type': 'test'}
        for i in range(10000)
    ]
    
    inefficient_loop(test_data)
    efficient_loop(test_data)
    
    print("\n5. List comprehension vs циклы:")
    
    numbers = list(range(100000))
    
    traditional_loop(numbers)
    list_comprehension(numbers)
    
    print("\n6. Генераторы vs списки:")
    
    n = 1000000
    
    print("   Создание списка в памяти:")
    memory_intensive_list(n)
    
    print("   Обработка через генератор:")
    process_with_generator(n)
    
    print("\n7. Профилирование кода:")
    # profile_function()  # Закомментировано для краткости вывода
    print("   (Профилирование отключено для краткости)")
    
    print("✅ Пример 5 завершен")


def main():
    """
    Главная функция для запуска всех примеров
    """
    examples = [
        ("Алгоритмы и анализ сложности", example_01_algorithms_and_complexity),
        ("Продвинутые структуры данных", example_02_data_structures),
        ("Паттерны проектирования", example_03_design_patterns),
        ("Параллелизм и асинхронность", example_04_concurrency_and_async),
        ("Оптимизация производительности", example_05_performance_optimization),
    ]
    
    print("🏗️ Примеры: Архитектура и CS фундамент в Python")
    print("=" * 70)
    print("Эти примеры демонстрируют:")
    print("- Фундаментальные алгоритмы и структуры данных")
    print("- Классические паттерны проектирования")
    print("- Современные подходы к параллелизму")
    print("- Техники оптимизации производительности")
    print("- Принципы архитектурного проектирования")
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
    
    print("\n🎉 Все примеры архитектуры и CS фундамента завершены!")


if __name__ == "__main__":
    main() 