# SQLAlchemy ORM - Object-Relational Mapping
try:
    from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship, joinedload, selectinload
    from sqlalchemy.sql import func
    from sqlalchemy import and_, or_, desc, asc
except ImportError:
    print("SQLAlchemy не установлен. Установите: pip install sqlalchemy")
    exit()

from datetime import datetime
import os

# Базовый класс для моделей
Base = declarative_base()

# Таблица связи многие-ко-многим для постов и тегов
post_tags = Table('post_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# Модели данных
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Связь один-ко-многим с постами
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Связи
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    
    def __repr__(self):
        return f"<Post(title='{self.title}', author='{self.author.username if self.author else 'None'}')>"

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Связи
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment(content='{self.content[:30]}...', author='{self.author.username if self.author else 'None'}')>"

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # Связь многие-ко-многим с постами
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag(name='{self.name}')>"

def create_database():
    """Создание базы данных и движка"""
    print("=== Создание базы данных ===")
    
    # Создание движка (в памяти для демонстрации)
    engine = create_engine('sqlite:///blog.db', echo=False)  # echo=True для отладки SQL
    
    # Создание всех таблиц
    Base.metadata.create_all(engine)
    
    # Создание сессии
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("База данных и таблицы созданы")
    return engine, session

def insert_sample_data(session):
    """Вставка примерных данных"""
    print("\n=== Вставка данных ===")
    
    # Создание пользователей
    users = [
        User(username='alice', email='alice@example.com', password_hash='hash1'),
        User(username='bob', email='bob@example.com', password_hash='hash2'),
        User(username='charlie', email='charlie@example.com', password_hash='hash3')
    ]
    
    session.add_all(users)
    session.flush()  # Получаем ID без коммита
    
    # Создание тегов
    tags = [
        Tag(name='python'),
        Tag(name='programming'),
        Tag(name='web'),
        Tag(name='database'),
        Tag(name='tutorial')
    ]
    
    session.add_all(tags)
    session.flush()
    
    # Создание постов
    posts = [
        Post(title='Введение в Python', content='Изучаем основы Python', author=users[0]),
        Post(title='Веб-разработка с Flask', content='Создаём веб-приложения', author=users[0]),
        Post(title='Базы данных и SQLAlchemy', content='ORM в Python', author=users[1]),
        Post(title='Лучшие практики программирования', content='Советы для разработчиков', author=users[2])
    ]
    
    # Добавляем теги к постам
    posts[0].tags = [tags[0], tags[1], tags[4]]  # python, programming, tutorial
    posts[1].tags = [tags[0], tags[2], tags[4]]  # python, web, tutorial
    posts[2].tags = [tags[0], tags[3], tags[4]]  # python, database, tutorial
    posts[3].tags = [tags[1]]  # programming
    
    session.add_all(posts)
    session.flush()
    
    # Создание комментариев
    comments = [
        Comment(content='Отличная статья!', post=posts[0], author=users[1]),
        Comment(content='Очень полезно, спасибо', post=posts[0], author=users[2]),
        Comment(content='Хотелось бы больше примеров', post=posts[1], author=users[2]),
        Comment(content='Согласен с автором', post=posts[2], author=users[0]),
        Comment(content='Добавлю в закладки', post=posts[3], author=users[0])
    ]
    
    session.add_all(comments)
    session.commit()
    
    print(f"Добавлено: {len(users)} пользователей, {len(posts)} постов, {len(tags)} тегов, {len(comments)} комментариев")

def query_examples(session):
    """Примеры различных запросов"""
    print("\n=== Примеры запросов ===")
    
    # 1. Простые запросы
    print("1. Все пользователи:")
    users = session.query(User).all()
    for user in users:
        print(f"   {user.username} ({user.email})")
    
    # 2. Фильтрация
    print("\n2. Активные пользователи:")
    active_users = session.query(User).filter(User.is_active == True).all()
    for user in active_users:
        print(f"   {user.username}")
    
    # 3. Фильтрация с условиями
    print("\n3. Пользователи с определённым email:")
    user = session.query(User).filter(User.email.like('%alice%')).first()
    if user:
        print(f"   {user.username}: {user.email}")
    
    # 4. Сложные условия
    print("\n4. Посты с длинными заголовками:")
    long_title_posts = session.query(Post).filter(
        and_(Post.title.like('%Python%'), func.length(Post.title) > 10)
    ).all()
    for post in long_title_posts:
        print(f"   '{post.title}' (длина: {len(post.title)})")
    
    # 5. Сортировка
    print("\n5. Посты по дате создания (новые первые):")
    recent_posts = session.query(Post).order_by(desc(Post.created_at)).all()
    for post in recent_posts:
        print(f"   '{post.title}' - {post.created_at}")
    
    # 6. Ограничение результатов
    print("\n6. Первые 2 поста:")
    first_posts = session.query(Post).limit(2).all()
    for post in first_posts:
        print(f"   '{post.title}'")

def relationship_examples(session):
    """Примеры работы со связями"""
    print("\n=== Работа со связями ===")
    
    # 1. Получение связанных объектов
    print("1. Посты пользователя alice:")
    alice = session.query(User).filter(User.username == 'alice').first()
    if alice:
        for post in alice.posts:
            print(f"   '{post.title}'")
    
    # 2. Обратная связь
    print("\n2. Автор первого поста:")
    first_post = session.query(Post).first()
    if first_post:
        print(f"   Пост: '{first_post.title}'")
        print(f"   Автор: {first_post.author.username}")
    
    # 3. Связи многие-ко-многим
    print("\n3. Теги для постов:")
    posts_with_tags = session.query(Post).all()
    for post in posts_with_tags:
        tag_names = [tag.name for tag in post.tags]
        print(f"   '{post.title}': {', '.join(tag_names)}")
    
    # 4. Обратная связь многие-ко-многим
    print("\n4. Посты по тегу 'python':")
    python_tag = session.query(Tag).filter(Tag.name == 'python').first()
    if python_tag:
        for post in python_tag.posts:
            print(f"   '{post.title}'")

def join_examples(session):
    """Примеры JOIN запросов"""
    print("\n=== JOIN запросы ===")
    
    # 1. Внутреннее соединение
    print("1. Посты с авторами (INNER JOIN):")
    posts_with_authors = session.query(Post, User).join(User).all()
    for post, author in posts_with_authors:
        print(f"   '{post.title}' by {author.username}")
    
    # 2. Левое соединение
    print("\n2. Пользователи и количество их постов:")
    user_post_counts = session.query(
        User.username, 
        func.count(Post.id).label('post_count')
    ).outerjoin(Post).group_by(User.id).all()
    
    for username, count in user_post_counts:
        print(f"   {username}: {count} постов")
    
    # 3. Соединение с фильтрацией
    print("\n3. Посты с комментариями:")
    posts_with_comments = session.query(Post).join(Comment).distinct().all()
    for post in posts_with_comments:
        print(f"   '{post.title}' (комментариев: {len(post.comments)})")

def eager_loading_examples(session):
    """Примеры жадной загрузки"""
    print("\n=== Жадная загрузка (Eager Loading) ===")
    
    # 1. Загрузка с joinedload
    print("1. Посты с авторами (joinedload):")
    posts = session.query(Post).options(joinedload(Post.author)).all()
    for post in posts:
        print(f"   '{post.title}' by {post.author.username}")
    
    # 2. Загрузка с selectinload
    print("\n2. Пользователи с постами (selectinload):")
    users = session.query(User).options(selectinload(User.posts)).all()
    for user in users:
        print(f"   {user.username}: {len(user.posts)} постов")
    
    # 3. Вложенная загрузка
    print("\n3. Посты с авторами и комментариями:")
    posts = session.query(Post).options(
        joinedload(Post.author),
        selectinload(Post.comments).joinedload(Comment.author)
    ).all()
    
    for post in posts:
        print(f"   '{post.title}' by {post.author.username}")
        for comment in post.comments:
            print(f"     - {comment.author.username}: {comment.content[:30]}...")

def aggregation_examples(session):
    """Примеры агрегационных функций"""
    print("\n=== Агрегационные функции ===")
    
    # 1. Подсчёт
    print("1. Статистика:")
    user_count = session.query(func.count(User.id)).scalar()
    post_count = session.query(func.count(Post.id)).scalar()
    comment_count = session.query(func.count(Comment.id)).scalar()
    
    print(f"   Пользователей: {user_count}")
    print(f"   Постов: {post_count}")
    print(f"   Комментариев: {comment_count}")
    
    # 2. Группировка
    print("\n2. Количество постов по пользователям:")
    post_counts = session.query(
        User.username,
        func.count(Post.id).label('post_count')
    ).outerjoin(Post).group_by(User.id).all()
    
    for username, count in post_counts:
        print(f"   {username}: {count}")
    
    # 3. Максимум, минимум, среднее
    print("\n3. Статистика по длине заголовков:")
    stats = session.query(
        func.min(func.length(Post.title)).label('min_length'),
        func.max(func.length(Post.title)).label('max_length'),
        func.avg(func.length(Post.title)).label('avg_length')
    ).first()
    
    print(f"   Минимальная длина: {stats.min_length}")
    print(f"   Максимальная длина: {stats.max_length}")
    print(f"   Средняя длина: {stats.avg_length:.2f}")

def crud_operations(session):
    """Операции CRUD"""
    print("\n=== CRUD операции ===")
    
    # CREATE
    print("1. Создание нового пользователя:")
    new_user = User(username='new_user', email='new@example.com', password_hash='hash_new')
    session.add(new_user)
    session.commit()
    print(f"   Создан пользователь: {new_user.username}")
    
    # READ
    print("\n2. Чтение пользователя:")
    user = session.query(User).filter(User.username == 'new_user').first()
    if user:
        print(f"   Найден: {user.username} ({user.email})")
    
    # UPDATE
    print("\n3. Обновление email:")
    if user:
        user.email = 'updated@example.com'
        session.commit()
        print(f"   Обновлён email: {user.email}")
    
    # DELETE
    print("\n4. Удаление пользователя:")
    if user:
        session.delete(user)
        session.commit()
        print("   Пользователь удалён")

def transaction_examples(session):
    """Примеры работы с транзакциями"""
    print("\n=== Транзакции ===")
    
    try:
        # Начинаем транзакцию
        print("1. Создание пользователя и поста в одной транзакции:")
        
        user = User(username='trans_user', email='trans@example.com', password_hash='hash')
        session.add(user)
        session.flush()  # Получаем ID без коммита
        
        post = Post(title='Транзакционный пост', content='Содержимое', author=user)
        session.add(post)
        
        # Имитация ошибки (раскомментируйте для тестирования)
        # raise Exception("Имитация ошибки")
        
        session.commit()
        print("   Транзакция успешно завершена")
        
    except Exception as e:
        session.rollback()
        print(f"   Ошибка в транзакции: {e}")
        print("   Изменения отменены")

def advanced_queries(session):
    """Продвинутые запросы"""
    print("\n=== Продвинутые запросы ===")
    
    # 1. Подзапросы
    print("1. Пользователи с наибольшим количеством постов:")
    max_posts_subquery = session.query(
        func.max(func.count(Post.id))
    ).select_from(Post).group_by(Post.user_id).subquery()
    
    user_post_counts = session.query(
        User.username,
        func.count(Post.id).label('post_count')
    ).outerjoin(Post).group_by(User.id).having(
        func.count(Post.id) == max_posts_subquery
    ).all()
    
    for username, count in user_post_counts:
        print(f"   {username}: {count} постов")
    
    # 2. EXISTS запросы
    print("\n2. Пользователи с комментариями:")
    users_with_comments = session.query(User).filter(
        session.query(Comment).filter(Comment.user_id == User.id).exists()
    ).all()
    
    for user in users_with_comments:
        print(f"   {user.username}")
    
    # 3. CASE выражения
    print("\n3. Классификация постов по длине заголовка:")
    post_classifications = session.query(
        Post.title,
        func.case(
            [(func.length(Post.title) < 20, 'Короткий')],
            else_='Длинный'
        ).label('classification')
    ).all()
    
    for title, classification in post_classifications:
        print(f"   '{title}': {classification}")

def cleanup_database():
    """Очистка базы данных"""
    print("\n=== Очистка ===")
    if os.path.exists('blog.db'):
        os.remove('blog.db')
        print("Файл базы данных удалён")

# Демонстрация всех возможностей
if __name__ == "__main__":
    try:
        print("Демонстрация SQLAlchemy ORM")
        print("=" * 50)
        
        # Создание базы данных и сессии
        engine, session = create_database()
        
        # Примеры работы с ORM
        insert_sample_data(session)
        query_examples(session)
        relationship_examples(session)
        join_examples(session)
        eager_loading_examples(session)
        aggregation_examples(session)
        crud_operations(session)
        transaction_examples(session)
        advanced_queries(session)
        
        # Закрытие сессии
        session.close()
        
        print("\n=== Преимущества SQLAlchemy ORM ===")
        advantages = [
            "1. Объектно-ориентированный подход к работе с БД",
            "2. Автоматическое создание SQL запросов",
            "3. Поддержка различных СУБД",
            "4. Ленивая загрузка связанных объектов",
            "5. Встроенная поддержка транзакций",
            "6. Миграции и версионирование схемы",
            "7. Защита от SQL инъекций",
            "8. Мощные возможности запросов"
        ]
        
        for advantage in advantages:
            print(f"   {advantage}")
            
        print("\n=== Лучшие практики ===")
        best_practices = [
            "1. Используйте контекстные менеджеры для сессий",
            "2. Применяйте жадную загрузку для избежания N+1 проблем",
            "3. Используйте индексы для оптимизации запросов",
            "4. Закрывайте сессии после использования",
            "5. Используйте flush() для получения ID перед commit()",
            "6. Обрабатывайте исключения и делайте rollback()",
            "7. Используйте connection pooling для производительности",
            "8. Валидируйте данные перед сохранением в БД"
        ]
        
        for practice in best_practices:
            print(f"   {practice}")
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    finally:
        # Очистка (раскомментируйте для удаления файла БД)
        # cleanup_database()
        print(f"\nФайл базы данных blog.db сохранён для изучения")
        print("Для очистки запустите функцию cleanup_database()") 