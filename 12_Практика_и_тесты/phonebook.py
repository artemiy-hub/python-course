# Телефонная книга - практическое задание
class PhoneBook:
    def __init__(self):
        self.contacts = {}
    
    def add_contact(self, name, phone):
        self.contacts[name] = phone
        print(f"Контакт {name} добавлен")
    
    def find_contact(self, name):
        if name in self.contacts:
            return self.contacts[name]
        return None
    
    def remove_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            print(f"Контакт {name} удален")
        else:
            print(f"Контакт {name} не найден")
    
    def list_contacts(self):
        if not self.contacts:
            print("Контактов нет")
            return
        
        for name, phone in self.contacts.items():
            print(f"{name}: {phone}")

def main():
    pb = PhoneBook()
    
    while True:
        print("\n1. Добавить контакт")
        print("2. Найти контакт")
        print("3. Удалить контакт")
        print("4. Показать все контакты")
        print("5. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            name = input("Имя: ")
            phone = input("Телефон: ")
            pb.add_contact(name, phone)
        elif choice == '2':
            name = input("Имя для поиска: ")
            phone = pb.find_contact(name)
            if phone:
                print(f"{name}: {phone}")
            else:
                print("Контакт не найден")
        elif choice == '3':
            name = input("Имя для удаления: ")
            pb.remove_contact(name)
        elif choice == '4':
            pb.list_contacts()
        elif choice == '5':
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main() 