#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практические примеры: Внешние библиотеки в Python

Этот файл содержит примеры для изучения:
- NumPy для научных вычислений
- Pandas для анализа данных
- Requests для HTTP запросов
- Flask для веб-разработки
- Matplotlib для визуализации
"""

import sys
import subprocess
import importlib

def check_and_install_package(package_name, import_name=None):
    """Проверка и установка пакета при необходимости"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        print(f"Пакет {package_name} не найден. Попытка установки...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
            print(f"Пакет {package_name} установлен успешно")
            return True
        except subprocess.CalledProcessError:
            print(f"Не удалось установить {package_name}")
            return False

def example_01_numpy_basics():
    """Пример 1: Основы NumPy"""
    
    if not check_and_install_package('numpy'):
        print("NumPy недоступен, пропускаем пример")
        return
    
    import numpy as np
    
    print("=== Пример 1: Основы NumPy ===")
    
    # Создание массивов
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.zeros((3, 3))
    arr3 = np.random.randint(1, 10, (2, 4))
    
    print(f"Одномерный массив: {arr1}")
    print(f"Матрица нулей:\n{arr2}")
    print(f"Случайная матрица:\n{arr3}")
    
    # Математические операции
    squared = arr1 ** 2
    mean_val = np.mean(arr3)
    
    print(f"Квадраты: {squared}")
    print(f"Среднее значение: {mean_val:.2f}")
    
    # Линейная алгебра
    matrix_a = np.random.rand(3, 3)
    matrix_b = np.random.rand(3, 3)
    product = np.dot(matrix_a, matrix_b)
    
    print(f"Произведение матриц shape: {product.shape}")
    print("✅ NumPy пример завершен")

def example_02_pandas_dataframes():
    """Пример 2: Pandas DataFrames"""
    
    if not check_and_install_package('pandas'):
        print("Pandas недоступен, пропускаем пример")
        return
    
    import pandas as pd
    import numpy as np
    
    print("=== Пример 2: Pandas DataFrames ===")
    
    # Создание DataFrame
    data = {
        'name': ['Алиса', 'Боб', 'Чарли', 'Диана'],
        'age': [25, 30, 35, 28],
        'salary': [95000, 105000, 85000, 98000],
        'department': ['IT', 'HR', 'IT', 'Finance']
    }
    
    df = pd.DataFrame(data)
    print("DataFrame:")
    print(df)
    
    # Базовые операции
    print(f"\nСредняя зарплата: {df['salary'].mean():,.0f}")
    print(f"IT сотрудники:\n{df[df['department'] == 'IT']}")
    
    # Группировка
    dept_stats = df.groupby('department')['salary'].agg(['mean', 'count'])
    print(f"\nСтатистика по отделам:\n{dept_stats}")
    
    print("✅ Pandas пример завершен")

def example_03_requests_http():
    """Пример 3: HTTP запросы с Requests"""
    
    if not check_and_install_package('requests'):
        print("Requests недоступен, пропускаем пример")
        return
    
    import requests
    
    print("=== Пример 3: HTTP запросы с Requests ===")
    
    try:
        # GET запрос
        response = requests.get('https://httpbin.org/get', timeout=5)
        print(f"GET статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"URL: {data.get('url')}")
        
        # POST запрос
        post_data = {'name': 'Python', 'version': '3.12'}
        response = requests.post('https://httpbin.org/post', 
                               json=post_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"POST данные отправлены: {result.get('json')}")
        
        print("✅ Requests пример завершен")
        
    except requests.RequestException as e:
        print(f"Ошибка HTTP запроса: {e}")

def example_04_matplotlib_plotting():
    """Пример 4: Визуализация с Matplotlib"""
    
    if not check_and_install_package('matplotlib'):
        print("Matplotlib недоступен, пропускаем пример")
        return
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    print("=== Пример 4: Визуализация с Matplotlib ===")
    
    # Данные для графика
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Создание графика
    plt.figure(figsize=(10, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(x, y1, label='sin(x)', linewidth=2)
    plt.plot(x, y2, label='cos(x)', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Тригонометрические функции')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Гистограмма
    plt.subplot(1, 2, 2)
    data = np.random.normal(100, 15, 1000)
    plt.hist(data, bins=30, alpha=0.7, color='skyblue')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.title('Гистограмма')
    plt.axvline(np.mean(data), color='red', linestyle='--')
    
    plt.tight_layout()
    
    # Сохранение вместо показа
    plt.savefig('matplotlib_example.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("График сохранен в matplotlib_example.png")
    print("✅ Matplotlib пример завершен")

def example_05_flask_webapp():
    """Пример 5: Простое веб-приложение Flask"""
    
    if not check_and_install_package('flask', 'flask'):
        print("Flask недоступен, пропускаем пример")
        return
    
    from flask import Flask, jsonify
    
    print("=== Пример 5: Простое веб-приложение Flask ===")
    
    # Создание приложения
    app = Flask(__name__)
    
    # Простые данные
    users = [
        {'id': 1, 'name': 'Алиса', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Боб', 'email': 'bob@example.com'}
    ]
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Добро пожаловать в Flask API',
            'endpoints': ['/users', '/users/<id>']
        })
    
    @app.route('/users')
    def get_users():
        return jsonify({'users': users, 'total': len(users)})
    
    @app.route('/users/<int:user_id>')
    def get_user(user_id):
        user = next((u for u in users if u['id'] == user_id), None)
        if user:
            return jsonify(user)
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    print("Flask приложение создано!")
    print("Доступные маршруты:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} [{', '.join(rule.methods - {'HEAD', 'OPTIONS'})}]")
    
    print("Для запуска: app.run(debug=True)")
    print("✅ Flask пример завершен")
    
    return app

def main():
    """Главная функция для запуска всех примеров"""
    
    examples = [
        ("NumPy - научные вычисления", example_01_numpy_basics),
        ("Pandas - анализ данных", example_02_pandas_dataframes),
        ("Requests - HTTP запросы", example_03_requests_http),
        ("Matplotlib - визуализация", example_04_matplotlib_plotting),
        ("Flask - веб-приложение", example_05_flask_webapp),
    ]
    
    print("📦 Примеры: Внешние библиотеки в Python")
    print("=" * 60)
    print("Эти примеры демонстрируют:")
    print("- Работу с популярными внешними библиотеками")
    print("- Автоматическую установку зависимостей")
    print("- Практическое применение библиотек")
    print("=" * 60)
    
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
    
    print("\n🎉 Все примеры внешних библиотек завершены!")

if __name__ == "__main__":
    main() 