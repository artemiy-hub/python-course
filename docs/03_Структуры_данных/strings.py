# Примеры работы со строками
s = "Привет, Python!"
print(s[0])        # 'П'
print(s[-1])       # '!'
print(s[2:7])      # 'ивет,'
print(len(s))      # 14
print(s.upper())   # 'ПРИВЕТ, PYTHON!'
print(s.replace("Python", "мир")) # 'Привет, мир!'

# Форматирование строк
name = "Анна"
age = 23
print(f"Меня зовут {name}, мне {age} года")
print("Меня зовут %s, мне %d года" % (name, age)) 