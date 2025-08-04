# Диаграммы: Модули и пакеты Python

## 🏗️ Структура модуля Python

```mermaid
graph TB
    subgraph "Python Module Structure"
        A[Module File .py] --> B[Module Header]
        A --> C[Imports Section]
        A --> D[Constants & Variables]
        A --> E[Functions]
        A --> F[Classes]
        A --> G[Main Block]
        
        B --> B1["Module docstring"]
        B --> B2["# -*- coding: utf-8 -*-"]
        
        C --> C1[import statements]
        C --> C2[from X import Y]
        
        D --> D1[CONSTANTS]
        D --> D2[module_variables]
        
        E --> E1["def function_name()"]
        E --> E2[function docstrings]
        
        F --> F1["class ClassName:"]
        F --> F2[class docstrings]
        
        G --> G1["if __name__ == '__main__':"]
        G --> G2[main execution code]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#ffeaa7
    style G fill:#fd79a8
```

## 📦 Иерархия пакетов

```mermaid
graph TD
    subgraph "Package Hierarchy"
        A[mypackage/] --> B[__init__.py]
        A --> C[module1.py]
        A --> D[module2.py]
        A --> E[subpackage/]
        A --> F[utils/]
        
        E --> E1[__init__.py]
        E --> E2[submodule.py]
        
        F --> F1[__init__.py]
        F --> F2[helpers.py]
        F --> F3[constants.py]
        
        B --> B1[Package initialization]
        B --> B2[__all__ definition]
        B --> B3[Version info]
        
        C --> C1[Module functions]
        C --> C2[Module classes]
        
        E2 --> E21[Submodule content]
        F2 --> F21[Helper functions]
        F3 --> F31[Package constants]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style E fill:#ffeaa7
    style F fill:#fd79a8
```

## 🔍 Механизм поиска модулей

```mermaid
flowchart TD
    A[import module_name] --> B{Модуль в sys.modules?}
    B -->|Да| C[Возврат кешированного модуля]
    B -->|Нет| D[Поиск в sys.path]
    
    D --> E[1. Текущая директория]
    E --> F{Найден?}
    F -->|Да| L[Загрузка модуля]
    F -->|Нет| G[2. PYTHONPATH]
    
    G --> H{Найден?}
    H -->|Да| L
    H -->|Нет| I[3. Стандартная библиотека]
    
    I --> J{Найден?}
    J -->|Да| L
    J -->|Нет| K[4. site-packages]
    
    K --> M{Найден?}
    M -->|Да| L
    M -->|Нет| N[ModuleNotFoundError]
    
    L --> O[Выполнение модуля]
    O --> P[Добавление в sys.modules]
    P --> Q[Возврат модуля]
    
    style A fill:#74b9ff
    style L fill:#00b894
    style N fill:#e17055
    style Q fill:#00b894
```

## 🌊 Жизненный цикл импорта

```mermaid
sequenceDiagram
    participant App as Application
    participant Imp as Import System
    participant FS as File System
    participant Mod as Module
    
    App->>Imp: import mymodule
    Imp->>Imp: Check sys.modules cache
    
    alt Module not cached
        Imp->>FS: Search in sys.path
        FS-->>Imp: Return module path
        Imp->>Mod: Create module object
        Imp->>Mod: Execute module code
        Mod-->>Imp: Module initialized
        Imp->>Imp: Store in sys.modules
    else Module cached
        Imp->>Imp: Return cached module
    end
    
    Imp-->>App: Return module object
    App->>Mod: Use module attributes
```

## 🎯 Типы импортов

```mermaid
mindmap
  root((Import Types))
    Absolute
      import module
      from package import module
      from package.subpackage import item
    Relative
      from . import module
      from .. import parent_module
      from .submodule import function
    Aliased
      import module as alias
      from module import function as func
    Conditional
      try/except ImportError
      Optional imports
    Dynamic
      importlib.import_module
      __import__ function
```

## 🏗️ Архитектура пакета

```mermaid
graph LR
    subgraph "Package Architecture"
        A[Package Root] --> B[__init__.py]
        A --> C[Core Modules]
        A --> D[Subpackages]
        A --> E[Utilities]
        A --> F[Tests]
        
        B --> B1[Public API]
        B --> B2[Version Info]
        B --> B3[Package Initialization]
        
        C --> C1[main.py]
        C --> C2[core.py]
        C --> C3[models.py]
        
        D --> D1[subpkg1/]
        D --> D2[subpkg2/]
        
        E --> E1[utils.py]
        E --> E2[helpers.py]
        E --> E3[constants.py]
        
        F --> F1[test_main.py]
        F --> F2[test_core.py]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#ffeaa7
    style F fill:#fd79a8
```

## 🔄 Процесс создания пакета

```mermaid
flowchart TD
    A[Планирование пакета] --> B[Создание структуры]
    B --> C[Написание кода]
    C --> D[Создание __init__.py]
    D --> E[Написание тестов]
    E --> F[Создание документации]
    F --> G[Настройка setup.py/pyproject.toml]
    G --> H[Локальное тестирование]
    H --> I{Тесты прошли?}
    I -->|Нет| C
    I -->|Да| J[Сборка пакета]
    J --> K[Публикация]
    
    B --> B1[mkdir mypackage]
    B --> B2[touch __init__.py]
    
    D --> D1[Определить __all__]
    D --> D2[Импортировать модули]
    D --> D3[Установить версию]
    
    G --> G1[Метаданные пакета]
    G --> G2[Зависимости]
    G --> G3[Entry points]
    
    J --> J1[python -m build]
    J --> J2[Создание wheel/sdist]
    
    K --> K1[TestPyPI]
    K --> K2[PyPI]
    
    style A fill:#74b9ff
    style H fill:#00b894
    style K fill:#fd79a8
```

## 📊 Сравнение инструментов управления зависимостями

```mermaid
quadrantChart
    title "Инструменты управления зависимостями"
    x-axis "Простота" --> "Сложность"
    y-axis "Базовый" --> "Продвинутый"
    
    quadrant-1 "Мощные решения"
    quadrant-2 "Избыточная сложность"
    quadrant-3 "Простые инструменты"
    quadrant-4 "Современные решения"
    
    pip: [0.2, 0.3]
    venv: [0.3, 0.2]
    pipenv: [0.6, 0.7]
    poetry: [0.8, 0.9]
    conda: [0.7, 0.8]
```

## 🎪 Виртуальные окружения

```mermaid
graph TB
    subgraph "Virtual Environment Ecosystem"
        A[System Python] --> B[Global site-packages]
        A --> C[Virtual Environment 1]
        A --> D[Virtual Environment 2]
        A --> E[Virtual Environment N]
        
        C --> C1[venv1/lib/python3.x/site-packages]
        C --> C2[venv1/bin/python]
        C --> C3[Project 1 dependencies]
        
        D --> D1[venv2/lib/python3.x/site-packages]
        D --> D2[venv2/bin/python]
        D --> D3[Project 2 dependencies]
        
        E --> E1[venvN/lib/python3.x/site-packages]
        E --> E2[venvN/bin/python]
        E --> E3[Project N dependencies]
        
        F[Activation Script] --> C2
        F --> D2
        F --> E2
    end
    
    style A fill:#74b9ff
    style C fill:#00b894
    style D fill:#ffeaa7
    style E fill:#fd79a8
```

## 🔗 Зависимости пакетов

```mermaid
graph TD
    subgraph "Package Dependencies"
        A[My Package] --> B[requests]
        A --> C[pandas]
        A --> D[click]
        
        B --> B1[urllib3]
        B --> B2[certifi]
        B --> B3[chardet]
        
        C --> C1[numpy]
        C --> C2[python-dateutil]
        C --> C3[pytz]
        
        C1 --> C11[BLAS libraries]
        C2 --> C21[six]
        
        D --> D1[colorama]
        
        style A fill:#74b9ff
        style B fill:#00b894
        style C fill:#ffeaa7
        style D fill:#fd79a8
        style C1 fill:#e17055
    end
```

## 🏭 Фабрика модулей

```mermaid
stateDiagram-v2
    [*] --> ModuleCreation: Create Module
    ModuleCreation --> CodeExecution: Execute Code
    CodeExecution --> NamespacePopulation: Populate Namespace
    NamespacePopulation --> CacheStorage: Store in sys.modules
    CacheStorage --> Ready: Module Ready
    
    Ready --> AttributeAccess: Access Attributes
    AttributeAccess --> Ready: Continue Usage
    
    Ready --> ModuleReload: Reload Module
    ModuleReload --> CodeExecution
    
    Ready --> [*]: Module Cleanup
    
    note right of ModuleCreation
        types.ModuleType()
        __file__, __name__ setup
    end note
    
    note right of CodeExecution
        exec() in module namespace
        Import resolution
    end note
    
    note right of CacheStorage
        sys.modules[name] = module
        Prevent re-execution
    end note
```

## 🎛️ Конфигурация пакета

```mermaid
graph LR
    subgraph "Package Configuration"
        A[setup.py] --> A1[Metadata]
        A --> A2[Dependencies]
        A --> A3[Entry Points]
        A --> A4[Classifiers]
        
        B[pyproject.toml] --> B1[Build System]
        B --> B2[Project Info]
        B --> B3[Tool Config]
        
        C[requirements.txt] --> C1[Production Deps]
        C --> C2[Version Specs]
        
        D[Pipfile] --> D1[Package Sources]
        D --> D2[Dev Dependencies]
        D --> D3[Scripts]
        
        E[poetry.lock] --> E1[Exact Versions]
        E --> E2[Dependency Graph]
        
        F[conda.yml] --> F1[Conda Channels]
        F --> F2[Environment Specs]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#ffeaa7
    style D fill:#fd79a8
```

## 🚀 Жизненный цикл пакета

```mermaid
journey
    title Жизненный цикл Python пакета
    section Разработка
      Планирование: 5: Разработчик
      Создание структуры: 4: Разработчик
      Написание кода: 5: Разработчик
      Локальное тестирование: 3: Разработчик
    section Подготовка
      Написание тестов: 4: Разработчик
      Документация: 3: Разработчик
      Настройка метаданных: 2: Разработчик
      Сборка пакета: 3: Разработчик
    section Публикация
      Тестирование на TestPyPI: 4: Разработчик
      Публикация на PyPI: 5: Разработчик
      Уведомление пользователей: 4: Разработчик
    section Поддержка
      Обновления: 3: Разработчик
      Исправление багов: 2: Разработчик
      Обратная связь: 4: Пользователи
```

## 🔧 Инструменты сборки

```mermaid
flowchart LR
    A[Source Code] --> B{Build Tool}
    
    B -->|setuptools| C[setup.py build]
    B -->|poetry| D[poetry build]
    B -->|flit| E[flit build]
    B -->|hatch| F[hatch build]
    
    C --> G[Wheel + Source Distribution]
    D --> G
    E --> G
    F --> G
    
    G --> H[Upload to PyPI]
    H --> I[pip install package]
    
    I --> J[User Installation]
    
    style A fill:#74b9ff
    style G fill:#00b894
    style H fill:#ffeaa7
    style J fill:#fd79a8
```

## 📈 Эволюция управления пакетами

```mermaid
timeline
    title Эволюция инструментов управления пакетами Python
    
    2000s : distutils
         : setup.py
         : Базовые инструменты сборки
    
    2004  : setuptools
         : pip (позже)
         : Улучшенная сборка пакетов
    
    2008  : virtualenv
         : Изоляция окружений
         : pip + virtualenv
    
    2012  : wheel format
         : Бинарные дистрибутивы
         : Быстрая установка
    
    2017  : pipenv
         : Pipfile/Pipfile.lock
         : Детерминированные сборки
    
    2018  : poetry
         : pyproject.toml
         : Современное управление зависимостями
    
    2021  : pip-tools
         : Разделение зависимостей
         : requirements.in → requirements.txt
```

## 🎯 Лучшие практики структуры

```mermaid
graph TB
    subgraph "Best Practices Package Structure"
        A[mypackage/] --> B[README.md]
        A --> C[LICENSE]
        A --> D[pyproject.toml]
        A --> E[src/mypackage/]
        A --> F[tests/]
        A --> G[docs/]
        A --> H[.gitignore]
        
        E --> E1[__init__.py]
        E --> E2[core.py]
        E --> E3[utils.py]
        E --> E4[cli.py]
        
        F --> F1[test_core.py]
        F --> F2[test_utils.py]
        F --> F3[conftest.py]
        
        G --> G1[index.md]
        G --> G2[api.md]
        G --> G3[examples/]
        
        I[Development Tools] --> I1[.pre-commit-config.yaml]
        I --> I2[tox.ini]
        I --> I3[.github/workflows/]
    end
    
    style A fill:#74b9ff
    style E fill:#00b894
    style F fill:#ffeaa7
    style G fill:#fd79a8
``` 