# Менеджер задач (ToDo) - мини-проект
class Task:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.completed = False
    
    def mark_completed(self):
        self.completed = True
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.title}: {self.description}"

class TaskManager:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, title, description=""):
        task = Task(title, description)
        self.tasks.append(task)
        print(f"Задача '{title}' добавлена")
    
    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            print(f"Задача '{self.tasks[index].title}' выполнена")
        else:
            print("Неверный номер задачи")
    
    def show_tasks(self):
        if not self.tasks:
            print("Нет задач")
            return
        
        for i, task in enumerate(self.tasks):
            print(f"{i + 1}. {task}")
    
    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            print(f"Задача '{removed.title}' удалена")
        else:
            print("Неверный номер задачи")

def main():
    tm = TaskManager()
    
    while True:
        print("\n=== Менеджер задач ===")
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Выполнить задачу")
        print("4. Удалить задачу")
        print("5. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            title = input("Название задачи: ")
            description = input("Описание (необязательно): ")
            tm.add_task(title, description)
        elif choice == '2':
            tm.show_tasks()
        elif choice == '3':
            tm.show_tasks()
            try:
                index = int(input("Номер задачи для выполнения: ")) - 1
                tm.complete_task(index)
            except ValueError:
                print("Введите корректный номер")
        elif choice == '4':
            tm.show_tasks()
            try:
                index = int(input("Номер задачи для удаления: ")) - 1
                tm.remove_task(index)
            except ValueError:
                print("Введите корректный номер")
        elif choice == '5':
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main() 