# Диаграммы: Базы данных в Python

## 🗄️ Архитектура работы с базами данных

### Слои доступа к данным

```mermaid
graph TD
    A[Application Layer] --> B[ORM Layer<br/>SQLAlchemy]
    A --> C[Database API<br/>sqlite3, psycopg2]
    
    B --> D[Query Builder]
    B --> E[Model Definitions]
    B --> F[Session Management]
    
    C --> G[Raw SQL]
    C --> H[Connection Management]
    C --> I[Transaction Control]
    
    D --> J[Database Engine]
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J
    
    J --> K[SQLite]
    J --> L[PostgreSQL]
    J --> M[MySQL]
    J --> N[Oracle]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style J fill:#f3e5f5
```

### Database Abstraction Layers

```mermaid
graph LR
    A[Python Database Access] --> B[High Level<br/>ORM]
    A --> C[Mid Level<br/>Query Builder]
    A --> D[Low Level<br/>DB-API]
    
    B --> B1[SQLAlchemy ORM]
    B --> B2[Django ORM]
    B --> B3[Peewee]
    B --> B4[Tortoise ORM]
    
    C --> C1[SQLAlchemy Core]
    C --> C2[Raw SQL with helpers]
    
    D --> D1[sqlite3]
    D --> D2[psycopg2]
    D --> D3[PyMySQL]
    D --> D4[cx_Oracle]
    
    B1 --> E[🎯 Object mapping<br/>🔄 Relationships<br/>📝 Migrations]
    C1 --> F[⚡ Performance<br/>🔧 Flexibility<br/>📊 Complex queries]
    D1 --> G[🚀 Speed<br/>🎛️ Full control<br/>⚠️ More code]
    
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#ffcdd2
```

## 🗃️ SQLite Architecture

### SQLite внутренняя архитектура

```mermaid
graph TD
    A[SQLite Engine] --> B[SQL Command Processor]
    B --> C[Parser]
    B --> D[Code Generator]
    B --> E[Virtual Machine]
    
    C --> F[Tokenizer]
    C --> G[Parser Tree]
    
    D --> H[Bytecode Generation]
    
    E --> I[Virtual Database Engine]
    I --> J[B-Tree]
    I --> K[Pager]
    I --> L[OS Interface]
    
    J --> M[Table B-Trees]
    J --> N[Index B-Trees]
    
    K --> O[Page Cache]
    K --> P[Lock Manager]
    
    L --> Q[File System]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style I fill:#fff3e0
    style J fill:#f3e5f5
```

### SQLite vs Server Databases

```mermaid
graph LR
    A[Database Types] --> B[SQLite<br/>Embedded]
    A --> C[PostgreSQL/MySQL<br/>Server-based]
    
    B --> B1[✅ Zero configuration]
    B --> B2[✅ Single file]
    B --> B3[✅ Cross-platform]
    B --> B4[✅ ACID compliant]
    B --> B5[❌ No concurrent writes]
    B --> B6[❌ Limited scalability]
    
    C --> C1[✅ High concurrency]
    C --> C2[✅ Advanced features]
    C --> C3[✅ User management]
    C --> C4[✅ Network access]
    C --> C5[❌ Complex setup]
    C --> C6[❌ Resource overhead]
    
    style B fill:#c8e6c9
    style C fill:#fff3e0
```

## 🏛️ SQLAlchemy ORM

### SQLAlchemy Architecture

```mermaid
graph TD
    A[SQLAlchemy ORM] --> B[Declarative Base]
    A --> C[Session]
    A --> D[Query]
    A --> E[Relationships]
    
    B --> F[Model Classes]
    B --> G[Table Metadata]
    B --> H[Column Definitions]
    
    C --> I[Unit of Work]
    C --> J[Identity Map]
    C --> K[Transaction Management]
    
    D --> L[Query Builder]
    D --> M[Lazy Loading]
    D --> N[Eager Loading]
    
    E --> O[One-to-Many]
    E --> P[Many-to-Many]
    E --> Q[One-to-One]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### SQLAlchemy Session Lifecycle

```mermaid
sequenceDiagram
    participant App as Application
    participant Session as SQLAlchemy Session
    participant DB as Database
    
    App->>Session: Create Session
    App->>Session: Query Objects
    Session->>DB: SELECT queries
    DB-->>Session: Result sets
    Session-->>App: Python objects
    
    App->>Session: Modify objects
    Note over Session: Changes tracked in Unit of Work
    
    App->>Session: session.commit()
    Session->>DB: BEGIN transaction
    Session->>DB: INSERT/UPDATE/DELETE
    Session->>DB: COMMIT transaction
    DB-->>Session: Success
    Session-->>App: Commit complete
    
    App->>Session: session.close()
    Note over Session: Session closed, objects detached
```

### ORM Relationships

```mermaid
graph TD
    A[ORM Relationships] --> B[One-to-Many]
    A --> C[Many-to-Many]
    A --> D[One-to-One]
    
    B --> B1[Parent has many Children]
    B --> B2[Foreign Key in Child]
    B --> B3["relationship() + backref"]
    
    C --> C1[Association Table]
    C --> C2[Many Parents, Many Children]
    C --> C3[secondary parameter]
    
    D --> D1[Unique Foreign Key]
    D --> D2[uselist=False]
    D --> D3[Bidirectional link]
    
    B --> E["class Parent:\n    children = relationship('Child')"]
    C --> F["class Student:\n    courses = relationship('Course',\n                        secondary=association_table)"]
    D --> G["class User:\n    profile = relationship('Profile',\n                       uselist=False)"]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

## 🔄 Транзакции и ACID

### ACID Properties

```mermaid
graph TD
    A[ACID Properties] --> B[Atomicity<br/>Атомарность]
    A --> C[Consistency<br/>Согласованность]
    A --> D[Isolation<br/>Изолированность]
    A --> E[Durability<br/>Долговечность]
    
    B --> B1[All or Nothing]
    B --> B2[Transaction успешна<br/>или откатывается полностью]
    
    C --> C1[Database Constraints]
    C --> C2[Данные остаются<br/>в корректном состоянии]
    
    D --> D1[Concurrent Transactions]
    D --> D2[Транзакции не влияют<br/>друг на друга]
    
    E --> E1[Persistent Storage]
    E --> E2[Committed данные<br/>сохраняются навсегда]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Transaction Isolation Levels

```mermaid
graph TD
    A[Isolation Levels] --> B[Read Uncommitted<br/>Уровень 0]
    A --> C[Read Committed<br/>Уровень 1]
    A --> D[Repeatable Read<br/>Уровень 2]
    A --> E[Serializable<br/>Уровень 3]
    
    B --> B1[😱 Dirty Reads]
    B --> B2[😱 Non-repeatable Reads]
    B --> B3[😱 Phantom Reads]
    
    C --> C1[✅ No Dirty Reads]
    C --> C2[😱 Non-repeatable Reads]
    C --> C3[😱 Phantom Reads]
    
    D --> D1[✅ No Dirty Reads]
    D --> D2[✅ No Non-repeatable Reads]
    D --> D3[😱 Phantom Reads]
    
    E --> E1[✅ No Dirty Reads]
    E --> E2[✅ No Non-repeatable Reads]
    E --> E3[✅ No Phantom Reads]
    
    F[Performance] --> G[Fast ⚡]
    F --> H[Medium 🚶]
    F --> I[Slow 🐌]
    F --> J[Slowest 🐢]
    
    B -.-> G
    C -.-> H
    D -.-> I
    E -.-> J
    
    style B fill:#ffcdd2
    style E fill:#c8e6c9
```

## 🏗️ Repository Pattern

### Repository Pattern Architecture

```mermaid
graph TD
    A[Repository Pattern] --> B[Domain Layer]
    A --> C[Repository Interface]
    A --> D[Repository Implementation]
    A --> E[Data Access Layer]
    
    B --> B1[Business Logic]
    B --> B2[Domain Models]
    B --> B3[Use Cases]
    
    C --> C1[Abstract Methods]
    C --> C2[Domain-focused API]
    C --> C3[Technology-agnostic]
    
    D --> D1[SQLAlchemy Implementation]
    D --> D2[MongoDB Implementation]
    D --> D3[Redis Implementation]
    
    E --> E1[Database]
    E --> E2[External APIs]
    E --> E3[File System]
    
    B1 --> C
    C --> D
    D --> E
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Repository vs Active Record

```mermaid
graph LR
    A[Data Access Patterns] --> B[Repository Pattern]
    A --> C[Active Record Pattern]
    
    B --> B1[Separation of Concerns]
    B --> B2[Testability]
    B --> B3[Domain-driven Design]
    B --> B4[Multiple Data Sources]
    
    C --> C1[Simple CRUD]
    C --> C2[Model = Database Row]
    C --> C3[Built-in ORM methods]
    C --> C4[Rapid Development]
    
    B --> D["UserRepository.save(user)"]
    C --> E["user.save()"]
    
    B1 --> F[✅ Clean Architecture]
    C1 --> G[✅ Quick Development]
    
    style B fill:#c8e6c9
    style C fill:#fff3e0
```

## 🔒 Database Security

### SQL Injection Prevention

```mermaid
graph TD
    A[SQL Injection Prevention] --> B[Parameterized Queries]
    A --> C[Input Validation]
    A --> D[Least Privilege]
    A --> E[Error Handling]
    
    B --> B1[Prepared Statements]
    B --> B2[ORM Query Methods]
    B --> B3[Never String Concatenation]
    
    C --> C1[Type Checking]
    C --> C2[Length Limits]
    C --> C3[Character Filtering]
    
    D --> D1[Minimal DB Permissions]
    D --> D2[Separate Users for Different Operations]
    D --> D3[No Admin Access for Apps]
    
    E --> E1[Don't Expose DB Errors]
    E --> E2[Generic Error Messages]
    E --> E3[Proper Logging]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Secure Database Connection

```mermaid
sequenceDiagram
    participant App as Application
    participant Pool as Connection Pool
    participant DB as Database
    
    Note over App,DB: Secure Connection Setup
    App->>Pool: Request Connection
    Pool->>DB: SSL/TLS Handshake
    DB-->>Pool: Certificate Exchange
    Pool->>DB: Authentication (username/password)
    DB-->>Pool: Connection Established
    Pool-->>App: Secure Connection
    
    Note over App,DB: Query Execution
    App->>Pool: Parameterized Query
    Pool->>DB: Prepared Statement + Parameters
    DB-->>Pool: Results
    Pool-->>App: Sanitized Results
    
    Note over App,DB: Connection Return
    App->>Pool: Release Connection
    Note over Pool: Connection returned to pool
```

## 📊 Performance Optimization

### Database Performance Strategies

```mermaid
graph TD
    A[Database Performance] --> B[Query Optimization]
    A --> C[Indexing Strategy]
    A --> D[Connection Management]
    A --> E[Caching]
    
    B --> B1[Query Analysis]
    B --> B2[EXPLAIN QUERY PLAN]
    B --> B3[Query Rewriting]
    B --> B4[Avoid N+1 Queries]
    
    C --> C1[Primary Keys]
    C --> C2[Foreign Keys]
    C --> C3[Composite Indexes]
    C --> C4[Partial Indexes]
    
    D --> D1[Connection Pooling]
    D --> D2[Connection Limits]
    D --> D3[Connection Lifecycle]
    
    E --> E1[Query Result Cache]
    E --> E2[Object Cache]
    E --> E3[Redis/Memcached]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Query Performance Analysis

```mermaid
graph LR
    A[Query Performance] --> B[Slow Query Identification]
    A --> C[Execution Plan Analysis]
    A --> D[Index Usage]
    A --> E[Query Optimization]
    
    B --> B1[Query Logs]
    B --> B2[Performance Monitoring]
    B --> B3[Profiling Tools]
    
    C --> C1[Table Scans]
    C --> C2[Index Scans]
    C --> C3[Join Operations]
    C --> C4[Sort Operations]
    
    D --> D1[Index Effectiveness]
    D --> D2[Missing Indexes]
    D --> D3[Index Overhead]
    
    E --> E1[Query Rewriting]
    E --> E2[Denormalization]
    E --> E3[Partitioning]
    
    style A fill:#e3f2fd
    style B fill:#ffcdd2
    style C fill:#fff3e0
    style D fill:#c8e6c9
    style E fill:#f3e5f5
```

## 🔄 Database Migrations

### Migration Workflow

```mermaid
graph TD
    A[Database Migrations] --> B[Schema Changes]
    A --> C[Data Migrations]
    A --> D[Rollback Strategy]
    A --> E[Version Control]
    
    B --> B1[Create Tables]
    B --> B2[Alter Columns]
    B --> B3[Add Indexes]
    B --> B4[Drop Objects]
    
    C --> C1[Data Transformation]
    C --> C2[Data Cleanup]
    C --> C3[Reference Updates]
    
    D --> D1[Reversible Operations]
    D --> D2[Backup Strategy]
    D --> D3[Testing Rollbacks]
    
    E --> E1[Migration Files]
    E --> E2[Version Numbers]
    E --> E3[Dependency Tracking]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#ffcdd2
    style E fill:#f3e5f5
```

### Alembic Migration Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Alembic as Alembic
    participant DB as Database
    participant Git as Version Control
    
    Dev->>Alembic: alembic revision --autogenerate
    Alembic->>DB: Compare current schema
    Alembic->>Alembic: Generate migration script
    Alembic-->>Dev: Migration file created
    
    Dev->>Git: Commit migration file
    
    Note over Dev,DB: Deployment
    Dev->>Alembic: alembic upgrade head
    Alembic->>DB: Check current version
    Alembic->>DB: Apply pending migrations
    DB-->>Alembic: Migration complete
    Alembic-->>Dev: Database updated
    
    Note over Dev,DB: Rollback (if needed)
    Dev->>Alembic: alembic downgrade -1
    Alembic->>DB: Rollback last migration
    DB-->>Alembic: Rollback complete
```

Эти диаграммы показывают полную картину работы с базами данных в Python от архитектуры до оптимизации производительности. 