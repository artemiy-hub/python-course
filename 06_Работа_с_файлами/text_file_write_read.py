# Запись и чтение текстового файла
with open('example.txt', 'w', encoding='utf-8') as f:
    f.write('Привет, файл!')

with open('example.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    print(text) 