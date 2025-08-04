# Итоговые тесты Python
def test_basic_types():
    """Тест базовых типов данных"""
    assert type(42) == int
    assert type(3.14) == float
    assert type("hello") == str
    assert type(True) == bool
    print("✓ Тест базовых типов пройден")

def test_list_operations():
    """Тест операций со списками"""
    lst = [1, 2, 3]
    lst.append(4)
    assert lst == [1, 2, 3, 4]
    
    lst.pop()
    assert lst == [1, 2, 3]
    print("✓ Тест списков пройден")

def test_dict_operations():
    """Тест операций со словарями"""
    d = {"a": 1, "b": 2}
    d["c"] = 3
    assert d == {"a": 1, "b": 2, "c": 3}
    
    assert "a" in d
    assert d.get("d", 0) == 0
    print("✓ Тест словарей пройден")

def test_functions():
    """Тест функций"""
    def square(x):
        return x ** 2
    
    assert square(3) == 9
    assert square(0) == 0
    print("✓ Тест функций пройден")

def test_classes():
    """Тест классов"""
    class Person:
        def __init__(self, name):
            self.name = name
        def greet(self):
            return f"Hello, {self.name}"
    
    p = Person("Alice")
    assert p.name == "Alice"
    assert p.greet() == "Hello, Alice"
    print("✓ Тест классов пройден")

def test_exceptions():
    """Тест исключений"""
    try:
        result = 10 / 0
        assert False, "Should have raised ZeroDivisionError"
    except ZeroDivisionError:
        pass
    print("✓ Тест исключений пройден")

def run_all_tests():
    """Запуск всех тестов"""
    print("Запуск итоговых тестов...")
    
    test_basic_types()
    test_list_operations()
    test_dict_operations()
    test_functions()
    test_classes()
    test_exceptions()
    
    print("\n🎉 Все тесты пройдены! Поздравляем с изучением Python!")

if __name__ == "__main__":
    run_all_tests() 