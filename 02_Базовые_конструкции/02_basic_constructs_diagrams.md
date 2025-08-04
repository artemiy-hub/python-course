# Диаграммы: Базовые конструкции Python

## 🔄 Типы данных и их иерархия

```mermaid
graph TD
    A[Python Objects] --> B[Immutable Types]
    A --> C[Mutable Types]
    
    B --> D[Numbers]
    B --> E[Strings]
    B --> F[Tuples]
    B --> G[Frozensets]
    B --> H[Bytes]
    
    C --> I[Lists]
    C --> J[Dictionaries]
    C --> K[Sets]
    C --> L[Bytearrays]
    
    D --> D1[int]
    D --> D2[float]
    D --> D3[complex]
    D --> D4[bool]
    
    style B fill:#e8f5e8
    style C fill:#ffeaa7
    style D1 fill:#74b9ff
    style D2 fill:#74b9ff
    style D3 fill:#74b9ff
    style D4 fill:#fd79a8
```

## 🔄 Жизненный цикл переменной

```mermaid
stateDiagram-v2
    [*] --> Declaration: Объявление переменной
    Declaration --> Assignment: Присваивание значения
    Assignment --> Usage: Использование
    Usage --> Reassignment: Переприсваивание
    Usage --> Access: Доступ к значению
    Reassignment --> Usage
    Access --> Usage
    Usage --> Deletion: del variable
    Deletion --> [*]
    
    note right of Assignment
        x = 42
        Python создает объект
        и связывает имя с ним
    end note
    
    note right of Reassignment
        x = "hello"
        Создается новый объект,
        старая связь удаляется
    end note
```

## 🧮 Операторы и их приоритет

```mermaid
graph TD
    A[Приоритет операторов<br/>↓ по убыванию] --> B["() [] {} - группировка"]
    B --> C["** - возведение в степень"]
    C --> D["+x -x ~x - унарные операторы"]
    D --> E["* / // % - умножение, деление"]
    E --> F["+ - - сложение, вычитание"]
    F --> G["<< >> - битовые сдвиги"]
    G --> H["& - битовое И"]
    H --> I["^ - битовое исключающее ИЛИ"]
    I --> J["| - битовое ИЛИ"]
    J --> K["== != < <= > >= is in - сравнения"]
    K --> L["not - логическое НЕ"]
    L --> M["and - логическое И"]
    M --> N["or - логическое ИЛИ"]
    
    style A fill:#ff7675
    style N fill:#00b894
```

## 🎯 Поток выполнения условных конструкций

```mermaid
flowchart TD
    A[Начало] --> B{Условие 1}
    B -->|True| C[Выполнить блок if]
    B -->|False| D{Условие 2}
    D -->|True| E[Выполнить блок elif]
    D -->|False| F{Есть ещё elif?}
    F -->|Да| G{Следующее условие}
    F -->|Нет| H[Выполнить блок else]
    G -->|True| I[Выполнить блок elif]
    G -->|False| F
    
    C --> J[Продолжить выполнение]
    E --> J
    I --> J
    H --> J
    J --> K[Конец]
    
    style B fill:#74b9ff
    style D fill:#74b9ff
    style G fill:#74b9ff
    style C fill:#00b894
    style E fill:#00b894
    style H fill:#fdcb6e
    style I fill:#00b894
```

## 🔄 Виды циклов в Python

```mermaid
graph LR
    A[Циклы в Python] --> B[for цикл]
    A --> C[while цикл]
    
    B --> B1[Итерация по последовательности]
    B --> B2["range()"]
    B --> B3["enumerate()"]
    B --> B4["zip()"]
    
    C --> C1[С предусловием]
    C --> C2[Бесконечный цикл]
    C --> C3[С флагом]
    
    B1 --> B1a["for item in items:"]
    B2 --> B2a["for i in range(10):"]
    B3 --> B3a["for i, item in enumerate(items):"]
    B4 --> B4a["for a, b in zip(list1, list2):"]
    
    C1 --> C1a["while condition:"]
    C2 --> C2a["while True:"]
    C3 --> C3a["while not flag:"]
    
    style B fill:#00b894
    style C fill:#74b9ff
```

## 🔄 Управление циклами

```mermaid
stateDiagram-v2
    [*] --> LoopStart: Начало цикла
    LoopStart --> Condition: Проверка условия
    Condition --> LoopBody: condition = True
    Condition --> LoopEnd: condition = False
    
    LoopBody --> Continue: continue statement
    LoopBody --> Break: break statement
    LoopBody --> Normal: обычное выполнение
    
    Continue --> Condition: Переход к следующей итерации
    Break --> LoopEnd: Выход из цикла
    Normal --> Condition: Переход к следующей итерации
    
    LoopEnd --> ElseBlock: else блок (если есть)
    LoopEnd --> End: Конец (если нет else)
    ElseBlock --> End
    Break --> End: else блок пропускается
    End --> [*]
    
    note right of Break
        break завершает цикл
        и пропускает else блок
    end note
    
    note right of Continue
        continue пропускает
        оставшуюся часть итерации
    end note
```

## 📊 Область видимости переменных (LEGB)

```mermaid
graph TB
    subgraph "Built-in Scope"
        B["Built-in функции\nprint, len, str, etc."]
    end
    
    subgraph "Global Scope"
        G["Глобальные переменные\nx = 'global'"]
    end
    
    subgraph "Enclosing Scope"
        E["Переменные внешней функции\ndef outer(): y = 'enclosing'"]
    end
    
    subgraph "Local Scope"
        L["Локальные переменные\ndef inner(): z = 'local'"]
    end
    
    L -.->|поиск| E
    E -.->|поиск| G
    G -.->|поиск| B
    
    style L fill:#ff7675
    style E fill:#fdcb6e
    style G fill:#00b894
    style B fill:#74b9ff
```

## 🔄 Преобразования типов данных

```mermaid
graph TD
    A[Исходный тип] --> B{Целевой тип}
    
    B -->|"int()"| C[Целое число]
    B -->|"float()"| D[Число с плавающей точкой]
    B -->|"str()"| E[Строка]
    B -->|"bool()"| F[Логическое значение]
    B -->|"list()"| G[Список]
    B -->|"tuple()"| H[Кортеж]
    B -->|"set()"| I[Множество]
    
    C --> C1["int('42') → 42\nint(3.14) → 3\nint(True) → 1"]
    D --> D1["float('3.14') → 3.14\nfloat(42) → 42.0\nfloat(True) → 1.0"]
    E --> E1["str(42) → '42'\nstr(3.14) → '3.14'\nstr(True) → 'True'"]
    F --> F1["bool(1) → True\nbool(0) → False\nbool('text') → True\nbool('') → False"]
    
    style C fill:#74b9ff
    style D fill:#00b894
    style E fill:#fdcb6e
    style F fill:#fd79a8
```

## 🎮 Логические операции и короткое замыкание

```mermaid
flowchart TD
    A[Выражение A and B] --> B{A истинно?}
    B -->|False| C[Результат: A<br/>B не вычисляется]
    B -->|True| D[Вычислить B]
    D --> E[Результат: B]
    
    F[Выражение A or B] --> G{A истинно?}
    G -->|True| H[Результат: A<br/>B не вычисляется]
    G -->|False| I[Вычислить B]
    I --> J[Результат: B]
    
    style C fill:#ff7675
    style E fill:#00b894
    style H fill:#00b894
    style J fill:#ff7675
```

## 🔄 Обработка пользовательского ввода

```mermaid
sequenceDiagram
    participant U as Пользователь
    participant P as Программа
    participant M as Память
    
    P->>U: Вывод приглашения input()
    U->>P: Ввод данных (строка)
    P->>P: Проверка типа данных
    
    alt Требуется число
        P->>P: int() или float()
        alt Успешное преобразование
            P->>M: Сохранить число
        else Ошибка преобразования
            P->>U: Сообщение об ошибке
            P->>U: Повторный запрос
        end
    else Требуется строка
        P->>M: Сохранить строку как есть
    end
    
    P->>P: Продолжить выполнение
```

## 🎯 Тернарный оператор

```mermaid
graph LR
    A[Условие] --> B{True/False}
    B -->|True| C[Значение если True]
    B -->|False| D[Значение если False]
    
    E["result = value_if_true if condition else value_if_false"]
    
    F["Примеры:<br/>status = 'adult' if age >= 18 else 'child'<br/>max_val = a if a > b else b<br/>sign = 'positive' if x > 0 else 'negative' if x < 0 else 'zero'"]
    
    style A fill:#74b9ff
    style C fill:#00b894
    style D fill:#ff7675
    style E fill:#fdcb6e
```

## 🔄 Цикл for с различными итерируемыми объектами

```mermaid
mindmap
  root((for цикл))
    Строки
      for char in Python
      for char in text.split
    Списки
      for item in list
      for i, item in enumerate
    Словари
      for key in dict.keys
      for value in dict.values
      for key, value in dict.items
    range
      for i in range(10)
      for i in range(1, 10, 2)
    Файлы
      for line in file
    Множества
      for item in set
    Кортежи
      for item in tuple
    zip
      for a, b in zip
```

## 📊 Операции со строками

```mermaid
graph TD
    A[Строковые операции] --> B[Создание]
    A --> C[Изменение]
    A --> D[Поиск]
    A --> E[Проверка]
    A --> F[Разделение]
    
    B --> B1[Одинарные кавычки]
    B --> B2[Двойные кавычки]
    B --> B3[Многострочные строки]
    B --> B4[f-строки]
    
    C --> C1[upper, lower]
    C --> C2[strip, replace]
    C --> C3[title, capitalize]
    
    D --> D1[find, index]
    D --> D2[count, startswith]
    D --> D3[endswith, in]
    
    E --> E1[isalpha, isdigit]
    E --> E2[isalnum, isspace]
    E --> E3[islower, isupper]
    
    F --> F1[split, rsplit]
    F --> F2[splitlines]
    F --> F3[join, partition]
    
    style B fill:#74b9ff
    style C fill:#00b894
    style D fill:#fdcb6e
    style E fill:#fd79a8
    style F fill:#a29bfe
```

## 🔄 Сравнение различных типов циклов

```mermaid
graph TB
    A[Когда использовать какой цикл?] --> B[Известно количество итераций]
    A --> C[Неизвестно количество итераций]
    A --> D[Итерация по коллекции]
    
    B --> B1["for i in range(n):<br/>    # выполнить n раз"]
    
    C --> C1["while condition:<br/>    # пока условие истинно<br/>    # обновить условие"]
    
    D --> D1["for item in collection:<br/>    # обработать каждый элемент"]
    
    E[Специальные случаи] --> E1["while True:<br/>    # бесконечный цикл<br/>    if condition: break"]
    E --> E2["for i, item in enumerate(items):<br/>    # нужны индекс и значение"]
    E --> E3["for a, b in zip(list1, list2):<br/>    # параллельная итерация"]
    
    style B1 fill:#74b9ff
    style C1 fill:#00b894
    style D1 fill:#fdcb6e
    style E1 fill:#ff7675
    style E2 fill:#a29bfe
    style E3 fill:#fd79a8
```

---

Эти диаграммы помогают визуализировать ключевые концепции базовых конструкций Python, включая типы данных, операторы, циклы, условия и область видимости переменных. 