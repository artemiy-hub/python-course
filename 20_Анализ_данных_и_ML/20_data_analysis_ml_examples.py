"""
Примеры: Анализ данных и машинное обучение

Этот файл содержит практические примеры анализа данных и машинного обучения
с использованием pandas, numpy, scikit-learn и других популярных библиотек.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.datasets import make_classification, make_regression, load_iris, load_boston
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import warnings
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import sqlite3
from pathlib import Path

warnings.filterwarnings('ignore')

# =============================================================================
# Пример 1: Базовая работа с pandas DataFrame
# =============================================================================

def pandas_basics_demo():
    """Демонстрация основных операций с pandas"""
    
    print("=== Pandas Basics Demo ===")
    
    # Создание данных
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
        'Age': [25, 30, 35, 28, 32, 27],
        'City': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin', 'Sydney'],
        'Salary': [50000, 60000, 75000, 55000, 68000, 52000],
        'Department': ['IT', 'HR', 'Finance', 'IT', 'Finance', 'HR'],
        'Join_Date': ['2020-01-15', '2019-06-20', '2018-03-10', '2021-09-05', '2020-11-30', '2022-02-14']
    }
    
    # Создание DataFrame
    df = pd.DataFrame(data)
    df['Join_Date'] = pd.to_datetime(df['Join_Date'])
    
    print("Исходные данные:")
    print(df)
    print(f"\nИнформация о DataFrame:")
    print(df.info())
    
    # Базовая статистика
    print(f"\nОписательная статистика:")
    print(df.describe())
    
    # Группировка данных
    print(f"\nСредняя зарплата по отделам:")
    dept_salary = df.groupby('Department')['Salary'].agg(['mean', 'median', 'count'])
    print(dept_salary)
    
    # Фильтрация данных
    high_earners = df[df['Salary'] > 60000]
    print(f"\nСотрудники с зарплатой > 60000:")
    print(high_earners[['Name', 'Salary', 'Department']])
    
    # Добавление вычисляемых столбцов
    df['Years_Employed'] = (datetime.now() - df['Join_Date']).dt.days / 365.25
    df['Salary_Category'] = pd.cut(df['Salary'], 
                                   bins=[0, 55000, 65000, float('inf')], 
                                   labels=['Low', 'Medium', 'High'])
    
    print(f"\nДанные с новыми столбцами:")
    print(df[['Name', 'Salary', 'Years_Employed', 'Salary_Category']])
    
    return df

def advanced_pandas_operations():
    """Продвинутые операции с pandas"""
    
    print("\n=== Advanced Pandas Operations ===")
    
    # Создание более сложного датасета
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=365, freq='D')
    
    sales_data = pd.DataFrame({
        'Date': dates,
        'Product': np.random.choice(['A', 'B', 'C'], 365),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 365),
        'Sales': np.random.normal(1000, 200, 365),
        'Units': np.random.poisson(50, 365),
        'Temperature': np.random.normal(20, 10, 365)
    })
    
    # Обеспечиваем положительные значения
    sales_data['Sales'] = np.abs(sales_data['Sales'])
    sales_data['Units'] = np.abs(sales_data['Units'])
    
    print("Данные о продажах:")
    print(sales_data.head())
    
    # Временные ряды
    sales_data.set_index('Date', inplace=True)
    monthly_sales = sales_data.resample('M')['Sales'].agg(['sum', 'mean', 'count'])
    print(f"\nМесячные продажи:")
    print(monthly_sales.head())
    
    # Pivot table
    pivot_table = sales_data.pivot_table(
        values='Sales', 
        index='Product', 
        columns='Region', 
        aggfunc='mean'
    )
    print(f"\nPivot table (средние продажи по продуктам и регионам):")
    print(pivot_table)
    
    # Корреляционный анализ
    correlation_matrix = sales_data[['Sales', 'Units', 'Temperature']].corr()
    print(f"\nКорреляционная матрица:")
    print(correlation_matrix)
    
    # Rolling window analysis
    sales_data['Sales_MA_7'] = sales_data['Sales'].rolling(window=7).mean()
    sales_data['Sales_MA_30'] = sales_data['Sales'].rolling(window=30).mean()
    
    print(f"\nДанные со скользящими средними:")
    print(sales_data[['Sales', 'Sales_MA_7', 'Sales_MA_30']].head(10))
    
    return sales_data

# =============================================================================
# Пример 2: Обработка и очистка данных
# =============================================================================

def data_cleaning_demo():
    """Демонстрация очистки и обработки данных"""
    
    print("\n=== Data Cleaning Demo ===")
    
    # Создание "грязных" данных
    dirty_data = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5, 6, 7, 8],
        'Name': ['Alice Smith', 'bob jones', 'CHARLIE BROWN', 'diana prince', None, 'eve adams', 'frank castle', ''],
        'Email': ['alice@email.com', 'BOB@EMAIL.COM', 'charlie@invalid', None, 'eve@email.com', 'invalid-email', 'frank@email.com', 'test@email.com'],
        'Age': [25, 30, None, 28, 150, 32, -5, 27],
        'Salary': [50000, '60000', 75000, None, 68000, '52k', 'unknown', 45000],
        'Join_Date': ['2020-01-15', '2019/06/20', '2018-03-10', None, '30-11-2020', '2022-02-14', 'invalid', '2021-09-05']
    })
    
    print("Исходные 'грязные' данные:")
    print(dirty_data)
    print(f"\nИнформация о пропущенных значениях:")
    print(dirty_data.isnull().sum())
    
    # Копия для обработки
    clean_data = dirty_data.copy()
    
    # Очистка имен
    def clean_name(name):
        if pd.isna(name) or name == '':
            return None
        return ' '.join(word.capitalize() for word in str(name).split())
    
    clean_data['Name'] = clean_data['Name'].apply(clean_name)
    
    # Очистка email
    def clean_email(email):
        if pd.isna(email):
            return None
        email = str(email).lower()
        if '@' in email and '.' in email:
            return email
        return None
    
    clean_data['Email'] = clean_data['Email'].apply(clean_email)
    
    # Очистка возраста
    def clean_age(age):
        if pd.isna(age):
            return None
        try:
            age = int(age)
            if 18 <= age <= 100:
                return age
        except:
            pass
        return None
    
    clean_data['Age'] = clean_data['Age'].apply(clean_age)
    
    # Очистка зарплаты
    def clean_salary(salary):
        if pd.isna(salary):
            return None
        
        salary_str = str(salary).lower().replace(',', '').replace('k', '000')
        
        try:
            # Извлекаем числа
            import re
            numbers = re.findall(r'\d+', salary_str)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return None
    
    clean_data['Salary'] = clean_data['Salary'].apply(clean_salary)
    
    # Очистка дат
    def clean_date(date):
        if pd.isna(date):
            return None
        
        date_str = str(date)
        
        # Различные форматы дат
        formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y']
        
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        
        try:
            return pd.to_datetime(date_str)
        except:
            return None
    
    clean_data['Join_Date'] = clean_data['Join_Date'].apply(clean_date)
    
    print(f"\nОчищенные данные:")
    print(clean_data)
    print(f"\nПропущенные значения после очистки:")
    print(clean_data.isnull().sum())
    
    # Заполнение пропущенных значений
    # Возраст - медианой
    clean_data['Age'].fillna(clean_data['Age'].median(), inplace=True)
    
    # Зарплата - средним по возрастной группе
    age_groups = pd.cut(clean_data['Age'], bins=[0, 30, 40, 100], labels=['Young', 'Middle', 'Senior'])
    clean_data['Age_Group'] = age_groups
    
    for group in ['Young', 'Middle', 'Senior']:
        group_mean_salary = clean_data[clean_data['Age_Group'] == group]['Salary'].mean()
        clean_data.loc[(clean_data['Age_Group'] == group) & (clean_data['Salary'].isna()), 'Salary'] = group_mean_salary
    
    print(f"\nДанные после заполнения пропусков:")
    print(clean_data)
    
    return clean_data

# =============================================================================
# Пример 3: Исследовательский анализ данных (EDA)
# =============================================================================

def exploratory_data_analysis():
    """Исследовательский анализ данных"""
    
    print("\n=== Exploratory Data Analysis ===")
    
    # Загрузим встроенный датасет iris
    iris = load_iris()
    iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris_df['species'] = iris.target
    iris_df['species_name'] = iris_df['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
    
    print("Датасет Iris:")
    print(iris_df.head())
    
    # Базовая статистика
    print(f"\nОписательная статистика:")
    print(iris_df.describe())
    
    # Анализ распределения по классам
    print(f"\nРаспределение по видам:")
    print(iris_df['species_name'].value_counts())
    
    # Корреляционный анализ
    correlation_matrix = iris_df.select_dtypes(include=[np.number]).corr()
    print(f"\nКорреляционная матрица:")
    print(correlation_matrix)
    
    # Статистика по группам
    print(f"\nСтатистика по видам:")
    species_stats = iris_df.groupby('species_name').agg({
        'sepal length (cm)': ['mean', 'std'],
        'sepal width (cm)': ['mean', 'std'],
        'petal length (cm)': ['mean', 'std'],
        'petal width (cm)': ['mean', 'std']
    })
    print(species_stats)
    
    # Выбросы (outliers)
    def detect_outliers(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        return outliers
    
    print(f"\nВыбросы в sepal length:")
    outliers = detect_outliers(iris_df, 'sepal length (cm)')
    print(f"Найдено выбросов: {len(outliers)}")
    if len(outliers) > 0:
        print(outliers[['sepal length (cm)', 'species_name']])
    
    return iris_df

# =============================================================================
# Пример 4: Машинное обучение - классификация
# =============================================================================

def machine_learning_classification():
    """Пример классификации с машинным обучением"""
    
    print("\n=== Machine Learning Classification ===")
    
    # Создание синтетических данных
    X, y = make_classification(
        n_samples=1000, 
        n_features=20, 
        n_informative=10, 
        n_redundant=5, 
        n_clusters_per_class=1, 
        random_state=42
    )
    
    # Преобразование в DataFrame для удобства
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    print(f"Размер датасета: {df.shape}")
    print(f"Распределение классов:")
    print(df['target'].value_counts())
    
    # Разделение на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"\nРазмеры выборок:")
    print(f"Обучающая: {X_train.shape}")
    print(f"Тестовая: {X_test.shape}")
    
    # Масштабирование признаков
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Обучение различных моделей
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n--- {name} ---")
        
        # Обучение
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        # Оценка качества
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Точность: {accuracy:.3f}")
        
        # Кросс-валидация
        if name == 'Logistic Regression':
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
        else:
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        print(f"Кросс-валидация (5-fold): {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        # Отчет о классификации
        print(f"Отчет о классификации:")
        print(classification_report(y_test, y_pred))
        
        results[name] = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    # Сравнение моделей
    print(f"\n=== Сравнение моделей ===")
    comparison_df = pd.DataFrame(results).T
    print(comparison_df)
    
    return models, results

# =============================================================================
# Пример 5: Машинное обучение - регрессия
# =============================================================================

def machine_learning_regression():
    """Пример регрессии с машинным обучением"""
    
    print("\n=== Machine Learning Regression ===")
    
    # Создание синтетических данных для регрессии
    X, y = make_regression(
        n_samples=1000, 
        n_features=10, 
        noise=0.1, 
        random_state=42
    )
    
    # Преобразование в DataFrame
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    print(f"Размер датасета: {df.shape}")
    print(f"Статистика целевой переменной:")
    print(df['target'].describe())
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    # Модели для регрессии
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n--- {name} ---")
        
        # Обучение
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Метрики
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        print(f"MSE: {mse:.3f}")
        print(f"RMSE: {rmse:.3f}")
        print(f"R²: {r2:.3f}")
        
        # Кросс-валидация
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        print(f"Кросс-валидация R² (5-fold): {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        results[name] = {
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'cv_r2_mean': cv_scores.mean(),
            'cv_r2_std': cv_scores.std()
        }
        
        # Важность признаков (для Random Forest)
        if hasattr(model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"Топ-5 важных признаков:")
            print(feature_importance.head())
    
    # Сравнение моделей
    print(f"\n=== Сравнение моделей ===")
    comparison_df = pd.DataFrame(results).T
    print(comparison_df)
    
    return models, results

# =============================================================================
# Пример 6: Гиперпараметрическая оптимизация
# =============================================================================

def hyperparameter_optimization():
    """Оптимизация гиперпараметров с Grid Search"""
    
    print("\n=== Hyperparameter Optimization ===")
    
    # Загрузка данных
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Определение сетки параметров для Random Forest
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    # Grid Search
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        rf, 
        param_grid, 
        cv=5, 
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    print("Выполняем Grid Search...")
    grid_search.fit(X_train, y_train)
    
    print(f"\nЛучшие параметры:")
    print(grid_search.best_params_)
    
    print(f"\nЛучший результат кросс-валидации: {grid_search.best_score_:.3f}")
    
    # Оценка на тестовой выборке
    best_model = grid_search.best_estimator_
    test_accuracy = best_model.score(X_test, y_test)
    print(f"Точность на тестовой выборке: {test_accuracy:.3f}")
    
    # Анализ результатов Grid Search
    results_df = pd.DataFrame(grid_search.cv_results_)
    
    print(f"\nТоп-5 комбинаций параметров:")
    top_results = results_df.nlargest(5, 'mean_test_score')[
        ['params', 'mean_test_score', 'std_test_score']
    ]
    print(top_results)
    
    return grid_search

# =============================================================================
# Пример 7: Pipeline для машинного обучения
# =============================================================================

def ml_pipeline_example():
    """Пример создания ML pipeline"""
    
    print("\n=== ML Pipeline Example ===")
    
    # Создание смешанных данных (числовые и категориальные)
    np.random.seed(42)
    n_samples = 1000
    
    data = pd.DataFrame({
        'age': np.random.randint(18, 65, n_samples),
        'income': np.random.normal(50000, 15000, n_samples),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples),
        'city': np.random.choice(['New York', 'London', 'Paris', 'Tokyo'], n_samples),
        'experience': np.random.randint(0, 30, n_samples)
    })
    
    # Создание целевой переменной на основе признаков
    target = (
        (data['age'] * 0.01) + 
        (data['income'] * 0.00001) + 
        (data['experience'] * 0.02) + 
        np.random.normal(0, 0.1, n_samples)
    )
    data['promoted'] = (target > np.median(target)).astype(int)
    
    print("Данные для pipeline:")
    print(data.head())
    print(f"\nТипы данных:")
    print(data.dtypes)
    
    # Определение признаков
    numeric_features = ['age', 'income', 'experience']
    categorical_features = ['education', 'city']
    
    X = data[numeric_features + categorical_features]
    y = data['promoted']
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Создание preprocessing pipeline
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    # Создание полного pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print(f"\nПайплайн:")
    print(pipeline)
    
    # Обучение pipeline
    pipeline.fit(X_train, y_train)
    
    # Предсказания
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nТочность pipeline: {accuracy:.3f}")
    
    # Получение названий признаков после preprocessing
    feature_names = (numeric_features + 
                    list(pipeline.named_steps['preprocessor']
                         .named_transformers_['cat']
                         .get_feature_names_out(categorical_features)))
    
    print(f"\nПризнаки после preprocessing ({len(feature_names)} признаков):")
    print(feature_names[:10])  # Первые 10 признаков
    
    # Важность признаков
    importances = pipeline.named_steps['classifier'].feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    print(f"\nТоп-10 важных признаков:")
    print(feature_importance_df.head(10))
    
    return pipeline

# =============================================================================
# Пример 8: Работа с временными рядами
# =============================================================================

def time_series_analysis():
    """Анализ временных рядов"""
    
    print("\n=== Time Series Analysis ===")
    
    # Создание временного ряда
    dates = pd.date_range('2020-01-01', periods=365*2, freq='D')
    
    # Создание синтетических данных с трендом и сезонностью
    trend = np.linspace(100, 200, len(dates))
    seasonal = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    noise = np.random.normal(0, 5, len(dates))
    
    ts_data = pd.DataFrame({
        'date': dates,
        'value': trend + seasonal + noise
    })
    ts_data.set_index('date', inplace=True)
    
    print("Временной ряд:")
    print(ts_data.head())
    
    # Базовая статистика
    print(f"\nОписательная статистика:")
    print(ts_data.describe())
    
    # Ресэмплинг
    monthly_data = ts_data.resample('M').agg({
        'value': ['mean', 'min', 'max', 'std']
    })
    monthly_data.columns = ['mean', 'min', 'max', 'std']
    
    print(f"\nМесячная агрегация (первые 10 месяцев):")
    print(monthly_data.head(10))
    
    # Скользящие средние
    ts_data['MA_7'] = ts_data['value'].rolling(window=7).mean()
    ts_data['MA_30'] = ts_data['value'].rolling(window=30).mean()
    ts_data['MA_90'] = ts_data['value'].rolling(window=90).mean()
    
    print(f"\nДанные со скользящими средними:")
    print(ts_data.head(10))
    
    # Расчет изменений
    ts_data['pct_change'] = ts_data['value'].pct_change()
    ts_data['diff'] = ts_data['value'].diff()
    
    # Выявление выбросов
    def detect_outliers_ts(series, window=30, threshold=3):
        rolling_mean = series.rolling(window=window).mean()
        rolling_std = series.rolling(window=window).std()
        
        z_scores = np.abs((series - rolling_mean) / rolling_std)
        return z_scores > threshold
    
    ts_data['outlier'] = detect_outliers_ts(ts_data['value'])
    outliers_count = ts_data['outlier'].sum()
    
    print(f"\nВыбросы найдены: {outliers_count}")
    if outliers_count > 0:
        print("Первые 5 выбросов:")
        print(ts_data[ts_data['outlier']].head()[['value', 'MA_30']])
    
    # Декомпозиция временного ряда (упрощенная)
    # Вычисляем тренд как скользящее среднее
    ts_data['trend'] = ts_data['value'].rolling(window=365, center=True).mean()
    
    # Деtrended данные
    ts_data['detrended'] = ts_data['value'] - ts_data['trend']
    
    # Сезонная компонента (упрощенно)
    ts_data['day_of_year'] = ts_data.index.dayofyear
    seasonal_pattern = ts_data.groupby('day_of_year')['detrended'].mean()
    ts_data['seasonal'] = ts_data['day_of_year'].map(seasonal_pattern)
    
    # Остатки
    ts_data['residual'] = ts_data['detrended'] - ts_data['seasonal']
    
    print(f"\nДекомпозиция временного ряда:")
    print(ts_data[['value', 'trend', 'seasonal', 'residual']].dropna().head())
    
    return ts_data

# =============================================================================
# Пример 9: A/B тестирование
# =============================================================================

def ab_testing_analysis():
    """Анализ A/B тестирования"""
    
    print("\n=== A/B Testing Analysis ===")
    
    # Генерация данных A/B теста
    np.random.seed(42)
    
    # Контрольная группа A
    n_control = 1000
    conversion_rate_control = 0.12
    control_conversions = np.random.binomial(1, conversion_rate_control, n_control)
    
    # Тестовая группа B
    n_treatment = 1000
    conversion_rate_treatment = 0.14  # На 2% выше
    treatment_conversions = np.random.binomial(1, conversion_rate_treatment, n_treatment)
    
    # Создание DataFrame
    ab_data = pd.DataFrame({
        'user_id': range(n_control + n_treatment),
        'group': ['A'] * n_control + ['B'] * n_treatment,
        'converted': np.concatenate([control_conversions, treatment_conversions])
    })
    
    print("Данные A/B теста:")
    print(ab_data.head())
    
    # Базовая статистика
    results = ab_data.groupby('group').agg({
        'converted': ['count', 'sum', 'mean']
    })
    results.columns = ['total_users', 'conversions', 'conversion_rate']
    
    print(f"\nРезультаты по группам:")
    print(results)
    
    # Расчет статистической значимости
    from scipy import stats
    
    # Данные для теста
    control_conversions_total = results.loc['A', 'conversions']
    control_total = results.loc['A', 'total_users']
    treatment_conversions_total = results.loc['B', 'conversions']
    treatment_total = results.loc['B', 'total_users']
    
    # Chi-square тест
    contingency_table = np.array([
        [control_conversions_total, control_total - control_conversions_total],
        [treatment_conversions_total, treatment_total - treatment_conversions_total]
    ])
    
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    print(f"\nСтатистический тест (Chi-square):")
    print(f"Chi-square статистика: {chi2:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Статистически значимо (p < 0.05): {p_value < 0.05}")
    
    # Доверительные интервалы для конверсии
    def proportion_confint(count, total, alpha=0.05):
        """Доверительный интервал для пропорции"""
        prop = count / total
        z = stats.norm.ppf(1 - alpha/2)
        se = np.sqrt(prop * (1 - prop) / total)
        return prop - z * se, prop + z * se
    
    control_ci = proportion_confint(control_conversions_total, control_total)
    treatment_ci = proportion_confint(treatment_conversions_total, treatment_total)
    
    print(f"\nДоверительные интервалы (95%):")
    print(f"Группа A: {control_ci[0]:.4f} - {control_ci[1]:.4f}")
    print(f"Группа B: {treatment_ci[0]:.4f} - {treatment_ci[1]:.4f}")
    
    # Relative lift
    control_rate = results.loc['A', 'conversion_rate']
    treatment_rate = results.loc['B', 'conversion_rate']
    relative_lift = (treatment_rate - control_rate) / control_rate * 100
    
    print(f"\nОтносительное улучшение: {relative_lift:.1f}%")
    
    # Размер эффекта (Cohen's h)
    def cohens_h(p1, p2):
        """Cohen's h для разности пропорций"""
        return 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))
    
    effect_size = cohens_h(treatment_rate, control_rate)
    print(f"Размер эффекта (Cohen's h): {effect_size:.4f}")
    
    # Интерпретация размера эффекта
    if abs(effect_size) < 0.2:
        effect_interpretation = "Малый"
    elif abs(effect_size) < 0.5:
        effect_interpretation = "Средний"
    else:
        effect_interpretation = "Большой"
    
    print(f"Интерпретация размера эффекта: {effect_interpretation}")
    
    return ab_data, results

# =============================================================================
# Главная функция для запуска всех примеров
# =============================================================================

def main():
    """Запуск всех примеров анализа данных и ML"""
    
    print("=== Анализ данных и машинное обучение ===\n")
    
    # 1. Pandas basics
    df_basic = pandas_basics_demo()
    
    # 2. Advanced pandas
    sales_df = advanced_pandas_operations()
    
    # 3. Data cleaning
    clean_df = data_cleaning_demo()
    
    # 4. EDA
    iris_df = exploratory_data_analysis()
    
    # 5. Classification ML
    classification_models, classification_results = machine_learning_classification()
    
    # 6. Regression ML
    regression_models, regression_results = machine_learning_regression()
    
    # 7. Hyperparameter optimization
    grid_search_result = hyperparameter_optimization()
    
    # 8. ML Pipeline
    pipeline = ml_pipeline_example()
    
    # 9. Time series analysis
    ts_data = time_series_analysis()
    
    # 10. A/B testing
    ab_data, ab_results = ab_testing_analysis()
    
    print("\n=== Сводка ===")
    print("✅ Pandas basics и advanced операции")
    print("✅ Очистка и preprocessing данных")
    print("✅ Исследовательский анализ данных (EDA)")
    print("✅ Машинное обучение: классификация и регрессия")
    print("✅ Оптимизация гиперпараметров")
    print("✅ ML Pipeline с preprocessing")
    print("✅ Анализ временных рядов")
    print("✅ A/B тестирование и статистический анализ")
    
    print("\nВсе примеры демонстрируют полный цикл работы с данными! 📊🤖")

if __name__ == "__main__":
    main() 