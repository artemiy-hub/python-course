# Различия в итераторах между Python 2 и 3

d = {"a": 1, "b": 2, "c": 3}

# Python 2:
# keys = d.keys()    # возвращает список
# values = d.values()  # возвращает список
# items = d.items()  # возвращает список

# Python 3:
keys = d.keys()      # возвращает dict_keys (итератор)
values = d.values()  # возвращает dict_values (итератор)
items = d.items()    # возвращает dict_items (итератор)

print(f"Ключи: {keys}, тип: {type(keys)}")
print(f"Значения: {values}, тип: {type(values)}")
print(f"Пары: {items}, тип: {type(items)}")

# Преобразование в список (если нужно):
keys_list = list(keys)
values_list = list(values)
items_list = list(items)

print(f"Ключи как список: {keys_list}")
print(f"Значения как список: {values_list}")
print(f"Пары как список: {items_list}")

# Range тоже изменился:
# Python 2: range(5) возвращает список
# Python 3: range(5) возвращает объект range
r = range(5)
print(f"Range: {r}, тип: {type(r)}")
print(f"Range как список: {list(r)}") 