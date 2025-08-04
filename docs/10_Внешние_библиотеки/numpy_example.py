# Пример использования библиотеки numpy
try:
    import numpy as np
    
    # Создание массивов
    a = np.array([1, 2, 3, 4, 5])
    print(f"Массив: {a}")
    print(f"Тип: {type(a)}")
    
    # Операции с массивами
    print(f"a * 2 = {a * 2}")
    print(f"Среднее: {a.mean()}")
    print(f"Сумма: {a.sum()}")
    
    # Многомерные массивы
    matrix = np.array([[1, 2], [3, 4]])
    print(f"Матрица:\n{matrix}")
    print(f"Форма: {matrix.shape}")
    
except ImportError:
    print("Библиотека numpy не установлена. Установите: pip install numpy") 