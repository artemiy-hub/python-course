# 15_Современный_Python

## Файлы примеров

- **walrus_operator.py** — оператор "морж" (:=) Python 3.8+
- **positional_only.py** — позиционные и keyword-only параметры
- **f_strings_advanced.py** — продвинутые f-strings с отладкой
- **match_case.py** — структурное сопоставление образцов Python 3.10+
- **modern_features.py** — сборник современных возможностей
- **type_union.py** — новый синтаксис Union типов (X | Y)

## Темы

### Python 3.8+
- Walrus operator (:=) для присваивания в выражениях
- Positional-only параметры (/)
- f-strings с = для отладки
- math.prod() для произведения
- Улучшения в typing

### Python 3.9+
- dict merge операторы (| и |=)
- str.removeprefix() и str.removesuffix()
- Новый синтаксис типов (list[int] вместо List[int])
- typing.Annotated
- functools.cache декоратор

### Python 3.10+
- Structural Pattern Matching (match/case)
- Union types с | синтаксисом
- Улучшенные сообщения об ошибках
- Новые функции в statistics

### Python 3.11+
- Exception Groups и except*
- Улучшенная производительность
- TOML support в томllib
- Новые возможности typing

## Как использовать

1. Убедитесь, что используете Python 3.8+
2. Запускайте файлы для изучения новых возможностей
3. Экспериментируйте с синтаксисом
4. Сравнивайте со старыми подходами

## Проверка версии

```python
import sys
print(f"Python версия: {sys.version}")

# Для конкретных возможностей
if sys.version_info >= (3, 8):
    print("Walrus operator доступен")
if sys.version_info >= (3, 10):
    print("Match/case доступен")
``` 