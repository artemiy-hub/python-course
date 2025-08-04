# 16_Веб_разработка

## Файлы примеров

- **flask_basics.py** — основы Flask веб-фреймворка
- **fastapi_example.py** — современный FastAPI фреймворк
- **requests_http.py** — HTTP клиент и работа с API
- **web_scraping.py** — веб-скрейпинг с requests и BeautifulSoup
- **json_api.py** — работа с JSON API
- **templates_example.py** — шаблоны Jinja2
- **simple_server.py** — простой HTTP сервер

## Темы

### Flask
- Основы маршрутизации
- Шаблоны Jinja2
- Обработка форм
- Статические файлы
- Сессии и cookies
- Обработка ошибок

### FastAPI
- Современный асинхронный фреймворк
- Автоматическая документация (OpenAPI/Swagger)
- Валидация данных с Pydantic
- Dependency Injection
- WebSocket поддержка

### HTTP клиент
- GET, POST, PUT, DELETE запросы
- Заголовки и параметры
- Аутентификация
- Обработка ответов
- Работа с cookies и сессиями

### Веб-скрейпинг
- Парсинг HTML с BeautifulSoup
- CSS селекторы
- Обход anti-bot защиты
- Работа с формами
- Обработка динамического контента

### REST API
- Принципы REST
- JSON формат данных
- Статус коды HTTP
- Версионирование API
- Документирование API

## Установка зависимостей

```bash
pip install flask fastapi uvicorn requests beautifulsoup4 jinja2 lxml
```

## Как использовать

1. Установите зависимости
2. Запустите Flask приложения: `python flask_basics.py`
3. Запустите FastAPI: `uvicorn fastapi_example:app --reload`
4. Изучайте примеры HTTP клиента и скрейпинга

## Полезные ресурсы

- Flask документация: https://flask.palletsprojects.com/
- FastAPI документация: https://fastapi.tiangolo.com/
- Requests документация: https://docs.python-requests.org/
- BeautifulSoup документация: https://www.crummy.com/software/BeautifulSoup/ 