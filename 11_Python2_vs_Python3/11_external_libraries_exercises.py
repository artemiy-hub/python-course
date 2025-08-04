#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упражнения: Внешние библиотеки в Python

Этот файл содержит практические упражнения для закрепления знаний:
- Анализ данных с Pandas и NumPy
- Веб-API с Flask/FastAPI
- Визуализация данных
"""

import sys
import subprocess
import importlib
import json
import time
from datetime import datetime, timedelta

def check_package(package_name, import_name=None):
    """Проверка доступности пакета"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def exercise_01_data_analysis_pipeline():
    """
    Упражнение 1: Пайплайн анализа данных
    
    Задача:
    Создайте полный пайплайн анализа данных с использованием
    Pandas и NumPy для обработки данных о продажах интернет-магазина.
    """
    print("=== Упражнение 1: Пайплайн анализа данных ===")
    
    if not (check_package('pandas') and check_package('numpy')):
        print("Необходимые пакеты недоступны: pandas, numpy")
        return
    
    import pandas as pd
    import numpy as np
    
    # РЕШЕНИЕ:
    
    class SalesAnalyzer:
        """Анализатор данных о продажах"""
        
        def __init__(self):
            self.data = None
            self.processed_data = None
        
        def generate_sample_data(self, n_records=1000):
            """Генерация тестовых данных о продажах"""
            np.random.seed(42)
            
            # Товары и категории
            products = ['Ноутбук', 'Смартфон', 'Планшет', 'Наушники', 'Клавиатура', 'Мышь']
            categories = ['Электроника', 'Аксессуары', 'Компьютеры']
            regions = ['Москва', 'СПб', 'Казань', 'Екатеринбург', 'Новосибирск']
            
            # Генерация данных
            data = []
            start_date = datetime(2023, 1, 1)
            
            for i in range(n_records):
                product = np.random.choice(products)
                
                # Цена зависит от товара
                price_map = {
                    'Ноутбук': (50000, 150000),
                    'Смартфон': (15000, 80000),
                    'Планшет': (20000, 60000),
                    'Наушники': (2000, 15000),
                    'Клавиатура': (1000, 8000),
                    'Мышь': (500, 5000)
                }
                
                min_price, max_price = price_map[product]
                price = np.random.uniform(min_price, max_price)
                quantity = np.random.randint(1, 6)
                
                # Дата продажи
                random_days = np.random.randint(0, 365)
                sale_date = start_date + timedelta(days=random_days)
                
                # Категория товара
                if product in ['Ноутбук', 'Планшет']:
                    category = 'Компьютеры'
                elif product in ['Смартфон']:
                    category = 'Электроника'
                else:
                    category = 'Аксессуары'
                
                data.append({
                    'date': sale_date,
                    'product': product,
                    'category': category,
                    'price': round(price, 2),
                    'quantity': quantity,
                    'region': np.random.choice(regions),
                    'customer_id': f'CUST_{i % 200:04d}',  # 200 уникальных клиентов
                    'discount': np.random.uniform(0, 0.3) if np.random.random() < 0.3 else 0
                })
            
            self.data = pd.DataFrame(data)
            self.data['revenue'] = self.data['price'] * self.data['quantity'] * (1 - self.data['discount'])
            
            print(f"Сгенерировано {len(self.data)} записей о продажах")
            return self.data
        
        def clean_data(self):
            """Очистка и предобработка данных"""
            if self.data is None:
                raise ValueError("Данные не загружены")
            
            print("Очистка данных...")
            
            # Копируем данные для обработки
            self.processed_data = self.data.copy()
            
            # Добавляем временные признаки
            self.processed_data['year'] = self.processed_data['date'].dt.year
            self.processed_data['month'] = self.processed_data['date'].dt.month
            self.processed_data['quarter'] = self.processed_data['date'].dt.quarter
            self.processed_data['day_of_week'] = self.processed_data['date'].dt.day_name()
            
            # Добавляем признаки для анализа
            self.processed_data['price_category'] = pd.cut(
                self.processed_data['price'], 
                bins=[0, 5000, 20000, 50000, float('inf')],
                labels=['Низкая', 'Средняя', 'Высокая', 'Премиум']
            )
            
            # Обнаружение выбросов по методу IQR
            Q1 = self.processed_data['revenue'].quantile(0.25)
            Q3 = self.processed_data['revenue'].quantile(0.75)
            IQR = Q3 - Q1
            
            outlier_mask = (
                (self.processed_data['revenue'] < (Q1 - 1.5 * IQR)) | 
                (self.processed_data['revenue'] > (Q3 + 1.5 * IQR))
            )
            
            print(f"Обнаружено выбросов: {outlier_mask.sum()}")
            
            # Маркируем выбросы, но не удаляем
            self.processed_data['is_outlier'] = outlier_mask
            
            print("Очистка данных завершена")
        
        def analyze_sales(self):
            """Основной анализ продаж"""
            if self.processed_data is None:
                raise ValueError("Данные не обработаны")
            
            print("Анализ продаж...")
            
            # Общая статистика
            total_revenue = self.processed_data['revenue'].sum()
            total_orders = len(self.processed_data)
            avg_order_value = self.processed_data['revenue'].mean()
            
            print(f"\n📊 Общая статистика:")
            print(f"  Общая выручка: {total_revenue:,.0f} руб.")
            print(f"  Количество заказов: {total_orders:,}")
            print(f"  Средний чек: {avg_order_value:,.0f} руб.")
            
            # Анализ по товарам
            product_stats = self.processed_data.groupby('product').agg({
                'revenue': ['sum', 'count', 'mean'],
                'quantity': 'sum'
            }).round(2)
            
            product_stats.columns = ['Выручка', 'Заказов', 'Средний_чек', 'Количество']
            product_stats = product_stats.sort_values('Выручка', ascending=False)
            
            print(f"\n💰 Топ товары по выручке:")
            print(product_stats.head())
            
            # Анализ по регионам
            region_stats = self.processed_data.groupby('region').agg({
                'revenue': 'sum',
                'customer_id': 'nunique'
            }).round(2)
            
            region_stats.columns = ['Выручка', 'Клиентов']
            region_stats = region_stats.sort_values('Выручка', ascending=False)
            
            print(f"\n🌍 Продажи по регионам:")
            print(region_stats)
            
            # Временной анализ
            monthly_sales = self.processed_data.groupby('month')['revenue'].sum()
            
            print(f"\n📅 Продажи по месяцам:")
            for month, revenue in monthly_sales.items():
                print(f"  Месяц {month}: {revenue:,.0f} руб.")
            
            # Анализ клиентов
            customer_stats = self.processed_data.groupby('customer_id').agg({
                'revenue': 'sum',
                'date': 'count'
            })
            customer_stats.columns = ['Общая_сумма', 'Заказов']
            
            print(f"\n👥 Анализ клиентов:")
            print(f"  Уникальных клиентов: {len(customer_stats)}")
            print(f"  Средняя сумма на клиента: {customer_stats['Общая_сумма'].mean():,.0f} руб.")
            print(f"  Среднее заказов на клиента: {customer_stats['Заказов'].mean():.1f}")
            
            # Топ клиенты
            top_customers = customer_stats.sort_values('Общая_сумма', ascending=False).head()
            print(f"\n🏆 Топ-5 клиентов:")
            print(top_customers)
            
            return {
                'total_revenue': total_revenue,
                'total_orders': total_orders,
                'avg_order_value': avg_order_value,
                'product_stats': product_stats,
                'region_stats': region_stats,
                'monthly_sales': monthly_sales
            }
        
        def create_pivot_tables(self):
            """Создание сводных таблиц"""
            if self.processed_data is None:
                return
            
            print("\n📋 Сводные таблицы:")
            
            # Сводная по регионам и категориям
            pivot1 = self.processed_data.pivot_table(
                values='revenue',
                index='region',
                columns='category',
                aggfunc='sum',
                fill_value=0
            )
            
            print("Выручка по регионам и категориям:")
            print(pivot1.round(0))
            
            # Сводная по месяцам и товарам
            pivot2 = self.processed_data.pivot_table(
                values='quantity',
                index='month',
                columns='product',
                aggfunc='sum',
                fill_value=0
            )
            
            print(f"\nКоличество продаж по месяцам:")
            print(pivot2)
        
        def export_results(self, filename='sales_analysis.json'):
            """Экспорт результатов анализа"""
            if self.processed_data is None:
                return
            
            results = self.analyze_sales()
            
            # Конвертируем pandas объекты в JSON-совместимые
            export_data = {
                'summary': {
                    'total_revenue': float(results['total_revenue']),
                    'total_orders': int(results['total_orders']),
                    'avg_order_value': float(results['avg_order_value'])
                },
                'monthly_sales': results['monthly_sales'].to_dict(),
                'top_products': results['product_stats'].head().to_dict(),
                'regions': results['region_stats'].to_dict()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"Результаты экспортированы в {filename}")
    
    # Демонстрация
    analyzer = SalesAnalyzer()
    
    # Генерируем данные
    analyzer.generate_sample_data(1500)
    
    # Обрабатываем
    analyzer.clean_data()
    
    # Анализируем
    analyzer.analyze_sales()
    
    # Сводные таблицы
    analyzer.create_pivot_tables()
    
    # Экспорт
    analyzer.export_results()
    
    print("✅ Упражнение 1 завершено")

def exercise_02_web_api_development():
    """
    Упражнение 2: Разработка Web API
    
    Задача:
    Создайте RESTful API для управления библиотекой книг
    с использованием Flask, включая CRUD операции и поиск.
    """
    print("=== Упражнение 2: Разработка Web API ===")
    
    if not check_package('flask'):
        print("Flask недоступен для этого упражнения")
        return
    
    from flask import Flask, request, jsonify
    import json
    from datetime import datetime
    
    # РЕШЕНИЕ:
    
    class Book:
        """Модель книги"""
        
        def __init__(self, title, author, isbn, year, genre):
            self.id = None
            self.title = title
            self.author = author
            self.isbn = isbn
            self.year = year
            self.genre = genre
            self.created_at = datetime.now().isoformat()
            self.updated_at = self.created_at
        
        def to_dict(self):
            return {
                'id': self.id,
                'title': self.title,
                'author': self.author,
                'isbn': self.isbn,
                'year': self.year,
                'genre': self.genre,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        
        def update(self, **kwargs):
            for key, value in kwargs.items():
                if hasattr(self, key) and key not in ['id', 'created_at']:
                    setattr(self, key, value)
            self.updated_at = datetime.now().isoformat()
    
    class BookManager:
        """Менеджер для управления книгами"""
        
        def __init__(self):
            self.books = {}
            self.next_id = 1
            self._load_sample_data()
        
        def _load_sample_data(self):
            """Загрузка тестовых данных"""
            sample_books = [
                Book("1984", "Джордж Оруэлл", "978-0-452-28423-4", 1949, "Антиутопия"),
                Book("Гарри Поттер", "Дж.К. Роулинг", "978-0-439-70818-8", 1997, "Фэнтези"),
                Book("Властелин колец", "Дж.Р.Р. Толкин", "978-0-547-92822-7", 1954, "Фэнтези"),
                Book("Мастер и Маргарита", "Михаил Булгаков", "978-5-17-082687-9", 1967, "Роман")
            ]
            
            for book in sample_books:
                self.add_book(book)
        
        def add_book(self, book):
            """Добавление книги"""
            book.id = self.next_id
            self.books[self.next_id] = book
            self.next_id += 1
            return book
        
        def get_book(self, book_id):
            """Получение книги по ID"""
            return self.books.get(book_id)
        
        def get_all_books(self):
            """Получение всех книг"""
            return list(self.books.values())
        
        def update_book(self, book_id, **kwargs):
            """Обновление книги"""
            book = self.books.get(book_id)
            if book:
                book.update(**kwargs)
                return book
            return None
        
        def delete_book(self, book_id):
            """Удаление книги"""
            return self.books.pop(book_id, None)
        
        def search_books(self, query):
            """Поиск книг по названию или автору"""
            results = []
            query_lower = query.lower()
            
            for book in self.books.values():
                if (query_lower in book.title.lower() or 
                    query_lower in book.author.lower() or
                    query_lower in book.genre.lower()):
                    results.append(book)
            
            return results
        
        def get_books_by_genre(self, genre):
            """Получение книг по жанру"""
            return [book for book in self.books.values() 
                   if book.genre.lower() == genre.lower()]
        
        def get_statistics(self):
            """Статистика библиотеки"""
            books = list(self.books.values())
            
            if not books:
                return {}
            
            # Подсчет по жанрам
            genres = {}
            years = []
            
            for book in books:
                genres[book.genre] = genres.get(book.genre, 0) + 1
                years.append(book.year)
            
            return {
                'total_books': len(books),
                'genres': genres,
                'oldest_book': min(years),
                'newest_book': max(years),
                'avg_year': sum(years) / len(years)
            }
    
    def create_library_api():
        """Создание Flask API для библиотеки"""
        
        app = Flask(__name__)
        book_manager = BookManager()
        
        @app.route('/api/books', methods=['GET'])
        def get_books():
            """Получить все книги или поиск"""
            search_query = request.args.get('search')
            genre = request.args.get('genre')
            
            if search_query:
                books = book_manager.search_books(search_query)
            elif genre:
                books = book_manager.get_books_by_genre(genre)
            else:
                books = book_manager.get_all_books()
            
            return jsonify({
                'books': [book.to_dict() for book in books],
                'total': len(books)
            })
        
        @app.route('/api/books/<int:book_id>', methods=['GET'])
        def get_book(book_id):
            """Получить книгу по ID"""
            book = book_manager.get_book(book_id)
            
            if book:
                return jsonify(book.to_dict())
            else:
                return jsonify({'error': 'Книга не найдена'}), 404
        
        @app.route('/api/books', methods=['POST'])
        def create_book():
            """Создать новую книгу"""
            data = request.get_json()
            
            required_fields = ['title', 'author', 'isbn', 'year', 'genre']
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Отсутствуют обязательные поля'}), 400
            
            try:
                book = Book(
                    title=data['title'],
                    author=data['author'],
                    isbn=data['isbn'],
                    year=int(data['year']),
                    genre=data['genre']
                )
                
                created_book = book_manager.add_book(book)
                return jsonify(created_book.to_dict()), 201
                
            except (ValueError, TypeError) as e:
                return jsonify({'error': f'Некорректные данные: {e}'}), 400
        
        @app.route('/api/books/<int:book_id>', methods=['PUT'])
        def update_book(book_id):
            """Обновить книгу"""
            data = request.get_json()
            
            updated_book = book_manager.update_book(book_id, **data)
            
            if updated_book:
                return jsonify(updated_book.to_dict())
            else:
                return jsonify({'error': 'Книга не найдена'}), 404
        
        @app.route('/api/books/<int:book_id>', methods=['DELETE'])
        def delete_book(book_id):
            """Удалить книгу"""
            deleted_book = book_manager.delete_book(book_id)
            
            if deleted_book:
                return jsonify({'message': 'Книга удалена', 'book': deleted_book.to_dict()})
            else:
                return jsonify({'error': 'Книга не найдена'}), 404
        
        @app.route('/api/statistics', methods=['GET'])
        def get_statistics():
            """Получить статистику библиотеки"""
            stats = book_manager.get_statistics()
            return jsonify(stats)
        
        @app.route('/', methods=['GET'])
        def index():
            """Главная страница с документацией API"""
            docs = {
                'message': 'Library API Documentation',
                'endpoints': {
                    'GET /api/books': 'Получить все книги',
                    'GET /api/books?search=query': 'Поиск книг',
                    'GET /api/books?genre=genre': 'Книги по жанру',
                    'GET /api/books/<id>': 'Получить книгу по ID',
                    'POST /api/books': 'Создать новую книгу',
                    'PUT /api/books/<id>': 'Обновить книгу',
                    'DELETE /api/books/<id>': 'Удалить книгу',
                    'GET /api/statistics': 'Статистика библиотеки'
                },
                'example_book': {
                    'title': 'Название книги',
                    'author': 'Автор',
                    'isbn': '978-0-123456-78-9',
                    'year': 2024,
                    'genre': 'Фантастика'
                }
            }
            return jsonify(docs)
        
        return app
    
    # Демонстрация API
    print("Создание Library API...")
    
    app = create_library_api()
    
    print("✅ Flask API создан!")
    print("\n📚 Доступные endpoints:")
    
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"  {methods:15} {rule.rule}")
    
    print("\nПример запросов:")
    print("  GET  /api/books              - Все книги")
    print("  GET  /api/books?search=Гарри - Поиск")
    print("  POST /api/books              - Создать книгу")
    print("  GET  /api/statistics         - Статистика")
    
    print("\nДля запуска сервера:")
    print("  app.run(debug=True, port=5000)")
    
    print("✅ Упражнение 2 завершено")

def exercise_03_data_visualization():
    """
    Упражнение 3: Визуализация данных
    
    Задача:
    Создайте дашборд для визуализации данных о продажах
    с различными типами графиков и интерактивными элементами.
    """
    print("=== Упражнение 3: Визуализация данных ===")
    
    if not (check_package('matplotlib') and check_package('pandas')):
        print("Необходимые пакеты недоступны")
        return
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    
    # РЕШЕНИЕ:
    
    class DataVisualizer:
        """Класс для создания визуализаций"""
        
        def __init__(self):
            self.data = None
            plt.style.use('default')
        
        def generate_sales_data(self):
            """Генерация данных для визуализации"""
            np.random.seed(42)
            
            # Данные за год
            dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
            
            # Тренд и сезонность
            trend = np.linspace(1000, 1500, len(dates))
            seasonal = 200 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
            weekly = 100 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
            noise = np.random.normal(0, 50, len(dates))
            
            sales = trend + seasonal + weekly + noise
            
            # Дополнительные данные
            categories = ['Электроника', 'Одежда', 'Книги', 'Спорт', 'Дом']
            regions = ['Москва', 'СПб', 'Казань', 'Екатеринбург']
            
            data = []
            for i, date in enumerate(dates):
                for category in categories:
                    for region in regions:
                        base_sales = sales[i] * np.random.uniform(0.5, 1.5)
                        data.append({
                            'date': date,
                            'category': category,
                            'region': region,
                            'sales': max(0, base_sales),
                            'orders': np.random.randint(10, 100),
                            'customers': np.random.randint(5, 50)
                        })
            
            self.data = pd.DataFrame(data)
            print(f"Сгенерировано {len(self.data)} записей для визуализации")
            
            return self.data
        
        def create_time_series_plot(self):
            """График временных рядов"""
            daily_sales = self.data.groupby('date')['sales'].sum()
            
            plt.figure(figsize=(15, 8))
            
            # Основной график
            plt.subplot(2, 2, 1)
            plt.plot(daily_sales.index, daily_sales.values, linewidth=1.5, alpha=0.7)
            
            # Скользящее среднее
            rolling_mean = daily_sales.rolling(window=30).mean()
            plt.plot(rolling_mean.index, rolling_mean.values, 'r-', linewidth=2, label='30-дневное среднее')
            
            plt.title('Продажи по дням (2023)')
            plt.xlabel('Дата')
            plt.ylabel('Продажи')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Месячная агрегация
            plt.subplot(2, 2, 2)
            monthly_sales = self.data.groupby(self.data['date'].dt.month)['sales'].sum()
            
            months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
                     'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
            
            bars = plt.bar(range(1, 13), monthly_sales.values, color='skyblue', alpha=0.8)
            plt.title('Продажи по месяцам')
            plt.xlabel('Месяц')
            plt.ylabel('Продажи')
            plt.xticks(range(1, 13), months, rotation=45)
            
            # Добавляем значения на столбцы
            for bar, value in zip(bars, monthly_sales.values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + value*0.01,
                        f'{value:.0f}', ha='center', va='bottom', fontsize=8)
            
            # Продажи по категориям
            plt.subplot(2, 2, 3)
            category_sales = self.data.groupby('category')['sales'].sum().sort_values(ascending=True)
            
            colors = plt.cm.Set3(np.linspace(0, 1, len(category_sales)))
            bars = plt.barh(range(len(category_sales)), category_sales.values, color=colors)
            
            plt.title('Продажи по категориям')
            plt.xlabel('Продажи')
            plt.yticks(range(len(category_sales)), category_sales.index)
            
            # Круговая диаграмма по регионам
            plt.subplot(2, 2, 4)
            region_sales = self.data.groupby('region')['sales'].sum()
            
            plt.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%',
                   startangle=90, colors=plt.cm.Pastel1(range(len(region_sales))))
            plt.title('Распределение продаж по регионам')
            
            plt.tight_layout()
            plt.savefig('sales_dashboard.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("График временных рядов сохранен: sales_dashboard.png")
        
        def create_correlation_analysis(self):
            """Анализ корреляций"""
            # Создаем данные для корреляционного анализа
            correlation_data = self.data.groupby(['date', 'region']).agg({
                'sales': 'sum',
                'orders': 'sum',
                'customers': 'sum'
            }).reset_index()
            
            correlation_data['avg_order_value'] = correlation_data['sales'] / correlation_data['orders']
            correlation_data['sales_per_customer'] = correlation_data['sales'] / correlation_data['customers']
            
            plt.figure(figsize=(12, 8))
            
            # Корреляционная матрица
            plt.subplot(2, 3, 1)
            numeric_cols = ['sales', 'orders', 'customers', 'avg_order_value', 'sales_per_customer']
            corr_matrix = correlation_data[numeric_cols].corr()
            
            im = plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
            plt.title('Корреляционная матрица')
            plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=45)
            plt.yticks(range(len(numeric_cols)), numeric_cols)
            
            # Добавляем значения корреляций
            for i in range(len(numeric_cols)):
                for j in range(len(numeric_cols)):
                    plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                           ha='center', va='center', fontsize=8)
            
            plt.colorbar(im)
            
            # Scatter plots
            plt.subplot(2, 3, 2)
            plt.scatter(correlation_data['orders'], correlation_data['sales'], alpha=0.6)
            plt.xlabel('Количество заказов')
            plt.ylabel('Продажи')
            plt.title('Заказы vs Продажи')
            
            # Добавляем линию тренда
            z = np.polyfit(correlation_data['orders'], correlation_data['sales'], 1)
            p = np.poly1d(z)
            plt.plot(correlation_data['orders'], p(correlation_data['orders']), "r--", alpha=0.8)
            
            plt.subplot(2, 3, 3)
            plt.scatter(correlation_data['customers'], correlation_data['sales'], alpha=0.6, color='green')
            plt.xlabel('Количество клиентов')
            plt.ylabel('Продажи')
            plt.title('Клиенты vs Продажи')
            
            # Гистограммы распределений
            plt.subplot(2, 3, 4)
            plt.hist(correlation_data['avg_order_value'], bins=30, alpha=0.7, color='orange')
            plt.xlabel('Средний чек')
            plt.ylabel('Частота')
            plt.title('Распределение среднего чека')
            
            plt.subplot(2, 3, 5)
            plt.boxplot([correlation_data[correlation_data['region'] == region]['sales'].values 
                        for region in correlation_data['region'].unique()],
                       labels=correlation_data['region'].unique())
            plt.title('Продажи по регионам (Box Plot)')
            plt.xticks(rotation=45)
            plt.ylabel('Продажи')
            
            # Временной анализ
            plt.subplot(2, 3, 6)
            monthly_trend = correlation_data.groupby(correlation_data['date'].dt.month)['avg_order_value'].mean()
            plt.plot(range(1, 13), monthly_trend.values, marker='o', linewidth=2)
            plt.title('Динамика среднего чека')
            plt.xlabel('Месяц')
            plt.ylabel('Средний чек')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("Анализ корреляций сохранен: correlation_analysis.png")
        
        def create_advanced_visualizations(self):
            """Продвинутые визуализации"""
            plt.figure(figsize=(16, 10))
            
            # Тепловая карта продаж по дням недели и месяцам
            plt.subplot(2, 3, 1)
            
            # Подготавливаем данные
            self.data['month'] = self.data['date'].dt.month
            self.data['day_of_week'] = self.data['date'].dt.day_name()
            
            heatmap_data = self.data.groupby(['month', 'day_of_week'])['sales'].sum().unstack(fill_value=0)
            
            # Упорядочиваем дни недели
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = heatmap_data.reindex(columns=day_order, fill_value=0)
            
            im = plt.imshow(heatmap_data.T, cmap='YlOrRd', aspect='auto')
            plt.title('Продажи: День недели vs Месяц')
            plt.xlabel('Месяц')
            plt.ylabel('День недели')
            plt.xticks(range(12), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
                                  'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
            plt.yticks(range(7), ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'])
            plt.colorbar(im)
            
            # Кумулятивные продажи
            plt.subplot(2, 3, 2)
            daily_sales = self.data.groupby('date')['sales'].sum().sort_index()
            cumulative_sales = daily_sales.cumsum()
            
            plt.plot(cumulative_sales.index, cumulative_sales.values, linewidth=2)
            plt.title('Кумулятивные продажи за год')
            plt.xlabel('Дата')
            plt.ylabel('Кумулятивные продажи')
            plt.grid(True, alpha=0.3)
            
            # Распределение продаж по категориям (violin plot имитация)
            plt.subplot(2, 3, 3)
            categories = self.data['category'].unique()
            category_data = [self.data[self.data['category'] == cat]['sales'].values for cat in categories]
            
            parts = plt.violinplot(category_data, positions=range(len(categories)), showmeans=True)
            plt.title('Распределение продаж по категориям')
            plt.xticks(range(len(categories)), categories, rotation=45)
            plt.ylabel('Продажи')
            
            # Сравнение регионов
            plt.subplot(2, 3, 4)
            region_monthly = self.data.groupby(['month', 'region'])['sales'].sum().unstack()
            
            for region in region_monthly.columns:
                plt.plot(region_monthly.index, region_monthly[region], marker='o', label=region, linewidth=2)
            
            plt.title('Продажи по регионам (помесячно)')
            plt.xlabel('Месяц')
            plt.ylabel('Продажи')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Анализ выбросов
            plt.subplot(2, 3, 5)
            daily_sales = self.data.groupby('date')['sales'].sum()
            
            Q1 = daily_sales.quantile(0.25)
            Q3 = daily_sales.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = daily_sales[(daily_sales < lower_bound) | (daily_sales > upper_bound)]
            normal_data = daily_sales[(daily_sales >= lower_bound) & (daily_sales <= upper_bound)]
            
            plt.scatter(normal_data.index, normal_data.values, alpha=0.6, s=10, label='Нормальные')
            plt.scatter(outliers.index, outliers.values, color='red', s=20, label='Выбросы')
            
            plt.axhline(y=lower_bound, color='red', linestyle='--', alpha=0.5, label='Границы')
            plt.axhline(y=upper_bound, color='red', linestyle='--', alpha=0.5)
            
            plt.title('Анализ выбросов в продажах')
            plt.xlabel('Дата')
            plt.ylabel('Продажи')
            plt.legend()
            
            # Прогноз тренда
            plt.subplot(2, 3, 6)
            
            # Простое скользящее среднее как прогноз
            window = 30
            rolling_mean = daily_sales.rolling(window=window).mean()
            
            plt.plot(daily_sales.index, daily_sales.values, alpha=0.3, label='Исходные данные')
            plt.plot(rolling_mean.index, rolling_mean.values, linewidth=2, label=f'Скользящее среднее ({window} дней)')
            
            # Простое продление тренда
            last_trend = rolling_mean.iloc[-10:].mean()
            future_dates = pd.date_range(daily_sales.index[-1] + pd.Timedelta(days=1), periods=30)
            future_trend = [last_trend] * len(future_dates)
            
            plt.plot(future_dates, future_trend, 'r--', linewidth=2, label='Прогноз')
            
            plt.title('Прогноз продаж')
            plt.xlabel('Дата')
            plt.ylabel('Продажи')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('advanced_visualizations.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("Продвинутые визуализации сохранены: advanced_visualizations.png")
        
        def generate_report(self):
            """Генерация итогового отчета"""
            if self.data is None:
                return
            
            report = {
                'period': '2023-01-01 to 2023-12-31',
                'total_sales': float(self.data['sales'].sum()),
                'total_orders': int(self.data['orders'].sum()),
                'total_customers': int(self.data['customers'].sum()),
                'avg_daily_sales': float(self.data.groupby('date')['sales'].sum().mean()),
                'best_category': self.data.groupby('category')['sales'].sum().idxmax(),
                'best_region': self.data.groupby('region')['sales'].sum().idxmax(),
                'best_month': self.data.groupby('month')['sales'].sum().idxmax()
            }
            
            with open('visualization_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"\n📊 Итоговый отчет:")
            print(f"  Общие продажи: {report['total_sales']:,.0f}")
            print(f"  Средние дневные продажи: {report['avg_daily_sales']:,.0f}")
            print(f"  Лучшая категория: {report['best_category']}")
            print(f"  Лучший регион: {report['best_region']}")
            print(f"  Лучший месяц: {report['best_month']}")
            print("Отчет сохранен: visualization_report.json")
    
    # Демонстрация
    visualizer = DataVisualizer()
    
    # Генерируем данные
    visualizer.generate_sales_data()
    
    # Создаем визуализации
    visualizer.create_time_series_plot()
    visualizer.create_correlation_analysis()
    visualizer.create_advanced_visualizations()
    
    # Генерируем отчет
    visualizer.generate_report()
    
    print("✅ Упражнение 3 завершено")
    print("Созданы файлы:")
    print("  - sales_dashboard.png")
    print("  - correlation_analysis.png")
    print("  - advanced_visualizations.png")
    print("  - visualization_report.json")

def main():
    """Главная функция для запуска всех упражнений"""
    
    exercises = [
        ("Пайплайн анализа данных", exercise_01_data_analysis_pipeline),
        ("Разработка Web API", exercise_02_web_api_development),
        ("Визуализация данных", exercise_03_data_visualization),
    ]
    
    print("📦 Упражнения: Внешние библиотеки в Python")
    print("=" * 70)
    print("Эти упражнения помогут освоить:")
    print("- Комплексный анализ данных с Pandas и NumPy")
    print("- Создание RESTful API с Flask")
    print("- Продвинутую визуализацию данных")
    print("- Интеграцию различных библиотек")
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
    
    print("\n🎉 Все упражнения внешних библиотек завершены!")

if __name__ == "__main__":
    main() 