#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Архитектура и CS фундамент в Python

Этот файл содержит практические упражнения для закрепления знаний:
- Алгоритмы и структуры данных
- Паттерны проектирования  
- Системная архитектура
- Производительность и оптимизация
"""

import asyncio
import threading
import time
import heapq
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Callable, TypeVar, Generic, Protocol
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum
import functools
import random


def exercise_01_advanced_data_structures_system():
    """
    Упражнение 1: Система продвинутых структур данных
    
    Задача:
    Создайте систему для эффективного хранения и поиска текстовых документов
    с использованием различных структур данных: Trie, BST, Hash Tables и Heap.
    """
    print("=== Упражнение 1: Система продвинутых структур данных ===")
    
    # РЕШЕНИЕ:
    
    @dataclass
    class Document:
        """Документ в системе"""
        id: int
        title: str
        content: str
        tags: List[str]
        priority: int = 1
        created_at: float = field(default_factory=time.time)
        
        def __lt__(self, other):
            """Для сортировки по приоритету"""
            return self.priority > other.priority  # Высокий приоритет = меньше в куче
    
    class TrieNode:
        """Узел Trie для быстрого поиска по префиксу"""
        
        def __init__(self):
            self.children = {}
            self.document_ids = set()
            self.is_end_of_word = False
    
    class DocumentTrie:
        """Trie для поиска документов по ключевым словам"""
        
        def __init__(self):
            self.root = TrieNode()
        
        def insert_document(self, document: Document):
            """Добавить документ в Trie"""
            words = self._extract_words(document)
            
            for word in words:
                node = self.root
                for char in word.lower():
                    if char not in node.children:
                        node.children[char] = TrieNode()
                    node = node.children[char]
                    node.document_ids.add(document.id)
                
                node.is_end_of_word = True
        
        def search_by_prefix(self, prefix: str) -> set:
            """Найти документы по префиксу"""
            node = self.root
            prefix = prefix.lower()
            
            for char in prefix:
                if char not in node.children:
                    return set()
                node = node.children[char]
            
            return node.document_ids
        
        def search_by_word(self, word: str) -> set:
            """Найти документы по полному слову"""
            node = self.root
            word = word.lower()
            
            for char in word:
                if char not in node.children:
                    return set()
                node = node.children[char]
            
            return node.document_ids if node.is_end_of_word else set()
        
        def _extract_words(self, document: Document) -> List[str]:
            """Извлечь слова из документа"""
            import re
            text = f"{document.title} {document.content} {' '.join(document.tags)}"
            words = re.findall(r'\b\w+\b', text)
            return [word for word in words if len(word) > 2]
    
    class DocumentBST:
        """BST для сортированного хранения документов по ID"""
        
        class Node:
            def __init__(self, document: Document):
                self.document = document
                self.left = None
                self.right = None
        
        def __init__(self):
            self.root = None
        
        def insert(self, document: Document):
            """Вставить документ"""
            if not self.root:
                self.root = self.Node(document)
            else:
                self._insert_recursive(self.root, document)
        
        def _insert_recursive(self, node, document):
            """Рекурсивная вставка"""
            if document.id < node.document.id:
                if node.left is None:
                    node.left = self.Node(document)
                else:
                    self._insert_recursive(node.left, document)
            else:
                if node.right is None:
                    node.right = self.Node(document)
                else:
                    self._insert_recursive(node.right, document)
        
        def find_by_id(self, doc_id: int) -> Optional[Document]:
            """Найти документ по ID"""
            return self._find_recursive(self.root, doc_id)
        
        def _find_recursive(self, node, doc_id):
            """Рекурсивный поиск"""
            if node is None:
                return None
            
            if doc_id == node.document.id:
                return node.document
            elif doc_id < node.document.id:
                return self._find_recursive(node.left, doc_id)
            else:
                return self._find_recursive(node.right, doc_id)
        
        def get_documents_in_range(self, min_id: int, max_id: int) -> List[Document]:
            """Получить документы в диапазоне ID"""
            result = []
            self._range_search(self.root, min_id, max_id, result)
            return result
        
        def _range_search(self, node, min_id, max_id, result):
            """Поиск в диапазоне"""
            if node is None:
                return
            
            if min_id <= node.document.id <= max_id:
                result.append(node.document)
            
            if min_id < node.document.id:
                self._range_search(node.left, min_id, max_id, result)
            
            if max_id > node.document.id:
                self._range_search(node.right, min_id, max_id, result)
    
    class DocumentSearchSystem:
        """Система поиска документов"""
        
        def __init__(self):
            self.documents = {}  # Hash table для O(1) доступа
            self.trie = DocumentTrie()  # Для поиска по содержимому
            self.bst = DocumentBST()  # Для сортированного доступа
            self.priority_heap = []  # Для приоритетной очереди
            self.tag_index = defaultdict(set)  # Индекс по тегам
            self.next_id = 1
        
        def add_document(self, title: str, content: str, tags: List[str], priority: int = 1) -> Document:
            """Добавить документ в систему"""
            document = Document(
                id=self.next_id,
                title=title,
                content=content,
                tags=tags,
                priority=priority
            )
            
            # Добавляем во все структуры данных
            self.documents[document.id] = document
            self.trie.insert_document(document)
            self.bst.insert(document)
            heapq.heappush(self.priority_heap, document)
            
            # Индексируем по тегам
            for tag in tags:
                self.tag_index[tag].add(document.id)
            
            self.next_id += 1
            return document
        
        def get_document_by_id(self, doc_id: int) -> Optional[Document]:
            """Получить документ по ID - O(1)"""
            return self.documents.get(doc_id)
        
        def search_by_content(self, query: str) -> List[Document]:
            """Поиск по содержимому"""
            words = query.split()
            result_ids = None
            
            for word in words:
                word_ids = self.trie.search_by_word(word)
                if result_ids is None:
                    result_ids = word_ids
                else:
                    result_ids = result_ids.intersection(word_ids)
                
                if not result_ids:
                    break
            
            return [self.documents[doc_id] for doc_id in (result_ids or [])]
        
        def search_by_prefix(self, prefix: str) -> List[Document]:
            """Поиск по префиксу"""
            doc_ids = self.trie.search_by_prefix(prefix)
            return [self.documents[doc_id] for doc_id in doc_ids]
        
        def search_by_tags(self, tags: List[str]) -> List[Document]:
            """Поиск по тегам"""
            if not tags:
                return []
            
            result_ids = self.tag_index[tags[0]]
            for tag in tags[1:]:
                result_ids = result_ids.intersection(self.tag_index[tag])
            
            return [self.documents[doc_id] for doc_id in result_ids]
        
        def get_documents_by_id_range(self, min_id: int, max_id: int) -> List[Document]:
            """Получить документы в диапазоне ID"""
            return self.bst.get_documents_in_range(min_id, max_id)
        
        def get_top_priority_documents(self, count: int) -> List[Document]:
            """Получить документы с наивысшим приоритетом"""
            temp_heap = self.priority_heap.copy()
            result = []
            
            for _ in range(min(count, len(temp_heap))):
                if temp_heap:
                    result.append(heapq.heappop(temp_heap))
            
            return result
        
        def complex_search(self, content_query: str = "", tags: List[str] = None, 
                          min_priority: int = 0) -> List[Document]:
            """Комплексный поиск с несколькими критериями"""
            candidates = set(self.documents.keys())
            
            # Фильтр по содержимому
            if content_query:
                content_docs = self.search_by_content(content_query)
                content_ids = {doc.id for doc in content_docs}
                candidates = candidates.intersection(content_ids)
            
            # Фильтр по тегам
            if tags:
                tag_docs = self.search_by_tags(tags)
                tag_ids = {doc.id for doc in tag_docs}
                candidates = candidates.intersection(tag_ids)
            
            # Фильтр по приоритету
            result = []
            for doc_id in candidates:
                doc = self.documents[doc_id]
                if doc.priority >= min_priority:
                    result.append(doc)
            
            # Сортируем по приоритету
            result.sort(key=lambda x: x.priority, reverse=True)
            return result
        
        def get_statistics(self) -> Dict[str, Any]:
            """Получить статистику системы"""
            return {
                "total_documents": len(self.documents),
                "total_tags": len(self.tag_index),
                "average_priority": sum(doc.priority for doc in self.documents.values()) / len(self.documents) if self.documents else 0,
                "documents_by_priority": {
                    f"priority_{i}": len([doc for doc in self.documents.values() if doc.priority == i])
                    for i in range(1, 6)
                }
            }
    
    # Демонстрация
    print("Создание системы поиска документов...")
    
    search_system = DocumentSearchSystem()
    
    # Добавляем тестовые документы
    documents_data = [
        ("Алгоритмы сортировки", "Изучение различных алгоритмов сортировки: быстрая, слиянием, пузырьком", ["алгоритмы", "сортировка", "CS"], 5),
        ("Структуры данных", "Основные структуры данных: массивы, списки, деревья, графы", ["структуры", "данные", "CS"], 4),
        ("Python основы", "Базовые концепции программирования на Python", ["python", "основы", "программирование"], 3),
        ("Веб-разработка", "Создание веб-приложений с использованием Flask и Django", ["веб", "flask", "django", "python"], 4),
        ("Машинное обучение", "Введение в ML: алгоритмы классификации и регрессии", ["ML", "алгоритмы", "классификация"], 5),
        ("Базы данных", "Проектирование и оптимизация баз данных", ["БД", "SQL", "оптимизация"], 3),
        ("Архитектура ПО", "Паттерны проектирования и принципы SOLID", ["архитектура", "паттерны", "SOLID"], 4),
    ]
    
    for title, content, tags, priority in documents_data:
        doc = search_system.add_document(title, content, tags, priority)
        print(f"Добавлен документ: {doc.title} (ID: {doc.id}, Приоритет: {doc.priority})")
    
    print("\n1. Поиск по ID:")
    doc = search_system.get_document_by_id(3)
    if doc:
        print(f"   Найден документ: {doc.title}")
    
    print("\n2. Поиск по содержимому:")
    results = search_system.search_by_content("алгоритмы")
    print(f"   Найдено документов со словом 'алгоритмы': {len(results)}")
    for doc in results:
        print(f"     - {doc.title}")
    
    print("\n3. Поиск по префиксу:")
    results = search_system.search_by_prefix("алгор")
    print(f"   Найдено документов с префиксом 'алгор': {len(results)}")
    for doc in results:
        print(f"     - {doc.title}")
    
    print("\n4. Поиск по тегам:")
    results = search_system.search_by_tags(["python"])
    print(f"   Найдено документов с тегом 'python': {len(results)}")
    for doc in results:
        print(f"     - {doc.title}")
    
    print("\n5. Документы в диапазоне ID:")
    results = search_system.get_documents_by_id_range(2, 5)
    print(f"   Документы с ID от 2 до 5: {len(results)}")
    for doc in results:
        print(f"     - {doc.title} (ID: {doc.id})")
    
    print("\n6. Топ приоритетных документов:")
    results = search_system.get_top_priority_documents(3)
    print(f"   Топ 3 документа по приоритету:")
    for doc in results:
        print(f"     - {doc.title} (Приоритет: {doc.priority})")
    
    print("\n7. Комплексный поиск:")
    results = search_system.complex_search(
        content_query="алгоритмы", 
        tags=["CS"], 
        min_priority=4
    )
    print(f"   Комплексный поиск (алгоритмы + CS + приоритет >= 4): {len(results)}")
    for doc in results:
        print(f"     - {doc.title} (Приоритет: {doc.priority})")
    
    print("\n8. Статистика системы:")
    stats = search_system.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("✅ Упражнение 1 завершено")


def exercise_02_distributed_task_system():
    """
    Упражнение 2: Распределенная система обработки задач
    
    Задача:
    Создайте систему для распределенной обработки задач с использованием
    паттернов проектирования: Observer, Strategy, Command, Factory.
    """
    print("=== Упражнение 2: Распределенная система обработки задач ===")
    
    # РЕШЕНИЕ:
    
    from abc import ABC, abstractmethod
    from enum import Enum
    import uuid
    import json
    
    # Типы задач
    class TaskType(Enum):
        CPU_INTENSIVE = "cpu_intensive"
        IO_BOUND = "io_bound"
        NETWORK = "network"
        DATA_PROCESSING = "data_processing"
    
    class TaskStatus(Enum):
        PENDING = "pending"
        RUNNING = "running"
        COMPLETED = "completed"
        FAILED = "failed"
        CANCELLED = "cancelled"
    
    # Command Pattern - Задачи как команды
    class Task(ABC):
        """Абстрактная задача"""
        
        def __init__(self, task_id: str = None, priority: int = 1, 
                     max_retries: int = 3, timeout: float = 30.0):
            self.task_id = task_id or str(uuid.uuid4())
            self.priority = priority
            self.status = TaskStatus.PENDING
            self.result = None
            self.error = None
            self.max_retries = max_retries
            self.retry_count = 0
            self.timeout = timeout
            self.created_at = time.time()
            self.started_at = None
            self.completed_at = None
        
        @abstractmethod
        def execute(self) -> Any:
            """Выполнить задачу"""
            pass
        
        @abstractmethod
        def get_task_type(self) -> TaskType:
            """Получить тип задачи"""
            pass
        
        def __lt__(self, other):
            """Для сортировки по приоритету"""
            return self.priority > other.priority
        
        def to_dict(self) -> Dict[str, Any]:
            """Сериализация задачи"""
            return {
                "task_id": self.task_id,
                "type": self.get_task_type().value,
                "priority": self.priority,
                "status": self.status.value,
                "result": self.result,
                "error": self.error,
                "retry_count": self.retry_count,
                "created_at": self.created_at,
                "started_at": self.started_at,
                "completed_at": self.completed_at
            }
    
    # Конкретные типы задач
    class CPUIntensiveTask(Task):
        """CPU-интенсивная задача"""
        
        def __init__(self, operation: str, data: Any, **kwargs):
            super().__init__(**kwargs)
            self.operation = operation
            self.data = data
        
        def execute(self) -> Any:
            """Выполнить CPU операцию"""
            if self.operation == "fibonacci":
                return self._fibonacci(self.data)
            elif self.operation == "prime_check":
                return self._is_prime(self.data)
            elif self.operation == "matrix_multiply":
                return self._matrix_multiply(self.data)
            else:
                raise ValueError(f"Неизвестная операция: {self.operation}")
        
        def get_task_type(self) -> TaskType:
            return TaskType.CPU_INTENSIVE
        
        def _fibonacci(self, n: int) -> int:
            """Вычисление числа Фибоначчи"""
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
        
        def _is_prime(self, n: int) -> bool:
            """Проверка на простоту"""
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        def _matrix_multiply(self, matrices: tuple) -> List[List[int]]:
            """Умножение матриц"""
            a, b = matrices
            result = [[0] * len(b[0]) for _ in range(len(a))]
            for i in range(len(a)):
                for j in range(len(b[0])):
                    for k in range(len(b)):
                        result[i][j] += a[i][k] * b[k][j]
            return result
    
    class IOBoundTask(Task):
        """I/O задача"""
        
        def __init__(self, operation: str, data: Any, **kwargs):
            super().__init__(**kwargs)
            self.operation = operation
            self.data = data
        
        def execute(self) -> Any:
            """Выполнить I/O операцию"""
            if self.operation == "read_file":
                return self._read_file(self.data)
            elif self.operation == "write_file":
                return self._write_file(self.data)
            elif self.operation == "database_query":
                return self._database_query(self.data)
            else:
                raise ValueError(f"Неизвестная операция: {self.operation}")
        
        def get_task_type(self) -> TaskType:
            return TaskType.IO_BOUND
        
        def _read_file(self, filename: str) -> str:
            """Имитация чтения файла"""
            time.sleep(0.5)  # Имитация I/O
            return f"Содержимое файла {filename}"
        
        def _write_file(self, file_data: dict) -> bool:
            """Имитация записи файла"""
            time.sleep(0.3)  # Имитация I/O
            return True
        
        def _database_query(self, query: str) -> List[dict]:
            """Имитация запроса к БД"""
            time.sleep(0.7)  # Имитация запроса
            return [{"id": i, "data": f"result_{i}"} for i in range(5)]
    
    # Factory Pattern - Фабрика задач
    class TaskFactory:
        """Фабрика для создания задач"""
        
        @staticmethod
        def create_task(task_type: TaskType, operation: str, data: Any, **kwargs) -> Task:
            """Создать задачу по типу"""
            if task_type == TaskType.CPU_INTENSIVE:
                return CPUIntensiveTask(operation, data, **kwargs)
            elif task_type == TaskType.IO_BOUND:
                return IOBoundTask(operation, data, **kwargs)
            else:
                raise ValueError(f"Неподдерживаемый тип задачи: {task_type}")
    
    # Strategy Pattern - Стратегии планирования
    class SchedulingStrategy(ABC):
        """Абстрактная стратегия планирования"""
        
        @abstractmethod
        def select_next_task(self, tasks: List[Task]) -> Optional[Task]:
            """Выбрать следующую задачу для выполнения"""
            pass
    
    class PrioritySchedulingStrategy(SchedulingStrategy):
        """Планирование по приоритету"""
        
        def select_next_task(self, tasks: List[Task]) -> Optional[Task]:
            if not tasks:
                return None
            return max(tasks, key=lambda t: t.priority)
    
    class FIFOSchedulingStrategy(SchedulingStrategy):
        """Планирование FIFO"""
        
        def select_next_task(self, tasks: List[Task]) -> Optional[Task]:
            if not tasks:
                return None
            return min(tasks, key=lambda t: t.created_at)
    
    class ShortestJobFirstStrategy(SchedulingStrategy):
        """Планирование по времени выполнения"""
        
        def select_next_task(self, tasks: List[Task]) -> Optional[Task]:
            if not tasks:
                return None
            # Предполагаем, что I/O задачи быстрее CPU
            io_tasks = [t for t in tasks if t.get_task_type() == TaskType.IO_BOUND]
            if io_tasks:
                return min(io_tasks, key=lambda t: t.created_at)
            return min(tasks, key=lambda t: t.created_at)
    
    # Observer Pattern - Наблюдатели за событиями
    class TaskObserver(ABC):
        """Абстрактный наблюдатель за задачами"""
        
        @abstractmethod
        def on_task_started(self, task: Task) -> None:
            pass
        
        @abstractmethod
        def on_task_completed(self, task: Task) -> None:
            pass
        
        @abstractmethod
        def on_task_failed(self, task: Task) -> None:
            pass
    
    class TaskLogger(TaskObserver):
        """Логгер задач"""
        
        def __init__(self, name: str):
            self.name = name
            self.logs = []
        
        def on_task_started(self, task: Task) -> None:
            log_entry = f"[{self.name}] Задача {task.task_id} запущена"
            self.logs.append(log_entry)
            print(f"   📝 {log_entry}")
        
        def on_task_completed(self, task: Task) -> None:
            duration = task.completed_at - task.started_at if task.completed_at and task.started_at else 0
            log_entry = f"[{self.name}] Задача {task.task_id} завершена за {duration:.2f}с"
            self.logs.append(log_entry)
            print(f"   ✅ {log_entry}")
        
        def on_task_failed(self, task: Task) -> None:
            log_entry = f"[{self.name}] Задача {task.task_id} завершена с ошибкой: {task.error}"
            self.logs.append(log_entry)
            print(f"   ❌ {log_entry}")
    
    class TaskMetricsCollector(TaskObserver):
        """Сборщик метрик"""
        
        def __init__(self):
            self.metrics = {
                "tasks_started": 0,
                "tasks_completed": 0,
                "tasks_failed": 0,
                "total_execution_time": 0.0,
                "tasks_by_type": defaultdict(int)
            }
        
        def on_task_started(self, task: Task) -> None:
            self.metrics["tasks_started"] += 1
            self.metrics["tasks_by_type"][task.get_task_type().value] += 1
        
        def on_task_completed(self, task: Task) -> None:
            self.metrics["tasks_completed"] += 1
            if task.started_at and task.completed_at:
                self.metrics["total_execution_time"] += task.completed_at - task.started_at
        
        def on_task_failed(self, task: Task) -> None:
            self.metrics["tasks_failed"] += 1
        
        def get_metrics(self) -> Dict[str, Any]:
            """Получить метрики"""
            avg_time = (self.metrics["total_execution_time"] / 
                       self.metrics["tasks_completed"]) if self.metrics["tasks_completed"] > 0 else 0
            
            return {
                **self.metrics,
                "average_execution_time": avg_time,
                "success_rate": (self.metrics["tasks_completed"] / 
                               max(1, self.metrics["tasks_started"])) * 100
            }
    
    # Основная система
    class DistributedTaskSystem:
        """Распределенная система обработки задач"""
        
        def __init__(self, scheduling_strategy: SchedulingStrategy, max_workers: int = 3):
            self.scheduling_strategy = scheduling_strategy
            self.max_workers = max_workers
            self.task_queue = []
            self.running_tasks = {}
            self.completed_tasks = {}
            self.observers = []
            self.workers_busy = 0
            self.is_running = False
        
        def add_observer(self, observer: TaskObserver) -> None:
            """Добавить наблюдателя"""
            self.observers.append(observer)
        
        def remove_observer(self, observer: TaskObserver) -> None:
            """Удалить наблюдателя"""
            self.observers.remove(observer)
        
        def submit_task(self, task: Task) -> None:
            """Добавить задачу в очередь"""
            self.task_queue.append(task)
            print(f"   📤 Задача {task.task_id} добавлена в очередь")
        
        def _notify_task_started(self, task: Task) -> None:
            """Уведомить о запуске задачи"""
            for observer in self.observers:
                observer.on_task_started(task)
        
        def _notify_task_completed(self, task: Task) -> None:
            """Уведомить о завершении задачи"""
            for observer in self.observers:
                observer.on_task_completed(task)
        
        def _notify_task_failed(self, task: Task) -> None:
            """Уведомить о сбое задачи"""
            for observer in self.observers:
                observer.on_task_failed(task)
        
        async def _execute_task(self, task: Task) -> None:
            """Выполнить задачу асинхронно"""
            try:
                self.workers_busy += 1
                task.status = TaskStatus.RUNNING
                task.started_at = time.time()
                self.running_tasks[task.task_id] = task
                
                self._notify_task_started(task)
                
                # Выполняем задачу
                await asyncio.get_event_loop().run_in_executor(
                    None, self._run_task_sync, task
                )
                
                task.status = TaskStatus.COMPLETED
                task.completed_at = time.time()
                self._notify_task_completed(task)
                
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.completed_at = time.time()
                self._notify_task_failed(task)
                
                # Повторная попытка
                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    task.status = TaskStatus.PENDING
                    self.task_queue.append(task)
                    print(f"   🔄 Повторная попытка для задачи {task.task_id} ({task.retry_count}/{task.max_retries})")
            
            finally:
                self.workers_busy -= 1
                if task.task_id in self.running_tasks:
                    del self.running_tasks[task.task_id]
                    self.completed_tasks[task.task_id] = task
        
        def _run_task_sync(self, task: Task) -> Any:
            """Синхронное выполнение задачи"""
            return task.execute()
        
        async def run(self, duration: float = 10.0) -> None:
            """Запустить систему на определенное время"""
            self.is_running = True
            start_time = time.time()
            
            print(f"   🚀 Система запущена на {duration}с")
            
            while self.is_running and (time.time() - start_time) < duration:
                # Выбираем задачи для выполнения
                while (self.workers_busy < self.max_workers and 
                       self.task_queue and self.is_running):
                    
                    # Выбираем следующую задачу по стратегии
                    next_task = self.scheduling_strategy.select_next_task(self.task_queue)
                    if next_task:
                        self.task_queue.remove(next_task)
                        # Запускаем задачу асинхронно
                        asyncio.create_task(self._execute_task(next_task))
                
                await asyncio.sleep(0.1)  # Небольшая пауза
            
            # Ждем завершения всех запущенных задач
            while self.running_tasks:
                await asyncio.sleep(0.1)
            
            self.is_running = False
            print("   🛑 Система остановлена")
        
        def stop(self) -> None:
            """Остановить систему"""
            self.is_running = False
        
        def get_status(self) -> Dict[str, Any]:
            """Получить статус системы"""
            return {
                "is_running": self.is_running,
                "workers_busy": self.workers_busy,
                "queue_length": len(self.task_queue),
                "running_tasks": len(self.running_tasks),
                "completed_tasks": len(self.completed_tasks),
                "scheduling_strategy": self.scheduling_strategy.__class__.__name__
            }
    
    # Демонстрация
    async def run_demo():
        print("Создание распределенной системы обработки задач...")
        
        # Создаем систему с приоритетным планированием
        system = DistributedTaskSystem(
            scheduling_strategy=PrioritySchedulingStrategy(),
            max_workers=2
        )
        
        # Добавляем наблюдателей
        logger = TaskLogger("SystemLogger")
        metrics = TaskMetricsCollector()
        
        system.add_observer(logger)
        system.add_observer(metrics)
        
        # Создаем различные задачи
        tasks = [
            TaskFactory.create_task(TaskType.CPU_INTENSIVE, "fibonacci", 35, priority=5),
            TaskFactory.create_task(TaskType.IO_BOUND, "read_file", "data.txt", priority=3),
            TaskFactory.create_task(TaskType.CPU_INTENSIVE, "prime_check", 982451653, priority=4),
            TaskFactory.create_task(TaskType.IO_BOUND, "database_query", "SELECT * FROM users", priority=2),
            TaskFactory.create_task(TaskType.CPU_INTENSIVE, "matrix_multiply", 
                                  ([[1, 2], [3, 4]], [[5, 6], [7, 8]]), priority=1),
        ]
        
        print(f"\nДобавление {len(tasks)} задач в систему:")
        for task in tasks:
            system.submit_task(task)
        
        print(f"\nСтатус системы перед запуском:")
        status = system.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        print(f"\nЗапуск системы...")
        await system.run(duration=8.0)
        
        print(f"\nФинальная статистика:")
        final_metrics = metrics.get_metrics()
        for key, value in final_metrics.items():
            print(f"   {key}: {value}")
        
        print(f"\nПоследние 5 записей лога:")
        for log_entry in logger.logs[-5:]:
            print(f"   {log_entry}")
    
    try:
        asyncio.run(run_demo())
    except Exception as e:
        print(f"Ошибка в демонстрации: {e}")
    
    print("✅ Упражнение 2 завершено")


def exercise_03_performance_optimization_system():
    """
    Упражнение 3: Система оптимизации производительности
    
    Задача:
    Создайте систему для автоматической оптимизации производительности
    с профилированием, кэшированием и различными стратегиями оптимизации.
    """
    print("=== Упражнение 3: Система оптимизации производительности ===")
    
    # РЕШЕНИЕ:
    
    import cProfile
    import pstats
    import io
    from typing import Any, Callable
    import functools
    import weakref
    
    # Декораторы для оптимизации
    class PerformanceOptimizer:
        """Система оптимизации производительности"""
        
        def __init__(self):
            self.cache_stats = defaultdict(lambda: {"hits": 0, "misses": 0})
            self.timing_stats = defaultdict(list)
            self.profiling_data = {}
        
        def timing_decorator(self, func: Callable) -> Callable:
            """Декоратор для измерения времени выполнения"""
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.perf_counter()
                    execution_time = end_time - start_time
                    self.timing_stats[func.__name__].append(execution_time)
            return wrapper
        
        def cache_decorator(self, maxsize: int = 128, ttl: float = None) -> Callable:
            """Продвинутый кэш с TTL"""
            def decorator(func: Callable) -> Callable:
                cache = {}
                cache_info = {"hits": 0, "misses": 0}
                
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    # Создаем ключ кэша
                    key = str(args) + str(sorted(kwargs.items()))
                    current_time = time.time()
                    
                    # Проверяем кэш
                    if key in cache:
                        cached_result, timestamp = cache[key]
                        
                        # Проверяем TTL
                        if ttl is None or (current_time - timestamp) < ttl:
                            cache_info["hits"] += 1
                            self.cache_stats[func.__name__]["hits"] += 1
                            return cached_result
                        else:
                            # Удаляем устаревшую запись
                            del cache[key]
                    
                    # Вычисляем результат
                    cache_info["misses"] += 1
                    self.cache_stats[func.__name__]["misses"] += 1
                    result = func(*args, **kwargs)
                    
                    # Сохраняем в кэш
                    if len(cache) >= maxsize:
                        # Удаляем старейшую запись (FIFO)
                        oldest_key = next(iter(cache))
                        del cache[oldest_key]
                    
                    cache[key] = (result, current_time)
                    return result
                
                wrapper.cache_info = lambda: cache_info.copy()
                wrapper.cache_clear = lambda: cache.clear()
                return wrapper
            return decorator
        
        def profile_decorator(self, func: Callable) -> Callable:
            """Декоратор для профилирования"""
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                profiler = cProfile.Profile()
                profiler.enable()
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    profiler.disable()
                    
                    # Сохраняем статистику
                    s = io.StringIO()
                    ps = pstats.Stats(profiler, stream=s)
                    ps.sort_stats('cumulative')
                    ps.print_stats(10)  # Топ 10 функций
                    
                    self.profiling_data[func.__name__] = s.getvalue()
            
            return wrapper
        
        def memoize_decorator(self, func: Callable) -> Callable:
            """Мемоизация с использованием weak references"""
            memo = weakref.WeakValueDictionary()
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = str(args) + str(sorted(kwargs.items()))
                
                if key in memo:
                    return memo[key]
                
                result = func(*args, **kwargs)
                
                # Сохраняем только если результат может быть weak reference
                try:
                    memo[key] = result
                except TypeError:
                    # Нельзя создать weak reference, возвращаем результат как есть
                    pass
                
                return result
            
            return wrapper
        
        def get_performance_report(self) -> Dict[str, Any]:
            """Получить отчет о производительности"""
            report = {
                "timing_stats": {},
                "cache_stats": dict(self.cache_stats),
                "profiling_available": list(self.profiling_data.keys())
            }
            
            # Агрегируем статистику по времени
            for func_name, times in self.timing_stats.items():
                if times:
                    report["timing_stats"][func_name] = {
                        "calls": len(times),
                        "total_time": sum(times),
                        "avg_time": sum(times) / len(times),
                        "min_time": min(times),
                        "max_time": max(times)
                    }
            
            return report
        
        def get_profiling_data(self, func_name: str) -> str:
            """Получить данные профилирования для функции"""
            return self.profiling_data.get(func_name, "Нет данных профилирования")
    
    # Алгоритмы для тестирования оптимизации
    class AlgorithmBenchmark:
        """Бенчмарк алгоритмов для тестирования оптимизации"""
        
        def __init__(self, optimizer: PerformanceOptimizer):
            self.optimizer = optimizer
        
        @property
        def timing(self):
            return self.optimizer.timing_decorator
        
        @property
        def cache(self):
            return self.optimizer.cache_decorator
        
        @property
        def profile(self):
            return self.optimizer.profile_decorator
        
        # Неоптимизированные версии
        def fibonacci_naive(self, n: int) -> int:
            """Наивное вычисление Фибоначчи"""
            if n <= 1:
                return n
            return self.fibonacci_naive(n - 1) + self.fibonacci_naive(n - 2)
        
        def factorial_iterative(self, n: int) -> int:
            """Итеративное вычисление факториала"""
            result = 1
            for i in range(1, n + 1):
                result *= i
            return result
        
        def is_prime_naive(self, n: int) -> bool:
            """Наивная проверка на простоту"""
            if n < 2:
                return False
            for i in range(2, n):
                if n % i == 0:
                    return False
            return True
        
        # Оптимизированные версии
        @timing
        @cache(maxsize=256, ttl=60.0)  # Кэш на 1 минуту
        def fibonacci_optimized(self, n: int) -> int:
            """Оптимизированное вычисление Фибоначчи"""
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
        
        @timing
        @cache(maxsize=128)
        def factorial_optimized(self, n: int) -> int:
            """Оптимизированное вычисление факториала с кэшем"""
            if n <= 1:
                return 1
            return n * self.factorial_optimized(n - 1)
        
        @timing
        @cache(maxsize=1000, ttl=120.0)
        def is_prime_optimized(self, n: int) -> bool:
            """Оптимизированная проверка на простоту"""
            if n < 2:
                return False
            if n == 2:
                return True
            if n % 2 == 0:
                return False
            
            # Проверяем только нечетные делители до sqrt(n)
            for i in range(3, int(n ** 0.5) + 1, 2):
                if n % i == 0:
                    return False
            return True
        
        @timing
        @profile
        def matrix_operations_heavy(self, size: int) -> List[List[int]]:
            """Тяжелые операции с матрицами"""
            # Создаем матрицы
            matrix_a = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
            matrix_b = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
            
            # Умножение матриц
            result = [[0] * size for _ in range(size)]
            for i in range(size):
                for j in range(size):
                    for k in range(size):
                        result[i][j] += matrix_a[i][k] * matrix_b[k][j]
            
            return result
        
        def benchmark_comparison(self, test_values: List[int]) -> Dict[str, Any]:
            """Сравнение производительности алгоритмов"""
            results = {
                "fibonacci": {"naive": [], "optimized": []},
                "factorial": {"naive": [], "optimized": []},
                "prime_check": {"naive": [], "optimized": []}
            }
            
            print("   Запуск бенчмарков...")
            
            for value in test_values:
                # Fibonacci
                if value <= 35:  # Ограничиваем для наивного алгоритма
                    start_time = time.perf_counter()
                    self.fibonacci_naive(value)
                    results["fibonacci"]["naive"].append(time.perf_counter() - start_time)
                
                start_time = time.perf_counter()
                self.fibonacci_optimized(value)
                results["fibonacci"]["optimized"].append(time.perf_counter() - start_time)
                
                # Factorial
                if value <= 20:  # Ограничиваем для избежания переполнения
                    start_time = time.perf_counter()
                    self.factorial_iterative(value)
                    results["factorial"]["naive"].append(time.perf_counter() - start_time)
                    
                    start_time = time.perf_counter()
                    self.factorial_optimized(value)
                    results["factorial"]["optimized"].append(time.perf_counter() - start_time)
                
                # Prime check
                prime_value = value * 1000 + 1  # Делаем числа больше
                
                if prime_value <= 10000:  # Ограничиваем для наивного алгоритма
                    start_time = time.perf_counter()
                    self.is_prime_naive(prime_value)
                    results["prime_check"]["naive"].append(time.perf_counter() - start_time)
                
                start_time = time.perf_counter()
                self.is_prime_optimized(prime_value)
                results["prime_check"]["optimized"].append(time.perf_counter() - start_time)
            
            return results
    
    # Анализатор производительности
    class PerformanceAnalyzer:
        """Анализатор производительности"""
        
        @staticmethod
        def analyze_benchmark_results(results: Dict[str, Any]) -> Dict[str, Any]:
            """Анализ результатов бенчмарка"""
            analysis = {}
            
            for algorithm, versions in results.items():
                if "naive" in versions and "optimized" in versions:
                    naive_times = versions["naive"]
                    optimized_times = versions["optimized"]
                    
                    if naive_times and optimized_times:
                        naive_avg = sum(naive_times) / len(naive_times)
                        optimized_avg = sum(optimized_times) / len(optimized_times)
                        
                        speedup = naive_avg / optimized_avg if optimized_avg > 0 else 0
                        
                        analysis[algorithm] = {
                            "naive_avg_time": naive_avg,
                            "optimized_avg_time": optimized_avg,
                            "speedup": speedup,
                            "improvement_percent": ((naive_avg - optimized_avg) / naive_avg) * 100 if naive_avg > 0 else 0
                        }
            
            return analysis
        
        @staticmethod
        def generate_optimization_recommendations(analysis: Dict[str, Any]) -> List[str]:
            """Генерация рекомендаций по оптимизации"""
            recommendations = []
            
            for algorithm, stats in analysis.items():
                speedup = stats.get("speedup", 0)
                improvement = stats.get("improvement_percent", 0)
                
                if speedup > 10:
                    recommendations.append(
                        f"🚀 {algorithm}: Отличная оптимизация! Ускорение в {speedup:.1f}x"
                    )
                elif speedup > 2:
                    recommendations.append(
                        f"✅ {algorithm}: Хорошая оптимизация. Ускорение в {speedup:.1f}x"
                    )
                elif speedup > 1:
                    recommendations.append(
                        f"📈 {algorithm}: Небольшое улучшение. Ускорение в {speedup:.1f}x"
                    )
                else:
                    recommendations.append(
                        f"⚠️ {algorithm}: Оптимизация не дала эффекта"
                    )
                
                if improvement > 50:
                    recommendations.append(
                        f"   💡 Время выполнения сокращено на {improvement:.1f}%"
                    )
            
            return recommendations
    
    # Демонстрация
    print("Создание системы оптимизации производительности...")
    
    # Создаем оптимизатор и бенчмарк
    optimizer = PerformanceOptimizer()
    benchmark = AlgorithmBenchmark(optimizer)
    analyzer = PerformanceAnalyzer()
    
    print("\n1. Тестирование кэширования:")
    
    # Тест кэширования
    print("   Первый вызов fibonacci_optimized(30):")
    start_time = time.perf_counter()
    result1 = benchmark.fibonacci_optimized(30)
    time1 = time.perf_counter() - start_time
    print(f"     Результат: {result1}, Время: {time1:.4f}с")
    
    print("   Второй вызов fibonacci_optimized(30) (из кэша):")
    start_time = time.perf_counter()
    result2 = benchmark.fibonacci_optimized(30)
    time2 = time.perf_counter() - start_time
    print(f"     Результат: {result2}, Время: {time2:.4f}с")
    print(f"     Ускорение: {time1/time2:.1f}x")
    
    print("\n2. Сравнительный бенчмарк:")
    
    test_values = [10, 15, 20, 25, 30]
    benchmark_results = benchmark.benchmark_comparison(test_values)
    
    # Анализируем результаты
    analysis = analyzer.analyze_benchmark_results(benchmark_results)
    
    print("   Результаты анализа:")
    for algorithm, stats in analysis.items():
        print(f"     {algorithm}:")
        print(f"       Наивный алгоритм: {stats['naive_avg_time']:.6f}с")
        print(f"       Оптимизированный: {stats['optimized_avg_time']:.6f}с")
        print(f"       Ускорение: {stats['speedup']:.1f}x")
        print(f"       Улучшение: {stats['improvement_percent']:.1f}%")
    
    print("\n3. Рекомендации по оптимизации:")
    recommendations = analyzer.generate_optimization_recommendations(analysis)
    for rec in recommendations:
        print(f"   {rec}")
    
    print("\n4. Тест тяжелых операций с профилированием:")
    
    # Тестируем матричные операции
    result_matrix = benchmark.matrix_operations_heavy(50)
    print(f"   Матричные операции выполнены. Размер результата: {len(result_matrix)}x{len(result_matrix[0])}")
    
    print("\n5. Общий отчет о производительности:")
    
    performance_report = optimizer.get_performance_report()
    
    print("   Статистика по времени выполнения:")
    for func_name, stats in performance_report["timing_stats"].items():
        print(f"     {func_name}:")
        print(f"       Вызовов: {stats['calls']}")
        print(f"       Общее время: {stats['total_time']:.4f}с")
        print(f"       Среднее время: {stats['avg_time']:.4f}с")
    
    print("   Статистика кэширования:")
    for func_name, stats in performance_report["cache_stats"].items():
        total = stats['hits'] + stats['misses']
        hit_rate = (stats['hits'] / total * 100) if total > 0 else 0
        print(f"     {func_name}: {stats['hits']} попаданий, {stats['misses']} промахов (Эффективность: {hit_rate:.1f}%)")
    
    # print("\n6. Данные профилирования:")
    # if performance_report["profiling_available"]:
    #     func_name = performance_report["profiling_available"][0]
    #     profiling_data = optimizer.get_profiling_data(func_name)
    #     print(f"   Профилирование {func_name}:")
    #     print("   " + "\n   ".join(profiling_data.split("\n")[:15]))  # Показываем первые 15 строк
    
    print("✅ Упражнение 3 завершено")


def main():
    """Главная функция для запуска всех упражнений"""
    
    exercises = [
        ("Система продвинутых структур данных", exercise_01_advanced_data_structures_system),
        ("Распределенная система обработки задач", exercise_02_distributed_task_system),
        ("Система оптимизации производительности", exercise_03_performance_optimization_system),
    ]
    
    print("🏗️ Упражнения: Архитектура и CS фундамент в Python")
    print("=" * 70)
    print("Эти упражнения помогут освоить:")
    print("- Продвинутые структуры данных и алгоритмы")
    print("- Паттерны проектирования в сложных системах")
    print("- Архитектурные принципы распределенных систем")
    print("- Техники оптимизации производительности")
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
            input("\nНажмите Enter для продолжения...")
    
    print("\n🎉 Все упражнения по архитектуре и CS фундаменту завершены!")


if __name__ == "__main__":
    main() 