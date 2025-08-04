# Примеры вложенных структур данных
matrix = [[1, 2, 3], [4, 5, 6]]
print(matrix[1][2])  # 6

dict_list = [{"id": 1}, {"id": 2}]
print(dict_list[0]["id"])

# Сложная структура
data = {
    "users": [
        {"name": "Анна", "age": 20},
        {"name": "Иван", "age": 22}
    ],
    "settings": {
        "theme": "dark",
        "language": "ru"
    }
}

print(data["users"][0]["name"])
print(data["settings"]["theme"]) 