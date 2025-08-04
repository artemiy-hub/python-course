# Использование with для работы с файлами
with open('context.txt', 'w') as f:
    f.write('Контекстный менеджер!')

with open('context.txt') as f:
    for line in f:
        print(line.strip()) 