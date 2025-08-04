# Собственный модуль
def hello():
    print("Hello from mymodule!")

def add(a, b):
    return a + b

PI = 3.14159

if __name__ == "__main__":
    print("Этот модуль запущен напрямую")
    hello()
else:
    print("Этот модуль импортирован") 