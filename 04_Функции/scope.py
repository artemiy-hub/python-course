# Примеры области видимости и замыканий
x = 5  # глобальная переменная

def outer():
    x = 10  # локальная переменная
    def inner():
        print(x)  # 10
    inner()
    print(x)  # 10

outer()
print(x)  # 5

# Замыкания
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15 