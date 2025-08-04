# 18_Тестирование

## Файлы примеров

- **unittest_basics.py** — основы модуля unittest
- **pytest_examples.py** — современное тестирование с pytest
- **mock_examples.py** — моки и патчинг
- **fixtures_examples.py** — фикстуры и настройка тестов
- **tdd_example.py** — разработка через тестирование (TDD)
- **coverage_example.py** — анализ покрытия кода
- **integration_tests.py** — интеграционные тесты

## Темы

### unittest
- Базовые тест-кейсы (TestCase)
- Методы assert (assertEqual, assertTrue, etc.)
- setUp и tearDown
- Тестовые наборы (TestSuite)
- Запуск тестов

### pytest
- Современный фреймворк тестирования
- Простой синтаксис assert
- Фикстуры и их области видимости
- Параметризованные тесты
- Плагины и настройка

### Моки и патчинг
- unittest.mock модуль
- Mock, MagicMock объекты
- Патчинг функций и классов
- Тестирование внешних зависимостей
- Моки для API и файловых операций

### TDD (Test-Driven Development)
- Красный-Зелёный-Рефакторинг цикл
- Написание тестов перед кодом
- Инкрементальная разработка
- Преимущества и недостатки

### Покрытие кода
- coverage.py для анализа
- Метрики покрытия
- Отчёты в разных форматах
- Интеграция с CI/CD

### Типы тестов
- Модульные (unit) тесты
- Интеграционные тесты
- Функциональные тесты
- Тесты производительности

## Установка зависимостей

```bash
# Основные пакеты для тестирования
pip install pytest pytest-cov pytest-mock

# Дополнительные инструменты
pip install coverage factory-boy faker

# Для веб-тестирования
pip install requests-mock httpretty
```

## Как использовать

1. Установите зависимости
2. Изучите основы unittest (встроен в Python)
3. Перейдите к pytest для более удобного тестирования
4. Практикуйте TDD подход
5. Анализируйте покрытие кода

## Команды для запуска тестов

```bash
# unittest
python -m unittest test_module.py
python -m unittest discover

# pytest
pytest
pytest test_file.py
pytest -v  # подробный вывод
pytest --cov=mymodule  # с покрытием

# coverage
coverage run -m pytest
coverage report
coverage html
```

## Полезные ресурсы

- pytest документация: https://docs.pytest.org/
- unittest документация: https://docs.python.org/3/library/unittest.html
- coverage.py: https://coverage.readthedocs.io/ 