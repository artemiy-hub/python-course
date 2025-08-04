# Анализ байткода Python
import dis
import types

def simple_function(x):
    y = x + 1
    return y * 2

print("=== Байткод простой функции ===")
dis.dis(simple_function)

def complex_function(items):
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result

print("\n=== Байткод сложной функции ===")
dis.dis(complex_function)

# Создание функции из байткода
def original():
    return 42

print(f"\nОригинальная функция: {original()}")

# Получаем байткод
bytecode = original.__code__

# Создаём новую функцию с тем же байткодом
new_function = types.FunctionType(bytecode, globals())
print(f"Новая функция: {new_function()}")

# Анализ отдельных инструкций
print("\n=== Детальный анализ инструкций ===")
for instruction in dis.get_instructions(simple_function):
    print(f"{instruction.offset:4} {instruction.opname:20} {instruction.arg or '':10} {instruction.argval or ''}")

# Компиляция и дизассемблирование строки кода
code_string = "x = 5; y = x * 2; print(y)"
compiled_code = compile(code_string, "<string>", "exec")
print(f"\n=== Байткод скомпилированной строки ===")
dis.dis(compiled_code) 