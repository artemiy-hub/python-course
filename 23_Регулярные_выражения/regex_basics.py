# Основы регулярных выражений в Python
import re
from typing import List, Optional, Match

def demonstrate_basic_functions():
    """Демонстрация основных функций модуля re"""
    print("=== Основные функции модуля re ===")
    
    text = "Телефон: +7-123-456-78-90, Email: user@example.com"
    
    # re.search() - поиск первого совпадения
    phone_match = re.search(r'\+7-\d{3}-\d{3}-\d{2}-\d{2}', text)
    if phone_match:
        print(f"re.search() найден телефон: {phone_match.group()}")
        print(f"Позиция: {phone_match.start()}-{phone_match.end()}")
    
    # re.match() - поиск в начале строки
    match_result = re.match(r'Телефон', text)
    if match_result:
        print(f"re.match() найдено в начале: {match_result.group()}")
    
    # re.findall() - поиск всех совпадений
    digits = re.findall(r'\d+', text)
    print(f"re.findall() все числа: {digits}")
    
    # re.finditer() - итератор совпадений
    print("re.finditer() все числа с позициями:")
    for match in re.finditer(r'\d+', text):
        print(f"   '{match.group()}' на позиции {match.start()}-{match.end()}")

def demonstrate_metacharacters():
    """Демонстрация метасимволов"""
    print("\n=== Метасимволы ===")
    
    test_strings = [
        "hello",
        "Hello", 
        "python123",
        "test@email.com",
        "line1\nline2"
    ]
    
    patterns = {
        r'.': "Любой символ (кроме \\n)",
        r'^[Hh]': "Начинается с H или h", 
        r'com$': "Заканчивается на 'com'",
        r'\d+': "Одна или более цифр",
        r'\w+': "Одно или более буквенно-цифровых символов",
        r'\S+@\S+': "Простой паттерн email"
    }
    
    for pattern, description in patterns.items():
        print(f"\nПаттерн: {pattern} ({description})")
        for text in test_strings:
            match = re.search(pattern, text)
            result = match.group() if match else "не найдено"
            print(f"   '{text}' -> {result}")

def demonstrate_quantifiers():
    """Демонстрация квантификаторов"""
    print("\n=== Квантификаторы ===")
    
    text = "a aa aaa aaaa aaaaa"
    
    quantifiers = {
        r'a': "Точно 'a'",
        r'a*': "0 или более 'a'",
        r'a+': "1 или более 'a'", 
        r'a?': "0 или 1 'a'",
        r'a{3}': "Точно 3 'a'",
        r'a{2,4}': "От 2 до 4 'a'",
        r'a{3,}': "3 или более 'a'"
    }
    
    for pattern, description in quantifiers.items():
        matches = re.findall(pattern, text)
        print(f"{pattern:8} ({description:15}) -> {matches}")

def demonstrate_character_classes():
    """Демонстрация символьных классов"""
    print("\n=== Символьные классы ===")
    
    text = "Hello World! 123 test@example.com"
    
    classes = {
        r'[aeiou]': "Гласные буквы",
        r'[^aeiou]': "НЕ гласные буквы",
        r'[a-z]': "Строчные латинские буквы",
        r'[A-Z]': "Заглавные латинские буквы",
        r'[0-9]': "Цифры",
        r'[a-zA-Z0-9]': "Буквы и цифры",
        r'\d': "Цифры (\\d)",
        r'\w': "Буквы, цифры, подчёркивание (\\w)",
        r'\s': "Пробельные символы (\\s)"
    }
    
    for pattern, description in classes.items():
        matches = re.findall(pattern, text)
        print(f"{pattern:15} ({description:30}) -> {matches[:10]}")  # Показываем первые 10

def demonstrate_anchors():
    """Демонстрация якорей"""
    print("\n=== Якоря ===")
    
    lines = [
        "python programming",
        "learn python today", 
        "python",
        "programming python"
    ]
    
    patterns = {
        r'^python': "Начинается с 'python'",
        r'python$': "Заканчивается на 'python'",
        r'^python$': "Строка точно равна 'python'",
        r'\bpython\b': "Слово 'python' целиком"
    }
    
    for pattern, description in patterns.items():
        print(f"\nПаттерн: {pattern} ({description})")
        for line in lines:
            match = re.search(pattern, line)
            result = "✓" if match else "✗"
            print(f"   '{line}' -> {result}")

def demonstrate_flags():
    """Демонстрация флагов"""
    print("\n=== Флаги ===")
    
    text = """Hello World
    PYTHON programming
    Test Email: USER@EXAMPLE.COM"""
    
    # re.IGNORECASE - игнорирование регистра
    pattern = r'python'
    normal_match = re.findall(pattern, text)
    ignore_case_match = re.findall(pattern, text, re.IGNORECASE)
    
    print(f"Паттерн '{pattern}' без флагов: {normal_match}")
    print(f"Паттерн '{pattern}' с re.IGNORECASE: {ignore_case_match}")
    
    # re.MULTILINE - многострочный режим
    multiline_pattern = r'^[A-Z]'
    normal_multiline = re.findall(multiline_pattern, text)
    multiline_flag = re.findall(multiline_pattern, text, re.MULTILINE)
    
    print(f"\nПаттерн '{multiline_pattern}' без флагов: {normal_multiline}")
    print(f"Паттерн '{multiline_pattern}' с re.MULTILINE: {multiline_flag}")
    
    # re.DOTALL - точка включает перевод строки
    dotall_pattern = r'Hello.*COM'
    normal_dotall = re.findall(dotall_pattern, text)
    dotall_flag = re.findall(dotall_pattern, text, re.DOTALL)
    
    print(f"\nПаттерн '{dotall_pattern}' без флагов: {normal_dotall}")
    print(f"Паттерн '{dotall_pattern}' с re.DOTALL: {dotall_flag}")

def demonstrate_compilation():
    """Демонстрация компиляции паттернов"""
    print("\n=== Компиляция паттернов ===")
    
    # Компилируем паттерн для многократного использования
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    emails = [
        "user@example.com",
        "test.email+tag@domain.co.uk", 
        "invalid.email",
        "another@test.org"
    ]
    
    print("Поиск email адресов с скомпилированным паттерном:")
    for email in emails:
        match = email_pattern.search(email)
        result = "валидный" if match else "невалидный"
        print(f"   {email:30} -> {result}")
    
    # Преимущества компиляции
    print("\nПреимущества компиляции паттернов:")
    advantages = [
        "1. Повышение производительности при многократном использовании",
        "2. Раннее обнаружение синтаксических ошибок в паттерне",
        "3. Возможность задать флаги один раз",
        "4. Более читаемый код при сложных паттернах"
    ]
    for advantage in advantages:
        print(f"   {advantage}")

def demonstrate_practical_examples():
    """Практические примеры использования regex"""
    print("\n=== Практические примеры ===")
    
    # Извлечение информации из текста
    log_entry = "2023-12-07 10:30:45 [ERROR] User 'john_doe' failed to login from IP 192.168.1.100"
    
    # Извлекаем компоненты лога
    log_pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) \[(\w+)\] User \'(\w+)\' .* IP (\d+\.\d+\.\d+\.\d+)'
    match = re.search(log_pattern, log_entry)
    
    if match:
        date, time, level, user, ip = match.groups()
        print(f"Анализ лог-записи:")
        print(f"   Дата: {date}")
        print(f"   Время: {time}")
        print(f"   Уровень: {level}")
        print(f"   Пользователь: {user}")
        print(f"   IP адрес: {ip}")
    
    # Валидация данных
    print(f"\nВалидация различных форматов:")
    
    validators = {
        'телефон': r'^\+?[78][-.\s]?\(?9\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}$',
        'email': r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$',
        'пароль': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    }
    
    test_data = {
        'телефон': ['+79123456789', '8-912-345-67-89', '123456'],
        'email': ['user@example.com', 'test.email@domain.co.uk', 'invalid.email'],
        'пароль': ['StrongPass123!', 'weakpass', 'Strong123!']
    }
    
    for data_type, pattern in validators.items():
        print(f"\n{data_type.capitalize()}:")
        for value in test_data[data_type]:
            is_valid = bool(re.match(pattern, value))
            status = "✓" if is_valid else "✗"
            print(f"   {value:20} -> {status}")

def demonstrate_common_mistakes():
    """Демонстрация распространённых ошибок"""
    print("\n=== Распространённые ошибки ===")
    
    # Ошибка 1: Забыть экранировать специальные символы
    text = "Price: $10.50"
    
    wrong_pattern = r'$10.50'  # Неправильно: $ и . имеют специальное значение
    correct_pattern = r'\$10\.50'  # Правильно: экранированы $ и .
    
    print(f"Текст: '{text}'")
    print(f"Неправильный паттерн '{wrong_pattern}': {bool(re.search(wrong_pattern, text))}")
    print(f"Правильный паттерн '{correct_pattern}': {bool(re.search(correct_pattern, text))}")
    
    # Ошибка 2: Жадные квантификаторы
    html = '<div>content</div><span>more</span>'
    
    greedy_pattern = r'<.*>'  # Жадный - захватит всё от первого < до последнего >
    non_greedy_pattern = r'<.*?>'  # Ленивый - захватит минимально возможное
    
    print(f"\nHTML: '{html}'")
    print(f"Жадный паттерн '{greedy_pattern}': {re.findall(greedy_pattern, html)}")
    print(f"Ленивый паттерн '{non_greedy_pattern}': {re.findall(non_greedy_pattern, html)}")
    
    # Ошибка 3: Не использовать raw strings
    path = r"C:\new\folder\test.txt"
    
    # Без raw string (может быть проблематично)
    wrong_search = "\\new\\"
    # С raw string (рекомендуется)
    correct_search = r"\\new\\"
    
    print(f"\nПуть: '{path}'")
    print(f"Рекомендуется использовать raw strings для regex паттернов")

def demonstrate_performance_tips():
    """Советы по производительности"""
    print("\n=== Советы по производительности ===")
    
    import time
    
    # Компиляция vs не компиляция
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    compiled_pattern = re.compile(pattern)
    
    test_text = "Contact us: info@company.com, support@example.org, sales@test.net" * 1000
    
    # Тест без компиляции
    start_time = time.perf_counter()
    for _ in range(100):
        re.findall(pattern, test_text)
    non_compiled_time = time.perf_counter() - start_time
    
    # Тест с компиляцией
    start_time = time.perf_counter()
    for _ in range(100):
        compiled_pattern.findall(test_text)
    compiled_time = time.perf_counter() - start_time
    
    print(f"Время без компиляции: {non_compiled_time:.4f} сек")
    print(f"Время с компиляцией: {compiled_time:.4f} сек")
    print(f"Ускорение: {non_compiled_time / compiled_time:.2f}x")
    
    print("\nСоветы по оптимизации:")
    tips = [
        "1. Компилируйте паттерны при многократном использовании",
        "2. Используйте ленивые квантификаторы (*?, +?) когда это возможно",
        "3. Ставьте наиболее селективные части паттерна в начало",
        "4. Избегайте захватывающих групп, если они не нужны",
        "5. Используйте \A и \Z вместо ^ и $ для строгой проверки",
        "6. Тестируйте производительность на реальных данных"
    ]
    for tip in tips:
        print(f"   {tip}")

if __name__ == "__main__":
    print("Основы регулярных выражений в Python")
    print("=" * 50)
    
    demonstrate_basic_functions()
    demonstrate_metacharacters()
    demonstrate_quantifiers()
    demonstrate_character_classes()
    demonstrate_anchors()
    demonstrate_flags()
    demonstrate_compilation()
    demonstrate_practical_examples()
    demonstrate_common_mistakes()
    demonstrate_performance_tips()
    
    print("\n=== Шпаргалка по regex ===")
    cheatsheet = {
        "Метасимволы": ". ^ $ * + ? { } [ ] \\ | ( )",
        "Квантификаторы": "* (0+), + (1+), ? (0|1), {n}, {n,}, {n,m}",
        "Якоря": "^ (начало), $ (конец), \\b (граница слова)",
        "Классы": "\\d (цифры), \\w (слово), \\s (пробел), [abc], [^abc]",
        "Группы": "() (захват), (?:) (без захвата), (?P<name>) (именованная)",
        "Флаги": "re.I (игнорировать регистр), re.M (многострочный), re.S (точка включает \\n)"
    }
    
    for category, patterns in cheatsheet.items():
        print(f"{category}: {patterns}")
    
    print("\n=== Полезные ресурсы ===")
    resources = [
        "regex101.com - тестирование и объяснение regex",
        "regexr.com - интерактивный редактор",
        "docs.python.org/3/library/re.html - официальная документация",
        "regexone.com - интерактивный учебник"
    ]
    for resource in resources:
        print(f"   {resource}") 