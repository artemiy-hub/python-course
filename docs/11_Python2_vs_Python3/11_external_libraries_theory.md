# Теория: Внешние библиотеки в Python

## 🎯 Цель раздела

Внешние библиотеки — это мощь Python. Огромная экосистема готовых решений позволяет разработчикам быстро создавать сложные приложения. Этот раздел охватывает работу с популярными внешними библиотеками и управление зависимостями.

## 📋 Содержание

1. [Управление пакетами с pip](#управление-пакетами-с-pip)
2. [Виртуальные окружения](#виртуальные-окружения)
3. [Научные вычисления](#научные-вычисления)
4. [Веб-разработка](#веб-разработка)
5. [Работа с данными](#работа-с-данными)
6. [HTTP и API](#http-и-api)
7. [Анализ данных](#анализ-данных)
8. [Машинное обучение](#машинное-обучение)
9. [Лучшие практики](#лучшие-практики)

---

## 📦 Управление пакетами с pip

### Основы pip

**pip** (Pip Installs Packages) — стандартный менеджер пакетов для Python, позволяющий устанавливать и управлять библиотеками из Python Package Index (PyPI).

```bash
# Установка пакета
pip install requests

# Установка конкретной версии
pip install Django==4.2.0

# Установка минимальной версии
pip install numpy>=1.20.0

# Установка из requirements.txt
pip install -r requirements.txt

# Обновление пакета
pip install --upgrade requests

# Удаление пакета
pip uninstall requests

# Просмотр установленных пакетов
pip list

# Информация о пакете
pip show requests

# Поиск пакетов
pip search machine-learning
```

### Работа с requirements.txt

```python
# requirements.txt - файл зависимостей проекта
"""
# Основные зависимости
requests>=2.28.0
numpy>=1.21.0
pandas>=1.3.0

# Веб-фреймворки
Django>=4.0.0,<5.0.0
Flask>=2.0.0

# Научные библиотеки
matplotlib>=3.5.0
scipy>=1.7.0
scikit-learn>=1.0.0

# Разработка и тестирование
pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0

# Опциональные зависимости
# Раскомментировать при необходимости
# tensorflow>=2.8.0
# torch>=1.11.0
"""

# Генерация requirements.txt из текущего окружения
import subprocess
import sys

def generate_requirements():
    """Генерация файла requirements.txt"""
    result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                          capture_output=True, text=True)
    
    with open('requirements.txt', 'w') as f:
        f.write(result.stdout)
    
    print("requirements.txt создан")

def install_from_requirements():
    """Установка пакетов из requirements.txt"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("Пакеты установлены успешно")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка установки: {e}")

# Программная установка пакетов
def install_package(package_name, version=None):
    """Программная установка пакета"""
    if version:
        package = f"{package_name}=={version}"
    else:
        package = package_name
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                      check=True)
        print(f"Пакет {package} установлен")
        return True
    except subprocess.CalledProcessError:
        print(f"Ошибка установки {package}")
        return False

# Проверка доступности пакета
def check_package_available(package_name):
    """Проверка наличия пакета"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

# Пример использования
if __name__ == "__main__":
    # Проверяем наличие requests
    if not check_package_available('requests'):
        print("Устанавливаем requests...")
        install_package('requests')
    else:
        print("requests уже установлен")
```

### Продвинутые возможности pip

```bash
# Установка из git репозитория
pip install git+https://github.com/username/repository.git

# Установка в режиме разработки
pip install -e .

# Установка с дополнительными зависимостями
pip install requests[security,socks]

# Загрузка без установки
pip download numpy

# Установка в пользовательскую директорию
pip install --user requests

# Принудительная переустановка
pip install --force-reinstall requests

# Установка без зависимостей
pip install --no-deps some-package

# Сухой запуск (проверка без установки)
pip install --dry-run requests

# Кэширование пакетов
pip install --cache-dir ./pip-cache requests
```

---

## 🐍 Виртуальные окружения

### venv - встроенный модуль

```bash
# Создание виртуального окружения
python -m venv myenv

# Активация (Windows)
myenv\Scripts\activate

# Активация (Unix/macOS)
source myenv/bin/activate

# Деактивация
deactivate

# Удаление окружения
rm -rf myenv  # Unix/macOS
rmdir /s myenv  # Windows
```

### Программное управление виртуальными окружениями

```python
import os
import sys
import subprocess
import venv
from pathlib import Path

class VirtualEnvironmentManager:
    """Менеджер виртуальных окружений"""
    
    def __init__(self, envs_dir="venvs"):
        self.envs_dir = Path(envs_dir)
        self.envs_dir.mkdir(exist_ok=True)
    
    def create_env(self, env_name, python_version=None):
        """Создание виртуального окружения"""
        env_path = self.envs_dir / env_name
        
        if env_path.exists():
            print(f"Окружение {env_name} уже существует")
            return False
        
        try:
            # Создаем окружение
            if python_version:
                subprocess.run([python_version, '-m', 'venv', str(env_path)], 
                             check=True)
            else:
                venv.create(env_path, with_pip=True)
            
            print(f"Окружение {env_name} создано в {env_path}")
            return True
        
        except Exception as e:
            print(f"Ошибка создания окружения: {e}")
            return False
    
    def list_environments(self):
        """Список виртуальных окружений"""
        environments = []
        
        for env_dir in self.envs_dir.iterdir():
            if env_dir.is_dir():
                # Проверяем, что это виртуальное окружение
                if (env_dir / 'pyvenv.cfg').exists():
                    environments.append(env_dir.name)
        
        return environments
    
    def get_env_python(self, env_name):
        """Получение пути к Python в окружении"""
        env_path = self.envs_dir / env_name
        
        if os.name == 'nt':  # Windows
            python_path = env_path / 'Scripts' / 'python.exe'
        else:  # Unix/macOS
            python_path = env_path / 'bin' / 'python'
        
        return str(python_path) if python_path.exists() else None
    
    def install_package(self, env_name, package):
        """Установка пакета в виртуальное окружение"""
        python_path = self.get_env_python(env_name)
        
        if not python_path:
            print(f"Окружение {env_name} не найдено")
            return False
        
        try:
            subprocess.run([python_path, '-m', 'pip', 'install', package], 
                         check=True)
            print(f"Пакет {package} установлен в {env_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Ошибка установки: {e}")
            return False
    
    def run_in_env(self, env_name, command):
        """Выполнение команды в виртуальном окружении"""
        python_path = self.get_env_python(env_name)
        
        if not python_path:
            print(f"Окружение {env_name} не найдено")
            return False
        
        try:
            if isinstance(command, str):
                # Выполняем Python код
                result = subprocess.run([python_path, '-c', command], 
                                      capture_output=True, text=True)
            else:
                # Выполняем команду как список
                result = subprocess.run([python_path] + command, 
                                      capture_output=True, text=True)
            
            print(f"Вывод:\n{result.stdout}")
            if result.stderr:
                print(f"Ошибки:\n{result.stderr}")
            
            return result.returncode == 0
        
        except Exception as e:
            print(f"Ошибка выполнения: {e}")
            return False

# Пример использования
def demonstrate_venv_management():
    """Демонстрация управления виртуальными окружениями"""
    
    manager = VirtualEnvironmentManager()
    
    # Создаем тестовое окружение
    env_name = "test_project"
    
    if manager.create_env(env_name):
        print(f"Окружение {env_name} создано")
    
    # Устанавливаем пакеты
    packages = ['requests', 'numpy']
    for package in packages:
        manager.install_package(env_name, package)
    
    # Тестируем установленные пакеты
    test_code = """
import sys
print(f"Python: {sys.version}")
try:
    import requests
    print(f"requests: {requests.__version__}")
except ImportError:
    print("requests не установлен")

try:
    import numpy
    print(f"numpy: {numpy.__version__}")
except ImportError:
    print("numpy не установлен")
"""
    
    print(f"\nТестирование окружения {env_name}:")
    manager.run_in_env(env_name, test_code)
    
    # Список окружений
    environments = manager.list_environments()
    print(f"\nДоступные окружения: {environments}")

# demonstrate_venv_management()
```

### Poetry - современный менеджер зависимостей

```bash
# Установка Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Создание нового проекта
poetry new my-project

# Инициализация в существующем проекте
poetry init

# Добавление зависимости
poetry add requests

# Добавление зависимости для разработки
poetry add pytest --group dev

# Установка зависимостей
poetry install

# Обновление зависимостей
poetry update

# Удаление зависимости
poetry remove requests

# Запуск команды в виртуальном окружении
poetry run python script.py

# Активация оболочки виртуального окружения
poetry shell
```

### pyproject.toml для Poetry

```toml
[tool.poetry]
name = "my-awesome-project"
version = "0.1.0"
description = "Описание проекта"
authors = ["Ваше Имя <email@example.com>"]
readme = "README.md"
packages = [{include = "my_project"}]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.0"
numpy = "^1.21.0"
pandas = "^1.3.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^22.0.0"
flake8 = "^4.0.0"
mypy = "^0.991"

[tool.poetry.group.docs.dependencies]
sphinx = "^4.5.0"
sphinx-rtd-theme = "^1.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.scripts]
my-script = "my_project.main:main"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
```

---

## 🔬 Научные вычисления

### NumPy - основа научных вычислений

```python
import numpy as np

# Основы NumPy
def numpy_basics():
    """Основы работы с NumPy"""
    
    # Создание массивов
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.zeros((3, 4))  # Массив нулей
    arr3 = np.ones((2, 3))   # Массив единиц
    arr4 = np.full((2, 2), 7)  # Массив заполненный значением
    arr5 = np.eye(3)         # Единичная матрица
    arr6 = np.arange(0, 10, 2)  # Диапазон с шагом
    arr7 = np.linspace(0, 1, 5)  # Равномерно распределенные значения
    
    print("Создание массивов:")
    print(f"Одномерный: {arr1}")
    print(f"Нули 3x4:\n{arr2}")
    print(f"Единицы 2x3:\n{arr3}")
    print(f"Заполненный 7:\n{arr4}")
    print(f"Единичная матрица:\n{arr5}")
    print(f"Диапазон: {arr6}")
    print(f"Linspace: {arr7}")
    
    # Свойства массивов
    matrix = np.random.randint(1, 10, (3, 4))
    print(f"\nСлучайная матрица 3x4:\n{matrix}")
    print(f"Форма: {matrix.shape}")
    print(f"Размерность: {matrix.ndim}")
    print(f"Размер: {matrix.size}")
    print(f"Тип данных: {matrix.dtype}")
    
    # Индексирование и срезы
    print(f"\nЭлемент [1,2]: {matrix[1, 2]}")
    print(f"Первая строка: {matrix[0, :]}")
    print(f"Второй столбец: {matrix[:, 1]}")
    print(f"Подматрица:\n{matrix[0:2, 1:3]}")
    
    # Математические операции
    arr_a = np.array([1, 2, 3])
    arr_b = np.array([4, 5, 6])
    
    print(f"\nМатематические операции:")
    print(f"A: {arr_a}, B: {arr_b}")
    print(f"A + B: {arr_a + arr_b}")
    print(f"A * B: {arr_a * arr_b}")  # Поэлементное умножение
    print(f"A @ B: {arr_a @ arr_b}")  # Скалярное произведение
    print(f"A ** 2: {arr_a ** 2}")
    
    # Статистические функции
    data = np.random.normal(100, 15, 1000)  # Нормальное распределение
    print(f"\nСтатистика для {len(data)} значений:")
    print(f"Среднее: {np.mean(data):.2f}")
    print(f"Медиана: {np.median(data):.2f}")
    print(f"Стд. отклонение: {np.std(data):.2f}")
    print(f"Минимум: {np.min(data):.2f}")
    print(f"Максимум: {np.max(data):.2f}")
    
    # Логические операции
    print(f"\nЛогические операции:")
    print(f"Значения > 110: {np.sum(data > 110)}")
    print(f"Значения в диапазоне [90, 110]: {np.sum((data >= 90) & (data <= 110))}")

def numpy_advanced():
    """Продвинутые возможности NumPy"""
    
    # Изменение формы массивов
    arr = np.arange(12)
    print(f"Исходный массив: {arr}")
    print(f"Reshape 3x4:\n{arr.reshape(3, 4)}")
    print(f"Reshape 2x2x3:\n{arr.reshape(2, 2, 3)}")
    
    # Объединение массивов
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    print(f"\nМассив A:\n{a}")
    print(f"Массив B:\n{b}")
    print(f"Concatenate по строкам:\n{np.concatenate([a, b], axis=0)}")
    print(f"Concatenate по столбцам:\n{np.concatenate([a, b], axis=1)}")
    print(f"Stack:\n{np.stack([a, b])}")
    print(f"Hstack:\n{np.hstack([a, b])}")
    print(f"Vstack:\n{np.vstack([a, b])}")
    
    # Разделение массивов
    big_array = np.arange(16).reshape(4, 4)
    print(f"\nБольшой массив:\n{big_array}")
    
    splits = np.split(big_array, 2, axis=0)
    print(f"Разделение по строкам: {len(splits)} частей")
    for i, split in enumerate(splits):
        print(f"  Часть {i}:\n{split}")
    
    # Условные операции
    data = np.random.randint(-10, 10, (3, 4))
    print(f"\nИсходные данные:\n{data}")
    print(f"Положительные значения:\n{np.where(data > 0, data, 0)}")
    print(f"Замена отрицательных на -1:\n{np.where(data < 0, -1, data)}")
    
    # Линейная алгебра
    matrix_a = np.random.rand(3, 3)
    matrix_b = np.random.rand(3, 3)
    
    print(f"\nЛинейная алгебра:")
    print(f"Определитель A: {np.linalg.det(matrix_a):.4f}")
    
    try:
        inv_a = np.linalg.inv(matrix_a)
        print(f"Обратная матрица найдена")
        print(f"A * A^-1 ≈ E:\n{np.allclose(matrix_a @ inv_a, np.eye(3))}")
    except np.linalg.LinAlgError:
        print("Матрица необратима")
    
    # Собственные значения и векторы
    eigenvals, eigenvecs = np.linalg.eig(matrix_a)
    print(f"Собственные значения: {eigenvals}")
    
    # Решение системы линейных уравнений Ax = b
    A = np.array([[2, 1], [1, 3]])
    b = np.array([3, 4])
    x = np.linalg.solve(A, b)
    print(f"\nРешение системы Ax = b:")
    print(f"A:\n{A}")
    print(f"b: {b}")
    print(f"x: {x}")
    print(f"Проверка Ax: {A @ x}")

# numpy_basics()
# numpy_advanced()
```

### SciPy - научные алгоритмы

```python
# Работа с SciPy
try:
    import scipy
    from scipy import optimize, integrate, stats, signal
    from scipy.spatial.distance import cdist
    from scipy.interpolate import interp1d
    
    def scipy_examples():
        """Примеры работы с SciPy"""
        
        # Оптимизация
        print("=== Оптимизация ===")
        
        # Минимизация функции
        def objective_function(x):
            return x**2 + 4*x + 4
        
        result = optimize.minimize_scalar(objective_function)
        print(f"Минимум функции x² + 4x + 4:")
        print(f"  x = {result.x:.4f}")
        print(f"  f(x) = {result.fun:.4f}")
        
        # Поиск корней
        def equation(x):
            return x**3 - 2*x - 5
        
        root = optimize.fsolve(equation, 2)[0]
        print(f"Корень уравнения x³ - 2x - 5 = 0: {root:.4f}")
        print(f"Проверка: f({root:.4f}) = {equation(root):.6f}")
        
        # Интегрирование
        print("\n=== Интегрирование ===")
        
        def integrand(x):
            return np.sin(x) * np.exp(-x)
        
        integral, error = integrate.quad(integrand, 0, np.inf)
        print(f"Интеграл sin(x)*exp(-x) от 0 до ∞: {integral:.6f} ± {error:.2e}")
        
        # Статистика
        print("\n=== Статистика ===")
        
        # Генерация случайных данных
        data1 = stats.norm.rvs(loc=100, scale=15, size=100)
        data2 = stats.norm.rvs(loc=105, scale=12, size=100)
        
        # t-тест
        t_stat, p_value = stats.ttest_ind(data1, data2)
        print(f"t-тест для двух выборок:")
        print(f"  t-статистика: {t_stat:.4f}")
        print(f"  p-value: {p_value:.6f}")
        
        # Корреляция
        correlation, p_val = stats.pearsonr(data1[:50], data2[:50])
        print(f"Корреляция Пирсона: {correlation:.4f} (p={p_val:.4f})")
        
        # Обработка сигналов
        print("\n=== Обработка сигналов ===")
        
        # Создание сигнала с шумом
        t = np.linspace(0, 1, 500)
        clean_signal = np.sin(2 * np.pi * 5 * t)  # 5 Гц
        noise = 0.3 * np.random.randn(len(t))
        noisy_signal = clean_signal + noise
        
        # Применение фильтра
        b, a = signal.butter(4, 0.1, 'low')  # Низкочастотный фильтр
        filtered_signal = signal.filtfilt(b, a, noisy_signal)
        
        # Оценка качества фильтрации
        mse_before = np.mean((noisy_signal - clean_signal)**2)
        mse_after = np.mean((filtered_signal - clean_signal)**2)
        
        print(f"MSE до фильтрации: {mse_before:.6f}")
        print(f"MSE после фильтрации: {mse_after:.6f}")
        print(f"Улучшение: {(mse_before/mse_after):.2f}x")
        
        # Интерполяция
        print("\n=== Интерполяция ===")
        
        x = np.array([0, 1, 2, 3, 4, 5])
        y = np.array([0, 1, 4, 9, 16, 25])  # y = x²
        
        # Создаем интерполяционную функцию
        f_linear = interp1d(x, y, kind='linear')
        f_cubic = interp1d(x, y, kind='cubic')
        
        # Тестируем интерполяцию
        x_new = np.array([1.5, 2.5, 3.5])
        y_linear = f_linear(x_new)
        y_cubic = f_cubic(x_new)
        y_true = x_new**2
        
        print(f"Точки для интерполяции: {x_new}")
        print(f"Истинные значения: {y_true}")
        print(f"Линейная интерполяция: {y_linear}")
        print(f"Кубическая интерполяция: {y_cubic}")
        
        # Расстояния между точками
        print("\n=== Расстояния ===")
        
        points = np.random.rand(5, 2) * 10  # 5 точек в 2D
        distances = cdist(points, points, metric='euclidean')
        
        print(f"Координаты точек:\n{points}")
        print(f"Матрица расстояний:\n{distances}")

    scipy_examples()

except ImportError:
    print("SciPy не установлен. Установите: pip install scipy")
```

### Matplotlib - визуализация данных

```python
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime, timedelta
    
    def matplotlib_examples():
        """Примеры визуализации с Matplotlib"""
        
        # Настройка стиля
        plt.style.use('default')  # Можно попробовать 'seaborn', 'ggplot'
        
        # 1. Простой график
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        
        plt.figure(figsize=(12, 8))
        
        # Первый подграфик
        plt.subplot(2, 2, 1)
        plt.plot(x, y1, label='sin(x)', linewidth=2)
        plt.plot(x, y2, label='cos(x)', linewidth=2, linestyle='--')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Тригонометрические функции')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. Гистограмма
        plt.subplot(2, 2, 2)
        data = np.random.normal(100, 15, 1000)
        plt.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.xlabel('Значение')
        plt.ylabel('Частота')
        plt.title('Гистограмма (нормальное распределение)')
        plt.axvline(np.mean(data), color='red', linestyle='--', 
                   label=f'Среднее: {np.mean(data):.1f}')
        plt.legend()
        
        # 3. Диаграмма рассеяния
        plt.subplot(2, 2, 3)
        x_scatter = np.random.randn(200)
        y_scatter = 2 * x_scatter + np.random.randn(200) * 0.5
        
        plt.scatter(x_scatter, y_scatter, alpha=0.6, c=y_scatter, cmap='viridis')
        plt.colorbar(label='Значение Y')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Диаграмма рассеяния')
        
        # Линия тренда
        z = np.polyfit(x_scatter, y_scatter, 1)
        p = np.poly1d(z)
        plt.plot(x_scatter, p(x_scatter), "r--", alpha=0.8, 
                label=f'Тренд: y={z[0]:.2f}x+{z[1]:.2f}')
        plt.legend()
        
        # 4. Временные ряды
        plt.subplot(2, 2, 4)
        
        # Генерируем временные данные
        start_date = datetime(2023, 1, 1)
        dates = [start_date + timedelta(days=i) for i in range(365)]
        trend = np.linspace(100, 120, 365)
        seasonal = 10 * np.sin(2 * np.pi * np.arange(365) / 365.25 * 4)
        noise = np.random.normal(0, 2, 365)
        values = trend + seasonal + noise
        
        plt.plot(dates, values, linewidth=1, alpha=0.7)
        plt.plot(dates, trend, 'r-', linewidth=2, label='Тренд')
        
        plt.xlabel('Дата')
        plt.ylabel('Значение')
        plt.title('Временной ряд')
        plt.legend()
        
        # Форматирование оси дат
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        # Дополнительные типы графиков
        plt.figure(figsize=(15, 10))
        
        # 1. Box plot
        plt.subplot(2, 3, 1)
        data_groups = [np.random.normal(100, 10, 100),
                      np.random.normal(110, 15, 100),
                      np.random.normal(95, 8, 100)]
        plt.boxplot(data_groups, labels=['Группа A', 'Группа B', 'Группа C'])
        plt.title('Box Plot')
        plt.ylabel('Значения')
        
        # 2. Круговая диаграмма
        plt.subplot(2, 3, 2)
        labels = ['Python', 'JavaScript', 'Java', 'C++', 'Другие']
        sizes = [35, 25, 20, 15, 5]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
        
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
               startangle=90)
        plt.title('Популярность языков программирования')
        
        # 3. Столбчатая диаграмма
        plt.subplot(2, 3, 3)
        categories = ['Кат. 1', 'Кат. 2', 'Кат. 3', 'Кат. 4']
        values1 = [20, 35, 30, 25]
        values2 = [25, 30, 35, 20]
        
        x = np.arange(len(categories))
        width = 0.35
        
        plt.bar(x - width/2, values1, width, label='Серия 1', alpha=0.8)
        plt.bar(x + width/2, values2, width, label='Серия 2', alpha=0.8)
        
        plt.xlabel('Категории')
        plt.ylabel('Значения')
        plt.title('Сравнение категорий')
        plt.xticks(x, categories)
        plt.legend()
        
        # 4. Тепловая карта
        plt.subplot(2, 3, 4)
        data_2d = np.random.rand(10, 12)
        
        im = plt.imshow(data_2d, cmap='hot', interpolation='nearest')
        plt.colorbar(im)
        plt.title('Тепловая карта')
        plt.xlabel('X координата')
        plt.ylabel('Y координата')
        
        # 5. Логарифмический график
        plt.subplot(2, 3, 5)
        x_log = np.logspace(0, 3, 100)  # От 10^0 до 10^3
        y_log = x_log ** 0.5
        
        plt.loglog(x_log, y_log, 'b-', linewidth=2)
        plt.xlabel('X (логарифмическая шкала)')
        plt.ylabel('Y (логарифмическая шкала)')
        plt.title('Логарифмический график')
        plt.grid(True, alpha=0.3)
        
        # 6. Полярный график
        plt.subplot(2, 3, 6, projection='polar')
        theta = np.linspace(0, 2*np.pi, 100)
        r = 2 + np.sin(5*theta)
        
        plt.plot(theta, r, linewidth=2)
        plt.fill(theta, r, alpha=0.3)
        plt.title('Полярный график')
        
        plt.tight_layout()
        plt.show()

    matplotlib_examples()

except ImportError:
    print("Matplotlib не установлен. Установите: pip install matplotlib")
```

---

## 🌐 Веб-разработка

### Requests - HTTP библиотека

```python
import requests
import json
from urllib.parse import urlencode

def requests_examples():
    """Примеры работы с HTTP запросами"""
    
    print("=== Примеры работы с Requests ===")
    
    # Базовые HTTP методы
    print("1. Базовые HTTP запросы:")
    
    # GET запрос
    try:
        response = requests.get('https://httpbin.org/get')
        print(f"GET запрос:")
        print(f"  Статус: {response.status_code}")
        print(f"  Заголовки: {dict(list(response.headers.items())[:3])}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  URL: {data.get('url')}")
            print(f"  User-Agent: {data.get('headers', {}).get('User-Agent', 'N/A')[:50]}...")
    
    except requests.RequestException as e:
        print(f"Ошибка GET запроса: {e}")
    
    # POST запрос с данными
    print("\n2. POST запрос с данными:")
    
    post_data = {
        'name': 'Иван Петров',
        'email': 'ivan@example.com',
        'age': 30
    }
    
    try:
        response = requests.post('https://httpbin.org/post', json=post_data)
        print(f"POST запрос:")
        print(f"  Статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            received_data = result.get('json', {})
            print(f"  Отправленные данные: {received_data}")
    
    except requests.RequestException as e:
        print(f"Ошибка POST запроса: {e}")
    
    # Работа с параметрами URL
    print("\n3. Параметры URL:")
    
    params = {
        'q': 'python programming',
        'lang': 'ru',
        'count': 10
    }
    
    try:
        response = requests.get('https://httpbin.org/get', params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"URL с параметрами: {data.get('url')}")
            print(f"Параметры: {data.get('args')}")
    
    except requests.RequestException as e:
        print(f"Ошибка запроса с параметрами: {e}")
    
    # Заголовки и аутентификация
    print("\n4. Заголовки и аутентификация:")
    
    headers = {
        'User-Agent': 'MyApp/1.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer fake-token-123'
    }
    
    try:
        response = requests.get('https://httpbin.org/headers', headers=headers)
        if response.status_code == 200:
            data = response.json()
            received_headers = data.get('headers', {})
            print(f"Отправленные заголовки:")
            for key in ['User-Agent', 'Accept', 'Authorization']:
                print(f"  {key}: {received_headers.get(key, 'N/A')}")
    
    except requests.RequestException as e:
        print(f"Ошибка запроса с заголовками: {e}")
    
    # Работа с cookies
    print("\n5. Работа с cookies:")
    
    session = requests.Session()
    
    try:
        # Устанавливаем cookie
        response1 = session.get('https://httpbin.org/cookies/set/session_id/abc123')
        
        # Проверяем, что cookie сохранилось
        response2 = session.get('https://httpbin.org/cookies')
        if response2.status_code == 200:
            cookies_data = response2.json()
            print(f"Cookies: {cookies_data.get('cookies')}")
    
    except requests.RequestException as e:
        print(f"Ошибка работы с cookies: {e}")
    
    # Обработка ошибок и таймауты
    print("\n6. Обработка ошибок и таймауты:")
    
    def safe_request(url, timeout=5, retries=3):
        """Безопасный HTTP запрос с повторными попытками"""
        
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()  # Вызовет исключение для 4xx/5xx
                return response
            
            except requests.exceptions.Timeout:
                print(f"  Попытка {attempt + 1}: Таймаут")
            except requests.exceptions.ConnectionError:
                print(f"  Попытка {attempt + 1}: Ошибка соединения")
            except requests.exceptions.HTTPError as e:
                print(f"  Попытка {attempt + 1}: HTTP ошибка {e}")
                break  # Не повторяем для HTTP ошибок
            except requests.exceptions.RequestException as e:
                print(f"  Попытка {attempt + 1}: Общая ошибка {e}")
            
            if attempt < retries - 1:
                print(f"    Повторная попытка через 1 секунду...")
                import time
                time.sleep(1)
        
        return None
    
    # Тестируем с несуществующим доменом
    print("Тест с несуществующим доменом:")
    result = safe_request('https://nonexistent-domain-12345.com')
    print(f"Результат: {'Успех' if result else 'Неудача'}")
    
    # Загрузка файлов
    print("\n7. Загрузка больших файлов:")
    
    def download_file(url, filename=None, chunk_size=8192):
        """Загрузка файла с прогрессом"""
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            if filename is None:
                filename = url.split('/')[-1] or 'downloaded_file'
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            print(f"Загружаем {filename} ({total_size} байт)")
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\rПрогресс: {progress:.1f}% ({downloaded}/{total_size})", 
                                 end='', flush=True)
            
            print(f"\nФайл {filename} загружен успешно")
            return filename
        
        except requests.RequestException as e:
            print(f"Ошибка загрузки: {e}")
            return None
    
    # Тестируем загрузку (небольшой файл для демонстрации)
    # downloaded_file = download_file('https://httpbin.org/json', 'test.json')

# requests_examples()
```

### Flask - микрофреймворк

```python
try:
    from flask import Flask, request, jsonify, render_template_string
    
    def create_demo_flask_app():
        """Создание демонстрационного Flask приложения"""
        
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'demo-secret-key'
        
        # Простые данные для демонстрации
        users = [
            {'id': 1, 'name': 'Алиса', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Боб', 'email': 'bob@example.com'},
            {'id': 3, 'name': 'Чарли', 'email': 'charlie@example.com'}
        ]
        
        # Главная страница
        @app.route('/')
        def index():
            html_template = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Demo Flask App</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
                    .method { color: #007bff; font-weight: bold; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🐍 Demo Flask Application</h1>
                    <p>Демонстрационное приложение Flask с примерами различных маршрутов.</p>
                    
                    <h2>Доступные endpoints:</h2>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/</code> - Главная страница
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/api/users</code> - Список пользователей (JSON)
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/api/users/&lt;id&gt;</code> - Пользователь по ID
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">POST</span> <code>/api/users</code> - Создание пользователя
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/hello/&lt;name&gt;</code> - Приветствие
                    </div>
                    
                    <div class="endpoint">
                        <span class="method">GET</span> <code>/search</code> - Поиск с параметрами
                    </div>
                    
                    <h2>Примеры использования:</h2>
                    <pre>
# Получить всех пользователей
curl http://localhost:5000/api/users

# Получить пользователя по ID
curl http://localhost:5000/api/users/1

# Создать нового пользователя
curl -X POST http://localhost:5000/api/users \\
     -H "Content-Type: application/json" \\
     -d '{"name": "Новый пользователь", "email": "new@example.com"}'

# Поиск с параметрами
curl "http://localhost:5000/search?q=python&limit=10"
                    </pre>
                </div>
            </body>
            </html>
            '''
            return html_template
        
        # API для работы с пользователями
        @app.route('/api/users', methods=['GET'])
        def get_users():
            """Получить список всех пользователей"""
            return jsonify({
                'users': users,
                'total': len(users)
            })
        
        @app.route('/api/users/<int:user_id>', methods=['GET'])
        def get_user(user_id):
            """Получить пользователя по ID"""
            user = next((u for u in users if u['id'] == user_id), None)
            
            if user:
                return jsonify(user)
            else:
                return jsonify({'error': 'Пользователь не найден'}), 404
        
        @app.route('/api/users', methods=['POST'])
        def create_user():
            """Создать нового пользователя"""
            data = request.get_json()
            
            if not data or 'name' not in data or 'email' not in data:
                return jsonify({'error': 'Требуются поля name и email'}), 400
            
            new_user = {
                'id': max(u['id'] for u in users) + 1 if users else 1,
                'name': data['name'],
                'email': data['email']
            }
            
            users.append(new_user)
            
            return jsonify(new_user), 201
        
        # Маршрут с параметрами
        @app.route('/hello/<name>')
        def hello(name):
            """Приветствие с именем"""
            return jsonify({
                'message': f'Привет, {name}!',
                'timestamp': '2024-01-15T10:30:00Z'
            })
        
        # Работа с параметрами запроса
        @app.route('/search')
        def search():
            """Поиск с параметрами"""
            query = request.args.get('q', '')
            limit = request.args.get('limit', 10, type=int)
            offset = request.args.get('offset', 0, type=int)
            
            # Простая имитация поиска
            results = [
                f"Результат {i}: {query}" 
                for i in range(offset + 1, offset + limit + 1)
            ]
            
            return jsonify({
                'query': query,
                'results': results,
                'total': limit,
                'offset': offset
            })
        
        # Обработка ошибок
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Страница не найдена'}), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
        
        return app
    
    def run_flask_demo():
        """Запуск демонстрационного Flask приложения"""
        
        print("=== Демонстрация Flask ===")
        print("Создание Flask приложения...")
        
        app = create_demo_flask_app()
        
        print("Flask приложение создано!")
        print("Маршруты:")
        
        # Показываем все маршруты
        for rule in app.url_map.iter_rules():
            methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
            print(f"  {methods:10} {rule.rule}")
        
        print("\nПриложение готово к запуску!")
        print("Для запуска выполните:")
        print("  app = create_demo_flask_app()")
        print("  app.run(debug=True)")
        print("\nИли для продакшена:")
        print("  app.run(host='0.0.0.0', port=5000)")
        
        return app

    # run_flask_demo()

except ImportError:
    print("Flask не установлен. Установите: pip install Flask")
```

---

## 📊 Работа с данными

### Pandas - анализ данных

```python
try:
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    def pandas_examples():
        """Примеры работы с Pandas"""
        
        print("=== Работа с Pandas ===")
        
        # Создание DataFrame
        print("1. Создание DataFrame:")
        
        # Из словаря
        data = {
            'name': ['Алиса', 'Боб', 'Чарли', 'Диана', 'Ева'],
            'age': [25, 30, 35, 28, 32],
            'city': ['Москва', 'СПб', 'Казань', 'Москва', 'СПб'],
            'salary': [95000, 105000, 85000, 98000, 110000],
            'department': ['IT', 'HR', 'IT', 'Finance', 'IT']
        }
        
        df = pd.DataFrame(data)
        print("DataFrame из словаря:")
        print(df)
        print(f"Форма: {df.shape}")
        print(f"Типы данных:\n{df.dtypes}")
        
        # Базовые операции
        print("\n2. Базовые операции:")
        print(f"Первые 3 строки:\n{df.head(3)}")
        print(f"Последние 2 строки:\n{df.tail(2)}")
        print(f"Информация о DataFrame:\n{df.info()}")
        print(f"Статистическое описание:\n{df.describe()}")
        
        # Индексирование и выборка
        print("\n3. Индексирование и выборка:")
        print(f"Столбец 'name':\n{df['name']}")
        print(f"Несколько столбцов:\n{df[['name', 'salary']]}")
        print(f"Строки 1-3:\n{df.iloc[1:4]}")
        print(f"Строки по условию (salary > 100000):\n{df[df['salary'] > 100000]}")
        
        # Добавление новых столбцов
        print("\n4. Добавление новых столбцов:")
        df['salary_usd'] = df['salary'] / 75  # Условный курс
        df['experience'] = np.random.randint(1, 10, len(df))
        df['bonus'] = df['salary'] * 0.1
        
        print("DataFrame с новыми столбцами:")
        print(df[['name', 'salary', 'salary_usd', 'experience', 'bonus']])
        
        # Группировка и агрегация
        print("\n5. Группировка и агрегация:")
        
        city_stats = df.groupby('city').agg({
            'salary': ['mean', 'min', 'max', 'count'],
            'age': 'mean',
            'experience': 'sum'
        }).round(2)
        
        print("Статистика по городам:")
        print(city_stats)
        
        department_stats = df.groupby('department')['salary'].describe()
        print(f"\nСтатистика по отделам:\n{department_stats}")
        
        # Сортировка
        print("\n6. Сортировка:")
        sorted_by_salary = df.sort_values('salary', ascending=False)
        print("Сортировка по зарплате (убывание):")
        print(sorted_by_salary[['name', 'salary', 'city']])
        
        sorted_multi = df.sort_values(['department', 'salary'], ascending=[True, False])
        print(f"\nСортировка по отделу и зарплате:\n{sorted_multi[['name', 'department', 'salary']]}")
        
        # Работа с пропущенными значениями
        print("\n7. Работа с пропущенными значениями:")
        
        # Добавляем пропущенные значения для демонстрации
        df_with_na = df.copy()
        df_with_na.loc[1, 'salary'] = np.nan
        df_with_na.loc[3, 'age'] = np.nan
        
        print("DataFrame с пропущенными значениями:")
        print(df_with_na[['name', 'age', 'salary']])
        print(f"Количество пропущенных значений:\n{df_with_na.isnull().sum()}")
        
        # Заполнение пропущенных значений
        df_filled = df_with_na.fillna({
            'age': df_with_na['age'].mean(),
            'salary': df_with_na['salary'].median()
        })
        
        print(f"После заполнения:\n{df_filled[['name', 'age', 'salary']]}")
        
        # Работа с датами
        print("\n8. Работа с датами:")
        
        # Создаем временные ряды
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        ts_data = pd.DataFrame({
            'date': dates,
            'value': np.random.randn(30).cumsum() + 100,
            'category': np.random.choice(['A', 'B', 'C'], 30)
        })
        
        ts_data['month'] = ts_data['date'].dt.month
        ts_data['day_of_week'] = ts_data['date'].dt.day_name()
        
        print("Временные ряды:")
        print(ts_data.head())
        
        # Группировка по месяцам
        monthly_avg = ts_data.groupby('month')['value'].mean()
        print(f"Среднее значение по месяцам:\n{monthly_avg}")
        
        # Ресэмплинг (агрегация по времени)
        ts_data.set_index('date', inplace=True)
        weekly_data = ts_data.resample('W')['value'].agg(['mean', 'std', 'count'])
        print(f"Недельная агрегация:\n{weekly_data}")
        
        # Объединение DataFrame
        print("\n9. Объединение DataFrame:")
        
        # Создаем дополнительные данные
        extra_info = pd.DataFrame({
            'name': ['Алиса', 'Боб', 'Чарли', 'Фрэнк'],
            'education': ['Магистр', 'Бакалавр', 'PhD', 'Магистр'],
            'languages': [3, 2, 4, 2]
        })
        
        # Объединение по ключу
        merged_df = pd.merge(df, extra_info, on='name', how='left')
        print("Объединенный DataFrame:")
        print(merged_df[['name', 'salary', 'education', 'languages']])
        
        # Сводные таблицы
        print("\n10. Сводные таблицы:")
        
        # Добавляем данные для демонстрации pivot table
        expanded_data = []
        for _, row in df.iterrows():
            for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
                expanded_data.append({
                    'name': row['name'],
                    'department': row['department'],
                    'quarter': quarter,
                    'sales': np.random.randint(10, 100)
                })
        
        sales_df = pd.DataFrame(expanded_data)
        
        # Создаем сводную таблицу
        pivot_table = sales_df.pivot_table(
            values='sales',
            index='department',
            columns='quarter',
            aggfunc=['sum', 'mean']
        )
        
        print("Сводная таблица продаж:")
        print(pivot_table)
        
        # Сохранение и загрузка
        print("\n11. Сохранение и загрузка:")
        
        # Сохранение в различных форматах
        df.to_csv('employees.csv', index=False, encoding='utf-8')
        df.to_json('employees.json', orient='records', force_ascii=False)
        df.to_excel('employees.xlsx', index=False) if 'openpyxl' in sys.modules else print("openpyxl не установлен для Excel")
        
        print("Данные сохранены в файлы: employees.csv, employees.json")
        
        # Загрузка из файла
        df_loaded = pd.read_csv('employees.csv')
        print(f"Загружено из CSV: {df_loaded.shape}")
        
        # Очистка файлов
        import os
        for file in ['employees.csv', 'employees.json', 'employees.xlsx']:
            if os.path.exists(file):
                os.remove(file)

    pandas_examples()

except ImportError:
    print("Pandas не установлен. Установите: pip install pandas")
```

### Работа с базами данных

```python
import sqlite3
import json
from contextlib import contextmanager

def database_examples():
    """Примеры работы с базами данных"""
    
    print("=== Работа с базами данных ===")
    
    # Контекстный менеджер для работы с БД
    @contextmanager
    def get_db_connection(db_path):
        """Контекстный менеджер для соединения с БД"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
        try:
            yield conn
        finally:
            conn.close()
    
    # Класс для работы с БД
    class DatabaseManager:
        """Менеджер базы данных"""
        
        def __init__(self, db_path='example.db'):
            self.db_path = db_path
            self.init_database()
        
        def init_database(self):
            """Инициализация базы данных"""
            with get_db_connection(self.db_path) as conn:
                # Создаем таблицы
                conn.executescript('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        age INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    
                    CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        title TEXT NOT NULL,
                        content TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    );
                    
                    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                    CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
                ''')
                conn.commit()
                print("База данных инициализирована")
        
        def create_user(self, name, email, age=None):
            """Создание пользователя"""
            with get_db_connection(self.db_path) as conn:
                try:
                    cursor = conn.execute(
                        'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                        (name, email, age)
                    )
                    conn.commit()
                    user_id = cursor.lastrowid
                    print(f"Пользователь создан с ID: {user_id}")
                    return user_id
                except sqlite3.IntegrityError:
                    print(f"Пользователь с email {email} уже существует")
                    return None
        
        def get_user(self, user_id):
            """Получение пользователя по ID"""
            with get_db_connection(self.db_path) as conn:
                cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        
        def get_users(self, limit=None):
            """Получение списка пользователей"""
            query = 'SELECT * FROM users ORDER BY created_at DESC'
            if limit:
                query += f' LIMIT {limit}'
            
            with get_db_connection(self.db_path) as conn:
                cursor = conn.execute(query)
                return [dict(row) for row in cursor.fetchall()]
        
        def update_user(self, user_id, **kwargs):
            """Обновление пользователя"""
            if not kwargs:
                return False
            
            # Формируем запрос динамически
            fields = []
            values = []
            for field, value in kwargs.items():
                if field in ['name', 'email', 'age']:
                    fields.append(f'{field} = ?')
                    values.append(value)
            
            if not fields:
                return False
            
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
            
            with get_db_connection(self.db_path) as conn:
                cursor = conn.execute(query, values)
                conn.commit()
                return cursor.rowcount > 0
        
        def delete_user(self, user_id):
            """Удаление пользователя"""
            with get_db_connection(self.db_path) as conn:
                # Сначала удаляем связанные посты
                conn.execute('DELETE FROM posts WHERE user_id = ?', (user_id,))
                # Затем удаляем пользователя
                cursor = conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        
        def create_post(self, user_id, title, content):
            """Создание поста"""
            with get_db_connection(self.db_path) as conn:
                cursor = conn.execute(
                    'INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)',
                    (user_id, title, content)
                )
                conn.commit()
                post_id = cursor.lastrowid
                print(f"Пост создан с ID: {post_id}")
                return post_id
        
        def get_user_posts(self, user_id):
            """Получение постов пользователя"""
            with get_db_connection(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT p.*, u.name as user_name 
                    FROM posts p 
                    JOIN users u ON p.user_id = u.id 
                    WHERE p.user_id = ? 
                    ORDER BY p.created_at DESC
                ''', (user_id,))
                return [dict(row) for row in cursor.fetchall()]
        
        def search_posts(self, search_term):
            """Поиск постов по содержимому"""
            with get_db_connection(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT p.*, u.name as user_name 
                    FROM posts p 
                    JOIN users u ON p.user_id = u.id 
                    WHERE p.title LIKE ? OR p.content LIKE ?
                    ORDER BY p.created_at DESC
                ''', (f'%{search_term}%', f'%{search_term}%'))
                return [dict(row) for row in cursor.fetchall()]
        
        def get_stats(self):
            """Получение статистики"""
            with get_db_connection(self.db_path) as conn:
                stats = {}
                
                # Количество пользователей
                cursor = conn.execute('SELECT COUNT(*) as count FROM users')
                stats['users_count'] = cursor.fetchone()['count']
                
                # Количество постов
                cursor = conn.execute('SELECT COUNT(*) as count FROM posts')
                stats['posts_count'] = cursor.fetchone()['count']
                
                # Средний возраст пользователей
                cursor = conn.execute('SELECT AVG(age) as avg_age FROM users WHERE age IS NOT NULL')
                avg_age = cursor.fetchone()['avg_age']
                stats['avg_age'] = round(avg_age, 1) if avg_age else None
                
                # Топ авторов по количеству постов
                cursor = conn.execute('''
                    SELECT u.name, COUNT(p.id) as posts_count 
                    FROM users u 
                    LEFT JOIN posts p ON u.id = p.user_id 
                    GROUP BY u.id 
                    ORDER BY posts_count DESC 
                    LIMIT 5
                ''')
                stats['top_authors'] = [dict(row) for row in cursor.fetchall()]
                
                return stats
        
        def cleanup(self):
            """Очистка базы данных"""
            import os
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                print(f"База данных {self.db_path} удалена")
    
    # Демонстрация работы
    print("1. Инициализация базы данных:")
    db = DatabaseManager('demo.db')
    
    print("\n2. Создание пользователей:")
    user_data = [
        ('Алиса Иванова', 'alice@example.com', 28),
        ('Боб Петров', 'bob@example.com', 32),
        ('Чарли Сидоров', 'charlie@example.com', 25),
        ('Диана Козлова', 'diana@example.com', 30)
    ]
    
    user_ids = []
    for name, email, age in user_data:
        user_id = db.create_user(name, email, age)
        if user_id:
            user_ids.append(user_id)
    
    print(f"Создано пользователей: {len(user_ids)}")
    
    print("\n3. Создание постов:")
    posts_data = [
        (user_ids[0], "Введение в Python", "Python - отличный язык для начинающих программистов..."),
        (user_ids[0], "Работа с базами данных", "SQLite - простая и удобная база данных для разработки..."),
        (user_ids[1], "Веб-разработка с Flask", "Flask позволяет быстро создавать веб-приложения..."),
        (user_ids[2], "Анализ данных с Pandas", "Pandas - мощная библиотека для анализа данных..."),
        (user_ids[3], "Машинное обучение", "Введение в концепции машинного обучения...")
    ]
    
    for user_id, title, content in posts_data:
        db.create_post(user_id, title, content)
    
    print("\n4. Получение данных:")
    
    # Все пользователи
    users = db.get_users()
    print(f"Всего пользователей: {len(users)}")
    for user in users:
        print(f"  {user['name']} ({user['email']}) - {user['age']} лет")
    
    # Посты первого пользователя
    if user_ids:
        posts = db.get_user_posts(user_ids[0])
        print(f"\nПосты пользователя {users[0]['name']}:")
        for post in posts:
            print(f"  - {post['title']}")
    
    print("\n5. Поиск постов:")
    search_results = db.search_posts("Python")
    print(f"Найдено постов с 'Python': {len(search_results)}")
    for post in search_results:
        print(f"  - {post['title']} (автор: {post['user_name']})")
    
    print("\n6. Обновление данных:")
    if user_ids:
        success = db.update_user(user_ids[0], age=29, name="Алиса Иванова (обновлено)")
        print(f"Обновление пользователя: {'успешно' if success else 'неудачно'}")
        
        updated_user = db.get_user(user_ids[0])
        print(f"Обновленные данные: {updated_user['name']}, возраст: {updated_user['age']}")
    
    print("\n7. Статистика:")
    stats = db.get_stats()
    print(f"Пользователей: {stats['users_count']}")
    print(f"Постов: {stats['posts_count']}")
    print(f"Средний возраст: {stats['avg_age']}")
    print("Топ авторов:")
    for author in stats['top_authors']:
        print(f"  {author['name']}: {author['posts_count']} постов")
    
    print("\n8. Работа с транзакциями:")
    
    def transfer_posts(from_user_id, to_user_id):
        """Перенос всех постов от одного пользователя к другому"""
        with get_db_connection(db.db_path) as conn:
            try:
                # Начинаем транзакцию
                cursor = conn.execute(
                    'UPDATE posts SET user_id = ? WHERE user_id = ?',
                    (to_user_id, from_user_id)
                )
                
                affected_rows = cursor.rowcount
                
                if affected_rows > 0:
                    conn.commit()
                    print(f"Перенесено {affected_rows} постов")
                    return True
                else:
                    print("Нет постов для переноса")
                    return False
                    
            except Exception as e:
                conn.rollback()
                print(f"Ошибка переноса постов: {e}")
                return False
    
    if len(user_ids) >= 2:
        transfer_posts(user_ids[1], user_ids[0])
    
    print("\n9. Очистка:")
    db.cleanup()

# database_examples()
```

Эта первая часть теории охватывает основные аспекты работы с внешними библиотеками. Продолжить с остальными разделами? 