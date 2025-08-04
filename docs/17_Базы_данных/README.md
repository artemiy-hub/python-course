# 17_Базы_данных

## Файлы примеров

- **sqlite_basics.py** — основы работы с SQLite
- **sqlalchemy_orm.py** — ORM SQLAlchemy
- **database_models.py** — модели данных и связи
- **migrations_example.py** — миграции базы данных
- **database_connection.py** — подключение к разным БД
- **crud_operations.py** — операции CRUD
- **transactions_example.py** — работа с транзакциями

## Темы

### SQLite
- Встроенная база данных Python
- Создание таблиц и индексов
- SQL запросы (SELECT, INSERT, UPDATE, DELETE)
- Работа с курсорами
- Обработка ошибок

### SQLAlchemy ORM
- Object-Relational Mapping
- Декларативные модели
- Сессии и запросы
- Связи между таблицами (один-к-одному, один-ко-многим, многие-ко-многим)
- Ленивая загрузка (lazy loading)

### Подключение к БД
- SQLite, PostgreSQL, MySQL
- Строки подключения
- Пулы соединений
- Настройка драйверов

### Миграции
- Alembic для SQLAlchemy
- Версионирование схемы
- Создание и применение миграций
- Откат изменений

### Продвинутые возможности
- Транзакции и ACID
- Индексы и оптимизация
- Хранимые процедуры
- Резервное копирование

## Установка зависимостей

```bash
# Основные пакеты
pip install sqlalchemy alembic

# Драйверы для разных БД
pip install psycopg2-binary  # PostgreSQL
pip install pymysql         # MySQL
pip install sqlite3         # Встроен в Python
```

## Как использовать

1. Установите зависимости
2. Изучите примеры с SQLite (не требует установки)
3. Настройте подключение к внешним БД при необходимости
4. Практикуйте CRUD операции и миграции

## Полезные ресурсы

- SQLAlchemy документация: https://docs.sqlalchemy.org/
- SQLite документация: https://sqlite.org/docs.html
- Alembic документация: https://alembic.sqlalchemy.org/ 