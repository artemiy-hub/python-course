x = int(input('Введите число: '))
if x > 0:
    print('Положительное')
elif x < 0:
    print('Отрицательное')
else:
    print('Ноль')

print('--- while ---')
n = 5
while n > 0:
    print(n)
    n -= 1
print('Старт!')

print('--- for ---')
for i in range(3):
    print('Итерация', i)

print('--- break, continue ---')
for i in range(5):
    if i == 2:
        continue
    if i == 4:
        break
    print(i)
else:
    print('Цикл завершён')

if True:
    pass 