"""
Примеры: Регулярные выражения

Этот файл содержит практические примеры использования регулярных выражений
в Python для валидации данных, парсинга текста, поиска паттернов и
обработки строк.
"""

import re
import time
from typing import Dict, List, Optional, Any, Tuple, Pattern, Match
from dataclasses import dataclass
import json
from pathlib import Path
import email
from email.mime.text import MimeText
import html
import urllib.parse
from datetime import datetime
from collections import defaultdict

# =============================================================================
# Пример 1: Базовые паттерны и валидация
# =============================================================================

class BasicRegexValidator:
    """Базовый валидатор с регулярными выражениями"""
    
    def __init__(self):
        # Компилируем регулярные выражения для лучшей производительности
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        self.phone_pattern = re.compile(
            r'^(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
        )
        
        self.url_pattern = re.compile(
            r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
        )
        
        self.ipv4_pattern = re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
        
        self.ipv6_pattern = re.compile(
            r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$'
        )
        
        self.credit_card_pattern = re.compile(
            r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})$'
        )
        
        self.password_patterns = {
            'length': re.compile(r'.{8,}'),
            'uppercase': re.compile(r'[A-Z]'),
            'lowercase': re.compile(r'[a-z]'),
            'digit': re.compile(r'\d'),
            'special': re.compile(r'[!@#$%^&*(),.?":{}|<>]')
        }
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """Валидация email адреса"""
        if not email:
            return {'valid': False, 'error': 'Email is required'}
        
        if len(email) > 254:
            return {'valid': False, 'error': 'Email too long'}
        
        if self.email_pattern.match(email):
            # Дополнительные проверки
            local, domain = email.split('@')
            
            if len(local) > 64:
                return {'valid': False, 'error': 'Local part too long'}
            
            # Проверка на последовательные точки
            if '..' in email:
                return {'valid': False, 'error': 'Consecutive dots not allowed'}
            
            return {'valid': True, 'normalized': email.lower()}
        
        return {'valid': False, 'error': 'Invalid email format'}
    
    def validate_phone(self, phone: str) -> Dict[str, Any]:
        """Валидация номера телефона"""
        if not phone:
            return {'valid': False, 'error': 'Phone number is required'}
        
        # Удаляем все кроме цифр и + для проверки
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        if self.phone_pattern.match(phone):
            return {
                'valid': True, 
                'original': phone,
                'cleaned': cleaned,
                'formatted': self._format_phone(cleaned)
            }
        
        return {'valid': False, 'error': 'Invalid phone format'}
    
    def _format_phone(self, phone: str) -> str:
        """Форматирование номера телефона"""
        if phone.startswith('+'):
            return phone
        
        if len(phone) == 10:
            return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
        elif len(phone) == 11 and phone.startswith('1'):
            return f"+1 ({phone[1:4]}) {phone[4:7]}-{phone[7:]}"
        
        return phone
    
    def validate_url(self, url: str) -> Dict[str, Any]:
        """Валидация URL"""
        if not url:
            return {'valid': False, 'error': 'URL is required'}
        
        if self.url_pattern.match(url):
            # Проверка длины
            if len(url) > 2048:
                return {'valid': False, 'error': 'URL too long'}
            
            return {'valid': True, 'normalized': url.lower()}
        
        return {'valid': False, 'error': 'Invalid URL format'}
    
    def validate_ip_address(self, ip: str) -> Dict[str, Any]:
        """Валидация IP адреса"""
        if not ip:
            return {'valid': False, 'error': 'IP address is required'}
        
        if self.ipv4_pattern.match(ip):
            return {'valid': True, 'version': 'IPv4', 'address': ip}
        
        if self.ipv6_pattern.match(ip):
            return {'valid': True, 'version': 'IPv6', 'address': ip}
        
        return {'valid': False, 'error': 'Invalid IP address format'}
    
    def validate_credit_card(self, card_number: str) -> Dict[str, Any]:
        """Валидация номера кредитной карты"""
        if not card_number:
            return {'valid': False, 'error': 'Card number is required'}
        
        # Удаляем пробелы и дефисы
        cleaned = re.sub(r'[\s-]', '', card_number)
        
        if not cleaned.isdigit():
            return {'valid': False, 'error': 'Card number must contain only digits'}
        
        if self.credit_card_pattern.match(cleaned):
            card_type = self._detect_card_type(cleaned)
            
            # Проверка алгоритмом Луна
            if self._luhn_check(cleaned):
                return {
                    'valid': True,
                    'type': card_type,
                    'masked': self._mask_card_number(cleaned)
                }
            else:
                return {'valid': False, 'error': 'Invalid card number (Luhn check failed)'}
        
        return {'valid': False, 'error': 'Invalid card number format'}
    
    def _detect_card_type(self, number: str) -> str:
        """Определение типа кредитной карты"""
        if number.startswith('4'):
            return 'Visa'
        elif number.startswith(('51', '52', '53', '54', '55')):
            return 'MasterCard'
        elif number.startswith(('34', '37')):
            return 'American Express'
        elif number.startswith('6011') or number.startswith('65'):
            return 'Discover'
        else:
            return 'Unknown'
    
    def _luhn_check(self, number: str) -> bool:
        """Проверка алгоритмом Луна"""
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        
        return checksum % 10 == 0
    
    def _mask_card_number(self, number: str) -> str:
        """Маскировка номера карты"""
        if len(number) < 8:
            return '*' * len(number)
        
        return number[:4] + '*' * (len(number) - 8) + number[-4:]
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Проверка силы пароля"""
        if not password:
            return {'valid': False, 'error': 'Password is required'}
        
        checks = {}
        score = 0
        feedback = []
        
        for check_name, pattern in self.password_patterns.items():
            passed = bool(pattern.search(password))
            checks[check_name] = passed
            
            if passed:
                score += 1
            else:
                feedback.append(f"Add {check_name}")
        
        # Дополнительные проверки
        if len(password) >= 12:
            score += 1
            checks['long'] = True
        else:
            checks['long'] = False
            if len(password) < 8:
                feedback.append("Minimum 8 characters")
        
        # Проверка на повторяющиеся символы
        if re.search(r'(.)\1{2,}', password):
            score -= 1
            feedback.append("Avoid repeating characters")
        
        # Проверка на последовательности
        if re.search(r'(abc|bcd|cde|123|234|345|qwe|wer|ert)', password.lower()):
            score -= 1
            feedback.append("Avoid common sequences")
        
        strength_levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong']
        strength = strength_levels[min(score, len(strength_levels) - 1)]
        
        return {
            'valid': score >= 3,
            'score': score,
            'strength': strength,
            'checks': checks,
            'feedback': feedback
        }

def basic_validation_demo():
    """Демонстрация базовой валидации"""
    print("=== Basic Regex Validation Demo ===")
    
    validator = BasicRegexValidator()
    
    # Тестовые данные
    test_data = {
        'emails': [
            'user@example.com',
            'invalid-email',
            'user.name+tag@example.co.uk',
            'very-long-email-address-that-might-be-too-long@very-long-domain-name-example.com'
        ],
        'phones': [
            '+1 (555) 123-4567',
            '555-123-4567',
            '(555) 123-4567',
            '555.123.4567',
            'invalid-phone'
        ],
        'urls': [
            'https://www.example.com',
            'http://subdomain.example.org/path?param=value',
            'invalid-url',
            'ftp://example.com'
        ],
        'passwords': [
            'weak',
            'StrongPass123!',
            'password123',
            'MyVerySecurePassword2023!'
        ]
    }
    
    # Валидация email
    print("\n--- Email Validation ---")
    for email in test_data['emails']:
        result = validator.validate_email(email)
        status = "✓" if result['valid'] else "✗"
        print(f"{status} {email}: {result}")
    
    # Валидация телефонов
    print("\n--- Phone Validation ---")
    for phone in test_data['phones']:
        result = validator.validate_phone(phone)
        status = "✓" if result['valid'] else "✗"
        print(f"{status} {phone}: {result}")
    
    # Валидация паролей
    print("\n--- Password Strength ---")
    for password in test_data['passwords']:
        result = validator.validate_password_strength(password)
        print(f"'{password}': {result['strength']} (Score: {result['score']})")
        if result['feedback']:
            print(f"  Feedback: {', '.join(result['feedback'])}")
    
    return validator

# =============================================================================
# Пример 2: Парсинг и извлечение данных
# =============================================================================

class TextDataExtractor:
    """Извлечение данных из текста с помощью регулярных выражений"""
    
    def __init__(self):
        # Паттерны для извлечения различных типов данных
        self.date_patterns = [
            re.compile(r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})\b'),  # MM/DD/YYYY
            re.compile(r'\b(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})\b'),  # YYYY/MM/DD
            re.compile(r'\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})\b', re.IGNORECASE),
            re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})\b', re.IGNORECASE)
        ]
        
        self.time_pattern = re.compile(r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)?\b', re.IGNORECASE)
        
        self.money_pattern = re.compile(r'[\$£€¥]\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)')
        
        self.social_security_pattern = re.compile(r'\b(\d{3})-(\d{2})-(\d{4})\b')
        
        self.hashtag_pattern = re.compile(r'#\w+')
        self.mention_pattern = re.compile(r'@\w+')
        
        self.html_tag_pattern = re.compile(r'<[^>]+>')
        self.html_entity_pattern = re.compile(r'&[a-zA-Z]+;|&#\d+;')
        
        self.code_block_pattern = re.compile(r'```(\w+)?\n(.*?)\n```', re.DOTALL)
        self.inline_code_pattern = re.compile(r'`([^`]+)`')
        
        self.link_pattern = re.compile(r'https?://[^\s<>"]+')
        
        # Паттерны для логов
        self.apache_log_pattern = re.compile(
            r'(\S+) \S+ \S+ \[(.*?)\] "(\w+) (.*?) HTTP/\d\.\d" (\d+) (\d+|-)'
        )
        
        self.json_pattern = re.compile(r'\{[^{}]*\}')
    
    def extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """Извлечение дат из текста"""
        dates = []
        
        for i, pattern in enumerate(self.date_patterns):
            for match in pattern.finditer(text):
                date_info = {
                    'original': match.group(0),
                    'start': match.start(),
                    'end': match.end(),
                    'pattern_type': i,
                    'groups': match.groups()
                }
                
                # Попытка нормализации даты
                try:
                    if i == 0:  # MM/DD/YYYY
                        month, day, year = match.groups()
                        normalized = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    elif i == 1:  # YYYY/MM/DD
                        year, month, day = match.groups()
                        normalized = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    elif i in (2, 3):  # Month name formats
                        groups = match.groups()
                        month_map = {
                            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                        }
                        
                        if i == 2:  # DD Month YYYY
                            day, month_name, year = groups
                            month = month_map.get(month_name[:3].lower(), '01')
                            normalized = f"{year}-{month}-{day.zfill(2)}"
                        else:  # Month DD, YYYY
                            month_name, day, year = groups
                            month = month_map.get(month_name[:3].lower(), '01')
                            normalized = f"{year}-{month}-{day.zfill(2)}"
                    
                    date_info['normalized'] = normalized
                    
                except:
                    date_info['normalized'] = None
                
                dates.append(date_info)
        
        return dates
    
    def extract_times(self, text: str) -> List[Dict[str, Any]]:
        """Извлечение времени из текста"""
        times = []
        
        for match in self.time_pattern.finditer(text):
            hour, minute, second, ampm = match.groups()
            
            time_info = {
                'original': match.group(0),
                'start': match.start(),
                'end': match.end(),
                'hour': hour,
                'minute': minute,
                'second': second or '00',
                'ampm': ampm
            }
            
            # Нормализация в 24-часовой формат
            try:
                hour_24 = int(hour)
                if ampm:
                    if ampm.upper() == 'PM' and hour_24 != 12:
                        hour_24 += 12
                    elif ampm.upper() == 'AM' and hour_24 == 12:
                        hour_24 = 0
                
                time_info['normalized'] = f"{hour_24:02d}:{minute}:{time_info['second']}"
            except:
                time_info['normalized'] = None
            
            times.append(time_info)
        
        return times
    
    def extract_money_amounts(self, text: str) -> List[Dict[str, Any]]:
        """Извлечение денежных сумм"""
        amounts = []
        
        for match in self.money_pattern.finditer(text):
            amount_str = match.group(1)
            
            amount_info = {
                'original': match.group(0),
                'start': match.start(),
                'end': match.end(),
                'amount_str': amount_str,
                'currency_symbol': match.group(0)[0]
            }
            
            # Преобразование в число
            try:
                amount_info['amount'] = float(amount_str.replace(',', ''))
            except:
                amount_info['amount'] = None
            
            amounts.append(amount_info)
        
        return amounts
    
    def extract_social_media_elements(self, text: str) -> Dict[str, List[str]]:
        """Извлечение элементов социальных сетей"""
        return {
            'hashtags': [match.group(0) for match in self.hashtag_pattern.finditer(text)],
            'mentions': [match.group(0) for match in self.mention_pattern.finditer(text)],
            'links': [match.group(0) for match in self.link_pattern.finditer(text)]
        }
    
    def clean_html(self, html_text: str) -> str:
        """Очистка HTML тегов и entities"""
        # Удаляем HTML теги
        no_tags = self.html_tag_pattern.sub('', html_text)
        
        # Декодируем HTML entities
        no_entities = html.unescape(no_tags)
        
        return no_entities.strip()
    
    def extract_code_blocks(self, markdown_text: str) -> List[Dict[str, str]]:
        """Извлечение блоков кода из Markdown"""
        code_blocks = []
        
        # Блоки кода
        for match in self.code_block_pattern.finditer(markdown_text):
            language = match.group(1) or 'text'
            code = match.group(2)
            
            code_blocks.append({
                'type': 'block',
                'language': language,
                'code': code,
                'start': match.start(),
                'end': match.end()
            })
        
        # Инлайн код
        for match in self.inline_code_pattern.finditer(markdown_text):
            code_blocks.append({
                'type': 'inline',
                'code': match.group(1),
                'start': match.start(),
                'end': match.end()
            })
        
        return code_blocks
    
    def parse_apache_log(self, log_line: str) -> Optional[Dict[str, str]]:
        """Парсинг строки Apache лога"""
        match = self.apache_log_pattern.match(log_line)
        
        if match:
            ip, timestamp, method, path, status, size = match.groups()
            
            return {
                'ip_address': ip,
                'timestamp': timestamp,
                'method': method,
                'path': path,
                'status_code': status,
                'response_size': size
            }
        
        return None
    
    def extract_json_objects(self, text: str) -> List[Dict[str, Any]]:
        """Извлечение JSON объектов из текста"""
        json_objects = []
        
        for match in self.json_pattern.finditer(text):
            try:
                json_str = match.group(0)
                parsed = json.loads(json_str)
                
                json_objects.append({
                    'original': json_str,
                    'parsed': parsed,
                    'start': match.start(),
                    'end': match.end()
                })
            except json.JSONDecodeError:
                continue
        
        return json_objects

def text_extraction_demo():
    """Демонстрация извлечения данных из текста"""
    print("\n=== Text Data Extraction Demo ===")
    
    extractor = TextDataExtractor()
    
    # Тестовый текст с различными данными
    sample_text = """
    Meeting scheduled for March 15, 2024 at 2:30 PM.
    Please transfer $1,250.50 to account by 12/31/2023.
    Contact John Doe at +1 (555) 123-4567 or john@example.com.
    
    Social media post: "Great day! #Python #Programming @developer_community
    Check out https://example.com/tutorial for more info."
    
    Log entry: 192.168.1.100 - - [15/Mar/2024:14:30:25 +0000] "GET /api/users HTTP/1.1" 200 1234
    
    Code example:
    ```python
    def hello_world():
        print("Hello, World!")
    ```
    
    Also found some inline `code` and HTML content:
    <p>This is <strong>bold</strong> text with &amp; entity.</p>
    """
    
    print("Исходный текст:")
    print(sample_text)
    
    # Извлечение дат
    print("\n--- Extracted Dates ---")
    dates = extractor.extract_dates(sample_text)
    for date in dates:
        print(f"Found: '{date['original']}' -> {date['normalized']}")
    
    # Извлечение времени
    print("\n--- Extracted Times ---")
    times = extractor.extract_times(sample_text)
    for time_info in times:
        print(f"Found: '{time_info['original']}' -> {time_info['normalized']}")
    
    # Извлечение денежных сумм
    print("\n--- Extracted Money ---")
    amounts = extractor.extract_money_amounts(sample_text)
    for amount in amounts:
        print(f"Found: '{amount['original']}' -> {amount['amount']}")
    
    # Социальные медиа элементы
    print("\n--- Social Media Elements ---")
    social = extractor.extract_social_media_elements(sample_text)
    for element_type, elements in social.items():
        if elements:
            print(f"{element_type.title()}: {elements}")
    
    # Блоки кода
    print("\n--- Code Blocks ---")
    code_blocks = extractor.extract_code_blocks(sample_text)
    for block in code_blocks:
        print(f"{block['type'].title()} code ({block.get('language', 'text')}): {block['code'][:50]}...")
    
    # Очистка HTML
    html_sample = "<p>This is <strong>bold</strong> text with &amp; entity.</p>"
    cleaned = extractor.clean_html(html_sample)
    print(f"\n--- HTML Cleaning ---")
    print(f"Original: {html_sample}")
    print(f"Cleaned: {cleaned}")
    
    return extractor

# =============================================================================
# Пример 3: Продвинутые паттерны и оптимизация
# =============================================================================

class AdvancedRegexProcessor:
    """Продвинутые техники работы с регулярными выражениями"""
    
    def __init__(self):
        # Предкомпилированные паттерны для лучшей производительности
        self.compiled_patterns = {}
        
        # Паттерны с именованными группами
        self.email_detailed = re.compile(
            r'(?P<local>[a-zA-Z0-9._%+-]+)@(?P<domain>[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        )
        
        self.url_detailed = re.compile(
            r'(?P<protocol>https?://)(?P<subdomain>www\.)?(?P<domain>[-a-zA-Z0-9@:%._\+~#=]{1,256})'
            r'\.(?P<tld>[a-zA-Z0-9()]{1,6})(?P<path>/[-a-zA-Z0-9()@:%_\+.~#?&//=]*)?'
        )
        
        # Lookahead и lookbehind паттерны
        self.password_complex = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        )
        
        # Паттерны для обработки CSV
        self.csv_field = re.compile(r',(?=(?:[^"]*"[^"]*")*[^"]*$)')
        
        # Паттерны для SQL injection detection
        self.sql_injection_patterns = [
            re.compile(r"(\bUNION\b|\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b)", re.IGNORECASE),
            re.compile(r"('|\";|\s;|\s--)", re.IGNORECASE),
            re.compile(r"(\bOR\s+\d+\s*=\s*\d+|\bAND\s+\d+\s*=\s*\d+)", re.IGNORECASE)
        ]
    
    def compile_and_cache_pattern(self, pattern: str, flags: int = 0) -> Pattern:
        """Компиляция и кеширование паттерна"""
        cache_key = (pattern, flags)
        
        if cache_key not in self.compiled_patterns:
            self.compiled_patterns[cache_key] = re.compile(pattern, flags)
        
        return self.compiled_patterns[cache_key]
    
    def extract_email_parts(self, email: str) -> Optional[Dict[str, str]]:
        """Извлечение частей email с именованными группами"""
        match = self.email_detailed.match(email)
        
        if match:
            return match.groupdict()
        
        return None
    
    def extract_url_parts(self, url: str) -> Optional[Dict[str, str]]:
        """Извлечение частей URL с именованными группами"""
        match = self.url_detailed.match(url)
        
        if match:
            parts = match.groupdict()
            # Убираем None значения
            return {k: v for k, v in parts.items() if v is not None}
        
        return None
    
    def validate_complex_password(self, password: str) -> Dict[str, Any]:
        """Валидация сложного пароля с lookahead"""
        result = {
            'valid': False,
            'checks': {},
            'score': 0
        }
        
        # Используем lookahead для проверки всех требований
        checks = {
            'has_lowercase': re.search(r'(?=.*[a-z])', password) is not None,
            'has_uppercase': re.search(r'(?=.*[A-Z])', password) is not None,
            'has_digit': re.search(r'(?=.*\d)', password) is not None,
            'has_special': re.search(r'(?=.*[@$!%*?&])', password) is not None,
            'min_length': len(password) >= 8,
            'no_common_patterns': not re.search(r'(123|abc|password|qwerty)', password.lower())
        }
        
        result['checks'] = checks
        result['score'] = sum(checks.values())
        result['valid'] = self.password_complex.match(password) is not None and checks['no_common_patterns']
        
        return result
    
    def parse_csv_line(self, csv_line: str) -> List[str]:
        """Парсинг CSV строки с учетом кавычек"""
        # Удаляем перенос строки
        csv_line = csv_line.strip()
        
        # Разделяем по запятым, игнорируя запятые в кавычках
        fields = self.csv_field.split(csv_line)
        
        # Очищаем поля от кавычек
        cleaned_fields = []
        for field in fields:
            field = field.strip()
            if field.startswith('"') and field.endswith('"'):
                field = field[1:-1].replace('""', '"')  # Удаляем кавычки и обрабатываем экранированные
            cleaned_fields.append(field)
        
        return cleaned_fields
    
    def detect_sql_injection(self, input_string: str) -> Dict[str, Any]:
        """Обнаружение попыток SQL injection"""
        threats = []
        risk_level = 0
        
        for i, pattern in enumerate(self.sql_injection_patterns):
            matches = pattern.findall(input_string)
            if matches:
                threat_info = {
                    'pattern_id': i,
                    'matches': matches,
                    'description': self._get_sql_threat_description(i)
                }
                threats.append(threat_info)
                risk_level += len(matches)
        
        return {
            'is_suspicious': len(threats) > 0,
            'risk_level': min(risk_level, 10),  # Ограничиваем до 10
            'threats': threats,
            'recommendation': 'Use parameterized queries' if threats else 'Input appears safe'
        }
    
    def _get_sql_threat_description(self, pattern_id: int) -> str:
        """Описание типа SQL угрозы"""
        descriptions = [
            "SQL keywords detected",
            "Dangerous characters found", 
            "Boolean injection attempt"
        ]
        return descriptions[pattern_id] if pattern_id < len(descriptions) else "Unknown threat"
    
    def benchmark_regex_performance(self, pattern: str, text: str, iterations: int = 10000) -> Dict[str, float]:
        """Бенчмарк производительности регулярных выражений"""
        # Тест без компиляции (каждый раз компилируется заново)
        start_time = time.time()
        for _ in range(iterations):
            re.search(pattern, text)
        no_compile_time = time.time() - start_time
        
        # Тест с предварительной компиляцией
        compiled_pattern = re.compile(pattern)
        start_time = time.time()
        for _ in range(iterations):
            compiled_pattern.search(text)
        compiled_time = time.time() - start_time
        
        return {
            'no_compilation_time': no_compile_time,
            'compiled_time': compiled_time,
            'speedup_factor': no_compile_time / compiled_time if compiled_time > 0 else 0,
            'iterations': iterations
        }
    
    def optimize_alternation(self, patterns: List[str]) -> str:
        """Оптимизация альтернации паттернов"""
        if not patterns:
            return ""
        
        # Сортируем по длине (более длинные первыми)
        sorted_patterns = sorted(patterns, key=len, reverse=True)
        
        # Ищем общие префиксы для оптимизации
        optimized = self._find_common_prefixes(sorted_patterns)
        
        return '|'.join(optimized)
    
    def _find_common_prefixes(self, patterns: List[str]) -> List[str]:
        """Поиск общих префиксов для оптимизации"""
        if len(patterns) <= 1:
            return patterns
        
        # Упрощенная оптимизация - просто возвращаем отсортированные паттерны
        # В реальном применении здесь была бы более сложная логика
        return patterns
    
    def create_fuzzy_pattern(self, word: str, max_errors: int = 1) -> str:
        """Создание нечеткого паттерна для поиска с ошибками"""
        # Упрощенная версия - позволяет 1 замену символа
        if max_errors == 0:
            return re.escape(word)
        
        # Создаем паттерн с возможными заменами
        fuzzy_parts = []
        for i in range(len(word)):
            # Оригинальное слово
            fuzzy_parts.append(re.escape(word))
            
            # Версии с заменой одного символа
            if max_errors >= 1:
                for char in 'abcdefghijklmnopqrstuvwxyz':
                    if char != word[i].lower():
                        modified = word[:i] + char + word[i+1:]
                        fuzzy_parts.append(re.escape(modified))
        
        return '|'.join(set(fuzzy_parts))  # Убираем дубликаты

def advanced_regex_demo():
    """Демонстрация продвинутых техник regex"""
    print("\n=== Advanced Regex Demo ===")
    
    processor = AdvancedRegexProcessor()
    
    # Именованные группы
    print("--- Named Groups ---")
    email_parts = processor.extract_email_parts("user.name@example.com")
    print(f"Email parts: {email_parts}")
    
    url_parts = processor.extract_url_parts("https://www.example.com/path?param=value")
    print(f"URL parts: {url_parts}")
    
    # Сложная валидация пароля
    print("\n--- Complex Password Validation ---")
    test_passwords = ["weak", "StrongPass123!", "NoSpecial123", "short!1A"]
    
    for pwd in test_passwords:
        result = processor.validate_complex_password(pwd)
        print(f"'{pwd}': Valid={result['valid']}, Score={result['score']}")
    
    # SQL Injection detection
    print("\n--- SQL Injection Detection ---")
    test_inputs = [
        "normal user input",
        "'; DROP TABLE users; --",
        "1 OR 1=1",
        "user@example.com"
    ]
    
    for input_str in test_inputs:
        result = processor.detect_sql_injection(input_str)
        print(f"'{input_str}': Suspicious={result['is_suspicious']}, Risk={result['risk_level']}")
    
    # Performance benchmark
    print("\n--- Performance Benchmark ---")
    pattern = r'\b\w+@\w+\.\w+\b'
    text = "Contact us at support@example.com or sales@company.org for assistance."
    
    benchmark = processor.benchmark_regex_performance(pattern, text, 1000)
    print(f"Speedup with compilation: {benchmark['speedup_factor']:.2f}x")
    print(f"Compiled time: {benchmark['compiled_time']:.4f}s")
    print(f"Non-compiled time: {benchmark['no_compilation_time']:.4f}s")
    
    return processor

# =============================================================================
# Пример 4: Обработка больших файлов и логов
# =============================================================================

class LogProcessor:
    """Обработчик логов с использованием регулярных выражений"""
    
    def __init__(self):
        # Паттерны для различных форматов логов
        self.log_patterns = {
            'apache': re.compile(
                r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<path>.*?) HTTP/\d\.\d" '
                r'(?P<status>\d+) (?P<size>\d+|-) "(?P<referer>.*?)" "(?P<user_agent>.*?)"'
            ),
            'nginx': re.compile(
                r'(?P<ip>\S+) - \S+ \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<path>.*?) HTTP/\d\.\d" '
                r'(?P<status>\d+) (?P<size>\d+) "(?P<referer>.*?)" "(?P<user_agent>.*?)"'
            ),
            'python': re.compile(
                r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - '
                r'(?P<logger>\S+) - (?P<level>\w+) - (?P<message>.*)'
            ),
            'syslog': re.compile(
                r'(?P<timestamp>\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (?P<hostname>\S+) '
                r'(?P<process>\S+): (?P<message>.*)'
            )
        }
        
        # Паттерны для анализа событий безопасности
        self.security_patterns = {
            'failed_login': re.compile(r'failed login|authentication failed|invalid credentials', re.IGNORECASE),
            'suspicious_ip': re.compile(r'(?P<ip>(?:\d{1,3}\.){3}\d{1,3})'),
            'sql_injection': re.compile(r'(union|select|insert|update|delete|drop)', re.IGNORECASE),
            'xss_attempt': re.compile(r'(<script|javascript:|on\w+\s*=)', re.IGNORECASE),
            'directory_traversal': re.compile(r'(\.\./|\.\.\\|\.\.\%2f)', re.IGNORECASE),
            'brute_force': re.compile(r'(password|login|auth).*?(attempt|try|fail)', re.IGNORECASE)
        }
        
        self.stats = {
            'total_lines': 0,
            'parsed_lines': 0,
            'security_events': defaultdict(int),
            'status_codes': defaultdict(int),
            'ip_addresses': defaultdict(int),
            'user_agents': defaultdict(int)
        }
    
    def detect_log_format(self, log_line: str) -> Optional[str]:
        """Автоматическое определение формата лога"""
        for format_name, pattern in self.log_patterns.items():
            if pattern.match(log_line):
                return format_name
        return None
    
    def parse_log_line(self, log_line: str, format_type: str = None) -> Optional[Dict[str, str]]:
        """Парсинг строки лога"""
        if format_type is None:
            format_type = self.detect_log_format(log_line)
        
        if format_type and format_type in self.log_patterns:
            match = self.log_patterns[format_type].match(log_line)
            if match:
                return match.groupdict()
        
        return None
    
    def analyze_security_events(self, log_line: str) -> List[str]:
        """Анализ событий безопасности в строке лога"""
        detected_events = []
        
        for event_type, pattern in self.security_patterns.items():
            if pattern.search(log_line):
                detected_events.append(event_type)
                self.stats['security_events'][event_type] += 1
        
        return detected_events
    
    def process_log_file(self, file_path: str, max_lines: int = None) -> Dict[str, Any]:
        """Обработка файла логов"""
        results = {
            'format_detected': None,
            'total_lines': 0,
            'parsed_entries': [],
            'security_events': [],
            'parsing_errors': [],
            'statistics': {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                format_detected = None
                
                for line_num, line in enumerate(file, 1):
                    if max_lines and line_num > max_lines:
                        break
                    
                    line = line.strip()
                    if not line:
                        continue
                    
                    results['total_lines'] += 1
                    self.stats['total_lines'] += 1
                    
                    # Определяем формат при первой строке
                    if format_detected is None:
                        format_detected = self.detect_log_format(line)
                        results['format_detected'] = format_detected
                    
                    # Парсим строку
                    parsed = self.parse_log_line(line, format_detected)
                    if parsed:
                        results['parsed_entries'].append(parsed)
                        self.stats['parsed_lines'] += 1
                        
                        # Собираем статистику
                        if 'status' in parsed:
                            self.stats['status_codes'][parsed['status']] += 1
                        
                        if 'ip' in parsed:
                            self.stats['ip_addresses'][parsed['ip']] += 1
                        
                        if 'user_agent' in parsed:
                            agent = parsed['user_agent'][:50]  # Ограничиваем длину
                            self.stats['user_agents'][agent] += 1
                    
                    else:
                        results['parsing_errors'].append({
                            'line_number': line_num,
                            'content': line[:100]  # Первые 100 символов
                        })
                    
                    # Анализируем события безопасности
                    security_events = self.analyze_security_events(line)
                    if security_events:
                        results['security_events'].append({
                            'line_number': line_num,
                            'events': security_events,
                            'content': line[:200]
                        })
        
        except Exception as e:
            results['error'] = str(e)
        
        # Добавляем статистику
        results['statistics'] = self.get_statistics()
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики обработки"""
        return {
            'total_lines_processed': self.stats['total_lines'],
            'successfully_parsed': self.stats['parsed_lines'],
            'parsing_success_rate': (
                self.stats['parsed_lines'] / max(self.stats['total_lines'], 1) * 100
            ),
            'top_status_codes': dict(sorted(
                self.stats['status_codes'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]),
            'top_ips': dict(sorted(
                self.stats['ip_addresses'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]),
            'security_events_summary': dict(self.stats['security_events']),
            'unique_ips': len(self.stats['ip_addresses']),
            'unique_user_agents': len(self.stats['user_agents'])
        }
    
    def generate_sample_log_file(self, file_path: str, num_lines: int = 1000):
        """Генерация примера файла лога для тестирования"""
        import random
        from datetime import datetime, timedelta
        
        sample_ips = ['192.168.1.100', '10.0.0.50', '203.0.113.25', '198.51.100.75']
        sample_paths = ['/index.html', '/api/users', '/login', '/admin', '/upload.php']
        sample_methods = ['GET', 'POST', 'PUT', 'DELETE']
        sample_status_codes = ['200', '404', '500', '301', '403']
        sample_user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'curl/7.68.0',
            'Python-urllib/3.8'
        ]
        
        with open(file_path, 'w') as f:
            base_time = datetime.now() - timedelta(days=1)
            
            for i in range(num_lines):
                # Генерируем случайную запись лога
                ip = random.choice(sample_ips)
                timestamp = (base_time + timedelta(seconds=i*10)).strftime('%d/%b/%Y:%H:%M:%S +0000')
                method = random.choice(sample_methods)
                path = random.choice(sample_paths)
                status = random.choice(sample_status_codes)
                size = random.randint(100, 10000)
                user_agent = random.choice(sample_user_agents)
                
                # Иногда добавляем подозрительные события
                if random.random() < 0.05:  # 5% подозрительных событий
                    if random.random() < 0.5:
                        path = "/admin' OR 1=1 --"  # SQL injection
                    else:
                        path = "/<script>alert('xss')</script>"  # XSS
                
                log_line = f'{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status} {size} "-" "{user_agent}"\n'
                f.write(log_line)

def log_processing_demo():
    """Демонстрация обработки логов"""
    print("\n=== Log Processing Demo ===")
    
    processor = LogProcessor()
    
    # Создаем временный файл лога
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
    temp_file.close()
    
    try:
        # Генерируем тестовый лог
        print("Генерируем тестовый лог файл...")
        processor.generate_sample_log_file(temp_file.name, 100)
        
        # Обрабатываем лог
        print("Обрабатываем лог файл...")
        results = processor.process_log_file(temp_file.name, max_lines=50)
        
        print(f"Формат лога: {results['format_detected']}")
        print(f"Обработано строк: {results['total_lines']}")
        print(f"Успешно спарсено: {len(results['parsed_entries'])}")
        print(f"Ошибки парсинга: {len(results['parsing_errors'])}")
        print(f"События безопасности: {len(results['security_events'])}")
        
        # Статистика
        stats = results['statistics']
        print(f"\n--- Статистика ---")
        print(f"Успешность парсинга: {stats['parsing_success_rate']:.1f}%")
        print(f"Уникальных IP: {stats['unique_ips']}")
        
        if stats['top_status_codes']:
            print("Топ статус коды:")
            for code, count in list(stats['top_status_codes'].items())[:5]:
                print(f"  {code}: {count}")
        
        if stats['security_events_summary']:
            print("События безопасности:")
            for event, count in stats['security_events_summary'].items():
                print(f"  {event}: {count}")
        
        # Примеры подозрительных событий
        if results['security_events']:
            print(f"\nПримеры подозрительных событий:")
            for event in results['security_events'][:3]:
                print(f"  Строка {event['line_number']}: {event['events']}")
                print(f"    {event['content'][:100]}...")
    
    finally:
        # Удаляем временный файл
        try:
            Path(temp_file.name).unlink()
        except:
            pass
    
    return processor

# =============================================================================
# Главная функция для демонстрации всех примеров
# =============================================================================

def main():
    """Запуск всех примеров регулярных выражений"""
    print("=== Регулярные выражения в Python ===\n")
    
    # 1. Базовая валидация
    validator = basic_validation_demo()
    
    # 2. Извлечение данных из текста
    extractor = text_extraction_demo()
    
    # 3. Продвинутые техники
    processor = advanced_regex_demo()
    
    # 4. Обработка логов
    log_processor = log_processing_demo()
    
    print("\n=== Сводка ===")
    print("✅ Валидация данных (email, телефон, URL, IP, кредитные карты)")
    print("✅ Извлечение структурированных данных из текста")
    print("✅ Парсинг дат, времени, денежных сумм")
    print("✅ Обработка HTML, Markdown, социальных медиа")
    print("✅ Продвинутые техники (именованные группы, lookahead/lookbehind)")
    print("✅ Оптимизация производительности regex")
    print("✅ Обнаружение SQL injection и XSS атак")
    print("✅ Обработка больших логов и файлов")
    print("✅ Автоматическое определение форматов")
    print("✅ Анализ событий безопасности")
    
    print("\nВсе примеры демонстрируют мощь и гибкость регулярных выражений! 🔍📝")

if __name__ == "__main__":
    main() 