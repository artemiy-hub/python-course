# Многоэтапная сборка Docker для Python приложения

# Этап 1: Базовый образ для разработки
FROM python:3.11-slim as base

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя приложения
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Установка рабочей директории
WORKDIR /app

# Копирование требований
COPY requirements.txt requirements-dev.txt ./

# Обновление pip и установка зависимостей
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Этап 2: Разработка
FROM base as development

# Установка зависимостей для разработки
RUN pip install --no-cache-dir -r requirements-dev.txt

# Копирование исходного кода
COPY --chown=appuser:appuser . .

# Переключение на пользователя приложения
USER appuser

# Команда по умолчанию для разработки
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000", "--debug"]

# Этап 3: Тестирование
FROM development as testing

# Запуск тестов
RUN python -m pytest tests/ --verbose --cov=src/

# Этап 4: Продакшн
FROM python:3.11-slim as production

# Установка только необходимых системных пакетов
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя приложения
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Установка рабочей директории
WORKDIR /app

# Копирование только requirements.txt для продакшн
COPY requirements.txt .

# Установка только продакшн зависимостей
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

# Копирование приложения
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser app.py .

# Переключение на пользователя приложения
USER appuser

# Открытие порта
EXPOSE 8000

# Настройка переменных окружения
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Проверка здоровья
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Команда запуска для продакшн
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"] 