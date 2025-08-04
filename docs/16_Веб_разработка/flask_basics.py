# Основы Flask веб-фреймворка
try:
    from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
except ImportError:
    print("Flask не установлен. Установите: pip install flask")
    exit()

import json
from datetime import datetime

# Создание Flask приложения
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Для сессий

# Простые данные для демонстрации
users = [
    {"id": 1, "name": "Анна", "email": "anna@example.com"},
    {"id": 2, "name": "Иван", "email": "ivan@example.com"},
    {"id": 3, "name": "Мария", "email": "maria@example.com"}
]

posts = [
    {"id": 1, "title": "Первый пост", "content": "Содержимое первого поста", "author_id": 1},
    {"id": 2, "title": "Второй пост", "content": "Содержимое второго поста", "author_id": 2}
]

# Базовая маршрутизация
@app.route('/')
def home():
    """Главная страница"""
    html = """
    <h1>Добро пожаловать в Flask приложение!</h1>
    <ul>
        <li><a href="/users">Пользователи</a></li>
        <li><a href="/posts">Посты</a></li>
        <li><a href="/about">О сайте</a></li>
        <li><a href="/api/users">API пользователей</a></li>
        <li><a href="/form">Форма</a></li>
        <li><a href="/session">Сессия</a></li>
    </ul>
    <p>Время: {{ current_time }}</p>
    """
    return render_template_string(html, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/about')
def about():
    """Страница о сайте"""
    return "<h1>О нашем сайте</h1><p>Это демонстрационное Flask приложение.</p>"

# Маршруты с параметрами
@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """Детали пользователя"""
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        html = f"""
        <h1>Пользователь: {user['name']}</h1>
        <p>Email: {user['email']}</p>
        <p>ID: {user['id']}</p>
        <a href="/users">Назад к списку</a>
        """
        return html
    else:
        return "<h1>Пользователь не найден</h1>", 404

@app.route('/users')
def users_list():
    """Список пользователей"""
    html = "<h1>Список пользователей</h1><ul>"
    for user in users:
        html += f'<li><a href="/user/{user["id"]}">{user["name"]}</a> - {user["email"]}</li>'
    html += "</ul><a href='/'>Главная</a>"
    return html

@app.route('/posts')
def posts_list():
    """Список постов"""
    html = "<h1>Список постов</h1>"
    for post in posts:
        author = next((u for u in users if u["id"] == post["author_id"]), {"name": "Неизвестен"})
        html += f"""
        <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
            <h3>{post['title']}</h3>
            <p>{post['content']}</p>
            <small>Автор: {author['name']}</small>
        </div>
        """
    html += "<a href='/'>Главная</a>"
    return html

# HTTP методы
@app.route('/api/users', methods=['GET'])
def api_users():
    """API для получения пользователей"""
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def api_create_user():
    """API для создания пользователя"""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Требуются поля name и email"}), 400
    
    new_user = {
        "id": max([u["id"] for u in users]) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    """API для обновления пользователя"""
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404
    
    data = request.get_json()
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
    
    return jsonify(user)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    """API для удаления пользователя"""
    global users
    users = [u for u in users if u["id"] != user_id]
    return '', 204

# Обработка форм
@app.route('/form', methods=['GET', 'POST'])
def form_example():
    """Пример обработки форм"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        result = f"""
        <h1>Форма отправлена!</h1>
        <p>Имя: {name}</p>
        <p>Email: {email}</p>
        <p>Сообщение: {message}</p>
        <a href="/form">Назад к форме</a>
        """
        return result
    
    # GET запрос - показываем форму
    form_html = """
    <h1>Контактная форма</h1>
    <form method="POST">
        <p>
            <label>Имя:</label><br>
            <input type="text" name="name" required>
        </p>
        <p>
            <label>Email:</label><br>
            <input type="email" name="email" required>
        </p>
        <p>
            <label>Сообщение:</label><br>
            <textarea name="message" required></textarea>
        </p>
        <p>
            <input type="submit" value="Отправить">
        </p>
    </form>
    <a href="/">Главная</a>
    """
    return form_html

# Работа с сессиями
@app.route('/session')
def session_example():
    """Пример работы с сессиями"""
    if 'visits' not in session:
        session['visits'] = 0
    session['visits'] += 1
    
    html = f"""
    <h1>Сессии в Flask</h1>
    <p>Количество посещений: {session['visits']}</p>
    <p><a href="/session">Обновить</a></p>
    <p><a href="/clear_session">Очистить сессию</a></p>
    <p><a href="/">Главная</a></p>
    """
    return html

@app.route('/clear_session')
def clear_session():
    """Очистка сессии"""
    session.clear()
    return redirect(url_for('session_example'))

# Обработка ошибок
@app.errorhandler(404)
def not_found(error):
    """Обработчик ошибки 404"""
    return """
    <h1>Страница не найдена</h1>
    <p>К сожалению, запрашиваемая страница не существует.</p>
    <a href="/">Вернуться на главную</a>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    """Обработчик ошибки 500"""
    return """
    <h1>Внутренняя ошибка сервера</h1>
    <p>Произошла ошибка на сервере.</p>
    <a href="/">Вернуться на главную</a>
    """, 500

# Фильтры для шаблонов
@app.template_filter('reverse')
def reverse_filter(text):
    """Фильтр для переворота текста"""
    return text[::-1]

# Контекстный процессор
@app.context_processor
def inject_globals():
    """Добавляет глобальные переменные в шаблоны"""
    return {
        'app_name': 'Flask Demo',
        'current_year': datetime.now().year
    }

# Before/After запросов
@app.before_request
def before_request():
    """Выполняется перед каждым запросом"""
    print(f"Запрос: {request.method} {request.url}")

@app.after_request
def after_request(response):
    """Выполняется после каждого запроса"""
    print(f"Ответ: {response.status_code}")
    return response

# Маршрут с несколькими методами
@app.route('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def data_handler():
    """Обработка разных HTTP методов"""
    method = request.method
    
    if method == 'GET':
        return jsonify({"message": "GET запрос", "data": users})
    elif method == 'POST':
        return jsonify({"message": "POST запрос", "received": request.get_json()})
    elif method == 'PUT':
        return jsonify({"message": "PUT запрос", "received": request.get_json()})
    elif method == 'DELETE':
        return jsonify({"message": "DELETE запрос"})

# Пример с query параметрами
@app.route('/search')
def search():
    """Поиск с query параметрами"""
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    
    html = f"""
    <h1>Поиск</h1>
    <form method="GET">
        <input type="text" name="q" value="{query}" placeholder="Поисковый запрос">
        <select name="category">
            <option value="all" {'selected' if category == 'all' else ''}>Все</option>
            <option value="users" {'selected' if category == 'users' else ''}>Пользователи</option>
            <option value="posts" {'selected' if category == 'posts' else ''}>Посты</option>
        </select>
        <input type="submit" value="Искать">
    </form>
    """
    
    if query:
        html += f"<p>Поиск '{query}' в категории '{category}'</p>"
        
        # Простой поиск
        if category == 'users' or category == 'all':
            found_users = [u for u in users if query.lower() in u['name'].lower()]
            if found_users:
                html += "<h3>Найденные пользователи:</h3><ul>"
                for user in found_users:
                    html += f"<li>{user['name']} - {user['email']}</li>"
                html += "</ul>"
    
    html += "<a href='/'>Главная</a>"
    return html

if __name__ == '__main__':
    print("Flask приложение запущено!")
    print("Откройте http://127.0.0.1:5000 в браузере")
    print("Для остановки нажмите Ctrl+C")
    
    # Запуск в режиме отладки
    app.run(debug=True, host='127.0.0.1', port=5000) 