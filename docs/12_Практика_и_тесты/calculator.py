# Калькулятор - практическое задание
def calculator():
    try:
        a = float(input("Введите первое число: "))
        operation = input("Введите операцию (+, -, *, /): ")
        b = float(input("Введите второе число: "))
        
        if operation == '+':
            result = a + b
        elif operation == '-':
            result = a - b
        elif operation == '*':
            result = a * b
        elif operation == '/':
            if b == 0:
                return "Ошибка: деление на ноль!"
            result = a / b
        else:
            return "Ошибка: неизвестная операция!"
        
        return f"{a} {operation} {b} = {result}"
    
    except ValueError:
        return "Ошибка: введите корректные числа!"

if __name__ == "__main__":
    print(calculator()) 