# Диаграммы: Внешние библиотеки в Python

## 📦 Экосистема Python пакетов

```mermaid
mindmap
  root((Python Ecosystem))
    Package Management
      pip
        PyPI Repository
        requirements.txt
        Version management
      conda
        Anaconda/Miniconda
        Environment management
        Binary packages
      Poetry
        pyproject.toml
        Dependency resolution
        Virtual environments
    
    Scientific Computing
      NumPy
        N-dimensional arrays
        Mathematical functions
        Linear algebra
      SciPy
        Scientific algorithms
        Optimization
        Statistical functions
      Matplotlib
        Data visualization
        Plotting library
        Charts and graphs
    
    Data Analysis
      Pandas
        DataFrames
        Data manipulation
        File I/O
      Jupyter
        Interactive notebooks
        Data exploration
        Visualization
      Seaborn
        Statistical visualization
        Beautiful plots
    
    Web Development
      Flask
        Microframework
        Simple routing
        Template engine
      Django
        Full framework
        ORM included
        Admin interface
      FastAPI
        Modern async
        Auto documentation
        Type hints
    
    Machine Learning
      scikit-learn
        Traditional ML
        Classification
        Regression
      TensorFlow
        Deep learning
        Neural networks
        Google ecosystem
      PyTorch
        Research focused
        Dynamic graphs
        Facebook ecosystem
```

## 🔄 Управление зависимостями

```mermaid
flowchart TD
    A[Python Project] --> B{Dependency Management}
    
    B -->|Traditional| C[pip + requirements.txt]
    B -->|Modern| D[Poetry + pyproject.toml]
    B -->|Scientific| E[conda + environment.yml]
    
    C --> C1[pip install package]
    C --> C2[pip freeze > requirements.txt]
    C --> C3[pip install -r requirements.txt]
    
    D --> D1[poetry add package]
    D --> D2[poetry.lock auto-generated]
    D --> D3[poetry install]
    
    E --> E1[conda install package]
    E --> E2[environment.yml manual]
    E --> E3[conda env create -f environment.yml]
    
    subgraph "Virtual Environments"
        F[venv] --> F1[python -m venv env]
        G[virtualenv] --> G1[virtualenv env]
        H[conda env] --> H1[conda create -n env]
        I[poetry env] --> I1[poetry shell]
    end
    
    C -.-> F
    D -.-> I
    E -.-> H
    
    style D fill:#c8e6c9
    style I fill:#c8e6c9
```

## 🧪 Научные библиотеки - иерархия

```mermaid
graph TD
    subgraph "Foundation Layer"
        A[NumPy] --> A1[N-dimensional arrays]
        A --> A2[Mathematical functions]
        A --> A3[Broadcasting]
    end
    
    subgraph "Scientific Layer"
        B[SciPy] --> B1[Optimization]
        B --> B2[Integration]
        B --> B3[Statistics]
        B --> B4[Signal Processing]
        
        C[Matplotlib] --> C1[2D Plotting]
        C --> C2[3D Plotting]
        C --> C3[Animations]
    end
    
    subgraph "Data Analysis Layer"
        D[Pandas] --> D1[DataFrames]
        D --> D2[Time Series]
        D --> D3[Data I/O]
        
        E[Seaborn] --> E1[Statistical Plots]
        E --> E2[Distribution Plots]
        
        F[Plotly] --> F1[Interactive Plots]
        F --> F2[Web Visualization]
    end
    
    subgraph "Machine Learning Layer"
        G[scikit-learn] --> G1[Classification]
        G --> G2[Regression]
        G --> G3[Clustering]
        
        H[TensorFlow] --> H1[Deep Learning]
        H --> H2[Neural Networks]
        
        I[PyTorch] --> I1[Research ML]
        I --> I2[Dynamic Graphs]
    end
    
    A --> B
    A --> C
    A --> D
    C --> E
    C --> F
    D --> G
    A --> H
    A --> I
    
    style A fill:#ff9999
    style D fill:#66b3ff
    style G fill:#99ff99
```

## 📊 Pandas DataFrame операции

```mermaid
sequenceDiagram
    participant User as User Code
    participant DF as DataFrame
    participant Index as Index
    participant Series as Series
    participant Engine as Pandas Engine
    
    User->>DF: pd.DataFrame(data)
    DF->>Index: Create index
    DF->>Series: Create columns
    
    User->>DF: df['column']
    DF->>Series: Return Series
    
    User->>DF: df.groupby('key')
    DF->>Engine: Group operations
    Engine->>DF: GroupBy object
    
    User->>DF: df.agg(functions)
    DF->>Engine: Apply aggregation
    Engine->>DF: Aggregated result
    
    User->>DF: df.merge(other)
    DF->>Engine: Join operation
    Engine->>DF: Merged DataFrame
    
    User->>DF: df.to_csv(filename)
    DF->>Engine: Serialize data
    Engine-->>User: File written
    
    Note over User,Engine: Pandas optimizes operations<br/>using Cython and NumPy
```

## 🌐 Веб-фреймворки сравнение

```mermaid
graph LR
    subgraph "Microframeworks"
        A[Flask] --> A1[Minimal core]
        A --> A2[Extensions]
        A --> A3[Flexibility]
        
        B[FastAPI] --> B1[Async support]
        B --> B2[Auto docs]
        B --> B3[Type hints]
    end
    
    subgraph "Full Frameworks"
        C[Django] --> C1[Batteries included]
        C --> C2[ORM built-in]
        C --> C3[Admin interface]
        C --> C4[Security features]
        
        D[Pyramid] --> D1[Flexible config]
        D --> D2[Multiple backends]
        D --> D3[Enterprise ready]
    end
    
    subgraph "Async Frameworks"
        E[Sanic] --> E1[High performance]
        E --> E2[Async/await]
        
        F[Quart] --> F1[Flask-like API]
        F --> F2[Async support]
        
        G[Starlette] --> G1[ASGI framework]
        G --> G2[WebSocket support]
    end
    
    subgraph "Use Cases"
        H[Prototypes/APIs] -.-> A
        I[Production APIs] -.-> B
        J[Full Web Apps] -.-> C
        K[Enterprise] -.-> D
        L[High Performance] -.-> E
        M[Async Web Apps] -.-> G
    end
    
    style A fill:#e1f5fe
    style B fill:#c8e6c9
    style C fill:#fff3e0
```

## 🔍 HTTP библиотеки

```mermaid
stateDiagram-v2
    [*] --> Request_Created
    
    Request_Created --> Preparing: Add headers, params
    Preparing --> Connecting: Establish connection
    Connecting --> Sending: Send request data
    Sending --> Waiting: Wait for response
    Waiting --> Receiving: Receive response
    Receiving --> Parsing: Parse response
    Parsing --> Complete: Response ready
    
    Connecting --> Connection_Error: Network error
    Sending --> Timeout_Error: Request timeout
    Waiting --> Timeout_Error: Response timeout
    Receiving --> HTTP_Error: 4xx/5xx status
    
    Connection_Error --> Retry: Retry logic
    Timeout_Error --> Retry: Retry logic
    HTTP_Error --> Error_Handling: Handle error
    Retry --> Connecting: Retry connection
    
    Complete --> [*]
    Error_Handling --> [*]
    
    note right of Preparing
        requests library handles:
        - SSL verification
        - Cookie persistence
        - Authentication
        - Redirects
    end note
    
    note right of Parsing
        Automatic parsing:
        - JSON responses
        - XML responses
        - Binary content
        - Text encoding
    end note
```

## 📈 NumPy массивы - архитектура

```mermaid
graph TB
    subgraph "NumPy Array Object"
        A[ndarray] --> B[Data pointer]
        A --> C[Shape tuple]
        A --> D[Strides tuple]
        A --> E[Data type]
        A --> F[Flags]
        
        B --> G[Contiguous memory block]
        C --> H["(rows, cols, depth)"]
        D --> I["Memory layout info"]
        E --> J[dtype object]
        F --> K[C_CONTIGUOUS, WRITEABLE, etc.]
    end
    
    subgraph "Memory Layout"
        L["C-order (row-major)"] --> L1["[1,2,3,4,5,6] → [[1,2,3],[4,5,6]]"]
        M["Fortran-order (column-major)"] --> M1["[1,2,3,4,5,6] → [[1,4],[2,5],[3,6]]"]
    end
    
    subgraph "Operations"
        N[Broadcasting] --> N1[Shape compatibility]
        O[Vectorization] --> O1[Element-wise ops]
        P[Views vs Copies] --> P1[Memory efficiency]
    end
    
    G -.-> L
    G -.-> M
    A -.-> N
    A -.-> O
    A -.-> P
    
    style A fill:#ff9999
    style G fill:#ffcc99
    style N fill:#99ff99
```

## 🗄️ Работа с базами данных

```mermaid
flowchart LR
    subgraph "Python Application"
        A[Python Code] --> B[Database Library]
    end
    
    subgraph "Database Libraries"
        B --> C[sqlite3]
        B --> D[psycopg2]
        B --> E[pymongo]
        B --> F[SQLAlchemy]
    end
    
    subgraph "Database Systems"
        C --> G[SQLite File]
        D --> H[PostgreSQL Server]
        E --> I[MongoDB Server]
        F --> J[Any SQL Database]
    end
    
    subgraph "ORM Layer"
        K[SQLAlchemy ORM] --> F
        L[Django ORM] --> M[django.db]
        N[Peewee ORM] --> O[peewee.db]
        P[Tortoise ORM] --> Q[async support]
    end
    
    subgraph "Operations"
        R[CRUD Operations]
        S[Transactions]
        T[Migrations]
        U[Connection Pooling]
        V[Query Optimization]
    end
    
    F -.-> R
    F -.-> S
    F -.-> T
    F -.-> U
    F -.-> V
    
    style F fill:#c8e6c9
    style K fill:#e1f5fe
```

## 🔧 Установка и управление пакетами

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant pip as pip
    participant PyPI as PyPI Repository
    participant Local as Local Environment
    participant VEnv as Virtual Environment
    
    Dev->>VEnv: python -m venv myenv
    VEnv->>Dev: Environment created
    
    Dev->>VEnv: source myenv/bin/activate
    VEnv->>Dev: Environment activated
    
    Dev->>pip: pip install requests
    pip->>PyPI: Search for requests
    PyPI->>pip: Package metadata
    pip->>PyPI: Download package + dependencies
    PyPI->>pip: Package files
    pip->>Local: Install package
    Local->>Dev: Package available
    
    Dev->>pip: pip freeze
    pip->>Local: List installed packages
    Local->>pip: Package list
    pip->>Dev: requirements.txt format
    
    Dev->>pip: pip install -r requirements.txt
    pip->>PyPI: Batch download
    PyPI->>pip: All packages
    pip->>Local: Batch install
    
    Note over Dev,Local: Virtual environment isolates<br/>dependencies from system Python
```

## 📊 Matplotlib архитектура

```mermaid
graph TD
    subgraph "Matplotlib Architecture"
        A[Figure] --> B[Axes]
        B --> C[Artist Objects]
        
        A --> D[Canvas]
        D --> E[Backend]
        
        C --> F[Primitive Artists]
        C --> G[Composite Artists]
        
        F --> H[Line2D, Rectangle, Text]
        G --> I[Axis, Tick, Legend]
        
        E --> J[Interactive Backends]
        E --> K[Non-interactive Backends]
        
        J --> L[Qt5Agg, TkAgg, notebook]
        K --> M[Agg, SVG, PDF, PS]
    end
    
    subgraph "Plotting Interfaces"
        N[pyplot] --> O[MATLAB-like interface]
        P[Object-oriented] --> Q[Direct object manipulation]
        R[Seaborn] --> S[Statistical plotting]
    end
    
    N -.-> A
    P -.-> B
    R -.-> N
    
    subgraph "Output Formats"
        T[PNG, JPG] 
        U[SVG, PDF]
        V[Interactive HTML]
        W[Animation GIF/MP4]
    end
    
    M --> T
    M --> U
    L --> V
    L --> W
    
    style A fill:#ff9999
    style B fill:#66b3ff
    style C fill:#99ff99
```

## 🤖 Машинное обучение - workflow

```mermaid
flowchart TD
    A[Raw Data] --> B[Data Preprocessing]
    B --> C[Feature Engineering]
    C --> D[Data Splitting]
    D --> E[Model Selection]
    E --> F[Model Training]
    F --> G[Model Evaluation]
    G --> H{Performance OK?}
    
    H -->|No| I[Hyperparameter Tuning]
    I --> E
    
    H -->|Yes| J[Model Validation]
    J --> K[Model Deployment]
    
    subgraph "Libraries Used"
        L[Pandas] -.-> B
        M[NumPy] -.-> C
        N[scikit-learn] -.-> D
        N -.-> E
        N -.-> F
        N -.-> G
        O[TensorFlow/PyTorch] -.-> F
        P[Matplotlib/Seaborn] -.-> G
    end
    
    subgraph "ML Models"
        Q[Linear Regression]
        R[Random Forest]
        S[Neural Networks]
        T[SVM]
        U[Clustering]
    end
    
    E -.-> Q
    E -.-> R
    E -.-> S
    E -.-> T
    E -.-> U
    
    style F fill:#c8e6c9
    style G fill:#fff3e0
    style K fill:#ffcdd2
```

## 🔄 Асинхронное программирование

```mermaid
sequenceDiagram
    participant Main as Main Thread
    participant EventLoop as Event Loop
    participant Task1 as Async Task 1
    participant Task2 as Async Task 2
    participant IO as I/O Operation
    
    Main->>EventLoop: "asyncio.run(main())"
    EventLoop->>Task1: Create task
    EventLoop->>Task2: Create task
    
    EventLoop->>Task1: Start execution
    Task1->>IO: "await http_request()"
    Note over Task1,IO: Task 1 suspended
    
    EventLoop->>Task2: Start execution
    Task2->>Task2: CPU work
    Task2->>EventLoop: Complete
    
    IO->>Task1: Response ready
    Task1->>EventLoop: Resume & complete
    
    EventLoop->>Main: All tasks done
    
    Note over Main,IO: Event loop manages<br/>concurrent execution<br/>without threads
```

## 📦 Популярные библиотеки по категориям

```mermaid
graph LR
    subgraph "Web Scraping"
        A[requests] --> A1[HTTP client]
        B[BeautifulSoup] --> B1[HTML parsing]
        C[Scrapy] --> C1[Web crawler]
        D[Selenium] --> D1[Browser automation]
    end
    
    subgraph "API Development"
        E[Flask] --> E1[Microframework]
        F[Django REST] --> F1[Full framework]
        G[FastAPI] --> G1[Modern async]
        H[Starlette] --> H1[ASGI base]
    end
    
    subgraph "Data Processing"
        I[Pandas] --> I1[DataFrames]
        J[NumPy] --> J1[Arrays]
        K[Dask] --> K1[Parallel computing]
        L[Apache Arrow] --> L1[Columnar data]
    end
    
    subgraph "Testing"
        M[pytest] --> M1[Testing framework]
        N[unittest] --> N1[Built-in testing]
        O[mock] --> O1[Mocking objects]
        P[coverage] --> P1[Code coverage]
    end
    
    subgraph "GUI Development"
        Q[Tkinter] --> Q1[Built-in GUI]
        R[PyQt/PySide] --> R1[Cross-platform]
        S[Kivy] --> S1[Mobile/touch]
        T[wxPython] --> T1[Native look]
    end
    
    style A fill:#e1f5fe
    style E fill:#c8e6c9
    style I fill:#fff3e0
    style M fill:#fce4ec
    style Q fill:#f3e5f5
```

## ⚡ Производительность библиотек

```mermaid
xychart-beta
    title "Сравнение производительности HTTP библиотек"
    x-axis [requests, httpx, aiohttp, urllib3]
    y-axis "Requests per second" 0 --> 1000
    bar [150, 300, 800, 400]
```

```mermaid
xychart-beta
    title "Время обработки данных (1M записей)"
    x-axis [Pure Python, NumPy, Pandas, Dask]
    y-axis "Время (секунды)" 0 --> 100
    line [95, 5, 8, 3]
```

## 🔐 Безопасность внешних библиотек

```mermaid
flowchart TD
    A[External Library] --> B{Security Check}
    
    B --> C[Known Vulnerabilities]
    B --> D[License Compatibility]
    B --> E[Maintenance Status]
    B --> F[Code Quality]
    
    C --> G[CVE Database]
    C --> H[Safety Check]
    C --> I[Snyk Scan]
    
    D --> J[MIT, Apache, BSD]
    D --> K[GPL Compatibility]
    
    E --> L[Last Update]
    E --> M[GitHub Activity]
    E --> N[Download Stats]
    
    F --> O[Code Review]
    F --> P[Test Coverage]
    F --> Q[Documentation]
    
    subgraph "Security Tools"
        R[bandit] --> S[Code security scan]
        T[safety] --> U[Vulnerability check]
        V[pip-audit] --> W[Dependency audit]
    end
    
    H -.-> T
    I -.-> V
    O -.-> R
    
    style C fill:#ffcdd2
    style D fill:#fff3e0
    style E fill:#c8e6c9
```

## 📈 Тренды популярности библиотек

```mermaid
flowchart TD
    subgraph "Python Ecosystem Timeline"
        A[2015: Python Foundation] --> B[Scientific Computing]
        A --> C[Web Development]
        A --> D[Machine Learning]
        
        B --> B1[NumPy dominance]
        B1 --> B2[Pandas growth]
        B2 --> B3[Matplotlib standard]
        B3 --> B4[Seaborn popular]
        
        C --> C1[Flask popular]
        C1 --> C2[Django stable]
        C2 --> C3[FastAPI emerges]
        
        D --> D1[scikit-learn stable]
        D1 --> D2[TensorFlow rise]
        D2 --> D3[PyTorch adoption]
        
        B4 --> E[2024: Current state]
        C3 --> E
        D3 --> E
    end
    
    style A fill:#ffeb3b
    style E fill:#4caf50
    style B fill:#2196f3
    style C fill:#ff9800
    style D fill:#9c27b0
```

## 🔄 Управление версиями пакетов

```mermaid
stateDiagram-v2
    [*] --> Development
    
    Development --> Testing: pip install package
    Testing --> Staging: requirements.txt
    Staging --> Production: Locked versions
    
    state Development {
        [*] --> Latest
        Latest --> Specific: Version conflict
        Specific --> Latest: Update needed
    }
    
    state Testing {
        [*] --> Integration
        Integration --> Unit: Test suite
        Unit --> Integration: CI/CD
    }
    
    state Production {
        [*] --> Stable
        Stable --> Hotfix: Critical bug
        Hotfix --> Stable: Patch applied
    }
    
    Production --> Development: New feature cycle
    
    note right of Production
        Use exact versions
        in production:
        package==1.2.3
    end note
    
    note right of Development
        Use flexible versions
        in development:
        package>=1.2.0,<2.0.0
    end note
``` 