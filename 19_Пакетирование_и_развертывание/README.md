# 19_Пакетирование_и_развертывание

## Файлы примеров

- **setup_py_example.py** — классический setup.py
- **pyproject_toml_example/** — современный pyproject.toml
- **poetry_example/** — управление зависимостями с Poetry
- **docker_example/** — контейнеризация с Docker
- **virtual_env_examples.py** — виртуальные окружения
- **requirements_examples/** — управление зависимостями
- **ci_cd_examples/** — примеры CI/CD

## Темы

### Виртуальные окружения
- venv (встроенный)
- virtualenv
- conda окружения
- pipenv
- Изоляция зависимостей

### Управление зависимостями
- requirements.txt
- pip-tools
- Poetry для современных проектов
- Pipfile и pipenv
- conda environment.yml

### Пакетирование
- setup.py (классический)
- pyproject.toml (современный)
- setuptools, wheel
- Создание дистрибутивов
- Публикация в PyPI

### Poetry
- Современный инструмент управления
- pyproject.toml конфигурация
- Автоматическое разрешение зависимостей
- Виртуальные окружения
- Публикация пакетов

### Docker
- Dockerfile для Python приложений
- Многоэтапная сборка
- Docker Compose
- Оптимизация образов
- Безопасность контейнеров

### CI/CD
- GitHub Actions
- GitLab CI
- Автоматическое тестирование
- Автоматическое развертывание
- Линтинг и форматирование

### Развертывание
- Heroku
- AWS, GCP, Azure
- Systemd сервисы
- Nginx + uWSGI/Gunicorn
- Мониторинг и логирование

## Установка инструментов

```bash
# Poetry
curl -sSL https://install.python-poetry.org | python3 -

# pipenv
pip install pipenv

# Docker (установка зависит от ОС)
# https://docs.docker.com/get-docker/

# Инструменты разработки
pip install black flake8 mypy pre-commit
```

## Как использовать

1. Изучите виртуальные окружения
2. Освойте Poetry для новых проектов
3. Практикуйте создание пакетов
4. Изучите Docker для контейнеризации
5. Настройте CI/CD пайплайны

## Команды для разработки

```bash
# Виртуальные окружения
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows

# Poetry
poetry init
poetry add requests
poetry install
poetry run python script.py

# Docker
docker build -t myapp .
docker run -p 8000:8000 myapp

# Публикация
python -m build
twine upload dist/*
```

## Полезные ресурсы

- Poetry документация: https://python-poetry.org/docs/
- PyPI: https://pypi.org/
- Docker документация: https://docs.docker.com/
- GitHub Actions: https://docs.github.com/en/actions 