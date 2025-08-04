# 22_Логирование_и_мониторинг

## Файлы примеров

- **logging_basics.py** — основы модуля logging
- **advanced_logging.py** — продвинутое логирование
- **structured_logging.py** — структурированное логирование
- **performance_monitoring.py** — мониторинг производительности
- **error_tracking.py** — отслеживание ошибок
- **log_analysis.py** — анализ логов
- **metrics_collection.py** — сбор метрик

## Темы

### Модуль logging
- Логгеры, обработчики, форматтеры
- Уровни логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Иерархия логгеров
- Конфигурация через код и файлы
- Ротация логов

### Обработчики (Handlers)
- StreamHandler для консоли
- FileHandler для файлов
- RotatingFileHandler для ротации
- TimedRotatingFileHandler по времени
- SMTPHandler для email уведомлений
- SysLogHandler для системных логов

### Форматирование
- Основные форматы логов
- Временные метки
- Уровни логирования
- Контекстная информация
- JSON форматирование

### Структурированное логирование
- JSON логи
- Контекстные поля
- Корреляционные ID
- Метаданные запросов
- Трассировка вызовов

### Мониторинг производительности
- Измерение времени выполнения
- Профилирование кода
- Мониторинг памяти
- CPU утилизация
- I/O операции

### Централизованное логирование
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Fluentd и Fluentbit
- Graylog
- Centralized logging patterns
- Log aggregation

### Метрики и алертинг
- Prometheus и Grafana
- StatsD метрики
- Счётчики, гистограммы, гауges
- Health checks
- Alerting правила

## Установка зависимостей

```bash
# Основные библиотеки
pip install structlog python-json-logger

# Мониторинг
pip install psutil memory-profiler

# Продвинутые инструменты
pip install prometheus-client statsd

# ELK интеграция
pip install elasticsearch-dsl python-logstash
```

## Как использовать

1. Изучите основы модуля logging
2. Настройте структурированное логирование
3. Реализуйте мониторинг производительности
4. Настройте централизованный сбор логов
5. Создайте дашборды для мониторинга
6. Настройте алертинг на критические события

## Конфигурация logging

```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

## Полезные ресурсы

- Python logging документация: https://docs.python.org/3/library/logging.html
- Twelve-Factor App Logs: https://12factor.net/logs
- Prometheus документация: https://prometheus.io/docs/
- ELK Stack: https://www.elastic.co/what-is/elk-stack 