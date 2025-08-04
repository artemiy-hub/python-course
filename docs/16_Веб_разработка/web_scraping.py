# Веб-скрейпинг с requests и BeautifulSoup
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Необходимые библиотеки не установлены.")
    print("Установите: pip install requests beautifulsoup4 lxml")
    exit()

import time
import re
from urllib.parse import urljoin, urlparse
import json

# Основы веб-скрейпинга
def basic_scraping_example():
    """Базовый пример скрейпинга"""
    print("=== Базовый веб-скрейпинг ===")
    
    # Простой HTML для демонстрации
    html_content = """
    <html>
    <head><title>Тестовая страница</title></head>
    <body>
        <h1>Главный заголовок</h1>
        <div class="content">
            <p class="text">Первый параграф</p>
            <p class="text important">Важный параграф</p>
            <ul>
                <li>Элемент 1</li>
                <li>Элемент 2</li>
                <li>Элемент 3</li>
            </ul>
            <div id="data" data-value="123">Данные</div>
        </div>
        <a href="https://example.com">Ссылка</a>
    </body>
    </html>
    """
    
    # Парсинг HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Поиск элементов
    print(f"Заголовок: {soup.find('h1').text}")
    print(f"Текст всех параграфов: {[p.text for p in soup.find_all('p')]}")
    print(f"Элементы списка: {[li.text for li in soup.find_all('li')]}")
    print(f"Ссылка: {soup.find('a')['href']}")
    print(f"Данные атрибута: {soup.find('div', id='data')['data-value']}")

def css_selectors_example():
    """Примеры CSS селекторов"""
    print("\n=== CSS селекторы ===")
    
    html = """
    <div class="container">
        <div class="item" id="item1">
            <h2>Заголовок 1</h2>
            <p class="description">Описание 1</p>
            <span class="price">100 руб</span>
        </div>
        <div class="item" id="item2">
            <h2>Заголовок 2</h2>
            <p class="description">Описание 2</p>
            <span class="price">200 руб</span>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # CSS селекторы
    print(f"По классу: {[item.text for item in soup.select('.item h2')]}")
    print(f"По ID: {soup.select('#item1 .price')[0].text}")
    print(f"Дочерние элементы: {[p.text for p in soup.select('.container > .item > p')]}")
    print(f"Соседние элементы: {[span.text for span in soup.select('p + span')]}")

def scrape_quotes_example():
    """Пример скрейпинга цитат"""
    print("\n=== Скрейпинг цитат ===")
    
    try:
        # Делаем запрос к сайту с цитатами
        url = "http://quotes.toscrape.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Находим все цитаты
        quotes = soup.find_all('div', class_='quote')
        
        for i, quote in enumerate(quotes[:3], 1):  # Берём первые 3
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            
            print(f"\nЦитата {i}:")
            print(f"Текст: {text}")
            print(f"Автор: {author}")
            print(f"Теги: {', '.join(tags)}")
            
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        print("Проверьте подключение к интернету")

def scrape_with_session():
    """Скрейпинг с использованием сессии"""
    print("\n=== Скрейпинг с сессией ===")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        # Первый запрос
        response = session.get("http://httpbin.org/cookies/set/session_id/12345")
        
        # Второй запрос (cookies сохранены)
        response = session.get("http://httpbin.org/cookies")
        data = response.json()
        
        print(f"Cookies в сессии: {data['cookies']}")
        
    except Exception as e:
        print(f"Ошибка: {e}")

def handle_forms():
    """Работа с формами"""
    print("\n=== Работа с формами ===")
    
    # HTML форма для демонстрации
    form_html = """
    <form id="login" action="/login" method="post">
        <input type="hidden" name="csrf_token" value="abc123">
        <input type="text" name="username" required>
        <input type="password" name="password" required>
        <input type="submit" value="Войти">
    </form>
    """
    
    soup = BeautifulSoup(form_html, 'html.parser')
    form = soup.find('form')
    
    # Извлекаем данные формы
    action = form.get('action', '')
    method = form.get('method', 'get')
    
    # Находим все поля
    inputs = form.find_all('input')
    form_data = {}
    
    for input_tag in inputs:
        name = input_tag.get('name')
        value = input_tag.get('value', '')
        input_type = input_tag.get('type', 'text')
        
        if name and input_type != 'submit':
            form_data[name] = value
    
    print(f"Действие формы: {action}")
    print(f"Метод: {method}")
    print(f"Поля формы: {form_data}")

def scrape_with_delay():
    """Скрейпинг с задержками (вежливый скрейпинг)"""
    print("\n=== Вежливый скрейпинг ===")
    
    urls = [
        "http://httpbin.org/delay/1",
        "http://httpbin.org/delay/1", 
        "http://httpbin.org/delay/1"
    ]
    
    for i, url in enumerate(urls, 1):
        print(f"Запрос {i}...")
        try:
            response = requests.get(url, timeout=5)
            print(f"Статус: {response.status_code}")
            
            # Задержка между запросами
            if i < len(urls):
                print("Ожидание 2 секунды...")
                time.sleep(2)
                
        except requests.Timeout:
            print(f"Таймаут для запроса {i}")
        except Exception as e:
            print(f"Ошибка: {e}")

def extract_links():
    """Извлечение ссылок со страницы"""
    print("\n=== Извлечение ссылок ===")
    
    html = """
    <div>
        <a href="https://example.com">Внешняя ссылка</a>
        <a href="/internal">Внутренняя ссылка</a>
        <a href="mailto:test@example.com">Email</a>
        <a href="#section">Якорь</a>
        <a href="javascript:void(0)">JavaScript</a>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    base_url = "https://example.com"
    
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link['href']
        text = link.text.strip()
        
        # Классификация ссылок
        if href.startswith('http'):
            link_type = "Абсолютная"
        elif href.startswith('/'):
            link_type = "Относительная"
            href = urljoin(base_url, href)
        elif href.startswith('mailto:'):
            link_type = "Email"
        elif href.startswith('#'):
            link_type = "Якорь"
        elif href.startswith('javascript:'):
            link_type = "JavaScript"
        else:
            link_type = "Другая"
        
        print(f"{link_type}: {href} ({text})")

def parse_table():
    """Парсинг таблиц"""
    print("\n=== Парсинг таблиц ===")
    
    table_html = """
    <table>
        <thead>
            <tr>
                <th>Имя</th>
                <th>Возраст</th>
                <th>Город</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Анна</td>
                <td>25</td>
                <td>Москва</td>
            </tr>
            <tr>
                <td>Иван</td>
                <td>30</td>
                <td>СПб</td>
            </tr>
            <tr>
                <td>Мария</td>
                <td>28</td>
                <td>Казань</td>
            </tr>
        </tbody>
    </table>
    """
    
    soup = BeautifulSoup(table_html, 'html.parser')
    table = soup.find('table')
    
    # Извлекаем заголовки
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    print(f"Заголовки: {headers}")
    
    # Извлекаем данные
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        row = [td.text.strip() for td in tr.find_all('td')]
        rows.append(dict(zip(headers, row)))
    
    print("Данные:")
    for row in rows:
        print(f"  {row}")

def advanced_scraping_tips():
    """Продвинутые техники скрейпинга"""
    print("\n=== Продвинутые техники ===")
    
    # Пример обработки различных кодировок
    def handle_encoding():
        print("1. Обработка кодировок:")
        html_bytes = "Привет мир".encode('utf-8')
        soup = BeautifulSoup(html_bytes, 'html.parser', from_encoding='utf-8')
        print(f"   Декодировано: {soup.get_text()}")
    
    # Пример поиска по регулярным выражениям
    def regex_search():
        print("\n2. Поиск по регулярным выражениям:")
        html = '<div class="item-123">Товар</div><div class="item-456">Другой товар</div>'
        soup = BeautifulSoup(html, 'html.parser')
        
        # Поиск по паттерну класса
        items = soup.find_all('div', class_=re.compile(r'item-\d+'))
        for item in items:
            print(f"   Найден: {item['class']} - {item.text}")
    
    # Пример обработки атрибутов данных
    def data_attributes():
        print("\n3. Атрибуты данных:")
        html = '<div data-id="123" data-name="product">Товар</div>'
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div')
        
        print(f"   data-id: {div.get('data-id')}")
        print(f"   data-name: {div.get('data-name')}")
    
    handle_encoding()
    regex_search()
    data_attributes()

def scraping_best_practices():
    """Лучшие практики веб-скрейпинга"""
    print("\n=== Лучшие практики ===")
    
    practices = [
        "1. Проверяйте robots.txt перед скрейпингом",
        "2. Используйте задержки между запросами",
        "3. Устанавливайте User-Agent заголовок",
        "4. Обрабатывайте ошибки и таймауты",
        "5. Кешируйте результаты когда возможно",
        "6. Используйте сессии для сохранения cookies",
        "7. Проверяйте статус-коды ответов",
        "8. Соблюдайте условия использования сайта",
        "9. Рассмотрите использование API если доступно",
        "10. Тестируйте на небольших данных сначала"
    ]
    
    for practice in practices:
        print(f"   {practice}")

# Демонстрация всех функций
if __name__ == "__main__":
    try:
        basic_scraping_example()
        css_selectors_example()
        scrape_quotes_example()
        scrape_with_session()
        handle_forms()
        scrape_with_delay()
        extract_links()
        parse_table()
        advanced_scraping_tips()
        scraping_best_practices()
        
        print("\n=== Заключение ===")
        print("Веб-скрейпинг - мощный инструмент для извлечения данных")
        print("Помните о этических и правовых аспектах")
        print("Всегда проверяйте robots.txt и условия использования")
        
    except KeyboardInterrupt:
        print("\nСкрипт прерван пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}") 