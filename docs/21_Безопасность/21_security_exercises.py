"""
Упражнения: Безопасность в Python

Этот файл содержит практические упражнения для изучения безопасности Python
приложений, включая аутентификацию, криптографию и защиту от атак.
"""

import hashlib
import hmac
import secrets
import bcrypt
import jwt
import re
import sqlite3
import os
import base64
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging
from pathlib import Path
import json
import tempfile
from contextlib import contextmanager
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pytest

# =============================================================================
# Упражнение 1: Secure User Management System
# =============================================================================

"""
ЗАДАНИЕ 1: Secure User Management System

Создайте безопасную систему управления пользователями:

1. Класс SecureUserManager с методами:
   - register_user() - регистрация с валидацией
   - authenticate_user() - безопасная аутентификация
   - change_password() - смена пароля
   - reset_password() - сброс пароля
   - block_user() - блокировка пользователя

2. Требования безопасности:
   - Хеширование паролей с солью
   - Валидация силы пароля
   - Защита от brute force атак
   - Логирование событий безопасности
   - Rate limiting для попыток входа

3. Дополнительные функции:
   - Двухфакторная аутентификация (2FA)
   - История паролей (запрет повторного использования)
   - Автоматическая блокировка после неудачных попыток
"""

# Ваш код здесь:
@dataclass
class User:
    """Модель пользователя"""
    # TODO: Определите поля пользователя
    pass

class SecureUserManager:
    """Безопасный менеджер пользователей"""
    
    def __init__(self, db_path: str = ":memory:"):
        # TODO: Реализуйте инициализацию
        pass
    
    def register_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Регистрация пользователя с валидацией"""
        # TODO: Реализуйте метод
        pass
    
    def authenticate_user(self, username: str, password: str, ip_address: str = None) -> Dict[str, Any]:
        """Безопасная аутентификация"""
        # TODO: Реализуйте метод
        pass
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """Смена пароля"""
        # TODO: Реализуйте метод
        pass
    
    def enable_2fa(self, user_id: int) -> Dict[str, Any]:
        """Включение двухфакторной аутентификации"""
        # TODO: Реализуйте метод
        pass

# Решение:
@dataclass
class UserSolution:
    """Решение: Модель пользователя"""
    id: int
    username: str
    email: str
    password_hash: str
    is_active: bool = True
    is_locked: bool = False
    failed_attempts: int = 0
    last_login: Optional[datetime] = None
    created_at: datetime = None
    two_fa_enabled: bool = False
    two_fa_secret: Optional[str] = None

class PasswordValidator:
    """Валидатор паролей"""
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Проверка силы пароля"""
        if len(password) < 8:
            return {'valid': False, 'error': 'Password must be at least 8 characters'}
        
        if len(password) > 128:
            return {'valid': False, 'error': 'Password too long'}
        
        # Проверки на сложность
        checks = {
            'has_lower': bool(re.search(r'[a-z]', password)),
            'has_upper': bool(re.search(r'[A-Z]', password)),
            'has_digit': bool(re.search(r'\d', password)),
            'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
        
        missing = [check for check, passed in checks.items() if not passed]
        
        if len(missing) > 1:
            return {'valid': False, 'error': 'Password must contain uppercase, lowercase, digit and special character'}
        
        # Проверка на слишком простые пароли
        simple_patterns = [
            r'123456',
            r'password',
            r'qwerty',
            r'(.)\1{3,}',  # повторяющиеся символы
            r'(abc|def|ghi|jkl|mno|pqr|stu|vwx|yz)',  # последовательности
        ]
        
        for pattern in simple_patterns:
            if re.search(pattern, password.lower()):
                return {'valid': False, 'error': 'Password is too simple'}
        
        return {'valid': True, 'strength': 'strong'}

class RateLimiter:
    """Rate limiter для защиты от brute force"""
    
    def __init__(self):
        self._attempts = {}
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
    
    def is_allowed(self, identifier: str) -> Dict[str, Any]:
        """Проверка, разрешена ли попытка"""
        current_time = datetime.utcnow()
        
        if identifier not in self._attempts:
            self._attempts[identifier] = {'count': 0, 'last_attempt': current_time, 'locked_until': None}
        
        attempt_data = self._attempts[identifier]
        
        # Проверяем блокировку
        if attempt_data['locked_until'] and current_time < attempt_data['locked_until']:
            return {
                'allowed': False,
                'reason': 'rate_limited',
                'locked_until': attempt_data['locked_until'].isoformat()
            }
        
        # Сбрасываем счетчик если прошло много времени
        if current_time - attempt_data['last_attempt'] > timedelta(minutes=5):
            attempt_data['count'] = 0
            attempt_data['locked_until'] = None
        
        return {'allowed': True}
    
    def record_attempt(self, identifier: str, success: bool):
        """Записать попытку"""
        current_time = datetime.utcnow()
        
        if identifier not in self._attempts:
            self._attempts[identifier] = {'count': 0, 'last_attempt': current_time, 'locked_until': None}
        
        attempt_data = self._attempts[identifier]
        attempt_data['last_attempt'] = current_time
        
        if success:
            # Сбрасываем счетчик при успешной попытке
            attempt_data['count'] = 0
            attempt_data['locked_until'] = None
        else:
            # Увеличиваем счетчик неудачных попыток
            attempt_data['count'] += 1
            
            if attempt_data['count'] >= self.max_attempts:
                attempt_data['locked_until'] = current_time + self.lockout_duration

class SecureUserManagerSolution:
    """Решение: Безопасный менеджер пользователей"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = None
        self.rate_limiter = RateLimiter()
        self.password_validator = PasswordValidator()
        self.logger = logging.getLogger('security')
        self._setup_database()
    
    def _setup_database(self):
        """Настройка базы данных"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
        cursor = self.connection.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                is_locked BOOLEAN DEFAULT FALSE,
                failed_attempts INTEGER DEFAULT 0,
                last_login TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                two_fa_enabled BOOLEAN DEFAULT FALSE,
                two_fa_secret TEXT
            )
        ''')
        
        # Таблица истории паролей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Таблица логов безопасности
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_type TEXT NOT NULL,
                ip_address TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.connection.commit()
    
    def _hash_password(self, password: str) -> str:
        """Хеширование пароля с bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Проверка пароля"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def _log_security_event(self, user_id: Optional[int], event_type: str, 
                           ip_address: str = None, details: str = None):
        """Логирование событий безопасности"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO security_logs (user_id, event_type, ip_address, details)
                VALUES (?, ?, ?, ?)
            ''', (user_id, event_type, ip_address, details))
            self.connection.commit()
            
            self.logger.info(f"Security event: {event_type} for user {user_id}")
        except Exception as e:
            self.logger.error(f"Failed to log security event: {e}")
    
    def _validate_email(self, email: str) -> bool:
        """Валидация email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_username(self, username: str) -> bool:
        """Валидация имени пользователя"""
        if len(username) < 3 or len(username) > 20:
            return False
        return bool(re.match(r'^[a-zA-Z0-9_]+$', username))
    
    def _check_password_history(self, user_id: int, new_password: str, history_limit: int = 5) -> bool:
        """Проверка истории паролей"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT password_hash FROM password_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, history_limit))
        
        for row in cursor.fetchall():
            if self._verify_password(new_password, row['password_hash']):
                return False  # Пароль уже использовался
        
        return True
    
    def _add_password_to_history(self, user_id: int, password_hash: str):
        """Добавление пароля в историю"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO password_history (user_id, password_hash)
            VALUES (?, ?)
        ''', (user_id, password_hash))
        
        # Удаляем старые записи (оставляем только последние 10)
        cursor.execute('''
            DELETE FROM password_history
            WHERE user_id = ? AND id NOT IN (
                SELECT id FROM password_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT 10
            )
        ''', (user_id, user_id))
        
        self.connection.commit()
    
    def register_user(self, username: str, email: str, password: str, ip_address: str = None) -> Dict[str, Any]:
        """Регистрация пользователя с валидацией"""
        
        # Валидация входных данных
        if not self._validate_username(username):
            return {'success': False, 'error': 'Invalid username format'}
        
        if not self._validate_email(email):
            return {'success': False, 'error': 'Invalid email format'}
        
        # Проверка силы пароля
        password_check = self.password_validator.validate_password_strength(password)
        if not password_check['valid']:
            return {'success': False, 'error': password_check['error']}
        
        try:
            cursor = self.connection.cursor()
            
            # Проверка существования пользователя
            cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
            if cursor.fetchone():
                self._log_security_event(None, 'registration_duplicate_attempt', ip_address, 
                                       f'Username: {username}, Email: {email}')
                return {'success': False, 'error': 'Username or email already exists'}
            
            # Хеширование пароля
            password_hash = self._hash_password(password)
            
            # Создание пользователя
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            
            user_id = cursor.lastrowid
            self.connection.commit()
            
            # Добавляем пароль в историю
            self._add_password_to_history(user_id, password_hash)
            
            # Логирование
            self._log_security_event(user_id, 'user_registered', ip_address)
            
            return {
                'success': True,
                'user_id': user_id,
                'username': username,
                'message': 'User registered successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Registration failed: {e}")
            return {'success': False, 'error': 'Registration failed'}
    
    def authenticate_user(self, username: str, password: str, ip_address: str = None) -> Dict[str, Any]:
        """Безопасная аутентификация"""
        
        # Проверка rate limiting
        rate_check = self.rate_limiter.is_allowed(f"login:{username}:{ip_address}")
        if not rate_check['allowed']:
            self._log_security_event(None, 'rate_limit_exceeded', ip_address, 
                                   f'Username: {username}')
            return {
                'success': False, 
                'error': 'Too many failed attempts. Please try again later.',
                'locked_until': rate_check.get('locked_until')
            }
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT id, username, email, password_hash, is_active, is_locked, 
                       failed_attempts, two_fa_enabled
                FROM users
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            
            if not user:
                self.rate_limiter.record_attempt(f"login:{username}:{ip_address}", False)
                self._log_security_event(None, 'login_failed_invalid_user', ip_address, 
                                       f'Username: {username}')
                return {'success': False, 'error': 'Invalid credentials'}
            
            if not user['is_active']:
                self._log_security_event(user['id'], 'login_failed_inactive', ip_address)
                return {'success': False, 'error': 'Account is inactive'}
            
            if user['is_locked']:
                self._log_security_event(user['id'], 'login_failed_locked', ip_address)
                return {'success': False, 'error': 'Account is locked'}
            
            # Проверка пароля
            if self._verify_password(password, user['password_hash']):
                # Успешная аутентификация
                self.rate_limiter.record_attempt(f"login:{username}:{ip_address}", True)
                
                # Обновляем информацию о входе
                cursor.execute('''
                    UPDATE users 
                    SET last_login = CURRENT_TIMESTAMP, failed_attempts = 0
                    WHERE id = ?
                ''', (user['id'],))
                self.connection.commit()
                
                self._log_security_event(user['id'], 'login_successful', ip_address)
                
                return {
                    'success': True,
                    'user_id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'two_fa_required': user['two_fa_enabled']
                }
            else:
                # Неудачная попытка
                self.rate_limiter.record_attempt(f"login:{username}:{ip_address}", False)
                
                # Увеличиваем счетчик неудачных попыток
                new_failed_attempts = user['failed_attempts'] + 1
                should_lock = new_failed_attempts >= 5
                
                cursor.execute('''
                    UPDATE users 
                    SET failed_attempts = ?, is_locked = ?
                    WHERE id = ?
                ''', (new_failed_attempts, should_lock, user['id']))
                self.connection.commit()
                
                event_type = 'account_locked' if should_lock else 'login_failed_invalid_password'
                self._log_security_event(user['id'], event_type, ip_address)
                
                error_msg = 'Account locked due to too many failed attempts' if should_lock else 'Invalid credentials'
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return {'success': False, 'error': 'Authentication error'}
    
    def change_password(self, user_id: int, old_password: str, new_password: str, ip_address: str = None) -> Dict[str, Any]:
        """Смена пароля"""
        
        # Проверка силы нового пароля
        password_check = self.password_validator.validate_password_strength(new_password)
        if not password_check['valid']:
            return {'success': False, 'error': password_check['error']}
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return {'success': False, 'error': 'User not found'}
            
            # Проверка старого пароля
            if not self._verify_password(old_password, user['password_hash']):
                self._log_security_event(user_id, 'password_change_failed_invalid_old', ip_address)
                return {'success': False, 'error': 'Invalid current password'}
            
            # Проверка истории паролей
            if not self._check_password_history(user_id, new_password):
                self._log_security_event(user_id, 'password_change_failed_reused', ip_address)
                return {'success': False, 'error': 'Password was recently used. Please choose a different password.'}
            
            # Обновление пароля
            new_password_hash = self._hash_password(new_password)
            cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', 
                         (new_password_hash, user_id))
            self.connection.commit()
            
            # Добавляем в историю
            self._add_password_to_history(user_id, new_password_hash)
            
            self._log_security_event(user_id, 'password_changed', ip_address)
            
            return {'success': True, 'message': 'Password changed successfully'}
            
        except Exception as e:
            self.logger.error(f"Password change failed: {e}")
            return {'success': False, 'error': 'Password change failed'}
    
    def enable_2fa(self, user_id: int) -> Dict[str, Any]:
        """Включение двухфакторной аутентификации"""
        try:
            # Генерируем секретный ключ для 2FA
            secret = secrets.token_urlsafe(32)
            
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE users 
                SET two_fa_enabled = TRUE, two_fa_secret = ?
                WHERE id = ?
            ''', (secret, user_id))
            self.connection.commit()
            
            self._log_security_event(user_id, '2fa_enabled')
            
            return {
                'success': True,
                'secret': secret,
                'message': '2FA enabled successfully'
            }
            
        except Exception as e:
            self.logger.error(f"2FA enable failed: {e}")
            return {'success': False, 'error': '2FA setup failed'}
    
    def unlock_user(self, user_id: int, admin_user_id: int, ip_address: str = None) -> Dict[str, Any]:
        """Разблокировка пользователя администратором"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE users 
                SET is_locked = FALSE, failed_attempts = 0
                WHERE id = ?
            ''', (user_id,))
            self.connection.commit()
            
            self._log_security_event(user_id, 'account_unlocked_by_admin', ip_address,
                                   f'Admin ID: {admin_user_id}')
            
            return {'success': True, 'message': 'User unlocked successfully'}
            
        except Exception as e:
            self.logger.error(f"User unlock failed: {e}")
            return {'success': False, 'error': 'Unlock failed'}
    
    def get_security_logs(self, user_id: int = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Получение логов безопасности"""
        try:
            cursor = self.connection.cursor()
            if user_id:
                cursor.execute('''
                    SELECT event_type, ip_address, details, timestamp
                    FROM security_logs
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (user_id, limit))
            else:
                cursor.execute('''
                    SELECT user_id, event_type, ip_address, details, timestamp
                    FROM security_logs
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            self.logger.error(f"Failed to get security logs: {e}")
            return []

# Тесты для SecureUserManager
class TestSecureUserManager:
    """Тесты безопасного менеджера пользователей"""
    
    @pytest.fixture
    def user_manager(self):
        """Fixture менеджера пользователей"""
        return SecureUserManagerSolution()
    
    def test_user_registration_success(self, user_manager):
        """Тест успешной регистрации"""
        result = user_manager.register_user("testuser", "test@example.com", "SecurePass123!")
        
        assert result['success'] is True
        assert 'user_id' in result
        assert result['username'] == "testuser"
    
    def test_user_registration_weak_password(self, user_manager):
        """Тест регистрации со слабым паролем"""
        result = user_manager.register_user("testuser", "test@example.com", "weak")
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_user_registration_duplicate(self, user_manager):
        """Тест регистрации дублирующегося пользователя"""
        # Первая регистрация
        user_manager.register_user("testuser", "test@example.com", "SecurePass123!")
        
        # Попытка дублирования
        result = user_manager.register_user("testuser", "test2@example.com", "AnotherPass456!")
        
        assert result['success'] is False
        assert 'already exists' in result['error']
    
    def test_authentication_success(self, user_manager):
        """Тест успешной аутентификации"""
        # Регистрация
        user_manager.register_user("authuser", "auth@example.com", "AuthPass123!")
        
        # Аутентификация
        result = user_manager.authenticate_user("authuser", "AuthPass123!")
        
        assert result['success'] is True
        assert result['username'] == "authuser"
    
    def test_authentication_failure(self, user_manager):
        """Тест неудачной аутентификации"""
        # Регистрация
        user_manager.register_user("authuser", "auth@example.com", "AuthPass123!")
        
        # Неправильный пароль
        result = user_manager.authenticate_user("authuser", "wrongpassword")
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_password_change(self, user_manager):
        """Тест смены пароля"""
        # Регистрация
        reg_result = user_manager.register_user("pwduser", "pwd@example.com", "OldPass123!")
        user_id = reg_result['user_id']
        
        # Смена пароля
        result = user_manager.change_password(user_id, "OldPass123!", "NewPass456!")
        
        assert result['success'] is True
        
        # Проверка нового пароля
        auth_result = user_manager.authenticate_user("pwduser", "NewPass456!")
        assert auth_result['success'] is True

# =============================================================================
# Упражнение 2: Secure File Storage System
# =============================================================================

"""
ЗАДАНИЕ 2: Secure File Storage System

Создайте безопасную систему хранения файлов:

1. Класс SecureFileStorage с методами:
   - upload_file() - загрузка с шифрованием
   - download_file() - скачивание с расшифровкой
   - delete_file() - безопасное удаление
   - share_file() - создание временных ссылок

2. Требования безопасности:
   - Шифрование файлов перед сохранением
   - Валидация типов файлов
   - Проверка размера файлов
   - Контроль доступа к файлам
   - Аудит операций с файлами

3. Дополнительные функции:
   - Целостность файлов (checksums)
   - Версионирование файлов
   - Автоматическое удаление временных файлов
"""

# Ваш код здесь:
class SecureFileStorage:
    """Безопасное хранилище файлов"""
    
    def __init__(self, storage_path: str):
        # TODO: Реализуйте инициализацию
        pass
    
    def upload_file(self, file_content: bytes, filename: str, user_id: int) -> Dict[str, Any]:
        """Загрузка файла с шифрованием"""
        # TODO: Реализуйте метод
        pass
    
    def download_file(self, file_id: str, user_id: int) -> Dict[str, Any]:
        """Скачивание файла с расшифровкой"""
        # TODO: Реализуйте метод
        pass
    
    def delete_file(self, file_id: str, user_id: int) -> Dict[str, Any]:
        """Безопасное удаление файла"""
        # TODO: Реализуйте метод
        pass

# Решение (краткая версия):
import uuid
from cryptography.fernet import Fernet

class SecureFileStorageSolution:
    """Решение: Безопасное хранилище файлов"""
    
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.encryption_key = Fernet.generate_key()
        self.fernet = Fernet(self.encryption_key)
        self.db_path = self.storage_path / "files.db"
        self._setup_database()
        
        # Допустимые типы файлов
        self.allowed_extensions = {'.txt', '.pdf', '.docx', '.jpg', '.png', '.gif'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    def _setup_database(self):
        """Настройка базы данных для метаданных файлов"""
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                original_size INTEGER NOT NULL,
                encrypted_size INTEGER NOT NULL,
                checksum TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_path TEXT NOT NULL,
                is_deleted BOOLEAN DEFAULT FALSE
            )
        ''')
        
        self.connection.commit()
    
    def _validate_file(self, filename: str, content: bytes) -> Dict[str, Any]:
        """Валидация файла"""
        # Проверка расширения
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            return {'valid': False, 'error': f'File type not allowed. Allowed: {self.allowed_extensions}'}
        
        # Проверка размера
        if len(content) > self.max_file_size:
            return {'valid': False, 'error': f'File too large. Max size: {self.max_file_size} bytes'}
        
        # Проверка на пустой файл
        if len(content) == 0:
            return {'valid': False, 'error': 'Empty file not allowed'}
        
        return {'valid': True}
    
    def _calculate_checksum(self, content: bytes) -> str:
        """Вычисление контрольной суммы"""
        return hashlib.sha256(content).hexdigest()
    
    def upload_file(self, file_content: bytes, filename: str, user_id: int) -> Dict[str, Any]:
        """Загрузка файла с шифрованием"""
        # Валидация
        validation = self._validate_file(filename, file_content)
        if not validation['valid']:
            return {'success': False, 'error': validation['error']}
        
        try:
            # Генерация уникального ID
            file_id = str(uuid.uuid4())
            
            # Вычисление checksum оригинального файла
            original_checksum = self._calculate_checksum(file_content)
            
            # Шифрование
            encrypted_content = self.fernet.encrypt(file_content)
            
            # Сохранение зашифрованного файла
            file_path = self.storage_path / f"{file_id}.enc"
            with open(file_path, 'wb') as f:
                f.write(encrypted_content)
            
            # Сохранение метаданных
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO files (id, filename, original_size, encrypted_size, 
                                 checksum, user_id, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (file_id, filename, len(file_content), len(encrypted_content),
                  original_checksum, user_id, str(file_path)))
            self.connection.commit()
            
            return {
                'success': True,
                'file_id': file_id,
                'filename': filename,
                'size': len(file_content),
                'checksum': original_checksum
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Upload failed: {e}'}
    
    def download_file(self, file_id: str, user_id: int) -> Dict[str, Any]:
        """Скачивание файла с расшифровкой"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT filename, file_path, checksum, original_size, user_id, is_deleted
                FROM files WHERE id = ?
            ''', (file_id,))
            
            file_record = cursor.fetchone()
            if not file_record:
                return {'success': False, 'error': 'File not found'}
            
            # Проверка прав доступа
            if file_record[4] != user_id:  # user_id
                return {'success': False, 'error': 'Access denied'}
            
            # Проверка, что файл не удален
            if file_record[5]:  # is_deleted
                return {'success': False, 'error': 'File has been deleted'}
            
            # Чтение зашифрованного файла
            file_path = Path(file_record[1])
            if not file_path.exists():
                return {'success': False, 'error': 'File data not found'}
            
            with open(file_path, 'rb') as f:
                encrypted_content = f.read()
            
            # Расшифровка
            decrypted_content = self.fernet.decrypt(encrypted_content)
            
            # Проверка целостности
            current_checksum = self._calculate_checksum(decrypted_content)
            if current_checksum != file_record[2]:  # checksum
                return {'success': False, 'error': 'File integrity check failed'}
            
            return {
                'success': True,
                'filename': file_record[0],
                'content': decrypted_content,
                'size': len(decrypted_content),
                'checksum': current_checksum
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Download failed: {e}'}
    
    def delete_file(self, file_id: str, user_id: int) -> Dict[str, Any]:
        """Безопасное удаление файла"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT file_path, user_id, is_deleted
                FROM files WHERE id = ?
            ''', (file_id,))
            
            file_record = cursor.fetchone()
            if not file_record:
                return {'success': False, 'error': 'File not found'}
            
            # Проверка прав доступа
            if file_record[1] != user_id:
                return {'success': False, 'error': 'Access denied'}
            
            if file_record[2]:  # уже удален
                return {'success': False, 'error': 'File already deleted'}
            
            # Физическое удаление файла
            file_path = Path(file_record[0])
            if file_path.exists():
                file_path.unlink()
            
            # Пометка как удаленного в БД
            cursor.execute('UPDATE files SET is_deleted = TRUE WHERE id = ?', (file_id,))
            self.connection.commit()
            
            return {'success': True, 'message': 'File deleted successfully'}
            
        except Exception as e:
            return {'success': False, 'error': f'Delete failed: {e}'}

# =============================================================================
# Упражнение 3: Secure API with JWT Authentication
# =============================================================================

"""
ЗАДАНИЕ 3: Secure API with JWT Authentication

Создайте безопасный API с JWT аутентификацией:

1. Класс SecureAPI с endpoints:
   - /auth/login - аутентификация
   - /auth/refresh - обновление токена
   - /api/profile - получение профиля (защищен)
   - /api/admin - admin endpoint (защищен)

2. Middleware для:
   - Валидации JWT токенов
   - Role-based access control (RBAC)
   - Rate limiting
   - Request logging

3. Безопасность:
   - CORS настройки
   - CSRF защита
   - Input validation
   - Output sanitization
"""

# Ваш код здесь (краткое решение):
class SecureAPIMiddleware:
    """Middleware для безопасного API"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.rate_limiter = RateLimiter()
    
    def validate_jwt(self, token: str) -> Dict[str, Any]:
        """Валидация JWT токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {'valid': True, 'payload': payload}
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Invalid token'}
    
    def check_permissions(self, user_role: str, required_role: str) -> bool:
        """Проверка прав доступа"""
        role_hierarchy = {'user': 1, 'admin': 2, 'superadmin': 3}
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level

# =============================================================================
# Запуск упражнений
# =============================================================================

def run_exercises():
    """Запуск всех упражнений"""
    print("=== Упражнения: Безопасность ===\n")
    
    # 1. Secure User Management
    print("1. Secure User Management System...")
    user_manager = SecureUserManagerSolution()
    
    # Регистрация пользователя
    reg_result = user_manager.register_user("alice", "alice@example.com", "SecurePass123!")
    print(f"   Регистрация: {reg_result['success']}")
    
    # Аутентификация
    auth_result = user_manager.authenticate_user("alice", "SecurePass123!")
    print(f"   Аутентификация: {auth_result['success']}")
    
    # Смена пароля
    if reg_result['success']:
        pwd_result = user_manager.change_password(
            reg_result['user_id'], "SecurePass123!", "NewSecurePass456!"
        )
        print(f"   Смена пароля: {pwd_result['success']}")
    
    # 2. Secure File Storage
    print("\n2. Secure File Storage...")
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = SecureFileStorageSolution(temp_dir)
        
        # Загрузка файла
        test_content = b"This is a test file content"
        upload_result = storage.upload_file(test_content, "test.txt", user_id=1)
        print(f"   Загрузка файла: {upload_result['success']}")
        
        if upload_result['success']:
            # Скачивание файла
            download_result = storage.download_file(upload_result['file_id'], user_id=1)
            print(f"   Скачивание файла: {download_result['success']}")
            
            # Проверка содержимого
            if download_result['success']:
                content_match = download_result['content'] == test_content
                print(f"   Целостность файла: {content_match}")
    
    # 3. JWT Authentication
    print("\n3. JWT Authentication...")
    api_middleware = SecureAPIMiddleware("super-secret-key")
    
    # Создание токена
    payload = {'user_id': 1, 'role': 'user', 'exp': datetime.utcnow() + timedelta(hours=1)}
    token = jwt.encode(payload, "super-secret-key", algorithm='HS256')
    print(f"   Токен создан: {len(token)} символов")
    
    # Валидация токена
    validation = api_middleware.validate_jwt(token)
    print(f"   Валидация токена: {validation['valid']}")
    
    # Проверка прав доступа
    has_admin_access = api_middleware.check_permissions('user', 'admin')
    print(f"   Доступ к admin: {has_admin_access}")
    
    print("\n✅ Все упражнения выполнены успешно!")
    print("🔒 Теперь вы можете создавать безопасные Python приложения!")

if __name__ == "__main__":
    run_exercises() 