# 23_Регулярные_выражения

## Файлы примеров

- **regex_basics.py** — основы регулярных выражений
- **regex_patterns.py** — распространённые паттерны
- **regex_groups.py** — группы и захваты
- **regex_advanced.py** — продвинутые возможности
- **text_processing.py** — обработка текста с regex
- **validation_examples.py** — валидация данных
- **regex_performance.py** — производительность и оптимизация

## Темы

### Основы regex
- Модуль re
- Функции search, match, findall, finditer
- Компиляция паттернов
- Флаги (re.IGNORECASE, re.MULTILINE, etc.)
- Raw strings (r"pattern")

### Метасимволы
- . (любой символ)
- ^ (начало строки)
- $ (конец строки)
- * (0 или больше)
- + (1 или больше)
- ? (0 или 1)
- {n,m} (от n до m раз)

### Символьные классы
- [abc] (любой из символов)
- [^abc] (любой кроме этих)
- [a-z] (диапазон)
- \d, \w, \s (предопределённые классы)
- \D, \W, \S (отрицание классов)

### Группы и захваты
- (pattern) - захватывающие группы
- (?:pattern) - незахватывающие группы
- (?P<name>pattern) - именованные группы
- Обратные ссылки (\1, \2)
- Условные группы

### Lookahead и Lookbehind
- (?=pattern) - positive lookahead
- (?!pattern) - negative lookahead
- (?<=pattern) - positive lookbehind
- (?<!pattern) - negative lookbehind

### Замены
- re.sub() для замен
- Обратные ссылки в заменах
- Функции как замена
- re.subn() с подсчётом замен

### Практические применения
- Валидация email, телефонов, URL
- Парсинг логов и данных
- Очистка и форматирование текста
- Извлечение информации
- Поиск и замена в файлах

## Установка зависимостей

```bash
# Модуль re встроен в Python
# Дополнительные инструменты для работы с regex
pip install regex  # Расширенный модуль regex

# Для тестирования и отладки
pip install pytest

# Для работы с большими текстами
pip install chardet  # Определение кодировки
```

## Как использовать

1. Изучите основные метасимволы
2. Практикуйте простые паттерны
3. Освойте группы и захваты
4. Изучите lookahead/lookbehind
5. Применяйте для валидации данных
6. Оптимизируйте производительность

## Полезные онлайн инструменты

- regex101.com - тестирование и объяснение regex
- regexr.com - интерактивный редактор
- regexpal.com - простой тестер
- debuggex.com - визуализация regex

## Популярные паттерны

```python
# Email
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Телефон (российский формат)
phone_pattern = r'\+?[78][-.\s]?\(?9\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}'

# URL
url_pattern = r'https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?'

# IP адрес
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# Дата (DD.MM.YYYY)
date_pattern = r'\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d\b'
```

## Полезные ресурсы

- Python re документация: https://docs.python.org/3/library/re.html
- Regular-Expressions.info: https://www.regular-expressions.info/
- RegexOne tutorial: https://regexone.com/
- Python Regex Howto: https://docs.python.org/3/howto/regex.html 