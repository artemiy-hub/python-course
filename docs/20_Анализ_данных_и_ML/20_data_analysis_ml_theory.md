# Теория: Анализ данных и машинное обучение в Python

## 🎯 Цель раздела

Этот раздел охватывает все аспекты анализа данных и машинного обучения в Python: от базовой работы с Pandas до создания и развертывания ML моделей.

## 📋 Содержание

1. [Pandas - анализ данных](#pandas---анализ-данных)
2. [NumPy - численные вычисления](#numpy---численные-вычисления)
3. [Визуализация данных](#визуализация-данных)
4. [Статистический анализ](#статистический-анализ)
5. [Машинное обучение с Scikit-learn](#машинное-обучение-с-scikit-learn)
6. [Deep Learning основы](#deep-learning-основы)
7. [MLOps и продакшн](#mlops-и-продакшн)

---

## 🐼 Pandas - анализ данных

Pandas - основная библиотека для анализа и обработки данных в Python.

### Основы работы с DataFrame

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union, Tuple
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    """Класс для анализа данных с расширенными возможностями"""
    
    def __init__(self, data: Union[str, pd.DataFrame, Dict] = None):
        """
        Инициализация анализатора данных
        
        Args:
            data: Путь к файлу, DataFrame или словарь с данными
        """
        self.df = None
        self.metadata = {}
        
        if data is not None:
            self.load_data(data)
    
    def load_data(self, data: Union[str, pd.DataFrame, Dict]):
        """Загрузка данных из различных источников"""
        
        if isinstance(data, str):
            # Загрузка из файла
            if data.endswith('.csv'):
                self.df = pd.read_csv(data)
            elif data.endswith('.xlsx') or data.endswith('.xls'):
                self.df = pd.read_excel(data)
            elif data.endswith('.json'):
                self.df = pd.read_json(data)
            elif data.endswith('.parquet'):
                self.df = pd.read_parquet(data)
            else:
                raise ValueError(f"Неподдерживаемый формат файла: {data}")
                
        elif isinstance(data, pd.DataFrame):
            self.df = data.copy()
            
        elif isinstance(data, dict):
            self.df = pd.DataFrame(data)
            
        else:
            raise TypeError("Данные должны быть путем к файлу, DataFrame или словарем")
        
        self._update_metadata()
        print(f"✅ Данные загружены: {self.df.shape[0]} строк, {self.df.shape[1]} столбцов")
    
    def _update_metadata(self):
        """Обновление метаданных датасета"""
        if self.df is not None:
            self.metadata = {
                'shape': self.df.shape,
                'columns': list(self.df.columns),
                'dtypes': dict(self.df.dtypes),
                'memory_usage': self.df.memory_usage(deep=True).sum(),
                'missing_values': dict(self.df.isnull().sum()),
                'created_at': datetime.now()
            }
    
    def basic_info(self) -> Dict[str, Any]:
        """Базовая информация о датасете"""
        if self.df is None:
            return {}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns
        
        return {
            'basic_stats': {
                'rows': len(self.df),
                'columns': len(self.df.columns),
                'memory_usage_mb': self.df.memory_usage(deep=True).sum() / (1024 * 1024),
                'missing_values_total': self.df.isnull().sum().sum(),
                'missing_percentage': (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
            },
            'column_types': {
                'numeric': len(numeric_cols),
                'categorical': len(categorical_cols),
                'datetime': len(datetime_cols)
            },
            'data_quality': {
                'duplicated_rows': self.df.duplicated().sum(),
                'unique_rows': len(self.df.drop_duplicates()),
                'columns_with_nulls': (self.df.isnull().sum() > 0).sum()
            }
        }
    
    def describe_data(self, include_all: bool = True) -> pd.DataFrame:
        """Расширенное описание данных"""
        if self.df is None:
            return pd.DataFrame()
        
        if include_all:
            return self.df.describe(include='all')
        else:
            return self.df.describe()
    
    def missing_values_analysis(self) -> Dict[str, Any]:
        """Анализ пропущенных значений"""
        if self.df is None:
            return {}
        
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'column': missing.index,
            'missing_count': missing.values,
            'missing_percentage': missing_percent.values
        }).sort_values('missing_percentage', ascending=False)
        
        # Паттерны пропущенных значений
        patterns = {}
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                pattern = self.df[col].isnull().value_counts()
                patterns[col] = {
                    'has_missing': pattern.get(True, 0),
                    'no_missing': pattern.get(False, 0)
                }
        
        return {
            'summary': missing_df,
            'patterns': patterns,
            'recommendations': self._get_missing_value_recommendations(missing_df)
        }
    
    def _get_missing_value_recommendations(self, missing_df: pd.DataFrame) -> List[str]:
        """Рекомендации по обработке пропущенных значений"""
        recommendations = []
        
        for _, row in missing_df.iterrows():
            col, missing_count, missing_pct = row['column'], row['missing_count'], row['missing_percentage']
            
            if missing_pct == 0:
                continue
            elif missing_pct < 5:
                recommendations.append(f"{col}: Мало пропусков ({missing_pct:.1f}%), можно удалить строки или заполнить")
            elif missing_pct < 30:
                recommendations.append(f"{col}: Умеренные пропуски ({missing_pct:.1f}%), рекомендуется импутация")
            elif missing_pct < 70:
                recommendations.append(f"{col}: Много пропусков ({missing_pct:.1f}%), рассмотрите удаление столбца")
            else:
                recommendations.append(f"{col}: Критично много пропусков ({missing_pct:.1f}%), рекомендуется удалить")
        
        return recommendations
    
    def outliers_analysis(self, method: str = 'iqr') -> Dict[str, Any]:
        """Анализ выбросов"""
        if self.df is None:
            return {}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers_info = {}
        
        for col in numeric_cols:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                
            elif method == 'zscore':
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                outliers = self.df[z_scores > 3]
            
            outliers_info[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(self.df)) * 100,
                'values': outliers[col].tolist() if len(outliers) < 20 else outliers[col].head(20).tolist()
            }
        
        return outliers_info
    
    def correlation_analysis(self, method: str = 'pearson') -> Dict[str, Any]:
        """Анализ корреляций"""
        if self.df is None:
            return {}
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return {'error': 'Недостаточно числовых столбцов для анализа корреляции'}
        
        correlation_matrix = numeric_df.corr(method=method)
        
        # Найдем сильные корреляции
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:  # Сильная корреляция
                    strong_correlations.append({
                        'feature1': correlation_matrix.columns[i],
                        'feature2': correlation_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        return {
            'matrix': correlation_matrix,
            'strong_correlations': strong_correlations,
            'summary': f"Найдено {len(strong_correlations)} сильных корреляций (|r| > 0.7)"
        }
    
    def categorical_analysis(self) -> Dict[str, Any]:
        """Анализ категориальных переменных"""
        if self.df is None:
            return {}
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        analysis = {}
        
        for col in categorical_cols:
            value_counts = self.df[col].value_counts()
            
            analysis[col] = {
                'unique_values': self.df[col].nunique(),
                'most_frequent': value_counts.index[0] if len(value_counts) > 0 else None,
                'most_frequent_count': value_counts.iloc[0] if len(value_counts) > 0 else 0,
                'distribution': value_counts.head(10).to_dict(),  # Топ-10
                'cardinality': self._assess_cardinality(self.df[col].nunique(), len(self.df))
            }
        
        return analysis
    
    def _assess_cardinality(self, unique_count: int, total_count: int) -> str:
        """Оценка кардинальности категориальной переменной"""
        ratio = unique_count / total_count
        
        if ratio < 0.05:
            return "Низкая кардинальность"
        elif ratio < 0.5:
            return "Средняя кардинальность"
        else:
            return "Высокая кардинальность"
    
    def time_series_analysis(self, date_column: str, value_column: str) -> Dict[str, Any]:
        """Анализ временных рядов"""
        if self.df is None or date_column not in self.df.columns or value_column not in self.df.columns:
            return {}
        
        # Преобразуем в datetime если нужно
        if not pd.api.types.is_datetime64_any_dtype(self.df[date_column]):
            self.df[date_column] = pd.to_datetime(self.df[date_column])
        
        # Сортируем по дате
        ts_df = self.df.sort_values(date_column)
        
        # Базовая статистика
        date_range = ts_df[date_column].max() - ts_df[date_column].min()
        frequency = self._detect_frequency(ts_df[date_column])
        
        # Тренд анализ (простая линейная регрессия)
        from scipy import stats
        x = np.arange(len(ts_df))
        y = ts_df[value_column].values
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Сезонность (упрощенная проверка)
        seasonality = self._detect_seasonality(ts_df, date_column, value_column)
        
        return {
            'basic_stats': {
                'start_date': ts_df[date_column].min(),
                'end_date': ts_df[date_column].max(),
                'date_range': str(date_range),
                'data_points': len(ts_df),
                'frequency': frequency
            },
            'trend': {
                'slope': slope,
                'r_squared': r_value**2,
                'p_value': p_value,
                'trend_direction': 'возрастающий' if slope > 0 else 'убывающий' if slope < 0 else 'стабильный'
            },
            'seasonality': seasonality,
            'missing_dates': self._find_missing_dates(ts_df, date_column, frequency)
        }
    
    def _detect_frequency(self, date_series: pd.Series) -> str:
        """Определение частоты временного ряда"""
        if len(date_series) < 2:
            return "unknown"
        
        diffs = date_series.diff().dropna()
        mode_diff = diffs.mode().iloc[0] if len(diffs.mode()) > 0 else diffs.median()
        
        if mode_diff <= timedelta(days=1):
            return "daily"
        elif mode_diff <= timedelta(days=7):
            return "weekly"
        elif mode_diff <= timedelta(days=31):
            return "monthly"
        else:
            return "irregular"
    
    def _detect_seasonality(self, df: pd.DataFrame, date_col: str, value_col: str) -> Dict[str, Any]:
        """Простое определение сезонности"""
        # Добавляем временные признаки
        df_temp = df.copy()
        df_temp['month'] = df_temp[date_col].dt.month
        df_temp['day_of_week'] = df_temp[date_col].dt.dayofweek
        df_temp['quarter'] = df_temp[date_col].dt.quarter
        
        # Анализируем вариацию по месяцам
        monthly_stats = df_temp.groupby('month')[value_col].agg(['mean', 'std']).reset_index()
        monthly_cv = (monthly_stats['std'] / monthly_stats['mean']).mean()
        
        # Анализируем вариацию по дням недели
        weekly_stats = df_temp.groupby('day_of_week')[value_col].agg(['mean', 'std']).reset_index()
        weekly_cv = (weekly_stats['std'] / weekly_stats['mean']).mean()
        
        return {
            'monthly_seasonality': monthly_cv > 0.1,
            'weekly_seasonality': weekly_cv > 0.1,
            'monthly_variation': monthly_cv,
            'weekly_variation': weekly_cv
        }
    
    def _find_missing_dates(self, df: pd.DataFrame, date_col: str, frequency: str) -> List[str]:
        """Поиск пропущенных дат"""
        if frequency == "daily":
            full_range = pd.date_range(start=df[date_col].min(), end=df[date_col].max(), freq='D')
        elif frequency == "weekly":
            full_range = pd.date_range(start=df[date_col].min(), end=df[date_col].max(), freq='W')
        elif frequency == "monthly":
            full_range = pd.date_range(start=df[date_col].min(), end=df[date_col].max(), freq='MS')
        else:
            return []
        
        existing_dates = set(df[date_col].dt.date)
        full_dates = set(full_range.date)
        missing_dates = full_dates - existing_dates
        
        return [str(date) for date in sorted(missing_dates)]

# Продвинутая обработка данных
class AdvancedDataProcessor:
    """Продвинутая обработка данных"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.transformations_log = []
    
    def handle_missing_values(self, strategy: Dict[str, str]) -> pd.DataFrame:
        """
        Обработка пропущенных значений
        
        Args:
            strategy: Словарь {column: method} где method может быть:
                     'drop', 'mean', 'median', 'mode', 'forward_fill', 'backward_fill', 'constant'
        """
        df_processed = self.df.copy()
        
        for column, method in strategy.items():
            if column not in df_processed.columns:
                continue
                
            if method == 'drop':
                df_processed = df_processed.dropna(subset=[column])
                
            elif method == 'mean' and pd.api.types.is_numeric_dtype(df_processed[column]):
                df_processed[column] = df_processed[column].fillna(df_processed[column].mean())
                
            elif method == 'median' and pd.api.types.is_numeric_dtype(df_processed[column]):
                df_processed[column] = df_processed[column].fillna(df_processed[column].median())
                
            elif method == 'mode':
                mode_value = df_processed[column].mode().iloc[0] if len(df_processed[column].mode()) > 0 else 0
                df_processed[column] = df_processed[column].fillna(mode_value)
                
            elif method == 'forward_fill':
                df_processed[column] = df_processed[column].fillna(method='ffill')
                
            elif method == 'backward_fill':
                df_processed[column] = df_processed[column].fillna(method='bfill')
                
            elif method.startswith('constant_'):
                constant_value = method.split('_', 1)[1]
                df_processed[column] = df_processed[column].fillna(constant_value)
            
            self.transformations_log.append(f"Missing values in {column} handled with {method}")
        
        return df_processed
    
    def handle_outliers(self, columns: List[str], method: str = 'iqr', action: str = 'remove') -> pd.DataFrame:
        """
        Обработка выбросов
        
        Args:
            columns: Список столбцов для обработки
            method: 'iqr' или 'zscore'
            action: 'remove', 'cap', 'transform'
        """
        df_processed = self.df.copy()
        
        for column in columns:
            if column not in df_processed.columns or not pd.api.types.is_numeric_dtype(df_processed[column]):
                continue
            
            if method == 'iqr':
                Q1 = df_processed[column].quantile(0.25)
                Q3 = df_processed[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                if action == 'remove':
                    df_processed = df_processed[
                        (df_processed[column] >= lower_bound) & 
                        (df_processed[column] <= upper_bound)
                    ]
                elif action == 'cap':
                    df_processed[column] = np.clip(df_processed[column], lower_bound, upper_bound)
                elif action == 'transform':
                    # Логарифмическое преобразование для положительных значений
                    if (df_processed[column] > 0).all():
                        df_processed[column] = np.log1p(df_processed[column])
            
            elif method == 'zscore':
                z_scores = np.abs((df_processed[column] - df_processed[column].mean()) / df_processed[column].std())
                
                if action == 'remove':
                    df_processed = df_processed[z_scores <= 3]
                elif action == 'cap':
                    mean_val = df_processed[column].mean()
                    std_val = df_processed[column].std()
                    lower_bound = mean_val - 3 * std_val
                    upper_bound = mean_val + 3 * std_val
                    df_processed[column] = np.clip(df_processed[column], lower_bound, upper_bound)
            
            self.transformations_log.append(f"Outliers in {column} handled with {method}-{action}")
        
        return df_processed
    
    def encode_categorical(self, columns: List[str], method: str = 'onehot') -> pd.DataFrame:
        """
        Кодирование категориальных переменных
        
        Args:
            columns: Список столбцов для кодирования
            method: 'onehot', 'label', 'target'
        """
        df_processed = self.df.copy()
        
        for column in columns:
            if column not in df_processed.columns:
                continue
            
            if method == 'onehot':
                # One-hot encoding
                dummies = pd.get_dummies(df_processed[column], prefix=column)
                df_processed = pd.concat([df_processed.drop(column, axis=1), dummies], axis=1)
                
            elif method == 'label':
                # Label encoding
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                df_processed[column] = le.fit_transform(df_processed[column].astype(str))
                
            self.transformations_log.append(f"Categorical encoding for {column} with {method}")
        
        return df_processed
    
    def scale_features(self, columns: List[str], method: str = 'standard') -> pd.DataFrame:
        """
        Масштабирование признаков
        
        Args:
            columns: Список столбцов для масштабирования
            method: 'standard', 'minmax', 'robust'
        """
        df_processed = self.df.copy()
        
        for column in columns:
            if column not in df_processed.columns or not pd.api.types.is_numeric_dtype(df_processed[column]):
                continue
            
            if method == 'standard':
                # Стандартизация (z-score)
                df_processed[column] = (df_processed[column] - df_processed[column].mean()) / df_processed[column].std()
                
            elif method == 'minmax':
                # Нормализация min-max
                min_val = df_processed[column].min()
                max_val = df_processed[column].max()
                df_processed[column] = (df_processed[column] - min_val) / (max_val - min_val)
                
            elif method == 'robust':
                # Робастное масштабирование
                median = df_processed[column].median()
                q75 = df_processed[column].quantile(0.75)
                q25 = df_processed[column].quantile(0.25)
                iqr = q75 - q25
                df_processed[column] = (df_processed[column] - median) / iqr
            
            self.transformations_log.append(f"Feature scaling for {column} with {method}")
        
        return df_processed
    
    def create_features(self, feature_config: Dict[str, Any]) -> pd.DataFrame:
        """
        Создание новых признаков
        
        Args:
            feature_config: Конфигурация для создания признаков
        """
        df_processed = self.df.copy()
        
        for feature_name, config in feature_config.items():
            feature_type = config.get('type')
            
            if feature_type == 'polynomial':
                # Полиномиальные признаки
                column = config['column']
                degree = config.get('degree', 2)
                if column in df_processed.columns:
                    df_processed[feature_name] = df_processed[column] ** degree
            
            elif feature_type == 'interaction':
                # Взаимодействие признаков
                columns = config['columns']
                if all(col in df_processed.columns for col in columns):
                    df_processed[feature_name] = df_processed[columns].prod(axis=1)
            
            elif feature_type == 'binning':
                # Биннинг
                column = config['column']
                bins = config.get('bins', 5)
                if column in df_processed.columns:
                    df_processed[feature_name] = pd.cut(df_processed[column], bins=bins, labels=False)
            
            elif feature_type == 'datetime':
                # Временные признаки
                column = config['column']
                if column in df_processed.columns:
                    df_processed[column] = pd.to_datetime(df_processed[column])
                    
                    if 'year' in config.get('extract', []):
                        df_processed[f"{feature_name}_year"] = df_processed[column].dt.year
                    if 'month' in config.get('extract', []):
                        df_processed[f"{feature_name}_month"] = df_processed[column].dt.month
                    if 'day' in config.get('extract', []):
                        df_processed[f"{feature_name}_day"] = df_processed[column].dt.day
                    if 'dayofweek' in config.get('extract', []):
                        df_processed[f"{feature_name}_dayofweek"] = df_processed[column].dt.dayofweek
            
            self.transformations_log.append(f"Feature {feature_name} created with type {feature_type}")
        
        return df_processed
    
    def get_transformation_summary(self) -> List[str]:
        """Получение сводки примененных преобразований"""
        return self.transformations_log.copy()

# Интеграция с базами данных
class DataBaseConnector:
    """Коннектор для работы с базами данных"""
    
    def __init__(self, connection_string: str):
        """
        Args:
            connection_string: Строка подключения к БД
        """
        self.connection_string = connection_string
        self.engine = None
        self._connect()
    
    def _connect(self):
        """Установка соединения с базой данных"""
        try:
            from sqlalchemy import create_engine
            self.engine = create_engine(self.connection_string)
            print("✅ Соединение с базой данных установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения к БД: {e}")
    
    def read_table(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """Чтение таблицы из базы данных"""
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            print(f"❌ Ошибка чтения таблицы {table_name}: {e}")
            return pd.DataFrame()
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Выполнение произвольного SQL запроса"""
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            print(f"❌ Ошибка выполнения запроса: {e}")
            return pd.DataFrame()
    
    def write_table(self, df: pd.DataFrame, table_name: str, 
                   if_exists: str = 'replace', index: bool = False) -> bool:
        """Запись DataFrame в базу данных"""
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=index)
            print(f"✅ Данные записаны в таблицу {table_name}")
            return True
        except Exception as e:
            print(f"❌ Ошибка записи в таблицу {table_name}: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Получение информации о таблице"""
        try:
            # Получаем схему таблицы
            columns_query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            """
            columns_info = pd.read_sql(columns_query, self.engine)
            
            # Получаем количество строк
            count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"
            row_count = pd.read_sql(count_query, self.engine)['row_count'].iloc[0]
            
            return {
                'columns': columns_info.to_dict('records'),
                'row_count': row_count,
                'table_name': table_name
            }
        except Exception as e:
            print(f"❌ Ошибка получения информации о таблице: {e}")
            return {}

# Пример создания полного пайплайна анализа данных
class DataAnalysisPipeline:
    """Полный пайплайн анализа данных"""
    
    def __init__(self, data_source: Union[str, pd.DataFrame]):
        self.analyzer = DataAnalyzer(data_source)
        self.processor = AdvancedDataProcessor(self.analyzer.df)
        self.results = {}
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """Запуск полного анализа данных"""
        print("🔍 Запуск полного анализа данных...")
        
        # Базовая информация
        self.results['basic_info'] = self.analyzer.basic_info()
        print("✅ Базовая информация собрана")
        
        # Анализ пропущенных значений
        self.results['missing_values'] = self.analyzer.missing_values_analysis()
        print("✅ Анализ пропущенных значений завершен")
        
        # Анализ выбросов
        self.results['outliers'] = self.analyzer.outliers_analysis()
        print("✅ Анализ выбросов завершен")
        
        # Корреляционный анализ
        self.results['correlations'] = self.analyzer.correlation_analysis()
        print("✅ Корреляционный анализ завершен")
        
        # Анализ категориальных переменных
        self.results['categorical'] = self.analyzer.categorical_analysis()
        print("✅ Анализ категориальных переменных завершен")
        
        print("🎉 Полный анализ данных завершен!")
        return self.results
    
    def generate_report(self) -> str:
        """Генерация текстового отчета"""
        if not self.results:
            return "Анализ не был выполнен. Запустите run_full_analysis() сначала."
        
        report = []
        report.append("📊 ОТЧЕТ ПО АНАЛИЗУ ДАННЫХ")
        report.append("=" * 50)
        
        # Базовая информация
        basic = self.results.get('basic_info', {})
        if basic:
            stats = basic.get('basic_stats', {})
            report.append(f"\n📋 Основная информация:")
            report.append(f"  • Строки: {stats.get('rows', 'N/A'):,}")
            report.append(f"  • Столбцы: {stats.get('columns', 'N/A')}")
            report.append(f"  • Размер в памяти: {stats.get('memory_usage_mb', 0):.1f} MB")
            report.append(f"  • Пропущенные значения: {stats.get('missing_values_total', 0):,}")
            report.append(f"  • Дублированные строки: {basic.get('data_quality', {}).get('duplicated_rows', 0):,}")
        
        # Пропущенные значения
        missing = self.results.get('missing_values', {})
        if missing and 'recommendations' in missing:
            report.append(f"\n🔍 Рекомендации по пропущенным значениям:")
            for rec in missing['recommendations'][:5]:  # Топ-5 рекомендаций
                report.append(f"  • {rec}")
        
        # Корреляции
        corr = self.results.get('correlations', {})
        if corr and 'strong_correlations' in corr:
            strong_corr = corr['strong_correlations']
            if strong_corr:
                report.append(f"\n🔗 Сильные корреляции (|r| > 0.7):")
                for item in strong_corr[:5]:  # Топ-5 корреляций
                    report.append(f"  • {item['feature1']} ↔ {item['feature2']}: {item['correlation']:.3f}")
        
        # Категориальные переменные
        cat = self.results.get('categorical', {})
        if cat:
            report.append(f"\n📊 Категориальные переменные:")
            for col, info in list(cat.items())[:5]:  # Топ-5 столбцов
                report.append(f"  • {col}: {info['unique_values']} уникальных значений ({info['cardinality']})")
        
        return "\n".join(report)

# Практический пример использования
def create_sample_dataset():
    """Создание примера датасета для демонстрации"""
    np.random.seed(42)
    n_samples = 1000
    
    # Создаем синтетические данные
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.normal(35, 12, n_samples).astype(int),
        'income': np.random.exponential(50000, n_samples),
        'spending_score': np.random.beta(2, 5, n_samples) * 100,
        'city': np.random.choice(['Москва', 'СПб', 'Екатеринбург', 'Казань', 'Новосибирск'], n_samples),
        'gender': np.random.choice(['М', 'Ж'], n_samples),
        'purchase_date': pd.date_range('2023-01-01', periods=n_samples, freq='H'),
        'category': np.random.choice(['Электроника', 'Одежда', 'Еда', 'Книги', 'Спорт'], n_samples)
    }
    
    # Добавляем некоторые пропущенные значения
    df = pd.DataFrame(data)
    df.loc[np.random.choice(df.index, 50), 'income'] = np.nan
    df.loc[np.random.choice(df.index, 30), 'city'] = np.nan
    
    # Добавляем несколько выбросов
    df.loc[np.random.choice(df.index, 10), 'income'] = df['income'].max() * 3
    
    return df

def demonstrate_analysis_pipeline():
    """Демонстрация полного пайплайна анализа"""
    # Создаем пример данных
    df = create_sample_dataset()
    
    # Запускаем анализ
    pipeline = DataAnalysisPipeline(df)
    results = pipeline.run_full_analysis()
    
    # Генерируем отчет
    report = pipeline.generate_report()
    print("\n" + report)
    
    return pipeline, results
```

---

## 🔢 NumPy - численные вычисления

NumPy - основа для численных вычислений и многомерных массивов в Python.

### Продвинутые операции с массивами

```python
import numpy as np
from typing import Tuple, List, Union, Optional, Callable
import time
from scipy import linalg, sparse
from numba import jit, vectorize
import matplotlib.pyplot as plt

class AdvancedNumPyOperations:
    """Продвинутые операции с NumPy"""
    
    @staticmethod
    def create_structured_arrays():
        """Создание структурированных массивов"""
        # Определяем тип данных
        dtype = np.dtype([
            ('name', 'U20'),
            ('age', 'i4'),
            ('height', 'f4'),
            ('weight', 'f4'),
            ('salary', 'f8')
        ])
        
        # Создаем структурированный массив
        people = np.array([
            ('Alice', 25, 165.5, 55.2, 50000.0),
            ('Bob', 30, 180.0, 75.8, 60000.0),
            ('Charlie', 35, 175.2, 70.1, 75000.0)
        ], dtype=dtype)
        
        return people
    
    @staticmethod
    def memory_optimization_example():
        """Пример оптимизации памяти"""
        # Сравнение использования памяти разных типов данных
        sizes = [1000000]
        
        results = {}
        for size in sizes:
            # float64 (по умолчанию)
            arr_64 = np.random.random(size).astype(np.float64)
            memory_64 = arr_64.nbytes / (1024 * 1024)  # МБ
            
            # float32
            arr_32 = arr_64.astype(np.float32)
            memory_32 = arr_32.nbytes / (1024 * 1024)
            
            # int16 для целых чисел в диапазоне -32768..32767
            if np.all(arr_64.astype(int) == arr_64) and np.all(arr_64 >= -32768) and np.all(arr_64 <= 32767):
                arr_16 = arr_64.astype(np.int16)
                memory_16 = arr_16.nbytes / (1024 * 1024)
            else:
                memory_16 = None
            
            results[size] = {
                'float64': memory_64,
                'float32': memory_32,
                'int16': memory_16,
                'savings_32': (memory_64 - memory_32) / memory_64 * 100
            }
        
        return results
    
    @staticmethod
    def vectorization_examples():
        """Примеры векторизации вычислений"""
        
        # Создаем тестовые данные
        size = 1000000
        x = np.random.random(size)
        y = np.random.random(size)
        
        # Пример 1: Медленный способ (циклы Python)
        def slow_calculation(x, y):
            result = np.zeros_like(x)
            for i in range(len(x)):
                result[i] = np.sqrt(x[i]**2 + y[i]**2) * np.sin(x[i]) + np.cos(y[i])
            return result
        
        # Пример 2: Векторизованный способ
        def fast_calculation(x, y):
            return np.sqrt(x**2 + y**2) * np.sin(x) + np.cos(y)
        
        # Пример 3: Ufunc с декоратором
        @vectorize(['float64(float64, float64)'], target='cpu')
        def numba_calculation(x, y):
            return np.sqrt(x**2 + y**2) * np.sin(x) + np.cos(y)
        
        # Замеры времени
        times = {}
        
        # Векторизованный способ
        start = time.time()
        result_fast = fast_calculation(x, y)
        times['vectorized'] = time.time() - start
        
        # Numba ufunc
        start = time.time()
        result_numba = numba_calculation(x, y)
        times['numba'] = time.time() - start
        
        # Медленный способ (только для небольшого размера)
        if size <= 10000:
            start = time.time()
            result_slow = slow_calculation(x[:10000], y[:10000])
            times['loops'] = time.time() - start
        
        return {
            'times': times,
            'speedup': times.get('loops', times['vectorized']) / times['vectorized'] if 'loops' in times else times['numba'] / times['vectorized']
        }
    
    @staticmethod
    def advanced_indexing_examples():
        """Продвинутые примеры индексирования"""
        # Создаем 3D массив
        arr_3d = np.random.randint(0, 100, (5, 6, 7))
        
        examples = {}
        
        # Fancy indexing
        examples['fancy_indexing'] = {
            'description': 'Выбор конкретных элементов по индексам',
            'code': 'arr[[0, 2, 4], [1, 3, 5]]',
            'result': arr_3d[[0, 2, 4], [1, 3, 5]].shape
        }
        
        # Boolean indexing
        mask = arr_3d > 50
        examples['boolean_indexing'] = {
            'description': 'Выбор элементов по условию',
            'code': 'arr[arr > 50]',
            'count': np.sum(mask)
        }
        
        # Mesh grid indexing
        x_idx, y_idx = np.meshgrid([0, 2, 4], [1, 3, 5])
        examples['meshgrid_indexing'] = {
            'description': 'Выбор блоков с помощью meshgrid',
            'shape': arr_3d[x_idx, y_idx].shape
        }
        
        # Advanced slicing
        examples['advanced_slicing'] = {
            'description': 'Сложные срезы',
            'every_other': arr_3d[::2, ::2, ::2].shape,
            'reverse': arr_3d[::-1, ::-1, ::-1].shape
        }
        
        return examples
    
    @staticmethod
    def broadcasting_examples():
        """Примеры broadcasting"""
        examples = {}
        
        # Базовый broadcasting
        a = np.array([[1, 2, 3],
                     [4, 5, 6]])  # (2, 3)
        b = np.array([10, 20, 30])  # (3,)
        
        examples['basic'] = {
            'a_shape': a.shape,
            'b_shape': b.shape,
            'result_shape': (a + b).shape,
            'result': a + b
        }
        
        # Сложный broadcasting
        c = np.random.random((5, 1, 3))  # (5, 1, 3)
        d = np.random.random((1, 4, 1))  # (1, 4, 1)
        
        examples['complex'] = {
            'c_shape': c.shape,
            'd_shape': d.shape,
            'result_shape': (c + d).shape
        }
        
        # Ошибки broadcasting
        try:
            e = np.random.random((3, 2))
            f = np.random.random((4, 2))
            result = e + f  # Должно вызвать ошибку
        except ValueError as error:
            examples['error'] = {
                'error_message': str(error),
                'incompatible_shapes': (e.shape, f.shape)
            }
        
        return examples

class LinearAlgebraOperations:
    """Операции линейной алгебры"""
    
    @staticmethod
    def matrix_operations_comparison():
        """Сравнение различных способов матричных операций"""
        size = 1000
        A = np.random.random((size, size))
        B = np.random.random((size, size))
        
        operations = {}
        
        # Умножение матриц
        start = time.time()
        C1 = np.dot(A, B)
        operations['np.dot'] = time.time() - start
        
        start = time.time()
        C2 = A @ B
        operations['@ operator'] = time.time() - start
        
        start = time.time()
        C3 = np.matmul(A, B)
        operations['np.matmul'] = time.time() - start
        
        # Проверяем, что результаты одинаковые
        operations['results_equal'] = np.allclose(C1, C2) and np.allclose(C2, C3)
        
        return operations
    
    @staticmethod
    def solve_linear_systems():
        """Решение систем линейных уравнений"""
        # Создаем систему Ax = b
        n = 100
        A = np.random.random((n, n))
        true_x = np.random.random(n)
        b = A @ true_x
        
        solutions = {}
        
        # Метод 1: np.linalg.solve
        start = time.time()
        x1 = np.linalg.solve(A, b)
        solutions['linalg.solve'] = {
            'time': time.time() - start,
            'error': np.linalg.norm(x1 - true_x)
        }
        
        # Метод 2: scipy.linalg.solve (часто быстрее)
        start = time.time()
        x2 = linalg.solve(A, b)
        solutions['scipy.solve'] = {
            'time': time.time() - start,
            'error': np.linalg.norm(x2 - true_x)
        }
        
        # Метод 3: псевдообратная матрица (для плохо обусловленных матриц)
        start = time.time()
        x3 = np.linalg.pinv(A) @ b
        solutions['pinv'] = {
            'time': time.time() - start,
            'error': np.linalg.norm(x3 - true_x)
        }
        
        return solutions
    
    @staticmethod
    def eigenvalue_analysis():
        """Анализ собственных значений и векторов"""
        # Создаем симметричную матрицу
        n = 100
        A = np.random.random((n, n))
        A = (A + A.T) / 2  # Делаем симметричной
        
        # Находим собственные значения и векторы
        eigenvalues, eigenvectors = np.linalg.eigh(A)  # для симметричных матриц
        
        analysis = {
            'max_eigenvalue': np.max(eigenvalues),
            'min_eigenvalue': np.min(eigenvalues),
            'condition_number': np.max(eigenvalues) / np.min(eigenvalues),
            'trace': np.trace(A),
            'sum_eigenvalues': np.sum(eigenvalues),
            'determinant': np.linalg.det(A),
            'product_eigenvalues': np.prod(eigenvalues)
        }
        
        # Проверяем ортогональность собственных векторов
        dot_product = eigenvectors.T @ eigenvectors
        is_orthogonal = np.allclose(dot_product, np.eye(n))
        analysis['eigenvectors_orthogonal'] = is_orthogonal
        
        return analysis
    
    @staticmethod
    def svd_analysis():
        """Анализ сингулярного разложения"""
        # Создаем матрицу для анализа
        m, n = 200, 150
        A = np.random.random((m, n))
        
        # SVD разложение
        U, s, Vt = np.linalg.svd(A, full_matrices=False)
        
        analysis = {
            'original_shape': A.shape,
            'U_shape': U.shape,
            'singular_values_shape': s.shape,
            'Vt_shape': Vt.shape,
            'rank': np.sum(s > 1e-10),
            'condition_number': s[0] / s[-1] if s[-1] > 1e-15 else np.inf,
            'frobenius_norm': np.linalg.norm(A, 'fro'),
            'nuclear_norm': np.sum(s)
        }
        
        # Аппроксимация низкого ранга
        ranks = [10, 30, 50, 100]
        approximations = {}
        
        for rank in ranks:
            if rank < len(s):
                A_approx = U[:, :rank] @ np.diag(s[:rank]) @ Vt[:rank, :]
                error = np.linalg.norm(A - A_approx, 'fro')
                compression_ratio = (rank * (m + n)) / (m * n)
                
                approximations[rank] = {
                    'error': error,
                    'relative_error': error / np.linalg.norm(A, 'fro'),
                    'compression_ratio': compression_ratio
                }
        
        analysis['low_rank_approximations'] = approximations
        
        return analysis

class PerformanceOptimization:
    """Оптимизация производительности NumPy"""
    
    @staticmethod
    def memory_layout_optimization():
        """Оптимизация расположения данных в памяти"""
        size = (1000, 1000)
        
        # C-style (row-major) vs Fortran-style (column-major)
        arr_c = np.random.random(size)  # По умолчанию C-style
        arr_f = np.asfortranarray(arr_c)  # Fortran-style
        
        results = {}
        
        # Тест доступа по строкам
        start = time.time()
        for i in range(size[0]):
            _ = arr_c[i, :].sum()
        results['row_access_c_style'] = time.time() - start
        
        start = time.time()
        for i in range(size[0]):
            _ = arr_f[i, :].sum()
        results['row_access_f_style'] = time.time() - start
        
        # Тест доступа по столбцам
        start = time.time()
        for j in range(size[1]):
            _ = arr_c[:, j].sum()
        results['column_access_c_style'] = time.time() - start
        
        start = time.time()
        for j in range(size[1]):
            _ = arr_f[:, j].sum()
        results['column_access_f_style'] = time.time() - start
        
        return results
    
    @staticmethod
    def cache_optimization():
        """Оптимизация использования кэша"""
        sizes = [100, 500, 1000, 2000]
        results = {}
        
        for size in sizes:
            A = np.random.random((size, size))
            B = np.random.random((size, size))
            
            # Обычное умножение
            start = time.time()
            C1 = A @ B
            time_normal = time.time() - start
            
            # Блочное умножение (может быть эффективнее для больших матриц)
            block_size = min(64, size // 4)
            C2 = np.zeros((size, size))
            
            start = time.time()
            for i in range(0, size, block_size):
                for j in range(0, size, block_size):
                    for k in range(0, size, block_size):
                        i_end = min(i + block_size, size)
                        j_end = min(j + block_size, size)
                        k_end = min(k + block_size, size)
                        
                        C2[i:i_end, j:j_end] += A[i:i_end, k:k_end] @ B[k:k_end, j:j_end]
            
            time_blocked = time.time() - start
            
            results[size] = {
                'normal_time': time_normal,
                'blocked_time': time_blocked,
                'speedup': time_normal / time_blocked,
                'results_equal': np.allclose(C1, C2)
            }
        
        return results
    
    @staticmethod
    @jit(nopython=True)
    def numba_optimized_function(arr):
        """Функция, оптимизированная с помощью Numba"""
        result = np.zeros_like(arr)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                result[i, j] = np.sqrt(arr[i, j]**2 + 1) * np.sin(arr[i, j])
        return result
    
    @staticmethod
    def compare_numba_performance():
        """Сравнение производительности с Numba"""
        size = (1000, 1000)
        arr = np.random.random(size)
        
        # Чистый NumPy
        start = time.time()
        result_numpy = np.sqrt(arr**2 + 1) * np.sin(arr)
        time_numpy = time.time() - start
        
        # Первый вызов Numba (включает компиляцию)
        start = time.time()
        result_numba_first = PerformanceOptimization.numba_optimized_function(arr)
        time_numba_first = time.time() - start
        
        # Второй вызов Numba (без компиляции)
        start = time.time()
        result_numba_second = PerformanceOptimization.numba_optimized_function(arr)
        time_numba_second = time.time() - start
        
        return {
            'numpy_time': time_numpy,
            'numba_first_call': time_numba_first,
            'numba_second_call': time_numba_second,
            'numba_speedup': time_numpy / time_numba_second,
            'results_close': np.allclose(result_numpy, result_numba_second)
        }

# Практические применения
class ScientificComputing:
    """Научные вычисления с NumPy"""
    
    @staticmethod
    def monte_carlo_pi_estimation(n_samples: int = 1000000):
        """Оценка π методом Монте-Карло"""
        # Генерируем случайные точки в квадрате [-1, 1] x [-1, 1]
        points = np.random.uniform(-1, 1, (n_samples, 2))
        
        # Считаем точки внутри единичного круга
        distances_squared = np.sum(points**2, axis=1)
        inside_circle = distances_squared <= 1
        
        # Оценка π
        pi_estimate = 4 * np.sum(inside_circle) / n_samples
        
        return {
            'pi_estimate': pi_estimate,
            'error': abs(pi_estimate - np.pi),
            'relative_error': abs(pi_estimate - np.pi) / np.pi * 100,
            'samples_used': n_samples
        }
    
    @staticmethod
    def numerical_integration(func: Callable, a: float, b: float, n: int = 1000000):
        """Численное интегрирование методом трапеций"""
        x = np.linspace(a, b, n)
        y = func(x)
        
        # Метод трапеций
        integral = np.trapz(y, x)
        
        return {
            'integral_value': integral,
            'method': 'trapezoidal',
            'intervals': n,
            'step_size': (b - a) / (n - 1)
        }
    
    @staticmethod
    def signal_processing_example():
        """Пример обработки сигналов"""
        # Создаем составной сигнал
        t = np.linspace(0, 1, 1000)
        signal = (np.sin(2 * np.pi * 5 * t) +  # 5 Hz
                 0.5 * np.sin(2 * np.pi * 20 * t) +  # 20 Hz
                 0.3 * np.sin(2 * np.pi * 50 * t) +  # 50 Hz
                 0.1 * np.random.normal(0, 1, len(t)))  # Шум
        
        # FFT для анализа спектра
        fft = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(len(signal), t[1] - t[0])
        
        # Находим доминирующие частоты
        magnitude = np.abs(fft)
        positive_freq_idx = frequencies > 0
        
        dominant_frequencies = frequencies[positive_freq_idx][
            np.argsort(magnitude[positive_freq_idx])[-5:]
        ]
        
        return {
            'signal_length': len(signal),
            'sampling_rate': 1 / (t[1] - t[0]),
            'dominant_frequencies': sorted(dominant_frequencies),
            'signal_power': np.mean(signal**2),
            'snr_estimate': np.var(signal[:-100]) / np.var(np.diff(signal))
        }

def demonstrate_numpy_capabilities():
    """Демонстрация возможностей NumPy"""
    print("🔢 Демонстрация продвинутых возможностей NumPy")
    print("=" * 50)
    
    # Векторизация
    print("\n⚡ Векторизация вычислений:")
    vec_results = AdvancedNumPyOperations.vectorization_examples()
    print(f"Ускорение векторизации: {vec_results['speedup']:.2f}x")
    for method, time_val in vec_results['times'].items():
        print(f"  {method}: {time_val:.4f} сек")
    
    # Линейная алгебра
    print("\n🧮 Анализ собственных значений:")
    eigen_results = LinearAlgebraOperations.eigenvalue_analysis()
    print(f"Число обусловленности: {eigen_results['condition_number']:.2f}")
    print(f"Максимальное собственное значение: {eigen_results['max_eigenvalue']:.4f}")
    
    # Научные вычисления
    print("\n🔬 Оценка π методом Монте-Карло:")
    pi_results = ScientificComputing.monte_carlo_pi_estimation()
    print(f"Оценка π: {pi_results['pi_estimate']:.6f}")
    print(f"Ошибка: {pi_results['relative_error']:.4f}%")
    
    # Оптимизация производительности
    print("\n🚀 Сравнение с Numba:")
    numba_results = PerformanceOptimization.compare_numba_performance()
    print(f"Ускорение Numba: {numba_results['numba_speedup']:.2f}x")
    
    return {
        'vectorization': vec_results,
        'eigenanalysis': eigen_results,
        'monte_carlo': pi_results,
        'numba_performance': numba_results
    }
```

Этот раздел охватывает продвинутые аспекты анализа данных и научных вычислений в Python, от базовой работы с Pandas до оптимизации производительности NumPy. 