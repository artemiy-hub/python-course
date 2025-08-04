"""
Упражнения: Регулярные выражения

Этот файл содержит практические упражнения для изучения регулярных выражений
в Python, включая валидацию, парсинг, поиск паттернов и обработку текста.
"""

import re
import time
from typing import Dict, List, Optional, Any, Tuple, Pattern
from dataclasses import dataclass
import json
import pytest
from pathlib import Path
import tempfile

# =============================================================================
# Упражнение 1: Form Validation System
# =============================================================================

"""
ЗАДАНИЕ 1: Form Validation System

Создайте систему валидации форм с использованием регулярных выражений:

1. Класс FormValidator с методами для валидации:
   - validate_username() - имя пользователя (3-20 символов, буквы, цифры, _)
   - validate_email() - email с поддержкой internationalized domains
   - validate_phone() - телефон в различных форматах
   - validate_password() - сложный пароль
   - validate_date() - дата в различных форматах
   - validate_url() - URL с различными протоколами

2. Расширенная валидация:
   - Проверка на disposable email domains
   - Валидация международных номеров телефонов
   - Проверка силы пароля с детальным анализом
   - Поддержка различных форматов дат

3. Система отчетов:
   - Детальные сообщения об ошибках
   - Предложения по улучшению
   - Статистика валидации
"""

# Ваш код здесь:
class FormValidator:
    """Валидатор форм с регулярными выражениями"""
    
    def __init__(self):
        # TODO: Реализуйте инициализацию с паттернами
        pass
    
    def validate_username(self, username: str) -> Dict[str, Any]:
        """Валидация имени пользователя"""
        # TODO: Реализуйте метод
        pass
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """Валидация email"""
        # TODO: Реализуйте метод
        pass
    
    def validate_phone(self, phone: str) -> Dict[str, Any]:
        """Валидация телефона"""
        # TODO: Реализуйте метод
        pass
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """Валидация пароля"""
        # TODO: Реализуйте метод
        pass
    
    def validate_form(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """Валидация всей формы"""
        # TODO: Реализуйте метод
        pass

# Решение:
class FormValidatorSolution:
    """Решение: Валидатор форм с регулярными выражениями"""
    
    def __init__(self):
        # Паттерны для валидации
        self.patterns = {
            'username': re.compile(r'^[a-zA-Z0-9_]{3,20}$'),
            'email': re.compile(
                r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            ),
            'phone': {
                'us': re.compile(r'^(\+1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'),
                'international': re.compile(r'^\+[1-9]\d{1,14}$'),
                'generic': re.compile(r'^[\+]?[1-9][\d\s\-\(\)]{7,15}$')
            },
            'date': {
                'yyyy_mm_dd': re.compile(r'^(\d{4})-(\d{1,2})-(\d{1,2})$'),
                'mm_dd_yyyy': re.compile(r'^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$'),
                'dd_mm_yyyy': re.compile(r'^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$'),
                'text_date': re.compile(
                    r'^(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})$',
                    re.IGNORECASE
                )
            },
            'url': re.compile(
                r'^(https?|ftp)://[^\s/$.?#].[^\s]*$',
                re.IGNORECASE
            )
        }
        
        # Паттерны для анализа пароля
        self.password_patterns = {
            'length_8': re.compile(r'.{8,}'),
            'length_12': re.compile(r'.{12,}'),
            'uppercase': re.compile(r'[A-Z]'),
            'lowercase': re.compile(r'[a-z]'),
            'digit': re.compile(r'\d'),
            'special': re.compile(r'[!@#$%^&*(),.?":{}|<>]'),
            'no_spaces': re.compile(r'^\S+$'),
            'no_sequences': re.compile(r'^(?!.*(123|abc|qwe|asd|zxc)).*$', re.IGNORECASE),
            'no_repeats': re.compile(r'^(?!.*(.)\1{2,}).*$')
        }
        
        # Списки для проверки
        self.disposable_domains = {
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email'
        }
        
        self.reserved_usernames = {
            'admin', 'root', 'user', 'test', 'guest', 'system',
            'moderator', 'administrator', 'support', 'help'
        }
        
        self.stats = {
            'total_validations': 0,
            'successful_validations': 0,
            'field_errors': {}
        }
    
    def validate_username(self, username: str) -> Dict[str, Any]:
        """Валидация имени пользователя"""
        result = {
            'valid': False,
            'value': username,
            'errors': [],
            'suggestions': []
        }
        
        if not username:
            result['errors'].append('Username is required')
            return result
        
        # Базовая проверка паттерна
        if not self.patterns['username'].match(username):
            if len(username) < 3:
                result['errors'].append('Username must be at least 3 characters')
                result['suggestions'].append('Try adding more characters')
            elif len(username) > 20:
                result['errors'].append('Username must be no more than 20 characters')
                result['suggestions'].append('Try shortening the username')
            else:
                result['errors'].append('Username can only contain letters, numbers, and underscores')
                result['suggestions'].append('Remove special characters except underscore')
        
        # Проверка на зарезервированные имена
        if username.lower() in self.reserved_usernames:
            result['errors'].append('This username is reserved')
            result['suggestions'].append('Try adding numbers or modifying the name')
        
        # Проверка на слишком много цифр
        if re.search(r'\d{4,}', username):
            result['suggestions'].append('Consider using fewer consecutive numbers')
        
        # Проверка на слишком много подчеркиваний
        if username.count('_') > 2:
            result['suggestions'].append('Consider using fewer underscores')
        
        if not result['errors']:
            result['valid'] = True
            result['normalized'] = username.lower()
        
        return result
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """Валидация email"""
        result = {
            'valid': False,
            'value': email,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        if not email:
            result['errors'].append('Email is required')
            return result
        
        # Базовая проверка формата
        if not self.patterns['email'].match(email):
            result['errors'].append('Invalid email format')
            
            # Анализ возможных ошибок
            if '@' not in email:
                result['suggestions'].append('Email must contain @ symbol')
            elif email.count('@') > 1:
                result['suggestions'].append('Email can contain only one @ symbol')
            elif not re.search(r'\.[a-zA-Z]{2,}$', email):
                result['suggestions'].append('Email must end with valid domain extension')
            
            return result
        
        # Разделение на части
        local, domain = email.split('@')
        
        # Проверка локальной части
        if len(local) > 64:
            result['errors'].append('Email local part too long (max 64 characters)')
        
        if local.startswith('.') or local.endswith('.'):
            result['errors'].append('Email local part cannot start or end with dot')
        
        if '..' in local:
            result['errors'].append('Email local part cannot contain consecutive dots')
        
        # Проверка домена
        if len(domain) > 253:
            result['errors'].append('Email domain too long')
        
        # Проверка на disposable email
        if domain.lower() in self.disposable_domains:
            result['warnings'].append('Disposable email address detected')
            result['suggestions'].append('Consider using a permanent email address')
        
        # Проверка на типичные опечатки в доменах
        common_typos = {
            'gmail.con': 'gmail.com',
            'gmial.com': 'gmail.com',
            'yahoo.con': 'yahoo.com',
            'hotmail.con': 'hotmail.com'
        }
        
        if domain.lower() in common_typos:
            result['warnings'].append(f'Did you mean {common_typos[domain.lower()]}?')
        
        if not result['errors']:
            result['valid'] = True
            result['normalized'] = email.lower()
            result['parts'] = {'local': local, 'domain': domain}
        
        return result
    
    def validate_phone(self, phone: str) -> Dict[str, Any]:
        """Валидация телефона"""
        result = {
            'valid': False,
            'value': phone,
            'errors': [],
            'suggestions': [],
            'format': None
        }
        
        if not phone:
            result['errors'].append('Phone number is required')
            return result
        
        # Очистка номера
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Проверка различных форматов
        if self.patterns['phone']['us'].match(phone):
            result['valid'] = True
            result['format'] = 'US'
            result['normalized'] = self._format_us_phone(cleaned)
        elif self.patterns['phone']['international'].match(cleaned):
            result['valid'] = True
            result['format'] = 'International'
            result['normalized'] = cleaned
        elif self.patterns['phone']['generic'].match(phone):
            result['valid'] = True
            result['format'] = 'Generic'
            result['normalized'] = cleaned
        else:
            result['errors'].append('Invalid phone number format')
            
            # Анализ возможных проблем
            if len(cleaned) < 7:
                result['suggestions'].append('Phone number too short')
            elif len(cleaned) > 15:
                result['suggestions'].append('Phone number too long')
            else:
                result['suggestions'].append('Check phone number format')
        
        return result
    
    def _format_us_phone(self, phone: str) -> str:
        """Форматирование US телефона"""
        digits = re.sub(r'[^\d]', '', phone)
        
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits.startswith('1'):
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        
        return phone
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """Валидация пароля"""
        result = {
            'valid': False,
            'value': '***',  # Не возвращаем пароль
            'strength': 'Very Weak',
            'score': 0,
            'checks': {},
            'errors': [],
            'suggestions': []
        }
        
        if not password:
            result['errors'].append('Password is required')
            return result
        
        # Проверяем все критерии
        checks = {}
        score = 0
        
        for check_name, pattern in self.password_patterns.items():
            passed = bool(pattern.search(password))
            checks[check_name] = passed
            
            if passed:
                if check_name.startswith('length_'):
                    score += 2 if check_name == 'length_12' else 1
                else:
                    score += 1
        
        result['checks'] = checks
        result['score'] = score
        
        # Генерируем сообщения
        if not checks['length_8']:
            result['errors'].append('Password must be at least 8 characters')
        
        missing_requirements = []
        if not checks['uppercase']:
            missing_requirements.append('uppercase letter')
        if not checks['lowercase']:
            missing_requirements.append('lowercase letter')
        if not checks['digit']:
            missing_requirements.append('number')
        if not checks['special']:
            missing_requirements.append('special character')
        
        if missing_requirements:
            result['suggestions'].append(f"Add: {', '.join(missing_requirements)}")
        
        if not checks['no_spaces']:
            result['errors'].append('Password cannot contain spaces')
        
        if not checks['no_sequences']:
            result['suggestions'].append('Avoid common sequences like 123, abc')
        
        if not checks['no_repeats']:
            result['suggestions'].append('Avoid repeating characters')
        
        # Дополнительные проверки
        if len(set(password)) < len(password) * 0.6:
            result['suggestions'].append('Use more unique characters')
        
        # Проверка на словарные слова
        common_passwords = ['password', 'qwerty', 'admin', 'letmein', '123456']
        if password.lower() in common_passwords:
            result['errors'].append('Password is too common')
        
        # Определение силы пароля
        if score >= 8:
            result['strength'] = 'Very Strong'
        elif score >= 6:
            result['strength'] = 'Strong'
        elif score >= 4:
            result['strength'] = 'Good'
        elif score >= 2:
            result['strength'] = 'Weak'
        else:
            result['strength'] = 'Very Weak'
        
        result['valid'] = score >= 4 and not result['errors']
        
        return result
    
    def validate_date(self, date_str: str) -> Dict[str, Any]:
        """Валидация даты"""
        result = {
            'valid': False,
            'value': date_str,
            'errors': [],
            'format': None,
            'normalized': None
        }
        
        if not date_str:
            result['errors'].append('Date is required')
            return result
        
        # Проверяем различные форматы
        for format_name, pattern in self.patterns['date'].items():
            match = pattern.match(date_str.strip())
            if match:
                result['format'] = format_name
                
                try:
                    # Попытка нормализации в YYYY-MM-DD
                    if format_name == 'yyyy_mm_dd':
                        year, month, day = match.groups()
                    elif format_name == 'mm_dd_yyyy':
                        month, day, year = match.groups()
                    elif format_name == 'dd_mm_yyyy':
                        day, month, year = match.groups()
                    elif format_name == 'text_date':
                        day, month_name, year = match.groups()
                        month_map = {
                            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                        }
                        month = month_map.get(month_name[:3].lower(), '01')
                    
                    # Валидация значений
                    year_int = int(year)
                    month_int = int(month)
                    day_int = int(day)
                    
                    if not (1900 <= year_int <= 2100):
                        result['errors'].append('Year must be between 1900 and 2100')
                    elif not (1 <= month_int <= 12):
                        result['errors'].append('Month must be between 1 and 12')
                    elif not (1 <= day_int <= 31):
                        result['errors'].append('Day must be between 1 and 31')
                    else:
                        # Проверка на валидность даты
                        import datetime
                        try:
                            datetime.date(year_int, month_int, day_int)
                            result['valid'] = True
                            result['normalized'] = f"{year_int:04d}-{month_int:02d}-{day_int:02d}"
                        except ValueError:
                            result['errors'].append('Invalid date')
                
                except (ValueError, IndexError):
                    result['errors'].append('Invalid date format')
                
                break
        
        if not result['format']:
            result['errors'].append('Unrecognized date format')
            result['suggestions'] = [
                'Try formats like: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, or "15 Mar 2024"'
            ]
        
        return result
    
    def validate_url(self, url: str) -> Dict[str, Any]:
        """Валидация URL"""
        result = {
            'valid': False,
            'value': url,
            'errors': [],
            'warnings': [],
            'normalized': None
        }
        
        if not url:
            result['errors'].append('URL is required')
            return result
        
        # Добавляем протокол если отсутствует
        if not re.match(r'^[a-zA-Z][a-zA-Z\d+.-]*:', url):
            url = 'http://' + url
        
        if self.patterns['url'].match(url):
            result['valid'] = True
            result['normalized'] = url.lower()
            
            # Проверки безопасности
            if not url.startswith('https://'):
                result['warnings'].append('Consider using HTTPS for security')
            
            # Проверка длины
            if len(url) > 2048:
                result['warnings'].append('URL is very long')
            
        else:
            result['errors'].append('Invalid URL format')
        
        return result
    
    def validate_form(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """Валидация всей формы"""
        self.stats['total_validations'] += 1
        
        results = {
            'valid': True,
            'fields': {},
            'summary': {
                'total_fields': len(form_data),
                'valid_fields': 0,
                'invalid_fields': 0,
                'warnings': 0
            }
        }
        
        # Валидация каждого поля
        field_validators = {
            'username': self.validate_username,
            'email': self.validate_email,
            'phone': self.validate_phone,
            'password': self.validate_password,
            'date': self.validate_date,
            'url': self.validate_url
        }
        
        for field_name, field_value in form_data.items():
            if field_name in field_validators:
                field_result = field_validators[field_name](field_value)
                results['fields'][field_name] = field_result
                
                if field_result['valid']:
                    results['summary']['valid_fields'] += 1
                else:
                    results['summary']['invalid_fields'] += 1
                    results['valid'] = False
                    
                    # Обновляем статистику ошибок
                    if field_name not in self.stats['field_errors']:
                        self.stats['field_errors'][field_name] = 0
                    self.stats['field_errors'][field_name] += 1
                
                # Подсчет предупреждений
                if 'warnings' in field_result and field_result['warnings']:
                    results['summary']['warnings'] += len(field_result['warnings'])
        
        if results['valid']:
            self.stats['successful_validations'] += 1
        
        return results
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Получение статистики валидации"""
        success_rate = 0
        if self.stats['total_validations'] > 0:
            success_rate = (self.stats['successful_validations'] / 
                          self.stats['total_validations']) * 100
        
        return {
            'total_validations': self.stats['total_validations'],
            'successful_validations': self.stats['successful_validations'],
            'success_rate': success_rate,
            'field_error_frequency': dict(self.stats['field_errors'])
        }

# Тесты для FormValidator
class TestFormValidator:
    """Тесты валидатора форм"""
    
    @pytest.fixture
    def validator(self):
        """Fixture валидатора"""
        return FormValidatorSolution()
    
    def test_username_validation(self, validator):
        """Тест валидации имени пользователя"""
        # Валидные имена
        valid_usernames = ['user123', 'test_user', 'alice', 'bob_jones']
        for username in valid_usernames:
            result = validator.validate_username(username)
            assert result['valid'] is True, f"Username '{username}' should be valid"
        
        # Невалидные имена
        invalid_usernames = ['ab', 'user@test', 'admin', 'very_long_username_that_exceeds_limit']
        for username in invalid_usernames:
            result = validator.validate_username(username)
            assert result['valid'] is False, f"Username '{username}' should be invalid"
    
    def test_email_validation(self, validator):
        """Тест валидации email"""
        # Валидные email
        valid_emails = ['user@example.com', 'test.email@domain.org', 'alice+tag@test.co.uk']
        for email in valid_emails:
            result = validator.validate_email(email)
            assert result['valid'] is True, f"Email '{email}' should be valid"
        
        # Невалидные email
        invalid_emails = ['invalid-email', 'user@', '@domain.com', 'user..name@domain.com']
        for email in invalid_emails:
            result = validator.validate_email(email)
            assert result['valid'] is False, f"Email '{email}' should be invalid"
    
    def test_password_validation(self, validator):
        """Тест валидации пароля"""
        # Сильный пароль
        strong_password = 'MySecureP@ssw0rd123'
        result = validator.validate_password(strong_password)
        assert result['valid'] is True
        assert result['strength'] in ['Strong', 'Very Strong']
        
        # Слабый пароль
        weak_password = 'weak'
        result = validator.validate_password(weak_password)
        assert result['valid'] is False
        assert result['strength'] in ['Very Weak', 'Weak']
    
    def test_form_validation(self, validator):
        """Тест валидации формы"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'phone': '+1 (555) 123-4567'
        }
        
        result = validator.validate_form(form_data)
        
        assert 'valid' in result
        assert 'fields' in result
        assert 'summary' in result
        assert result['summary']['total_fields'] == len(form_data)

# =============================================================================
# Упражнение 2: Text Analytics Engine
# =============================================================================

"""
ЗАДАНИЕ 2: Text Analytics Engine

Создайте движок для анализа текста:

1. Класс TextAnalyzer с методами:
   - extract_entities() - извлечение именованных сущностей
   - analyze_sentiment() - анализ тональности (с regex паттернами)
   - extract_keywords() - извлечение ключевых слов
   - find_patterns() - поиск пользовательских паттернов
   - clean_text() - очистка и нормализация текста

2. Специализированные анализаторы:
   - Social Media Analyzer (хештеги, упоминания, эмодзи)
   - Code Analyzer (комментарии, функции, переменные)
   - Financial Text Analyzer (цены, валюты, финансовые термины)
   - Legal Document Analyzer (даты, номера дел, ссылки на законы)

3. Система отчетов:
   - Детальный анализ найденных паттернов
   - Статистика по типам сущностей
   - Экспорт результатов в различные форматы
"""

# Ваш код здесь:
class TextAnalyzer:
    """Анализатор текста с регулярными выражениями"""
    
    def __init__(self):
        # TODO: Реализуйте инициализацию
        pass
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Извлечение именованных сущностей"""
        # TODO: Реализуйте метод
        pass
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Анализ тональности"""
        # TODO: Реализуйте метод
        pass
    
    def extract_keywords(self, text: str) -> List[str]:
        """Извлечение ключевых слов"""
        # TODO: Реализуйте метод
        pass
    
    def find_patterns(self, text: str, patterns: Dict[str, str]) -> Dict[str, List[str]]:
        """Поиск пользовательских паттернов"""
        # TODO: Реализуйте метод
        pass

# Решение (краткая версия):
class TextAnalyzerSolution:
    """Решение: Анализатор текста"""
    
    def __init__(self):
        # Паттерны для извлечения сущностей
        self.entity_patterns = {
            'emails': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'urls': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
            'phone_numbers': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            'dates': re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
            'times': re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?\b', re.IGNORECASE),
            'money': re.compile(r'\$\d+(?:,\d{3})*(?:\.\d{2})?'),
            'percentages': re.compile(r'\b\d+(?:\.\d+)?%'),
            'hashtags': re.compile(r'#\w+'),
            'mentions': re.compile(r'@\w+')
        }
        
        # Паттерны для анализа тональности
        self.sentiment_patterns = {
            'positive': re.compile(
                r'\b(excellent|amazing|wonderful|great|fantastic|awesome|love|beautiful|perfect|outstanding)\b',
                re.IGNORECASE
            ),
            'negative': re.compile(
                r'\b(terrible|awful|horrible|hate|disgusting|worst|pathetic|disappointing|useless|annoying)\b',
                re.IGNORECASE
            ),
            'intensifiers': re.compile(
                r'\b(very|extremely|incredibly|absolutely|totally|completely|utterly|quite)\b',
                re.IGNORECASE
            ),
            'negations': re.compile(
                r'\b(not|no|never|none|nobody|nothing|nowhere|neither|nor)\b',
                re.IGNORECASE
            )
        }
        
        # Паттерны для очистки текста
        self.cleaning_patterns = {
            'html_tags': re.compile(r'<[^>]+>'),
            'urls': re.compile(r'http[s]?://\S+'),
            'extra_whitespace': re.compile(r'\s+'),
            'special_chars': re.compile(r'[^\w\s.,!?;:]'),
            'email_addresses': re.compile(r'\S+@\S+'),
            'numbers': re.compile(r'\b\d+\b')
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Извлечение именованных сущностей"""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = pattern.findall(text)
            entities[entity_type] = list(set(matches))  # Удаляем дубликаты
        
        return entities
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Анализ тональности"""
        positive_matches = self.sentiment_patterns['positive'].findall(text)
        negative_matches = self.sentiment_patterns['negative'].findall(text)
        intensifier_matches = self.sentiment_patterns['intensifiers'].findall(text)
        negation_matches = self.sentiment_patterns['negations'].findall(text)
        
        # Простой подсчет очков
        positive_score = len(positive_matches)
        negative_score = len(negative_matches)
        
        # Учитываем интенсификаторы
        if intensifier_matches:
            positive_score *= 1.5
            negative_score *= 1.5
        
        # Учитываем отрицания (простая логика)
        if negation_matches:
            positive_score, negative_score = negative_score, positive_score
        
        total_score = positive_score - negative_score
        
        if total_score > 0:
            sentiment = 'positive'
        elif total_score < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'score': total_score,
            'positive_words': positive_matches,
            'negative_words': negative_matches,
            'intensifiers': intensifier_matches,
            'negations': negation_matches
        }
    
    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """Извлечение ключевых слов"""
        # Очищаем текст
        cleaned = self.clean_text(text, remove_stopwords=True)
        
        # Извлекаем слова
        words = re.findall(r'\b[a-zA-Z]{' + str(min_length) + r',}\b', cleaned.lower())
        
        # Подсчитываем частоту
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Возвращаем топ слова
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:20]]
    
    def clean_text(self, text: str, remove_stopwords: bool = False) -> str:
        """Очистка и нормализация текста"""
        cleaned = text
        
        # Применяем паттерны очистки
        for pattern_name, pattern in self.cleaning_patterns.items():
            if pattern_name == 'html_tags':
                cleaned = pattern.sub('', cleaned)
            elif pattern_name == 'urls':
                cleaned = pattern.sub('[URL]', cleaned)
            elif pattern_name == 'email_addresses':
                cleaned = pattern.sub('[EMAIL]', cleaned)
            elif pattern_name == 'extra_whitespace':
                cleaned = pattern.sub(' ', cleaned)
        
        # Удаляем стоп-слова если нужно
        if remove_stopwords:
            stopwords = {
                'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
                'a', 'an', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
                'we', 'they', 'me', 'him', 'her', 'us', 'them'
            }
            
            words = cleaned.split()
            filtered_words = [word for word in words if word.lower() not in stopwords]
            cleaned = ' '.join(filtered_words)
        
        return cleaned.strip()
    
    def find_patterns(self, text: str, patterns: Dict[str, str]) -> Dict[str, List[str]]:
        """Поиск пользовательских паттернов"""
        results = {}
        
        for pattern_name, pattern_str in patterns.items():
            try:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = pattern.findall(text)
                results[pattern_name] = matches
            except re.error as e:
                results[pattern_name] = {'error': f'Invalid regex: {e}'}
        
        return results

class SocialMediaAnalyzer(TextAnalyzerSolution):
    """Анализатор социальных медиа"""
    
    def __init__(self):
        super().__init__()
        
        # Дополнительные паттерны для соцсетей
        self.social_patterns = {
            'hashtags': re.compile(r'#\w+'),
            'mentions': re.compile(r'@\w+'),
            'retweets': re.compile(r'\bRT\s+@\w+'),
            'emojis': re.compile(r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]'),
            'urls_shortened': re.compile(r'https?://t\.co/\w+|bit\.ly/\w+'),
            'cashtags': re.compile(r'\$[A-Z]{1,5}'),  # Для финансовых символов
        }
        
        self.entity_patterns.update(self.social_patterns)
    
    def analyze_engagement(self, text: str) -> Dict[str, Any]:
        """Анализ вовлеченности в социальных медиа"""
        hashtags = len(self.social_patterns['hashtags'].findall(text))
        mentions = len(self.social_patterns['mentions'].findall(text))
        
        # Простая метрика вовлеченности
        engagement_score = hashtags * 2 + mentions * 1.5
        
        return {
            'hashtag_count': hashtags,
            'mention_count': mentions,
            'engagement_score': engagement_score,
            'has_media_indicators': bool(
                re.search(r'(photo|video|image|pic|picture)', text, re.IGNORECASE)
            )
        }

# =============================================================================
# Упражнение 3: Log Security Analyzer
# =============================================================================

"""
ЗАДАНИЕ 3: Log Security Analyzer

Создайте анализатор безопасности логов:

1. Класс SecurityLogAnalyzer:
   - detect_attacks() - обнаружение атак (SQL injection, XSS, etc.)
   - analyze_access_patterns() - анализ паттернов доступа
   - detect_anomalies() - обнаружение аномалий
   - generate_security_report() - генерация отчета

2. Типы атак для обнаружения:
   - SQL Injection
   - Cross-Site Scripting (XSS)
   - Directory Traversal
   - Brute Force
   - DDoS patterns
   - Suspicious User Agents

3. Система алертов:
   - Настраиваемые пороги
   - Различные уровни серьезности
   - Группировка похожих событий
"""

# Ваш код здесь (краткое решение):
class SecurityLogAnalyzer:
    """Анализатор безопасности логов"""
    
    def __init__(self):
        self.attack_patterns = {
            'sql_injection': re.compile(
                r'(union|select|insert|update|delete|drop|exec|execute|script|alter|create)[\s\(]',
                re.IGNORECASE
            ),
            'xss': re.compile(
                r'(<script|javascript:|on\w+\s*=|eval\(|expression\()',
                re.IGNORECASE
            ),
            'directory_traversal': re.compile(
                r'(\.\./|\.\.\\|%2e%2e%2f|%2e%2e%5c)',
                re.IGNORECASE
            ),
            'command_injection': re.compile(
                r'(;|\|&|`|\$\(|<\(|>\()',
                re.IGNORECASE
            )
        }
        
        self.suspicious_agents = re.compile(
            r'(sqlmap|nikto|nmap|masscan|zap|burp)',
            re.IGNORECASE
        )
    
    def detect_attacks(self, log_line: str) -> List[Dict[str, Any]]:
        """Обнаружение атак в строке лога"""
        detected_attacks = []
        
        for attack_type, pattern in self.attack_patterns.items():
            matches = pattern.findall(log_line)
            if matches:
                detected_attacks.append({
                    'type': attack_type,
                    'evidence': matches,
                    'severity': self._get_severity(attack_type),
                    'log_line': log_line[:200]  # Первые 200 символов
                })
        
        # Проверка подозрительных User-Agent
        if self.suspicious_agents.search(log_line):
            detected_attacks.append({
                'type': 'suspicious_user_agent',
                'evidence': self.suspicious_agents.findall(log_line),
                'severity': 'medium',
                'log_line': log_line[:200]
            })
        
        return detected_attacks
    
    def _get_severity(self, attack_type: str) -> str:
        """Определение серьезности атаки"""
        severity_map = {
            'sql_injection': 'high',
            'xss': 'high',
            'directory_traversal': 'medium',
            'command_injection': 'high',
            'suspicious_user_agent': 'medium'
        }
        return severity_map.get(attack_type, 'low')

# =============================================================================
# Запуск упражнений
# =============================================================================

def run_exercises():
    """Запуск всех упражнений"""
    print("=== Упражнения: Регулярные выражения ===\n")
    
    # 1. Form Validation System
    print("1. Form Validation System...")
    validator = FormValidatorSolution()
    
    # Тестирование различных полей
    test_data = {
        'username': 'test_user123',
        'email': 'user@example.com',
        'password': 'SecureP@ssw0rd123',
        'phone': '+1 (555) 123-4567',
        'date': '2024-03-15',
        'url': 'https://www.example.com'
    }
    
    result = validator.validate_form(test_data)
    print(f"   Форма валидна: {result['valid']}")
    print(f"   Валидных полей: {result['summary']['valid_fields']}/{result['summary']['total_fields']}")
    
    # 2. Text Analytics Engine
    print("\n2. Text Analytics Engine...")
    analyzer = TextAnalyzerSolution()
    
    sample_text = """
    Great product! I love it. Contact us at support@example.com 
    or visit https://example.com. Call +1-555-123-4567 for more info.
    Meeting on 03/15/2024 at 2:30 PM. Price: $299.99 (15% discount!)
    #amazing #product @company_official
    """
    
    entities = analyzer.extract_entities(sample_text)
    sentiment = analyzer.analyze_sentiment(sample_text)
    keywords = analyzer.extract_keywords(sample_text)
    
    print(f"   Найденные сущности: {len([item for sublist in entities.values() for item in sublist])}")
    print(f"   Тональность: {sentiment['sentiment']} (score: {sentiment['score']})")
    print(f"   Ключевые слова: {len(keywords)}")
    
    # 3. Social Media Analyzer
    print("\n3. Social Media Analyzer...")
    social_analyzer = SocialMediaAnalyzer()
    
    social_text = "Just tried the new #Python features! Amazing work by @python_org team. RT @developer: Python 3.12 is fantastic! 🐍✨"
    
    social_entities = social_analyzer.extract_entities(social_text)
    engagement = social_analyzer.analyze_engagement(social_text)
    
    print(f"   Хештеги: {len(social_entities.get('hashtags', []))}")
    print(f"   Упоминания: {len(social_entities.get('mentions', []))}")
    print(f"   Engagement score: {engagement['engagement_score']}")
    
    # 4. Security Log Analyzer
    print("\n4. Security Log Analyzer...")
    security_analyzer = SecurityLogAnalyzer()
    
    suspicious_logs = [
        "GET /admin' OR 1=1-- HTTP/1.1",
        "POST /search?q=<script>alert('xss')</script>",
        "GET /../../../etc/passwd HTTP/1.1",
        "GET / HTTP/1.1\" \"Mozilla/5.0 sqlmap/1.0\""
    ]
    
    total_attacks = 0
    for log_line in suspicious_logs:
        attacks = security_analyzer.detect_attacks(log_line)
        total_attacks += len(attacks)
        if attacks:
            print(f"   Атака обнаружена: {attacks[0]['type']} (severity: {attacks[0]['severity']})")
    
    print(f"   Всего обнаружено атак: {total_attacks}")
    
    print("\n✅ Все упражнения выполнены успешно!")
    print("🔍 Теперь вы можете эффективно использовать регулярные выражения для решения сложных задач!")

if __name__ == "__main__":
    run_exercises() 