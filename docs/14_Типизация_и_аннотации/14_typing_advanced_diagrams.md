# Диаграммы: Продвинутая типизация и аннотации

## 🎯 Архитектура системы типов Python

### Эволюция типизации в Python

```mermaid
graph TD
    A["Python 2.x\nБез типов"] --> B["Python 3.0-3.4\nФункциональные аннотации"]
    B --> C["Python 3.5\ntyping module"]
    C --> D["Python 3.6\nVariable annotations"]
    D --> E["Python 3.7\nForward references"]
    E --> F["Python 3.8\nProtocols, Literal"]
    F --> G["Python 3.9\nBuilt-in generics"]
    G --> H["Python 3.10\nUnion operator |"]
    H --> I["Python 3.11\nSelf type"]
    I --> J["Python 3.12\nGeneric type alias"]
    
    style A fill:#ffcdd2
    style C fill:#c8e6c9
    style G fill:#fff3e0
    style J fill:#e1f5fe
```

### Иерархия системы типов

```mermaid
graph TD
    A[typing System] --> B[Basic Types]
    A --> C[Generic Types]
    A --> D[Protocols]
    A --> E[Type Variables]
    A --> F[Special Forms]
    
    B --> B1[int, str, bool]
    B --> B2[List, Dict, Set]
    B --> B3[Optional, Union]
    
    C --> C1[TypeVar]
    C --> C2[Generic]
    C --> C3[Parameterized]
    
    D --> D1[Protocol]
    D --> D2[runtime_checkable]
    D --> D3[Structural typing]
    
    E --> E1[Bound TypeVar]
    E --> E2[Constrained TypeVar]
    E --> E3[Covariant/Contravariant]
    
    F --> F1[Any, NoReturn]
    F --> F2[Type, ClassVar]
    F --> F3[Final, Literal]
    
    style A fill:#e3f2fd
    style C fill:#f3e5f5
    style D fill:#e8f5e8
```

## 🔧 TypeVar и ограничения

### TypeVar с ограничениями

```mermaid
graph LR
    A[TypeVar Definition] --> B{Bound или Constraint?}
    
    B -->|Bound| C["T = TypeVar('T', bound=BaseClass)"]
    B -->|Constraint| D["T = TypeVar('T', int, str, float)"]
    
    C --> C1["T должен быть\nподклассом BaseClass"]
    C --> C2["Например: bound=Comparable"]
    
    D --> D1["T может быть только\nодним из указанных типов"]
    D --> D2[Строгое ограничение]
    
    C1 --> E[Более гибко]
    D1 --> F[Более строго]
    
    style B fill:#ffffcc
    style C1 fill:#c8e6c9
    style D1 fill:#ffcdd2
```

### Ковариантность и контравариантность

```mermaid
graph TD
    A[Variance в типах] --> B[Covariant<br/>covariant=True]
    A --> C[Contravariant<br/>contravariant=True]
    A --> D[Invariant<br/>default]
    
    B --> B1["List[Dog] → List[Animal]<br/>✅ Можно читать"]
    B --> B2["Producer[T_co]<br/>Только возвращает T"]
    
    C --> C1["Callable[[Animal], None]<br/>← Callable[[Dog], None]<br/>✅ Можно принимать"]
    C --> C2["Consumer[T_contra]<br/>Только принимает T"]
    
    D --> D1["List[Dog] ≠ List[Animal]<br/>❌ Нет связи"]
    D --> D2["Mutable[T]<br/>И читает, и пишет"]
    
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#ffcdd2
```

## 🏛️ Протоколы и структурная типизация

### Протоколы vs Наследование

```mermaid
graph LR
    A[Typing Approaches] --> B["Nominal Typing\nНаследование"]
    A --> C["Structural Typing\nПротоколы"]
    
    B --> B1["class Dog extends Animal"]
    B --> B2[Явное наследование]
    B --> B3["isinstance() работает"]
    
    C --> C1["Protocol: Drawable\ndef draw(self)"]
    C --> C2[Duck typing]
    C --> C3[Проверка по структуре]
    
    B1 --> D[Жёсткая связь]
    C1 --> E[Гибкость]
    
    style B fill:#ffcdd2
    style C fill:#c8e6c9
```

### Runtime проверяемые протоколы

```mermaid
graph TD
    A["@runtime_checkable\nProtocol"] --> B[Compile Time]
    A --> C[Runtime]
    
    B --> B1[MyPy проверка]
    B --> B2[IDE поддержка]
    B --> B3[Static analysis]
    
    C --> C1["isinstance() работает"]
    C --> C2[Runtime validation]
    C --> C3[Dynamic checks]
    
    A --> D[Два мира типизации]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#f3e5f5
```

## 🎯 Условная типизация

### Type Guards и сужение типов

```mermaid
graph TD
    A["Union[str, int]"] --> B{Type Guard Function}
    
    B -->|"is_string(x)"| C["TypeGuard[str]"]
    B -->|"is_int(x)"| D["TypeGuard[int]"]
    
    C --> C1["x: str в этой ветке"]
    D --> D1["x: int в этой ветке"]
    
    A --> E["Без Type Guard x: Union[str, int]"]
    
    style B fill:#ffffcc
    style C1 fill:#c8e6c9
    style D1 fill:#c8e6c9
    style E fill:#ffcdd2
```

### Overload и множественные сигнатуры

```mermaid
graph LR
    A["@overload def func(x: int) → str"] --> D["Runtime Implementation def func(x)"]
    B["@overload def func(x: str) → int"] --> D
    C["@overload def func(x: list) → bool"] --> D
    
    D --> E["Одна реализация Множество типов"]
    
    A --> F["Type Checker видит все варианты"]
    B --> F
    C --> F
    
    style D fill:#e3f2fd
    style F fill:#fff3e0
```

## 📦 Интеграция с Pydantic

### Pydantic модели и типизация

```mermaid
graph TD
    A[Pydantic Model] --> B[Runtime Validation]
    A --> C[Type Annotations]
    A --> D[JSON Schema]
    
    B --> B1[Parsing]
    B --> B2[Validation]
    B --> B3[Coercion]
    
    C --> C1[Static Analysis]
    C --> C2[IDE Support]
    C --> C3[Documentation]
    
    D --> D1[API Docs]
    D --> D2[Client Generation]
    D --> D3[OpenAPI]
    
    E[BaseModel] --> A
    F[Field] --> A
    G[validator] --> A
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

### Валидация и типы

```mermaid
graph LR
    A[Input Data] --> B[Pydantic Model]
    
    B --> C{Validation}
    
    C -->|✅ Success| D[Typed Instance]
    C -->|❌ Error| E[ValidationError]
    
    D --> F[100% Type Safe]
    E --> G[Detailed Error Info]
    
    B --> H[Type Hints]
    H --> I[Static Checking]
    H --> J[Runtime Validation]
    
    style C fill:#ffffcc
    style D fill:#c8e6c9
    style E fill:#ffcdd2
    style F fill:#4caf50
```

## 🚀 Продвинутые Generic типы

### Сложные Generic конструкции

```mermaid
graph TD
    A[Generic Types] --> B["Simple Generic\nList[T]"]
    A --> C["Multi-parameter\nDict[K, V]"]
    A --> D["Constrained\nMapping[K, V]"]
    A --> E["Recursive\nTree[T]"]
    
    B --> B1["Container[T]"]
    B --> B2["Iterator[T]"]
    
    C --> C1["Callable[[P], R]"]
    C --> C2["Tuple[T1, T2, T3]"]
    
    D --> D1[TypeVar bounds]
    D --> D2[Protocol constraints]
    
    E --> E1[Self-referencing]
    E --> E2[Forward references]
    
    style A fill:#e3f2fd
    style E fill:#fff3e0
```

### Generic классы в действии

```mermaid
graph LR
    A["Generic[T] Class"] --> B[Type Parameter T]
    
    B --> C[Instance Creation]
    C --> D["MyClass[int]"]
    C --> E["MyClass[str]"]
    C --> F["MyClass[CustomType]"]
    
    D --> G["Type Safety\nдля int"]
    E --> H["Type Safety\nдля str"]
    F --> I["Type Safety\nдля CustomType"]
    
    A --> J["Method Signatures\nиспользуют T"]
    J --> K[Return T]
    J --> L[Accept T]
    
    style A fill:#e3f2fd
    style B fill:#ffffcc
    style G fill:#c8e6c9
    style H fill:#c8e6c9
    style I fill:#c8e6c9
```

## 🔍 Static Analysis Tools

### Экосистема инструментов

```mermaid
graph TD
    A[Python Type Checking] --> B[MyPy]
    A --> C[Pyright/Pylance]
    A --> D[PyCharm]
    A --> E[Pyre]
    
    B --> B1[Строгая проверка]
    B --> B2[Incremental mode]
    B --> B3[Plugin system]
    
    C --> C1[Fast checking]
    C --> C2[VS Code integration]
    C --> C3[Language server]
    
    D --> D1[IDE integration]
    D --> D2[Refactoring]
    D --> D3[Code completion]
    
    E --> E1[Facebook's checker]
    E --> E2[Performance focus]
    E --> E3[Large codebases]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#ffcdd2
```

### Настройка и конфигурация

```mermaid
graph LR
    A[Type Checking Setup] --> B[mypy.ini]
    A --> C[pyproject.toml]
    A --> D[IDE Settings]
    
    B --> B1[strict = true]
    B --> B2[ignore_missing_imports]
    B --> B3[disallow_untyped_defs]
    
    C --> C1[[tool.mypy]]
    C --> C2[python_version]
    C --> C3[plugins]
    
    D --> D1[Real-time checking]
    D --> D2[Error highlighting]
    D --> D3[Quick fixes]
    
    E[CI/CD Integration] --> F[Pre-commit hooks]
    E --> G[GitHub Actions]
    E --> H[Type coverage]
    
    style A fill:#e3f2fd
    style E fill:#fff3e0
```

## 📈 Прогрессивная типизация

### Стратегия внедрения типов

```mermaid
graph TD
    A[Legacy Codebase] --> B[Step 1: Add basic types]
    B --> C[Step 2: Function signatures]
    C --> D[Step 3: Class attributes]
    D --> E[Step 4: Generic types]
    E --> F[Step 5: Protocols]
    F --> G[Fully Typed Codebase]
    
    B --> B1[str, int, bool]
    C --> C1["→ return types\n← parameter types"]
    D --> D1[Instance variables<br/>Class variables]
    E --> E1["List[T], Dict[K,V]"]
    F --> F1["Custom protocols\nStructural typing"]
    
    H[Type Coverage] --> I[0%] 
    I --> J[25%]
    J --> K[50%]
    K --> L[75%]
    L --> M[90%+]
    
    style A fill:#ffcdd2
    style G fill:#4caf50
    style M fill:#4caf50
```

Эти диаграммы показывают полную картину продвинутой типизации в Python, от базовых концепций до сложных паттернов и инструментов. 