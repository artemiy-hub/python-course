# Основы анализа данных с Pandas
try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("pandas или numpy не установлены. Установите: pip install pandas numpy")
    exit()

import datetime
from io import StringIO

def demonstrate_series():
    """Демонстрация работы с Series"""
    print("=== Pandas Series ===")
    
    # Создание Series различными способами
    print("1. Создание Series:")
    
    # Из списка
    series_from_list = pd.Series([1, 2, 3, 4, 5])
    print(f"Из списка:\n{series_from_list}\n")
    
    # С индексами
    series_with_index = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
    print(f"С индексами:\n{series_with_index}\n")
    
    # Из словаря
    data_dict = {'Москва': 12500000, 'СПб': 5400000, 'Новосибирск': 1600000}
    series_from_dict = pd.Series(data_dict)
    print(f"Из словаря:\n{series_from_dict}\n")
    
    # Основные операции с Series
    print("2. Основные операции:")
    print(f"Размер: {series_from_dict.size}")
    print(f"Индекс: {series_from_dict.index.tolist()}")
    print(f"Значения: {series_from_dict.values}")
    print(f"Максимум: {series_from_dict.max()}")
    print(f"Сумма: {series_from_dict.sum()}")
    
    # Индексирование
    print("\n3. Индексирование:")
    print(f"По метке: {series_from_dict['Москва']}")
    print(f"По позиции: {series_from_dict.iloc[0]}")
    print(f"Несколько элементов: {series_from_dict[['Москва', 'СПб']].tolist()}")
    
    # Фильтрация
    print("\n4. Фильтрация:")
    large_cities = series_from_dict[series_from_dict > 2000000]
    print(f"Города с населением > 2 млн:\n{large_cities}")

def demonstrate_dataframe():
    """Демонстрация работы с DataFrame"""
    print("\n=== Pandas DataFrame ===")
    
    # Создание DataFrame
    print("1. Создание DataFrame:")
    
    # Из словаря
    data = {
        'Имя': ['Анна', 'Борис', 'Виктор', 'Галина', 'Дмитрий'],
        'Возраст': [25, 30, 35, 28, 32],
        'Город': ['Москва', 'СПб', 'Екатеринбург', 'Москва', 'Новосибирск'],
        'Зарплата': [80000, 90000, 70000, 85000, 75000]
    }
    
    df = pd.DataFrame(data)
    print(df)
    print(f"\nИнформация о DataFrame:\n{df.info()}")
    
    # Основные свойства
    print(f"\n2. Основные свойства:")
    print(f"Форма: {df.shape}")
    print(f"Размер: {df.size}")
    print(f"Столбцы: {df.columns.tolist()}")
    print(f"Типы данных:\n{df.dtypes}")
    
    # Статистика
    print(f"\n3. Описательная статистика:")
    print(df.describe())
    
    # Первые и последние строки
    print(f"\n4. Первые и последние строки:")
    print(f"Первые 3 строки:\n{df.head(3)}")
    print(f"\nПоследние 2 строки:\n{df.tail(2)}")

def demonstrate_indexing_and_selection():
    """Демонстрация индексирования и выбора данных"""
    print("\n=== Индексирование и выбор данных ===")
    
    # Создаём DataFrame для демонстрации
    data = {
        'Продукт': ['Хлеб', 'Молоко', 'Яйца', 'Масло', 'Сыр'],
        'Цена': [30, 60, 80, 120, 250],
        'Количество': [10, 15, 20, 5, 8],
        'Категория': ['Выпечка', 'Молочные', 'Молочные', 'Молочные', 'Молочные']
    }
    df = pd.DataFrame(data)
    print("Исходные данные:")
    print(df)
    
    # Выбор столбцов
    print("\n1. Выбор столбцов:")
    print(f"Один столбец:\n{df['Продукт']}")
    print(f"\nНесколько столбцов:\n{df[['Продукт', 'Цена']]}")
    
    # Выбор строк
    print("\n2. Выбор строк:")
    print(f"По индексу (iloc):\n{df.iloc[0]}")  # Первая строка
    print(f"\nНесколько строк:\n{df.iloc[1:3]}")  # Строки 1-2
    
    # Условная фильтрация
    print("\n3. Условная фильтрация:")
    expensive_products = df[df['Цена'] > 100]
    print(f"Дорогие продукты (цена > 100):\n{expensive_products}")
    
    # Множественные условия
    dairy_expensive = df[(df['Категория'] == 'Молочные') & (df['Цена'] > 80)]
    print(f"\nДорогие молочные продукты:\n{dairy_expensive}")
    
    # Выбор по метке (loc)
    print("\n4. Выбор по метке и условию:")
    print(f"Конкретные строки и столбцы:\n{df.loc[df['Цена'] > 100, ['Продукт', 'Цена']]}")

def demonstrate_data_operations():
    """Демонстрация операций с данными"""
    print("\n=== Операции с данными ===")
    
    # Создаём DataFrame продаж
    sales_data = {
        'Дата': pd.date_range('2023-01-01', periods=10, freq='D'),
        'Продукт': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
        'Количество': [10, 15, 12, 8, 20, 14, 6, 18, 16, 9],
        'Цена': [100, 150, 100, 200, 150, 100, 200, 150, 100, 200]
    }
    df = pd.DataFrame(sales_data)
    df['Сумма'] = df['Количество'] * df['Цена']  # Добавляем вычисляемый столбец
    
    print("Данные продаж:")
    print(df)
    
    # Группировка и агрегация
    print("\n1. Группировка по продуктам:")
    product_stats = df.groupby('Продукт').agg({
        'Количество': ['sum', 'mean'],
        'Сумма': ['sum', 'max']
    })
    print(product_stats)
    
    # Сводная таблица
    print("\n2. Сводная таблица:")
    pivot_table = df.pivot_table(
        values='Сумма',
        index='Продукт',
        aggfunc=['sum', 'count', 'mean']
    )
    print(pivot_table)
    
    # Сортировка
    print("\n3. Сортировка:")
    sorted_by_sum = df.sort_values('Сумма', ascending=False)
    print(f"Топ-3 продажи:\n{sorted_by_sum.head(3)}")

def demonstrate_data_cleaning():
    """Демонстрация очистки данных"""
    print("\n=== Очистка данных ===")
    
    # Создаём данные с проблемами
    dirty_data = {
        'Имя': ['Анна', 'Борис', None, 'Галина', 'Дмитрий', 'Анна'],  # Пропуск и дубликат
        'Возраст': [25, 30, 35, None, 32, 25],  # Пропущенное значение
        'Зарплата': ['80000', '90k', '70000', '85000', 'N/A', '80000'],  # Разные форматы
        'Email': ['anna@test.com', 'boris@test', 'viktor@test.com', 'galina@test.com', 'dmitry@test.com', 'anna@test.com']
    }
    
    df = pd.DataFrame(dirty_data)
    print("Исходные 'грязные' данные:")
    print(df)
    print(f"\nИнформация о пропущенных значениях:\n{df.isnull().sum()}")
    
    # Обработка пропущенных значений
    print("\n1. Обработка пропущенных значений:")
    
    # Удаление строк с пропусками
    df_no_na = df.dropna()
    print(f"После удаления строк с пропусками ({len(df_no_na)} строк):\n{df_no_na}")
    
    # Заполнение пропусков
    df_filled = df.copy()
    df_filled['Имя'].fillna('Неизвестно', inplace=True)
    df_filled['Возраст'].fillna(df_filled['Возраст'].mean(), inplace=True)
    print(f"\nПосле заполнения пропусков:\n{df_filled}")
    
    # Удаление дубликатов
    print("\n2. Удаление дубликатов:")
    df_no_duplicates = df_filled.drop_duplicates()
    print(f"После удаления дубликатов ({len(df_no_duplicates)} строк):\n{df_no_duplicates}")
    
    # Преобразование типов данных
    print("\n3. Преобразование типов данных:")
    df_clean = df_no_duplicates.copy()
    
    # Очистка зарплаты
    def clean_salary(salary):
        if isinstance(salary, str):
            if salary == 'N/A':
                return None
            if 'k' in salary:
                return float(salary.replace('k', '')) * 1000
            return float(salary)
        return salary
    
    df_clean['Зарплата'] = df_clean['Зарплата'].apply(clean_salary)
    df_clean['Зарплата'] = pd.to_numeric(df_clean['Зарплата'], errors='coerce')
    
    print(f"После очистки зарплаты:\n{df_clean}")
    print(f"\nТипы данных после очистки:\n{df_clean.dtypes}")

def demonstrate_file_operations():
    """Демонстрация работы с файлами"""
    print("\n=== Работа с файлами ===")
    
    # Создаём тестовые данные
    test_data = pd.DataFrame({
        'ID': range(1, 6),
        'Название': ['Товар A', 'Товар B', 'Товар C', 'Товар D', 'Товар E'],
        'Цена': [100, 200, 150, 300, 250],
        'В наличии': [True, False, True, True, False]
    })
    
    print("Тестовые данные для сохранения:")
    print(test_data)
    
    # Сохранение в CSV
    csv_file = 'test_data.csv'
    test_data.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"\nДанные сохранены в {csv_file}")
    
    # Чтение из CSV
    loaded_data = pd.read_csv(csv_file)
    print(f"Данные загружены из CSV:\n{loaded_data}")
    
    # Сохранение в Excel (требует openpyxl)
    try:
        excel_file = 'test_data.xlsx'
        test_data.to_excel(excel_file, index=False, sheet_name='Товары')
        print(f"Данные сохранены в {excel_file}")
        
        # Чтение из Excel
        loaded_excel = pd.read_excel(excel_file, sheet_name='Товары')
        print(f"Данные загружены из Excel:\n{loaded_excel}")
        
    except ImportError:
        print("openpyxl не установлен, пропускаем работу с Excel")
    
    # Работа с JSON
    json_file = 'test_data.json'
    test_data.to_json(json_file, orient='records', force_ascii=False, indent=2)
    print(f"Данные сохранены в {json_file}")
    
    loaded_json = pd.read_json(json_file)
    print(f"Данные загружены из JSON:\n{loaded_json}")

def demonstrate_time_series():
    """Демонстрация работы с временными рядами"""
    print("\n=== Временные ряды ===")
    
    # Создаём временной ряд
    dates = pd.date_range('2023-01-01', periods=30, freq='D')
    np.random.seed(42)
    values = np.random.randn(30).cumsum() + 100
    
    ts = pd.Series(values, index=dates)
    print("Временной ряд (первые 10 значений):")
    print(ts.head(10))
    
    # Операции с датами
    print(f"\n1. Операции с датами:")
    print(f"Начальная дата: {ts.index.min()}")
    print(f"Конечная дата: {ts.index.max()}")
    print(f"Количество дней: {len(ts)}")
    
    # Ресемплинг (изменение частоты)
    print(f"\n2. Недельные агрегаты:")
    weekly_mean = ts.resample('W').mean()
    print(weekly_mean)
    
    # Скользящее среднее
    print(f"\n3. Скользящее среднее (окно 7 дней):")
    rolling_mean = ts.rolling(window=7).mean()
    print(rolling_mean.tail(10))

def demonstrate_advanced_operations():
    """Демонстрация продвинутых операций"""
    print("\n=== Продвинутые операции ===")
    
    # Создаём два DataFrame для объединения
    df1 = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Имя': ['Анна', 'Борис', 'Виктор', 'Галина']
    })
    
    df2 = pd.DataFrame({
        'ID': [1, 2, 3, 5],
        'Зарплата': [80000, 90000, 70000, 85000]
    })
    
    print("DataFrame 1 (сотрудники):")
    print(df1)
    print("\nDataFrame 2 (зарплаты):")
    print(df2)
    
    # Inner join
    inner_join = pd.merge(df1, df2, on='ID', how='inner')
    print(f"\nInner join:\n{inner_join}")
    
    # Left join
    left_join = pd.merge(df1, df2, on='ID', how='left')
    print(f"\nLeft join:\n{left_join}")
    
    # Конкатенация
    df3 = pd.DataFrame({
        'ID': [6, 7],
        'Имя': ['Дмитрий', 'Елена']
    })
    
    concatenated = pd.concat([df1, df3], ignore_index=True)
    print(f"\nКонкатенация:\n{concatenated}")
    
    # Apply функция
    print(f"\n4. Применение функций:")
    df_with_salary = inner_join.copy()
    df_with_salary['Налог'] = df_with_salary['Зарплата'].apply(lambda x: x * 0.13)
    df_with_salary['Чистая зарплата'] = df_with_salary['Зарплата'] - df_with_salary['Налог']
    print(df_with_salary)

def cleanup_files():
    """Очистка созданных файлов"""
    import os
    files_to_remove = ['test_data.csv', 'test_data.xlsx', 'test_data.json']
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"Удален файл: {file}")

if __name__ == "__main__":
    try:
        print("Основы анализа данных с Pandas")
        print("=" * 50)
        
        demonstrate_series()
        demonstrate_dataframe()
        demonstrate_indexing_and_selection()
        demonstrate_data_operations()
        demonstrate_data_cleaning()
        demonstrate_file_operations()
        demonstrate_time_series()
        demonstrate_advanced_operations()
        
        print("\n=== Лучшие практики Pandas ===")
        best_practices = [
            "1. Используйте vectorized операции вместо циклов",
            "2. Устанавливайте правильные типы данных (dtypes)",
            "3. Используйте категориальные данные для строк с повторениями",
            "4. Избегайте chained assignment (df[col][row] = value)",
            "5. Используйте copy() при необходимости независимых копий",
            "6. Применяйте chunking для больших файлов",
            "7. Используйте query() для сложных фильтров",
            "8. Оптимизируйте память с помощью категорий и правильных типов"
        ]
        
        for practice in best_practices:
            print(f"   {practice}")
        
        print("\n=== Полезные методы Pandas ===")
        useful_methods = [
            "df.info() - информация о DataFrame",
            "df.describe() - описательная статистика", 
            "df.head()/tail() - первые/последние строки",
            "df.shape - размерность данных",
            "df.isnull().sum() - количество пропусков",
            "df.value_counts() - подсчёт уникальных значений",
            "df.groupby() - группировка данных",
            "df.pivot_table() - сводные таблицы",
            "df.merge() - объединение DataFrames",
            "df.apply() - применение функций"
        ]
        
        for method in useful_methods:
            print(f"   {method}")
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    finally:
        # Очистка файлов (раскомментируйте для удаления)
        # cleanup_files()
        print(f"\nФайлы примеров сохранены для изучения")
        print("Для очистки запустите функцию cleanup_files()") 