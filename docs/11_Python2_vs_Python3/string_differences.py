# Различия в строках между Python 2 и 3

# Python 2:
# s = "байты"      # str (байты)
# u = u"текст"     # unicode (текст)

# Python 3:
s = "текст"        # str (Unicode по умолчанию)
b = b"байты"       # bytes (байты)

print(f"Строка: {s}, тип: {type(s)}")
print(f"Байты: {b}, тип: {type(b)}")

# Кодирование/декодирование:
text = "Привет"
encoded = text.encode('utf-8')  # str -> bytes
decoded = encoded.decode('utf-8')  # bytes -> str

print(f"Исходный текст: {text}")
print(f"Закодировано: {encoded}")
print(f"Декодировано: {decoded}")

# Работа с файлами:
with open('test_utf8.txt', 'w', encoding='utf-8') as f:
    f.write("Русский текст")

with open('test_utf8.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"Содержимое файла: {content}") 