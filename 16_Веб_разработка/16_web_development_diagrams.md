# Диаграммы: Веб-разработка на Python

## 🌐 Архитектура веб-приложений

### Общая архитектура веб-приложения

```mermaid
graph TD
    A[Client Browser] --> B[Web Server<br/>Nginx/Apache]
    B --> C[WSGI Server<br/>Gunicorn/uWSGI]
    C --> D[Python Web Framework<br/>Flask/FastAPI/Django]
    
    D --> E[Business Logic]
    D --> F[Database Layer]
    D --> G[Cache Layer]
    D --> H[External APIs]
    
    E --> E1[Controllers/Views]
    E --> E2[Services]
    E --> E3[Models]
    
    F --> F1[PostgreSQL]
    F --> F2[MongoDB]
    F --> F3[SQLite]
    
    G --> G1[Redis]
    G --> G2[Memcached]
    
    H --> H1[REST APIs]
    H --> H2[Third-party Services]
    
    style A fill:#e3f2fd
    style D fill:#c8e6c9
    style E fill:#fff3e0
    style F fill:#f3e5f5
    style G fill:#fce4ec
    style H fill:#e8f5e8
```

### MVC vs MVP vs MVVM паттерны

```mermaid
graph TD
    A[Architectural Patterns] --> B[MVC<br/>Model-View-Controller]
    A --> C[MVP<br/>Model-View-Presenter]
    A --> D[MVVM<br/>Model-View-ViewModel]
    
    B --> B1[Model ↔ Controller ↔ View]
    B --> B2[Django, Flask]
    B --> B3[Server-side rendering]
    
    C --> C1[Model ↔ Presenter ↔ View]
    C --> C2[Better testability]
    C --> C3[Loose coupling]
    
    D --> D1[Model ↔ ViewModel ↔ View]
    D --> D2[Data binding]
    D --> D3[Frontend frameworks]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

## 🚀 Flask Framework

### Flask архитектура и компоненты

```mermaid
graph TD
    A[Flask Application] --> B[Blueprint System]
    A --> C[Request Context]
    A --> D[Application Context]
    A --> E[Extensions]
    
    B --> B1[Modular design]
    B --> B2[URL routing]
    B --> B3[Template organization]
    
    C --> C1[request object]
    C --> C2[session object]
    C --> C3[g object]
    
    D --> D1[current_app]
    D --> D2[Application config]
    D --> D3[Teardown handlers]
    
    E --> E1[Flask-SQLAlchemy]
    E --> E2[Flask-Login]
    E --> E3[Flask-WTF]
    E --> E4[Flask-Mail]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Flask Request Lifecycle

```mermaid
sequenceDiagram
    participant Client
    participant Flask
    participant Blueprint
    participant View
    participant Database
    participant Template
    
    Client->>Flask: HTTP Request
    Flask->>Flask: Create Request Context
    Flask->>Blueprint: Route Resolution
    Blueprint->>View: Execute View Function
    
    alt Database Operation
        View->>Database: Query Data
        Database-->>View: Return Results
    end
    
    View->>Template: Render Template
    Template-->>View: HTML Response
    View-->>Flask: Response Object
    Flask->>Flask: Teardown Context
    Flask-->>Client: HTTP Response
```

### Flask vs FastAPI сравнение

```mermaid
graph LR
    A[Web Framework Choice] --> B[Flask]
    A --> C[FastAPI]
    
    B --> B1[✅ Простота]
    B --> B2[✅ Гибкость]
    B --> B3[✅ Большая экосистема]
    B --> B4[❌ Нет встроенной валидации]
    B --> B5[❌ Sync по умолчанию]
    
    C --> C1[✅ Автоматическая валидация]
    C --> C2[✅ OpenAPI/Swagger]
    C --> C3[✅ Async/await]
    C --> C4[✅ Type hints]
    C --> C5[❌ Меньше расширений]
    
    style B fill:#ffeb3b
    style C fill:#4caf50
```

## ⚡ FastAPI Framework

### FastAPI архитектура

```mermaid
graph TD
    A[FastAPI Application] --> B[Pydantic Models]
    A --> C[Dependency Injection]
    A --> D[OpenAPI Generation]
    A --> E[ASGI Support]
    
    B --> B1[Request validation]
    B --> B2[Response serialization]
    B --> B3[Type safety]
    
    C --> C1[Database connections]
    C --> C2[Authentication]
    C --> C3[Configuration]
    
    D --> D1[Automatic docs]
    D --> D2[Client generation]
    D --> D3[API specification]
    
    E --> E1[High performance]
    E --> E2[Async support]
    E --> E3[WebSocket support]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### FastAPI Request Processing

```mermaid
flowchart TD
    A[HTTP Request] --> B{Route Exists?}
    B -->|No| C[404 Not Found]
    B -->|Yes| D[Parse Path Parameters]
    
    D --> E[Validate Query Parameters]
    E --> F{Valid Parameters?}
    F -->|No| G[422 Validation Error]
    F -->|Yes| H[Parse Request Body]
    
    H --> I[Validate Request Model]
    I --> J{Valid Model?}
    J -->|No| K[422 Validation Error]
    J -->|Yes| L[Resolve Dependencies]
    
    L --> M[Execute Route Handler]
    M --> N[Validate Response Model]
    N --> O[Serialize Response]
    O --> P[Return HTTP Response]
    
    style A fill:#e3f2fd
    style B fill:#ffffcc
    style F fill:#ffffcc
    style J fill:#ffffcc
    style P fill:#c8e6c9
```

## 🌐 HTTP Protocol

### HTTP Request/Response Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    
    Note over C,S: HTTP Request
    C->>S: Request Line (GET /api/users HTTP/1.1)
    C->>S: Headers (Content-Type, Authorization, etc.)
    C->>S: Body (for POST/PUT)
    
    Note over S: Processing
    S->>S: Parse Request
    S->>S: Route to Handler
    S->>S: Business Logic
    S->>S: Generate Response
    
    Note over C,S: HTTP Response
    S-->>C: Status Line (HTTP/1.1 200 OK)
    S-->>C: Headers (Content-Type, Set-Cookie, etc.)
    S-->>C: Body (HTML, JSON, etc.)
```

### HTTP Status Codes

```mermaid
graph TD
    A[HTTP Status Codes] --> B[1xx Informational]
    A --> C[2xx Success]
    A --> D[3xx Redirection]
    A --> E[4xx Client Error]
    A --> F[5xx Server Error]
    
    B --> B1[100 Continue]
    B --> B2[101 Switching Protocols]
    
    C --> C1[200 OK]
    C --> C2[201 Created]
    C --> C3[204 No Content]
    
    D --> D1[301 Moved Permanently]
    D --> D2[302 Found]
    D --> D3[304 Not Modified]
    
    E --> E1[400 Bad Request]
    E --> E2[401 Unauthorized]
    E --> E3[404 Not Found]
    E --> E4[422 Unprocessable Entity]
    
    F --> F1[500 Internal Server Error]
    F --> F2[502 Bad Gateway]
    F --> F3[503 Service Unavailable]
    
    style C fill:#c8e6c9
    style E fill:#ffcdd2
    style F fill:#ff5722
```

## 🕷️ Web Scraping

### Web Scraping Architecture

```mermaid
graph TD
    A[Web Scraping System] --> B[HTTP Client<br/>requests/httpx]
    A --> C[HTML Parser<br/>BeautifulSoup/lxml]
    A --> D[Data Storage<br/>Database/Files]
    A --> E[Rate Limiting]
    A --> F[Error Handling]
    
    B --> B1[Session management]
    B --> B2[Headers/Cookies]
    B --> B3[Proxy support]
    
    C --> C1[CSS selectors]
    C --> C2[XPath queries]
    C --> C3[Text extraction]
    
    D --> D1[Structured data]
    D --> D2[Raw HTML]
    D --> D3[Media files]
    
    E --> E1[Delays between requests]
    E --> E2[Concurrent limits]
    E --> E3[Respectful scraping]
    
    F --> F1[Retry logic]
    F --> F2[Error logging]
    F --> F3[Graceful degradation]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#fce4ec
    style F fill:#e8f5e8
```

### Beautiful Soup селекторы

```mermaid
graph LR
    A[BeautifulSoup Selectors] --> B[Tag Selectors]
    A --> C[Attribute Selectors]
    A --> D[CSS Selectors]
    A --> E[XPath-like]
    
    B --> B1["soup.find('div')"]
    B --> B2["soup.find_all('p')"]
    B --> B3["soup.select('h1')"]
    
    C --> C1["find(attrs={'class': 'name'})"]
    C --> C2["find('a', href=True)"]
    C --> C3["find(id='header')"]
    
    D --> D1["select('.class-name')"]
    D --> D2["select('#element-id')"]
    D --> D3["select('div > p')"]
    D --> D4["select('[data-value]')"]
    
    E --> E1["find_next()"]
    E --> E2["find_previous()"]
    E --> E3["find_parent()"]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

## 🔗 WebSocket Communication

### WebSocket vs HTTP

```mermaid
graph TD
    A[Communication Patterns] --> B[HTTP Request/Response]
    A --> C[WebSocket Full-Duplex]
    
    B --> B1[👥 Client initiates]
    B --> B2[📤 Request → Response]
    B --> B3[🔄 Stateless]
    B --> B4[⏱️ Higher latency]
    
    C --> C1[🔄 Bidirectional]
    C --> C2[💬 Real-time messaging]
    C --> C3[📊 Persistent connection]
    C --> C4[⚡ Lower latency]
    
    B --> D[👍 REST APIs<br/>Web pages<br/>File downloads]
    C --> E[👍 Chat applications<br/>Live updates<br/>Gaming<br/>Trading platforms]
    
    style B fill:#ffcdd2
    style C fill:#c8e6c9
    style D fill:#fff3e0
    style E fill:#e8f5e8
```

### WebSocket Lifecycle

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: WebSocket Handshake
    Client->>Server: HTTP Upgrade Request
    Server-->>Client: HTTP 101 Switching Protocols
    
    Note over Client,Server: WebSocket Communication
    Client->>Server: WebSocket Frame (Message 1)
    Server->>Client: WebSocket Frame (Response 1)
    Server->>Client: WebSocket Frame (Push Message)
    Client->>Server: WebSocket Frame (Message 2)
    
    Note over Client,Server: Connection Management
    Client->>Server: Ping Frame
    Server-->>Client: Pong Frame
    
    Note over Client,Server: Connection Close
    Client->>Server: Close Frame
    Server-->>Client: Close Frame
    Note over Client,Server: Connection Closed
```

## 🚀 Deployment Strategies

### Deployment архитектура

```mermaid
graph TD
    A[Deployment Options] --> B[Development]
    A --> C[Staging]
    A --> D[Production]
    
    B --> B1[Flask dev server]
    B --> B2[Debug mode]
    B --> B3[Auto-reload]
    
    C --> C1[Gunicorn + Nginx]
    C --> C2[Docker containers]
    C --> C3[Environment parity]
    
    D --> D1[Load Balancer]
    D --> D2[Multiple Workers]
    D --> D3[Health Checks]
    D --> D4[Monitoring]
    
    D1 --> E[Server 1<br/>Gunicorn]
    D1 --> F[Server 2<br/>Gunicorn]
    D1 --> G[Server N<br/>Gunicorn]
    
    style A fill:#e3f2fd
    style B fill:#ffcdd2
    style C fill:#fff3e0
    style D fill:#c8e6c9
```

### Container Deployment

```mermaid
graph LR
    A[Container Strategy] --> B[Single Container]
    A --> C[Multi-Container]
    A --> D[Orchestration]
    
    B --> B1[App + Database]
    B --> B2[Simple deployment]
    B --> B3[Development/Testing]
    
    C --> C1[Separate services]
    C --> C2[Docker Compose]
    C --> C3[Service isolation]
    
    D --> D1[Kubernetes]
    D --> D2[Docker Swarm]
    D --> D3[Auto-scaling]
    D --> D4[High availability]
    
    style A fill:#e3f2fd
    style B fill:#ffcdd2
    style C fill:#fff3e0
    style D fill:#c8e6c9
```

## 📊 Performance Optimization

### Web Application Performance

```mermaid
graph TD
    A[Performance Optimization] --> B[Frontend]
    A --> C[Backend]
    A --> D[Database]
    A --> E[Infrastructure]
    
    B --> B1[Minification]
    B --> B2[Compression]
    B --> B3[Caching]
    B --> B4[CDN]
    
    C --> C1[Async/await]
    C --> C2[Connection pooling]
    C --> C3[Response caching]
    C --> C4[Code optimization]
    
    D --> D1[Query optimization]
    D --> D2[Indexing]
    D --> D3[Connection pooling]
    D --> D4[Read replicas]
    
    E --> E1[Load balancing]
    E --> E2[Auto-scaling]
    E --> E3[Monitoring]
    E --> E4[Health checks]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Caching Strategies

```mermaid
graph TD
    A[Caching Layers] --> B[Browser Cache]
    A --> C[CDN Cache]
    A --> D[Reverse Proxy Cache]
    A --> E[Application Cache]
    A --> F[Database Cache]
    
    B --> B1[Static assets]
    B --> B2[HTML pages]
    
    C --> C1[Global distribution]
    C --> C2[Edge locations]
    
    D --> D1[Nginx cache]
    D --> D2[Varnish]
    
    E --> E1[Redis]
    E --> E2[Memcached]
    E --> E3[In-memory cache]
    
    F --> F1[Query result cache]
    F --> F2[Buffer pool]
    
    style A fill:#e3f2fd
    style B fill:#e8f5e8
    style C fill:#f3e5f5
    style D fill:#fff3e0
    style E fill:#c8e6c9
    style F fill:#fce4ec
```

Эти диаграммы охватывают все аспекты веб-разработки на Python от архитектуры до развертывания. 