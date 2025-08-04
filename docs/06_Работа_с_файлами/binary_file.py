# Работа с бинарными файлами
with open('bytes.bin', 'wb') as f:
    f.write(b'\x01\x02\x03')

with open('bytes.bin', 'rb') as f:
    data = f.read()
    print(data) 