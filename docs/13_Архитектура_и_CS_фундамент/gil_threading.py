# GIL и многопоточность в Python
import threading
import multiprocessing
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# CPU-bound задача
def cpu_bound_task(n):
    """CPU-интенсивная задача"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# I/O-bound задача
def io_bound_task(duration):
    """I/O-интенсивная задача (имитация)"""
    time.sleep(duration)
    return f"Задача выполнена за {duration} сек"

# Демонстрация влияния GIL на CPU-bound задачи
def test_cpu_bound():
    print("=== CPU-bound задачи ===")
    n = 1000000
    
    # Последовательное выполнение
    start = time.perf_counter()
    for _ in range(4):
        cpu_bound_task(n)
    sequential_time = time.perf_counter() - start
    print(f"Последовательно: {sequential_time:.2f} сек")
    
    # Многопоточное выполнение (GIL мешает)
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_bound_task, n) for _ in range(4)]
        for future in futures:
            future.result()
    threading_time = time.perf_counter() - start
    print(f"Многопоточно: {threading_time:.2f} сек")
    
    # Многопроцессное выполнение (без GIL)
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_bound_task, n) for _ in range(4)]
        for future in futures:
            future.result()
    multiprocessing_time = time.perf_counter() - start
    print(f"Многопроцессно: {multiprocessing_time:.2f} сек")
    
    print(f"Ускорение от многопроцессности: {sequential_time / multiprocessing_time:.2f}x")

# Демонстрация эффективности потоков для I/O-bound задач
def test_io_bound():
    print("\n=== I/O-bound задачи ===")
    duration = 0.5
    
    # Последовательное выполнение
    start = time.perf_counter()
    for _ in range(4):
        io_bound_task(duration)
    sequential_time = time.perf_counter() - start
    print(f"Последовательно: {sequential_time:.2f} сек")
    
    # Многопоточное выполнение (эффективно для I/O)
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(io_bound_task, duration) for _ in range(4)]
        for future in futures:
            future.result()
    threading_time = time.perf_counter() - start
    print(f"Многопоточно: {threading_time:.2f} сек")
    
    print(f"Ускорение от многопоточности: {sequential_time / threading_time:.2f}x")

# Асинхронное программирование
async def async_io_task(duration, task_id):
    """Асинхронная I/O задача"""
    print(f"Задача {task_id} начата")
    await asyncio.sleep(duration)
    print(f"Задача {task_id} завершена")
    return f"Результат задачи {task_id}"

async def test_async():
    print("\n=== Асинхронное выполнение ===")
    start = time.perf_counter()
    
    # Создаём и запускаем асинхронные задачи
    tasks = [async_io_task(0.5, i) for i in range(4)]
    results = await asyncio.gather(*tasks)
    
    async_time = time.perf_counter() - start
    print(f"Асинхронно: {async_time:.2f} сек")
    
    for result in results:
        print(result)

# Информация о GIL
def gil_info():
    print("\n=== Информация о GIL ===")
    print(f"Количество CPU ядер: {multiprocessing.cpu_count()}")
    print(f"Активных потоков: {threading.active_count()}")
    print(f"Текущий поток: {threading.current_thread().name}")
    
    # Создаём несколько потоков для демонстрации
    def worker(name):
        print(f"Поток {name} работает")
        time.sleep(1)
        print(f"Поток {name} завершён")
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"Worker-{i}",))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    test_cpu_bound()
    test_io_bound()
    
    # Запуск асинхронного теста
    asyncio.run(test_async())
    
    gil_info() 