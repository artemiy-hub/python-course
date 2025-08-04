"""
Примеры: Безопасность в Python

Этот файл содержит практические примеры обеспечения безопасности Python
приложений, включая хеширование паролей, криптографию, валидацию входных
данных и защиту от основных уязвимостей.
"""

import hashlib
import hmac
import secrets
import bcrypt
import argon2
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import jwt
import re
import sqlite3
import os
import base64
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
import logging
from pathlib import Path
import json
from contextlib import contextmanager
import tempfile

# Настройка логирования для безопасности
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# =============================================================================
# Пример 1: Безопасное хеширование паролей
# =============================================================================

class PasswordSecurity:
    """Класс для безопасной работы с паролями"""
    
    def __init__(self):
        # Argon2 hasher с настройками по умолчанию
        self.argon2_hasher = PasswordHasher()
        
        # Настройки для bcrypt
        self.bcrypt_rounds = 12
        
        # Настройки для PBKDF2
        self.pbkdf2_iterations = 100000

    def hash_password_bcrypt(self, password: str) -> str:
        """Хеширование пароля с использованием bcrypt"""
        # Генерируем соль и хешируем пароль
        salt = bcrypt.gensalt(rounds=self.bcrypt_rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password_bcrypt(self, password: str, hashed: str) -> bool:
        """Проверка пароля с bcrypt хешем"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            security_logger.warning(f"Password verification failed: {e}")
            return False

    def hash_password_argon2(self, password: str) -> str:
        """Хеширование пароля с использованием Argon2"""
        try:
            return self.argon2_hasher.hash(password)
        except Exception as e:
            security_logger.error(f"Argon2 hashing failed: {e}")
            raise

    def verify_password_argon2(self, password: str, hashed: str) -> bool:
        """Проверка пароля с Argon2 хешем"""
        try:
            self.argon2_hasher.verify(hashed, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        except Exception as e:
            security_logger.warning(f"Argon2 verification failed: {e}")
            return False

    def hash_password_pbkdf2(self, password: str, salt: bytes = None) -> Tuple[str, str]:
        """Хеширование пароля с использованием PBKDF2"""
        if salt is None:
            salt = secrets.token_bytes(32)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.pbkdf2_iterations,
        )
        
        key = kdf.derive(password.encode('utf-8'))
        
        # Возвращаем base64-encoded хеш и соль
        hashed = base64.b64encode(key).decode('utf-8')
        salt_encoded = base64.b64encode(salt).decode('utf-8')
        
        return hashed, salt_encoded

    def verify_password_pbkdf2(self, password: str, hashed: str, salt: str) -> bool:
        """Проверка пароля с PBKDF2 хешем"""
        try:
            salt_bytes = base64.b64decode(salt.encode('utf-8'))
            expected_hash, _ = self.hash_password_pbkdf2(password, salt_bytes)
            
            # Используем secure compare для защиты от timing attacks
            return hmac.compare_digest(hashed, expected_hash)
        except Exception as e:
            security_logger.warning(f"PBKDF2 verification failed: {e}")
            return False

    def generate_secure_password(self, length: int = 16) -> str:
        """Генерация криптографически стойкого пароля"""
        # Набор символов для пароля
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def check_password_strength(self, password: str) -> Dict[str, Any]:
        """Проверка силы пароля"""
        score = 0
        feedback = []
        
        # Длина
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Пароль должен быть не менее 8 символов")
        
        # Наличие разных типов символов
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Добавьте строчные буквы")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Добавьте заглавные буквы")
        
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Добавьте цифры")
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            feedback.append("Добавьте специальные символы")
        
        # Проверка на популярные пароли (упрощенная)
        weak_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein']
        if password.lower() in weak_passwords:
            score = 0
            feedback.append("Пароль слишком популярный")
        
        # Определение уровня
        if score >= 6:
            strength = "Сильный"
        elif score >= 4:
            strength = "Средний"
        elif score >= 2:
            strength = "Слабый"
        else:
            strength = "Очень слабый"
        
        return {
            'score': score,
            'strength': strength,
            'feedback': feedback
        }

def password_security_demo():
    """Демонстрация безопасной работы с паролями"""
    print("=== Password Security Demo ===")
    
    ps = PasswordSecurity()
    test_password = "MySecurePassword123!"
    
    print(f"Тестовый пароль: {test_password}")
    
    # Проверка силы пароля
    strength = ps.check_password_strength(test_password)
    print(f"Сила пароля: {strength['strength']} (score: {strength['score']})")
    
    # Bcrypt
    print("\n--- BCrypt ---")
    bcrypt_hash = ps.hash_password_bcrypt(test_password)
    print(f"BCrypt hash: {bcrypt_hash}")
    print(f"Verification: {ps.verify_password_bcrypt(test_password, bcrypt_hash)}")
    
    # Argon2
    print("\n--- Argon2 ---")
    argon2_hash = ps.hash_password_argon2(test_password)
    print(f"Argon2 hash: {argon2_hash}")
    print(f"Verification: {ps.verify_password_argon2(test_password, argon2_hash)}")
    
    # PBKDF2
    print("\n--- PBKDF2 ---")
    pbkdf2_hash, salt = ps.hash_password_pbkdf2(test_password)
    print(f"PBKDF2 hash: {pbkdf2_hash}")
    print(f"Salt: {salt}")
    print(f"Verification: {ps.verify_password_pbkdf2(test_password, pbkdf2_hash, salt)}")
    
    # Генерация безопасного пароля
    secure_password = ps.generate_secure_password(16)
    print(f"\nСгенерированный пароль: {secure_password}")
    
    return ps

# =============================================================================
# Пример 2: Симметричное и асимметричное шифрование
# =============================================================================

class CryptographyManager:
    """Менеджер для работы с шифрованием"""
    
    def __init__(self):
        self.fernet_key = None
        self.fernet_cipher = None
        self.rsa_private_key = None
        self.rsa_public_key = None

    def generate_symmetric_key(self) -> bytes:
        """Генерация ключа для симметричного шифрования"""
        key = Fernet.generate_key()
        self.fernet_key = key
        self.fernet_cipher = Fernet(key)
        return key

    def load_symmetric_key(self, key: bytes):
        """Загрузка существующего ключа"""
        self.fernet_key = key
        self.fernet_cipher = Fernet(key)

    def encrypt_symmetric(self, data: str) -> bytes:
        """Симметричное шифрование"""
        if not self.fernet_cipher:
            raise ValueError("Symmetric key not set")
        
        return self.fernet_cipher.encrypt(data.encode('utf-8'))

    def decrypt_symmetric(self, encrypted_data: bytes) -> str:
        """Симметричное расшифрование"""
        if not self.fernet_cipher:
            raise ValueError("Symmetric key not set")
        
        try:
            decrypted = self.fernet_cipher.decrypt(encrypted_data)
            return decrypted.decode('utf-8')
        except Exception as e:
            security_logger.error(f"Decryption failed: {e}")
            raise

    def generate_rsa_keys(self, key_size: int = 2048) -> Tuple[bytes, bytes]:
        """Генерация RSA ключей"""
        # Генерация приватного ключа
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )
        
        # Получение публичного ключа
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
        
        self.rsa_private_key = private_key
        self.rsa_public_key = public_key
        
        return private_pem, public_pem

    def load_rsa_keys(self, private_pem: bytes, public_pem: bytes):
        """Загрузка RSA ключей"""
        self.rsa_private_key = serialization.load_pem_private_key(
            private_pem, password=None
        )
        self.rsa_public_key = serialization.load_pem_public_key(public_pem)

    def encrypt_rsa(self, data: str) -> bytes:
        """RSA шифрование"""
        if not self.rsa_public_key:
            raise ValueError("RSA public key not set")
        
        # RSA может шифровать только ограниченное количество данных
        max_length = (self.rsa_public_key.key_size // 8) - 2 * (hashes.SHA256().digest_size) - 2
        
        if len(data.encode('utf-8')) > max_length:
            raise ValueError(f"Data too long for RSA encryption. Max: {max_length} bytes")
        
        encrypted = self.rsa_public_key.encrypt(
            data.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return encrypted

    def decrypt_rsa(self, encrypted_data: bytes) -> str:
        """RSA расшифрование"""
        if not self.rsa_private_key:
            raise ValueError("RSA private key not set")
        
        try:
            decrypted = self.rsa_private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted.decode('utf-8')
        except Exception as e:
            security_logger.error(f"RSA decryption failed: {e}")
            raise

    def sign_data(self, data: str) -> bytes:
        """Создание цифровой подписи"""
        if not self.rsa_private_key:
            raise ValueError("RSA private key not set")
        
        signature = self.rsa_private_key.sign(
            data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return signature

    def verify_signature(self, data: str, signature: bytes) -> bool:
        """Проверка цифровой подписи"""
        if not self.rsa_public_key:
            raise ValueError("RSA public key not set")
        
        try:
            self.rsa_public_key.verify(
                signature,
                data.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            security_logger.warning(f"Signature verification failed: {e}")
            return False

    def encrypt_file(self, file_path: str, encrypted_path: str):
        """Шифрование файла"""
        if not self.fernet_cipher:
            raise ValueError("Symmetric key not set")
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = self.fernet_cipher.encrypt(file_data)
        
        with open(encrypted_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

    def decrypt_file(self, encrypted_path: str, decrypted_path: str):
        """Расшифрование файла"""
        if not self.fernet_cipher:
            raise ValueError("Symmetric key not set")
        
        with open(encrypted_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        try:
            decrypted_data = self.fernet_cipher.decrypt(encrypted_data)
            
            with open(decrypted_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
        except Exception as e:
            security_logger.error(f"File decryption failed: {e}")
            raise

def cryptography_demo():
    """Демонстрация криптографических функций"""
    print("\n=== Cryptography Demo ===")
    
    crypto = CryptographyManager()
    test_data = "Это секретные данные, которые нужно зашифровать!"
    
    # Симметричное шифрование
    print("--- Симметричное шифрование (Fernet) ---")
    symmetric_key = crypto.generate_symmetric_key()
    print(f"Ключ: {symmetric_key.decode() if isinstance(symmetric_key, bytes) else symmetric_key}")
    
    encrypted_symmetric = crypto.encrypt_symmetric(test_data)
    print(f"Зашифровано: {encrypted_symmetric}")
    
    decrypted_symmetric = crypto.decrypt_symmetric(encrypted_symmetric)
    print(f"Расшифровано: {decrypted_symmetric}")
    
    # Асимметричное шифрование
    print("\n--- Асимметричное шифрование (RSA) ---")
    private_key, public_key = crypto.generate_rsa_keys()
    print(f"Приватный ключ сгенерирован: {len(private_key)} байт")
    print(f"Публичный ключ сгенерирован: {len(public_key)} байт")
    
    # Короткие данные для RSA
    short_data = "Secret message"
    encrypted_rsa = crypto.encrypt_rsa(short_data)
    print(f"RSA зашифровано: {len(encrypted_rsa)} байт")
    
    decrypted_rsa = crypto.decrypt_rsa(encrypted_rsa)
    print(f"RSA расшифровано: {decrypted_rsa}")
    
    # Цифровая подпись
    print("\n--- Цифровая подпись ---")
    signature = crypto.sign_data(test_data)
    print(f"Подпись создана: {len(signature)} байт")
    
    is_valid = crypto.verify_signature(test_data, signature)
    print(f"Подпись валидна: {is_valid}")
    
    # Проверка с измененными данными
    is_valid_fake = crypto.verify_signature(test_data + " (изменено)", signature)
    print(f"Подпись для измененных данных: {is_valid_fake}")
    
    return crypto

# =============================================================================
# Пример 3: JWT токены и сессии
# =============================================================================

class TokenManager:
    """Менеджер для работы с JWT токенами"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = 'HS256'
    
    def create_access_token(self, user_id: str, permissions: List[str] = None, 
                           expires_delta: timedelta = None) -> str:
        """Создание access токена"""
        if expires_delta is None:
            expires_delta = timedelta(minutes=15)
        
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            'user_id': user_id,
            'permissions': permissions or [],
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str, expires_delta: timedelta = None) -> str:
        """Создание refresh токена"""
        if expires_delta is None:
            expires_delta = timedelta(days=30)
        
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            'user_id': user_id,
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Проверка и декодирование токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """Обновление access токена с помощью refresh токена"""
        try:
            payload = self.verify_token(refresh_token)
            
            if payload.get('type') != 'refresh':
                raise ValueError("Not a refresh token")
            
            user_id = payload['user_id']
            return self.create_access_token(user_id)
            
        except Exception as e:
            security_logger.warning(f"Token refresh failed: {e}")
            raise
    
    def extract_user_from_token(self, token: str) -> Dict[str, Any]:
        """Извлечение данных пользователя из токена"""
        payload = self.verify_token(token)
        
        return {
            'user_id': payload.get('user_id'),
            'permissions': payload.get('permissions', []),
            'issued_at': datetime.fromtimestamp(payload.get('iat', 0)),
            'expires_at': datetime.fromtimestamp(payload.get('exp', 0)),
            'token_type': payload.get('type', 'unknown')
        }

class SessionManager:
    """Менеджер сессий"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = timedelta(hours=2)
    
    def create_session(self, user_id: str, user_data: Dict[str, Any] = None) -> str:
        """Создание новой сессии"""
        session_id = secrets.token_urlsafe(32)
        
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'last_activity': datetime.utcnow(),
            'user_data': user_data or {},
            'is_active': True
        }
        
        self.sessions[session_id] = session_data
        
        security_logger.info(f"Session created for user {user_id}: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Получение данных сессии"""
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        # Проверка timeout
        if datetime.utcnow() - session['last_activity'] > self.session_timeout:
            self.destroy_session(session_id)
            return None
        
        # Обновление времени активности
        session['last_activity'] = datetime.utcnow()
        
        return session
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Обновление данных сессии"""
        session = self.get_session(session_id)
        
        if not session:
            return False
        
        session['user_data'].update(data)
        session['last_activity'] = datetime.utcnow()
        
        return True
    
    def destroy_session(self, session_id: str) -> bool:
        """Уничтожение сессии"""
        if session_id in self.sessions:
            user_id = self.sessions[session_id].get('user_id', 'unknown')
            del self.sessions[session_id]
            security_logger.info(f"Session destroyed for user {user_id}: {session_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Очистка истекших сессий"""
        expired_sessions = []
        current_time = datetime.utcnow()
        
        for session_id, session_data in self.sessions.items():
            if current_time - session_data['last_activity'] > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.destroy_session(session_id)
        
        if expired_sessions:
            security_logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

def auth_demo():
    """Демонстрация аутентификации и авторизации"""
    print("\n=== Authentication Demo ===")
    
    # JWT токены
    print("--- JWT Tokens ---")
    token_manager = TokenManager()
    
    user_id = "user123"
    permissions = ["read", "write", "admin"]
    
    # Создание токенов
    access_token = token_manager.create_access_token(user_id, permissions)
    refresh_token = token_manager.create_refresh_token(user_id)
    
    print(f"Access token создан: {access_token[:50]}...")
    print(f"Refresh token создан: {refresh_token[:50]}...")
    
    # Проверка токена
    user_data = token_manager.extract_user_from_token(access_token)
    print(f"Данные из токена: {user_data}")
    
    # Обновление токена
    new_access_token = token_manager.refresh_access_token(refresh_token)
    print(f"Новый access token: {new_access_token[:50]}...")
    
    # Сессии
    print("\n--- Sessions ---")
    session_manager = SessionManager()
    
    session_id = session_manager.create_session(user_id, {"role": "admin", "name": "John Doe"})
    print(f"Сессия создана: {session_id}")
    
    session_data = session_manager.get_session(session_id)
    print(f"Данные сессии: {session_data}")
    
    # Обновление сессии
    session_manager.update_session(session_id, {"last_login": datetime.utcnow().isoformat()})
    updated_session = session_manager.get_session(session_id)
    print(f"Обновленная сессия: {updated_session['user_data']}")
    
    return token_manager, session_manager

# =============================================================================
# Пример 4: Валидация входных данных и защита от атак
# =============================================================================

class InputValidator:
    """Валидатор входных данных"""
    
    def __init__(self):
        # Регулярные выражения для валидации
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.phone_pattern = re.compile(r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$')
        self.username_pattern = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
        
        # Черный список для SQL injection
        self.sql_blacklist = [
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
            'UNION', 'OR 1=1', 'OR 1 = 1', "'; DROP TABLE", '--', '/*', '*/',
            'EXEC', 'EXECUTE', 'xp_', 'sp_'
        ]
        
        # Черный список для XSS
        self.xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>.*?</iframe>',
            r'<object[^>]*>.*?</object>',
            r'<embed[^>]*>.*?</embed>'
        ]

    def validate_email(self, email: str) -> Dict[str, Any]:
        """Валидация email адреса"""
        if not email:
            return {'valid': False, 'error': 'Email is required'}
        
        if len(email) > 254:  # RFC 5321 limit
            return {'valid': False, 'error': 'Email too long'}
        
        if not self.email_pattern.match(email):
            return {'valid': False, 'error': 'Invalid email format'}
        
        return {'valid': True, 'email': email.lower()}

    def validate_password(self, password: str) -> Dict[str, Any]:
        """Валидация пароля"""
        if not password:
            return {'valid': False, 'error': 'Password is required'}
        
        if len(password) < 8:
            return {'valid': False, 'error': 'Password must be at least 8 characters'}
        
        if len(password) > 128:
            return {'valid': False, 'error': 'Password too long'}
        
        # Проверяем сложность
        has_lower = re.search(r'[a-z]', password)
        has_upper = re.search(r'[A-Z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        
        missing = []
        if not has_lower:
            missing.append('lowercase letter')
        if not has_upper:
            missing.append('uppercase letter')
        if not has_digit:
            missing.append('digit')
        if not has_special:
            missing.append('special character')
        
        if missing:
            return {'valid': False, 'error': f'Password must contain: {", ".join(missing)}'}
        
        return {'valid': True}

    def validate_username(self, username: str) -> Dict[str, Any]:
        """Валидация имени пользователя"""
        if not username:
            return {'valid': False, 'error': 'Username is required'}
        
        if not self.username_pattern.match(username):
            return {'valid': False, 'error': 'Username must be 3-20 characters, letters, numbers and underscore only'}
        
        # Проверяем на reserved names
        reserved = ['admin', 'root', 'system', 'user', 'test', 'guest']
        if username.lower() in reserved:
            return {'valid': False, 'error': 'Username is reserved'}
        
        return {'valid': True, 'username': username}

    def sanitize_sql_input(self, input_string: str) -> str:
        """Очистка входных данных от SQL injection"""
        if not input_string:
            return input_string
        
        # Удаляем потенциально опасные конструкции
        sanitized = input_string
        
        for dangerous in self.sql_blacklist:
            sanitized = re.sub(dangerous, '', sanitized, flags=re.IGNORECASE)
        
        # Экранируем специальные символы
        sanitized = sanitized.replace("'", "''")
        sanitized = sanitized.replace('"', '""')
        sanitized = sanitized.replace('\\', '\\\\')
        
        return sanitized

    def sanitize_html_input(self, input_string: str) -> str:
        """Очистка входных данных от XSS"""
        if not input_string:
            return input_string
        
        sanitized = input_string
        
        # Удаляем опасные HTML конструкции
        for pattern in self.xss_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        
        # Экранируем HTML символы
        html_escape_table = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;'
        }
        
        for char, escape in html_escape_table.items():
            sanitized = sanitized.replace(char, escape)
        
        return sanitized

    def validate_file_upload(self, filename: str, content: bytes, 
                           allowed_extensions: List[str] = None,
                           max_size: int = 10 * 1024 * 1024) -> Dict[str, Any]:
        """Валидация загружаемого файла"""
        if not filename:
            return {'valid': False, 'error': 'Filename is required'}
        
        # Проверка расширения
        if allowed_extensions:
            file_ext = filename.lower().split('.')[-1] if '.' in filename else ''
            if file_ext not in [ext.lower().lstrip('.') for ext in allowed_extensions]:
                return {'valid': False, 'error': f'File type not allowed. Allowed: {allowed_extensions}'}
        
        # Проверка размера
        if len(content) > max_size:
            return {'valid': False, 'error': f'File too large. Max size: {max_size} bytes'}
        
        # Проверка на опасные символы в имени файла
        dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in dangerous_chars:
            if char in filename:
                return {'valid': False, 'error': 'Filename contains dangerous characters'}
        
        # Проверка MIME типа по magic bytes
        mime_type = self._detect_mime_type(content)
        
        return {
            'valid': True,
            'filename': filename,
            'size': len(content),
            'mime_type': mime_type
        }

    def _detect_mime_type(self, content: bytes) -> str:
        """Определение MIME типа по magic bytes"""
        if not content:
            return 'unknown'
        
        # Простая проверка по первым байтам
        if content.startswith(b'\x89PNG'):
            return 'image/png'
        elif content.startswith(b'\xFF\xD8\xFF'):
            return 'image/jpeg'
        elif content.startswith(b'GIF8'):
            return 'image/gif'
        elif content.startswith(b'%PDF'):
            return 'application/pdf'
        elif content.startswith(b'PK'):
            return 'application/zip'
        
        return 'unknown'

    def rate_limit_check(self, user_id: str, action: str, 
                        max_attempts: int = 5, window_minutes: int = 15) -> Dict[str, Any]:
        """Проверка rate limiting"""
        # В реальном приложении это должно храниться в Redis или базе данных
        if not hasattr(self, '_rate_limits'):
            self._rate_limits = {}
        
        key = f"{user_id}:{action}"
        current_time = datetime.utcnow()
        window_start = current_time - timedelta(minutes=window_minutes)
        
        if key not in self._rate_limits:
            self._rate_limits[key] = []
        
        # Удаляем старые записи
        self._rate_limits[key] = [
            timestamp for timestamp in self._rate_limits[key] 
            if timestamp > window_start
        ]
        
        # Проверяем лимит
        if len(self._rate_limits[key]) >= max_attempts:
            return {
                'allowed': False,
                'remaining': 0,
                'reset_time': (self._rate_limits[key][0] + timedelta(minutes=window_minutes)).isoformat()
            }
        
        # Добавляем текущую попытку
        self._rate_limits[key].append(current_time)
        
        return {
            'allowed': True,
            'remaining': max_attempts - len(self._rate_limits[key]),
            'reset_time': (current_time + timedelta(minutes=window_minutes)).isoformat()
        }

def validation_demo():
    """Демонстрация валидации входных данных"""
    print("\n=== Input Validation Demo ===")
    
    validator = InputValidator()
    
    # Валидация email
    print("--- Email Validation ---")
    emails = ["user@example.com", "invalid-email", "very-long-email" + "x" * 250 + "@example.com"]
    for email in emails:
        result = validator.validate_email(email)
        print(f"{email}: {result}")
    
    # Валидация пароля
    print("\n--- Password Validation ---")
    passwords = ["weak", "StrongPass123!", ""]
    for password in passwords:
        result = validator.validate_password(password)
        print(f"'{password}': {result}")
    
    # SQL injection защита
    print("\n--- SQL Injection Protection ---")
    dangerous_input = "'; DROP TABLE users; --"
    sanitized = validator.sanitize_sql_input(dangerous_input)
    print(f"Original: {dangerous_input}")
    print(f"Sanitized: {sanitized}")
    
    # XSS защита
    print("\n--- XSS Protection ---")
    xss_input = "<script>alert('XSS')</script><h1>Hello</h1>"
    sanitized_html = validator.sanitize_html_input(xss_input)
    print(f"Original: {xss_input}")
    print(f"Sanitized: {sanitized_html}")
    
    # Rate limiting
    print("\n--- Rate Limiting ---")
    user_id = "user123"
    for i in range(7):
        result = validator.rate_limit_check(user_id, "login")
        print(f"Attempt {i+1}: {result}")
    
    return validator

# =============================================================================
# Пример 5: Secure Database Operations
# =============================================================================

class SecureDatabase:
    """Безопасная работа с базой данных"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = None
        self._setup_database()
    
    def _setup_database(self):
        """Настройка базы данных"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Для именованного доступа к колонкам
        
        # Создание таблиц
        cursor = self.connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.connection.commit()
    
    def create_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Безопасное создание пользователя"""
        # Валидация входных данных
        validator = InputValidator()
        
        username_validation = validator.validate_username(username)
        if not username_validation['valid']:
            return {'success': False, 'error': username_validation['error']}
        
        email_validation = validator.validate_email(email)
        if not email_validation['valid']:
            return {'success': False, 'error': email_validation['error']}
        
        password_validation = validator.validate_password(password)
        if not password_validation['valid']:
            return {'success': False, 'error': password_validation['error']}
        
        # Хеширование пароля
        ps = PasswordSecurity()
        password_hash = ps.hash_password_argon2(password)
        
        try:
            cursor = self.connection.cursor()
            
            # Использование параметризованных запросов для защиты от SQL injection
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            
            user_id = cursor.lastrowid
            self.connection.commit()
            
            security_logger.info(f"User created: {username} (ID: {user_id})")
            
            return {
                'success': True,
                'user_id': user_id,
                'username': username,
                'email': email
            }
            
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return {'success': False, 'error': 'Username already exists'}
            elif 'email' in str(e):
                return {'success': False, 'error': 'Email already exists'}
            else:
                return {'success': False, 'error': 'Database integrity error'}
        except Exception as e:
            security_logger.error(f"User creation failed: {e}")
            return {'success': False, 'error': 'Internal error'}
    
    def authenticate_user(self, username: str, password: str, ip_address: str = None) -> Dict[str, Any]:
        """Безопасная аутентификация пользователя"""
        try:
            cursor = self.connection.cursor()
            
            # Получение пользователя
            cursor.execute('''
                SELECT id, username, email, password_hash, is_active
                FROM users 
                WHERE username = ? AND is_active = TRUE
            ''', (username,))
            
            user = cursor.fetchone()
            
            if not user:
                self._log_login_attempt(username, ip_address, False)
                return {'success': False, 'error': 'Invalid credentials'}
            
            # Проверка пароля
            ps = PasswordSecurity()
            if ps.verify_password_argon2(password, user['password_hash']):
                self._log_login_attempt(username, ip_address, True)
                
                return {
                    'success': True,
                    'user_id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
            else:
                self._log_login_attempt(username, ip_address, False)
                return {'success': False, 'error': 'Invalid credentials'}
                
        except Exception as e:
            security_logger.error(f"Authentication failed: {e}")
            return {'success': False, 'error': 'Internal error'}
    
    def _log_login_attempt(self, username: str, ip_address: str, success: bool):
        """Логирование попыток входа"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO login_attempts (username, ip_address, success)
                VALUES (?, ?, ?)
            ''', (username, ip_address or 'unknown', success))
            self.connection.commit()
            
            if success:
                security_logger.info(f"Successful login: {username} from {ip_address}")
            else:
                security_logger.warning(f"Failed login attempt: {username} from {ip_address}")
                
        except Exception as e:
            security_logger.error(f"Failed to log login attempt: {e}")
    
    def get_user_login_history(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Получение истории входов пользователя"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT ip_address, success, attempt_time
                FROM login_attempts
                WHERE username = ?
                ORDER BY attempt_time DESC
                LIMIT ?
            ''', (username, limit))
            
            attempts = cursor.fetchall()
            
            return [
                {
                    'ip_address': attempt['ip_address'],
                    'success': bool(attempt['success']),
                    'attempt_time': attempt['attempt_time']
                }
                for attempt in attempts
            ]
            
        except Exception as e:
            security_logger.error(f"Failed to get login history: {e}")
            return []
    
    def get_security_report(self) -> Dict[str, Any]:
        """Получение отчета по безопасности"""
        try:
            cursor = self.connection.cursor()
            
            # Общее количество пользователей
            cursor.execute('SELECT COUNT(*) as total FROM users WHERE is_active = TRUE')
            total_users = cursor.fetchone()['total']
            
            # Неудачные попытки за последние 24 часа
            cursor.execute('''
                SELECT COUNT(*) as failed_attempts
                FROM login_attempts
                WHERE success = FALSE 
                AND attempt_time > datetime('now', '-24 hours')
            ''')
            failed_attempts_24h = cursor.fetchone()['failed_attempts']
            
            # Топ IP с неудачными попытками
            cursor.execute('''
                SELECT ip_address, COUNT(*) as attempts
                FROM login_attempts
                WHERE success = FALSE 
                AND attempt_time > datetime('now', '-24 hours')
                GROUP BY ip_address
                ORDER BY attempts DESC
                LIMIT 5
            ''')
            top_failed_ips = [
                {'ip': row['ip_address'], 'attempts': row['attempts']}
                for row in cursor.fetchall()
            ]
            
            # Последние успешные входы
            cursor.execute('''
                SELECT username, ip_address, attempt_time
                FROM login_attempts
                WHERE success = TRUE
                ORDER BY attempt_time DESC
                LIMIT 5
            ''')
            recent_logins = [
                {
                    'username': row['username'],
                    'ip_address': row['ip_address'],
                    'time': row['attempt_time']
                }
                for row in cursor.fetchall()
            ]
            
            return {
                'total_active_users': total_users,
                'failed_attempts_24h': failed_attempts_24h,
                'top_failed_ips': top_failed_ips,
                'recent_successful_logins': recent_logins,
                'report_generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            security_logger.error(f"Failed to generate security report: {e}")
            return {'error': 'Failed to generate report'}
    
    def close(self):
        """Закрытие соединения с базой данных"""
        if self.connection:
            self.connection.close()

def database_security_demo():
    """Демонстрация безопасной работы с базой данных"""
    print("\n=== Database Security Demo ===")
    
    db = SecureDatabase()
    
    # Создание пользователей
    print("--- User Creation ---")
    users = [
        ("alice", "alice@example.com", "SecurePass123!"),
        ("bob", "bob@example.com", "AnotherPass456@"),
        ("charlie", "charlie@example.com", "weak"),  # слабый пароль
        ("alice", "alice2@example.com", "DuplicateUser1!")  # дублирующийся username
    ]
    
    for username, email, password in users:
        result = db.create_user(username, email, password)
        print(f"Create user {username}: {result}")
    
    # Аутентификация
    print("\n--- Authentication ---")
    auth_attempts = [
        ("alice", "SecurePass123!", "192.168.1.100"),
        ("alice", "wrongpassword", "192.168.1.100"),
        ("bob", "AnotherPass456@", "10.0.0.5"),
        ("nonexistent", "password", "192.168.1.200")
    ]
    
    for username, password, ip in auth_attempts:
        result = db.authenticate_user(username, password, ip)
        print(f"Auth {username}: {result}")
    
    # История входов
    print("\n--- Login History ---")
    history = db.get_user_login_history("alice")
    print(f"Alice login history: {history}")
    
    # Отчет по безопасности
    print("\n--- Security Report ---")
    report = db.get_security_report()
    print(f"Security report: {json.dumps(report, indent=2, default=str)}")
    
    db.close()
    return db

# =============================================================================
# Главная функция для демонстрации всех примеров
# =============================================================================

def main():
    """Запуск всех примеров безопасности"""
    print("=== Безопасность в Python ===\n")
    
    # 1. Безопасность паролей
    password_security = password_security_demo()
    
    # 2. Криптография
    crypto_manager = cryptography_demo()
    
    # 3. Аутентификация и авторизация
    token_manager, session_manager = auth_demo()
    
    # 4. Валидация входных данных
    validator = validation_demo()
    
    # 5. Безопасная работа с базой данных
    secure_db = database_security_demo()
    
    print("\n=== Сводка ===")
    print("✅ Безопасное хеширование паролей (bcrypt, Argon2, PBKDF2)")
    print("✅ Симметричное и асимметричное шифрование")
    print("✅ Цифровые подписи и проверка целостности")
    print("✅ JWT токены и управление сессиями")
    print("✅ Валидация входных данных и защита от атак")
    print("✅ Безопасная работа с базой данных")
    print("✅ Логирование событий безопасности")
    print("✅ Rate limiting и мониторинг")
    
    print("\nВсе примеры демонстрируют современные практики безопасности! 🔒🛡️")

if __name__ == "__main__":
    main() 