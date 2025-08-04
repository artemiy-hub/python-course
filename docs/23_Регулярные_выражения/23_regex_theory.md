# Теория: Регулярные выражения в Python

## 🎯 Цель раздела

Этот раздел охватывает все аспекты работы с регулярными выражениями в Python: от базового синтаксиса до продвинутых техник, оптимизации производительности и практических применений.

## 📋 Содержание

1. [Основы регулярных выражений](#основы-регулярных-выражений)
2. [Метасимволы и квантификаторы](#метасимволы-и-квантификаторы)
3. [Группы и захват](#группы-и-захват)
4. [Продвинутые техники](#продвинутые-техники)
5. [Практические применения](#практические-применения)
6. [Оптимизация производительности](#оптимизация-производительности)
7. [Альтернативы regex](#альтернативы-regex)

---

## 🎭 Основы регулярных выражений

Регулярные выражения - мощный инструмент для поиска и обработки текста по паттернам.

### Базовый синтаксис и модуль re

```python
import re
from typing import List, Dict, Optional, Union, Iterator, Tuple, Any
import time
from dataclasses import dataclass
from enum import Enum
import functools

class RegexPatterns:
    """Коллекция полезных регулярных выражений"""
    
    # Основные паттерны
    EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_RU = r'(?:\+7|8)[-.\s]?\(?(?:9\d{2}|[1-6]\d{2}|7[0-9][0-9])\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}'
    URL = r'https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?'
    IPV4 = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    IPV6 = r'(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}'
    
    # Форматы данных
    DATE_ISO = r'\d{4}-\d{2}-\d{2}'
    DATE_US = r'\d{1,2}/\d{1,2}/\d{4}'
    DATE_EU = r'\d{1,2}\.\d{1,2}\.\d{4}'
    TIME_24H = r'(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?'
    
    # Финансы
    PRICE = r'\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?'
    CREDIT_CARD = r'\b(?:\d{4}[-.\s]?){3}\d{4}\b'
    
    # Программирование
    PYTHON_VARIABLE = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    HEX_COLOR = r'#(?:[0-9a-fA-F]{3}){1,2}\b'
    
    # Безопасность
    SQL_INJECTION = r'(?i)(union|select|insert|update|delete|drop|create|alter|exec|execute)\s'
    XSS_BASIC = r'<script[^>]*>.*?</script>'

@dataclass
class RegexMatch:
    """Результат совпадения регулярного выражения"""
    text: str
    start: int
    end: int
    groups: List[str]
    named_groups: Dict[str, str]
    pattern: str

class RegexEngine:
    """Движок для работы с регулярными выражениями"""
    
    def __init__(self, case_sensitive: bool = True, multiline: bool = False, 
                 dotall: bool = False, unicode: bool = True):
        self.flags = 0
        
        if not case_sensitive:
            self.flags |= re.IGNORECASE
        if multiline:
            self.flags |= re.MULTILINE
        if dotall:
            self.flags |= re.DOTALL
        if unicode:
            self.flags |= re.UNICODE
        
        self._compiled_patterns = {}
    
    def compile_pattern(self, pattern: str) -> re.Pattern:
        """Компиляция и кэширование паттерна"""
        if pattern not in self._compiled_patterns:
            self._compiled_patterns[pattern] = re.compile(pattern, self.flags)
        return self._compiled_patterns[pattern]
    
    def search(self, pattern: str, text: str) -> Optional[RegexMatch]:
        """Поиск первого совпадения"""
        compiled_pattern = self.compile_pattern(pattern)
        match = compiled_pattern.search(text)
        
        if match:
            return RegexMatch(
                text=match.group(0),
                start=match.start(),
                end=match.end(),
                groups=list(match.groups()),
                named_groups=match.groupdict(),
                pattern=pattern
            )
        return None
    
    def find_all(self, pattern: str, text: str) -> List[RegexMatch]:
        """Поиск всех совпадений"""
        compiled_pattern = self.compile_pattern(pattern)
        matches = []
        
        for match in compiled_pattern.finditer(text):
            matches.append(RegexMatch(
                text=match.group(0),
                start=match.start(),
                end=match.end(),
                groups=list(match.groups()),
                named_groups=match.groupdict(),
                pattern=pattern
            ))
        
        return matches
    
    def substitute(self, pattern: str, replacement: str, text: str, 
                  count: int = 0) -> Tuple[str, int]:
        """Замена с подсчетом"""
        compiled_pattern = self.compile_pattern(pattern)
        result = compiled_pattern.subn(replacement, text, count=count)
        return result
    
    def split(self, pattern: str, text: str, max_split: int = 0) -> List[str]:
        """Разделение текста по паттерну"""
        compiled_pattern = self.compile_pattern(pattern)
        return compiled_pattern.split(text, maxsplit=max_split)
    
    def match_full(self, pattern: str, text: str) -> Optional[RegexMatch]:
        """Проверка полного совпадения"""
        compiled_pattern = self.compile_pattern(pattern)
        match = compiled_pattern.fullmatch(text)
        
        if match:
            return RegexMatch(
                text=match.group(0),
                start=match.start(),
                end=match.end(),
                groups=list(match.groups()),
                named_groups=match.groupdict(),
                pattern=pattern
            )
        return None

class TextValidator:
    """Валидатор текста с помощью регулярных выражений"""
    
    def __init__(self):
        self.engine = RegexEngine()
        self.validation_rules = {}
    
    def add_rule(self, name: str, pattern: str, description: str = "",
                error_message: str = "Недопустимый формат"):
        """Добавление правила валидации"""
        self.validation_rules[name] = {
            'pattern': pattern,
            'description': description,
            'error_message': error_message
        }
    
    def validate(self, rule_name: str, text: str) -> Dict[str, Any]:
        """Валидация текста по правилу"""
        if rule_name not in self.validation_rules:
            return {
                'valid': False,
                'error': f"Правило '{rule_name}' не найдено"
            }
        
        rule = self.validation_rules[rule_name]
        match = self.engine.match_full(rule['pattern'], text)
        
        return {
            'valid': match is not None,
            'error': None if match else rule['error_message'],
            'match': match
        }
    
    def validate_multiple(self, rules: List[str], text: str) -> Dict[str, Any]:
        """Валидация по нескольким правилам"""
        results = {}
        all_valid = True
        
        for rule_name in rules:
            result = self.validate(rule_name, text)
            results[rule_name] = result
            
            if not result['valid']:
                all_valid = False
        
        return {
            'all_valid': all_valid,
            'results': results
        }

# Предустановленные правила валидации
def setup_common_validators() -> TextValidator:
    """Настройка общих валидаторов"""
    validator = TextValidator()
    
    # Email
    validator.add_rule(
        'email',
        RegexPatterns.EMAIL,
        'Проверка email адреса',
        'Некорректный email адрес'
    )
    
    # Российский телефон
    validator.add_rule(
        'phone_ru',
        RegexPatterns.PHONE_RU,
        'Проверка российского номера телефона',
        'Некорректный номер телефона'
    )
    
    # URL
    validator.add_rule(
        'url',
        RegexPatterns.URL,
        'Проверка URL',
        'Некорректный URL'
    )
    
    # Пароль (минимум 8 символов, буквы и цифры)
    validator.add_rule(
        'password_basic',
        r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$',
        'Базовая проверка пароля',
        'Пароль должен содержать минимум 8 символов, включая буквы и цифры'
    )
    
    # Сильный пароль
    validator.add_rule(
        'password_strong',
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$',
        'Проверка сильного пароля',
        'Пароль должен содержать минимум 12 символов: строчные, заглавные буквы, цифры и спецсимволы'
    )
    
    # Имя пользователя
    validator.add_rule(
        'username',
        r'^[a-zA-Z0-9_]{3,20}$',
        'Проверка имени пользователя',
        'Имя пользователя должно содержать 3-20 символов (буквы, цифры, подчеркивание)'
    )
    
    # Российский ИНН
    validator.add_rule(
        'inn_ru',
        r'^\d{10}$|^\d{12}$',
        'Проверка российского ИНН',
        'ИНН должен содержать 10 или 12 цифр'
    )
    
    return validator

# Продвинутые техники
class AdvancedRegexTechniques:
    """Продвинутые техники работы с регулярными выражениями"""
    
    @staticmethod
    def lookahead_lookbehind_examples():
        """Примеры look-ahead и look-behind"""
        examples = {}
        
        # Positive lookahead - найти слово, за которым следует другое слово
        text = "Python is great, Java is good, JavaScript is popular"
        pattern = r'\w+(?=\s+is)'  # Слова перед "is"
        examples['positive_lookahead'] = {
            'pattern': pattern,
            'text': text,
            'matches': re.findall(pattern, text)
        }
        
        # Negative lookahead - найти слово, за которым НЕ следует другое слово
        pattern = r'\w+(?!\s+is)'  # Слова НЕ перед "is"
        examples['negative_lookahead'] = {
            'pattern': pattern,
            'text': text,
            'matches': re.findall(pattern, text)
        }
        
        # Positive lookbehind - найти слово, которому предшествует другое слово
        pattern = r'(?<=is\s)\w+'  # Слова после "is"
        examples['positive_lookbehind'] = {
            'pattern': pattern,
            'text': text,
            'matches': re.findall(pattern, text)
        }
        
        # Negative lookbehind - найти слово, которому НЕ предшествует другое слово
        pattern = r'(?<!is\s)\w+'  # Слова НЕ после "is"
        examples['negative_lookbehind'] = {
            'pattern': pattern,
            'text': text,
            'matches': re.findall(pattern, text)
        }
        
        return examples
    
    @staticmethod
    def greedy_vs_lazy():
        """Сравнение жадного и ленивого поиска"""
        text = '<div>content1</div><div>content2</div>'
        
        # Жадный поиск
        greedy_pattern = r'<div>.*</div>'
        greedy_match = re.search(greedy_pattern, text)
        
        # Ленивый поиск
        lazy_pattern = r'<div>.*?</div>'
        lazy_matches = re.findall(lazy_pattern, text)
        
        return {
            'text': text,
            'greedy': {
                'pattern': greedy_pattern,
                'result': greedy_match.group(0) if greedy_match else None
            },
            'lazy': {
                'pattern': lazy_pattern,
                'results': lazy_matches
            }
        }
    
    @staticmethod
    def named_groups_example():
        """Пример использования именованных групп"""
        text = "Дата: 2024-01-15, Время: 14:30:00"
        pattern = r'Дата: (?P<date>\d{4}-\d{2}-\d{2}), Время: (?P<time>\d{2}:\d{2}:\d{2})'
        
        match = re.search(pattern, text)
        
        if match:
            return {
                'pattern': pattern,
                'text': text,
                'full_match': match.group(0),
                'date': match.group('date'),
                'time': match.group('time'),
                'all_groups': match.groupdict()
            }
        
        return None
    
    @staticmethod
    def conditional_patterns():
        """Условные паттерны"""
        # Паттерн для номера телефона с международным кодом или без
        pattern = r'(?P<country>\+\d{1,3}[-.\s]?)?(?P<area>\(?\d{3}\)?[-.\s]?)(?P<number>\d{3}[-.\s]?\d{4})'
        
        test_numbers = [
            "+7 (495) 123-4567",
            "495 123-4567",
            "+1-555-123-4567",
            "123-4567"
        ]
        
        results = []
        for number in test_numbers:
            match = re.search(pattern, number)
            if match:
                results.append({
                    'number': number,
                    'groups': match.groupdict(),
                    'has_country': bool(match.group('country'))
                })
        
        return {
            'pattern': pattern,
            'results': results
        }

class TextProcessor:
    """Процессор текста с использованием регулярных выражений"""
    
    def __init__(self):
        self.engine = RegexEngine()
    
    def extract_emails(self, text: str) -> List[str]:
        """Извлечение email адресов"""
        matches = self.engine.find_all(RegexPatterns.EMAIL, text)
        return [match.text for match in matches]
    
    def extract_phones(self, text: str, country: str = 'ru') -> List[str]:
        """Извлечение номеров телефонов"""
        if country == 'ru':
            pattern = RegexPatterns.PHONE_RU
        else:
            # Общий международный паттерн
            pattern = r'\+?[1-9]\d{1,14}'
        
        matches = self.engine.find_all(pattern, text)
        return [match.text for match in matches]
    
    def extract_urls(self, text: str) -> List[str]:
        """Извлечение URL"""
        matches = self.engine.find_all(RegexPatterns.URL, text)
        return [match.text for match in matches]
    
    def extract_dates(self, text: str, format_type: str = 'iso') -> List[str]:
        """Извлечение дат"""
        patterns = {
            'iso': RegexPatterns.DATE_ISO,
            'us': RegexPatterns.DATE_US,
            'eu': RegexPatterns.DATE_EU
        }
        
        pattern = patterns.get(format_type, RegexPatterns.DATE_ISO)
        matches = self.engine.find_all(pattern, text)
        return [match.text for match in matches]
    
    def clean_html(self, text: str) -> str:
        """Удаление HTML тегов"""
        # Удаляем скрипты и стили полностью
        text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Удаляем обычные HTML теги
        text = re.sub(r'<[^>]+>', '', text)
        
        # Декодируем HTML entities
        html_entities = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&nbsp;': ' '
        }
        
        for entity, char in html_entities.items():
            text = text.replace(entity, char)
        
        return text.strip()
    
    def normalize_whitespace(self, text: str) -> str:
        """Нормализация пробелов"""
        # Заменяем множественные пробелы одним
        text = re.sub(r'\s+', ' ', text)
        
        # Удаляем пробелы в начале и конце строк
        text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
        
        return text
    
    def extract_mentions(self, text: str) -> List[str]:
        """Извлечение упоминаний (@username)"""
        pattern = r'@([a-zA-Z0-9_]+)'
        matches = self.engine.find_all(pattern, text)
        return [match.groups[0] for match in matches]
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Извлечение хештегов"""
        pattern = r'#([a-zA-Z0-9_]+)'
        matches = self.engine.find_all(pattern, text)
        return [match.groups[0] for match in matches]
    
    def mask_sensitive_data(self, text: str) -> str:
        """Маскировка чувствительных данных"""
        # Маскируем номера карт
        text = re.sub(RegexPatterns.CREDIT_CARD, 
                     lambda m: m.group(0)[:4] + '*' * (len(m.group(0)) - 8) + m.group(0)[-4:], 
                     text)
        
        # Маскируем email (оставляем первую букву и домен)
        text = re.sub(RegexPatterns.EMAIL,
                     lambda m: m.group(0)[0] + '*' * (m.group(0).find('@') - 1) + m.group(0)[m.group(0).find('@'):],
                     text)
        
        # Маскируем телефоны
        text = re.sub(RegexPatterns.PHONE_RU,
                     lambda m: m.group(0)[:3] + '*' * (len(re.sub(r'[^\d]', '', m.group(0))) - 6) + m.group(0)[-3:],
                     text)
        
        return text

class RegexPerformanceAnalyzer:
    """Анализатор производительности регулярных выражений"""
    
    def __init__(self):
        self.results = {}
    
    def benchmark_pattern(self, pattern: str, text: str, iterations: int = 1000) -> Dict[str, Any]:
        """Бенчмарк паттерна"""
        # Тест без компиляции
        start_time = time.time()
        for _ in range(iterations):
            re.search(pattern, text)
        uncompiled_time = time.time() - start_time
        
        # Тест с компиляцией
        compiled_pattern = re.compile(pattern)
        start_time = time.time()
        for _ in range(iterations):
            compiled_pattern.search(text)
        compiled_time = time.time() - start_time
        
        # Тест findall
        start_time = time.time()
        for _ in range(iterations // 10):  # Меньше итераций для findall
            compiled_pattern.findall(text)
        findall_time = (time.time() - start_time) * 10  # Нормализуем
        
        return {
            'pattern': pattern,
            'text_length': len(text),
            'iterations': iterations,
            'uncompiled_time': uncompiled_time,
            'compiled_time': compiled_time,
            'findall_time': findall_time,
            'speedup_compilation': uncompiled_time / compiled_time if compiled_time > 0 else 0,
            'matches_found': len(compiled_pattern.findall(text))
        }
    
    def compare_patterns(self, patterns: List[str], text: str) -> Dict[str, Any]:
        """Сравнение производительности нескольких паттернов"""
        results = {}
        
        for i, pattern in enumerate(patterns):
            try:
                result = self.benchmark_pattern(pattern, text)
                results[f'pattern_{i}'] = result
            except re.error as e:
                results[f'pattern_{i}'] = {
                    'pattern': pattern,
                    'error': str(e)
                }
        
        return results
    
    def analyze_complexity(self, pattern: str) -> Dict[str, Any]:
        """Анализ сложности паттерна"""
        analysis = {
            'pattern': pattern,
            'length': len(pattern),
            'metacharacters': 0,
            'quantifiers': 0,
            'groups': 0,
            'character_classes': 0,
            'anchors': 0,
            'lookarounds': 0,
            'complexity_score': 0
        }
        
        # Подсчет метасимволов
        metacharacters = r'\.^$*+?{}[]|()'
        analysis['metacharacters'] = sum(1 for char in pattern if char in metacharacters)
        
        # Подсчет квантификаторов
        quantifiers = ['*', '+', '?', '{']
        analysis['quantifiers'] = sum(1 for char in pattern if char in quantifiers)
        
        # Подсчет групп
        analysis['groups'] = pattern.count('(')
        
        # Подсчет символьных классов
        analysis['character_classes'] = pattern.count('[')
        
        # Подсчет якорей
        anchors = ['^', '$', r'\b', r'\B']
        analysis['anchors'] = sum(pattern.count(anchor) for anchor in anchors)
        
        # Подсчет lookaround
        lookarounds = ['(?=', '(?!', '(?<=', '(?<!']
        analysis['lookarounds'] = sum(pattern.count(look) for look in lookarounds)
        
        # Простая оценка сложности
        analysis['complexity_score'] = (
            analysis['metacharacters'] +
            analysis['quantifiers'] * 2 +
            analysis['groups'] * 1.5 +
            analysis['character_classes'] * 1.2 +
            analysis['anchors'] * 0.5 +
            analysis['lookarounds'] * 3
        )
        
        return analysis

class RegexDebugger:
    """Отладчик регулярных выражений"""
    
    def __init__(self):
        self.debug_info = {}
    
    def explain_pattern(self, pattern: str) -> Dict[str, Any]:
        """Объяснение паттерна"""
        explanation = {
            'pattern': pattern,
            'components': [],
            'flags': [],
            'groups': []
        }
        
        # Простой анализ компонентов (базовая версия)
        i = 0
        while i < len(pattern):
            char = pattern[i]
            
            if char == '\\' and i + 1 < len(pattern):
                next_char = pattern[i + 1]
                if next_char == 'd':
                    explanation['components'].append({
                        'position': i,
                        'pattern': '\\d',
                        'meaning': 'Любая цифра (0-9)'
                    })
                elif next_char == 'w':
                    explanation['components'].append({
                        'position': i,
                        'pattern': '\\w',
                        'meaning': 'Любой буквенно-цифровой символ'
                    })
                elif next_char == 's':
                    explanation['components'].append({
                        'position': i,
                        'pattern': '\\s',
                        'meaning': 'Любой пробельный символ'
                    })
                i += 2
            
            elif char == '.':
                explanation['components'].append({
                    'position': i,
                    'pattern': '.',
                    'meaning': 'Любой символ кроме новой строки'
                })
                i += 1
            
            elif char == '*':
                explanation['components'].append({
                    'position': i,
                    'pattern': '*',
                    'meaning': 'Ноль или больше повторений предыдущего элемента'
                })
                i += 1
            
            elif char == '+':
                explanation['components'].append({
                    'position': i,
                    'pattern': '+',
                    'meaning': 'Один или больше повторений предыдущего элемента'
                })
                i += 1
            
            elif char == '?':
                explanation['components'].append({
                    'position': i,
                    'pattern': '?',
                    'meaning': 'Ноль или одно повторение предыдущего элемента'
                })
                i += 1
            
            elif char == '^':
                explanation['components'].append({
                    'position': i,
                    'pattern': '^',
                    'meaning': 'Начало строки'
                })
                i += 1
            
            elif char == '$':
                explanation['components'].append({
                    'position': i,
                    'pattern': '$',
                    'meaning': 'Конец строки'
                })
                i += 1
            
            else:
                i += 1
        
        return explanation
    
    def test_pattern(self, pattern: str, test_strings: List[str]) -> Dict[str, Any]:
        """Тестирование паттерна на множестве строк"""
        results = {
            'pattern': pattern,
            'tests': []
        }
        
        try:
            compiled_pattern = re.compile(pattern)
            
            for test_string in test_strings:
                match = compiled_pattern.search(test_string)
                
                test_result = {
                    'string': test_string,
                    'matches': match is not None,
                    'match_text': match.group(0) if match else None,
                    'match_groups': list(match.groups()) if match else [],
                    'match_position': (match.start(), match.end()) if match else None
                }
                
                results['tests'].append(test_result)
                
        except re.error as e:
            results['error'] = str(e)
        
        return results

def demonstrate_regex_capabilities():
    """Демонстрация возможностей регулярных выражений"""
    print("🎭 Демонстрация регулярных выражений")
    print("=" * 50)
    
    # Создаем компоненты
    engine = RegexEngine(case_sensitive=False)
    validator = setup_common_validators()
    processor = TextProcessor()
    analyzer = RegexPerformanceAnalyzer()
    debugger = RegexDebugger()
    
    # Тестовый текст
    test_text = """
    Контакты:
    Email: john.doe@example.com, admin@site.ru
    Телефон: +7 (495) 123-45-67, 8-800-555-35-35
    Сайт: https://example.com/page?id=123
    Дата встречи: 2024-01-15
    Время: 14:30:00
    
    #python #regex @developer
    """
    
    print("\n📧 Извлеченные email:")
    emails = processor.extract_emails(test_text)
    for email in emails:
        print(f"  • {email}")
    
    print("\n📞 Извлеченные телефоны:")
    phones = processor.extract_phones(test_text)
    for phone in phones:
        print(f"  • {phone}")
    
    print("\n🌐 Извлеченные URL:")
    urls = processor.extract_urls(test_text)
    for url in urls:
        print(f"  • {url}")
    
    print("\n📅 Извлеченные даты:")
    dates = processor.extract_dates(test_text)
    for date in dates:
        print(f"  • {date}")
    
    print("\n#️⃣ Хештеги и упоминания:")
    hashtags = processor.extract_hashtags(test_text)
    mentions = processor.extract_mentions(test_text)
    print(f"  Хештеги: {hashtags}")
    print(f"  Упоминания: {mentions}")
    
    # Валидация
    print("\n✅ Валидация данных:")
    test_cases = [
        ('email', 'user@example.com'),
        ('email', 'invalid-email'),
        ('password_strong', 'MyPass123!@#'),
        ('password_strong', '123456'),
    ]
    
    for rule, test_value in test_cases:
        result = validator.validate(rule, test_value)
        status = "✅" if result['valid'] else "❌"
        print(f"  {status} {rule}: '{test_value}' - {result.get('error', 'OK')}")
    
    # Продвинутые техники
    print("\n🔍 Продвинутые техники:")
    lookahead_examples = AdvancedRegexTechniques.lookahead_lookbehind_examples()
    print(f"  Positive lookahead найдено: {len(lookahead_examples['positive_lookahead']['matches'])} совпадений")
    
    greedy_lazy = AdvancedRegexTechniques.greedy_vs_lazy()
    print(f"  Жадный поиск: {len(greedy_lazy['greedy']['result']) if greedy_lazy['greedy']['result'] else 0} символов")
    print(f"  Ленивый поиск: {len(greedy_lazy['lazy']['results'])} совпадений")
    
    # Анализ производительности
    print("\n⚡ Анализ производительности:")
    performance = analyzer.benchmark_pattern(RegexPatterns.EMAIL, test_text * 100)
    print(f"  Ускорение от компиляции: {performance['speedup_compilation']:.2f}x")
    print(f"  Найдено совпадений: {performance['matches_found']}")
    
    return {
        'emails': emails,
        'phones': phones,
        'urls': urls,
        'dates': dates,
        'hashtags': hashtags,
        'mentions': mentions,
        'performance': performance
    }

# Альтернативы регулярным выражениям
class RegexAlternatives:
    """Альтернативы регулярным выражениям для специфических задач"""
    
    @staticmethod
    def parse_csv_simple(text: str) -> List[List[str]]:
        """Простой парсер CSV без regex"""
        import csv
        import io
        
        reader = csv.reader(io.StringIO(text))
        return list(reader)
    
    @staticmethod
    def extract_urls_simple(text: str) -> List[str]:
        """Простое извлечение URL без regex"""
        urls = []
        words = text.split()
        
        for word in words:
            if word.startswith(('http://', 'https://', 'www.')):
                # Удаляем знаки препинания в конце
                url = word.rstrip('.,!?;')
                urls.append(url)
        
        return urls
    
    @staticmethod
    def validate_email_simple(email: str) -> bool:
        """Простая валидация email без regex"""
        # Базовая проверка структуры
        if email.count('@') != 1:
            return False
        
        local, domain = email.split('@')
        
        # Проверка локальной части
        if not local or len(local) > 64:
            return False
        
        # Проверка домена
        if not domain or '.' not in domain:
            return False
        
        # Проверка на допустимые символы (упрощенно)
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_')
        
        if not all(c in allowed_chars for c in email):
            return False
        
        return True
    
    @staticmethod
    def performance_comparison():
        """Сравнение производительности regex vs альтернатив"""
        test_text = "Contact us at: admin@example.com, support@test.org, or visit https://example.com"
        
        # Тест извлечения URL
        iterations = 10000
        
        # Regex метод
        start_time = time.time()
        for _ in range(iterations):
            re.findall(RegexPatterns.URL, test_text)
        regex_time = time.time() - start_time
        
        # Простой метод
        start_time = time.time()
        for _ in range(iterations):
            RegexAlternatives.extract_urls_simple(test_text)
        simple_time = time.time() - start_time
        
        return {
            'regex_time': regex_time,
            'simple_time': simple_time,
            'speedup': regex_time / simple_time if simple_time > 0 else 0
        }

if __name__ == "__main__":
    # Демонстрация всех возможностей
    results = demonstrate_regex_capabilities()
    
    print("\n🔄 Сравнение с альтернативами:")
    comparison = RegexAlternatives.performance_comparison()
    print(f"  Regex время: {comparison['regex_time']:.4f}s")
    print(f"  Простой метод: {comparison['simple_time']:.4f}s")
    
    if comparison['speedup'] > 1:
        print(f"  Простой метод быстрее в {comparison['speedup']:.2f} раз")
    else:
        print(f"  Regex быстрее в {1/comparison['speedup']:.2f} раз") 