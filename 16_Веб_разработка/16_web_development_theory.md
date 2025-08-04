# Теория: Веб-разработка на Python

## 🎯 Цель раздела

Этот раздел охватывает все аспекты веб-разработки на Python: от создания простых веб-приложений до сложных API, от веб-скрапинга до современных асинхронных фреймворков.

## 📋 Содержание

1. [HTTP и веб-основы](#http-и-веб-основы)
2. [Flask - микрофреймворк](#flask---микрофреймворк)
3. [FastAPI - современный API](#fastapi---современный-api)
4. [Django - полнофункциональный фреймворк](#django---полнофункциональный-фреймворк)
5. [Веб-скрапинг](#веб-скрапинг)
6. [WebSocket и real-time](#websocket-и-real-time)
7. [Развертывание веб-приложений](#развертывание-веб-приложений)

---

## 🌐 HTTP и веб-основы

### Протокол HTTP

HTTP (HyperText Transfer Protocol) - основа веб-коммуникации. Понимание HTTP критично для веб-разработки.

```python
import requests
from typing import Dict, Any, Optional
import json

class HTTPClient:
    """Класс для демонстрации HTTP концепций"""
    
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """GET запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.get(url, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
             json_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """POST запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if json_data:
            return self.session.post(url, json=json_data)
        return self.session.post(url, data=data)
    
    def put(self, endpoint: str, json_data: Dict[str, Any]) -> requests.Response:
        """PUT запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.put(url, json=json_data)
    
    def delete(self, endpoint: str) -> requests.Response:
        """DELETE запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.delete(url)

# Практический пример работы с REST API
def demonstrate_rest_api():
    """Демонстрация работы с REST API"""
    
    # Создаем клиент
    client = HTTPClient(
        base_url="https://jsonplaceholder.typicode.com",
        headers={"User-Agent": "Python-HTTP-Client/1.0"}
    )
    
    # GET запрос - получение списка постов
    response = client.get("/posts", params={"_limit": 5})
    if response.status_code == 200:
        posts = response.json()
        print(f"Получено {len(posts)} постов")
    
    # POST запрос - создание нового поста
    new_post = {
        "title": "Мой новый пост",
        "body": "Содержимое поста",
        "userId": 1
    }
    
    response = client.post("/posts", json_data=new_post)
    if response.status_code == 201:
        created_post = response.json()
        print(f"Создан пост с ID: {created_post.get('id')}")
    
    # PUT запрос - обновление поста
    updated_post = {
        "id": 1,
        "title": "Обновленный заголовок",
        "body": "Обновленное содержимое",
        "userId": 1
    }
    
    response = client.put("/posts/1", json_data=updated_post)
    if response.status_code == 200:
        print("Пост успешно обновлен")
    
    # DELETE запрос - удаление поста
    response = client.delete("/posts/1")
    if response.status_code == 200:
        print("Пост успешно удален")

# Обработка ошибок HTTP
class HTTPError(Exception):
    """Базовый класс для HTTP ошибок"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")

class APIClient:
    """Продвинутый API клиент с обработкой ошибок"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.session = requests.Session()
        
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Внутренний метод для выполнения запросов"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # Бросает исключение для HTTP ошибок
            
            # Пытаемся декодировать JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"content": response.text}
                
        except requests.exceptions.Timeout:
            raise HTTPError(408, "Timeout")
        except requests.exceptions.ConnectionError:
            raise HTTPError(503, "Service Unavailable")
        except requests.exceptions.HTTPError as e:
            raise HTTPError(e.response.status_code, str(e))
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._make_request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self._make_request("POST", endpoint, **kwargs)
```

### Cookies и сессии

```python
import requests
from http.cookies import SimpleCookie
from typing import Dict, Optional

class SessionManager:
    """Управление сессиями и cookies"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session_data: Dict[str, Any] = {}
    
    def login(self, username: str, password: str, login_url: str) -> bool:
        """Авторизация с сохранением сессии"""
        login_data = {
            "username": username,
            "password": password
        }
        
        response = self.session.post(login_url, data=login_data)
        
        if response.status_code == 200:
            # Сохраняем информацию о сессии
            self.session_data["username"] = username
            self.session_data["logged_in"] = True
            return True
        
        return False
    
    def get_session_info(self) -> Dict[str, Any]:
        """Получение информации о сессии"""
        cookies_info = {}
        for cookie in self.session.cookies:
            cookies_info[cookie.name] = {
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "secure": cookie.secure,
                "expires": cookie.expires
            }
        
        return {
            "session_data": self.session_data,
            "cookies": cookies_info
        }
    
    def make_authenticated_request(self, url: str) -> requests.Response:
        """Выполнение авторизованного запроса"""
        if not self.session_data.get("logged_in"):
            raise Exception("Не авторизован")
        
        return self.session.get(url)

# Работа с cookies
def cookie_example():
    """Пример работы с cookies"""
    
    # Создание cookie
    cookie = SimpleCookie()
    cookie["user_preference"] = "dark_theme"
    cookie["user_preference"]["expires"] = "Wed, 31 Dec 2025 23:59:59 GMT"
    cookie["user_preference"]["path"] = "/"
    
    print(f"Cookie: {cookie}")
    
    # Парсинг cookie строки
    cookie_string = "session_id=abc123; user_lang=en; theme=dark"
    parsed_cookies = SimpleCookie(cookie_string)
    
    for name, morsel in parsed_cookies.items():
        print(f"Cookie {name}: {morsel.value}")
```

---

## 🌶️ Flask - микрофреймворк

Flask - минималистичный и гибкий веб-фреймворк для Python.

### Основы Flask

```python
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from typing import Dict, Any, Optional
import os

# Создание приложения Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Конфигурация
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    DEBUG = os.environ.get('FLASK_ENV') == 'development'

app.config.from_object(Config)

# Простые маршруты
@app.route('/')
def home():
    """Главная страница"""
    return render_template('index.html', title='Главная')

@app.route('/hello/<name>')
def hello(name: str):
    """Приветствие с параметром"""
    return f"Привет, {name}!"

@app.route('/user/<int:user_id>')
def user_profile(user_id: int):
    """Профиль пользователя с типизированным параметром"""
    # Имитация получения пользователя из БД
    user = {"id": user_id, "name": f"User_{user_id}", "email": f"user{user_id}@example.com"}
    return render_template('user.html', user=user)

# HTTP методы
@app.route('/api/users', methods=['GET', 'POST'])
def users_api():
    """API для работы с пользователями"""
    if request.method == 'GET':
        # Получение списка пользователей
        users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ]
        return jsonify(users)
    
    elif request.method == 'POST':
        # Создание нового пользователя
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({"error": "Name and email are required"}), 400
        
        new_user = {
            "id": 3,  # В реальности генерируется БД
            "name": data['name'],
            "email": data['email']
        }
        
        return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail_api(user_id: int):
    """API для работы с конкретным пользователем"""
    if request.method == 'GET':
        user = {"id": user_id, "name": f"User_{user_id}"}
        return jsonify(user)
    
    elif request.method == 'PUT':
        data = request.get_json()
        updated_user = {"id": user_id, **data}
        return jsonify(updated_user)
    
    elif request.method == 'DELETE':
        return '', 204

# Формы и валидация
from werkzeug.datastructures import ImmutableMultiDict

class FormValidator:
    """Валидатор форм"""
    
    @staticmethod
    def validate_registration(form_data: ImmutableMultiDict) -> Dict[str, Any]:
        errors = {}
        
        username = form_data.get('username', '').strip()
        email = form_data.get('email', '').strip()
        password = form_data.get('password', '')
        confirm_password = form_data.get('confirm_password', '')
        
        if not username or len(username) < 3:
            errors['username'] = 'Username должен содержать минимум 3 символа'
        
        if not email or '@' not in email:
            errors['email'] = 'Некорректный email'
        
        if not password or len(password) < 8:
            errors['password'] = 'Пароль должен содержать минимум 8 символов'
        
        if password != confirm_password:
            errors['confirm_password'] = 'Пароли не совпадают'
        
        return errors

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация пользователя"""
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        errors = FormValidator.validate_registration(request.form)
        
        if errors:
            return render_template('register.html', errors=errors), 400
        
        # Создание пользователя
        password_hash = generate_password_hash(request.form['password'])
        
        # Здесь должно быть сохранение в БД
        user_data = {
            'username': request.form['username'],
            'email': request.form['email'],
            'password_hash': password_hash
        }
        
        session['user_id'] = 1  # ID созданного пользователя
        session['username'] = user_data['username']
        
        return redirect(url_for('dashboard'))

# Авторизация и сессии
def login_required(f):
    """Декоратор для проверки авторизации"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Авторизация пользователя"""
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Здесь должна быть проверка в БД
        # Для примера используем статические данные
        if username == 'admin' and password == 'password':
            session['user_id'] = 1
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Неверные учетные данные')

@app.route('/logout')
def logout():
    """Выход из системы"""
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Панель управления (требует авторизации)"""
    return render_template('dashboard.html', username=session['username'])

# Обработка ошибок
@app.errorhandler(404)
def not_found(error):
    """Обработка ошибки 404"""
    if request.path.startswith('/api/'):
        return jsonify({"error": "Not Found"}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Обработка внутренних ошибок"""
    if request.path.startswith('/api/'):
        return jsonify({"error": "Internal Server Error"}), 500
    return render_template('500.html'), 500

# Middleware
@app.before_request
def before_request():
    """Выполняется перед каждым запросом"""
    # Логирование запросов
    print(f"Request: {request.method} {request.path}")

@app.after_request
def after_request(response):
    """Выполняется после каждого запроса"""
    # Добавление заголовков безопасности
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Blueprints для модульности
from flask import Blueprint

# API Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/health')
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({"status": "healthy", "version": "1.0.0"})

@api_bp.route('/status')
def status():
    """Статус сервиса"""
    return jsonify({
        "uptime": "1h 30m",
        "requests_processed": 1547,
        "active_users": 23
    })

# Регистрация Blueprint
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Flask Extensions

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime

# Настройка расширений
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модели базы данных
class User(UserMixin, db.Model):
    """Модель пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Связи
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def check_password(self, password: str) -> bool:
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    """Модель поста"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Внешний ключ
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.title}>'

@login_manager.user_loader
def load_user(user_id: str):
    """Загрузка пользователя для Flask-Login"""
    return User.query.get(int(user_id))

# WTForms формы
class LoginForm(FlaskForm):
    """Форма авторизации"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    """Форма регистрации"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Зарегистрироваться')

class PostForm(FlaskForm):
    """Форма создания поста"""
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=200)])
    content = StringField('Содержимое', validators=[DataRequired()])
    submit = SubmitField('Создать пост')

# Маршруты с использованием расширений
@app.route('/posts')
def posts():
    """Список всех постов"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5, error_out=False)
    return render_template('posts.html', posts=posts)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    """Создание нового поста"""
    form = PostForm()
    
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('posts'))
    
    return render_template('create_post.html', form=form)
```

---

## ⚡ FastAPI - современный API

FastAPI - современный, быстрый веб-фреймворк для создания API с автоматической документацией.

### Основы FastAPI

```python
from fastapi import FastAPI, HTTPException, Depends, status, Request, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
import uvicorn

# Создание приложения
app = FastAPI(
    title="Modern API",
    description="Современный API с автоматической документацией",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Pydantic модели
class UserBase(BaseModel):
    """Базовая модель пользователя"""
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: str = Field(..., description="Email адрес")
    full_name: Optional[str] = Field(None, max_length=100, description="Полное имя")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Некорректный email')
        return v.lower()

class UserCreate(UserBase):
    """Модель для создания пользователя"""
    password: str = Field(..., min_length=8, description="Пароль")

class UserResponse(UserBase):
    """Модель ответа с пользователем"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True  # Для совместимости с ORM

class PostBase(BaseModel):
    """Базовая модель поста"""
    title: str = Field(..., max_length=200)
    content: str = Field(..., description="Содержимое поста")

class PostCreate(PostBase):
    """Модель для создания поста"""
    pass

class PostResponse(PostBase):
    """Модель ответа с постом"""
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Базы данных и аутентификация (упрощенно)
fake_users_db = {}
fake_posts_db = {}

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Получение текущего пользователя"""
    # В реальности здесь должна быть проверка JWT токена
    token = credentials.credentials
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"id": 1, "username": "admin", "email": "admin@example.com"}

# Основные маршруты
@app.get("/", tags=["general"])
async def root():
    """Корневой маршрут"""
    return {"message": "Добро пожаловать в Modern API"}

@app.get("/health", tags=["general"])
async def health_check():
    """Проверка здоровья сервиса"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

# CRUD операции для пользователей
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
async def create_user(user: UserCreate):
    """Создание нового пользователя"""
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    user_id = len(fake_users_db) + 1
    user_data = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": True,
        "created_at": datetime.now()
    }
    
    fake_users_db[user.username] = user_data
    return UserResponse(**user_data)

@app.get("/users/", response_model=List[UserResponse], tags=["users"])
async def get_users(skip: int = 0, limit: int = 10):
    """Получение списка пользователей"""
    users = list(fake_users_db.values())[skip:skip + limit]
    return [UserResponse(**user) for user in users]

@app.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(user_id: int):
    """Получение пользователя по ID"""
    for user in fake_users_db.values():
        if user["id"] == user_id:
            return UserResponse(**user)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

@app.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(user_id: int, user_update: UserBase, current_user: dict = Depends(get_current_user)):
    """Обновление пользователя"""
    for username, user in fake_users_db.items():
        if user["id"] == user_id:
            user.update({
                "username": user_update.username,
                "email": user_update.email,
                "full_name": user_update.full_name
            })
            return UserResponse(**user)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """Удаление пользователя"""
    for username, user in list(fake_users_db.items()):
        if user["id"] == user_id:
            del fake_users_db[username]
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

# Асинхронные операции
@app.post("/posts/", response_model=PostResponse, tags=["posts"])
async def create_post(post: PostCreate, background_tasks: BackgroundTasks, 
                     current_user: dict = Depends(get_current_user)):
    """Создание поста с фоновыми задачами"""
    
    post_id = len(fake_posts_db) + 1
    post_data = {
        "id": post_id,
        "title": post.title,
        "content": post.content,
        "author_id": current_user["id"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    fake_posts_db[post_id] = post_data
    
    # Добавляем фоновую задачу
    background_tasks.add_task(send_notification, post_data["title"])
    
    return PostResponse(**post_data)

async def send_notification(post_title: str):
    """Фоновая задача для отправки уведомлений"""
    await asyncio.sleep(2)  # Имитация отправки email/push
    print(f"Уведомление отправлено о новом посте: {post_title}")

@app.get("/posts/", response_model=List[PostResponse], tags=["posts"])
async def get_posts(skip: int = 0, limit: int = 10):
    """Получение списка постов"""
    posts = list(fake_posts_db.values())[skip:skip + limit]
    return [PostResponse(**post) for post in posts]

# WebSocket поддержка
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """Менеджер WebSocket соединений"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """WebSocket для real-time коммуникации"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Вы сказали: {data}", websocket)
            await manager.broadcast(f"Клиент #{client_id} сказал: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Клиент #{client_id} отключился")

# Обработка ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Кастомная обработка HTTP ошибок"""
    return {
        "error": True,
        "message": exc.detail,
        "status_code": exc.status_code,
        "path": request.url.path
    }

# Middleware для логирования
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логирование запросов"""
    start_time = datetime.now()
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### Продвинутые возможности FastAPI

```python
from fastapi import FastAPI, Query, Path, Body, Cookie, Header, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional, Union
import aiofiles
from pathlib import Path as PathLib

app = FastAPI()

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Продвинутые параметры запросов
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^[a-zA-Z ]+$"),
    skip: int = Query(0, ge=0, description="Количество элементов для пропуска"),
    limit: int = Query(10, gt=0, le=100, description="Максимальное количество элементов"),
    sort_by: Optional[str] = Query("created_at", enum=["created_at", "name", "price"]),
    tags: List[str] = Query([], description="Список тегов для фильтрации")
):
    """Получение элементов с расширенной фильтрацией"""
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "tags": tags
    }

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., gt=0, description="ID элемента"),
    user_agent: Optional[str] = Header(None),
    session_id: Optional[str] = Cookie(None)
):
    """Получение элемента с информацией о клиенте"""
    return {
        "item_id": item_id,
        "user_agent": user_agent,
        "session_id": session_id
    }

# Загрузка файлов
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Загрузка файла"""
    # Проверка типа файла
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Только изображения разрешены")
    
    # Сохранение файла
    file_path = PathLib("uploads") / file.filename
    file_path.parent.mkdir(exist_ok=True)
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content)
    }

@app.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Загрузка нескольких файлов"""
    results = []
    
    for file in files:
        file_path = PathLib("uploads") / file.filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        results.append({
            "filename": file.filename,
            "size": len(content)
        })
    
    return {"uploaded_files": results}

# Формы
@app.post("/forms/contact/")
async def contact_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    newsletter: bool = Form(False)
):
    """Обработка контактной формы"""
    return {
        "name": name,
        "email": email,
        "message": message,
        "newsletter": newsletter
    }

# Различные типы ответов
@app.get("/download/{filename}")
async def download_file(filename: str):
    """Скачивание файла"""
    file_path = PathLib("downloads") / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.get("/html", response_class=HTMLResponse)
async def get_html():
    """Возврат HTML"""
    return """
    <html>
        <head>
            <title>FastAPI HTML</title>
        </head>
        <body>
            <h1>Это HTML ответ</h1>
            <p>Создан с помощью FastAPI</p>
        </body>
    </html>
    """

# Условные ответы
class Item(BaseModel):
    name: str
    price: float
    
class ErrorModel(BaseModel):
    message: str
    code: int

@app.get("/items/{item_id}/details",
         responses={
             200: {"model": Item, "description": "Успешный ответ"},
             404: {"model": ErrorModel, "description": "Элемент не найден"},
             422: {"model": ErrorModel, "description": "Ошибка валидации"}
         })
async def get_item_details(item_id: int):
    """Получение деталей элемента с документированными ответами"""
    if item_id == 42:
        return Item(name="Особый элемент", price=99.99)
    elif item_id < 0:
        raise HTTPException(
            status_code=422,
            detail=ErrorModel(message="ID не может быть отрицательным", code=422).dict()
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=ErrorModel(message="Элемент не найден", code=404).dict()
        )
```

Этот раздел охватывает основы веб-разработки на Python, от простых HTTP клиентов до сложных API с современными возможностями. 