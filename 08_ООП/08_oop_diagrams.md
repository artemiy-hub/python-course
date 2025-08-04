# Диаграммы: Объектно-ориентированное программирование в Python

## 🏗️ Основы ООП - Четыре столпа

```mermaid
mindmap
  root((ООП))
    Инкапсуляция
      Сокрытие данных
      Объединение данных и методов
      Контролируемый доступ
      Properties и дескрипторы
    Наследование
      Переиспользование кода
      Иерархия классов
      Множественное наследование
      MRO (Method Resolution Order)
    Полиморфизм
      Один интерфейс разные реализации
      Duck typing
      Перегрузка методов
      Протоколы
    Абстракция
      Скрытие сложности
      Абстрактные классы
      Интерфейсы
      Высокоуровневые концепции
```

## 🏭 Архитектура класса Python

```mermaid
graph TD
    subgraph "Python Class Architecture"
        A[Class Definition] --> B[Class Object]
        B --> C[Instance Creation]
        C --> D[Instance Object]
        
        E[Class Attributes] --> B
        F[Class Methods] --> B
        G[Static Methods] --> B
        
        H[Instance Attributes] --> D
        I[Instance Methods] --> D
        
        J[Special Methods<br/>__init__, __str__, __repr__] --> B
        
        K[Metaclass] --> B
        L[Base Classes] --> B
        
        B --> M[__dict__<br/>Namespace]
        D --> N[__dict__<br/>Instance Data]
        
        O[Descriptor Protocol] --> P[Properties]
        P --> B
    end
    
    style B fill:#3498db
    style D fill:#2ecc71
    style K fill:#e74c3c
    style J fill:#f39c12
```

## 🧬 Наследование и MRO (Method Resolution Order)

```mermaid
graph TD
    subgraph "Multiple Inheritance Diamond Problem"
        A[Animal] --> B[Mammal]
        A --> C[Bird]
        B --> D[Bat]
        C --> D
        
        E[MRO: Bat → Mammal → Bird → Animal → object]
    end
    
    subgraph "Linearization Algorithm (C3)"
        F[Start with class] --> G[Add parents left-to-right]
        G --> H[Ensure no class appears<br/>before its parents]
        H --> I[Add object at the end]
        I --> J[Result: Linear order]
    end
    
    style D fill:#e74c3c
    style E fill:#f39c12
```

## 🔄 Жизненный цикл объекта

```mermaid
stateDiagram-v2
    [*] --> ClassDefined: class MyClass
    ClassDefined --> MetaclassCall: __new__()
    MetaclassCall --> ClassObject: Class created
    
    ClassObject --> InstanceCreation: MyClass()
    InstanceCreation --> AllocateMemory: __new__()
    AllocateMemory --> InitializeObject: __init__()
    InitializeObject --> ObjectReady: Instance ready
    
    ObjectReady --> MethodCall: obj.method()
    MethodCall --> ObjectReady
    
    ObjectReady --> AttributeAccess: obj.attr
    AttributeAccess --> DescriptorCall: __get__()
    DescriptorCall --> ObjectReady
    
    ObjectReady --> AttributeSet: obj.attr = value
    AttributeSet --> DescriptorSet: __set__()
    DescriptorSet --> ObjectReady
    
    ObjectReady --> GarbageCollection: No references
    GarbageCollection --> Finalize: __del__()
    Finalize --> [*]
    
    note right of MetaclassCall
        Metaclass controls
        class creation
    end note
    
    note right of DescriptorCall
        Descriptors control
        attribute access
    end note
```

## 🎭 Полиморфизм в действии

```mermaid
graph LR
    subgraph "Polymorphic Interface"
        A[Client Code] --> B["draw_shape(shape)"]
        
        B --> C{What type?}
        
        C -->|Circle| D["Circle.draw()"]
        C -->|Rectangle| E["Rectangle.draw()"]
        C -->|Triangle| F["Triangle.draw()"]
        
        D --> G[Drawing Circle]
        E --> H[Drawing Rectangle]
        F --> I[Drawing Triangle]
        
        G --> J["Same interface\nDifferent behavior"]
        H --> J
        I --> J
    end
    
    subgraph "Duck Typing"
        K["if hasattr(obj, 'quack')"] --> L["obj.quack()"]
        M[Duck] --> L
        N[Person] --> L
        O[Robot] --> L
    end
    
    style B fill:#3498db
    style J fill:#2ecc71
    style L fill:#f39c12
```

## 🔒 Инкапсуляция и уровни доступа

```mermaid
graph TD
    subgraph "Access Levels in Python"
        A["Public Attributes\nself.name"] --> B[Accessible everywhere]
        
        C["Protected Attributes\nself._name"] --> D["Convention: internal use\nStill accessible"]
        
        E["Private Attributes\nself.__name"] --> F["Name mangling\nself._ClassName__name"]
        
        G["Properties\n@property"] --> H["Controlled access\nGetter/Setter logic"]
        
        I["Descriptors\n__get__, __set__"] --> J["Advanced control\nValidation, computation"]
    end
    
    subgraph "Encapsulation Benefits"
        K[Data Hiding] --> L["Internal implementation\ncan change"]
        M[Validation] --> N[Control data integrity]
        O[Computed Properties] --> P[Dynamic values]
        Q[Access Control] --> R[Security and consistency]
    end
    
    style A fill:#2ecc71
    style C fill:#f39c12
    style E fill:#e74c3c
    style G fill:#3498db
    style I fill:#9b59b6
```

## 🏛️ Абстрактные классы и интерфейсы

```mermaid
graph TD
    subgraph "Abstract Base Classes (ABC)"
        A[ABC Class] --> B["@abstractmethod"]
        A --> C["@abstractproperty"]
        A --> D["@abstractclassmethod"]
        A --> E["@abstractstaticmethod"]
        
        F[Concrete Methods] --> A
        G[Cannot instantiate] --> A
        
        H[Child Class] --> I["Must implement\nall abstract methods"]
        A --> H
    end
    
    subgraph "Protocols (Python 3.8+)"
        J[Protocol Class] --> K[Structural typing]
        K --> L["Duck typing with\ntype checking"]
        
        M["@runtime_checkable"] --> J
        N["isinstance() support"] --> M
        
        O[No inheritance needed] --> J
    end
    
    subgraph "Interface Design"
        P[Define Contract] --> Q[Common behavior]
        Q --> R[Multiple implementations]
        R --> S[Polymorphic usage]
    end
    
    style A fill:#e74c3c
    style J fill:#3498db
    style P fill:#2ecc71
```

## 🎯 Специальные методы (Magic Methods)

```mermaid
graph LR
    subgraph "Object Lifecycle"
        A[__new__] --> B[Object creation]
        C[__init__] --> D[Object initialization]
        E[__del__] --> F[Object destruction]
    end
    
    subgraph "String Representation"
        G[__str__] --> H[User-friendly string]
        I[__repr__] --> J[Developer string]
        K[__format__] --> L[Custom formatting]
    end
    
    subgraph "Operators"
        M[__add__] --> N[+ operator]
        O[__eq__] --> P[== operator]
        Q[__lt__] --> R[< operator]
        S[__len__] --> T["len() function"]
    end
    
    subgraph "Container Protocol"
        U[__getitem__] --> V["obj[key]"]
        W[__setitem__] --> X["obj[key] = value"]
        Y[__delitem__] --> Z["del obj[key]"]
        AA[__contains__] --> BB["key in obj"]
    end
    
    subgraph "Attribute Access"
        CC[__getattr__] --> DD[Fallback access]
        EE[__setattr__] --> FF[Attribute setting]
        GG[__delattr__] --> HH[Attribute deletion]
        II[__getattribute__] --> JJ[All attribute access]
    end
    
    style A fill:#e74c3c
    style G fill:#2ecc71
    style M fill:#f39c12
    style U fill:#3498db
    style CC fill:#9b59b6
```

## 🔧 Дескрипторы - протокол доступа к атрибутам

```mermaid
sequenceDiagram
    participant C as Client Code
    participant O as Object
    participant D as Descriptor
    participant T as Type System
    
    Note over C,T: Attribute Access Flow
    
    C->>O: obj.attr
    O->>T: Look up 'attr' in type(obj).__dict__
    T->>D: Found descriptor
    D->>D: __get__(obj, type(obj))
    D->>O: Return computed value
    O->>C: Return result
    
    Note over C,T: Attribute Assignment Flow
    
    C->>O: obj.attr = value
    O->>T: Look up 'attr' in type(obj).__dict__
    T->>D: Found descriptor
    D->>D: __set__(obj, value)
    D->>D: Validate and store
    D->>O: Assignment complete
    O->>C: Assignment done
    
    Note over C,T: Descriptor Types
    Note over D: Data Descriptor: __get__ + __set__
    Note over D: Non-data Descriptor: __get__ only
```

## 🏗️ Метаклассы - классы классов

```mermaid
graph TD
    subgraph "Metaclass Hierarchy"
        A[type] --> B[Custom Metaclass]
        B --> C[Your Class]
        C --> D[Instance]
        
        E[type.__new__] --> F[Class creation]
        G[type.__init__] --> H[Class initialization]
        
        I[__new__] --> J[Control instance creation]
        K[__init__] --> L[Instance initialization]
    end
    
    subgraph "Metaclass Usage"
        M[Singleton Pattern] --> N[One instance only]
        O[ORM Models] --> P[Database mapping]
        Q[API Registration] --> R[Auto-registration]
        S[Validation] --> T[Class-level validation]
    end
    
    subgraph "Class Creation Process"
        U[class MyClass:] --> V[Collect class dict]
        V --> W[Find metaclass]
        W --> X[Call metaclass.__new__]
        X --> Y[Call metaclass.__init__]
        Y --> Z[Class object ready]
    end
    
    style A fill:#e74c3c
    style B fill:#f39c12
    style C fill:#3498db
    style D fill:#2ecc71
```

## 🔄 Паттерны проектирования в ООП

```mermaid
graph TD
    subgraph "Creational Patterns"
        A[Singleton] --> A1[One instance]
        B[Factory] --> B1[Object creation]
        C[Builder] --> C1[Complex objects]
    end
    
    subgraph "Structural Patterns"
        D[Adapter] --> D1[Interface compatibility]
        E[Decorator] --> E1[Add behavior]
        F[Facade] --> F1[Simplified interface]
        G[Composite] --> G1[Tree structures]
    end
    
    subgraph "Behavioral Patterns"
        H[Observer] --> H1[Event notification]
        I[Strategy] --> I1[Algorithm selection]
        J[Command] --> J1[Encapsulate requests]
        K[State] --> K1[State-dependent behavior]
    end
    
    subgraph "Implementation in Python"
        L[Use ABC for interfaces]
        M[Properties for controlled access]
        N[Decorators for cross-cutting concerns]
        O[Context managers for resources]
    end
    
    style A fill:#e74c3c
    style D fill:#f39c12
    style H fill:#3498db
    style L fill:#2ecc71
```

## 🎨 Композиция vs Наследование

```mermaid
graph LR
    subgraph "Inheritance (IS-A)"
        A[Vehicle] --> B[Car]
        A --> C[Motorcycle]
        B --> D[ElectricCar]
        
        E[Problems:]
        E --> F[Tight coupling]
        E --> G[Diamond problem]
        E --> H[Inflexible hierarchy]
    end
    
    subgraph "Composition (HAS-A)"
        I[Car] --> J[Engine]
        I --> K[GPS]
        I --> L[Radio]
        
        M[Benefits:]
        M --> N[Loose coupling]
        M --> O[Flexible design]
        M --> P[Runtime composition]
        M --> Q[Easier testing]
    end
    
    subgraph "When to Use"
        R[Use Inheritance when:]
        R --> S[True IS-A relationship]
        R --> T[Shared behavior]
        R --> U[Polymorphism needed]
        
        V[Use Composition when:]
        V --> W[HAS-A relationship]
        V --> X[Mix different behaviors]
        V --> Y[Runtime flexibility]
    end
    
    style B fill:#e74c3c
    style I fill:#2ecc71
    style R fill:#f39c12
    style V fill:#3498db
```

## 📊 Сравнение подходов к ООП

```mermaid
quadrantChart
    title "Подходы к ООП в Python"
    x-axis "Простота" --> "Сложность"
    y-axis "Гибкость" --> "Жесткость"
    
    quadrant-1 "Гибкий и сложный"
    quadrant-2 "Жесткий и сложный"
    quadrant-3 "Жесткий и простой"
    quadrant-4 "Гибкий и простой"
    
    "Duck Typing": [0.8, 0.2]
    "Properties": [0.4, 0.4]
    "Простое наследование": [0.2, 0.6]
    "Множественное наследование": [0.7, 0.7]
    "Метаклассы": [0.9, 0.8]
    "Композиция": [0.3, 0.3]
    "Абстрактные классы": [0.5, 0.7]
    "Протоколы": [0.6, 0.4]
```

## 🔄 Жизненный цикл разработки ООП

```mermaid
journey
    title Разработка ООП системы
    section Анализ
      Определить требования: 5: Разработчик
      Выделить объекты: 4: Разработчик
      Найти отношения: 3: Разработчик
    section Дизайн
      Создать иерархию: 4: Архитектор
      Определить интерфейсы: 5: Архитектор
      Выбрать паттерны: 4: Архитектор
    section Реализация
      Написать базовые классы: 4: Программист
      Реализовать методы: 3: Программист
      Добавить специальные методы: 2: Программист
    section Тестирование
      Юнит-тесты: 4: Тестировщик
      Интеграционные тесты: 3: Тестировщик
      Тесты полиморфизма: 2: Тестировщик
    section Рефакторинг
      Улучшить дизайн: 4: Разработчик
      Оптимизировать производительность: 3: Разработчик
      Добавить документацию: 5: Разработчик
```

## 🎯 Принципы SOLID в Python

```mermaid
graph TD
    subgraph "SOLID Principles"
        A[S - Single Responsibility<br/>Одна ответственность] --> A1[Класс должен иметь<br/>только одну причину для изменения]
        
        B[O - Open/Closed<br/>Открыт/Закрыт] --> B1[Открыт для расширения<br/>Закрыт для модификации]
        
        C[L - Liskov Substitution<br/>Подстановки Лисков] --> C1[Объекты подклассов должны<br/>заменять объекты базового класса]
        
        D[I - Interface Segregation<br/>Разделение интерфейсов] --> D1[Много специфичных интерфейсов<br/>лучше одного общего]
        
        E[D - Dependency Inversion<br/>Инверсия зависимостей] --> E1[Зависеть от абстракций<br/>а не от конкретных реализаций]
    end
    
    subgraph "Python Implementation"
        F[ABC для абстракций] --> B
        F --> E
        
        G[Protocol для интерфейсов] --> D
        G --> C
        
        H[Композиция и DI] --> E
        
        I[Мелкие классы] --> A
        
        J[Наследование с осторожностью] --> C
        J --> B
    end
    
    style A fill:#e74c3c
    style B fill:#f39c12
    style C fill:#3498db
    style D fill:#2ecc71
    style E fill:#9b59b6
```

## 🔄 Процесс создания и вызова методов

```mermaid
sequenceDiagram
    participant Code as Client Code
    participant Obj as Object Instance
    participant Type as Class Type
    participant MRO as Method Resolution
    participant Method as Method Object
    
    Code->>Obj: obj.method_name()
    Obj->>Type: Look up method in type(obj)
    Type->>MRO: Search in MRO chain
    
    alt Method found in class
        MRO->>Method: Get method object
        Method->>Method: Bind to instance (self)
        Method->>Code: Execute bound method
    else Method not found
        MRO->>Obj: Check __getattr__
        alt __getattr__ exists
            Obj->>Code: Call __getattr__('method_name')
        else No __getattr__
            Obj->>Code: Raise AttributeError
        end
    end
    
    Note over Code,Method: Bound method execution
    Note over Code,Method: self is automatically passed
```

## 🧩 Компоненты системы ООП

```mermaid
graph LR
    subgraph "Class Components"
        A[Class Definition] --> B[Methods]
        A --> C[Attributes]
        A --> D[Properties]
        A --> E[Class Methods]
        A --> F[Static Methods]
        
        B --> B1[Instance Methods]
        B --> B2[Special Methods]
        
        C --> C1[Class Variables]
        C --> C2[Instance Variables]
        
        D --> D1[Getters]
        D --> D2[Setters]
        D --> D3[Deleters]
    end
    
    subgraph "Relationships"
        G[Inheritance] --> H[IS-A]
        I[Composition] --> J[HAS-A]
        K[Aggregation] --> L[USES-A]
        M[Association] --> N[KNOWS-A]
    end
    
    subgraph "Advanced Features"
        O[Metaclasses] --> P[Class Creation Control]
        Q[Descriptors] --> R[Attribute Access Control]
        S[Context Managers] --> T[Resource Management]
        U[Iterators] --> V[Sequence Protocol]
    end
    
    style A fill:#3498db
    style G fill:#e74c3c
    style O fill:#9b59b6
```

## 📈 Эволюция ООП подходов в Python

```mermaid
timeline
    title Эволюция ООП в Python
    
    section Python 1.x
        1991 : Базовые классы
             : Простое наследование
             : Специальные методы
    
    section Python 2.x
        2001 : New-style classes
             : Properties
             : Descriptors
             : super()
    
    section Python 3.0-3.5
        2008 : Abstract Base Classes
             : Multiple inheritance improvements
             : Method Resolution Order (MRO)
    
    section Python 3.6-3.8
        2016 : __set_name__ for descriptors
             : Data classes
             : Protocols (3.8)
    
    section Python 3.9+
        2020 : Structural pattern matching
             : Generic types improvements
             : Better type hints
``` 