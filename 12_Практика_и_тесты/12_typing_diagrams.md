# Диаграммы: Типизация и аннотации типов в Python

## 🏷️ Эволюция системы типов Python

```mermaid
timeline
    title История типизации в Python
    
    2006 : Python 2.5
         : Function annotations (PEP 3107)
    
    2014 : Python 3.5
         : Type hints (PEP 484)
         : typing module
         : mypy integration
    
    2016 : Python 3.6
         : Variable annotations (PEP 526)
         : Literal types
    
    2018 : Python 3.7
         : Postponed evaluation (PEP 563)
         : from __future__ import annotations
    
    2019 : Python 3.8
         : TypedDict (PEP 589)
         : Literal types (PEP 586)
         : Final qualifier (PEP 591)
    
    2020 : Python 3.9
         : Built-in generics (PEP 585)
         : list[int] instead of List[int]
    
    2021 : Python 3.10
         : Union types (PEP 604)
         : int | str instead of Union[int, str]
         : Parameter specification (PEP 612)
    
    2022 : Python 3.11
         : Self type (PEP 673)
         : Exception groups typing
```

## 🎯 Система типов Python

```mermaid
mindmap
  root((Python Types))
    Built-in Types
      int, float, str, bool
      list, dict, set, tuple
      None, Any
    
    Typing Module
      Optional
        Optional[T]
        T or None (3.10+)
      Union
        Union[int, str]
        int or str (3.10+)
      Generic
        List[T]
        Dict[K, V]
        Custom Generic
      
    Special Forms
      Literal
        Literal debug info
        Literal 1 2 3
      Final
        Final variables
        Final methods
      ClassVar
        Class variables
        
    Protocols
      Structural typing
      Runtime checkable
      Duck typing with types
      
    Advanced
      TypeVar
        Bounded TypeVar
        Constrained TypeVar
      NewType
        Distinct types
      Overload
        Function overloading
      TypedDict
        Structured dicts
```

## 🔄 Градуальная типизация

```mermaid
flowchart LR
    A[Untyped Code] --> B[Partial Typing]
    B --> C[Full Typing]
    B --> D[Type Ignores]
    C --> E[Static Analysis]
    D --> B
    
    subgraph "Migration Strategy"
        F[Add return types] --> G[Add parameter types]
        G --> H[Add variable types]
        H --> I[Remove type ignores]
    end
    
    subgraph "Tools"
        J[mypy] --> K[Type checking]
        L[pyright] --> K
        M[pyre] --> K
        N[IDE support] --> O[IntelliSense]
    end
    
    B -.-> F
    E -.-> J
    
    style A fill:#ffcdd2
    style C fill:#c8e6c9
    style E fill:#e1f5fe
```

## 📦 Структура модуля typing

```mermaid
graph TD
    subgraph "typing module"
        A[Core Types] --> A1[Any, Union, Optional]
        A --> A2[List, Dict, Set, Tuple]
        A --> A3[Callable, Iterator]
        
        B[Generic Types] --> B1[TypeVar]
        B --> B2[Generic]
        B --> B3[Constraints & Bounds]
        
        C[Special Forms] --> C1[Literal]
        C --> C2[Final]
        C --> C3[ClassVar]
        C --> C4[NewType]
        
        D[Protocols] --> D1[Protocol]
        D --> D2[runtime_checkable]
        
        E[Advanced] --> E1[overload]
        E --> E2[TypedDict]
        E --> E3[TYPE_CHECKING]
        
        F[Python 3.9+] --> F1[Built-in generics]
        F --> F2["list[int], dict[str, int]"]
        
        G[Python 3.10+] --> G1["Union operator |"]
        G --> G2["int | str | None"]
    end
    
    style A fill:#e1f5fe
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#fce4ec
    style F fill:#e8f5e8
    style G fill:#fff8e1
```

## 🎭 Протоколы vs Абстракции

```mermaid
graph LR
    subgraph "Traditional Inheritance"
        A[Abstract Base Class] --> B[Concrete Class 1]
        A --> C[Concrete Class 2]
        A --> D[Concrete Class 3]
    end
    
    subgraph "Protocol (Structural)"
        E[Protocol Definition] -.-> F[Any Class with Methods]
        E -.-> G[Another Compatible Class]
        E -.-> H[Third Compatible Class]
    end
    
    subgraph "Comparison"
        I[Nominal Typing] --> J[Explicit inheritance required]
        K[Structural Typing] --> L[Duck typing with type safety]
    end
    
    A -.-> I
    E -.-> K
    
    style A fill:#ffcdd2
    style E fill:#c8e6c9
    style I fill:#fff3e0
    style K fill:#e8f5e8
```

## 🔗 TypeVar и Generic классы

```mermaid
sequenceDiagram
    participant Client as Client Code
    participant Generic as Generic[T]
    participant TypeVar as TypeVar('T')
    participant Checker as Type Checker
    
    Client->>TypeVar: Define T = TypeVar('T')
    Client->>Generic: class Stack(Generic[T])
    Client->>Generic: def push(self, item: T)
    Client->>Generic: def pop(self) -> Optional[T]
    
    Client->>Checker: stack: Stack[int] = Stack()
    Checker->>TypeVar: Bind T to int
    
    Client->>Generic: stack.push(42)
    Checker->>Checker: Check: 42 is int ✓
    
    Client->>Generic: result = stack.pop()
    Checker->>Checker: Infer: result is Optional[int]
    
    Client->>Generic: stack.push("hello")
    Checker->>Checker: Check: "hello" is int ✗
    Checker-->>Client: Type error!
```

## 📊 Dataclasses архитектура

```mermaid
graph TD
    subgraph "Dataclass Decorator"
        A["@dataclass"] --> B[Field Analysis]
        B --> C[Method Generation]
        C --> D[Type Annotation Processing]
    end
    
    subgraph "Generated Methods"
        E["__init__"] --> F[Constructor with types]
        G["__repr__"] --> H[String representation]
        I["__eq__"] --> J[Equality comparison]
        K["__hash__"] --> L[Hash function]
        M["__lt__, __le__, etc."] --> N[Ordering methods]
    end
    
    subgraph "Field Configuration"
        O["field()"] --> P[default_factory]
        O --> Q[compare=False]
        O --> R[repr=False]
        O --> S[init=False]
    end
    
    subgraph "Class Configuration"
        T[frozen=True] --> U[Immutable class]
        V[order=True] --> W[Comparison methods]
        X[unsafe_hash=True] --> Y[Force hash method]
    end
    
    A --> E
    A --> G
    A --> I
    D --> O
    A --> T
    
    style A fill:#c8e6c9
    style E fill:#e1f5fe
    style O fill:#fff3e0
    style T fill:#fce4ec
```

## 🔍 Статический анализ workflow

```mermaid
flowchart TD
    A[Python Source Code] --> B[Parse Type Annotations]
    B --> C[Build Type Graph]
    C --> D[Type Inference]
    D --> E[Type Checking]
    
    E --> F{Type Errors?}
    F -->|Yes| G[Report Errors]
    F -->|No| H[Success]
    
    subgraph "Type Checkers"
        I[mypy] --> J[Most Popular]
        K[pyright] --> L[Microsoft/Fast]
        M[pyre] --> N[Facebook/Meta]
    end
    
    subgraph "IDE Integration"
        O[PyCharm] --> P[Built-in checking]
        Q[VS Code] --> R[Pylance extension]
        S[Vim/Neovim] --> T[Language servers]
    end
    
    E -.-> I
    E -.-> K
    E -.-> M
    
    G -.-> O
    G -.-> Q
    
    style E fill:#fff3e0
    style G fill:#ffcdd2
    style H fill:#c8e6c9
```

## 🎯 Литералы и перечисления

```mermaid
graph LR
    subgraph "Literal Types"
        A["Literal['debug', 'info']"] --> B[String Literals]
        C["Literal[1, 2, 3]"] --> D[Numeric Literals]
        E["Literal[True, False]"] --> F[Boolean Literals]
    end
    
    subgraph "Enum Integration"
        G["class Color(Enum)"] --> H[Color.RED]
        G --> I[Color.GREEN]
        G --> J[Color.BLUE]
    end
    
    subgraph "Use Cases"
        K[API Endpoints] --> L["Literal['/users', '/products']"]
        M[Configuration] --> N["Literal['dev', 'prod', 'test']"]
        O[State Machines] --> P["Literal['idle', 'running', 'stopped']"]
    end
    
    B -.-> K
    B -.-> M
    B -.-> O
    
    style A fill:#e1f5fe
    style G fill:#c8e6c9
    style K fill:#fff3e0
```

## 🔄 Overload демонстрация

```mermaid
sequenceDiagram
    participant Code as User Code
    participant Overload as @overload
    participant Checker as Type Checker
    participant Runtime as Runtime
    
    Code->>Overload: @overload def func(x: int) -> str
    Code->>Overload: @overload def func(x: str) -> int
    Code->>Code: def func(x: Union[int, str]) -> Union[str, int]
    
    Code->>Checker: result = func(42)
    Checker->>Checker: Match first overload
    Checker->>Code: result: str
    
    Code->>Checker: result = func("hello")
    Checker->>Checker: Match second overload
    Checker->>Code: result: int
    
    Code->>Runtime: func(42)
    Runtime->>Runtime: Execute actual implementation
    Runtime->>Code: Return actual result
    
    Note over Overload,Runtime: Overloads are for type checking only<br/>Runtime uses single implementation
```

## 📚 TypedDict структура

```mermaid
graph TD
    subgraph "TypedDict Definition"
        A["class UserDict(TypedDict)"] --> B[name: str]
        A --> C[age: int]
        A --> D[email: str]
    end
    
    subgraph "Inheritance"
        E["class ExtendedDict(UserDict)"] --> F[phone: str]
        E --> G[address: str]
    end
    
    subgraph "Total/Partial"
        H[total=True] --> I[All fields required]
        J[total=False] --> K[All fields optional]
        L["Required[str]"] --> M[Individual field control]
        N["NotRequired[str]"] --> O[Optional in total=True]
    end
    
    subgraph "Runtime Behavior"
        P[Regular dict] --> Q[No runtime validation]
        P --> R[Type checking only]
        P --> S[IDE support]
    end
    
    A --> E
    A -.-> H
    A -.-> J
    E -.-> P
    
    style A fill:#e1f5fe
    style H fill:#c8e6c9
    style P fill:#fff3e0
```

## 🔧 Type checking конфигурация

```mermaid
flowchart LR
    subgraph "mypy Configuration"
        A[mypy.ini] --> B[Global settings]
        C[per-module overrides] --> D[Module-specific rules]
        E[inline comments] --> F[# type: ignore]
    end
    
    subgraph "Check Levels"
        G[--strict] --> H[Maximum strictness]
        I[--ignore-missing-imports] --> J[Skip external libs]
        K[--disallow-untyped-defs] --> L[Require all annotations]
    end
    
    subgraph "IDE Integration"
        M[VS Code] --> N[Python extension]
        O[PyCharm] --> P[Built-in mypy]
        Q[Sublime Text] --> R[LSP-mypy]
    end
    
    subgraph "CI/CD Integration"
        S[GitHub Actions] --> T[mypy check job]
        U[pre-commit] --> V[mypy hook]
        W[tox] --> X[multi-version testing]
    end
    
    B -.-> G
    N -.-> S
    P -.-> U
    
    style A fill:#fff3e0
    style G fill:#c8e6c9
    style M fill:#e1f5fe
    style S fill:#fce4ec
```

## 🎨 Performance impact of typing

```mermaid
xychart-beta
    title "Performance Impact of Type Annotations"
    x-axis [Import Time, Runtime, Memory Usage, Type Check Time]
    y-axis "Relative Impact (%)" 0 --> 20
    bar [5, 1, 3, 100]
```

```mermaid
pie title Type Checking Time Distribution
    "Parsing" : 20
    "Type inference" : 35
    "Constraint solving" : 25
    "Error reporting" : 15
    "Cache operations" : 5
```

## 🚀 Best practices workflow

```mermaid
flowchart TD
    A[Start New Project] --> B{Add Type Hints?}
    B -->|Yes| C[Configure mypy]
    B -->|No| D[Add gradually]
    
    C --> E[Start with function signatures]
    D --> E
    
    E --> F[Add variable annotations]
    F --> G[Use dataclasses for data]
    G --> H[Implement protocols]
    H --> I[Add generic types]
    
    I --> J[Run type checker]
    J --> K{Errors found?}
    K -->|Yes| L[Fix type errors]
    K -->|No| M[Code review]
    
    L --> J
    M --> N[CI/CD integration]
    N --> O[Production ready]
    
    subgraph "Tools"
        P[mypy]
        Q[black] 
        R[isort]
        S[pre-commit]
    end
    
    J -.-> P
    M -.-> Q
    M -.-> R
    N -.-> S
    
    style C fill:#c8e6c9
    style O fill:#e1f5fe
    style L fill:#fff3e0
```

## 🔬 Advanced typing patterns

```mermaid
graph TD
    subgraph "Conditional Types"
        A[TYPE_CHECKING] --> B[Import only for typing]
        C[sys.version_info] --> D[Version-specific types]
    end
    
    subgraph "Generic Constraints"
        E[TypeVar bounds] --> F["T: bound=Comparable"]
        G[TypeVar constraints] --> H["T: constrained to int,str"]
    end
    
    subgraph "Recursive Types"
        I["JSON = Union[Dict[str, JSON], List[JSON], str, int, float, bool, None]"]
        J["Tree = Union[Leaf, Node[Tree]]"]
    end
    
    subgraph "Higher-Order Types"
        K[ParamSpec] --> L[Decorator typing]
        M[Concatenate] --> N[Partial application]
    end
    
    style I fill:#ffcdd2
    style K fill:#c8e6c9
    style A fill:#e1f5fe
    style E fill:#fff3e0
```

## 📈 Typing adoption timeline

```mermaid
gantt
    title Python Typing Adoption in Projects
    dateFormat  X
    axisFormat %s
    
    section Early (2015-2017)
    Experimental usage    :a1, 0, 2
    Basic annotations     :a2, 1, 3
    
    section Growth (2018-2020)
    Library adoption      :b1, 2, 5
    Tool maturation       :b2, 3, 6
    Community acceptance  :b3, 4, 7
    
    section Mainstream (2021+)
    Standard practice     :c1, 6, 8
    Advanced patterns     :c2, 7, 9
    Performance tools     :c3, 8, 10
``` 