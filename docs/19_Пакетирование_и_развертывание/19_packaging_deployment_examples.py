"""
Примеры: Пакетирование и развертывание Python

Этот файл содержит практические примеры пакетирования Python приложений,
управления зависимостями, контейнеризации и развертывания.
"""

import os
import subprocess
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import zipfile
import tarfile
from datetime import datetime
import yaml

# =============================================================================
# Пример 1: Создание Python пакета с pyproject.toml
# =============================================================================

def create_python_package_structure():
    """Демонстрация создания структуры Python пакета"""
    
    print("=== Создание структуры Python пакета ===")
    
    # Структура проекта
    project_structure = {
        "my_awesome_package/": {
            "src/": {
                "my_awesome_package/": {
                    "__init__.py": "",
                    "core.py": "",
                    "utils.py": "",
                    "cli.py": "",
                },
            },
            "tests/": {
                "__init__.py": "",
                "test_core.py": "",
                "test_utils.py": "",
                "conftest.py": "",
            },
            "docs/": {
                "README.md": "",
                "api.md": "",
            },
            "pyproject.toml": "",
            "README.md": "",
            "LICENSE": "",
            ".gitignore": "",
        }
    }
    
    def print_structure(structure, indent=0):
        """Рекурсивно выводит структуру директорий"""
        for name, content in structure.items():
            print("  " * indent + name)
            if isinstance(content, dict):
                print_structure(content, indent + 1)
    
    print("Структура проекта:")
    print_structure(project_structure)

def generate_pyproject_toml():
    """Генерация современного pyproject.toml"""
    
    pyproject_content = """[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-awesome-package"
description = "A package that does awesome things"
readme = "README.md"
license = {file = "LICENSE"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
maintainers = [
    {name = "Your Name", email = "your.email@example.com"},
]
keywords = ["python", "package", "awesome"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
requires-python = ">=3.8"
dependencies = [
    "click>=8.0.0",
    "requests>=2.25.0",
    "pydantic>=1.8.0",
]
dynamic = ["version"]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-cov>=2.10",
    "black>=21.0",
    "flake8>=3.8",
    "mypy>=0.800",
    "pre-commit>=2.10",
]
docs = [
    "mkdocs>=1.2",
    "mkdocs-material>=7.0",
    "mkdocstrings>=0.15",
]
test = [
    "pytest>=6.0",
    "pytest-cov>=2.10",
    "pytest-mock>=3.6",
    "httpx>=0.24.0",
]

[project.scripts]
my-awesome-cli = "my_awesome_package.cli:main"

[project.urls]
Homepage = "https://github.com/username/my-awesome-package"
Documentation = "https://my-awesome-package.readthedocs.io"
Repository = "https://github.com/username/my-awesome-package.git"
Issues = "https://github.com/username/my-awesome-package/issues"
Changelog = "https://github.com/username/my-awesome-package/blob/main/CHANGELOG.md"

[tool.hatch.version]
path = "src/my_awesome_package/__init__.py"

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/tests",
    "/docs",
]

[tool.hatch.build.targets.wheel]
packages = ["src/my_awesome_package"]

[tool.black]
line-length = 88
target-version = ['py38']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --strict-markers --strict-config"
testpaths = ["tests"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
"""
    
    print("\n=== pyproject.toml ===")
    print(pyproject_content)
    return pyproject_content

def generate_package_files():
    """Генерация основных файлов пакета"""
    
    # __init__.py
    init_content = '''"""
My Awesome Package

A Python package that does awesome things.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core import AwesomeClass, awesome_function
from .utils import utility_function

__all__ = [
    "AwesomeClass",
    "awesome_function", 
    "utility_function",
]
'''
    
    # core.py
    core_content = '''"""
Core functionality of the awesome package.
"""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AwesomeClass:
    """A class that does awesome things."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        logger.info(f"Created AwesomeClass instance: {name}")
    
    def do_awesome_thing(self, data: str) -> str:
        """Do something awesome with the data."""
        result = f"Awesome result for {self.name}: {data.upper()}"
        logger.debug(f"Processing: {data} -> {result}")
        return result
    
    def configure(self, **kwargs) -> None:
        """Update configuration."""
        self.config.update(kwargs)
        logger.info(f"Updated config for {self.name}: {kwargs}")


def awesome_function(input_data: str, multiplier: int = 1) -> str:
    """A standalone awesome function."""
    result = input_data * multiplier
    logger.debug(f"awesome_function: {input_data} * {multiplier} = {result}")
    return result
'''
    
    # utils.py
    utils_content = '''"""
Utility functions for the awesome package.
"""

import json
from typing import Any, Dict, List, Optional
from pathlib import Path


def utility_function(data: List[Any]) -> Dict[str, int]:
    """A utility function that counts types in a list."""
    type_counts = {}
    for item in data:
        type_name = type(item).__name__
        type_counts[type_name] = type_counts.get(type_name, 0) + 1
    return type_counts


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")


def save_config(config: Dict[str, Any], config_path: Path) -> None:
    """Save configuration to a JSON file."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


class ConfigManager:
    """Configuration manager with file persistence."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("config.json")
        self._config = load_config(self.config_path)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
    
    def save(self) -> None:
        """Save configuration to file."""
        save_config(self._config, self.config_path)
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._config = load_config(self.config_path)
'''
    
    # cli.py
    cli_content = '''"""
Command-line interface for the awesome package.
"""

import click
import logging
from pathlib import Path
from .core import AwesomeClass, awesome_function
from .utils import ConfigManager


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config', '-c', type=click.Path(), help='Configuration file path')
@click.pass_context
def main(ctx, verbose, config):
    """My Awesome Package CLI."""
    
    # Setup logging
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')
    
    # Setup context
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config_manager'] = ConfigManager(Path(config) if config else None)


@main.command()
@click.argument('name')
@click.argument('data')
@click.option('--multiplier', '-m', default=1, help='Multiplier for the operation')
@click.pass_context
def process(ctx, name, data, multiplier):
    """Process data with the awesome functionality."""
    
    awesome = AwesomeClass(name)
    result = awesome.do_awesome_thing(data)
    
    if multiplier > 1:
        result = awesome_function(result, multiplier)
    
    click.echo(f"Result: {result}")


@main.command()
@click.option('--key', required=True, help='Configuration key')
@click.option('--value', required=True, help='Configuration value')
@click.pass_context
def config_set(ctx, key, value):
    """Set a configuration value."""
    
    config_manager = ctx.obj['config_manager']
    config_manager.set(key, value)
    config_manager.save()
    
    click.echo(f"Set {key} = {value}")


@main.command()
@click.option('--key', help='Configuration key to get (if not provided, show all)')
@click.pass_context
def config_get(ctx, key):
    """Get configuration value(s)."""
    
    config_manager = ctx.obj['config_manager']
    
    if key:
        value = config_manager.get(key)
        click.echo(f"{key} = {value}")
    else:
        config_manager.reload()
        for k, v in config_manager._config.items():
            click.echo(f"{k} = {v}")


if __name__ == '__main__':
    main()
'''
    
    print("\n=== Основные файлы пакета ===")
    files = {
        "__init__.py": init_content,
        "core.py": core_content,
        "utils.py": utils_content,
        "cli.py": cli_content,
    }
    
    for filename, content in files.items():
        print(f"\n--- {filename} ---")
        print(content[:500] + "..." if len(content) > 500 else content)
    
    return files

# =============================================================================
# Пример 2: Poetry для управления зависимостями
# =============================================================================

def demonstrate_poetry_workflow():
    """Демонстрация работы с Poetry"""
    
    print("\n=== Poetry Workflow ===")
    
    # pyproject.toml для Poetry
    poetry_config = """[tool.poetry]
name = "my-poetry-project"
version = "0.1.0"
description = "A project managed with Poetry"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "my_poetry_project", from = "src"}]

[tool.poetry.dependencies]
python = "^3.8"
click = "^8.0.0"
requests = "^2.25.0"
pydantic = "^1.8.0"

[tool.poetry.group.dev.dependencies]
pytest = "^6.0"
pytest-cov = "^2.10"
black = "^21.0"
flake8 = "^3.8"
mypy = "^0.800"
pre-commit = "^2.10"

[tool.poetry.group.docs.dependencies]
mkdocs = "^1.2"
mkdocs-material = "^7.0"

[tool.poetry.scripts]
my-cli = "my_poetry_project.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    
    print("Poetry pyproject.toml:")
    print(poetry_config)
    
    # Основные команды Poetry
    poetry_commands = [
        ("poetry init", "Интерактивное создание pyproject.toml"),
        ("poetry install", "Установка всех зависимостей"),
        ("poetry add requests", "Добавить зависимость"),
        ("poetry add --group dev pytest", "Добавить dev зависимость"),
        ("poetry remove requests", "Удалить зависимость"),
        ("poetry update", "Обновить все зависимости"),
        ("poetry show", "Показать установленные пакеты"),
        ("poetry show --tree", "Показать дерево зависимостей"),
        ("poetry build", "Собрать пакет (wheel и sdist)"),
        ("poetry publish", "Опубликовать в PyPI"),
        ("poetry run python script.py", "Запустить скрипт в виртуальном окружении"),
        ("poetry shell", "Активировать виртуальное окружение"),
        ("poetry env info", "Информация о виртуальном окружении"),
        ("poetry lock", "Обновить poetry.lock"),
        ("poetry check", "Проверить валидность pyproject.toml"),
    ]
    
    print("\nОсновные команды Poetry:")
    for command, description in poetry_commands:
        print(f"  {command:<30} # {description}")

# =============================================================================
# Пример 3: Docker контейнеризация
# =============================================================================

def generate_dockerfile_examples():
    """Генерация примеров Dockerfile для Python приложений"""
    
    print("\n=== Docker Examples ===")
    
    # Простой Dockerfile
    simple_dockerfile = """# Simple Python Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
"""
    
    # Multi-stage Dockerfile
    multistage_dockerfile = """# Multi-stage Docker build for Python
# Stage 1: Build stage
FROM python:3.11 as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim

# Create non-root user
RUN groupadd --gid 1000 appuser \\
    && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Install runtime dependencies
RUN apt-get update && apt-get install -y \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Update PATH to include local packages
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "app.py"]
"""
    
    # Production-ready Dockerfile
    production_dockerfile = """# Production-ready Python Dockerfile
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \\
    PYTHONDONTWRITEBYTECODE=1 \\
    PIP_NO_CACHE_DIR=1 \\
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Build stage
FROM base as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --user -r requirements.txt

# Production stage
FROM base as production

# Create non-root user
RUN groupadd --gid 1000 appuser \\
    && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Update PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
"""
    
    dockerfiles = {
        "Simple Dockerfile": simple_dockerfile,
        "Multi-stage Dockerfile": multistage_dockerfile,
        "Production Dockerfile": production_dockerfile,
    }
    
    for name, content in dockerfiles.items():
        print(f"\n--- {name} ---")
        print(content)
    
    return dockerfiles

def generate_docker_compose_example():
    """Генерация примера Docker Compose"""
    
    docker_compose = """version: '3.8'

services:
  web:
    build: 
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  worker:
    build: 
      context: .
      dockerfile: Dockerfile
      target: production
    command: celery -A app.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network
    restart: unless-stopped

  scheduler:
    build: 
      context: .
      dockerfile: Dockerfile
      target: production
    command: celery -A app.celery beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - static_volume:/app/static
    depends_on:
      - web
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_volume:

networks:
  app-network:
    driver: bridge
"""
    
    print("\n=== Docker Compose Example ===")
    print(docker_compose)
    
    return docker_compose

# =============================================================================
# Пример 4: CI/CD с GitHub Actions
# =============================================================================

def generate_github_actions_workflow():
    """Генерация GitHub Actions workflow"""
    
    workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

env:
  PYTHON_VERSION: '3.11'
  POETRY_VERSION: '1.4.2'

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: ${{ env.POETRY_VERSION }}
        virtualenvs-create: true
        virtualenvs-in-project: true
    
    - name: Load cached venv
      id: cached-poetry-dependencies
      uses: actions/cache@v3
      with:
        path: .venv
        key: venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}
    
    - name: Install dependencies
      if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
      run: poetry install --no-interaction --no-root
    
    - name: Install project
      run: poetry install --no-interaction
    
    - name: Run linting
      run: |
        poetry run flake8 src tests
        poetry run black --check src tests
        poetry run isort --check-only src tests
    
    - name: Run type checking
      run: poetry run mypy src
    
    - name: Run security check
      run: poetry run bandit -r src
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379/0
      run: |
        poetry run pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: ${{ env.POETRY_VERSION }}
    
    - name: Build package
      run: poetry build
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  docker:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ghcr.io/${{ github.repository }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    needs: [build, docker]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment..."
        # Here you would add your deployment commands
        # For example, using kubectl, ansible, or cloud provider CLI
    
    - name: Run smoke tests
      run: |
        echo "Running smoke tests..."
        # Add smoke tests for the deployed application
    
    - name: Deploy to production
      if: success()
      run: |
        echo "Deploying to production environment..."
        # Production deployment commands

  publish:
    needs: [build]
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: ${{ env.POETRY_VERSION }}
    
    - name: Build package
      run: poetry build
    
    - name: Publish to PyPI
      env:
        POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_TOKEN }}
      run: poetry publish
"""
    
    print("\n=== GitHub Actions Workflow ===")
    print(workflow)
    return workflow

# =============================================================================
# Пример 5: Kubernetes развертывание
# =============================================================================

def generate_kubernetes_manifests():
    """Генерация Kubernetes манифестов"""
    
    # Deployment
    deployment = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-app
  labels:
    app: python-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: python-app
  template:
    metadata:
      labels:
        app: python-app
    spec:
      containers:
      - name: app
        image: ghcr.io/username/python-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis-url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: app-config-volume
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: app-config-volume
        configMap:
          name: app-config
      imagePullSecrets:
      - name: ghcr-secret
"""
    
    # Service
    service = """apiVersion: v1
kind: Service
metadata:
  name: python-app-service
spec:
  selector:
    app: python-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
"""
    
    # Ingress
    ingress = """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: python-app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: python-app-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: python-app-service
            port:
              number: 80
"""
    
    # ConfigMap
    configmap = """apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  redis-url: "redis://redis-service:6379/0"
  log-level: "INFO"
  workers: "4"
  config.json: |
    {
      "feature_flags": {
        "new_feature": true,
        "beta_feature": false
      },
      "limits": {
        "max_requests_per_minute": 100,
        "max_upload_size": "10MB"
      }
    }
"""
    
    # Secret
    secret = """apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  database-url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc3dvcmRAZGI6NTQzMi9teWRi  # base64 encoded
  secret-key: bXlfc2VjcmV0X2tleV9oZXJl  # base64 encoded
"""
    
    # HorizontalPodAutoscaler
    hpa = """apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: python-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: python-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
"""
    
    manifests = {
        "deployment.yaml": deployment,
        "service.yaml": service,
        "ingress.yaml": ingress,
        "configmap.yaml": configmap,
        "secret.yaml": secret,
        "hpa.yaml": hpa,
    }
    
    print("\n=== Kubernetes Manifests ===")
    for name, content in manifests.items():
        print(f"\n--- {name} ---")
        print(content)
    
    return manifests

# =============================================================================
# Пример 6: Мониторинг и логирование
# =============================================================================

def generate_monitoring_config():
    """Генерация конфигурации мониторинга"""
    
    # Prometheus configuration
    prometheus_config = """global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'python-app'
    static_configs:
      - targets: ['python-app:8000']
    metrics_path: /metrics
    scrape_interval: 10s
    
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
    - role: pod
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
"""
    
    # Grafana dashboard
    grafana_dashboard = """{
  "dashboard": {
    "id": null,
    "title": "Python Application Dashboard",
    "tags": ["python", "application"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ],
        "yAxes": [
          {
            "label": "Requests/sec"
          }
        ]
      },
      {
        "id": 2,
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "Error Rate"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "5s"
  }
}"""
    
    # ELK Stack configuration
    logstash_config = """input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] == "python-app" {
    json {
      source => "message"
    }
    
    date {
      match => [ "timestamp", "ISO8601" ]
    }
    
    if [level] == "ERROR" {
      mutate {
        add_tag => ["error"]
      }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "python-app-%{+YYYY.MM.dd}"
  }
  
  if "error" in [tags] {
    slack {
      url => "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
      channel => "#alerts"
      username => "LogstashBot"
    }
  }
}
"""
    
    configs = {
        "prometheus.yml": prometheus_config,
        "grafana-dashboard.json": grafana_dashboard,
        "logstash.conf": logstash_config,
    }
    
    print("\n=== Monitoring Configuration ===")
    for name, content in configs.items():
        print(f"\n--- {name} ---")
        print(content[:500] + "..." if len(content) > 500 else content)
    
    return configs

# =============================================================================
# Главная функция для демонстрации всех примеров
# =============================================================================

def main():
    """Запуск всех примеров пакетирования и развертывания"""
    
    print("=== Пакетирование и развертывание Python ===\n")
    
    # 1. Структура пакета
    create_python_package_structure()
    
    # 2. pyproject.toml
    pyproject_content = generate_pyproject_toml()
    
    # 3. Файлы пакета
    package_files = generate_package_files()
    
    # 4. Poetry workflow
    demonstrate_poetry_workflow()
    
    # 5. Docker примеры
    dockerfiles = generate_dockerfile_examples()
    docker_compose = generate_docker_compose_example()
    
    # 6. CI/CD
    github_workflow = generate_github_actions_workflow()
    
    # 7. Kubernetes
    k8s_manifests = generate_kubernetes_manifests()
    
    # 8. Мониторинг
    monitoring_configs = generate_monitoring_config()
    
    print("\n=== Сводка ===")
    print("✅ Структура Python пакета")
    print("✅ Современный pyproject.toml")
    print("✅ Poetry для управления зависимостями")
    print("✅ Docker контейнеризация")
    print("✅ CI/CD с GitHub Actions")
    print("✅ Kubernetes развертывание")
    print("✅ Мониторинг и логирование")
    
    print("\nВсе примеры демонстрируют современные практики разработки и развертывания Python приложений! 🚀")

if __name__ == "__main__":
    main() 