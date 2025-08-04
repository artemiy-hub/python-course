# Запись списка чисел в файл и построчное чтение
numbers = [1, 2, 3, 4, 5]
with open('numbers.txt', 'w') as f:
    for n in numbers:
        f.write(f"{n}\n")

with open('numbers.txt') as f:
    for line in f:
        print(int(line.strip())) 