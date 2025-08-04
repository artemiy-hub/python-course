# Диаграммы: Модули и пакеты в Python

## 📦 Структура модулей и пакетов

```mermaid
graph TD
    subgraph "Python Module System"
        A[Python Program] --> B[Import Statement]
        B --> C{Module Type?}
        
        C -->|Built-in| D[Built-in Modules<br/>sys, os, math]
        C -->|Standard Library| E[Standard Library<br/>json, datetime, collections]
        C -->|Third-party| F[Third-party Packages<br/>requests, numpy, pandas]
        C -->|User-defined| G[User Modules<br/>my_module.py]
        
        D --> H[Module Object]
        E --> H
        F --> H
        G --> H
        
        H --> I[Module Namespace]
        I --> J[Functions]
        I --> K[Classes]
        I --> L[Variables]
        I --> M[Constants]
    end
    
    style A fill:#e1f5fe
    style H fill:#c8e6c9
    style I fill:#fff3e0
```

## 🔍 Процесс поиска и загрузки модулей

```mermaid
sequenceDiagram
    participant P as Python Program
    participant I as Import System
    participant F as Module Finder
    participant L as Module Loader
    participant C as Module Cache
    participant M as Module Object
    
    P->>I: import module_name
    I->>C: Check sys.modules
    
    alt Module in cache
        C->>P: Return cached module
    else Module not cached
        I->>F: Find module spec
        F->>F: Search in sys.path
        
        alt Module found
            F->>L: Create loader
            L->>M: Create module object
            L->>M: Execute module code
            M->>C: Cache module
            C->>P: Return module
        else Module not found
            F->>P: ImportError
        end
    end
    
    Note over P,M: sys.path search order:<br/>1. Current directory<br/>2. PYTHONPATH<br/>3. Standard library<br/>4. Site-packages
```

## 📁 Структура пакета

```mermaid
graph TB
    subgraph "Package Structure"
        A[mypackage/] --> B[__init__.py]
        A --> C[module1.py]
        A --> D[module2.py]
        A --> E[subpackage/]
        A --> F[utils/]
        A --> G[tests/]
        
        E --> H[__init__.py]
        E --> I[submodule1.py]
        E --> J[submodule2.py]
        
        F --> K[__init__.py]
        F --> L[helpers.py]
        F --> M[validators.py]
        
        G --> N[__init__.py]
        G --> O[test_module1.py]
        G --> P[test_module2.py]
    end
    
    subgraph "Import Paths"
        Q["import mypackage"]
        R["from mypackage import module1"]
        S["from mypackage.subpackage import submodule1"]
        T["from mypackage.utils import helpers"]
    end
    
    B -.-> Q
    C -.-> R
    I -.-> S
    L -.-> T
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style E fill:#e8f5e8
    style F fill:#fce4ec
```

## 🔄 Типы импортов

```mermaid
graph LR
    subgraph "Import Types"
        A[Import Statement] --> B{Import Type}
        
        B -->|import module| C[Full Module Import]
        B -->|from module import item| D[Selective Import]
        B -->|import module as alias| E[Aliased Import]
        B -->|from module import *| F[Wildcard Import]
        
        C --> G["module.function()"]
        D --> H["function()"]
        E --> I["alias.function()"]
        F --> J["function()"]
        
        subgraph "Relative Imports"
            K[from . import module] --> L[Same Package]
            M[from .. import module] --> N[Parent Package]
            O[from .subpackage import module] --> P[Sub Package]
        end
    end
    
    style C fill:#c8e6c9
    style D fill:#bbdefb
    style E fill:#f8bbd9
    style F fill:#ffcdd2
    style K fill:#dcedc8
    style M fill:#f3e5f5
    style O fill:#e0f2f1
```

## 🚀 Динамический импорт

```mermaid
flowchart TD
    A[Dynamic Import Need] --> B{Import Method}
    
    B -->|importlib.import_module| C[Runtime Module Import]
    B -->|importlib.util.spec_from_file_location| D[File-based Import]
    B -->|exec + types.ModuleType| E[Code String Import]
    B -->|__import__| F[Built-in Import]
    
    C --> G[Module Discovery]
    D --> H[Direct File Loading]
    E --> I[Code Execution]
    F --> J[Low-level Import]
    
    G --> K[Module Object]
    H --> K
    I --> K
    J --> K
    
    K --> L[sys.modules Registration]
    L --> M[Module Available for Use]
    
    subgraph "Use Cases"
        N[Plugin Systems]
        O[Conditional Imports]
        P[Configuration Loading]
        Q[Hot Reloading]
    end
    
    A -.-> N
    A -.-> O
    A -.-> P
    A -.-> Q
    
    style A fill:#ffeb3b
    style K fill:#4caf50
    style M fill:#2196f3
```

## 🎯 Система путей поиска (sys.path)

```mermaid
graph TD
    subgraph "sys.path Priority Order"
        A[1. Script Directory] --> B[2. PYTHONPATH Environment]
        B --> C[3. Standard Library]
        C --> D[4. Site-packages]
        D --> E[5. Additional Paths]
    end
    
    subgraph "Path Sources"
        F[Current Working Directory] --> A
        G[PYTHONPATH Variable] --> B
        H[Python Installation] --> C
        I[pip install location] --> D
        J["sys.path.append()"] --> E
    end
    
    subgraph "Module Resolution"
        K[Module Search] --> L{Check each path}
        L -->|Found| M[Load Module]
        L -->|Not Found| N[Next Path]
        N --> L
        L -->|All Paths Checked| O[ImportError]
    end
    
    A -.-> K
    B -.-> K
    C -.-> K
    D -.-> K
    E -.-> K
    
    style A fill:#f44336
    style B fill:#ff9800
    style C fill:#4caf50
    style D fill:#2196f3
    style E fill:#9c27b0
```

## 🔧 Атрибуты модулей

```mermaid
mindmap
  root((Module Attributes))
    Special Attributes
      __name__
        Module name
        "__main__" for scripts
      __file__
        Module file path
        None for built-ins
      __doc__
        Module docstring
        First string literal
      __package__
        Package name
        None for top-level
      __path__
        Package search path
        List of directories
    
    Custom Attributes
      __version__
        Version string
        "1.0.0"
      __author__
        Author information
        "Developer Name"
      __all__
        Public API definition
        List of names
      __license__
        License information
        "MIT", "GPL", etc.
    
    Runtime Attributes
      Functions
        Defined functions
        Imported functions
      Classes
        Defined classes
        Imported classes
      Variables
        Module-level variables
        Configuration settings
      Constants
        UPPER_CASE values
        Immutable settings
```

## 📋 Жизненный цикл модуля

```mermaid
stateDiagram-v2
    [*] --> NotLoaded: Module not imported
    
    NotLoaded --> Loading: import statement
    Loading --> Compiling: Parse .py file
    Compiling --> Executing: Create module object
    Executing --> Loaded: Execute module code
    Loaded --> Cached: Add to sys.modules
    
    Cached --> InUse: Module available
    InUse --> InUse: Subsequent imports
    
    InUse --> Reloading: importlib.reload()
    Reloading --> Executing: Re-execute code
    
    InUse --> Unloaded: del sys.modules[name]
    Unloaded --> [*]: Garbage collected
    
    Loading --> Error: Import fails
    Compiling --> Error: Syntax error
    Executing --> Error: Runtime error
    Error --> [*]: ImportError raised
    
    note right of Cached
        Module cached in
        sys.modules for
        fast subsequent
        access
    end note
    
    note right of Reloading
        Used for development
        and hot reloading
        scenarios
    end note
```

## 🏗️ Структура проекта

```mermaid
graph TD
    subgraph "Project Structure Best Practices"
        A[myproject/] --> B[README.md]
        A --> C[LICENSE]
        A --> D[pyproject.toml]
        A --> E[requirements.txt]
        A --> F[.gitignore]
        
        A --> G[src/myproject/]
        G --> H[__init__.py]
        G --> I[core/]
        G --> J[utils/]
        G --> K[api/]
        G --> L[config/]
        
        I --> M[__init__.py]
        I --> N[models.py]
        I --> O[services.py]
        
        J --> P[__init__.py]
        J --> Q[helpers.py]
        J --> R[validators.py]
        
        K --> S[__init__.py]
        K --> T[routes.py]
        K --> U[schemas.py]
        
        A --> V[tests/]
        V --> W[__init__.py]
        V --> X[test_core/]
        V --> Y[test_utils/]
        V --> Z[test_api/]
        
        A --> AA[docs/]
        AA --> BB[conf.py]
        AA --> CC[index.rst]
        
        A --> DD[scripts/]
        DD --> EE[setup.sh]
        DD --> FF[deploy.py]
    end
    
    style A fill:#e1f5fe
    style G fill:#e8f5e8
    style I fill:#fff3e0
    style J fill:#fce4ec
    style K fill:#f3e5f5
    style V fill:#ffebee
```

## 🔄 Система плагинов

```mermaid
sequenceDiagram
    participant App as Application
    participant PM as Plugin Manager
    participant FS as File System
    participant PL as Plugin Loader
    participant P1 as Plugin 1
    participant P2 as Plugin 2
    
    App->>PM: Initialize plugin system
    PM->>FS: Scan plugin directory
    FS->>PM: Return plugin files
    
    loop For each plugin file
        PM->>PL: Load plugin file
        PL->>PL: Import as module
        PL->>PL: Find plugin classes
        PL->>P1: Instantiate plugin
        P1->>PM: Register plugin
    end
    
    App->>PM: Get available plugins
    PM->>App: Return plugin list
    
    App->>PM: Execute plugin "data_processor"
    PM->>P1: Call execute method
    P1->>App: Return result
    
    App->>PM: Execute plugin "formatter"
    PM->>P2: Call execute method
    P2->>App: Return result
    
    Note over App,P2: Plugins can be loaded/unloaded<br/>dynamically at runtime
```

## 📦 Управление зависимостями

```mermaid
graph TB
    subgraph "Dependency Management"
        A[Project Requirements] --> B{Specification Method}
        
        B -->|Traditional| C[requirements.txt]
        B -->|Modern| D[pyproject.toml]
        B -->|Pipenv| E[Pipfile]
        B -->|Poetry| F[pyproject.toml + poetry.lock]
        
        C --> G[pip install -r requirements.txt]
        D --> H[pip install -e .]
        E --> I[pipenv install]
        F --> J[poetry install]
        
        G --> K[Virtual Environment]
        H --> K
        I --> L[Pipenv Environment]
        J --> M[Poetry Environment]
        
        K --> N[Isolated Dependencies]
        L --> N
        M --> N
    end
    
    subgraph "Environment Types"
        O[Development]
        P[Testing]
        Q[Production]
        R[Documentation]
    end
    
    N --> O
    N --> P
    N --> Q
    N --> R
    
    style A fill:#ffeb3b
    style K fill:#4caf50
    style N fill:#2196f3
```

## 🔍 Импорт по условию

```mermaid
flowchart TD
    A[Import Statement] --> B{Condition Check}
    
    B -->|Version Check| C["sys.version_info >= (3, 8)"]
    B -->|Platform Check| D["platform.system() == 'Windows'"]
    B -->|Availability Check| E[Module Available?]
    B -->|Feature Check| F["hasattr(module, 'feature')"]
    
    C -->|True| G[Import new feature]
    C -->|False| H[Import fallback/alternative]
    
    D -->|True| I[Import Windows-specific]
    D -->|False| J[Import Unix-specific]
    
    E -->|Available| K[Import optional dependency]
    E -->|Not Available| L[Skip or use alternative]
    
    F -->|Has Feature| M[Use advanced feature]
    F -->|No Feature| N[Use basic implementation]
    
    subgraph "Example Patterns"
        O["try:\n    import ujson as json\nexcept ImportError:\n    import json"]
        
        P["if sys.version_info >= (3, 8):\n    from functools import cached_property\nelse:\n    # Custom implementation"]
        
        Q["HAS_NUMPY = True\ntry:\n    import numpy\nexcept ImportError:\n    HAS_NUMPY = False"]
    end
    
    G -.-> O
    C -.-> P
    E -.-> Q
    
    style A fill:#ffeb3b
    style B fill:#ff9800
    style G fill:#4caf50
    style H fill:#f44336
```

## 🎨 Namespace пакеты

```mermaid
graph TD
    subgraph "Regular Package"
        A[mypackage/] --> B[__init__.py]
        A --> C[module1.py]
        A --> D[module2.py]
    end
    
    subgraph "Namespace Package (PEP 420)"
        E[Location 1] --> F[mycompany/]
        G[Location 2] --> H[mycompany/]
        
        F --> I[package1/]
        F --> J[__init__.py - optional]
        
        H --> K[package2/]
        H --> L[__init__.py - optional]
        
        I --> M[module1.py]
        K --> N[module2.py]
    end
    
    subgraph "Usage"
        O["import mycompany.package1.module1"]
        P["import mycompany.package2.module2"]
        Q["# Both work seamlessly"]
    end
    
    M -.-> O
    N -.-> P
    
    subgraph "Benefits"
        R[Distributed Development]
        S[Plugin Architecture]
        T[Modular Installation]
        U[No __init__.py Required]
    end
    
    style E fill:#e3f2fd
    style G fill:#e3f2fd
    style F fill:#c8e6c9
    style H fill:#c8e6c9
    style R fill:#fff3e0
    style S fill:#fce4ec
    style T fill:#f3e5f5
    style U fill:#e0f2f1
```

## 📊 Производительность импортов

```mermaid
graph LR
    subgraph "Import Performance"
        A[Module Import] --> B{Import Type}
        
        B -->|Direct| C[Fast Import<br/>~1ms]
        B -->|With Dependencies| D[Medium Import<br/>~10ms]
        B -->|Heavy Libraries| E[Slow Import<br/>~100ms+]
        
        C --> F[Built-in Modules]
        D --> G[Standard Library]
        E --> H[Large Packages<br/>numpy, pandas]
        
        subgraph "Optimization Strategies"
            I[Lazy Imports]
            J[Conditional Imports]
            K[Import Caching]
            L[Partial Imports]
        end
        
        E -.-> I
        E -.-> J
        D -.-> K
        E -.-> L
    end
    
    subgraph "Timing Comparison"
        M["import sys: 0.1ms"]
        N["import json: 1ms"]
        O["import requests: 50ms"]
        P["import pandas: 200ms"]
        Q["import tensorflow: 2000ms"]
    end
    
    F -.-> M
    G -.-> N
    H -.-> O
    H -.-> P
    H -.-> Q
    
    style C fill:#4caf50
    style D fill:#ff9800
    style E fill:#f44336
    style I fill:#e1f5fe
```

## 🔄 Циклические импорты

```mermaid
graph TD
    subgraph "Circular Import Problem"
        A[module_a.py] -->|imports| B[module_b.py]
        B -->|imports| A
        
        C[Import Error!<br/>Circular dependency]
    end
    
    A -.-> C
    B -.-> C
    
    subgraph "Solutions"
        D[Delayed Import] --> E["def function():<br/>    import module_b"]
        F[Restructure Code] --> G["Move shared code<br/>to common module"]
        H[Import in Function] --> I["Import only when needed<br/>inside functions"]
        J[Dependency Injection] --> K["Pass dependencies<br/>as parameters"]
    end
    
    subgraph "Prevention"
        L[Good Design] --> M["Minimize dependencies<br/>between modules"]
        N[Layered Architecture] --> O["Higher layers import<br/>lower layers only"]
        P[Interface Segregation] --> Q["Use abstract interfaces<br/>to break cycles"]
    end
    
    style A fill:#ffcdd2
    style B fill:#ffcdd2
    style C fill:#f44336
    style D fill:#c8e6c9
    style F fill:#c8e6c9
    style H fill:#c8e6c9
    style J fill:#c8e6c9
```

## 📚 Эволюция системы модулей

```mermaid
timeline
    title История системы модулей Python
    
    section Python 1.x
        1991 : Базовые модули
             : import statement
             : Простая система путей
    
    section Python 2.0-2.7
        2000 : Пакеты с __init__.py
             : from __future__ import
             : Относительные импорты
        2002 : Import hooks
             : sys.meta_path
    
    section Python 3.0-3.3
        2008 : Абсолютные импорты по умолчанию
             : importlib модуль
             : Улучшенная система импорта
    
    section Python 3.4+
        2014 : PEP 420 Namespace packages
             : importlib.util
             : Модульная система импорта
        2016 : importlib.machinery
             : Лучшая производительность
    
    section Python 3.8+
        2019 : Улучшения importlib
             : Лучшая обработка ошибок
             : Оптимизации скорости
```

## 🎯 Лучшие практики импортов

```mermaid
graph TB
    subgraph "Import Best Practices"
        A[Import Guidelines] --> B[Order]
        A --> C[Style]
        A --> D[Performance]
        A --> E[Maintainability]
        
        B --> F["1. Standard library<br/>2. Third-party<br/>3. Local application"]
        
        C --> G["Use explicit imports<br/>Avoid import *<br/>Use meaningful aliases"]
        
        D --> H["Lazy imports for heavy modules<br/>Conditional imports<br/>Group related imports"]
        
        E --> I["Document import dependencies<br/>Use __all__ for public API<br/>Minimize circular dependencies"]
    end
    
    subgraph "Anti-patterns"
        J[Import *] --> K["Namespace pollution<br/>Hidden dependencies"]
        L[Circular imports] --> M["Runtime errors<br/>Complex debugging"]
        N[Heavy imports at top] --> O["Slow startup time<br/>Unnecessary overhead"]
    end
    
    style F fill:#c8e6c9
    style G fill:#c8e6c9
    style H fill:#c8e6c9
    style I fill:#c8e6c9
    style J fill:#ffcdd2
    style L fill:#ffcdd2
    style N fill:#ffcdd2
``` 