# Основы работы с SQLite в Python
import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

# Создание и подключение к базе данных
def create_connection():
    """Создание подключения к базе данных"""
    print("=== Создание подключения к SQLite ===")
    
    # Подключение к файлу базы данных
    conn = sqlite3.connect('example.db')
    print("Подключение к example.db создано")
    
    # Включение поддержки Row factory для удобного доступа к столбцам
    conn.row_factory = sqlite3.Row
    
    return conn

def create_tables(conn):
    """Создание таблиц"""
    print("\n=== Создание таблиц ===")
    
    cursor = conn.cursor()
    
    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Создание таблицы постов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Создание таблицы комментариев
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Создание индексов для оптимизации
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts (user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments (post_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)')
    
    conn.commit()
    print("Таблицы и индексы созданы")

def insert_sample_data(conn):
    """Вставка примерных данных"""
    print("\n=== Вставка данных ===")
    
    cursor = conn.cursor()
    
    # Вставка пользователей
    users_data = [
        ('alice', 'alice@example.com', 'hash1'),
        ('bob', 'bob@example.com', 'hash2'),
        ('charlie', 'charlie@example.com', 'hash3')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        users_data
    )
    
    # Получение ID пользователей
    cursor.execute('SELECT id, username FROM users')
    users = {row['username']: row['id'] for row in cursor.fetchall()}
    
    # Вставка постов
    posts_data = [
        ('Первый пост Алисы', 'Содержимое первого поста', users['alice']),
        ('Второй пост Алисы', 'Содержимое второго поста', users['alice']),
        ('Пост Боба', 'Мысли Боба о программировании', users['bob']),
        ('Пост Чарли', 'Интересные факты', users['charlie'])
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO posts (title, content, user_id) VALUES (?, ?, ?)',
        posts_data
    )
    
    # Получение ID постов
    cursor.execute('SELECT id, title FROM posts')
    posts = {row['title']: row['id'] for row in cursor.fetchall()}
    
    # Вставка комментариев
    comments_data = [
        ('Отличный пост!', posts['Первый пост Алисы'], users['bob']),
        ('Согласен с автором', posts['Первый пост Алисы'], users['charlie']),
        ('Интересная точка зрения', posts['Пост Боба'], users['alice']),
        ('Спасибо за информацию', posts['Пост Чарли'], users['alice'])
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO comments (content, post_id, user_id) VALUES (?, ?, ?)',
        comments_data
    )
    
    conn.commit()
    print(f"Добавлено {len(users_data)} пользователей, {len(posts_data)} постов, {len(comments_data)} комментариев")

def query_examples(conn):
    """Примеры различных запросов"""
    print("\n=== Примеры запросов ===")
    
    cursor = conn.cursor()
    
    # 1. Простой SELECT
    print("1. Все пользователи:")
    cursor.execute('SELECT * FROM users')
    for row in cursor.fetchall():
        print(f"   {row['id']}: {row['username']} ({row['email']})")
    
    # 2. SELECT с условием
    print("\n2. Активные пользователи:")
    cursor.execute('SELECT username, email FROM users WHERE is_active = 1')
    for row in cursor.fetchall():
        print(f"   {row['username']}: {row['email']}")
    
    # 3. JOIN запрос
    print("\n3. Посты с именами авторов:")
    cursor.execute('''
        SELECT p.title, p.content, u.username, p.created_at
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    ''')
    for row in cursor.fetchall():
        print(f"   '{row['title']}' by {row['username']} at {row['created_at']}")
    
    # 4. Агрегация
    print("\n4. Количество постов по пользователям:")
    cursor.execute('''
        SELECT u.username, COUNT(p.id) as post_count
        FROM users u
        LEFT JOIN posts p ON u.id = p.user_id
        GROUP BY u.id, u.username
        ORDER BY post_count DESC
    ''')
    for row in cursor.fetchall():
        print(f"   {row['username']}: {row['post_count']} постов")
    
    # 5. Сложный запрос с подзапросом
    print("\n5. Пользователи с комментариями:")
    cursor.execute('''
        SELECT DISTINCT u.username, u.email
        FROM users u
        WHERE u.id IN (
            SELECT DISTINCT user_id FROM comments
        )
    ''')
    for row in cursor.fetchall():
        print(f"   {row['username']}: {row['email']}")

def update_and_delete_examples(conn):
    """Примеры UPDATE и DELETE"""
    print("\n=== UPDATE и DELETE операции ===")
    
    cursor = conn.cursor()
    
    # UPDATE
    print("1. Обновление email пользователя:")
    cursor.execute(
        'UPDATE users SET email = ? WHERE username = ?',
        ('alice.new@example.com', 'alice')
    )
    print(f"   Обновлено строк: {cursor.rowcount}")
    
    # Проверяем обновление
    cursor.execute('SELECT username, email FROM users WHERE username = ?', ('alice',))
    row = cursor.fetchone()
    if row:
        print(f"   Новый email Alice: {row['email']}")
    
    # UPDATE с условием
    print("\n2. Обновление времени изменения постов:")
    cursor.execute(
        'UPDATE posts SET updated_at = CURRENT_TIMESTAMP WHERE user_id = (SELECT id FROM users WHERE username = ?)',
        ('alice',)
    )
    print(f"   Обновлено постов: {cursor.rowcount}")
    
    # DELETE (осторожно!)
    print("\n3. Удаление комментария:")
    cursor.execute('DELETE FROM comments WHERE id = (SELECT MAX(id) FROM comments)')
    print(f"   Удалено комментариев: {cursor.rowcount}")
    
    conn.commit()

def prepared_statements_examples(conn):
    """Примеры подготовленных запросов (защита от SQL инъекций)"""
    print("\n=== Подготовленные запросы ===")
    
    cursor = conn.cursor()
    
    # Безопасный способ
    username = "alice"
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        print(f"Найден пользователь: {user['username']}")
    
    # Пример потенциально опасного кода (НЕ ДЕЛАЙТЕ ТАК!)
    print("\nПример опасного кода (закомментирован):")
    print("# cursor.execute(f\"SELECT * FROM users WHERE username = '{username}'\")")
    print("Используйте параметризованные запросы!")
    
    # Массовая вставка с executemany
    print("\nМассовая вставка тестовых данных:")
    test_users = [
        (f'user{i}', f'user{i}@test.com', f'hash{i}') 
        for i in range(1, 4)
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        test_users
    )
    print(f"Добавлено пользователей: {cursor.rowcount}")
    conn.commit()

def transaction_examples(conn):
    """Примеры работы с транзакциями"""
    print("\n=== Транзакции ===")
    
    cursor = conn.cursor()
    
    try:
        # Начинаем транзакцию
        conn.execute('BEGIN')
        
        # Создаем нового пользователя
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            ('transaction_user', 'trans@example.com', 'hash_trans')
        )
        user_id = cursor.lastrowid
        
        # Создаем пост для этого пользователя
        cursor.execute(
            'INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)',
            ('Транзакционный пост', 'Содержимое поста', user_id)
        )
        
        # Если все ОК - фиксируем изменения
        conn.commit()
        print("Транзакция успешно завершена")
        
    except Exception as e:
        # Если ошибка - откатываем изменения
        conn.rollback()
        print(f"Ошибка в транзакции: {e}")
        print("Изменения отменены")

def database_info(conn):
    """Информация о базе данных"""
    print("\n=== Информация о базе данных ===")
    
    cursor = conn.cursor()
    
    # Список таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Таблицы в базе: {tables}")
    
    # Информация о таблице users
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    print("\nСтруктура таблицы users:")
    for col in columns:
        print(f"   {col[1]} {col[2]} {'PRIMARY KEY' if col[5] else ''}")
    
    # Размер базы данных
    cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
    size = cursor.fetchone()[0]
    print(f"\nРазмер базы данных: {size} байт")

@contextmanager
def database_connection(db_path):
    """Контекстный менеджер для работы с базой данных"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def backup_database(source_db, backup_db):
    """Резервное копирование базы данных"""
    print(f"\n=== Резервное копирование ===")
    
    with database_connection(source_db) as source_conn:
        with database_connection(backup_db) as backup_conn:
            source_conn.backup(backup_conn)
    
    print(f"База данных скопирована: {source_db} -> {backup_db}")

def cleanup():
    """Очистка (удаление файлов БД)"""
    files_to_remove = ['example.db', 'backup.db']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"Удален файл: {file}")

# Демонстрация всех возможностей
if __name__ == "__main__":
    try:
        print("Демонстрация работы с SQLite в Python")
        print("=" * 50)
        
        # Основная работа с базой данных
        conn = create_connection()
        
        create_tables(conn)
        insert_sample_data(conn)
        query_examples(conn)
        update_and_delete_examples(conn)
        prepared_statements_examples(conn)
        transaction_examples(conn)
        database_info(conn)
        
        conn.close()
        
        # Резервное копирование
        backup_database('example.db', 'backup.db')
        
        # Использование контекстного менеджера
        print("\n=== Использование контекстного менеджера ===")
        with database_connection('example.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM users')
            count = cursor.fetchone()['count']
            print(f"Общее количество пользователей: {count}")
        
        print("\n=== Лучшие практики ===")
        best_practices = [
            "1. Всегда используйте параметризованные запросы",
            "2. Закрывайте соединения или используйте контекстные менеджеры",
            "3. Обрабатывайте исключения",
            "4. Используйте транзакции для связанных операций",
            "5. Создавайте индексы для часто запрашиваемых полей",
            "6. Регулярно делайте резервные копии",
            "7. Используйте FOREIGN KEY для целостности данных",
            "8. Ограничивайте размер результатов с LIMIT"
        ]
        
        for practice in best_practices:
            print(f"   {practice}")
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    finally:
        # Очистка (раскомментируйте для удаления файлов)
        # cleanup()
        print(f"\nФайлы базы данных сохранены для изучения")
        print("Для очистки запустите функцию cleanup()") 