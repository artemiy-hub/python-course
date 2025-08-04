# Использование finally для закрытия файла
try:
    f = open('test.txt', 'w')
    f.write('Hello!')
finally:
    f.close()
    print('Файл закрыт') 