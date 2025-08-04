# Генератор паролей - мини-проект
import random
import string

def generate_password(length=12, use_uppercase=True, use_lowercase=True, 
                     use_digits=True, use_symbols=True):
    """
    Генерирует случайный пароль с заданными параметрами.
    """
    characters = ""
    
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not characters:
        return "Ошибка: выберите хотя бы один тип символов"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_password_strength(password):
    """
    Оценивает силу пароля.
    """
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Пароль должен быть не менее 8 символов")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Добавьте строчные буквы")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Добавьте заглавные буквы")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Добавьте цифры")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Добавьте специальные символы")
    
    if score <= 2:
        strength = "Слабый"
    elif score <= 3:
        strength = "Средний"
    else:
        strength = "Сильный"
    
    return strength, feedback

def main():
    while True:
        print("\n=== Генератор паролей ===")
        print("1. Сгенерировать пароль")
        print("2. Проверить силу пароля")
        print("3. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            try:
                length = int(input("Длина пароля (по умолчанию 12): ") or "12")
                use_upper = input("Использовать заглавные буквы? (y/n): ").lower() != 'n'
                use_lower = input("Использовать строчные буквы? (y/n): ").lower() != 'n'
                use_digits = input("Использовать цифры? (y/n): ").lower() != 'n'
                use_symbols = input("Использовать символы? (y/n): ").lower() != 'n'
                
                password = generate_password(length, use_upper, use_lower, 
                                           use_digits, use_symbols)
                print(f"\nСгенерированный пароль: {password}")
                
                strength, feedback = check_password_strength(password)
                print(f"Сила пароля: {strength}")
                
            except ValueError:
                print("Введите корректную длину пароля")
        
        elif choice == '2':
            password = input("Введите пароль для проверки: ")
            strength, feedback = check_password_strength(password)
            print(f"Сила пароля: {strength}")
            if feedback:
                print("Рекомендации:")
                for tip in feedback:
                    print(f"- {tip}")
        
        elif choice == '3':
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main() 