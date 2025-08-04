# Примеры определения и вызова функций
def greet(name):
    print(f"Привет, {name}!")

greet("Анна")

def add(a, b):
    return a + b

result = add(2, 3)
print(result)

def power(base, exponent=2):
    return base ** exponent

print(power(3))  # 9
print(power(3, 3))  # 27 