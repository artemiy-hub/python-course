"""
Упражнения: Анализ данных и машинное обучение

Этот файл содержит практические упражнения для изучения анализа данных
и машинного обучения с использованием pandas, numpy, scikit-learn.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.datasets import make_classification, make_regression
import pytest
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import tempfile
import sqlite3
from pathlib import Path

# =============================================================================
# Упражнение 1: Анализ продаж магазина
# =============================================================================

"""
ЗАДАНИЕ 1: Store Sales Analysis

У вас есть данные о продажах магазина. Необходимо:

1. Создать класс SalesAnalyzer для анализа продаж
2. Реализовать методы:
   - load_data() - загрузка данных
   - clean_data() - очистка данных
   - calculate_metrics() - расчет метрик
   - find_best_products() - поиск топ продуктов
   - analyze_trends() - анализ трендов

3. Обработать следующие проблемы в данных:
   - Пропущенные значения
   - Отрицательные цены/количества
   - Дублирующие записи
   - Неправильные форматы дат

Данные содержат: date, product_id, product_name, category, price, quantity, customer_id
"""

# Ваш код здесь:
class SalesAnalyzer:
    """Анализатор продаж"""
    
    def __init__(self):
        # TODO: Реализуйте инициализацию
        pass
    
    def load_data(self, data_source) -> pd.DataFrame:
        """Загрузить данные о продажах"""
        # TODO: Реализуйте метод
        pass
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Очистить данные"""
        # TODO: Реализуйте метод
        pass
    
    def calculate_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Рассчитать основные метрики"""
        # TODO: Реализуйте метод
        pass
    
    def find_best_products(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """Найти топ продуктов по продажам"""
        # TODO: Реализуйте метод
        pass
    
    def analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ трендов продаж"""
        # TODO: Реализуйте метод
        pass

# Решение:
@dataclass
class SalesMetrics:
    """Метрики продаж"""
    total_revenue: float
    total_orders: int
    average_order_value: float
    unique_customers: int
    unique_products: int
    best_month: str
    worst_month: str

class SalesAnalyzerSolution:
    """Решение: Анализатор продаж"""
    
    def __init__(self):
        self.data = None
        self.clean_data_cache = None
    
    def generate_sample_data(self, n_records: int = 1000) -> pd.DataFrame:
        """Генерация тестовых данных"""
        np.random.seed(42)
        
        # Генерация дат
        start_date = datetime(2023, 1, 1)
        dates = [start_date + timedelta(days=x) for x in range(365)]
        
        # Продукты и категории
        products = [
            ('Laptop', 'Electronics'), ('Mouse', 'Electronics'), ('Keyboard', 'Electronics'),
            ('Monitor', 'Electronics'), ('Phone', 'Electronics'),
            ('Coffee', 'Food'), ('Tea', 'Food'), ('Cookies', 'Food'), ('Bread', 'Food'),
            ('T-Shirt', 'Clothing'), ('Jeans', 'Clothing'), ('Shoes', 'Clothing'),
            ('Book', 'Media'), ('DVD', 'Media'), ('Magazine', 'Media')
        ]
        
        # Генерация записей
        records = []
        for _ in range(n_records):
            date = np.random.choice(dates)
            product_name, category = products[np.random.randint(0, len(products))]
            product_id = f"P{hash(product_name) % 10000:04d}"
            
            # Различные цены для разных категорий
            if category == 'Electronics':
                price = np.random.uniform(50, 2000)
            elif category == 'Food':
                price = np.random.uniform(1, 50)
            elif category == 'Clothing':
                price = np.random.uniform(20, 200)
            else:  # Media
                price = np.random.uniform(5, 100)
            
            quantity = np.random.randint(1, 6)
            customer_id = f"C{np.random.randint(1, 500):04d}"
            
            records.append({
                'date': date,
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'price': price,
                'quantity': quantity,
                'customer_id': customer_id
            })
        
        df = pd.DataFrame(records)
        
        # Добавляем "проблемы" в данные для демонстрации очистки
        # Пропущенные значения
        missing_indices = np.random.choice(df.index, size=int(0.05 * len(df)), replace=False)
        df.loc[missing_indices[:len(missing_indices)//3], 'price'] = np.nan
        df.loc[missing_indices[len(missing_indices)//3:2*len(missing_indices)//3], 'product_name'] = np.nan
        df.loc[missing_indices[2*len(missing_indices)//3:], 'customer_id'] = np.nan
        
        # Отрицательные значения
        negative_indices = np.random.choice(df.index, size=int(0.02 * len(df)), replace=False)
        df.loc[negative_indices[:len(negative_indices)//2], 'price'] = -df.loc[negative_indices[:len(negative_indices)//2], 'price']
        df.loc[negative_indices[len(negative_indices)//2:], 'quantity'] = -df.loc[negative_indices[len(negative_indices)//2:], 'quantity']
        
        # Дубликаты
        duplicate_indices = np.random.choice(df.index, size=int(0.03 * len(df)), replace=False)
        duplicates = df.loc[duplicate_indices].copy()
        df = pd.concat([df, duplicates], ignore_index=True)
        
        return df
    
    def load_data(self, data_source=None) -> pd.DataFrame:
        """Загрузить данные о продажах"""
        if data_source is None:
            # Генерируем тестовые данные
            self.data = self.generate_sample_data()
        elif isinstance(data_source, str):
            # Загрузка из файла
            if data_source.endswith('.csv'):
                self.data = pd.read_csv(data_source)
            elif data_source.endswith('.xlsx'):
                self.data = pd.read_excel(data_source)
            else:
                raise ValueError("Unsupported file format")
        elif isinstance(data_source, pd.DataFrame):
            self.data = data_source.copy()
        else:
            raise ValueError("Invalid data source")
        
        return self.data
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Очистить данные"""
        cleaned_df = df.copy()
        
        # Статистика до очистки
        initial_count = len(cleaned_df)
        
        # 1. Удаление дубликатов
        cleaned_df = cleaned_df.drop_duplicates()
        duplicates_removed = initial_count - len(cleaned_df)
        
        # 2. Очистка отрицательных значений
        cleaned_df = cleaned_df[
            (cleaned_df['price'] > 0) & 
            (cleaned_df['quantity'] > 0)
        ].copy()
        
        # 3. Обработка пропущенных значений
        # Удаляем записи без названия продукта
        cleaned_df = cleaned_df.dropna(subset=['product_name'])
        
        # Заполняем пропущенные цены медианой по категории
        for category in cleaned_df['category'].unique():
            category_median_price = cleaned_df[
                (cleaned_df['category'] == category) & 
                (cleaned_df['price'].notna())
            ]['price'].median()
            
            cleaned_df.loc[
                (cleaned_df['category'] == category) & 
                (cleaned_df['price'].isna()), 
                'price'
            ] = category_median_price
        
        # Удаляем записи без customer_id (можно заполнить 'Unknown')
        cleaned_df = cleaned_df.dropna(subset=['customer_id'])
        
        # 4. Приведение типов данных
        cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
        cleaned_df['price'] = cleaned_df['price'].astype(float)
        cleaned_df['quantity'] = cleaned_df['quantity'].astype(int)
        
        # 5. Добавление вычисляемых полей
        cleaned_df['total_amount'] = cleaned_df['price'] * cleaned_df['quantity']
        cleaned_df['year'] = cleaned_df['date'].dt.year
        cleaned_df['month'] = cleaned_df['date'].dt.month
        cleaned_df['day_of_week'] = cleaned_df['date'].dt.dayofweek
        
        self.clean_data_cache = cleaned_df
        
        print(f"Очистка данных завершена:")
        print(f"  Исходных записей: {initial_count}")
        print(f"  Удалено дубликатов: {duplicates_removed}")
        print(f"  Осталось записей: {len(cleaned_df)}")
        print(f"  Процент потерь: {(initial_count - len(cleaned_df)) / initial_count * 100:.1f}%")
        
        return cleaned_df
    
    def calculate_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Рассчитать основные метрики"""
        metrics = {}
        
        # Основные метрики
        metrics['total_revenue'] = df['total_amount'].sum()
        metrics['total_orders'] = len(df)
        metrics['average_order_value'] = df['total_amount'].mean()
        metrics['median_order_value'] = df['total_amount'].median()
        
        # Клиенты и продукты
        metrics['unique_customers'] = df['customer_id'].nunique()
        metrics['unique_products'] = df['product_id'].nunique()
        metrics['unique_categories'] = df['category'].nunique()
        
        # Временные метрики
        monthly_sales = df.groupby(['year', 'month'])['total_amount'].sum()
        best_month_idx = monthly_sales.idxmax()
        worst_month_idx = monthly_sales.idxmin()
        
        metrics['best_month'] = f"{best_month_idx[0]}-{best_month_idx[1]:02d}"
        metrics['worst_month'] = f"{worst_month_idx[0]}-{worst_month_idx[1]:02d}"
        metrics['best_month_revenue'] = monthly_sales.max()
        metrics['worst_month_revenue'] = monthly_sales.min()
        
        # Статистика по категориям
        category_stats = df.groupby('category').agg({
            'total_amount': ['sum', 'count', 'mean'],
            'customer_id': 'nunique'
        }).round(2)
        
        metrics['category_performance'] = category_stats
        
        # День недели
        dow_sales = df.groupby('day_of_week')['total_amount'].mean()
        metrics['best_day_of_week'] = dow_sales.idxmax()  # 0=Monday, 6=Sunday
        metrics['worst_day_of_week'] = dow_sales.idxmin()
        
        return metrics
    
    def find_best_products(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """Найти топ продуктов по продажам"""
        product_performance = df.groupby(['product_id', 'product_name', 'category']).agg({
            'total_amount': ['sum', 'count', 'mean'],
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).round(2)
        
        # Упрощаем названия колонок
        product_performance.columns = [
            'total_revenue', 'order_count', 'avg_order_value', 
            'total_quantity', 'unique_customers'
        ]
        
        # Добавляем метрики
        product_performance['revenue_per_customer'] = (
            product_performance['total_revenue'] / product_performance['unique_customers']
        ).round(2)
        
        # Сортируем по выручке
        top_products = product_performance.sort_values('total_revenue', ascending=False).head(n)
        
        return top_products.reset_index()
    
    def analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Анализ трендов продаж"""
        trends = {}
        
        # Ежемесячные тренды
        monthly_trends = df.groupby(['year', 'month']).agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        monthly_trends['date'] = pd.to_datetime(monthly_trends[['year', 'month']].assign(day=1))
        monthly_trends = monthly_trends.sort_values('date')
        
        # Рост по месяцам
        monthly_trends['revenue_growth'] = monthly_trends['total_amount'].pct_change() * 100
        monthly_trends['customer_growth'] = monthly_trends['customer_id'].pct_change() * 100
        
        trends['monthly_data'] = monthly_trends
        trends['avg_monthly_growth'] = monthly_trends['revenue_growth'].mean()
        
        # Сезонность (по месяцам)
        seasonal_pattern = df.groupby('month')['total_amount'].mean()
        trends['seasonal_pattern'] = seasonal_pattern
        trends['peak_season_month'] = seasonal_pattern.idxmax()
        trends['low_season_month'] = seasonal_pattern.idxmin()
        
        # Тренды по дням недели
        dow_pattern = df.groupby('day_of_week')['total_amount'].mean()
        trends['daily_pattern'] = dow_pattern
        
        # Когортный анализ (упрощенный)
        # Первая покупка каждого клиента
        customer_first_purchase = df.groupby('customer_id')['date'].min().reset_index()
        customer_first_purchase['cohort_month'] = customer_first_purchase['date'].dt.to_period('M')
        
        # Добавляем когорту к основным данным
        df_with_cohort = df.merge(
            customer_first_purchase[['customer_id', 'cohort_month']], 
            on='customer_id'
        )
        df_with_cohort['order_month'] = df_with_cohort['date'].dt.to_period('M')
        
        # Период с момента первой покупки
        df_with_cohort['period_number'] = (
            df_with_cohort['order_month'] - df_with_cohort['cohort_month']
        ).apply(attrgetter('n'))
        
        # Таблица когорт (упрощенная)
        cohort_table = df_with_cohort.groupby(['cohort_month', 'period_number'])['customer_id'].nunique().reset_index()
        cohort_sizes = customer_first_purchase.groupby('cohort_month')['customer_id'].nunique()
        
        trends['cohort_analysis'] = {
            'cohort_table': cohort_table,
            'cohort_sizes': cohort_sizes
        }
        
        return trends

from operator import attrgetter

# Тесты для SalesAnalyzer
class TestSalesAnalyzer:
    """Тесты анализатора продаж"""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture анализатора продаж"""
        return SalesAnalyzerSolution()
    
    @pytest.fixture
    def sample_data(self, analyzer):
        """Fixture с тестовыми данными"""
        return analyzer.generate_sample_data(100)
    
    def test_load_data(self, analyzer):
        """Тест загрузки данных"""
        data = analyzer.load_data()
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert all(col in data.columns for col in ['date', 'product_id', 'price', 'quantity'])
    
    def test_clean_data(self, analyzer, sample_data):
        """Тест очистки данных"""
        cleaned = analyzer.clean_data(sample_data)
        
        # Проверяем, что нет отрицательных значений
        assert (cleaned['price'] > 0).all()
        assert (cleaned['quantity'] > 0).all()
        
        # Проверяем, что добавлены вычисляемые поля
        assert 'total_amount' in cleaned.columns
        assert 'year' in cleaned.columns
        assert 'month' in cleaned.columns
        
        # Проверяем, что total_amount рассчитан правильно
        assert (cleaned['total_amount'] == cleaned['price'] * cleaned['quantity']).all()
    
    def test_calculate_metrics(self, analyzer, sample_data):
        """Тест расчета метрик"""
        cleaned_data = analyzer.clean_data(sample_data)
        metrics = analyzer.calculate_metrics(cleaned_data)
        
        # Проверяем основные метрики
        assert 'total_revenue' in metrics
        assert 'total_orders' in metrics
        assert 'average_order_value' in metrics
        assert 'unique_customers' in metrics
        assert 'unique_products' in metrics
        
        # Проверяем логику расчетов
        expected_total_revenue = cleaned_data['total_amount'].sum()
        assert abs(metrics['total_revenue'] - expected_total_revenue) < 0.01
        
        assert metrics['total_orders'] == len(cleaned_data)
    
    def test_find_best_products(self, analyzer, sample_data):
        """Тест поиска топ продуктов"""
        cleaned_data = analyzer.clean_data(sample_data)
        top_products = analyzer.find_best_products(cleaned_data, n=5)
        
        assert len(top_products) <= 5
        assert 'total_revenue' in top_products.columns
        assert 'product_name' in top_products.columns
        
        # Проверяем, что сортировка по убыванию выручки
        revenues = top_products['total_revenue'].values
        assert all(revenues[i] >= revenues[i+1] for i in range(len(revenues)-1))

# =============================================================================
# Упражнение 2: Предсказание цен на недвижимость
# =============================================================================

"""
ЗАДАНИЕ 2: House Price Prediction

Создайте систему предсказания цен на недвижимость:

1. Класс HousePricePredictor
2. Методы:
   - prepare_features() - подготовка признаков
   - train_model() - обучение модели
   - evaluate_model() - оценка качества
   - predict_price() - предсказание цены
   - feature_importance() - важность признаков

3. Обработка различных типов данных:
   - Числовые признаки (площадь, количество комнат, возраст)
   - Категориальные признаки (район, тип дома)
   - Feature engineering (создание новых признаков)

Используйте несколько алгоритмов и выберите лучший.
"""

# Ваш код здесь:
class HousePricePredictor:
    """Предсказатель цен на недвижимость"""
    
    def __init__(self):
        # TODO: Реализуйте инициализацию
        pass
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Подготовить признаки для модели"""
        # TODO: Реализуйте метод
        pass
    
    def train_model(self, X: pd.DataFrame, y: pd.Series):
        """Обучить модель"""
        # TODO: Реализуйте метод
        pass
    
    def evaluate_model(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """Оценить качество модели"""
        # TODO: Реализуйте метод
        pass
    
    def predict_price(self, house_features: Dict[str, Any]) -> float:
        """Предсказать цену дома"""
        # TODO: Реализуйте метод
        pass

# Решение:
class HousePricePredictorSolution:
    """Решение: Предсказатель цен на недвижимость"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.best_model_name = None
        self.training_data = None
    
    def generate_house_data(self, n_houses: int = 1000) -> pd.DataFrame:
        """Генерация данных о недвижимости"""
        np.random.seed(42)
        
        # Базовые характеристики
        areas = np.random.normal(150, 50, n_houses)  # площадь в кв.м
        areas = np.clip(areas, 50, 500)  # ограничиваем разумными пределами
        
        rooms = np.random.poisson(3, n_houses) + 1  # количество комнат
        rooms = np.clip(rooms, 1, 8)
        
        age = np.random.exponential(15, n_houses)  # возраст дома
        age = np.clip(age, 0, 100)
        
        # Категориальные признаки
        districts = np.random.choice(['Downtown', 'Suburb', 'Outskirts'], n_houses, p=[0.3, 0.5, 0.2])
        house_types = np.random.choice(['Apartment', 'House', 'Townhouse'], n_houses, p=[0.6, 0.3, 0.1])
        conditions = np.random.choice(['Excellent', 'Good', 'Fair', 'Poor'], n_houses, p=[0.2, 0.4, 0.3, 0.1])
        
        # Feature engineering
        area_per_room = areas / rooms
        is_new = (age < 5).astype(int)
        is_large = (areas > 200).astype(int)
        
        # Расчет цены на основе признаков (с некоторым шумом)
        price_base = (
            areas * 2000 +  # базовая цена за кв.м
            rooms * 10000 +  # доплата за комнаты
            -age * 500 +  # скидка за возраст
            area_per_room * 1000  # доплата за просторность
        )
        
        # Коррекция по району
        district_multiplier = {'Downtown': 1.5, 'Suburb': 1.0, 'Outskirts': 0.7}
        price_base *= [district_multiplier[d] for d in districts]
        
        # Коррекция по типу дома
        type_multiplier = {'House': 1.2, 'Townhouse': 1.0, 'Apartment': 0.9}
        price_base *= [type_multiplier[t] for t in house_types]
        
        # Коррекция по состоянию
        condition_multiplier = {'Excellent': 1.2, 'Good': 1.0, 'Fair': 0.8, 'Poor': 0.6}
        price_base *= [condition_multiplier[c] for c in conditions]
        
        # Добавляем шум
        noise = np.random.normal(0, 20000, n_houses)
        prices = price_base + noise
        prices = np.clip(prices, 50000, 2000000)  # разумные пределы цен
        
        return pd.DataFrame({
            'area': areas,
            'rooms': rooms,
            'age': age,
            'district': districts,
            'house_type': house_types,
            'condition': conditions,
            'area_per_room': area_per_room,
            'is_new': is_new,
            'is_large': is_large,
            'price': prices
        })
    
    def prepare_features(self, df: pd.DataFrame, is_training: bool = True) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """Подготовить признаки для модели"""
        feature_df = df.copy()
        
        # Создание дополнительных признаков
        if 'area' in feature_df.columns and 'rooms' in feature_df.columns:
            feature_df['area_per_room'] = feature_df['area'] / feature_df['rooms']
        
        if 'age' in feature_df.columns:
            feature_df['is_new'] = (feature_df['age'] < 5).astype(int)
            feature_df['age_category'] = pd.cut(feature_df['age'], 
                                               bins=[0, 5, 15, 30, 100], 
                                               labels=['New', 'Recent', 'Mature', 'Old'])
        
        if 'area' in feature_df.columns:
            feature_df['is_large'] = (feature_df['area'] > 200).astype(int)
            feature_df['area_category'] = pd.cut(feature_df['area'], 
                                                bins=[0, 100, 150, 200, 500], 
                                                labels=['Small', 'Medium', 'Large', 'XLarge'])
        
        # Обработка категориальных признаков
        categorical_columns = ['district', 'house_type', 'condition', 'age_category', 'area_category']
        
        for col in categorical_columns:
            if col in feature_df.columns:
                if is_training:
                    # Создаем и сохраняем encoder
                    self.label_encoders[col] = LabelEncoder()
                    feature_df[col] = self.label_encoders[col].fit_transform(feature_df[col].astype(str))
                else:
                    # Используем сохраненный encoder
                    if col in self.label_encoders:
                        # Обрабатываем новые категории
                        unique_values = set(self.label_encoders[col].classes_)
                        feature_df[col] = feature_df[col].astype(str)
                        
                        # Заменяем неизвестные категории на самую частую
                        most_frequent = self.label_encoders[col].classes_[0]
                        feature_df[col] = feature_df[col].apply(
                            lambda x: x if x in unique_values else most_frequent
                        )
                        
                        feature_df[col] = self.label_encoders[col].transform(feature_df[col])
        
        # Выбираем признаки (исключаем цену)
        feature_columns = [col for col in feature_df.columns if col != 'price']
        X = feature_df[feature_columns]
        
        if is_training:
            self.feature_columns = feature_columns
        
        # Масштабирование признаков
        if is_training:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns, index=X.index)
        
        # Целевая переменная
        y = df['price'] if 'price' in df.columns else None
        
        return X_scaled_df, y
    
    def train_model(self, df: pd.DataFrame):
        """Обучить модели"""
        self.training_data = df.copy()
        
        # Подготовка данных
        X, y = self.prepare_features(df, is_training=True)
        
        # Разделение на обучающую и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Различные модели
        models_to_train = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Random Forest Tuned': RandomForestRegressor(
                n_estimators=200, 
                max_depth=15, 
                min_samples_split=5,
                random_state=42
            )
        }
        
        best_score = float('-inf')
        
        print("Обучение моделей:")
        for name, model in models_to_train.items():
            print(f"\n--- {name} ---")
            
            # Обучение
            model.fit(X_train, y_train)
            
            # Предсказания
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            
            # Метрики
            train_r2 = r2_score(y_train, y_pred_train)
            test_r2 = r2_score(y_test, y_pred_test)
            train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
            
            print(f"Train R²: {train_r2:.3f}, RMSE: {train_rmse:.0f}")
            print(f"Test R²: {test_r2:.3f}, RMSE: {test_rmse:.0f}")
            
            # Кросс-валидация
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
            print(f"CV R² (5-fold): {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
            
            # Сохраняем модель
            self.models[name] = {
                'model': model,
                'train_r2': train_r2,
                'test_r2': test_r2,
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'cv_r2_mean': cv_scores.mean(),
                'cv_r2_std': cv_scores.std()
            }
            
            # Определяем лучшую модель
            if test_r2 > best_score:
                best_score = test_r2
                self.best_model_name = name
        
        print(f"\nЛучшая модель: {self.best_model_name} (Test R²: {best_score:.3f})")
        
        # Сохраняем тестовые данные для дальнейшего использования
        self.X_test = X_test
        self.y_test = y_test
        
        return self.models
    
    def evaluate_model(self, model_name: str = None) -> Dict[str, float]:
        """Оценить качество модели"""
        if model_name is None:
            model_name = self.best_model_name
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model_info = self.models[model_name]
        
        evaluation = {
            'model_name': model_name,
            'train_r2': model_info['train_r2'],
            'test_r2': model_info['test_r2'],
            'train_rmse': model_info['train_rmse'],
            'test_rmse': model_info['test_rmse'],
            'cv_r2_mean': model_info['cv_r2_mean'],
            'cv_r2_std': model_info['cv_r2_std']
        }
        
        return evaluation
    
    def feature_importance(self, model_name: str = None) -> pd.DataFrame:
        """Важность признаков"""
        if model_name is None:
            model_name = self.best_model_name
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model = self.models[model_name]['model']
        
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            return importance_df
        else:
            # Для линейной регрессии используем коэффициенты
            if hasattr(model, 'coef_'):
                importance_df = pd.DataFrame({
                    'feature': self.feature_columns,
                    'coefficient': model.coef_,
                    'abs_coefficient': np.abs(model.coef_)
                }).sort_values('abs_coefficient', ascending=False)
                
                return importance_df
        
        return pd.DataFrame()
    
    def predict_price(self, house_features: Dict[str, Any]) -> Dict[str, Any]:
        """Предсказать цену дома"""
        if not self.models or self.best_model_name is None:
            raise ValueError("Model not trained yet")
        
        # Создаем DataFrame из входных данных
        input_df = pd.DataFrame([house_features])
        
        # Подготавливаем признаки
        X_input, _ = self.prepare_features(input_df, is_training=False)
        
        # Предсказание лучшей моделью
        best_model = self.models[self.best_model_name]['model']
        prediction = best_model.predict(X_input)[0]
        
        # Предсказания всеми моделями
        all_predictions = {}
        for name, model_info in self.models.items():
            model_pred = model_info['model'].predict(X_input)[0]
            all_predictions[name] = model_pred
        
        return {
            'predicted_price': prediction,
            'model_used': self.best_model_name,
            'all_predictions': all_predictions,
            'input_features': house_features
        }

# Тесты для HousePricePredictor
class TestHousePricePredictor:
    """Тесты предсказателя цен на недвижимость"""
    
    @pytest.fixture
    def predictor(self):
        """Fixture предсказателя"""
        return HousePricePredictorSolution()
    
    @pytest.fixture
    def house_data(self, predictor):
        """Fixture с данными о недвижимости"""
        return predictor.generate_house_data(200)
    
    def test_generate_house_data(self, predictor):
        """Тест генерации данных"""
        data = predictor.generate_house_data(100)
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 100
        assert 'price' in data.columns
        assert 'area' in data.columns
        assert 'rooms' in data.columns
        
        # Проверяем разумность данных
        assert (data['price'] > 0).all()
        assert (data['area'] > 0).all()
        assert (data['rooms'] > 0).all()
    
    def test_prepare_features(self, predictor, house_data):
        """Тест подготовки признаков"""
        X, y = predictor.prepare_features(house_data, is_training=True)
        
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert len(X) == len(y)
        assert 'price' not in X.columns  # цена не должна быть в признаках
    
    def test_train_model(self, predictor, house_data):
        """Тест обучения модели"""
        models = predictor.train_model(house_data)
        
        assert len(models) > 0
        assert predictor.best_model_name is not None
        assert predictor.best_model_name in models
        
        # Проверяем качество лучшей модели
        best_model_info = models[predictor.best_model_name]
        assert best_model_info['test_r2'] > 0.5  # Разумное качество для синтетических данных
    
    def test_predict_price(self, predictor, house_data):
        """Тест предсказания цены"""
        predictor.train_model(house_data)
        
        # Тестовые характеристики дома
        test_house = {
            'area': 150,
            'rooms': 3,
            'age': 10,
            'district': 'Suburb',
            'house_type': 'House',
            'condition': 'Good'
        }
        
        result = predictor.predict_price(test_house)
        
        assert 'predicted_price' in result
        assert 'model_used' in result
        assert result['predicted_price'] > 0
        assert isinstance(result['predicted_price'], (int, float))

# =============================================================================
# Упражнение 3: Анализ клиентской сегментации
# =============================================================================

"""
ЗАДАНИЕ 3: Customer Segmentation

Создайте систему сегментации клиентов:

1. Класс CustomerSegmentation
2. RFM анализ (Recency, Frequency, Monetary)
3. K-means кластеризация
4. Профилирование сегментов
5. Рекомендации по работе с сегментами

Данные: customer_id, purchase_date, amount, product_category
"""

# Ваш код здесь:
class CustomerSegmentation:
    """Сегментация клиентов"""
    
    def __init__(self):
        # TODO: Реализуйте инициализацию
        pass
    
    def calculate_rfm(self, df: pd.DataFrame) -> pd.DataFrame:
        """Рассчитать RFM метрики"""
        # TODO: Реализуйте метод
        pass
    
    def perform_clustering(self, rfm_df: pd.DataFrame, n_clusters: int = 4):
        """Выполнить кластеризацию"""
        # TODO: Реализуйте метод
        pass
    
    def profile_segments(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Профилировать сегменты"""
        # TODO: Реализуйте метод
        pass

# Решение (краткая версия):
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class CustomerSegmentationSolution:
    """Решение: Сегментация клиентов"""
    
    def __init__(self):
        self.kmeans = None
        self.scaler = StandardScaler()
        self.rfm_data = None
        self.segments = None
    
    def generate_customer_data(self, n_customers: int = 500, n_transactions: int = 5000) -> pd.DataFrame:
        """Генерация данных о клиентах"""
        np.random.seed(42)
        
        # Генерация транзакций
        transactions = []
        customer_ids = [f"C{i:04d}" for i in range(1, n_customers + 1)]
        
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        
        categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home']
        
        for _ in range(n_transactions):
            customer_id = np.random.choice(customer_ids)
            
            # Генерируем случайную дату
            days_diff = (end_date - start_date).days
            random_days = np.random.randint(0, days_diff)
            purchase_date = start_date + timedelta(days=random_days)
            
            # Сумма покупки зависит от категории
            category = np.random.choice(categories)
            if category == 'Electronics':
                amount = np.random.uniform(100, 2000)
            elif category == 'Clothing':
                amount = np.random.uniform(20, 500)
            elif category == 'Food':
                amount = np.random.uniform(5, 100)
            elif category == 'Books':
                amount = np.random.uniform(10, 80)
            else:  # Home
                amount = np.random.uniform(30, 800)
            
            transactions.append({
                'customer_id': customer_id,
                'purchase_date': purchase_date,
                'amount': amount,
                'product_category': category
            })
        
        return pd.DataFrame(transactions)
    
    def calculate_rfm(self, df: pd.DataFrame, reference_date: datetime = None) -> pd.DataFrame:
        """Рассчитать RFM метрики"""
        if reference_date is None:
            reference_date = df['purchase_date'].max() + timedelta(days=1)
        
        # Группируем по клиентам
        rfm = df.groupby('customer_id').agg({
            'purchase_date': lambda x: (reference_date - x.max()).days,  # Recency
            'amount': ['count', 'sum']  # Frequency, Monetary
        })
        
        # Упрощаем названия колонок
        rfm.columns = ['Recency', 'Frequency', 'Monetary']
        
        # RFM scores (1-5, где 5 - лучше)
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
        
        # Комбинированный RFM score
        rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
        
        self.rfm_data = rfm
        return rfm
    
    def perform_clustering(self, rfm_df: pd.DataFrame = None, n_clusters: int = 4):
        """Выполнить кластеризацию"""
        if rfm_df is None:
            rfm_df = self.rfm_data
        
        if rfm_df is None:
            raise ValueError("RFM data not calculated. Run calculate_rfm first.")
        
        # Подготовка данных для кластеризации
        clustering_data = rfm_df[['Recency', 'Frequency', 'Monetary']]
        
        # Масштабирование
        scaled_data = self.scaler.fit_transform(clustering_data)
        
        # K-means кластеризация
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = self.kmeans.fit_predict(scaled_data)
        
        # Добавляем кластеры к RFM данным
        rfm_df['Cluster'] = clusters
        
        self.segments = rfm_df
        return rfm_df
    
    def profile_segments(self, df: pd.DataFrame = None) -> Dict[str, Any]:
        """Профилировать сегменты"""
        if df is None:
            df = self.segments
        
        if df is None or 'Cluster' not in df.columns:
            raise ValueError("Clustering not performed. Run perform_clustering first.")
        
        profiles = {}
        
        # Статистика по кластерам
        cluster_stats = df.groupby('Cluster').agg({
            'Recency': ['mean', 'median'],
            'Frequency': ['mean', 'median'],
            'Monetary': ['mean', 'median'],
            'R_Score': 'mean',
            'F_Score': 'mean',
            'M_Score': 'mean'
        }).round(2)
        
        profiles['cluster_statistics'] = cluster_stats
        
        # Размеры кластеров
        cluster_sizes = df['Cluster'].value_counts().sort_index()
        profiles['cluster_sizes'] = cluster_sizes
        
        # Интерпретация кластеров
        interpretations = {}
        for cluster in df['Cluster'].unique():
            cluster_data = df[df['Cluster'] == cluster]
            
            avg_recency = cluster_data['Recency'].mean()
            avg_frequency = cluster_data['Frequency'].mean()
            avg_monetary = cluster_data['Monetary'].mean()
            
            # Простая логика интерпретации
            if avg_recency < 30 and avg_frequency > 5 and avg_monetary > 500:
                interpretation = "Champions (Лучшие клиенты)"
            elif avg_recency < 60 and avg_frequency > 3:
                interpretation = "Loyal Customers (Лояльные клиенты)"
            elif avg_monetary > 1000:
                interpretation = "Big Spenders (Много тратящие)"
            elif avg_recency > 180:
                interpretation = "Lost Customers (Потерянные клиенты)"
            else:
                interpretation = "Regular Customers (Обычные клиенты)"
            
            interpretations[cluster] = interpretation
        
        profiles['interpretations'] = interpretations
        
        return profiles

# =============================================================================
# Запуск упражнений
# =============================================================================

def run_exercises():
    """Запуск всех упражнений"""
    print("=== Упражнения: Анализ данных и ML ===\n")
    
    # 1. Анализ продаж
    print("1. Анализ продаж магазина...")
    analyzer = SalesAnalyzerSolution()
    sales_data = analyzer.load_data()
    cleaned_data = analyzer.clean_data(sales_data)
    metrics = analyzer.calculate_metrics(cleaned_data)
    
    print(f"   Общая выручка: ${metrics['total_revenue']:,.0f}")
    print(f"   Количество заказов: {metrics['total_orders']}")
    print(f"   Средний чек: ${metrics['average_order_value']:.0f}")
    
    # 2. Предсказание цен на недвижимость
    print("\n2. Предсказание цен на недвижимость...")
    predictor = HousePricePredictorSolution()
    house_data = predictor.generate_house_data(500)
    models = predictor.train_model(house_data)
    
    # Тестовое предсказание
    test_house = {
        'area': 150,
        'rooms': 3,
        'age': 10,
        'district': 'Suburb',
        'house_type': 'House',
        'condition': 'Good'
    }
    
    prediction = predictor.predict_price(test_house)
    print(f"   Предсказанная цена дома: ${prediction['predicted_price']:,.0f}")
    print(f"   Лучшая модель: {prediction['model_used']}")
    
    # 3. Сегментация клиентов
    print("\n3. Сегментация клиентов...")
    segmentation = CustomerSegmentationSolution()
    customer_data = segmentation.generate_customer_data(200, 2000)
    
    rfm = segmentation.calculate_rfm(customer_data)
    clustered_rfm = segmentation.perform_clustering(rfm, n_clusters=4)
    profiles = segmentation.profile_segments()
    
    print(f"   Количество клиентов: {len(rfm)}")
    print(f"   Количество сегментов: {len(profiles['cluster_sizes'])}")
    
    for cluster, interpretation in profiles['interpretations'].items():
        size = profiles['cluster_sizes'][cluster]
        print(f"   Сегмент {cluster}: {interpretation} ({size} клиентов)")
    
    print("\n✅ Все упражнения выполнены успешно!")
    print("📊 Теперь вы можете анализировать данные и строить ML модели!")

if __name__ == "__main__":
    run_exercises() 