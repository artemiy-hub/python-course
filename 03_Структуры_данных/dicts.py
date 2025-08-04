# Примеры работы со словарями
d = {"имя": "Иван", "возраст": 30}
print(d["имя"])
d["город"] = "Москва"
print(d)

# Итерация по словарю
for key, value in d.items():
    print(key, value)

# Методы словарей
print(d.keys())
print(d.values())
print(d.get("имя", "не найдено"))
print(d.get("телефон", "не найдено")) 