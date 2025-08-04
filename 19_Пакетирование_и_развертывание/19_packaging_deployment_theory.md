# Теория: Пакетирование и развертывание Python приложений

## 🎯 Цель раздела

Этот раздел охватывает все аспекты пакетирования и развертывания Python приложений: от создания виртуальных окружений до контейнеризации с Docker и развертывания в облаке.

## 📋 Содержание

1. [Виртуальные окружения](#виртуальные-окружения)
2. [Управление зависимостями](#управление-зависимостями)
3. [Создание пакетов Python](#создание-пакетов-python)
4. [Контейнеризация с Docker](#контейнеризация-с-docker)
5. [CI/CD процессы](#cicd-процессы)
6. [Облачное развертывание](#облачное-развертывание)
7. [Мониторинг и логирование](#мониторинг-и-логирование)

---

## 🌍 Виртуальные окружения

Виртуальные окружения изолируют зависимости проектов и предотвращают конфликты версий.

### Встроенный venv

```python
"""
Создание и управление виртуальными окружениями с venv
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
import json

class VenvManager:
    """Менеджер виртуальных окружений"""
    
    def __init__(self, base_dir: str = "venvs"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def create_venv(self, name: str, python_version: str = None) -> bool:
        """Создание виртуального окружения"""
        venv_path = self.base_dir / name
        
        if venv_path.exists():
            print(f"Виртуальное окружение {name} уже существует")
            return False
        
        try:
            # Определяем интерпретатор Python
            python_executable = python_version or sys.executable
            
            # Создаем виртуальное окружение
            subprocess.run([
                python_executable, "-m", "venv", str(venv_path)
            ], check=True)
            
            print(f"Виртуальное окружение {name} создано успешно")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Ошибка создания виртуального окружения: {e}")
            return False
    
    def list_venvs(self) -> List[Dict[str, str]]:
        """Список всех виртуальных окружений"""
        venvs = []
        
        for venv_dir in self.base_dir.iterdir():
            if venv_dir.is_dir():
                # Проверяем, является ли это виртуальным окружением
                python_path = self._get_python_path(venv_dir)
                if python_path and python_path.exists():
                    venvs.append({
                        'name': venv_dir.name,
                        'path': str(venv_dir),
                        'python': str(python_path),
                        'active': self._is_active(venv_dir)
                    })
        
        return venvs
    
    def delete_venv(self, name: str) -> bool:
        """Удаление виртуального окружения"""
        venv_path = self.base_dir / name
        
        if not venv_path.exists():
            print(f"Виртуальное окружение {name} не найдено")
            return False
        
        try:
            import shutil
            shutil.rmtree(venv_path)
            print(f"Виртуальное окружение {name} удалено")
            return True
        except Exception as e:
            print(f"Ошибка удаления: {e}")
            return False
    
    def get_activation_command(self, name: str) -> Optional[str]:
        """Получение команды активации"""
        venv_path = self.base_dir / name
        
        if not venv_path.exists():
            return None
        
        if os.name == 'nt':  # Windows
            activate_path = venv_path / "Scripts" / "activate.bat"
            return f"{activate_path}"
        else:  # Unix/Linux/macOS
            activate_path = venv_path / "bin" / "activate"
            return f"source {activate_path}"
    
    def _get_python_path(self, venv_dir: Path) -> Optional[Path]:
        """Получение пути к Python в виртуальном окружении"""
        if os.name == 'nt':  # Windows
            return venv_dir / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            return venv_dir / "bin" / "python"
    
    def _is_active(self, venv_dir: Path) -> bool:
        """Проверка, активно ли виртуальное окружение"""
        current_prefix = getattr(sys, 'prefix', '')
        return str(venv_dir) in current_prefix

# Практический пример использования
def demonstrate_venv_management():
    """Демонстрация управления виртуальными окружениями"""
    
    manager = VenvManager()
    
    # Создаем виртуальные окружения для разных проектов
    projects = [
        "web_app",
        "data_analysis", 
        "ml_project",
        "api_service"
    ]
    
    for project in projects:
        print(f"\n📦 Создание окружения для {project}...")
        if manager.create_venv(project):
            activation_cmd = manager.get_activation_command(project)
            print(f"💡 Для активации используйте: {activation_cmd}")
    
    # Показываем список окружений
    print("\n📋 Список виртуальных окружений:")
    venvs = manager.list_venvs()
    for venv in venvs:
        status = "🟢 Активно" if venv['active'] else "⚪ Неактивно"
        print(f"  {venv['name']}: {status}")
        print(f"    Путь: {venv['path']}")
        print(f"    Python: {venv['python']}")

# Продвинутый менеджер окружений
class AdvancedEnvironmentManager:
    """Продвинутый менеджер окружений с дополнительными возможностями"""
    
    def __init__(self, config_file: str = "environments.json"):
        self.config_file = Path(config_file)
        self.environments = self._load_config()
    
    def _load_config(self) -> Dict[str, Dict]:
        """Загрузка конфигурации окружений"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        """Сохранение конфигурации"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.environments, f, indent=2, ensure_ascii=False)
    
    def create_project_environment(self, project_name: str, 
                                 python_version: str = None,
                                 requirements: List[str] = None,
                                 description: str = "") -> bool:
        """Создание окружения для проекта с метаданными"""
        
        # Создаем виртуальное окружение
        venv_manager = VenvManager()
        if not venv_manager.create_venv(project_name, python_version):
            return False
        
        # Сохраняем метаданные
        self.environments[project_name] = {
            'description': description,
            'python_version': python_version or sys.version,
            'created_at': str(datetime.now()),
            'requirements': requirements or [],
            'status': 'active'
        }
        
        # Устанавливаем зависимости если указаны
        if requirements:
            self._install_requirements(project_name, requirements)
        
        self._save_config()
        return True
    
    def _install_requirements(self, project_name: str, requirements: List[str]):
        """Установка зависимостей в виртуальное окружение"""
        venv_path = Path("venvs") / project_name
        
        if os.name == 'nt':
            pip_path = venv_path / "Scripts" / "pip.exe"
        else:
            pip_path = venv_path / "bin" / "pip"
        
        try:
            for requirement in requirements:
                subprocess.run([
                    str(pip_path), "install", requirement
                ], check=True, capture_output=True)
            
            print(f"✅ Зависимости установлены в {project_name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки зависимостей: {e}")
    
    def export_requirements(self, project_name: str, output_file: str = None) -> bool:
        """Экспорт зависимостей в requirements.txt"""
        if project_name not in self.environments:
            print(f"Проект {project_name} не найден")
            return False
        
        venv_path = Path("venvs") / project_name
        
        if os.name == 'nt':
            pip_path = venv_path / "Scripts" / "pip.exe"
        else:
            pip_path = venv_path / "bin" / "pip"
        
        output_file = output_file or f"{project_name}_requirements.txt"
        
        try:
            result = subprocess.run([
                str(pip_path), "freeze"
            ], check=True, capture_output=True, text=True)
            
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            print(f"📄 Зависимости экспортированы в {output_file}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка экспорта: {e}")
            return False
    
    def clone_environment(self, source_project: str, target_project: str) -> bool:
        """Клонирование окружения"""
        if source_project not in self.environments:
            print(f"Исходный проект {source_project} не найден")
            return False
        
        # Экспортируем зависимости исходного проекта
        temp_requirements = f"temp_{source_project}_req.txt"
        if not self.export_requirements(source_project, temp_requirements):
            return False
        
        try:
            # Читаем зависимости
            with open(temp_requirements, 'r') as f:
                requirements = [line.strip() for line in f if line.strip()]
            
            # Создаем новое окружение
            source_config = self.environments[source_project]
            success = self.create_project_environment(
                target_project,
                python_version=source_config.get('python_version'),
                requirements=requirements,
                description=f"Клон проекта {source_project}"
            )
            
            # Удаляем временный файл
            os.unlink(temp_requirements)
            
            return success
            
        except Exception as e:
            print(f"❌ Ошибка клонирования: {e}")
            if os.path.exists(temp_requirements):
                os.unlink(temp_requirements)
            return False
    
    def get_project_info(self, project_name: str) -> Optional[Dict]:
        """Получение информации о проекте"""
        if project_name not in self.environments:
            return None
        
        config = self.environments[project_name].copy()
        
        # Добавляем информацию о текущих зависимостях
        venv_path = Path("venvs") / project_name
        if venv_path.exists():
            if os.name == 'nt':
                pip_path = venv_path / "Scripts" / "pip.exe"
            else:
                pip_path = venv_path / "bin" / "pip"
            
            try:
                result = subprocess.run([
                    str(pip_path), "list", "--format=json"
                ], capture_output=True, text=True, check=True)
                
                installed_packages = json.loads(result.stdout)
                config['installed_packages'] = installed_packages
                
            except (subprocess.CalledProcessError, json.JSONDecodeError):
                config['installed_packages'] = []
        
        return config

# Сравнение инструментов управления окружениями
class EnvironmentToolsComparison:
    """Сравнение различных инструментов управления окружениями"""
    
    @staticmethod
    def compare_tools():
        """Сравнение популярных инструментов"""
        
        tools_comparison = {
            'venv': {
                'плюсы': [
                    'Встроен в Python 3.3+',
                    'Простота использования',
                    'Стандартное решение',
                    'Нет зависимостей'
                ],
                'минусы': [
                    'Только Python окружения',
                    'Нет управления версиями Python',
                    'Базовая функциональность'
                ],
                'использование': 'Простые проекты, начинающие'
            },
            
            'virtualenv': {
                'плюсы': [
                    'Работает с Python 2.7+',
                    'Больше возможностей чем venv',
                    'Совместимость со старыми версиями'
                ],
                'минусы': [
                    'Внешняя зависимость',
                    'Дублирует функциональность venv'
                ],
                'использование': 'Проекты с Python < 3.3'
            },
            
            'conda': {
                'плюсы': [
                    'Управление любыми пакетами (не только Python)',
                    'Разные версии Python',
                    'Отличная поддержка Data Science',
                    'Бинарные зависимости'
                ],
                'минусы': [
                    'Большой размер',
                    'Медленное разрешение зависимостей',
                    'Избыточность для простых проектов'
                ],
                'использование': 'Data Science, ML, научные вычисления'
            },
            
            'pipenv': {
                'плюсы': [
                    'Pipfile вместо requirements.txt',
                    'Автоматическое создание venv',
                    'Определение зависимостей разработки',
                    'Графы зависимостей'
                ],
                'минусы': [
                    'Медленное разрешение зависимостей',
                    'Сложности с некоторыми пакетами',
                    'Менее предсказуемое поведение'
                ],
                'использование': 'Средние и крупные проекты'
            },
            
            'poetry': {
                'плюсы': [
                    'Современное управление зависимостями',
                    'Создание и публикация пакетов',
                    'Быстрое разрешение зависимостей',
                    'Детерминированные сборки'
                ],
                'минусы': [
                    'Кривая обучения',
                    'Не все пакеты совместимы',
                    'Относительно новый инструмент'
                ],
                'использование': 'Современные проекты, библиотеки'
            }
        }
        
        return tools_comparison
    
    @staticmethod
    def print_comparison():
        """Вывод сравнения инструментов"""
        comparison = EnvironmentToolsComparison.compare_tools()
        
        for tool, info in comparison.items():
            print(f"\n🔧 {tool.upper()}")
            print("=" * 40)
            
            print("✅ Плюсы:")
            for plus in info['плюсы']:
                print(f"  • {plus}")
            
            print("\n❌ Минусы:")
            for minus in info['минусы']:
                print(f"  • {minus}")
            
            print(f"\n🎯 Лучше всего для: {info['использование']}")
```

---

## 📦 Управление зависимостями

Современные подходы к управлению зависимостями в Python проектах.

### Poetry - современный менеджер

```python
"""
Управление зависимостями с Poetry
"""

import subprocess
import toml
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

class PoetryManager:
    """Менеджер для работы с Poetry"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.pyproject_path = self.project_path / "pyproject.toml"
    
    def init_project(self, name: str, version: str = "0.1.0", 
                    description: str = "", author: str = "") -> bool:
        """Инициализация нового проекта Poetry"""
        try:
            cmd = ["poetry", "init", "--no-interaction"]
            
            if name:
                cmd.extend(["--name", name])
            if version:
                cmd.extend(["--version", version])
            if description:
                cmd.extend(["--description", description])
            if author:
                cmd.extend(["--author", author])
            
            subprocess.run(cmd, cwd=self.project_path, check=True)
            print(f"✅ Проект {name} инициализирован")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка инициализации: {e}")
            return False
    
    def add_dependency(self, package: str, group: str = "main", 
                      dev: bool = False) -> bool:
        """Добавление зависимости"""
        try:
            cmd = ["poetry", "add", package]
            
            if dev:
                cmd.append("--group=dev")
            elif group != "main":
                cmd.extend(["--group", group])
            
            subprocess.run(cmd, cwd=self.project_path, check=True)
            print(f"✅ Зависимость {package} добавлена")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка добавления зависимости: {e}")
            return False
    
    def remove_dependency(self, package: str, group: str = "main") -> bool:
        """Удаление зависимости"""
        try:
            cmd = ["poetry", "remove", package]
            
            if group != "main":
                cmd.extend(["--group", group])
            
            subprocess.run(cmd, cwd=self.project_path, check=True)
            print(f"✅ Зависимость {package} удалена")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка удаления зависимости: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """Установка всех зависимостей"""
        try:
            subprocess.run(
                ["poetry", "install"], 
                cwd=self.project_path, 
                check=True
            )
            print("✅ Все зависимости установлены")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки зависимостей: {e}")
            return False
    
    def update_dependencies(self) -> bool:
        """Обновление зависимостей"""
        try:
            subprocess.run(
                ["poetry", "update"], 
                cwd=self.project_path, 
                check=True
            )
            print("✅ Зависимости обновлены")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка обновления зависимостей: {e}")
            return False
    
    def show_dependencies(self) -> Optional[Dict[str, Any]]:
        """Показать информацию о зависимостях"""
        try:
            result = subprocess.run(
                ["poetry", "show", "--tree"], 
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"tree": result.stdout}
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка получения информации: {e}")
            return None
    
    def export_requirements(self, output_file: str = "requirements.txt",
                          include_dev: bool = False) -> bool:
        """Экспорт в requirements.txt формат"""
        try:
            cmd = ["poetry", "export", "-f", "requirements.txt", 
                   "--output", output_file]
            
            if include_dev:
                cmd.append("--with=dev")
            
            subprocess.run(cmd, cwd=self.project_path, check=True)
            print(f"✅ Зависимости экспортированы в {output_file}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка экспорта: {e}")
            return False
    
    def build_package(self) -> bool:
        """Сборка пакета"""
        try:
            subprocess.run(
                ["poetry", "build"], 
                cwd=self.project_path, 
                check=True
            )
            print("✅ Пакет собран")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка сборки пакета: {e}")
            return False
    
    def publish_package(self, repository: str = None) -> bool:
        """Публикация пакета"""
        try:
            cmd = ["poetry", "publish"]
            
            if repository:
                cmd.extend(["--repository", repository])
            
            subprocess.run(cmd, cwd=self.project_path, check=True)
            print("✅ Пакет опубликован")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка публикации: {e}")
            return False
    
    def read_pyproject_toml(self) -> Optional[Dict[str, Any]]:
        """Чтение pyproject.toml"""
        if not self.pyproject_path.exists():
            return None
        
        try:
            with open(self.pyproject_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        except Exception as e:
            print(f"❌ Ошибка чтения pyproject.toml: {e}")
            return None
    
    def write_pyproject_toml(self, config: Dict[str, Any]) -> bool:
        """Запись pyproject.toml"""
        try:
            with open(self.pyproject_path, 'w', encoding='utf-8') as f:
                toml.dump(config, f)
            return True
        except Exception as e:
            print(f"❌ Ошибка записи pyproject.toml: {e}")
            return False

# Продвинутая конфигурация Poetry проекта
class PoetryProjectTemplate:
    """Шаблон для создания Poetry проектов"""
    
    @staticmethod
    def create_web_app_project(name: str, path: str = ".") -> Dict[str, Any]:
        """Шаблон для веб-приложения"""
        return {
            "tool": {
                "poetry": {
                    "name": name,
                    "version": "0.1.0",
                    "description": "Modern web application",
                    "authors": ["Your Name <your.email@example.com>"],
                    "readme": "README.md",
                    "packages": [{"include": name.replace("-", "_")}],
                    
                    "dependencies": {
                        "python": "^3.9",
                        "fastapi": "^0.104.0",
                        "uvicorn": {
                            "extras": ["standard"],
                            "version": "^0.24.0"
                        },
                        "pydantic": "^2.5.0",
                        "sqlalchemy": "^2.0.0",
                        "alembic": "^1.13.0",
                        "python-multipart": "^0.0.6",
                        "python-jose": {
                            "extras": ["cryptography"],
                            "version": "^3.3.0"
                        },
                        "passlib": {
                            "extras": ["bcrypt"],
                            "version": "^1.7.4"
                        }
                    },
                    
                    "group": {
                        "dev": {
                            "dependencies": {
                                "pytest": "^7.4.0",
                                "pytest-asyncio": "^0.21.0",
                                "httpx": "^0.25.0",
                                "black": "^23.0.0",
                                "isort": "^5.12.0",
                                "flake8": "^6.0.0",
                                "mypy": "^1.7.0",
                                "pre-commit": "^3.5.0"
                            }
                        },
                        "test": {
                            "dependencies": {
                                "pytest-cov": "^4.1.0",
                                "pytest-mock": "^3.12.0",
                                "factory-boy": "^3.3.0"
                            }
                        }
                    },
                    
                    "scripts": {
                        "start": "uvicorn main:app --reload",
                        "test": "pytest",
                        "lint": "flake8 .",
                        "format": "black . && isort .",
                        "typecheck": "mypy ."
                    }
                }
            },
            
            "build-system": {
                "requires": ["poetry-core"],
                "build-backend": "poetry.core.masonry.api"
            }
        }
    
    @staticmethod
    def create_data_science_project(name: str) -> Dict[str, Any]:
        """Шаблон для Data Science проекта"""
        return {
            "tool": {
                "poetry": {
                    "name": name,
                    "version": "0.1.0",
                    "description": "Data Science project",
                    "authors": ["Your Name <your.email@example.com>"],
                    
                    "dependencies": {
                        "python": "^3.9",
                        "pandas": "^2.1.0",
                        "numpy": "^1.24.0",
                        "matplotlib": "^3.8.0",
                        "seaborn": "^0.13.0",
                        "scikit-learn": "^1.3.0",
                        "jupyter": "^1.0.0",
                        "plotly": "^5.17.0",
                        "requests": "^2.31.0"
                    },
                    
                    "group": {
                        "dev": {
                            "dependencies": {
                                "pytest": "^7.4.0",
                                "black": "^23.0.0",
                                "isort": "^5.12.0",
                                "flake8": "^6.0.0",
                                "jupyter-black": "^0.3.4"
                            }
                        },
                        "ml": {
                            "dependencies": {
                                "tensorflow": "^2.14.0",
                                "torch": "^2.1.0",
                                "transformers": "^4.35.0",
                                "xgboost": "^2.0.0"
                            }
                        }
                    },
                    
                    "scripts": {
                        "notebook": "jupyter notebook",
                        "lab": "jupyter lab",
                        "format": "black . && isort ."
                    }
                }
            },
            
            "build-system": {
                "requires": ["poetry-core"],
                "build-backend": "poetry.core.masonry.api"
            }
        }
    
    @staticmethod
    def create_library_project(name: str) -> Dict[str, Any]:
        """Шаблон для библиотеки"""
        return {
            "tool": {
                "poetry": {
                    "name": name,
                    "version": "0.1.0",
                    "description": "Python library",
                    "authors": ["Your Name <your.email@example.com>"],
                    "license": "MIT",
                    "readme": "README.md",
                    "homepage": f"https://github.com/username/{name}",
                    "repository": f"https://github.com/username/{name}",
                    "documentation": f"https://{name}.readthedocs.io",
                    "keywords": ["python", "library"],
                    "classifiers": [
                        "Development Status :: 3 - Alpha",
                        "Intended Audience :: Developers",
                        "License :: OSI Approved :: MIT License",
                        "Programming Language :: Python :: 3",
                        "Programming Language :: Python :: 3.9",
                        "Programming Language :: Python :: 3.10",
                        "Programming Language :: Python :: 3.11"
                    ],
                    "packages": [{"include": name.replace("-", "_")}],
                    
                    "dependencies": {
                        "python": "^3.9"
                    },
                    
                    "group": {
                        "dev": {
                            "dependencies": {
                                "pytest": "^7.4.0",
                                "pytest-cov": "^4.1.0",
                                "black": "^23.0.0",
                                "isort": "^5.12.0",
                                "flake8": "^6.0.0",
                                "mypy": "^1.7.0",
                                "sphinx": "^7.2.0",
                                "sphinx-rtd-theme": "^1.3.0"
                            }
                        }
                    },
                    
                    "scripts": {
                        "test": "pytest --cov",
                        "docs": "sphinx-build -b html docs docs/_build",
                        "format": "black . && isort .",
                        "lint": "flake8 . && mypy .",
                        "publish": "poetry publish --build"
                    }
                }
            },
            
            "tool": {
                "black": {
                    "line-length": 88,
                    "target-version": ["py39"]
                },
                "isort": {
                    "profile": "black",
                    "multi_line_output": 3
                },
                "mypy": {
                    "python_version": "3.9",
                    "warn_return_any": True,
                    "warn_unused_configs": True,
                    "disallow_untyped_defs": True
                },
                "pytest": {
                    "ini_options": {
                        "testpaths": ["tests"],
                        "python_files": ["test_*.py"],
                        "python_classes": ["Test*"],
                        "python_functions": ["test_*"],
                        "addopts": "--strict-markers --strict-config --verbose"
                    }
                }
            },
            
            "build-system": {
                "requires": ["poetry-core"],
                "build-backend": "poetry.core.masonry.api"
            }
        }

# Управление зависимостями в команде
class TeamDependencyManager:
    """Управление зависимостями в команде разработки"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.lock_file = self.project_path / "poetry.lock"
    
    def check_lock_file_sync(self) -> bool:
        """Проверка синхронизации lock файла"""
        try:
            result = subprocess.run(
                ["poetry", "check"], 
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ poetry.lock синхронизирован с pyproject.toml")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ poetry.lock не синхронизирован: {e.stderr}")
            return False
    
    def generate_requirements_for_deployment(self) -> bool:
        """Генерация requirements.txt для развертывания"""
        poetry_manager = PoetryManager(self.project_path)
        
        # Основные зависимости
        if not poetry_manager.export_requirements("requirements.txt"):
            return False
        
        # Зависимости разработки
        if not poetry_manager.export_requirements(
            "requirements-dev.txt", 
            include_dev=True
        ):
            return False
        
        print("✅ Requirements файлы созданы для развертывания")
        return True
    
    def audit_dependencies(self) -> Dict[str, Any]:
        """Аудит безопасности зависимостей"""
        try:
            # Используем safety для проверки безопасности
            result = subprocess.run(
                ["poetry", "run", "safety", "check", "--json"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {"status": "safe", "vulnerabilities": []}
            else:
                vulnerabilities = json.loads(result.stdout)
                return {
                    "status": "vulnerable", 
                    "vulnerabilities": vulnerabilities
                }
                
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return {"status": "error", "message": "Не удалось выполнить аудит"}
    
    def update_outdated_dependencies(self) -> List[str]:
        """Обновление устаревших зависимостей"""
        try:
            # Получаем список устаревших пакетов
            result = subprocess.run(
                ["poetry", "show", "--outdated"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            outdated_packages = []
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('!'):
                    package_name = line.split()[0]
                    outdated_packages.append(package_name)
            
            return outdated_packages
            
        except subprocess.CalledProcessError:
            return []
```

---

## 🏗️ Создание пакетов Python

Создание и публикация собственных Python пакетов.

### Структура пакета

```python
"""
Создание профессиональных Python пакетов
"""

from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import tempfile
import shutil

class PythonPackageGenerator:
    """Генератор структуры Python пакетов"""
    
    def __init__(self, package_name: str, author: str, email: str):
        self.package_name = package_name
        self.author = author
        self.email = email
        self.module_name = package_name.replace("-", "_")
    
    def create_package_structure(self, target_dir: str = None) -> Path:
        """Создание полной структуры пакета"""
        
        if target_dir is None:
            target_dir = self.package_name
        
        package_path = Path(target_dir)
        package_path.mkdir(exist_ok=True)
        
        # Создаем основные директории
        self._create_source_structure(package_path)
        self._create_tests_structure(package_path)
        self._create_docs_structure(package_path)
        self._create_config_files(package_path)
        
        print(f"✅ Структура пакета {self.package_name} создана в {package_path}")
        return package_path
    
    def _create_source_structure(self, package_path: Path):
        """Создание структуры исходного кода"""
        src_path = package_path / "src" / self.module_name
        src_path.mkdir(parents=True, exist_ok=True)
        
        # __init__.py
        init_content = f'''"""
{self.package_name}: A Python package
"""

__version__ = "0.1.0"
__author__ = "{self.author}"
__email__ = "{self.email}"

from .core import main_function
from .utils import helper_function

__all__ = ["main_function", "helper_function"]
'''
        (src_path / "__init__.py").write_text(init_content)
        
        # core.py - основная функциональность
        core_content = '''"""
Core functionality of the package
"""

from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def main_function(data: Any) -> Dict[str, Any]:
    """
    Main function of the package.
    
    Args:
        data: Input data to process
        
    Returns:
        Dictionary with processed results
        
    Examples:
        >>> result = main_function("test")
        >>> print(result['status'])
        success
    """
    logger.info(f"Processing data: {data}")
    
    return {
        "status": "success",
        "data": data,
        "processed": True
    }


class MainClass:
    """
    Main class for advanced functionality.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the main class.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_level = self.config.get('log_level', 'INFO')
        logging.basicConfig(level=getattr(logging, log_level))
    
    def process(self, items: List[Any]) -> List[Dict[str, Any]]:
        """
        Process a list of items.
        
        Args:
            items: List of items to process
            
        Returns:
            List of processed results
        """
        results = []
        
        for item in items:
            try:
                result = main_function(item)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing item {item}: {e}")
                results.append({
                    "status": "error",
                    "data": item,
                    "error": str(e)
                })
        
        return results
'''
        (src_path / "core.py").write_text(core_content)
        
        # utils.py - вспомогательные функции
        utils_content = '''"""
Utility functions for the package
"""

from typing import Any, Dict, List, Union
import json
import os
from pathlib import Path


def helper_function(value: Union[str, int, float]) -> str:
    """
    Helper function for data conversion.
    
    Args:
        value: Value to convert
        
    Returns:
        String representation of the value
    """
    return f"processed_{value}"


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is not valid JSON
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config: Dict[str, Any], config_path: Union[str, Path]) -> bool:
    """
    Save configuration to a JSON file.
    
    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the config
        
    Returns:
        True if successful, False otherwise
    """
    try:
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception:
        return False


def validate_input(data: Any, required_fields: List[str]) -> bool:
    """
    Validate input data structure.
    
    Args:
        data: Data to validate
        required_fields: List of required field names
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    return all(field in data for field in required_fields)


class FileManager:
    """
    File management utilities.
    """
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> Path:
        """
        Ensure directory exists, create if necessary.
        
        Args:
            path: Directory path
            
        Returns:
            Path object of the directory
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def cleanup_temp_files(temp_dir: Union[str, Path], 
                          pattern: str = "*.tmp") -> int:
        """
        Clean up temporary files in a directory.
        
        Args:
            temp_dir: Directory to clean
            pattern: File pattern to match
            
        Returns:
            Number of files deleted
        """
        temp_dir = Path(temp_dir)
        deleted_count = 0
        
        for file_path in temp_dir.glob(pattern):
            try:
                file_path.unlink()
                deleted_count += 1
            except OSError:
                pass  # Ignore errors
        
        return deleted_count
'''
        (src_path / "utils.py").write_text(utils_content)
        
        # cli.py - интерфейс командной строки
        cli_content = '''"""
Command line interface for the package
"""

import argparse
import sys
from typing import Optional, List
import json

from .core import main_function, MainClass
from .utils import load_config, save_config


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description=f"{__package__} command line interface",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"{__package__} {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process data")
    process_parser.add_argument(
        "data", 
        help="Data to process"
    )
    process_parser.add_argument(
        "--config", 
        help="Configuration file path"
    )
    process_parser.add_argument(
        "--output", 
        help="Output file path"
    )
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch process multiple items")
    batch_parser.add_argument(
        "items", 
        nargs="+", 
        help="Items to process"
    )
    batch_parser.add_argument(
        "--config", 
        help="Configuration file path"
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for CLI.
    
    Args:
        argv: Command line arguments
        
    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Load configuration if provided
        config = {}
        if hasattr(args, 'config') and args.config:
            config = load_config(args.config)
        
        if args.command == "process":
            result = main_function(args.data)
            
            if args.output:
                save_config(result, args.output)
                print(f"Result saved to {args.output}")
            else:
                print(json.dumps(result, indent=2))
        
        elif args.command == "batch":
            processor = MainClass(config)
            results = processor.process(args.items)
            
            print(json.dumps(results, indent=2))
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
'''
        (src_path / "cli.py").write_text(cli_content)
    
    def _create_tests_structure(self, package_path: Path):
        """Создание структуры тестов"""
        tests_path = package_path / "tests"
        tests_path.mkdir(exist_ok=True)
        
        # __init__.py для tests
        (tests_path / "__init__.py").write_text("")
        
        # conftest.py - конфигурация pytest
        conftest_content = '''"""
Test configuration and fixtures
"""

import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any

from src.''' + self.module_name + '''.core import MainClass


@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return {
        "name": "test_item",
        "value": 42,
        "enabled": True
    }


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "log_level": "DEBUG",
        "timeout": 30,
        "retries": 3
    }


@pytest.fixture
def main_class_instance(sample_config):
    """Instance of MainClass for testing."""
    return MainClass(sample_config)


@pytest.fixture
def temp_directory():
    """Temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def config_file(temp_directory, sample_config):
    """Temporary config file for testing."""
    import json
    
    config_path = temp_directory / "test_config.json"
    with open(config_path, 'w') as f:
        json.dump(sample_config, f)
    
    return config_path
'''
        (tests_path / "conftest.py").write_text(conftest_content)
        
        # test_core.py
        test_core_content = '''"""
Tests for core functionality
"""

import pytest
from src.''' + self.module_name + '''.core import main_function, MainClass


class TestMainFunction:
    """Tests for main_function."""
    
    def test_main_function_basic(self):
        """Test basic functionality of main_function."""
        result = main_function("test_data")
        
        assert result["status"] == "success"
        assert result["data"] == "test_data"
        assert result["processed"] is True
    
    def test_main_function_with_dict(self, sample_data):
        """Test main_function with dictionary input."""
        result = main_function(sample_data)
        
        assert result["status"] == "success"
        assert result["data"] == sample_data
        assert result["processed"] is True
    
    def test_main_function_with_none(self):
        """Test main_function with None input."""
        result = main_function(None)
        
        assert result["status"] == "success"
        assert result["data"] is None
        assert result["processed"] is True


class TestMainClass:
    """Tests for MainClass."""
    
    def test_init_without_config(self):
        """Test MainClass initialization without config."""
        instance = MainClass()
        assert instance.config == {}
    
    def test_init_with_config(self, sample_config):
        """Test MainClass initialization with config."""
        instance = MainClass(sample_config)
        assert instance.config == sample_config
    
    def test_process_single_item(self, main_class_instance):
        """Test processing single item."""
        items = ["test_item"]
        results = main_class_instance.process(items)
        
        assert len(results) == 1
        assert results[0]["status"] == "success"
        assert results[0]["data"] == "test_item"
    
    def test_process_multiple_items(self, main_class_instance):
        """Test processing multiple items."""
        items = ["item1", "item2", "item3"]
        results = main_class_instance.process(items)
        
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result["status"] == "success"
            assert result["data"] == f"item{i+1}"
    
    def test_process_empty_list(self, main_class_instance):
        """Test processing empty list."""
        results = main_class_instance.process([])
        assert results == []
    
    @pytest.mark.parametrize("items,expected_count", [
        (["a"], 1),
        (["a", "b"], 2),
        (["a", "b", "c", "d"], 4),
        ([], 0)
    ])
    def test_process_parametrized(self, main_class_instance, items, expected_count):
        """Parametrized test for process method."""
        results = main_class_instance.process(items)
        assert len(results) == expected_count
'''
        (tests_path / "test_core.py").write_text(test_core_content)
        
        # test_utils.py
        test_utils_content = '''"""
Tests for utility functions
"""

import pytest
import json
from pathlib import Path

from src.''' + self.module_name + '''.utils import (
    helper_function, 
    load_config, 
    save_config, 
    validate_input,
    FileManager
)


class TestHelperFunction:
    """Tests for helper_function."""
    
    @pytest.mark.parametrize("input_value,expected", [
        ("test", "processed_test"),
        (42, "processed_42"),
        (3.14, "processed_3.14"),
        ("", "processed_")
    ])
    def test_helper_function(self, input_value, expected):
        """Test helper function with various inputs."""
        result = helper_function(input_value)
        assert result == expected


class TestConfigFunctions:
    """Tests for configuration functions."""
    
    def test_load_config_success(self, config_file, sample_config):
        """Test successful config loading."""
        loaded_config = load_config(config_file)
        assert loaded_config == sample_config
    
    def test_load_config_file_not_found(self, temp_directory):
        """Test config loading with non-existent file."""
        non_existent_file = temp_directory / "non_existent.json"
        
        with pytest.raises(FileNotFoundError):
            load_config(non_existent_file)
    
    def test_save_config_success(self, temp_directory, sample_config):
        """Test successful config saving."""
        config_path = temp_directory / "saved_config.json"
        
        result = save_config(sample_config, config_path)
        assert result is True
        assert config_path.exists()
        
        # Verify saved content
        with open(config_path) as f:
            saved_config = json.load(f)
        assert saved_config == sample_config
    
    def test_save_config_create_directory(self, temp_directory, sample_config):
        """Test config saving with directory creation."""
        config_path = temp_directory / "subdir" / "config.json"
        
        result = save_config(sample_config, config_path)
        assert result is True
        assert config_path.exists()
        assert config_path.parent.exists()


class TestValidateInput:
    """Tests for input validation."""
    
    def test_validate_input_success(self):
        """Test successful input validation."""
        data = {"name": "test", "value": 42}
        required_fields = ["name", "value"]
        
        assert validate_input(data, required_fields) is True
    
    def test_validate_input_missing_field(self):
        """Test validation with missing field."""
        data = {"name": "test"}
        required_fields = ["name", "value"]
        
        assert validate_input(data, required_fields) is False
    
    def test_validate_input_not_dict(self):
        """Test validation with non-dict input."""
        data = "not a dict"
        required_fields = ["name"]
        
        assert validate_input(data, required_fields) is False
    
    def test_validate_input_empty_requirements(self):
        """Test validation with empty requirements."""
        data = {"name": "test"}
        required_fields = []
        
        assert validate_input(data, required_fields) is True


class TestFileManager:
    """Tests for FileManager class."""
    
    def test_ensure_directory_new(self, temp_directory):
        """Test creating new directory."""
        new_dir = temp_directory / "new_directory"
        
        result = FileManager.ensure_directory(new_dir)
        assert result == new_dir
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_ensure_directory_existing(self, temp_directory):
        """Test with existing directory."""
        result = FileManager.ensure_directory(temp_directory)
        assert result == temp_directory
        assert temp_directory.exists()
    
    def test_cleanup_temp_files(self, temp_directory):
        """Test cleanup of temporary files."""
        # Create some temp files
        (temp_directory / "file1.tmp").touch()
        (temp_directory / "file2.tmp").touch()
        (temp_directory / "file3.txt").touch()  # Not a .tmp file
        
        deleted_count = FileManager.cleanup_temp_files(temp_directory, "*.tmp")
        
        assert deleted_count == 2
        assert not (temp_directory / "file1.tmp").exists()
        assert not (temp_directory / "file2.tmp").exists()
        assert (temp_directory / "file3.txt").exists()  # Should still exist
'''
        (tests_path / "test_utils.py").write_text(test_utils_content)
    
    def _create_docs_structure(self, package_path: Path):
        """Создание структуры документации"""
        docs_path = package_path / "docs"
        docs_path.mkdir(exist_ok=True)
        
        # README.md
        readme_content = f'''# {self.package_name}

A modern Python package with best practices.

## Installation

```bash
pip install {self.package_name}
```

## Quick Start

```python
from {self.module_name} import main_function

result = main_function("your_data")
print(result)
```

## Features

- ✅ Modern Python packaging with Poetry
- ✅ Comprehensive test suite with pytest
- ✅ Type hints and mypy support
- ✅ Code formatting with Black and isort
- ✅ Linting with flake8
- ✅ Documentation with Sphinx
- ✅ CI/CD ready configuration

## Development

1. Clone the repository
2. Install dependencies: `poetry install`
3. Run tests: `poetry run pytest`
4. Format code: `poetry run black . && poetry run isort .`

## API Reference

### main_function(data)

Main function for processing data.

**Parameters:**
- `data`: Input data to process

**Returns:**
- Dictionary with processing results

## License

This project is licensed under the MIT License.
'''
        (package_path / "README.md").write_text(readme_content)
        
        # CHANGELOG.md
        changelog_content = '''# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial package structure
- Core functionality
- Comprehensive test suite
- Documentation

## [0.1.0] - 2024-01-01

### Added
- Initial release
'''
        (package_path / "CHANGELOG.md").write_text(changelog_content)
        
        # LICENSE
        license_content = '''MIT License

Copyright (c) 2024 ''' + self.author + '''

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
        (package_path / "LICENSE").write_text(license_content)
    
    def _create_config_files(self, package_path: Path):
        """Создание конфигурационных файлов"""
        
        # .gitignore
        gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
'''
        (package_path / ".gitignore").write_text(gitignore_content)
        
        # Makefile для автоматизации
        makefile_content = '''# Makefile for package development

.PHONY: help install test lint format type-check docs clean build publish

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

install:  ## Install dependencies
	poetry install

test:  ## Run tests
	poetry run pytest --cov --cov-report=html --cov-report=term

test-fast:  ## Run tests without coverage
	poetry run pytest -x -v

lint:  ## Run linting
	poetry run flake8 src tests
	poetry run mypy src

format:  ## Format code
	poetry run black src tests
	poetry run isort src tests

format-check:  ## Check code formatting
	poetry run black --check src tests
	poetry run isort --check-only src tests

type-check:  ## Run type checking
	poetry run mypy src

docs:  ## Build documentation
	cd docs && poetry run make html

docs-serve:  ## Serve documentation locally
	cd docs && poetry run python -m http.server 8000 --directory _build/html

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	poetry build

publish:  ## Publish package to PyPI
	poetry publish

publish-test:  ## Publish package to Test PyPI
	poetry publish --repository testpypi

check:  ## Run all checks
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test

pre-commit:  ## Run pre-commit checks
	$(MAKE) format
	$(MAKE) check

.DEFAULT_GOAL := help
'''
        (package_path / "Makefile").write_text(makefile_content)
        
        # tox.ini для тестирования в разных окружениях
        tox_content = '''[tox]
envlist = py39,py310,py311,lint,type

[testenv]
deps = 
    pytest
    pytest-cov
commands = pytest {posargs}

[testenv:lint]
deps = 
    flake8
    black
    isort
commands = 
    flake8 src tests
    black --check src tests
    isort --check-only src tests

[testenv:type]
deps = mypy
commands = mypy src

[testenv:docs]
deps = 
    sphinx
    sphinx-rtd-theme
commands = sphinx-build -b html docs docs/_build
'''
        (package_path / "tox.ini").write_text(tox_content)

# Автоматизация публикации пакетов
class PackagePublisher:
    """Автоматизация публикации Python пакетов"""
    
    def __init__(self, package_path: str = "."):
        self.package_path = Path(package_path)
        self.poetry_manager = PoetryManager(package_path)
    
    def pre_publish_checks(self) -> bool:
        """Предварительные проверки перед публикацией"""
        checks = []
        
        # Проверка poetry.lock синхронизации
        try:
            subprocess.run(
                ["poetry", "check"], 
                cwd=self.package_path, 
                check=True
            )
            checks.append(("✅", "Poetry configuration is valid"))
        except subprocess.CalledProcessError:
            checks.append(("❌", "Poetry configuration is invalid"))
            return False
        
        # Проверка тестов
        try:
            subprocess.run(
                ["poetry", "run", "pytest"], 
                cwd=self.package_path, 
                check=True,
                capture_output=True
            )
            checks.append(("✅", "All tests pass"))
        except subprocess.CalledProcessError:
            checks.append(("❌", "Some tests fail"))
            return False
        
        # Проверка линтера
        try:
            subprocess.run(
                ["poetry", "run", "flake8", "src"], 
                cwd=self.package_path, 
                check=True,
                capture_output=True
            )
            checks.append(("✅", "Code passes linting"))
        except subprocess.CalledProcessError:
            checks.append(("❌", "Code has linting issues"))
            return False
        
        # Проверка типов
        try:
            subprocess.run(
                ["poetry", "run", "mypy", "src"], 
                cwd=self.package_path, 
                check=True,
                capture_output=True
            )
            checks.append(("✅", "Type checking passes"))
        except subprocess.CalledProcessError:
            checks.append(("❌", "Type checking issues found"))
            return False
        
        # Вывод результатов проверок
        print("\n📋 Pre-publish checks:")
        for status, message in checks:
            print(f"  {status} {message}")
        
        return all(status == "✅" for status, _ in checks)
    
    def build_and_test_package(self) -> bool:
        """Сборка и тестирование пакета"""
        try:
            # Очистка предыдущих сборок
            subprocess.run(
                ["rm", "-rf", "dist/"], 
                cwd=self.package_path
            )
            
            # Сборка пакета
            if not self.poetry_manager.build_package():
                return False
            
            # Проверка сборки
            dist_path = self.package_path / "dist"
            if not dist_path.exists() or not list(dist_path.glob("*")):
                print("❌ No build artifacts found")
                return False
            
            print("✅ Package built successfully")
            
            # Список файлов сборки
            print("\n📦 Build artifacts:")
            for file_path in dist_path.glob("*"):
                print(f"  • {file_path.name}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            return False
    
    def publish_to_test_pypi(self) -> bool:
        """Публикация в Test PyPI"""
        try:
            subprocess.run(
                ["poetry", "publish", "--repository", "testpypi"], 
                cwd=self.package_path, 
                check=True
            )
            print("✅ Published to Test PyPI")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Test PyPI publication failed: {e}")
            return False
    
    def publish_to_pypi(self) -> bool:
        """Публикация в PyPI"""
        try:
            subprocess.run(
                ["poetry", "publish"], 
                cwd=self.package_path, 
                check=True
            )
            print("✅ Published to PyPI")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ PyPI publication failed: {e}")
            return False
    
    def full_publish_workflow(self, test_first: bool = True) -> bool:
        """Полный workflow публикации"""
        print("🚀 Starting publication workflow...")
        
        # Предварительные проверки
        if not self.pre_publish_checks():
            print("❌ Pre-publish checks failed")
            return False
        
        # Сборка и тестирование
        if not self.build_and_test_package():
            print("❌ Build and test failed")
            return False
        
        # Публикация в Test PyPI (опционально)
        if test_first:
            print("\n📤 Publishing to Test PyPI first...")
            if not self.publish_to_test_pypi():
                print("❌ Test PyPI publication failed")
                return False
            
            # Подтверждение для продолжения
            response = input("\n✅ Test PyPI publication successful. Continue with PyPI? (y/N): ")
            if response.lower() != 'y':
                print("📤 Publication workflow stopped by user")
                return True
        
        # Публикация в PyPI
        print("\n📤 Publishing to PyPI...")
        if not self.publish_to_pypi():
            print("❌ PyPI publication failed")
            return False
        
        print("\n🎉 Package successfully published to PyPI!")
        return True 