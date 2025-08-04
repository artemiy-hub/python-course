# Теория: Работа с базами данных в Python

## 🎯 Цель раздела

Этот раздел охватывает все аспекты работы с базами данных в Python: от простых SQLite операций до сложных ORM систем, от реляционных до NoSQL баз данных.

## 📋 Содержание

1. [SQLite - встроенная БД](#sqlite---встроенная-бд)
2. [SQL основы и лучшие практики](#sql-основы-и-лучшие-практики)
3. [SQLAlchemy ORM](#sqlalchemy-orm)
4. [Миграции и схемы](#миграции-и-схемы)
5. [PostgreSQL и MySQL](#postgresql-и-mysql)
6. [NoSQL базы данных](#nosql-базы-данных)
7. [Производительность и оптимизация](#производительность-и-оптимизация)

---

## 💾 SQLite - встроенная БД

SQLite - легкая встроенная база данных, идеальная для прототипирования и небольших приложений.

### Основы работы с SQLite

```python
import sqlite3
from typing import List, Dict, Any, Optional, Union
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
import json

class DatabaseManager:
    """Менеджер для работы с SQLite"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для подключения"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Для удобного доступа к колонкам
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()
    
    def init_database(self):
        """Инициализация базы данных"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Создание таблицы пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Создание таблицы постов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    category_id INTEGER,
                    is_published BOOLEAN DEFAULT 0,
                    views_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)
            
            # Создание таблицы категорий
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    parent_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES categories (id)
                )
            """)
            
            # Создание таблицы тегов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    color TEXT DEFAULT '#007bff'
                )
            """)
            
            # Связующая таблица для постов и тегов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS post_tags (
                    post_id INTEGER,
                    tag_id INTEGER,
                    PRIMARY KEY (post_id, tag_id),
                    FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
                )
            """)
            
            # Создание индексов для производительности
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_author ON posts (author_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_category ON posts (category_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_published ON posts (is_published)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Выполнение SELECT запроса"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Выполнение INSERT/UPDATE/DELETE запроса"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Выполнение INSERT запроса с возвратом ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid

# Модели данных
@dataclass
class User:
    """Модель пользователя"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'User':
        """Создание объекта из строки БД"""
        return cls(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            full_name=row['full_name'],
            is_active=bool(row['is_active']),
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )

@dataclass
class Post:
    """Модель поста"""
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    author_id: int = 0
    category_id: Optional[int] = None
    is_published: bool = False
    views_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Post':
        """Создание объекта из строки БД"""
        return cls(
            id=row['id'],
            title=row['title'],
            content=row['content'],
            author_id=row['author_id'],
            category_id=row['category_id'],
            is_published=bool(row['is_published']),
            views_count=row['views_count'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )

# Repository паттерн
class UserRepository:
    """Репозиторий для работы с пользователями"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def create(self, user: User) -> User:
        """Создание пользователя"""
        query = """
            INSERT INTO users (username, email, password_hash, full_name, is_active)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (user.username, user.email, user.password_hash, user.full_name, user.is_active)
        
        user_id = self.db.execute_insert(query, params)
        user.id = user_id
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        query = "SELECT * FROM users WHERE id = ?"
        rows = self.db.execute_query(query, (user_id,))
        
        if rows:
            return User.from_row(rows[0])
        return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        query = "SELECT * FROM users WHERE email = ?"
        rows = self.db.execute_query(query, (email,))
        
        if rows:
            return User.from_row(rows[0])
        return None
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Получение всех пользователей"""
        query = "SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?"
        rows = self.db.execute_query(query, (limit, offset))
        
        return [User.from_row(row) for row in rows]
    
    def update(self, user: User) -> bool:
        """Обновление пользователя"""
        query = """
            UPDATE users 
            SET username = ?, email = ?, full_name = ?, is_active = ?, 
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = (user.username, user.email, user.full_name, user.is_active, user.id)
        
        rows_affected = self.db.execute_update(query, params)
        return rows_affected > 0
    
    def delete(self, user_id: int) -> bool:
        """Удаление пользователя"""
        query = "DELETE FROM users WHERE id = ?"
        rows_affected = self.db.execute_update(query, (user_id,))
        return rows_affected > 0
    
    def search(self, search_term: str) -> List[User]:
        """Поиск пользователей"""
        query = """
            SELECT * FROM users 
            WHERE username LIKE ? OR email LIKE ? OR full_name LIKE ?
            ORDER BY username
        """
        search_pattern = f"%{search_term}%"
        rows = self.db.execute_query(query, (search_pattern, search_pattern, search_pattern))
        
        return [User.from_row(row) for row in rows]

class PostRepository:
    """Репозиторий для работы с постами"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def create(self, post: Post) -> Post:
        """Создание поста"""
        query = """
            INSERT INTO posts (title, content, author_id, category_id, is_published)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (post.title, post.content, post.author_id, post.category_id, post.is_published)
        
        post_id = self.db.execute_insert(query, params)
        post.id = post_id
        return post
    
    def get_by_id(self, post_id: int) -> Optional[Post]:
        """Получение поста по ID"""
        query = "SELECT * FROM posts WHERE id = ?"
        rows = self.db.execute_query(query, (post_id,))
        
        if rows:
            return Post.from_row(rows[0])
        return None
    
    def get_by_author(self, author_id: int) -> List[Post]:
        """Получение постов автора"""
        query = "SELECT * FROM posts WHERE author_id = ? ORDER BY created_at DESC"
        rows = self.db.execute_query(query, (author_id,))
        
        return [Post.from_row(row) for row in rows]
    
    def get_published(self, limit: int = 50, offset: int = 0) -> List[Post]:
        """Получение опубликованных постов"""
        query = """
            SELECT * FROM posts 
            WHERE is_published = 1 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        """
        rows = self.db.execute_query(query, (limit, offset))
        
        return [Post.from_row(row) for row in rows]
    
    def update(self, post: Post) -> bool:
        """Обновление поста"""
        query = """
            UPDATE posts 
            SET title = ?, content = ?, category_id = ?, is_published = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = (post.title, post.content, post.category_id, post.is_published, post.id)
        
        rows_affected = self.db.execute_update(query, params)
        return rows_affected > 0
    
    def increment_views(self, post_id: int) -> bool:
        """Увеличение счетчика просмотров"""
        query = "UPDATE posts SET views_count = views_count + 1 WHERE id = ?"
        rows_affected = self.db.execute_update(query, (post_id,))
        return rows_affected > 0
    
    def delete(self, post_id: int) -> bool:
        """Удаление поста"""
        query = "DELETE FROM posts WHERE id = ?"
        rows_affected = self.db.execute_update(query, (post_id,))
        return rows_affected > 0
    
    def get_with_author_info(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Получение постов с информацией об авторах"""
        query = """
            SELECT p.*, u.username, u.full_name
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE p.is_published = 1
            ORDER BY p.created_at DESC
            LIMIT ?
        """
        rows = self.db.execute_query(query, (limit,))
        
        result = []
        for row in rows:
            post_data = {
                'post': Post.from_row(row),
                'author_username': row['username'],
                'author_full_name': row['full_name']
            }
            result.append(post_data)
        
        return result

# Сервисный слой
class BlogService:
    """Сервис для работы с блогом"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.user_repo = UserRepository(db)
        self.post_repo = PostRepository(db)
    
    def register_user(self, username: str, email: str, password: str, full_name: str = None) -> User:
        """Регистрация пользователя"""
        # Проверяем уникальность email
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")
        
        # Хешируем пароль (в реальности используйте bcrypt)
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )
        
        return self.user_repo.create(user)
    
    def create_post(self, title: str, content: str, author_id: int, 
                   category_id: int = None, publish: bool = False) -> Post:
        """Создание поста"""
        # Проверяем существование автора
        author = self.user_repo.get_by_id(author_id)
        if not author:
            raise ValueError("Автор не найден")
        
        post = Post(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category_id,
            is_published=publish
        )
        
        return self.post_repo.create(post)
    
    def get_user_dashboard(self, user_id: int) -> Dict[str, Any]:
        """Получение данных для панели пользователя"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        
        user_posts = self.post_repo.get_by_author(user_id)
        published_posts = [p for p in user_posts if p.is_published]
        draft_posts = [p for p in user_posts if not p.is_published]
        
        total_views = sum(p.views_count for p in published_posts)
        
        return {
            'user': user,
            'total_posts': len(user_posts),
            'published_posts': len(published_posts),
            'draft_posts': len(draft_posts),
            'total_views': total_views,
            'recent_posts': user_posts[:5]
        }
    
    def get_blog_stats(self) -> Dict[str, Any]:
        """Получение статистики блога"""
        # Общее количество пользователей
        all_users = self.user_repo.get_all()
        active_users = [u for u in all_users if u.is_active]
        
        # Статистика по постам
        posts_query = "SELECT COUNT(*) as total, SUM(views_count) as total_views FROM posts"
        published_query = "SELECT COUNT(*) as published FROM posts WHERE is_published = 1"
        
        total_stats = self.db.execute_query(posts_query)[0]
        published_stats = self.db.execute_query(published_query)[0]
        
        return {
            'total_users': len(all_users),
            'active_users': len(active_users),
            'total_posts': total_stats['total'],
            'published_posts': published_stats['published'],
            'draft_posts': total_stats['total'] - published_stats['published'],
            'total_views': total_stats['total_views'] or 0
        }
```

### Транзакции и безопасность

```python
class TransactionalService:
    """Сервис с поддержкой транзакций"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def transfer_post_ownership(self, post_id: int, new_author_id: int, old_author_id: int) -> bool:
        """Перенос права собственности на пост (транзакционно)"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Проверяем существование поста и старого автора
                cursor.execute("SELECT author_id FROM posts WHERE id = ?", (post_id,))
                post_row = cursor.fetchone()
                
                if not post_row or post_row['author_id'] != old_author_id:
                    raise ValueError("Пост не найден или принадлежит другому автору")
                
                # Проверяем существование нового автора
                cursor.execute("SELECT id FROM users WHERE id = ?", (new_author_id,))
                if not cursor.fetchone():
                    raise ValueError("Новый автор не найден")
                
                # Обновляем автора поста
                cursor.execute(
                    "UPDATE posts SET author_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (new_author_id, post_id)
                )
                
                # Логируем операцию
                cursor.execute(
                    "INSERT INTO activity_log (action, post_id, old_author_id, new_author_id, timestamp) VALUES (?, ?, ?, ?, ?)",
                    ("transfer_ownership", post_id, old_author_id, new_author_id, datetime.now().isoformat())
                )
                
                return True
                
            except Exception as e:
                # Транзакция автоматически откатится при выходе из контекста
                raise e
    
    def bulk_update_posts(self, post_updates: List[Dict[str, Any]]) -> int:
        """Массовое обновление постов"""
        updated_count = 0
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            for update in post_updates:
                post_id = update.get('id')
                title = update.get('title')
                content = update.get('content')
                is_published = update.get('is_published')
                
                if not post_id:
                    continue
                
                cursor.execute(
                    """UPDATE posts 
                       SET title = COALESCE(?, title),
                           content = COALESCE(?, content),
                           is_published = COALESCE(?, is_published),
                           updated_at = CURRENT_TIMESTAMP
                       WHERE id = ?""",
                    (title, content, is_published, post_id)
                )
                
                if cursor.rowcount > 0:
                    updated_count += 1
        
        return updated_count

# SQL Injection защита
class SecureQueries:
    """Примеры безопасных запросов"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def safe_search(self, search_term: str, table: str, columns: List[str]) -> List[sqlite3.Row]:
        """Безопасный поиск с защитой от SQL injection"""
        
        # Валидация имени таблицы (whitelist)
        allowed_tables = {'users', 'posts', 'categories', 'tags'}
        if table not in allowed_tables:
            raise ValueError(f"Недопустимая таблица: {table}")
        
        # Валидация колонок (whitelist)
        allowed_columns = {
            'users': {'username', 'email', 'full_name'},
            'posts': {'title', 'content'},
            'categories': {'name', 'description'},
            'tags': {'name'}
        }
        
        table_columns = allowed_columns.get(table, set())
        valid_columns = [col for col in columns if col in table_columns]
        
        if not valid_columns:
            raise ValueError("Нет допустимых колонок для поиска")
        
        # Построение безопасного запроса
        where_clauses = []
        params = []
        
        for column in valid_columns:
            where_clauses.append(f"{column} LIKE ?")
            params.append(f"%{search_term}%")
        
        query = f"SELECT * FROM {table} WHERE {' OR '.join(where_clauses)}"
        
        return self.db.execute_query(query, tuple(params))
    
    def parameterized_filter(self, filters: Dict[str, Any]) -> List[sqlite3.Row]:
        """Безопасная фильтрация с параметризованными запросами"""
        
        where_clauses = []
        params = []
        
        # Безопасная обработка фильтров
        safe_filters = {
            'author_id': 'author_id = ?',
            'is_published': 'is_published = ?',
            'category_id': 'category_id = ?',
            'min_views': 'views_count >= ?',
            'max_views': 'views_count <= ?'
        }
        
        for key, value in filters.items():
            if key in safe_filters and value is not None:
                where_clauses.append(safe_filters[key])
                params.append(value)
        
        base_query = "SELECT * FROM posts"
        
        if where_clauses:
            query = f"{base_query} WHERE {' AND '.join(where_clauses)}"
        else:
            query = base_query
        
        query += " ORDER BY created_at DESC"
        
        return self.db.execute_query(query, tuple(params))

# Производительность и индексы
class PerformanceOptimizer:
    """Класс для оптимизации производительности БД"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def analyze_query_performance(self, query: str, params: tuple = ()) -> Dict[str, Any]:
        """Анализ производительности запроса"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Получаем план выполнения запроса
            explain_query = f"EXPLAIN QUERY PLAN {query}"
            cursor.execute(explain_query, params)
            query_plan = cursor.fetchall()
            
            # Измеряем время выполнения
            import time
            start_time = time.time()
            cursor.execute(query, params)
            results = cursor.fetchall()
            execution_time = time.time() - start_time
            
            return {
                'execution_time': execution_time,
                'rows_returned': len(results),
                'query_plan': [dict(row) for row in query_plan]
            }
    
    def create_indexes(self):
        """Создание индексов для оптимизации"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_posts_title_content ON posts (title, content)",
            "CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts (created_at)",
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)",
            "CREATE INDEX IF NOT EXISTS idx_posts_views ON posts (views_count DESC)",
        ]
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            for index_query in indexes:
                cursor.execute(index_query)
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Получение статистики базы данных"""
        stats_queries = {
            'total_tables': "SELECT COUNT(*) as count FROM sqlite_master WHERE type='table'",
            'total_indexes': "SELECT COUNT(*) as count FROM sqlite_master WHERE type='index'",
            'database_size': "SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()",
            'users_count': "SELECT COUNT(*) as count FROM users",
            'posts_count': "SELECT COUNT(*) as count FROM posts",
        }
        
        stats = {}
        for key, query in stats_queries.items():
            result = self.db.execute_query(query)
            if result:
                stats[key] = result[0]['count'] if 'count' in result[0].keys() else result[0]['size']
        
        return stats
```

---

## 🔧 SQLAlchemy ORM

SQLAlchemy - мощная и гибкая ORM система для Python.

### Основы SQLAlchemy

```python
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional
import os

# Настройка базы данных
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
engine = create_engine(DATABASE_URL, echo=False)

# Базовый класс для моделей
Base = declarative_base()

# Связующая таблица для many-to-many отношений
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# Модели SQLAlchemy
class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Отношения
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author")
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Сериализация в словарь"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Category(Base):
    """Модель категории"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Самосвязь для иерархии категорий
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    
    # Отношения с постами
    posts = relationship("Post", back_populates="category")
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Tag(Base):
    """Модель тега"""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    color = Column(String(7), default='#007bff')  # HEX цвет
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Many-to-many отношение с постами
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Post(Base):
    """Модель поста"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text)  # Краткое описание
    slug = Column(String(200), unique=True, nullable=False, index=True)
    
    # Статус публикации
    is_published = Column(Boolean, default=False, nullable=False, index=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # Метрики
    views_count = Column(Integer, default=0, nullable=False)
    likes_count = Column(Integer, default=0, nullable=False)
    
    # Временные метки
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    published_at = Column(DateTime)
    
    # Внешние ключи
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), index=True)
    
    # Отношения
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def to_dict(self, include_content=False):
        """Сериализация в словарь"""
        data = {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'slug': self.slug,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'author': self.author.to_dict() if self.author else None,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'tags': [{'id': tag.id, 'name': tag.name, 'color': tag.color} for tag in self.tags]
        }
        
        if include_content:
            data['content'] = self.content
        
        return data

class Comment(Base):
    """Модель комментария"""
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Внешние ключи
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('comments.id'))  # Для вложенных комментариев
    
    # Отношения
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent")
    
    def __repr__(self):
        return f'<Comment {self.id} by {self.author.username if self.author else "Unknown"}>'

# Создание таблиц
Base.metadata.create_all(engine)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Получение сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Repository классы для SQLAlchemy
class SQLAlchemyUserRepository:
    """Репозиторий пользователей для SQLAlchemy"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, user_data: dict) -> User:
        """Создание пользователя"""
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        return self.session.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Получение пользователя по username"""
        return self.session.query(User).filter(User.username == username).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[User]:
        """Получение всех пользователей"""
        query = self.session.query(User)
        
        if active_only:
            query = query.filter(User.is_active == True)
        
        return query.offset(skip).limit(limit).all()
    
    def update(self, user_id: int, update_data: dict) -> Optional[User]:
        """Обновление пользователя"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Удаление пользователя"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.session.delete(user)
        self.session.commit()
        return True
    
    def search(self, search_term: str) -> List[User]:
        """Поиск пользователей"""
        return self.session.query(User).filter(
            (User.username.contains(search_term)) |
            (User.email.contains(search_term)) |
            (User.full_name.contains(search_term))
        ).all()

class SQLAlchemyPostRepository:
    """Репозиторий постов для SQLAlchemy"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, post_data: dict) -> Post:
        """Создание поста"""
        post = Post(**post_data)
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post
    
    def get_by_id(self, post_id: int) -> Optional[Post]:
        """Получение поста по ID"""
        return self.session.query(Post).filter(Post.id == post_id).first()
    
    def get_by_slug(self, slug: str) -> Optional[Post]:
        """Получение поста по slug"""
        return self.session.query(Post).filter(Post.slug == slug).first()
    
    def get_published(self, skip: int = 0, limit: int = 20) -> List[Post]:
        """Получение опубликованных постов"""
        return self.session.query(Post).filter(
            Post.is_published == True
        ).order_by(
            Post.published_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_author(self, author_id: int, published_only: bool = False) -> List[Post]:
        """Получение постов автора"""
        query = self.session.query(Post).filter(Post.author_id == author_id)
        
        if published_only:
            query = query.filter(Post.is_published == True)
        
        return query.order_by(Post.created_at.desc()).all()
    
    def get_by_category(self, category_id: int, published_only: bool = True) -> List[Post]:
        """Получение постов категории"""
        query = self.session.query(Post).filter(Post.category_id == category_id)
        
        if published_only:
            query = query.filter(Post.is_published == True)
        
        return query.order_by(Post.published_at.desc()).all()
    
    def get_by_tag(self, tag_name: str, published_only: bool = True) -> List[Post]:
        """Получение постов по тегу"""
        query = self.session.query(Post).join(Post.tags).filter(Tag.name == tag_name)
        
        if published_only:
            query = query.filter(Post.is_published == True)
        
        return query.order_by(Post.published_at.desc()).all()
    
    def get_featured(self, limit: int = 5) -> List[Post]:
        """Получение рекомендуемых постов"""
        return self.session.query(Post).filter(
            Post.is_published == True,
            Post.is_featured == True
        ).order_by(Post.published_at.desc()).limit(limit).all()
    
    def get_popular(self, limit: int = 10, days: int = 30) -> List[Post]:
        """Получение популярных постов"""
        from datetime import datetime, timedelta
        
        since_date = datetime.now() - timedelta(days=days)
        
        return self.session.query(Post).filter(
            Post.is_published == True,
            Post.published_at >= since_date
        ).order_by(Post.views_count.desc()).limit(limit).all()
    
    def update_views(self, post_id: int) -> bool:
        """Увеличение счетчика просмотров"""
        post = self.get_by_id(post_id)
        if not post:
            return False
        
        post.views_count += 1
        self.session.commit()
        return True
    
    def search(self, search_term: str, published_only: bool = True) -> List[Post]:
        """Поиск постов"""
        query = self.session.query(Post).filter(
            (Post.title.contains(search_term)) |
            (Post.content.contains(search_term)) |
            (Post.summary.contains(search_term))
        )
        
        if published_only:
            query = query.filter(Post.is_published == True)
        
        return query.order_by(Post.published_at.desc()).all()

# Сервисный слой для SQLAlchemy
class BlogService:
    """Сервис для работы с блогом на SQLAlchemy"""
    
    def __init__(self, session: Session):
        self.session = session
        self.user_repo = SQLAlchemyUserRepository(session)
        self.post_repo = SQLAlchemyPostRepository(session)
    
    def create_user(self, username: str, email: str, password_hash: str, 
                   full_name: str = None, is_admin: bool = False) -> User:
        """Создание пользователя"""
        # Проверяем уникальность
        if self.user_repo.get_by_email(email):
            raise ValueError("Email уже используется")
        
        if self.user_repo.get_by_username(username):
            raise ValueError("Username уже используется")
        
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'full_name': full_name,
            'is_admin': is_admin
        }
        
        return self.user_repo.create(user_data)
    
    def create_post(self, title: str, content: str, author_id: int,
                   category_id: int = None, tags: List[str] = None,
                   summary: str = None, publish: bool = False) -> Post:
        """Создание поста"""
        # Проверяем автора
        author = self.user_repo.get_by_id(author_id)
        if not author:
            raise ValueError("Автор не найден")
        
        # Генерируем slug
        import re
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        
        # Проверяем уникальность slug
        counter = 1
        original_slug = slug
        while self.post_repo.get_by_slug(slug):
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        post_data = {
            'title': title,
            'content': content,
            'summary': summary or content[:200] + '...' if len(content) > 200 else content,
            'slug': slug,
            'author_id': author_id,
            'category_id': category_id,
            'is_published': publish
        }
        
        if publish:
            post_data['published_at'] = datetime.now()
        
        post = self.post_repo.create(post_data)
        
        # Добавляем теги
        if tags:
            for tag_name in tags:
                tag = self.session.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    self.session.add(tag)
                
                post.tags.append(tag)
            
            self.session.commit()
        
        return post
    
    def get_dashboard_data(self, user_id: int) -> dict:
        """Данные для панели пользователя"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        
        user_posts = self.post_repo.get_by_author(user_id)
        published_posts = [p for p in user_posts if p.is_published]
        
        return {
            'user': user.to_dict(),
            'total_posts': len(user_posts),
            'published_posts': len(published_posts),
            'draft_posts': len(user_posts) - len(published_posts),
            'total_views': sum(p.views_count for p in published_posts),
            'total_likes': sum(p.likes_count for p in published_posts),
            'recent_posts': [p.to_dict() for p in user_posts[:5]]
        }
```

Этот раздел представляет собой полное руководство по работе с базами данных в Python, от простых SQLite операций до сложных ORM систем с SQLAlchemy. 