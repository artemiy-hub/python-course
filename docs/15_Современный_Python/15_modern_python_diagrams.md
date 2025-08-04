# Диаграммы: Современный Python (3.8+)

## 🎯 Эволюция современного Python

### Timeline новых возможностей

```mermaid
timeline
    title Современные возможности Python
    
    section Python 3.8
        Walrus Operator : Assignment Expressions
        Positional-only params : def func(a, /, b)
        f-strings : Self-documenting expressions
        
    section Python 3.9
        Dictionary merge : dict1 | dict2
        Built-in generics : list[int] instead of List[int]
        str methods : removeprefix, removesuffix
        
    section Python 3.10
        Structural Pattern Matching : match/case statements
        Union operator : str | int instead of Union[str, int]
        Better error messages : More precise locations
        
    section Python 3.11
        Exception Groups : Multiple exceptions
        Task Groups : Async exception handling
        TOML support : tomllib module
        
    section Python 3.12
        f-string improvements : Nested quotes
        Buffer protocol : Performance improvements
        Type alias syntax : type Point = tuple[float, float]
```

## 🎯 Walrus Operator (:=)

### Применение в различных конструкциях

```mermaid
graph TD
    A[Walrus Operator :=] --> B[If Statements]
    A --> C[While Loops]
    A --> D[List Comprehensions]
    A --> E[Match/Case]
    
    B --> B1["if (n := len(data)) > 10:<br/>    process(n)"]
    B --> B2[Избегает повторных<br/>вычислений]
    
    C --> C1["while (line := file.readline()):<br/>    process(line)"]
    C --> C2[Чтение до EOF]
    
    D --> D1["[y for x in data<br/> if (y := func(x)) is not None]"]
    D --> D2[Сохраняет результат<br/>вычисления]
    
    E --> E1["match value:<br/>    case x if (n := len(x)) > 5:<br/>        handle_long(n)"]
    E --> E2[Захват в условии]
    
    style A fill:#e3f2fd
    style B1 fill:#c8e6c9
    style C1 fill:#c8e6c9
    style D1 fill:#c8e6c9
    style E1 fill:#c8e6c9
```

### Производительность и читаемость

```mermaid
graph LR
    A[Без Walrus] --> B[Повторные вычисления]
    A --> C[Дополнительные переменные]
    A --> D[Больше строк кода]
    
    E[С Walrus] --> F[Одно вычисление]
    E --> G[Инлайн присваивание]
    E --> H[Компактный код]
    
    B --> I[❌ Неэффективно]
    F --> J[✅ Эффективно]
    
    C --> K[❌ Загромождение]
    G --> L[✅ Чистота]
    
    style A fill:#ffcdd2
    style E fill:#c8e6c9
    style I fill:#ff5722
    style J fill:#4caf50
    style K fill:#ff5722
    style L fill:#4caf50
```

## 🔄 Structural Pattern Matching

### Архитектура match/case

```mermaid
graph TD
    A[match expression] --> B{Pattern Matching}
    
    B --> C[Value Patterns]
    B --> D[Sequence Patterns]
    B --> E[Mapping Patterns]
    B --> F[Class Patterns]
    B --> G[Guard Patterns]
    
    C --> C1["case 42:\ncase 'hello':\ncase True:"]
    
    D --> D1["case [x, y]:\ncase [x, *rest]:\ncase (a, b, c):"]
    
    E --> E1["case {'key': value}:\ncase {'a': x, **rest}:"]
    
    F --> F1["case Point(x, y):\ncase Person(name='John'):"]
    
    G --> G1["case x if x > 0:\ncase [x, y] if x == y:"]
    
    style A fill:#e3f2fd
    style B fill:#ffffcc
    style C1 fill:#fff3e0
    style D1 fill:#f3e5f5
    style E1 fill:#e8f5e8
    style F1 fill:#fce4ec
    style G1 fill:#e1f5fe
```

### Сравнение с if/elif

```mermaid
graph LR
    A[Traditional if/elif] --> B["Множественные isinstance()"]
    A --> C[Сложные условия]
    A --> D[Повторяющийся код]
    
    E[Pattern Matching] --> F[Деструктуризация]
    E --> G[Четкие паттерны]
    E --> H[Автоматическое связывание]
    
    B --> I[❌ Verbose]
    F --> J[✅ Concise]
    
    C --> K[❌ Hard to read]
    G --> L[✅ Clear intent]
    
    D --> M[❌ DRY violation]
    H --> N[✅ DRY principle]
    
    style A fill:#ffcdd2
    style E fill:#c8e6c9
```

### Практические паттерны

```mermaid
graph TD
    A[Match/Case Patterns] --> B[HTTP Request Handling]
    A --> C[JSON API Processing]
    A --> D[State Machine]
    A --> E[Command Pattern]
    
    B --> B1["match request:<br/>    case {'method': 'GET', 'path': path}:<br/>    case {'method': 'POST', 'data': data}:"]
    
    C --> C1["match response:<br/>    case {'status': 'success', 'data': items}:<br/>    case {'status': 'error', 'message': msg}:"]
    
    D --> D1["match state:<br/>    case State.IDLE:<br/>    case State.PROCESSING:"]
    
    E --> E1["match command:<br/>    case SaveCommand(filename):<br/>    case LoadCommand(source):"]
    
    style A fill:#e3f2fd
    style B1 fill:#fff3e0
    style C1 fill:#f3e5f5
    style D1 fill:#e8f5e8
    style E1 fill:#fce4ec
```

## 📍 Positional-Only Parameters

### Синтаксис и применение

```mermaid
graph LR
    A["def func(a, b, /, c, d, *, e, f)"] --> B["Positional-only\na, b"]
    A --> C["Normal\nc, d"]
    A --> D["Keyword-only\ne, f"]
    
    B --> B1["func(1, 2, ...)"]
    B --> B2["❌ func(a=1, b=2)"]
    
    C --> C1["func(..., 3, 4, ...)"]
    C --> C2["func(..., c=3, d=4, ...)"]
    
    D --> D1["func(..., e=5, f=6)"]
    D --> D2["❌ func(..., 5, 6)"]
    
    style A fill:#e3f2fd
    style B1 fill:#c8e6c9
    style B2 fill:#ffcdd2
    style C1 fill:#c8e6c9
    style C2 fill:#c8e6c9
    style D1 fill:#c8e6c9
    style D2 fill:#ffcdd2
```

### Преимущества для API дизайна

```mermaid
graph TD
    A[Positional-Only Benefits] --> B[API Stability]
    A --> C[Performance]
    A --> D[Clarity]
    
    B --> B1[Можно переименовать<br/>параметры]
    B --> B2[Backward compatibility]
    B --> B3[Внутренние изменения<br/>не влияют на вызовы]
    
    C --> C1[Меньше проверок<br/>аргументов]
    C --> C2[Быстрее парсинг]
    C --> C3[Оптимизация<br/>интерпретатора]
    
    D --> D1[Четкое разделение<br/>типов параметров]
    D --> D2[Явные намерения<br/>разработчика]
    D --> D3[Лучшая документация]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

## 📝 Улучшения f-strings

### Новые возможности отладки

```mermaid
graph TD
    A[f-string Improvements] --> B["Debug Expressions\nf'{variable=}'"]
    A --> C["Nested Quotes\nf'{'nested quotes'}'"]
    A --> D[Multiline Support]
    A --> E[Performance Boost]
    
    B --> B1["Автоматический вывод\nимени переменной"]
    B --> B2[Удобная отладка]
    
    C --> C1["Сложные строки\nвнутри f-strings"]
    C --> C2[JSON в f-strings]
    
    D --> D1["Читаемые длинные\nформатированные строки"]
    
    E --> E1["Быстрее чем .format()"]
    E --> E2[Compile-time оптимизация]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

## 🔧 Операторы слияния словарей

### Dictionary merge operators

```mermaid
graph LR
    A[Dictionary Operations] --> B["Merge |"]
    A --> C["Update |="]
    A --> D[Old Methods]
    
    B --> B1["dict1 | dict2"]
    B --> B2[Non-destructive]
    B --> B3[Returns new dict]
    
    C --> C1["dict1 |= dict2"]
    C --> C2[In-place update]
    C --> C3[Modifies dict1]
    
    D --> D1["dict.update()"]
    D --> D2["{**dict1, **dict2}"]
    D --> D3[Более verbose]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#ffcdd2
```

### Производительность операций

```mermaid
graph TD
    A[Performance Comparison] --> B["Small Dicts\n< 100 items"]
    A --> C["Medium Dicts\n100-1000 items"]
    A --> D["Large Dicts\n> 1000 items"]
    
    B --> B1["| operator: ⚡⚡⚡"]
    B --> B2["**unpacking: ⚡⚡"]
    B --> B3["update(): ⚡"]
    
    C --> C1["| operator: ⚡⚡⚡"]
    C --> C2["**unpacking: ⚡⚡"]
    C --> C3["update(): ⚡⚡"]
    
    D --> D1["| operator: ⚡⚡⚡"]
    D --> D2["**unpacking: ⚡"]
    D --> D3["update(): ⚡⚡⚡"]
    
    style A fill:#e3f2fd
    style B1 fill:#4caf50
    style C1 fill:#4caf50
    style D1 fill:#4caf50
    style D3 fill:#4caf50
```

## 🏗️ Новые встроенные generics

### Упрощение типизации

```mermaid
graph LR
    A[Built-in Generics] --> B[Python 3.8]
    A --> C[Python 3.9+]
    
    B --> B1["from typing import List"]
    B --> B2["List[int]"]
    B --> B3["Dict[str, int]"]
    B --> B4["Tuple[int, ...]"]
    
    C --> C1[Без импортов]
    C --> C2["list[int]"]
    C --> C3["dict[str, int]"]
    C --> C4["tuple[int, ...]"]
    
    B1 --> D[❌ Требует импорт]
    C1 --> E[✅ Встроено]
    
    style A fill:#e3f2fd
    style B fill:#ffcdd2
    style C fill:#c8e6c9
    style D fill:#ff5722
    style E fill:#4caf50
```

## ⚡ functools улучшения

### Новые возможности functools

```mermaid
graph TD
    A[functools Enhancements] --> B[cache decorator]
    A --> C[cached_property]
    A --> D[singledispatch improvements]
    A --> E[partial improvements]
    
    B --> B1["@cache\nПростое кэширование"]
    B --> B2[LRU без размера]
    B --> B3["Быстрее lru_cache()"]
    
    C --> C1[Property + caching]
    C --> C2[Computed once]
    C --> C3[Memory efficient]
    
    D --> D1["Generic function\noverloading"]
    D --> D2[Type-based dispatch]
    D --> D3["register() method"]
    
    E --> E1["Better keyword\nhandling"]
    E --> E2[More efficient]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

## 🎯 Практические применения

### Современные паттерны

```mermaid
graph TD
    A[Modern Python Patterns] --> B[Data Processing]
    A --> C[API Development]
    A --> D[Configuration]
    A --> E[Error Handling]
    
    B --> B1[Walrus in comprehensions]
    B --> B2[Match for data validation]
    B --> B3[Built-in generics]
    
    C --> C1[Match for routing]
    C --> C2[Positional-only params]
    C --> C3["Union types with |"]
    
    D --> D1[Dict merge operators]
    D --> D2[f-string debugging]
    D --> D3[Pattern matching config]
    
    E --> E1[Match for exception types]
    E --> E2[Walrus in conditions]
    E --> E3[Better error messages]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Миграция на современный Python

```mermaid
graph LR
    A[Legacy Code] --> B[Assessment]
    B --> C[Gradual Migration]
    C --> D[Modern Python]
    
    A --> A1[Old patterns]
    A --> A2[Verbose syntax]
    A --> A3[Performance issues]
    
    B --> B1[Identify opportunities]
    B --> B2[Check compatibility]
    B --> B3[Plan refactoring]
    
    C --> C1[Replace if/elif with match]
    C --> C2[Use walrus operator]
    C --> C3[Modern type hints]
    
    D --> D1[✅ Cleaner code]
    D --> D2[✅ Better performance]
    D --> D3[✅ Modern practices]
    
    style A fill:#ffcdd2
    style D fill:#c8e6c9
```

Эти диаграммы показывают все современные возможности Python и их практическое применение. 