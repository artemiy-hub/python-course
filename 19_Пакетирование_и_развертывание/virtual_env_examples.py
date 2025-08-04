# Виртуальные окружения в Python
import os
import sys
import subprocess
import venv
from pathlib import Path

def demonstrate_venv_concepts():
    """Демонстрация концепций виртуальных окружений"""
    print("=== Концепции виртуальных окружений ===")
    
    print("Зачем нужны виртуальные окружения:")
    reasons = [
        "1. Изоляция зависимостей между проектами",
        "2. Предотвращение конфликтов версий пакетов",
        "3. Воспроизводимость окружения",
        "4. Безопасность - не засоряем системный Python",
        "5. Возможность использования разных версий Python"
    ]
    
    for reason in reasons:
        print(f"   {reason}")
    
    print(f"\nТекущий Python интерпретатор: {sys.executable}")
    print(f"Версия Python: {sys.version}")
    print(f"Путь к site-packages: {[p for p in sys.path if 'site-packages' in p]}")

def show_current_environment():
    """Показать информацию о текущем окружении"""
    print("\n=== Информация о текущем окружении ===")
    
    # Проверяем, находимся ли в виртуальном окружении
    in_venv = sys.prefix != sys.base_prefix
    print(f"В виртуальном окружении: {in_venv}")
    
    if in_venv:
        print(f"Путь к виртуальному окружению: {sys.prefix}")
    
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version_info}")
    
    # Показываем установленные пакеты
    try:
        import pkg_resources
        installed_packages = [d for d in pkg_resources.working_set]
        print(f"Установленных пакетов: {len(installed_packages)}")
        
        # Показываем первые 10 пакетов
        print("Некоторые установленные пакеты:")
        for pkg in sorted(installed_packages, key=lambda x: x.project_name)[:10]:
            print(f"   {pkg.project_name}: {pkg.version}")
    except ImportError:
        print("pkg_resources недоступен")

def create_venv_programmatically():
    """Создание виртуального окружения программно"""
    print("\n=== Создание виртуального окружения программно ===")
    
    venv_path = Path("example_venv")
    
    # Удаляем существующее окружение, если есть
    if venv_path.exists():
        print(f"Удаление существующего окружения: {venv_path}")
        import shutil
        shutil.rmtree(venv_path)
    
    print(f"Создание виртуального окружения: {venv_path}")
    
    # Создаём виртуальное окружение
    builder = venv.EnvBuilder(
        system_site_packages=False,  # Не использовать системные пакеты
        clear=True,                  # Очистить если существует
        symlinks=False,              # Не использовать символические ссылки
        upgrade=False,               # Не обновлять pip
        with_pip=True                # Установить pip
    )
    
    builder.create(venv_path)
    print(f"Виртуальное окружение создано в: {venv_path.absolute()}")
    
    # Пути к исполняемым файлам
    if os.name == 'nt':  # Windows
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
        activate_script = venv_path / "Scripts" / "activate.bat"
    else:  # Unix/Linux/Mac
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
        activate_script = venv_path / "bin" / "activate"
    
    print(f"Python в окружении: {python_exe}")
    print(f"pip в окружении: {pip_exe}")
    print(f"Скрипт активации: {activate_script}")
    
    return venv_path, python_exe, pip_exe

def demonstrate_pip_operations(python_exe, pip_exe):
    """Демонстрация операций pip в виртуальном окружении"""
    print("\n=== Операции pip в виртуальном окружении ===")
    
    try:
        # Обновляем pip
        print("Обновление pip...")
        subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        
        # Устанавливаем пакет
        print("Установка пакета requests...")
        result = subprocess.run([str(pip_exe), "install", "requests"], 
                              check=True, capture_output=True, text=True)
        print(f"Установка завершена: {result.returncode == 0}")
        
        # Показываем установленные пакеты
        print("Список установленных пакетов:")
        result = subprocess.run([str(pip_exe), "list"], 
                              capture_output=True, text=True)
        print(result.stdout)
        
        # Создаём requirements.txt
        print("Создание requirements.txt...")
        result = subprocess.run([str(pip_exe), "freeze"], 
                              capture_output=True, text=True)
        
        requirements_path = Path("example_requirements.txt")
        with open(requirements_path, 'w') as f:
            f.write(result.stdout)
        
        print(f"requirements.txt создан: {requirements_path}")
        print("Содержимое:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")

def demonstrate_different_venv_tools():
    """Демонстрация различных инструментов для виртуальных окружений"""
    print("\n=== Различные инструменты виртуальных окружений ===")
    
    tools = {
        "venv": {
            "description": "Встроенный модуль Python 3.3+",
            "commands": [
                "python -m venv myenv",
                "source myenv/bin/activate  # Linux/Mac",
                "myenv\\Scripts\\activate   # Windows",
                "deactivate"
            ],
            "pros": ["Встроенный", "Лёгкий", "Стандартный"],
            "cons": ["Базовая функциональность"]
        },
        "virtualenv": {
            "description": "Внешний пакет с дополнительными возможностями",
            "commands": [
                "pip install virtualenv",
                "virtualenv myenv",
                "source myenv/bin/activate",
                "deactivate"
            ],
            "pros": ["Больше возможностей", "Поддержка Python 2.7"],
            "cons": ["Требует установки"]
        },
        "pipenv": {
            "description": "Высокоуровневый инструмент управления зависимостями",
            "commands": [
                "pip install pipenv",
                "pipenv install",
                "pipenv shell",
                "pipenv install requests",
                "pipenv lock"
            ],
            "pros": ["Автоматическое управление", "Pipfile", "Безопасность"],
            "cons": ["Медленнее", "Сложнее для простых проектов"]
        },
        "conda": {
            "description": "Менеджер пакетов и окружений Anaconda",
            "commands": [
                "conda create -n myenv python=3.9",
                "conda activate myenv",
                "conda install numpy",
                "conda deactivate"
            ],
            "pros": ["Научные пакеты", "Управление Python версиями"],
            "cons": ["Большой размер", "Отдельная экосистема"]
        },
        "poetry": {
            "description": "Современный инструмент управления зависимостями",
            "commands": [
                "pip install poetry",
                "poetry init",
                "poetry add requests",
                "poetry shell",
                "poetry install"
            ],
            "pros": ["Современный", "pyproject.toml", "Автоматическое разрешение"],
            "cons": ["Новее, меньше поддержки в старых системах"]
        }
    }
    
    for tool_name, info in tools.items():
        print(f"\n{tool_name.upper()}:")
        print(f"   Описание: {info['description']}")
        print("   Основные команды:")
        for cmd in info['commands']:
            print(f"      {cmd}")
        print(f"   Плюсы: {', '.join(info['pros'])}")
        print(f"   Минусы: {', '.join(info['cons'])}")

def demonstrate_environment_variables():
    """Демонстрация переменных окружения"""
    print("\n=== Переменные окружения для Python ===")
    
    important_vars = {
        "VIRTUAL_ENV": "Путь к активному виртуальному окружению",
        "PYTHONPATH": "Дополнительные пути для поиска модулей", 
        "PYTHONHOME": "Альтернативный путь к Python",
        "PYTHONDONTWRITEBYTECODE": "Отключение создания .pyc файлов",
        "PYTHONUNBUFFERED": "Отключение буферизации вывода",
        "PIP_INDEX_URL": "URL индекса для pip",
        "PIP_TRUSTED_HOST": "Доверенные хосты для pip"
    }
    
    for var, description in important_vars.items():
        value = os.environ.get(var, "не установлена")
        print(f"   {var}: {description}")
        print(f"      Текущее значение: {value}")

def demonstrate_best_practices():
    """Лучшие практики работы с виртуальными окружениями"""
    print("\n=== Лучшие практики ===")
    
    practices = [
        "1. Всегда используйте виртуальные окружения для проектов",
        "2. Создавайте requirements.txt или pyproject.toml",
        "3. Добавляйте виртуальные окружения в .gitignore",
        "4. Используйте осмысленные имена для окружений",
        "5. Регулярно обновляйте зависимости",
        "6. Используйте один инструмент на проект",
        "7. Документируйте требования к Python версии",
        "8. Тестируйте в чистом окружении перед релизом",
        "9. Используйте pip-tools для закрепления версий",
        "10. Настройте автоматическую активацию в IDE"
    ]
    
    for practice in practices:
        print(f"   {practice}")

def create_project_structure():
    """Создание структуры проекта с виртуальным окружением"""
    print("\n=== Создание структуры проекта ===")
    
    project_structure = """
    my_project/
    ├── venv/                    # Виртуальное окружение
    ├── src/
    │   └── my_package/
    │       ├── __init__.py
    │       └── main.py
    ├── tests/
    │   └── test_main.py
    ├── requirements.txt         # Зависимости
    ├── requirements-dev.txt     # Зависимости для разработки
    ├── .gitignore              # Git игнорирование
    ├── README.md               # Документация
    └── setup.py                # Установочный скрипт
    """
    
    print("Рекомендуемая структура проекта:")
    print(project_structure)
    
    # Создаём пример .gitignore
    gitignore_content = """
# Виртуальные окружения
venv/
env/
ENV/
.venv/
.env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""
    
    print("Пример .gitignore для Python проекта:")
    print(gitignore_content)

def demonstrate_troubleshooting():
    """Демонстрация решения проблем"""
    print("\n=== Решение проблем ===")
    
    problems_solutions = {
        "Команда 'python' не найдена": [
            "Проверьте установку Python",
            "Добавьте Python в PATH",
            "Используйте python3 вместо python"
        ],
        "pip не устанавливает пакеты": [
            "Обновите pip: python -m pip install --upgrade pip",
            "Проверьте права доступа",
            "Используйте --user флаг",
            "Проверьте сетевое соединение"
        ],
        "Конфликты зависимостей": [
            "Создайте новое чистое окружение",
            "Используйте pip-tools или poetry",
            "Закрепите версии в requirements.txt",
            "Проверьте совместимость пакетов"
        ],
        "Окружение не активируется": [
            "Проверьте путь к скрипту активации",
            "Используйте правильную команду для вашей ОС",
            "Проверьте права доступа к файлам",
            "Пересоздайте окружение"
        ]
    }
    
    for problem, solutions in problems_solutions.items():
        print(f"\nПроблема: {problem}")
        print("Решения:")
        for solution in solutions:
            print(f"   - {solution}")

def cleanup_example_files():
    """Очистка примеров файлов"""
    print("\n=== Очистка ===")
    
    files_to_remove = [
        "example_requirements.txt",
        "example_venv"
    ]
    
    for item in files_to_remove:
        path = Path(item)
        if path.exists():
            if path.is_dir():
                import shutil
                shutil.rmtree(path)
                print(f"Удалена папка: {item}")
            else:
                path.unlink()
                print(f"Удален файл: {item}")

if __name__ == "__main__":
    try:
        print("Демонстрация виртуальных окружений Python")
        print("=" * 60)
        
        demonstrate_venv_concepts()
        show_current_environment()
        
        # Создание и работа с виртуальным окружением
        venv_path, python_exe, pip_exe = create_venv_programmatically()
        demonstrate_pip_operations(python_exe, pip_exe)
        
        demonstrate_different_venv_tools()
        demonstrate_environment_variables()
        demonstrate_best_practices()
        create_project_structure()
        demonstrate_troubleshooting()
        
        print("\n=== Команды для быстрого старта ===")
        quick_start = [
            "# Создание виртуального окружения",
            "python -m venv myproject_env",
            "",
            "# Активация (Linux/Mac)",
            "source myproject_env/bin/activate",
            "",
            "# Активация (Windows)",
            "myproject_env\\Scripts\\activate",
            "",
            "# Установка зависимостей",
            "pip install -r requirements.txt",
            "",
            "# Работа с проектом",
            "python main.py",
            "",
            "# Деактивация",
            "deactivate"
        ]
        
        for cmd in quick_start:
            print(cmd)
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    finally:
        # Очистка (раскомментируйте для удаления файлов)
        # cleanup_example_files()
        print(f"\nПример файлы сохранены для изучения")
        print("Для очистки запустите функцию cleanup_example_files()") 