# Безопасность паролей и хеширование
import hashlib
import secrets
import time
import re
from typing import Optional

# Попытка импортировать bcrypt
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    print("bcrypt не установлен. Установите: pip install bcrypt")
    BCRYPT_AVAILABLE = False

def demonstrate_weak_hashing():
    """Демонстрация слабых методов хеширования (НЕ ИСПОЛЬЗУЙТЕ!)"""
    print("=== Слабые методы хеширования (НЕ ИСПОЛЬЗУЙТЕ!) ===")
    
    password = "mypassword123"
    
    # MD5 - крайне небезопасен
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    print(f"MD5: {md5_hash}")
    
    # SHA1 - также небезопасен
    sha1_hash = hashlib.sha1(password.encode()).hexdigest()
    print(f"SHA1: {sha1_hash}")
    
    # Даже SHA256 без соли - плохая практика
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"SHA256 без соли: {sha256_hash}")
    
    print("\nПроблемы этих методов:")
    problems = [
        "1. Радужные таблицы (rainbow tables)",
        "2. Быстрые вычисления - возможность брутфорса",
        "3. Одинаковые пароли дают одинаковые хеши",
        "4. Отсутствие защиты от timing атак"
    ]
    for problem in problems:
        print(f"   {problem}")

def demonstrate_salt_importance():
    """Демонстрация важности соли"""
    print("\n=== Важность соли (salt) ===")
    
    password = "password123"
    
    # Хеширование без соли
    hash_without_salt = hashlib.sha256(password.encode()).hexdigest()
    print(f"Без соли: {hash_without_salt}")
    
    # Хеширование с солью
    salt1 = secrets.token_bytes(32)
    salt2 = secrets.token_bytes(32)
    
    hash_with_salt1 = hashlib.sha256(salt1 + password.encode()).hexdigest()
    hash_with_salt2 = hashlib.sha256(salt2 + password.encode()).hexdigest()
    
    print(f"С солью 1: {hash_with_salt1}")
    print(f"С солью 2: {hash_with_salt2}")
    
    print("\nПреимущества соли:")
    advantages = [
        "1. Разные хеши для одинаковых паролей",
        "2. Защита от радужных таблиц",
        "3. Усложнение атак по словарю",
        "4. Уникальность каждого хеша"
    ]
    for advantage in advantages:
        print(f"   {advantage}")

def demonstrate_secure_random():
    """Демонстрация безопасной генерации случайных чисел"""
    print("\n=== Безопасная генерация случайных чисел ===")
    
    # НЕ ИСПОЛЬЗУЙТЕ random для безопасности!
    import random
    weak_random = random.randint(1000, 9999)
    print(f"Небезопасный random (НЕ для паролей!): {weak_random}")
    
    # Используйте secrets для криптографически стойких чисел
    secure_random = secrets.randbelow(10000)
    print(f"Безопасный secrets: {secure_random}")
    
    # Генерация случайной соли
    salt = secrets.token_bytes(32)
    print(f"Случайная соль (32 байта): {salt.hex()}")
    
    # Генерация случайного токена
    token = secrets.token_urlsafe(32)
    print(f"URL-безопасный токен: {token}")
    
    # Сравнение времени генерации
    start = time.time()
    for _ in range(1000):
        secrets.token_bytes(32)
    secure_time = time.time() - start
    
    start = time.time()
    for _ in range(1000):
        random.randbytes(32)
    weak_time = time.time() - start
    
    print(f"\nВремя генерации 1000 токенов:")
    print(f"secrets: {secure_time:.4f} сек")
    print(f"random: {weak_time:.4f} сек")

class PasswordHasher:
    """Класс для безопасного хеширования паролей"""
    
    def __init__(self):
        if not BCRYPT_AVAILABLE:
            print("Внимание: bcrypt недоступен, используется резервный метод")
    
    def hash_password_bcrypt(self, password: str) -> str:
        """Хеширование пароля с bcrypt"""
        if not BCRYPT_AVAILABLE:
            return self._fallback_hash(password)
        
        # Генерируем соль и хешируем пароль
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password_bcrypt(self, password: str, hashed: str) -> bool:
        """Проверка пароля с bcrypt"""
        if not BCRYPT_AVAILABLE:
            return self._fallback_verify(password, hashed)
        
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def _fallback_hash(self, password: str) -> str:
        """Резервный метод хеширования (PBKDF2)"""
        import hashlib
        
        salt = secrets.token_bytes(32)
        # PBKDF2 с множественными итерациями
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        
        # Объединяем соль и ключ для хранения
        return salt.hex() + ':' + key.hex()
    
    def _fallback_verify(self, password: str, stored_hash: str) -> bool:
        """Резервная проверка пароля"""
        import hashlib
        
        try:
            salt_hex, key_hex = stored_hash.split(':')
            salt = bytes.fromhex(salt_hex)
            stored_key = bytes.fromhex(key_hex)
            
            # Вычисляем ключ для введённого пароля
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            
            # Сравниваем ключи безопасным способом
            return secrets.compare_digest(key, stored_key)
        except ValueError:
            return False

def demonstrate_password_hashing():
    """Демонстрация хеширования паролей"""
    print("\n=== Безопасное хеширование паролей ===")
    
    hasher = PasswordHasher()
    
    # Тестовые пароли
    passwords = ["password123", "MyStr0ngP@ssw0rd!", "простой_пароль"]
    
    for password in passwords:
        print(f"\nПароль: {password}")
        
        # Хешируем пароль
        start_time = time.time()
        hashed = hasher.hash_password_bcrypt(password)
        hash_time = time.time() - start_time
        
        print(f"Хеш: {hashed}")
        print(f"Время хеширования: {hash_time:.4f} сек")
        
        # Проверяем правильный пароль
        start_time = time.time()
        is_valid = hasher.verify_password_bcrypt(password, hashed)
        verify_time = time.time() - start_time
        
        print(f"Проверка правильного пароля: {is_valid}")
        print(f"Время проверки: {verify_time:.4f} сек")
        
        # Проверяем неправильный пароль
        is_invalid = hasher.verify_password_bcrypt("wrong_password", hashed)
        print(f"Проверка неправильного пароля: {is_invalid}")

def password_strength_checker(password: str) -> dict:
    """Проверка силы пароля"""
    result = {
        'score': 0,
        'feedback': [],
        'strength': 'Очень слабый'
    }
    
    # Длина пароля
    if len(password) >= 8:
        result['score'] += 1
    else:
        result['feedback'].append("Пароль должен быть не менее 8 символов")
    
    if len(password) >= 12:
        result['score'] += 1
    
    # Содержание различных типов символов
    if re.search(r'[a-z]', password):
        result['score'] += 1
    else:
        result['feedback'].append("Добавьте строчные буквы")
    
    if re.search(r'[A-Z]', password):
        result['score'] += 1
    else:
        result['feedback'].append("Добавьте заглавные буквы")
    
    if re.search(r'\d', password):
        result['score'] += 1
    else:
        result['feedback'].append("Добавьте цифры")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        result['score'] += 1
    else:
        result['feedback'].append("Добавьте специальные символы")
    
    # Проверка на общие слабости
    common_patterns = [
        r'123', r'abc', r'qwerty', r'password', r'admin',
        r'(\w)\1{2,}',  # Повторяющиеся символы
    ]
    
    for pattern in common_patterns:
        if re.search(pattern, password.lower()):
            result['score'] -= 1
            result['feedback'].append(f"Избегайте простых паттернов")
            break
    
    # Определение силы пароля
    if result['score'] <= 2:
        result['strength'] = 'Очень слабый'
    elif result['score'] <= 3:
        result['strength'] = 'Слабый'
    elif result['score'] <= 4:
        result['strength'] = 'Средний'
    elif result['score'] <= 5:
        result['strength'] = 'Сильный'
    else:
        result['strength'] = 'Очень сильный'
    
    return result

def demonstrate_password_strength():
    """Демонстрация проверки силы пароля"""
    print("\n=== Проверка силы пароля ===")
    
    test_passwords = [
        "123456",
        "password",
        "Password123",
        "MyStr0ng!P@ssw0rd",
        "Очень_Сложный_Пароль_2023!"
    ]
    
    for password in test_passwords:
        result = password_strength_checker(password)
        print(f"\nПароль: {password}")
        print(f"Сила: {result['strength']} (очки: {result['score']})")
        
        if result['feedback']:
            print("Рекомендации:")
            for feedback in result['feedback']:
                print(f"  - {feedback}")

def demonstrate_timing_attacks():
    """Демонстрация защиты от timing атак"""
    print("\n=== Защита от timing атак ===")
    
    def unsafe_compare(a: str, b: str) -> bool:
        """Небезопасное сравнение (уязвимо к timing атакам)"""
        if len(a) != len(b):
            return False
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
        return True
    
    def safe_compare(a: str, b: str) -> bool:
        """Безопасное сравнение"""
        return secrets.compare_digest(a, b)
    
    # Тестовые данные
    correct_token = "secret_token_12345"
    wrong_tokens = [
        "secret_token_54321",  # Отличается в конце
        "wrong_token_12345",   # Отличается в начале
        "completely_different"  # Совсем другой
    ]
    
    print("Сравнение времени выполнения:")
    
    for token in wrong_tokens:
        # Небезопасное сравнение
        start = time.perf_counter()
        for _ in range(10000):
            unsafe_compare(correct_token, token)
        unsafe_time = time.perf_counter() - start
        
        # Безопасное сравнение
        start = time.perf_counter()
        for _ in range(10000):
            safe_compare(correct_token, token)
        safe_time = time.perf_counter() - start
        
        print(f"\nТокен: {token[:15]}...")
        print(f"Небезопасное: {unsafe_time:.6f} сек")
        print(f"Безопасное: {safe_time:.6f} сек")

def generate_secure_password(length: int = 16) -> str:
    """Генерация безопасного пароля"""
    import string
    
    # Различные наборы символов
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Гарантируем хотя бы один символ каждого типа
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(special)
    ]
    
    # Заполняем остальные позиции
    all_chars = lowercase + uppercase + digits + special
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))
    
    # Перемешиваем символы
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def demonstrate_password_generation():
    """Демонстрация генерации безопасных паролей"""
    print("\n=== Генерация безопасных паролей ===")
    
    lengths = [8, 12, 16, 24]
    
    for length in lengths:
        password = generate_secure_password(length)
        strength = password_strength_checker(password)
        
        print(f"\nДлина {length}: {password}")
        print(f"Сила: {strength['strength']}")

if __name__ == "__main__":
    print("Безопасность паролей в Python")
    print("=" * 50)
    
    demonstrate_weak_hashing()
    demonstrate_salt_importance()
    demonstrate_secure_random()
    demonstrate_password_hashing()
    demonstrate_password_strength()
    demonstrate_timing_attacks()
    demonstrate_password_generation()
    
    print("\n=== Лучшие практики безопасности паролей ===")
    best_practices = [
        "1. Используйте bcrypt, scrypt или Argon2 для хеширования",
        "2. Всегда используйте соль (salt)",
        "3. Используйте secrets для генерации случайных данных",
        "4. Применяйте secrets.compare_digest() для сравнения",
        "5. Настройте достаточную стоимость (cost) для bcrypt",
        "6. Регулярно обновляйте алгоритмы хеширования",
        "7. Никогда не храните пароли в открытом виде",
        "8. Реализуйте политику сильных паролей",
        "9. Ограничивайте количество попыток входа",
        "10. Используйте двухфакторную аутентификацию"
    ]
    
    for practice in best_practices:
        print(f"   {practice}")
    
    print("\n=== Что НЕ делать ===")
    dont_do = [
        "❌ Не используйте MD5 или SHA1 для паролей",
        "❌ Не храните пароли в открытом виде",
        "❌ Не используйте простое SHA256 без соли",
        "❌ Не используйте random для криптографических задач",
        "❌ Не сравнивайте хеши простым ==",
        "❌ Не делайте слишком быстрое хеширование",
        "❌ Не логируйте пароли",
        "❌ Не отправляйте пароли по незащищённым каналам"
    ]
    
    for dont in dont_do:
        print(f"   {dont}") 