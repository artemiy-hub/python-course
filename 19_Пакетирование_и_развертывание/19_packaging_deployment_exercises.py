"""
Упражнения: Пакетирование и развертывание Python

Этот файл содержит практические упражнения для изучения пакетирования Python
приложений, управления зависимостями, контейнеризации и развертывания.
"""

import os
import subprocess
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import zipfile
import tarfile
from datetime import datetime
import yaml
import configparser
from dataclasses import dataclass, asdict
from unittest.mock import Mock, patch
import pytest

# =============================================================================
# Упражнение 1: Создание Python пакета
# =============================================================================

"""
ЗАДАНИЕ 1: Math Utilities Package

Создайте Python пакет "mathutils" со следующей структурой:

mathutils/
├── src/
│   └── mathutils/
│       ├── __init__.py
│       ├── basic.py      # основные операции
│       ├── advanced.py   # продвинутые функции
│       └── constants.py  # математические константы
├── tests/
│   ├── test_basic.py
│   └── test_advanced.py
├── pyproject.toml
├── README.md
└── LICENSE

Требования:
1. basic.py: add, subtract, multiply, divide, power
2. advanced.py: factorial, fibonacci, gcd, lcm
3. constants.py: PI, E, GOLDEN_RATIO
4. Все функции должны быть типизированы
5. Создать pyproject.toml с правильными метаданными
"""

# Ваш код здесь:
class PackageCreator:
    """Создатель Python пакетов"""
    
    def __init__(self, package_name: str, base_dir: Path):
        # TODO: Реализуйте инициализацию
        pass
    
    def create_structure(self):
        """Создать структуру пакета"""
        # TODO: Реализуйте метод
        pass
    
    def generate_pyproject_toml(self) -> str:
        """Сгенерировать pyproject.toml"""
        # TODO: Реализуйте метод
        pass
    
    def generate_source_files(self):
        """Сгенерировать исходные файлы"""
        # TODO: Реализуйте метод
        pass

# Решение:
@dataclass
class PackageMetadata:
    """Метаданные пакета"""
    name: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    author_email: str = ""
    license: str = "MIT"
    requires_python: str = ">=3.8"
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class PackageCreatorSolution:
    """Решение: Создатель Python пакетов"""
    
    def __init__(self, package_name: str, base_dir: Path, metadata: PackageMetadata = None):
        self.package_name = package_name
        self.base_dir = Path(base_dir)
        self.metadata = metadata or PackageMetadata(name=package_name)
        self.package_dir = self.base_dir / package_name
    
    def create_structure(self):
        """Создать структуру пакета"""
        # Основные директории
        directories = [
            self.package_dir,
            self.package_dir / "src" / self.package_name,
            self.package_dir / "tests",
            self.package_dir / "docs",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Создать файлы
        self._create_source_files()
        self._create_test_files()
        self._create_config_files()
        self._create_documentation()
    
    def _create_source_files(self):
        """Создать исходные файлы"""
        src_dir = self.package_dir / "src" / self.package_name
        
        # __init__.py
        init_content = f'''"""
{self.metadata.description or f"{self.package_name} package"}

A Python package for mathematical utilities.
"""

__version__ = "{self.metadata.version}"
__author__ = "{self.metadata.author}"

from .basic import add, subtract, multiply, divide, power
from .advanced import factorial, fibonacci, gcd, lcm
from .constants import PI, E, GOLDEN_RATIO

__all__ = [
    "add", "subtract", "multiply", "divide", "power",
    "factorial", "fibonacci", "gcd", "lcm",
    "PI", "E", "GOLDEN_RATIO",
]
'''
        
        # basic.py
        basic_content = '''"""
Basic mathematical operations.
"""

from typing import Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Add two numbers."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Subtract two numbers."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Multiply two numbers."""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: Number, exponent: Number) -> Number:
    """Raise base to the power of exponent."""
    return base ** exponent
'''
        
        # advanced.py
        advanced_content = '''"""
Advanced mathematical operations.
"""

from typing import Union


def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number."""
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Calculate least common multiple."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)
'''
        
        # constants.py
        constants_content = '''"""
Mathematical constants.
"""

import math

PI = math.pi
E = math.e
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
'''
        
        files = {
            "__init__.py": init_content,
            "basic.py": basic_content,
            "advanced.py": advanced_content,
            "constants.py": constants_content,
        }
        
        for filename, content in files.items():
            (src_dir / filename).write_text(content)
    
    def _create_test_files(self):
        """Создать тестовые файлы"""
        tests_dir = self.package_dir / "tests"
        
        # test_basic.py
        test_basic = f'''"""
Tests for basic mathematical operations.
"""

import pytest
from {self.package_name}.basic import add, subtract, multiply, divide, power


class TestBasicOperations:
    """Test basic mathematical operations."""
    
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0.1, 0.2) == pytest.approx(0.3)
    
    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
    
    def test_multiply(self):
        assert multiply(4, 3) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0
    
    def test_divide(self):
        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)
    
    def test_power(self):
        assert power(2, 3) == 8
        assert power(5, 0) == 1
        assert power(10, 1) == 10
'''
        
        # test_advanced.py
        test_advanced = f'''"""
Tests for advanced mathematical operations.
"""

import pytest
from {self.package_name}.advanced import factorial, fibonacci, gcd, lcm


class TestAdvancedOperations:
    """Test advanced mathematical operations."""
    
    def test_factorial(self):
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120
    
    def test_factorial_negative(self):
        with pytest.raises(ValueError):
            factorial(-1)
    
    def test_fibonacci(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(10) == 55
    
    def test_fibonacci_negative(self):
        with pytest.raises(ValueError):
            fibonacci(-1)
    
    def test_gcd(self):
        assert gcd(12, 8) == 4
        assert gcd(17, 13) == 1
        assert gcd(-12, 8) == 4
    
    def test_lcm(self):
        assert lcm(12, 8) == 24
        assert lcm(17, 13) == 221
        assert lcm(0, 5) == 0
'''
        
        (tests_dir / "test_basic.py").write_text(test_basic)
        (tests_dir / "test_advanced.py").write_text(test_advanced)
    
    def _create_config_files(self):
        """Создать конфигурационные файлы"""
        # pyproject.toml
        pyproject_content = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{self.metadata.name}"
version = "{self.metadata.version}"
description = "{self.metadata.description or f'A Python package: {self.metadata.name}'}"
readme = "README.md"
license = {{file = "LICENSE"}}
authors = [
    {{name = "{self.metadata.author}", email = "{self.metadata.author_email}"}},
]
requires-python = "{self.metadata.requires_python}"
dependencies = {self.metadata.dependencies}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "black>=21.0",
    "flake8>=3.8",
    "mypy>=0.800",
]

[tool.hatch.version]
path = "src/{self.metadata.name}/__init__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/{self.metadata.name}"]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.pytest.ini_options]
testpaths = ["tests"]
'''
        
        (self.package_dir / "pyproject.toml").write_text(pyproject_content)
    
    def _create_documentation(self):
        """Создать документацию"""
        # README.md
        readme_content = f'''# {self.metadata.name}

{self.metadata.description or f"A Python package: {self.metadata.name}"}

## Installation

```bash
pip install {self.metadata.name}
```

## Usage

```python
from {self.metadata.name} import add, factorial, PI

# Basic operations
result = add(2, 3)
print(f"2 + 3 = {{result}}")

# Advanced operations
fact = factorial(5)
print(f"5! = {{fact}}")

# Constants
print(f"PI = {{PI}}")
```

## Development

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black src tests

# Type checking
mypy src
```

## License

{self.metadata.license}
'''
        
        # LICENSE
        license_content = '''MIT License

Copyright (c) 2024

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
        
        (self.package_dir / "README.md").write_text(readme_content)
        (self.package_dir / "LICENSE").write_text(license_content)

# Тесты для PackageCreator
class TestPackageCreator:
    """Тесты создателя пакетов"""
    
    @pytest.fixture
    def temp_dir(self):
        """Временная директория для тестов"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)
    
    @pytest.fixture
    def package_metadata(self):
        """Метаданные тестового пакета"""
        return PackageMetadata(
            name="testmath",
            description="Test math utilities",
            author="Test Author",
            author_email="test@example.com"
        )
    
    def test_create_package_structure(self, temp_dir, package_metadata):
        """Тест создания структуры пакета"""
        creator = PackageCreatorSolution("testmath", temp_dir, package_metadata)
        creator.create_structure()
        
        # Проверяем структуру директорий
        package_dir = temp_dir / "testmath"
        assert package_dir.exists()
        assert (package_dir / "src" / "testmath").exists()
        assert (package_dir / "tests").exists()
        assert (package_dir / "docs").exists()
        
        # Проверяем основные файлы
        assert (package_dir / "pyproject.toml").exists()
        assert (package_dir / "README.md").exists()
        assert (package_dir / "LICENSE").exists()
        
        # Проверяем исходные файлы
        src_dir = package_dir / "src" / "testmath"
        assert (src_dir / "__init__.py").exists()
        assert (src_dir / "basic.py").exists()
        assert (src_dir / "advanced.py").exists()
        assert (src_dir / "constants.py").exists()
    
    def test_pyproject_toml_content(self, temp_dir, package_metadata):
        """Тест содержимого pyproject.toml"""
        creator = PackageCreatorSolution("testmath", temp_dir, package_metadata)
        creator.create_structure()
        
        pyproject_path = temp_dir / "testmath" / "pyproject.toml"
        content = pyproject_path.read_text()
        
        assert "testmath" in content
        assert "Test math utilities" in content
        assert "Test Author" in content

# =============================================================================
# Упражнение 2: Docker контейнеризация
# =============================================================================

"""
ЗАДАНИЕ 2: Flask Application Dockerization

Создайте Docker контейнер для Flask приложения:

1. Простое Flask приложение с API
2. Requirements.txt с зависимостями
3. Dockerfile с multi-stage build
4. Docker Compose для развертывания с базой данных
5. Health checks и proper logging

Требования:
- Приложение должно отвечать на /health
- Использовать non-root пользователя
- Оптимизировать размер образа
- Настроить логирование
"""

# Ваш код здесь:
class DockerizedFlaskApp:
    """Создатель Docker контейнера для Flask приложения"""
    
    def __init__(self, app_name: str, app_dir: Path):
        # TODO: Реализуйте инициализацию
        pass
    
    def create_flask_app(self) -> str:
        """Создать Flask приложение"""
        # TODO: Реализуйте метод
        pass
    
    def create_dockerfile(self) -> str:
        """Создать Dockerfile"""
        # TODO: Реализуйте метод
        pass
    
    def create_docker_compose(self) -> str:
        """Создать docker-compose.yml"""
        # TODO: Реализуйте метод
        pass

# Решение:
class DockerizedFlaskAppSolution:
    """Решение: Создатель Docker контейнера для Flask приложения"""
    
    def __init__(self, app_name: str, app_dir: Path):
        self.app_name = app_name
        self.app_dir = Path(app_dir)
        self.app_dir.mkdir(parents=True, exist_ok=True)
    
    def create_flask_app(self) -> str:
        """Создать Flask приложение"""
        app_content = '''"""
Simple Flask application for Docker demonstration.
"""

from flask import Flask, jsonify, request
import logging
import os
import sys
from datetime import datetime
import psutil

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    """Home endpoint."""
    return jsonify({
        "message": "Welcome to Flask Docker App!",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        # Basic health checks
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        status = "healthy" if memory_usage < 90 and disk_usage < 90 else "unhealthy"
        
        return jsonify({
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "memory_usage_percent": memory_usage,
                "disk_usage_percent": disk_usage,
                "python_version": sys.version
            }
        }), 200 if status == "healthy" else 503
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503


@app.route('/api/info')
def app_info():
    """Application information endpoint."""
    return jsonify({
        "app_name": "Flask Docker Demo",
        "environment": os.getenv("FLASK_ENV", "production"),
        "debug": app.debug,
        "host": request.host,
        "user_agent": request.headers.get("User-Agent"),
    })


@app.route('/api/echo', methods=['POST'])
def echo():
    """Echo endpoint for testing."""
    data = request.get_json()
    logger.info(f"Echo request: {data}")
    
    return jsonify({
        "echo": data,
        "timestamp": datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
'''
        
        (self.app_dir / "app.py").write_text(app_content)
        return app_content
    
    def create_requirements(self) -> str:
        """Создать requirements.txt"""
        requirements = '''Flask==2.3.2
gunicorn==21.2.0
psutil==5.9.5
requests==2.31.0
'''
        (self.app_dir / "requirements.txt").write_text(requirements)
        return requirements
    
    def create_dockerfile(self) -> str:
        """Создать Dockerfile"""
        dockerfile_content = '''# Multi-stage Docker build for Flask application

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \\
    PYTHONDONTWRITEBYTECODE=1 \\
    PATH=/home/appuser/.local/bin:$PATH \\
    FLASK_ENV=production \\
    PORT=5000

# Install runtime dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1000 appuser \\
    && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
'''
        
        (self.app_dir / "Dockerfile").write_text(dockerfile_content)
        return dockerfile_content
    
    def create_docker_compose(self) -> str:
        """Создать docker-compose.yml"""
        compose_content = f'''version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://user:password@db:5432/{self.app_name}
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB={self.app_name}
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d {self.app_name}"]
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
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
'''
        
        (self.app_dir / "docker-compose.yml").write_text(compose_content)
        return compose_content
    
    def create_nginx_config(self) -> str:
        """Создать конфигурацию Nginx"""
        nginx_config = '''events {
    worker_connections 1024;
}

http {
    upstream flask_app {
        server web:5000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://flask_app/health;
            access_log off;
        }
    }
}
'''
        
        (self.app_dir / "nginx.conf").write_text(nginx_config)
        return nginx_config
    
    def build_complete_app(self):
        """Создать полное приложение"""
        self.create_flask_app()
        self.create_requirements()
        self.create_dockerfile()
        self.create_docker_compose()
        self.create_nginx_config()
        
        # .dockerignore
        dockerignore = '''*.pyc
*.pyo
*.pyd
__pycache__/
.git/
.pytest_cache/
*.egg-info/
build/
dist/
.coverage
htmlcov/
.tox/
.cache
.DS_Store
'''
        (self.app_dir / ".dockerignore").write_text(dockerignore)

# Тесты для Docker приложения
class TestDockerizedFlaskApp:
    """Тесты Docker приложения"""
    
    @pytest.fixture
    def temp_dir(self):
        """Временная директория для тестов"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)
    
    @pytest.fixture
    def docker_app(self, temp_dir):
        """Docker приложение"""
        app = DockerizedFlaskAppSolution("testapp", temp_dir)
        app.build_complete_app()
        return app
    
    def test_flask_app_creation(self, docker_app, temp_dir):
        """Тест создания Flask приложения"""
        app_file = temp_dir / "app.py"
        assert app_file.exists()
        
        content = app_file.read_text()
        assert "Flask" in content
        assert "/health" in content
        assert "def health():" in content
    
    def test_dockerfile_creation(self, docker_app, temp_dir):
        """Тест создания Dockerfile"""
        dockerfile = temp_dir / "Dockerfile"
        assert dockerfile.exists()
        
        content = dockerfile.read_text()
        assert "FROM python:" in content
        assert "multi-stage" in content.lower()
        assert "appuser" in content
        assert "HEALTHCHECK" in content
    
    def test_docker_compose_creation(self, docker_app, temp_dir):
        """Тест создания docker-compose.yml"""
        compose_file = temp_dir / "docker-compose.yml"
        assert compose_file.exists()
        
        content = compose_file.read_text()
        assert "services:" in content
        assert "web:" in content
        assert "db:" in content
        assert "redis:" in content

# =============================================================================
# Упражнение 3: CI/CD Pipeline
# =============================================================================

"""
ЗАДАНИЕ 3: GitHub Actions Pipeline

Создайте CI/CD pipeline для Python проекта:

1. Workflow для тестирования на множественных версиях Python
2. Code quality checks (linting, formatting, type checking)
3. Security scanning
4. Docker build и push
5. Automatic deployment на staging
6. Release management

Требования:
- Тесты должны проходить на Python 3.8, 3.9, 3.10, 3.11
- Проверка с flake8, black, mypy
- Security check с bandit
- Coverage report
- Conditional deployment
"""

# Ваш код здесь:
class CIPipelineGenerator:
    """Генератор CI/CD pipeline"""
    
    def __init__(self, project_name: str):
        # TODO: Реализуйте инициализацию
        pass
    
    def generate_test_workflow(self) -> str:
        """Создать workflow для тестирования"""
        # TODO: Реализуйте метод
        pass
    
    def generate_deploy_workflow(self) -> str:
        """Создать workflow для развертывания"""
        # TODO: Реализуйте метод
        pass

# Решение:
class CIPipelineGeneratorSolution:
    """Решение: Генератор CI/CD pipeline"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
    
    def generate_test_workflow(self) -> str:
        """Создать workflow для тестирования"""
        workflow = f'''name: Test and Quality Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'

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

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{{{ matrix.python-version }}}}
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ matrix.python-version }}}}
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{{{ runner.os }}}}-pip-${{{{ hashFiles('**/requirements*.txt') }}}}
        restore-keys: |
          ${{{{ runner.os }}}}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
      run: |
        pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{{{ env.PYTHON_VERSION }}}}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black flake8 mypy bandit safety
    
    - name: Check code formatting with Black
      run: black --check src tests
    
    - name: Lint with flake8
      run: flake8 src tests --max-line-length=88
    
    - name: Type check with mypy
      run: mypy src --ignore-missing-imports
    
    - name: Security check with bandit
      run: bandit -r src -f json -o bandit-report.json
    
    - name: Safety check
      run: safety check --json --output safety-report.json
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

  build:
    needs: [test, quality]
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
        username: ${{{{ github.actor }}}}
        password: ${{{{ secrets.GITHUB_TOKEN }}}}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ghcr.io/${{{{ github.repository }}}}
        tags: |
          type=ref,event=branch
          type=sha,prefix=${{{{github.ref_name}}}}-
          type=raw,value=latest,enable=${{{{is_default_branch}}}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{{{ steps.meta.outputs.tags }}}}
        labels: ${{{{ steps.meta.outputs.labels }}}}
        cache-from: type=gha
        cache-to: type=gha,mode=max
'''
        
        return workflow
    
    def generate_deploy_workflow(self) -> str:
        """Создать workflow для развертывания"""
        workflow = f'''name: Deploy

on:
  push:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
        aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
        aws-region: us-west-2
    
    - name: Deploy to ECS Staging
      run: |
        aws ecs update-service \\
          --cluster {self.project_name}-staging \\
          --service {self.project_name}-service \\
          --force-new-deployment
    
    - name: Wait for deployment
      run: |
        aws ecs wait services-stable \\
          --cluster {self.project_name}-staging \\
          --services {self.project_name}-service
    
    - name: Run smoke tests
      run: |
        curl -f https://staging.{self.project_name}.com/health
        # Add more smoke tests here

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.event_name == 'release'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
        aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
        aws-region: us-west-2
    
    - name: Deploy to ECS Production
      run: |
        aws ecs update-service \\
          --cluster {self.project_name}-production \\
          --service {self.project_name}-service \\
          --force-new-deployment
    
    - name: Wait for deployment
      run: |
        aws ecs wait services-stable \\
          --cluster {self.project_name}-production \\
          --services {self.project_name}-service
    
    - name: Run production smoke tests
      run: |
        curl -f https://{self.project_name}.com/health
    
    - name: Notify Slack
      uses: 8398a7/action-slack@v3
      with:
        status: ${{{{ job.status }}}}
        channel: '#deployments'
        webhook_url: ${{{{ secrets.SLACK_WEBHOOK }}}}
      if: always()
'''
        
        return workflow
    
    def generate_release_workflow(self) -> str:
        """Создать workflow для релизов"""
        workflow = '''name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
    
    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      with:
        files: dist/*
        generate_release_notes: true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'''
        
        return workflow

# Тесты для CI/CD генератора
class TestCIPipelineGenerator:
    """Тесты генератора CI/CD pipeline"""
    
    def test_test_workflow_generation(self):
        """Тест генерации workflow для тестирования"""
        generator = CIPipelineGeneratorSolution("myproject")
        workflow = generator.generate_test_workflow()
        
        assert "Test and Quality Check" in workflow
        assert "matrix:" in workflow
        assert "python-version" in workflow
        assert "pytest" in workflow
        assert "black --check" in workflow
        assert "flake8" in workflow
        assert "mypy" in workflow
        assert "bandit" in workflow
    
    def test_deploy_workflow_generation(self):
        """Тест генерации workflow для развертывания"""
        generator = CIPipelineGeneratorSolution("myproject")
        workflow = generator.generate_deploy_workflow()
        
        assert "Deploy" in workflow
        assert "deploy-staging" in workflow
        assert "deploy-production" in workflow
        assert "aws ecs update-service" in workflow
        assert "environment: staging" in workflow
        assert "environment: production" in workflow

# =============================================================================
# Запуск упражнений
# =============================================================================

def run_exercises():
    """Запуск всех упражнений"""
    print("=== Упражнения: Пакетирование и развертывание ===\n")
    
    # Демонстрация создания пакета
    print("1. Создание Python пакета...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        metadata = PackageMetadata(
            name="mathutils",
            description="Mathematical utilities package",
            author="Demo Author",
            author_email="demo@example.com"
        )
        
        creator = PackageCreatorSolution("mathutils", Path(tmp_dir), metadata)
        creator.create_structure()
        
        # Проверяем созданную структуру
        package_dir = Path(tmp_dir) / "mathutils"
        created_files = list(package_dir.rglob("*"))
        print(f"   Создано файлов: {len([f for f in created_files if f.is_file()])}")
        print(f"   Создано директорий: {len([f for f in created_files if f.is_dir()])}")
    
    # Демонстрация Docker приложения
    print("\n2. Docker приложение...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        docker_app = DockerizedFlaskAppSolution("demoapp", Path(tmp_dir))
        docker_app.build_complete_app()
        
        app_dir = Path(tmp_dir)
        docker_files = ["Dockerfile", "docker-compose.yml", "app.py", "requirements.txt"]
        created_docker_files = [f for f in docker_files if (app_dir / f).exists()]
        print(f"   Создано Docker файлов: {len(created_docker_files)}")
    
    # Демонстрация CI/CD pipeline
    print("\n3. CI/CD Pipeline...")
    generator = CIPipelineGeneratorSolution("democproject")
    
    test_workflow = generator.generate_test_workflow()
    deploy_workflow = generator.generate_deploy_workflow()
    
    print(f"   Test workflow: {len(test_workflow.split('\\n'))} строк")
    print(f"   Deploy workflow: {len(deploy_workflow.split('\\n'))} строк")
    
    print("\n✅ Все упражнения выполнены успешно!")
    print("💡 Теперь вы можете создавать, упаковывать и развертывать Python приложения!")

if __name__ == "__main__":
    run_exercises() 