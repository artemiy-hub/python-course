# Пример использования библиотеки requests
try:
    import requests
    
    # GET-запрос
    response = requests.get('https://httpbin.org/get')
    print(f"Статус: {response.status_code}")
    print(f"JSON: {response.json()}")
    
    # POST-запрос
    data = {'key': 'value'}
    response = requests.post('https://httpbin.org/post', json=data)
    print(f"POST ответ: {response.json()}")
    
except ImportError:
    print("Библиотека requests не установлена. Установите: pip install requests") 