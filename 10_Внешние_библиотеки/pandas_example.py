# Пример использования библиотеки pandas
try:
    import pandas as pd
    
    # Создание DataFrame
    df = pd.DataFrame({
        'имя': ['Анна', 'Иван', 'Мария'],
        'возраст': [25, 30, 22],
        'зарплата': [50000, 60000, 45000]
    })
    
    print("DataFrame:")
    print(df)
    print(f"\nИнформация о данных:")
    print(df.info())
    print(f"\nСтатистика:")
    print(df.describe())
    
    # Операции с данными
    print(f"\nСредний возраст: {df['возраст'].mean()}")
    print(f"Максимальная зарплата: {df['зарплата'].max()}")
    
    # Фильтрация
    young = df[df['возраст'] < 30]
    print(f"\nМолодые сотрудники:\n{young}")
    
except ImportError:
    print("Библиотека pandas не установлена. Установите: pip install pandas") 