# Диаграммы: Функции в Python

## 🎯 Анатомия функции

```mermaid
graph TB
    subgraph "Python Function Structure"
        A[def keyword] --> B[function_name]
        B --> C[Parameters]
        C --> D[Colon :]
        D --> E[Docstring]
        E --> F[Function Body]
        F --> G[return Statement]
        
        C --> C1[Positional]
        C --> C2[Default Values] 
        C --> C3[*args]
        C --> C4[**kwargs]
        
        F --> F1[Local Variables]
        F --> F2[Logic/Computation]
        F --> F3[Function Calls]
    end
    
    style A fill:#74b9ff
    style E fill:#00b894
    style G fill:#fd79a8
```

## 🔄 Типы параметров и их порядок

```mermaid
flowchart LR
    A[Function Definition] --> B[Positional Parameters]
    B --> C[Default Parameters]
    C --> D[*args]
    D --> E[Keyword-only]
    E --> F[**kwargs]
    
    B1[pos1, pos2] -.-> B
    C1[param=default] -.-> C
    D1[*args] -.-> D
    E1[*, kwd_only] -.-> E
    F1[**kwargs] -.-> F
    
    style A fill:#74b9ff
    style D fill:#ffeaa7
    style F fill:#fd79a8
```

## 🌍 Область видимости (LEGB Rule)

```mermaid
graph TB
    subgraph "LEGB Scope Resolution"
        L[Local Scope<br/>Локальная область функции]
        E[Enclosing Scope<br/>Объемлющая область вложенных функций]
        G[Global Scope<br/>Глобальная область модуля]
        B[Built-in Scope<br/>Встроенная область Python]
        
        L --> E
        E --> G
        G --> B
        
        L1[x = 'local'] -.-> L
        E1[x = 'enclosing'] -.-> E
        G1[x = 'global'] -.-> G
        B1[len, print, str] -.-> B
    end
    
    style L fill:#fd79a8
    style E fill:#ffeaa7
    style G fill:#74b9ff
    style B fill:#e8f5e8
```

## 🎭 Жизненный цикл функции

```mermaid
stateDiagram-v2
    [*] --> Defined: def function_name()
    Defined --> Called: function_name()
    Called --> LocalScope: Создание локальной области
    LocalScope --> Execution: Выполнение тела функции
    Execution --> Return: return value
    Return --> Cleanup: Очистка локальной области
    Cleanup --> [*]: Возврат к вызывающему коду
    
    Execution --> Exception: raise Exception
    Exception --> Cleanup: Обработка исключения
    
    note right of LocalScope
        Создаются локальные переменные
        Связываются параметры
    end note
    
    note left of Cleanup
        Удаляются локальные переменные
        Освобождается память
    end note
```

## 🏗️ Архитектура замыкания

```mermaid
graph TB
    subgraph "Closure Architecture"
        A[Outer Function] --> B[Local Variables]
        A --> C[Inner Function]
        
        C --> D[Captures Variables]
        C --> E[Returned Function Object]
        
        D -.-> B
        E --> F[Maintains Reference]
        F -.-> B
        
        B --> B1[var1 = 'captured']
        B --> B2[var2 = 42]
        
        G[Function Call] --> E
        E --> H[Access to Captured Variables]
    end
    
    style A fill:#74b9ff
    style C fill:#00b894
    style E fill:#fd79a8
    style D fill:#ffeaa7
```

## 🎨 Паттерн декоратора

```mermaid
flowchart TD
    A[Original Function] --> B[Decorator Function]
    B --> C[Wrapper Function]
    C --> D[Enhanced Function]
    
    E[Before Logic] --> F[Call Original]
    F --> G[After Logic]
    
    C -.-> E
    F -.-> A
    G --> H[Return Result]
    
    I["@decorator\ndef function"] --> B
    
    style B fill:#74b9ff
    style C fill:#00b894
    style D fill:#fd79a8
```

## 🔄 Генератор vs Обычная функция

```mermaid
graph LR
    subgraph "Regular_Function"
        A1[def func] --> B1["return value<br/>(immediate)"]
        B1 --> C1["Function Ends<br/>(cleanup)"]
        C1 --> D1["Memory Cleaned<br/>(garbage collection)"]
    end
    
    subgraph "Generator_Function"
        A2[def func] --> B2["yield value<br/>(pause execution)"]
        B2 --> C2["Suspend State<br/>(save context)"]
        C2 --> D2["Resume on next<br/>(continue execution)"]
        D2 --> B2
        D2 --> E2["StopIteration<br/>(end generator)"]
    end
    
    style B1 fill:#e17055
    style B2 fill:#00b894
    style C2 fill:#ffeaa7
    style D2 fill:#74b9ff
    style E2 fill:#ff7675
```

## 📊 Сравнение способов передачи аргументов

```mermaid
quadrantChart
    title Function Arguments Analysis
    x-axis Simple --> Complex
    y-axis Low --> High_Flexibility
    
    quadrant-1 Advanced_Features
    quadrant-2 Over_Engineering
    quadrant-3 Basic_Usage
    quadrant-4 Practical_Choice
    
    Positional: [0.2, 0.3]
    Default: [0.4, 0.5]
    Named: [0.6, 0.7]
    args: [0.7, 0.8]
    kwargs: [0.9, 0.9]
```

## 🎯 Применение декораторов

```mermaid
mindmap
  root((Декораторы))
    Логирование
      @log_calls
      @debug
      @audit
    Кеширование
      @lru_cache
      @memoize
      @cache_result
    Авторизация
      @login_required
      @admin_only
      @permission_check
    Валидация
      @validate_types
      @check_params
      @sanitize_input
    Производительность
      @timer
      @retry
      @timeout
    Метапрограммирование
      @property
      @staticmethod
      @classmethod
```

## 🔄 Цепочка вызовов функций

```mermaid
sequenceDiagram
    participant Main
    participant FuncA
    participant FuncB
    participant FuncC
    
    Main->>FuncA: call func_a(x)
    activate FuncA
    
    FuncA->>FuncB: call func_b(y)
    activate FuncB
    
    FuncB->>FuncC: call func_c(z)
    activate FuncC
    
    FuncC-->>FuncB: return result_c
    deactivate FuncC
    
    FuncB-->>FuncA: return result_b
    deactivate FuncB
    
    FuncA-->>Main: return result_a
    deactivate FuncA
    
    Note over Main,FuncC: Call Stack: Main -> FuncA -> FuncB -> FuncC
```

## 🧠 Стратегии оптимизации функций

```mermaid
flowchart TD
    A[Функция требует оптимизации] --> B{Тип проблемы?}
    
    B -->|Медленные вычисления| C[Кеширование]
    B -->|Повторные вызовы| D[Мемоизация]
    B -->|Большие данные| E[Генераторы]
    B -->|Много параметров| F[Частичное применение]
    
    C --> C1["@lru_cache"]
    C --> C2[Ручное кеширование]
    
    D --> D1["functools.cache"]
    D --> D2[Словарь результатов]
    
    E --> E1["yield вместо return"]
    E --> E2[Ленивые вычисления]
    
    F --> F1["functools.partial"]
    F --> F2[Замыкания]
    
    style C fill:#00b894
    style D fill:#74b9ff
    style E fill:#ffeaa7
    style F fill:#fd79a8
```

## 🎪 Функции высшего порядка

```mermaid
graph TB
    subgraph "Higher-Order Functions"
        A[map] --> A1[Применяет функцию<br/>к каждому элементу]
        B[filter] --> B1[Фильтрует элементы<br/>по условию]
        C[reduce] --> C1[Сводит последовательность<br/>к одному значению]
        D[sorted] --> D1[Сортирует с помощью<br/>ключевой функции]
        
        E[Custom HOF] --> E1[Принимает функции<br/>как аргументы]
        E --> E2[Возвращает функции<br/>как результат]
    end
    
    F[lambda x: x*2] -.-> A
    G[lambda x: x>0] -.-> B
    H[lambda a,b: a+b] -.-> C
    I[lambda x: x.lower] -.-> D
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#ffeaa7
    style D fill:#fd79a8
```

## 📈 Производительность: Функции vs Методы vs Лямбды

```mermaid
graph TB
    subgraph "Performance Comparison"
        A[Regular Function] --> A1[def func_name]
        A1 --> A2[Fastest for<br/>complex logic]
        
        B[Method] --> B1[class.method]
        B1 --> B2[Slightly slower<br/>due to self lookup]
        
        C[Lambda] --> C1[lambda x: expr]
        C1 --> C2[Good for simple<br/>one-liners]
        
        D[Built-in] --> D1[map, filter, sum]
        D1 --> D2[Optimized C code<br/>Usually fastest]
        
        E[List Comprehension] --> E1[expr for x in iter]
        E1 --> E2[Often faster than<br/>map/filter]
    end
    
    style D2 fill:#00b894
    style E2 fill:#00b894
    style A2 fill:#74b9ff
```

## 🔄 Паттерны использования генераторов

```mermaid
journey
    title Жизненный цикл генератора
    section Создание
      Вызов функции: 5: Python
      Создание объекта-генератора: 4: Python
      Сохранение состояния: 3: Python
    section Выполнение
      Вызов next(): 5: Разработчик
      Выполнение до yield: 4: Python
      Возврат значения: 5: Python
      Приостановка: 3: Python
    section Завершение
      Достижение конца: 3: Python
      StopIteration: 2: Python
      Очистка ресурсов: 1: Python
```

## 🎯 Архитектура функционального программирования

```mermaid
graph LR
    subgraph "Functional Programming Concepts"
        A[Pure Functions] --> A1[No Side Effects]
        A --> A2[Same Input = Same Output]
        
        B[Immutability] --> B1[No Mutation]
        B --> B2[New Objects Created]
        
        C[Higher-Order Functions] --> C1[Functions as Arguments]
        C --> C2[Functions as Return Values]
        
        D[Function Composition] --> D1["f(g(x))"]
        D --> D2[Pipeline Processing]
        
        E[Recursion] --> E1[Self-Calling Functions]
        E --> E2[Base Case + Recursive Case]
    end
    
    style A fill:#00b894
    style B fill:#74b9ff
    style C fill:#ffeaa7
    style D fill:#fd79a8
    style E fill:#e17055
```

## 🛠️ Инструменты отладки функций

```mermaid
flowchart TD
    A[Function Debugging] --> B[Logging]
    A --> C[Decorators]
    A --> D[Type Hints]
    A --> E[Docstrings]
    A --> F[Unit Tests]
    
    B --> B1["@log_calls\nPrint arguments"]
    B --> B2["logging.info\nExecution flow"]
    
    C --> C1["@timer\nPerformance"]
    C --> C2["@validate\nInput checking"]
    
    D --> D1["mypy\nStatic analysis"]
    D --> D2["IDE support\nAutocompletion"]
    
    E --> E1[Help documentation]
    E --> E2[Usage examples]
    
    F --> F1["pytest\nAutomated testing"]
    F --> F2[Coverage analysis]
    
    style B fill:#74b9ff
    style C fill:#00b894
    style D fill:#ffeaa7
    style F fill:#fd79a8
``` 
