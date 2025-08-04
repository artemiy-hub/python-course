# Примеры управления памятью в Python
import sys
import gc

# Счётчик ссылок
x = []
print(f"Счётчик ссылок на x: {sys.getrefcount(x)}")

y = x  # увеличиваем счётчик ссылок
print(f"После y = x: {sys.getrefcount(x)}")

del y  # уменьшаем счётчик ссылок
print(f"После del y: {sys.getrefcount(x)}")

# Циклические ссылки
class Node:
    def __init__(self, value):
        self.value = value
        self.child = None
        self.parent = None

# Создаём циклическую ссылку
node1 = Node(1)
node2 = Node(2)
node1.child = node2
node2.parent = node1

print(f"Объектов до сборки мусора: {len(gc.get_objects())}")

# Удаляем ссылки, но объекты остаются из-за цикла
del node1, node2

# Принудительная сборка мусора
collected = gc.collect()
print(f"Собрано объектов: {collected}")
print(f"Объектов после сборки мусора: {len(gc.get_objects())}")

# Информация о сборщике мусора
print(f"Пороги сборки мусора: {gc.get_threshold()}")
print(f"Статистика поколений: {gc.get_stats()}") 