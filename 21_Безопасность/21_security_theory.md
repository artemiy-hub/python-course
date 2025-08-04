# Теория: Безопасность в Python

## 🎯 Цель раздела

Этот раздел охватывает все аспекты безопасности в Python-разработке: от безопасного хранения паролей до защиты от уязвимостей, криптографии и лучших практик безопасного программирования.

## 📋 Содержание

1. [Хеширование и пароли](#хеширование-и-пароли)
2. [Криптография](#криптография)
3. [Веб-безопасность](#веб-безопасность)
4. [Безопасность данных](#безопасность-данных)
5. [Аудит и мониторинг](#аудит-и-мониторинг)
6. [Безопасная разработка](#безопасная-разработка)
7. [Compliance и стандарты](#compliance-и-стандарты)

---

## 🔐 Хеширование и пароли

Безопасное хранение и обработка паролей - основа любой защищенной системы.

### Современные методы хеширования

```python
import hashlib
import secrets
import bcrypt
import argon2
from argon2 import PasswordHasher
from typing import Dict, Optional, Tuple, Union
import time
import base64
import hmac
from dataclasses import dataclass
from datetime import datetime, timedelta
import re

@dataclass
class PasswordPolicy:
    """Политика безопасности паролей"""
    min_length: int = 8
    max_length: int = 128
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digits: bool = True
    require_special: bool = True
    special_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    max_repeated_chars: int = 2
    min_unique_chars: int = 4
    block_common_passwords: bool = True
    block_personal_info: bool = True

class SecurePasswordManager:
    """Менеджер для безопасной работы с паролями"""
    
    def __init__(self, policy: Optional[PasswordPolicy] = None):
        self.policy = policy or PasswordPolicy()
        self.ph = PasswordHasher()
        
        # Загружаем список популярных паролей для блокировки
        self.common_passwords = self._load_common_passwords()
    
    def _load_common_passwords(self) -> set:
        """Загрузка списка популярных паролей"""
        # В реальном приложении это должен быть файл с популярными паролями
        return {
            'password', '123456', 'password123', 'admin', 'qwerty',
            'letmein', 'welcome', 'monkey', '1234567890', 'abc123',
            'Password1', 'password1', '12345678', 'qwerty123'
        }
    
    def validate_password(self, password: str, user_info: Optional[Dict[str, str]] = None) -> Dict[str, Union[bool, str, list]]:
        """
        Комплексная валидация пароля
        
        Args:
            password: Пароль для проверки
            user_info: Информация о пользователе (имя, email и т.д.)
            
        Returns:
            Результат валидации с детальной информацией
        """
        errors = []
        warnings = []
        score = 0
        
        # Проверка длины
        if len(password) < self.policy.min_length:
            errors.append(f"Пароль должен содержать минимум {self.policy.min_length} символов")
        elif len(password) > self.policy.max_length:
            errors.append(f"Пароль не должен превышать {self.policy.max_length} символов")
        else:
            score += min(len(password) - self.policy.min_length, 10)
        
        # Проверка требований к символам
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in self.policy.special_chars for c in password)
        
        if self.policy.require_uppercase and not has_upper:
            errors.append("Пароль должен содержать заглавные буквы")
        elif has_upper:
            score += 5
        
        if self.policy.require_lowercase and not has_lower:
            errors.append("Пароль должен содержать строчные буквы")
        elif has_lower:
            score += 5
        
        if self.policy.require_digits and not has_digit:
            errors.append("Пароль должен содержать цифры")
        elif has_digit:
            score += 5
        
        if self.policy.require_special and not has_special:
            errors.append(f"Пароль должен содержать специальные символы: {self.policy.special_chars}")
        elif has_special:
            score += 10
        
        # Проверка повторяющихся символов
        repeated_chars = self._check_repeated_chars(password)
        if repeated_chars > self.policy.max_repeated_chars:
            errors.append(f"Слишком много повторяющихся символов подряд (максимум {self.policy.max_repeated_chars})")
        
        # Проверка уникальности символов
        unique_chars = len(set(password))
        if unique_chars < self.policy.min_unique_chars:
            errors.append(f"Пароль должен содержать минимум {self.policy.min_unique_chars} уникальных символов")
        else:
            score += min(unique_chars - self.policy.min_unique_chars, 15)
        
        # Проверка популярных паролей
        if self.policy.block_common_passwords and password.lower() in self.common_passwords:
            errors.append("Пароль слишком популярен и небезопасен")
        
        # Проверка персональной информации
        if self.policy.block_personal_info and user_info:
            personal_info_errors = self._check_personal_info(password, user_info)
            errors.extend(personal_info_errors)
        
        # Проверка паттернов
        pattern_warnings = self._check_patterns(password)
        warnings.extend(pattern_warnings)
        
        # Энтропийная оценка
        entropy = self._calculate_entropy(password)
        if entropy < 30:
            warnings.append("Низкая энтропия пароля")
        elif entropy > 60:
            score += 20
        
        # Итоговая оценка силы
        strength = self._calculate_strength(score, len(errors))
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'score': score,
            'strength': strength,
            'entropy': entropy,
            'details': {
                'length': len(password),
                'unique_chars': unique_chars,
                'has_upper': has_upper,
                'has_lower': has_lower,
                'has_digit': has_digit,
                'has_special': has_special
            }
        }
    
    def _check_repeated_chars(self, password: str) -> int:
        """Проверка повторяющихся символов"""
        max_repeated = 0
        current_count = 1
        
        for i in range(1, len(password)):
            if password[i] == password[i-1]:
                current_count += 1
            else:
                max_repeated = max(max_repeated, current_count)
                current_count = 1
        
        return max(max_repeated, current_count)
    
    def _check_personal_info(self, password: str, user_info: Dict[str, str]) -> list:
        """Проверка наличия персональной информации в пароле"""
        errors = []
        password_lower = password.lower()
        
        for field, value in user_info.items():
            if value and len(value) >= 3:
                if value.lower() in password_lower:
                    errors.append(f"Пароль не должен содержать {field}")
        
        return errors
    
    def _check_patterns(self, password: str) -> list:
        """Проверка небезопасных паттернов"""
        warnings = []
        
        # Последовательности клавиатуры
        keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '123456', 'abcdef']
        for pattern in keyboard_patterns:
            if pattern in password.lower():
                warnings.append(f"Обнаружена клавиатурная последовательность: {pattern}")
        
        # Даты
        date_pattern = re.compile(r'\d{4}|\d{2}/\d{2}|\d{2}-\d{2}')
        if date_pattern.search(password):
            warnings.append("Пароль содержит дату")
        
        # Простые замены (a->@, o->0 и т.д.)
        simple_substitutions = {'@': 'a', '0': 'o', '3': 'e', '1': 'i', '5': 's'}
        simplified = password.lower()
        for symbol, letter in simple_substitutions.items():
            simplified = simplified.replace(symbol, letter)
        
        if simplified in self.common_passwords:
            warnings.append("Пароль - это популярный пароль с простыми заменами")
        
        return warnings
    
    def _calculate_entropy(self, password: str) -> float:
        """Расчет энтропии пароля"""
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26  # a-z
        if any(c.isupper() for c in password):
            charset_size += 26  # A-Z
        if any(c.isdigit() for c in password):
            charset_size += 10  # 0-9
        if any(c in self.policy.special_chars for c in password):
            charset_size += len(self.policy.special_chars)
        
        if charset_size == 0:
            return 0
        
        import math
        return len(password) * math.log2(charset_size)
    
    def _calculate_strength(self, score: int, error_count: int) -> str:
        """Определение силы пароля"""
        if error_count > 0:
            return "Очень слабый"
        elif score < 20:
            return "Слабый"
        elif score < 40:
            return "Средний"
        elif score < 60:
            return "Сильный"
        else:
            return "Очень сильный"
    
    def generate_secure_password(self, length: int = 16, 
                                include_symbols: bool = True) -> str:
        """Генерация безопасного пароля"""
        import string
        
        # Базовый набор символов
        chars = string.ascii_letters + string.digits
        
        if include_symbols:
            chars += self.policy.special_chars
        
        # Гарантируем наличие всех типов символов
        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits)
        ]
        
        if include_symbols:
            password.append(secrets.choice(self.policy.special_chars))
        
        # Дополняем до нужной длины
        for _ in range(length - len(password)):
            password.append(secrets.choice(chars))
        
        # Перемешиваем
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)

class ModernHashingAlgorithms:
    """Современные алгоритмы хеширования паролей"""
    
    @staticmethod
    def hash_password_bcrypt(password: str, rounds: int = 12) -> str:
        """Хеширование с помощью bcrypt"""
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password_bcrypt(password: str, hashed: str) -> bool:
        """Проверка пароля bcrypt"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def hash_password_argon2(password: str, time_cost: int = 3, 
                           memory_cost: int = 65536, parallelism: int = 1) -> str:
        """Хеширование с помощью Argon2"""
        ph = PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism
        )
        return ph.hash(password)
    
    @staticmethod
    def verify_password_argon2(password: str, hashed: str) -> bool:
        """Проверка пароля Argon2"""
        ph = PasswordHasher()
        try:
            ph.verify(hashed, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
    
    @staticmethod
    def hash_password_scrypt(password: str, salt: Optional[bytes] = None,
                           n: int = 16384, r: int = 8, p: int = 1) -> Tuple[str, str]:
        """Хеширование с помощью scrypt"""
        if salt is None:
            salt = secrets.token_bytes(32)
        
        dk = hashlib.scrypt(
            password.encode('utf-8'),
            salt=salt,
            n=n, r=r, p=p,
            dklen=64
        )
        
        # Возвращаем hash и salt в base64
        return (
            base64.b64encode(dk).decode('utf-8'),
            base64.b64encode(salt).decode('utf-8')
        )
    
    @staticmethod
    def verify_password_scrypt(password: str, hashed: str, salt: str,
                             n: int = 16384, r: int = 8, p: int = 1) -> bool:
        """Проверка пароля scrypt"""
        try:
            salt_bytes = base64.b64decode(salt.encode('utf-8'))
            dk = hashlib.scrypt(
                password.encode('utf-8'),
                salt=salt_bytes,
                n=n, r=r, p=p,
                dklen=64
            )
            computed_hash = base64.b64encode(dk).decode('utf-8')
            return hmac.compare_digest(computed_hash, hashed)
        except Exception:
            return False
    
    @staticmethod
    def benchmark_algorithms(password: str = "test_password_123!") -> Dict[str, Dict[str, float]]:
        """Бенчмарк различных алгоритмов хеширования"""
        results = {}
        
        # bcrypt
        start_time = time.time()
        bcrypt_hash = ModernHashingAlgorithms.hash_password_bcrypt(password)
        bcrypt_hash_time = time.time() - start_time
        
        start_time = time.time()
        ModernHashingAlgorithms.verify_password_bcrypt(password, bcrypt_hash)
        bcrypt_verify_time = time.time() - start_time
        
        results['bcrypt'] = {
            'hash_time': bcrypt_hash_time,
            'verify_time': bcrypt_verify_time,
            'total_time': bcrypt_hash_time + bcrypt_verify_time
        }
        
        # Argon2
        start_time = time.time()
        argon2_hash = ModernHashingAlgorithms.hash_password_argon2(password)
        argon2_hash_time = time.time() - start_time
        
        start_time = time.time()
        ModernHashingAlgorithms.verify_password_argon2(password, argon2_hash)
        argon2_verify_time = time.time() - start_time
        
        results['argon2'] = {
            'hash_time': argon2_hash_time,
            'verify_time': argon2_verify_time,
            'total_time': argon2_hash_time + argon2_verify_time
        }
        
        # scrypt
        start_time = time.time()
        scrypt_hash, scrypt_salt = ModernHashingAlgorithms.hash_password_scrypt(password)
        scrypt_hash_time = time.time() - start_time
        
        start_time = time.time()
        ModernHashingAlgorithms.verify_password_scrypt(password, scrypt_hash, scrypt_salt)
        scrypt_verify_time = time.time() - start_time
        
        results['scrypt'] = {
            'hash_time': scrypt_hash_time,
            'verify_time': scrypt_verify_time,
            'total_time': scrypt_hash_time + scrypt_verify_time
        }
        
        return results

class TimingAttackProtection:
    """Защита от timing-атак"""
    
    @staticmethod
    def secure_compare(a: str, b: str) -> bool:
        """Безопасное сравнение строк"""
        return hmac.compare_digest(a, b)
    
    @staticmethod
    def constant_time_user_lookup(username: str, users_db: Dict[str, Dict]) -> Optional[Dict]:
        """Поиск пользователя с защитой от timing-атак"""
        # Всегда выполняем одинаковое количество операций
        found_user = None
        dummy_hash = "$2b$12$dummy.hash.to.prevent.timing.attacks"
        
        for stored_username, user_data in users_db.items():
            # Используем secure_compare для всех пользователей
            if TimingAttackProtection.secure_compare(username, stored_username):
                found_user = user_data
        
        # Если пользователь не найден, все равно выполняем операцию хеширования
        if found_user is None:
            bcrypt.checkpw(b"dummy", dummy_hash.encode('utf-8'))
        
        return found_user
    
    @staticmethod
    def rate_limited_login(username: str, password: str, 
                          users_db: Dict[str, Dict],
                          failed_attempts: Dict[str, list]) -> Dict[str, Union[bool, str]]:
        """Логин с ограничением скорости попыток"""
        current_time = datetime.now()
        
        # Очищаем старые неудачные попытки (старше 15 минут)
        if username in failed_attempts:
            failed_attempts[username] = [
                attempt_time for attempt_time in failed_attempts[username]
                if current_time - attempt_time < timedelta(minutes=15)
            ]
        
        # Проверяем количество неудачных попыток
        attempts_count = len(failed_attempts.get(username, []))
        
        if attempts_count >= 5:
            return {
                'success': False,
                'error': 'Слишком много неудачных попыток. Попробуйте позже.',
                'locked_until': current_time + timedelta(minutes=15)
            }
        
        # Добавляем искусственную задержку, увеличивающуюся с каждой попыткой
        delay = min(attempts_count * 0.5, 3.0)  # Максимум 3 секунды
        time.sleep(delay)
        
        # Безопасный поиск пользователя
        user = TimingAttackProtection.constant_time_user_lookup(username, users_db)
        
        if user and ModernHashingAlgorithms.verify_password_bcrypt(password, user['password_hash']):
            # Успешный логин - очищаем неудачные попытки
            if username in failed_attempts:
                del failed_attempts[username]
            
            return {
                'success': True,
                'user': user
            }
        else:
            # Неудачная попытка
            if username not in failed_attempts:
                failed_attempts[username] = []
            failed_attempts[username].append(current_time)
            
            return {
                'success': False,
                'error': 'Неверное имя пользователя или пароль',
                'attempts_remaining': 5 - len(failed_attempts[username])
            }

# Генерация и управление токенами
class SecureTokenManager:
    """Менеджер для безопасной работы с токенами"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
    
    def generate_csrf_token(self) -> str:
        """Генерация CSRF токена"""
        return secrets.token_urlsafe(32)
    
    def generate_session_token(self) -> str:
        """Генерация токена сессии"""
        return secrets.token_urlsafe(64)
    
    def generate_api_key(self, prefix: str = "ak") -> str:
        """Генерация API ключа"""
        key_part = secrets.token_urlsafe(32)
        return f"{prefix}_{key_part}"
    
    def generate_reset_token(self, user_id: str, expires_in: int = 3600) -> Dict[str, Union[str, datetime]]:
        """Генерация токена для сброса пароля"""
        token_data = f"{user_id}:{int(time.time() + expires_in)}"
        token_hash = hmac.new(
            self.secret_key.encode('utf-8'),
            token_data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        token = base64.urlsafe_b64encode(
            f"{token_data}:{token_hash}".encode('utf-8')
        ).decode('utf-8')
        
        return {
            'token': token,
            'expires_at': datetime.fromtimestamp(time.time() + expires_in)
        }
    
    def verify_reset_token(self, token: str, user_id: str) -> bool:
        """Проверка токена сброса пароля"""
        try:
            decoded = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
            token_data, received_hash = decoded.rsplit(':', 1)
            
            # Проверяем подпись
            expected_hash = hmac.new(
                self.secret_key.encode('utf-8'),
                token_data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(received_hash, expected_hash):
                return False
            
            # Проверяем данные токена
            token_user_id, expires_timestamp = token_data.split(':', 1)
            
            if token_user_id != user_id:
                return False
            
            if int(expires_timestamp) < time.time():
                return False
            
            return True
            
        except Exception:
            return False
    
    def create_signed_value(self, value: str) -> str:
        """Создание подписанного значения"""
        timestamp = str(int(time.time()))
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            f"{value}:{timestamp}".encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return base64.urlsafe_b64encode(
            f"{value}:{timestamp}:{signature}".encode('utf-8')
        ).decode('utf-8')
    
    def verify_signed_value(self, signed_value: str, max_age: int = 3600) -> Optional[str]:
        """Проверка подписанного значения"""
        try:
            decoded = base64.urlsafe_b64decode(signed_value.encode('utf-8')).decode('utf-8')
            value, timestamp, signature = decoded.rsplit(':', 2)
            
            # Проверяем подпись
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                f"{value}:{timestamp}".encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return None
            
            # Проверяем возраст
            if int(timestamp) + max_age < time.time():
                return None
            
            return value
            
        except Exception:
            return None

# Менеджер секретов
class SecretManager:
    """Менеджер для работы с секретами"""
    
    def __init__(self):
        self.secrets_store = {}
    
    def add_secret(self, name: str, value: str, tags: Optional[list] = None) -> bool:
        """Добавление секрета"""
        try:
            encrypted_value = self._encrypt_secret(value)
            self.secrets_store[name] = {
                'value': encrypted_value,
                'created_at': datetime.now(),
                'tags': tags or [],
                'accessed_count': 0,
                'last_accessed': None
            }
            return True
        except Exception:
            return False
    
    def get_secret(self, name: str) -> Optional[str]:
        """Получение секрета"""
        if name not in self.secrets_store:
            return None
        
        try:
            secret_data = self.secrets_store[name]
            decrypted_value = self._decrypt_secret(secret_data['value'])
            
            # Обновляем статистику доступа
            secret_data['accessed_count'] += 1
            secret_data['last_accessed'] = datetime.now()
            
            return decrypted_value
        except Exception:
            return None
    
    def _encrypt_secret(self, value: str) -> str:
        """Шифрование секрета (упрощенная версия)"""
        # В реальном приложении используйте Fernet или подобное
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')
    
    def _decrypt_secret(self, encrypted_value: str) -> str:
        """Расшифровка секрета (упрощенная версия)"""
        # В реальном приложении используйте Fernet или подобное
        return base64.b64decode(encrypted_value.encode('utf-8')).decode('utf-8')
    
    def rotate_secret(self, name: str, new_value: str) -> bool:
        """Ротация секрета"""
        if name not in self.secrets_store:
            return False
        
        old_data = self.secrets_store[name].copy()
        
        if self.add_secret(name, new_value, old_data['tags']):
            # Сохраняем старую версию для отката
            self.secrets_store[f"{name}_old"] = old_data
            return True
        
        return False
    
    def list_secrets(self) -> Dict[str, Dict]:
        """Список всех секретов (без значений)"""
        return {
            name: {
                'created_at': data['created_at'],
                'tags': data['tags'],
                'accessed_count': data['accessed_count'],
                'last_accessed': data['last_accessed']
            }
            for name, data in self.secrets_store.items()
            if not name.endswith('_old')
        }

def demonstrate_password_security():
    """Демонстрация безопасности паролей"""
    print("🔐 Демонстрация безопасности паролей")
    print("=" * 50)
    
    # Создаем менеджер паролей
    pm = SecurePasswordManager()
    
    # Тестируем различные пароли
    test_passwords = [
        "123456",           # Очень слабый
        "password",         # Популярный
        "Password1",        # Слабый
        "MySecure123!",     # Средний
        "Tr0ub4dor&3",      # Сильный
        "correcthorsebatterystaple"  # Длинный
    ]
    
    print("\n📊 Анализ силы паролей:")
    for password in test_passwords:
        result = pm.validate_password(password)
        print(f"'{password}' - {result['strength']} (оценка: {result['score']}, энтропия: {result['entropy']:.1f})")
        
        if result['errors']:
            print(f"  ❌ Ошибки: {', '.join(result['errors'][:2])}")
        
        if result['warnings']:
            print(f"  ⚠️  Предупреждения: {', '.join(result['warnings'][:2])}")
    
    # Генерируем безопасный пароль
    secure_password = pm.generate_secure_password(16)
    secure_result = pm.validate_password(secure_password)
    print(f"\n🎲 Сгенерированный пароль: '{secure_password}'")
    print(f"   Сила: {secure_result['strength']} (оценка: {secure_result['score']})")
    
    # Бенчмарк алгоритмов
    print("\n⏱️  Бенчмарк алгоритмов хеширования:")
    benchmark = ModernHashingAlgorithms.benchmark_algorithms()
    
    for algorithm, times in benchmark.items():
        print(f"{algorithm.upper():>8}: {times['total_time']:.4f}s (hash: {times['hash_time']:.4f}s, verify: {times['verify_time']:.4f}s)")
    
    return {
        'password_analysis': [pm.validate_password(p) for p in test_passwords],
        'generated_password': secure_password,
        'benchmark': benchmark
    }
```

---

## 🔒 Криптография

Современные криптографические методы для защиты данных.

### Симметричное и асимметричное шифрование

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from typing import Tuple, Optional, Dict, Any
import json

class SymmetricEncryption:
    """Симметричное шифрование"""
    
    @staticmethod
    def generate_key() -> bytes:
        """Генерация ключа для Fernet"""
        return Fernet.generate_key()
    
    @staticmethod
    def derive_key_from_password(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """Получение ключа из пароля с помощью PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key, salt
    
    @staticmethod
    def encrypt_data(data: str, key: bytes) -> str:
        """Шифрование данных с помощью Fernet"""
        f = Fernet(key)
        encrypted = f.encrypt(data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')
    
    @staticmethod
    def decrypt_data(encrypted_data: str, key: bytes) -> Optional[str]:
        """Расшифровка данных"""
        try:
            f = Fernet(key)
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted = f.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def encrypt_file(file_path: str, key: bytes, output_path: Optional[str] = None) -> bool:
        """Шифрование файла"""
        try:
            if output_path is None:
                output_path = file_path + '.encrypted'
            
            f = Fernet(key)
            
            with open(file_path, 'rb') as infile:
                file_data = infile.read()
            
            encrypted_data = f.encrypt(file_data)
            
            with open(output_path, 'wb') as outfile:
                outfile.write(encrypted_data)
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def decrypt_file(encrypted_file_path: str, key: bytes, output_path: Optional[str] = None) -> bool:
        """Расшифровка файла"""
        try:
            if output_path is None:
                output_path = encrypted_file_path.replace('.encrypted', '.decrypted')
            
            f = Fernet(key)
            
            with open(encrypted_file_path, 'rb') as infile:
                encrypted_data = infile.read()
            
            decrypted_data = f.decrypt(encrypted_data)
            
            with open(output_path, 'wb') as outfile:
                outfile.write(decrypted_data)
            
            return True
        except Exception:
            return False

class AsymmetricEncryption:
    """Асимметричное шифрование"""
    
    @staticmethod
    def generate_key_pair(key_size: int = 2048) -> Tuple[bytes, bytes]:
        """Генерация пары ключей RSA"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )
        
        public_key = private_key.public_key()
        
        # Сериализация ключей
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    @staticmethod
    def load_private_key(private_key_pem: bytes, password: Optional[bytes] = None):
        """Загрузка приватного ключа"""
        return serialization.load_pem_private_key(
            private_key_pem,
            password=password,
        )
    
    @staticmethod
    def load_public_key(public_key_pem: bytes):
        """Загрузка публичного ключа"""
        return serialization.load_pem_public_key(public_key_pem)
    
    @staticmethod
    def encrypt_with_public_key(data: str, public_key_pem: bytes) -> str:
        """Шифрование публичным ключом"""
        public_key = AsymmetricEncryption.load_public_key(public_key_pem)
        
        encrypted = public_key.encrypt(
            data.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return base64.b64encode(encrypted).decode('utf-8')
    
    @staticmethod
    def decrypt_with_private_key(encrypted_data: str, private_key_pem: bytes) -> Optional[str]:
        """Расшифровка приватным ключом"""
        try:
            private_key = AsymmetricEncryption.load_private_key(private_key_pem)
            
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            decrypted = private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return decrypted.decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def sign_data(data: str, private_key_pem: bytes) -> str:
        """Создание цифровой подписи"""
        private_key = AsymmetricEncryption.load_private_key(private_key_pem)
        
        signature = private_key.sign(
            data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode('utf-8')
    
    @staticmethod
    def verify_signature(data: str, signature: str, public_key_pem: bytes) -> bool:
        """Проверка цифровой подписи"""
        try:
            public_key = AsymmetricEncryption.load_public_key(public_key_pem)
            signature_bytes = base64.b64decode(signature.encode('utf-8'))
            
            public_key.verify(
                signature_bytes,
                data.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

class HybridEncryption:
    """Гибридное шифрование (RSA + AES)"""
    
    @staticmethod
    def encrypt_large_data(data: str, public_key_pem: bytes) -> Dict[str, str]:
        """Шифрование больших данных гибридным способом"""
        # Генерируем симметричный ключ
        symmetric_key = Fernet.generate_key()
        
        # Шифруем данные симметричным ключом
        f = Fernet(symmetric_key)
        encrypted_data = f.encrypt(data.encode('utf-8'))
        
        # Шифруем симметричный ключ асимметричным способом
        encrypted_key = AsymmetricEncryption.encrypt_with_public_key(
            symmetric_key.decode('utf-8'), 
            public_key_pem
        )
        
        return {
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
            'encrypted_key': encrypted_key
        }
    
    @staticmethod
    def decrypt_large_data(encrypted_package: Dict[str, str], 
                          private_key_pem: bytes) -> Optional[str]:
        """Расшифровка больших данных"""
        try:
            # Расшифровываем симметричный ключ
            symmetric_key_str = AsymmetricEncryption.decrypt_with_private_key(
                encrypted_package['encrypted_key'],
                private_key_pem
            )
            
            if symmetric_key_str is None:
                return None
            
            symmetric_key = symmetric_key_str.encode('utf-8')
            
            # Расшифровываем данные симметричным ключом
            f = Fernet(symmetric_key)
            encrypted_data = base64.b64decode(encrypted_package['encrypted_data'])
            decrypted_data = f.decrypt(encrypted_data)
            
            return decrypted_data.decode('utf-8')
        except Exception:
            return None

class CryptographicUtils:
    """Криптографические утилиты"""
    
    @staticmethod
    def secure_hash(data: str, algorithm: str = 'sha256') -> str:
        """Безопасное хеширование"""
        if algorithm == 'sha256':
            digest = hashes.Hash(hashes.SHA256())
        elif algorithm == 'sha512':
            digest = hashes.Hash(hashes.SHA512())
        elif algorithm == 'sha3_256':
            digest = hashes.Hash(hashes.SHA3_256())
        else:
            raise ValueError(f"Неподдерживаемый алгоритм: {algorithm}")
        
        digest.update(data.encode('utf-8'))
        return digest.finalize().hex()
    
    @staticmethod
    def hmac_sign(data: str, key: str, algorithm: str = 'sha256') -> str:
        """HMAC подпись"""
        import hmac as hmac_lib
        
        if algorithm == 'sha256':
            hash_func = hashlib.sha256
        elif algorithm == 'sha512':
            hash_func = hashlib.sha512
        else:
            raise ValueError(f"Неподдерживаемый алгоритм: {algorithm}")
        
        signature = hmac_lib.new(
            key.encode('utf-8'),
            data.encode('utf-8'),
            hash_func
        ).hexdigest()
        
        return signature
    
    @staticmethod
    def verify_hmac(data: str, signature: str, key: str, algorithm: str = 'sha256') -> bool:
        """Проверка HMAC подписи"""
        expected_signature = CryptographicUtils.hmac_sign(data, key, algorithm)
        return hmac.compare_digest(signature, expected_signature)
    
    @staticmethod
    def generate_salt(length: int = 16) -> str:
        """Генерация соли"""
        return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8')
    
    @staticmethod
    def secure_random_string(length: int = 32) -> str:
        """Генерация безопасной случайной строки"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def key_derivation(password: str, salt: str, iterations: int = 100000) -> str:
        """Деривация ключа из пароля"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode('utf-8'),
            iterations=iterations,
        )
        key = kdf.derive(password.encode('utf-8'))
        return base64.urlsafe_b64encode(key).decode('utf-8')

def demonstrate_cryptography():
    """Демонстрация криптографических возможностей"""
    print("🔐 Демонстрация криптографии")
    print("=" * 50)
    
    # Симметричное шифрование
    print("\n🔑 Симметричное шифрование:")
    symmetric_key = SymmetricEncryption.generate_key()
    test_data = "Секретное сообщение для шифрования"
    
    encrypted = SymmetricEncryption.encrypt_data(test_data, symmetric_key)
    decrypted = SymmetricEncryption.decrypt_data(encrypted, symmetric_key)
    
    print(f"Исходное сообщение: {test_data}")
    print(f"Зашифровано: {encrypted[:50]}...")
    print(f"Расшифровано: {decrypted}")
    print(f"Успешно: {test_data == decrypted}")
    
    # Асимметричное шифрование
    print("\n🔐 Асимметричное шифрование:")
    private_key, public_key = AsymmetricEncryption.generate_key_pair()
    
    encrypted_asym = AsymmetricEncryption.encrypt_with_public_key(test_data, public_key)
    decrypted_asym = AsymmetricEncryption.decrypt_with_private_key(encrypted_asym, private_key)
    
    print(f"RSA шифрование успешно: {test_data == decrypted_asym}")
    
    # Цифровая подпись
    print("\n✍️ Цифровая подпись:")
    signature = AsymmetricEncryption.sign_data(test_data, private_key)
    is_valid = AsymmetricEncryption.verify_signature(test_data, signature, public_key)
    
    print(f"Подпись создана: {len(signature)} символов")
    print(f"Подпись действительна: {is_valid}")
    
    # Гибридное шифрование
    print("\n🔄 Гибридное шифрование:")
    large_data = "Это очень длинное сообщение " * 100
    
    encrypted_package = HybridEncryption.encrypt_large_data(large_data, public_key)
    decrypted_large = HybridEncryption.decrypt_large_data(encrypted_package, private_key)
    
    print(f"Размер исходных данных: {len(large_data)} символов")
    print(f"Гибридное шифрование успешно: {large_data == decrypted_large}")
    
    # Хеширование
    print("\n# Криптографическое хеширование:")
    hash_sha256 = CryptographicUtils.secure_hash(test_data, 'sha256')
    hash_sha512 = CryptographicUtils.secure_hash(test_data, 'sha512')
    
    print(f"SHA256: {hash_sha256}")
    print(f"SHA512: {hash_sha512[:64]}...")
    
    return {
        'symmetric_success': test_data == decrypted,
        'asymmetric_success': test_data == decrypted_asym,
        'signature_valid': is_valid,
        'hybrid_success': large_data == decrypted_large,
        'hash_sha256': hash_sha256
    }
```

Этот раздел покрывает все основные аспекты безопасности в Python: от современного хеширования паролей до криптографии и защиты от атак. 