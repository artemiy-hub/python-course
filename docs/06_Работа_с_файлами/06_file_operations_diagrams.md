# Диаграммы: Работа с файлами Python

## 🏗️ Иерархия файловых объектов

```mermaid
graph TD
    subgraph "File Objects Hierarchy"
        A[File Objects] --> B[Text Files]
        A --> C[Binary Files]
        A --> D[Buffered Files]
        
        B --> B1[TextIOWrapper]
        B --> B2[StringIO]
        
        C --> C1[BufferedReader]
        C --> C2[BufferedWriter]
        C --> C3[BufferedRandom]
        C --> C4[BytesIO]
        
        D --> D1[FileIO]
        D --> D2[Raw Files]
        
        E[Context Managers] --> F[__enter__]
        E --> G[__exit__]
        
        H[File Modes] --> H1[r - read]
        H --> H2[w - write]
        H --> H3[a - append]
        H --> H4[x - exclusive]
        H --> H5[+ - read/write]
        H --> H6[b - binary]
        H --> H7[t - text]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#ffeaa7
    style E fill:#fd79a8
```

## 📖 Процесс открытия файла

```mermaid
flowchart TD
    A["open(filename, mode)"] --> B{File exists?}
    
    B -->|Yes| C{Mode check}
    B -->|No| D{Create mode?}
    
    D -->|w, a, x| E[Create file]
    D -->|r| F[FileNotFoundError]
    
    E --> C
    F --> Z[Exception]
    
    C --> G{Text or Binary?}
    
    G -->|Text| H[TextIOWrapper]
    G -->|Binary| I[BufferedReader/Writer]
    
    H --> J[Encoding specified?]
    J -->|Yes| K[Use specified]
    J -->|No| L[Use default encoding]
    
    K --> M[File Object]
    L --> M
    I --> M
    
    M --> N[Return file handle]
    
    style A fill:#74b9ff
    style M fill:#00b894
    style F fill:#e17055
    style Z fill:#e17055
```

## 🔄 Жизненный цикл файла

```mermaid
stateDiagram-v2
    [*] --> Closed: File not opened
    Closed --> Opening: open()
    Opening --> Open: Success
    Opening --> Error: Failure
    
    Open --> Reading: read operations
    Open --> Writing: write operations
    Open --> Seeking: seek/tell
    
    Reading --> Open: Continue
    Writing --> Open: Continue
    Seeking --> Open: Continue
    
    Open --> Flushing: flush()
    Flushing --> Open: Buffer cleared
    
    Open --> Closing: close() or __exit__
    Closing --> Closed: File closed
    
    Error --> [*]: Handle exception
    
    note right of Open
        File handle active
        Buffer operations
        Position tracking
    end note
    
    note right of Closed
        Resources released
        Handle invalid
    end note
```

## 🎯 Режимы работы с файлами

```mermaid
mindmap
  root((File Modes))
    Read
      r (read only)
      r+ (read/write)
      rb (binary read)
      r+b (binary read/write)
    Write  
      w (write, truncate)
      w+ (write/read, truncate)
      wb (binary write)
      w+b (binary write/read)
    Append
      a (append)
      a+ (append/read)
      ab (binary append)
      a+b (binary append/read)
    Exclusive
      x (exclusive create)
      x+ (exclusive create/read)
      xb (binary exclusive)
      x+b (binary exclusive/read)
```

## 🌐 Обработка кодировок

```mermaid
graph LR
    subgraph "Encoding Process"
        A[Python String] --> B[Encoder]
        B --> C[Bytes]
        C --> D[File System]
        
        D --> E[Bytes]
        E --> F[Decoder]
        F --> G[Python String]
        
        H[Encoding Types] --> H1[UTF-8]
        H --> H2[UTF-16]
        H --> H3[ASCII]
        H --> H4[CP1251]
        H --> H5[KOI8-R]
        
        I[Error Handling] --> I1[strict]
        I --> I2[ignore]
        I --> I3[replace]
        I --> I4[backslashreplace]
        I --> I5[xmlcharrefreplace]
    end
    
    style A fill:#74b9ff
    style G fill:#74b9ff
    style D fill:#00b894
    style H1 fill:#ffeaa7
```

## 🗂️ Работа с путями

```mermaid
graph TB
    subgraph "Path Operations"
        A[Path Types] --> A1[Absolute]
        A --> A2[Relative]
        
        A1 --> A11["/home/user/file.txt"]
        A1 --> A12["C:\\Users\\file.txt"]
        
        A2 --> A21["./file.txt"]
        A2 --> A22["../parent/file.txt"]
        
        B[pathlib.Path] --> B1[name]
        B --> B2[stem]
        B --> B3[suffix]
        B --> B4[parent]
        B --> B5[parts]
        
        C[Operations] --> C1["exists()"]
        C --> C2["is_file()"]
        C --> C3["is_dir()"]
        C --> C4["mkdir()"]
        C --> C5["touch()"]
        C --> C6["unlink()"]
        
        D[os.path] --> D1["dirname()"]
        D --> D2["basename()"]
        D --> D3["splitext()"]
        D --> D4["join()"]
        D --> D5["abspath()"]
    end
    
    style B fill:#00b894
    style C fill:#ffeaa7
    style D fill:#fd79a8
```

## 📊 Сравнение методов чтения

```mermaid
quadrantChart
    title "Методы чтения файлов"
    x-axis "Объем памяти" --> "Высокий"
    y-axis "Медленно" --> "Быстро"
    
    quadrant-1 "Быстро, много памяти"
    quadrant-2 "Медленно, много памяти"
    quadrant-3 "Медленно, мало памяти"
    quadrant-4 "Быстро, мало памяти"
    
    "read()": [0.8, 0.7]
    "readlines()": [0.9, 0.6]
    "readline()": [0.2, 0.3]
    iteration: [0.1, 0.8]
    chunks: [0.3, 0.6]
```

## 🔄 Контекстные менеджеры

```mermaid
sequenceDiagram
    participant App as Application
    participant CM as Context Manager
    participant File as File Object
    participant OS as Operating System
    
    App->>CM: with open(file) as f:
    CM->>File: __enter__()
    File->>OS: Open file handle
    OS-->>File: File descriptor
    File-->>CM: File object
    CM-->>App: File handle
    
    App->>File: read/write operations
    File->>OS: I/O operations
    OS-->>File: Data
    File-->>App: Results
    
    Note over App,OS: Normal execution or exception
    
    CM->>File: __exit__()
    File->>OS: Close file handle
    OS-->>File: Cleanup complete
    File-->>CM: Cleanup done
    CM-->>App: Context closed
```

## 📂 Структура директорий

```mermaid
graph TD
    subgraph "Directory Tree"
        A[Root /] --> B[home]
        A --> C[usr]
        A --> D[var]
        A --> E[etc]
        
        B --> B1[user]
        B1 --> B11[documents]
        B1 --> B12[downloads]
        B1 --> B13[.config]
        
        B11 --> B111[file1.txt]
        B11 --> B112[project/]
        B12 --> B121[archive.zip]
        B13 --> B131[app.conf]
        
        C --> C1[bin]
        C --> C2[lib]
        
        D --> D1[log]
        D --> D2[tmp]
        
        E --> E1[passwd]
        E --> E2[hosts]
    end
    
    style A fill:#74b9ff
    style B11 fill:#00b894
    style B111 fill:#ffeaa7
    style B121 fill:#fd79a8
```

## 🔍 Поиск файлов

```mermaid
flowchart TD
    A[Start Search] --> B[Choose Method]
    
    B --> C["os.listdir()"]
    B --> D["os.walk()"]
    B --> E["pathlib.glob()"]
    B --> F["pathlib.rglob()"]
    
    C --> C1[Single directory]
    C1 --> C2[Filter manually]
    
    D --> D1[Recursive walk]
    D1 --> D2[All subdirectories]
    
    E --> E1[Pattern matching]
    E1 --> E2[Single level]
    
    F --> F1[Pattern matching]
    F1 --> F2[Recursive]
    
    C2 --> G[Filter Results]
    D2 --> G
    E2 --> G
    F2 --> G
    
    G --> H{Apply Filters}
    H --> H1[By extension]
    H --> H2[By size]
    H --> H3[By date]
    H --> H4[By permissions]
    
    H1 --> I[Filtered Results]
    H2 --> I
    H3 --> I
    H4 --> I
    
    style A fill:#74b9ff
    style G fill:#00b894
    style I fill:#ffeaa7
```

## 📄 Форматы файлов

```mermaid
graph LR
    subgraph "File Formats"
        A[Text Files] --> A1[Plain Text]
        A --> A2[CSV]
        A --> A3[JSON]
        A --> A4[XML]
        A --> A5[YAML]
        A --> A6[INI]
        
        B[Binary Files] --> B1[Images]
        B --> B2[Audio]
        B --> B3[Video]
        B --> B4[Archives]
        B --> B5[Executables]
        
        C[Structured] --> C1[Databases]
        C --> C2[Spreadsheets]
        C --> C3[Documents]
        
        D[Processing] --> D1[csv module]
        D --> D2[json module]
        D --> D3[xml.etree]
        D --> D4[zipfile]
        D --> D5[tarfile]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#ffeaa7
    style D fill:#fd79a8
```

## 🗜️ Архивы и сжатие

```mermaid
graph TB
    subgraph "Archive Types"
        A[ZIP Archives] --> A1[zipfile.ZipFile]
        A --> A2[Compression levels]
        A --> A3[Password protection]
        
        B[TAR Archives] --> B1[tarfile.TarFile]
        B --> B2[Compression types]
        B2 --> B21[.tar]
        B2 --> B22[.tar.gz]
        B2 --> B23[.tar.bz2]
        B2 --> B24[.tar.xz]
        
        C[Operations] --> C1[Create]
        C --> C2[Extract]
        C --> C3[List contents]
        C --> C4[Add files]
        C --> C5[Remove files]
        
        D[Compression Algorithms] --> D1[DEFLATE]
        D --> D2[GZIP]
        D --> D3[BZIP2]
        D --> D4[LZMA]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#ffeaa7
    style D fill:#fd79a8
```

## 🔄 Временные файлы

```mermaid
stateDiagram-v2
    [*] --> Creating: tempfile.NamedTemporaryFile()
    Creating --> Created: File created in temp dir
    
    Created --> Writing: Write data
    Created --> Reading: Read data
    
    Writing --> Created: Continue operations
    Reading --> Created: Continue operations
    
    Created --> Cleanup: delete=True (default)
    Created --> Manual: delete=False
    
    Cleanup --> Deleted: Auto cleanup on close
    Manual --> UserDelete: Manual cleanup required
    
    UserDelete --> Deleted: os.unlink()
    
    Deleted --> [*]: Resources freed
    
    note right of Created
        Unique filename
        Random generation
        Platform temp dir
    end note
    
    note right of Cleanup
        Automatic on:
        - Context exit
        - Object deletion
        - Process termination
    end note
```

## 🎯 Стратегии чтения больших файлов

```mermaid
graph TD
    subgraph "Large File Strategies"
        A[Large File] --> B{File Size}
        
        B -->|< 100MB| C["read() - Load all"]
        B -->|100MB - 1GB| D[Chunked Reading]
        B -->|> 1GB| E[Line by Line]
        B -->|> 10GB| F[Memory Mapping]
        
        C --> C1[Simple & Fast]
        C --> C2[High Memory Usage]
        
        D --> D1[Balanced Approach]
        D --> D2[Configurable Chunks]
        D --> D3[8KB - 64KB chunks]
        
        E --> E1[Low Memory]
        E --> E2[Iterator Pattern]
        E --> E3[Generator Friendly]
        
        F --> F1[mmap module]
        F --> F2[OS Virtual Memory]
        F --> F3[Random Access]
        
        G[Performance Tips] --> G1[Use buffering]
        G --> G2["Avoid seek() in loops"]
        G --> G3[Process in batches]
        G --> G4[Use generators]
    end
    
    style C fill:#e17055
    style D fill:#ffeaa7
    style E fill:#00b894
    style F fill:#74b9ff
```

## 🔐 Безопасность файлов

```mermaid
flowchart TD
    A[File Security] --> B[Path Validation]
    A --> C[Permission Checks]
    A --> D[Atomic Operations]
    A --> E[Input Sanitization]
    
    B --> B1[Prevent Path Traversal]
    B --> B2[Resolve Symlinks]
    B --> B3[Check Base Directory]
    B1 --> B11["../../../etc/passwd ❌"]
    B1 --> B12["./safe/file.txt ✅"]
    
    C --> C1["os.access()"]
    C --> C2["stat.filemode()"]
    C --> C3[Check R/W/X]
    
    D --> D1[Temp + Rename]
    D --> D2[Backup + Restore]
    D --> D3[Transaction-like]
    
    E --> E1[Validate Extensions]
    E --> E2[Check MIME Types]
    E --> E3[Sanitize Names]
    
    F[Common Attacks] --> F1[Directory Traversal]
    F --> F2[File Upload Attacks]
    F --> F3[Symlink Attacks]
    F --> F4[Race Conditions]
    
    style B1 fill:#e17055
    style F fill:#e17055
    style D fill:#00b894
```

## 📊 Производительность I/O

```mermaid
graph LR
    subgraph "I/O Performance"
        A[Buffer Sizes] --> A1[No Buffer: 0]
        A --> A2[Line Buffer: 1]
        A --> A3[Custom: 8192]
        A --> A4[Default: -1]
        
        B[Read Strategies] --> B1["read()"]
        B --> B2["readline()"]
        B --> B3["readlines()"]
        B --> B4[iteration]
        
        C[Write Strategies] --> C1["write()"]
        C --> C2["writelines()"]
        C --> C3["print()"]
        C --> C4["flush()"]
        
        D[Optimization] --> D1[Batch Operations]
        D --> D2[Avoid Seek]
        D --> D3[Use Generators]
        D --> D4[Memory Mapping]
        
        E[Measurements] --> E1[timeit]
        E --> E2[cProfile]
        E --> E3[memory_profiler]
        E --> E4[psutil]
    end
    
    style A4 fill:#00b894
    style B4 fill:#00b894
    style D fill:#ffeaa7
    style E fill:#fd79a8
```

## 🔍 Мониторинг файловой системы

```mermaid
graph TD
    subgraph "File System Monitoring"
        A[watchdog.Observer] --> B[Event Types]
        
        B --> B1[FileCreatedEvent]
        B --> B2[FileModifiedEvent] 
        B --> B3[FileDeletedEvent]
        B --> B4[FileMovedEvent]
        B --> B5[DirCreatedEvent]
        B --> B6[DirModifiedEvent]
        B --> B7[DirDeletedEvent]
        B --> B8[DirMovedEvent]
        
        C[Event Handler] --> C1["on_created()"]
        C --> C2["on_modified()"]
        C --> C3["on_deleted()"]
        C --> C4["on_moved()"]
        
        D[Observer Setup] --> D1[Create Handler]
        D --> D2[Schedule Path]
        D --> D3[Start Observer]
        D --> D4[Monitor Loop]
        D --> D5[Stop Observer]
        
        E[Use Cases] --> E1[Auto Backup]
        E --> E2[File Sync]
        E --> E3[Log Processing]
        E --> E4[Hot Reload]
    end
    
    style A fill:#74b9ff
    style C fill:#00b894
    style E fill:#ffeaa7
```

## 🎭 Паттерны работы с файлами

```mermaid
graph TB
    subgraph "File Operation Patterns"
        A[Reader Pattern] --> A1[File Iterator]
        A --> A2[Chunk Reader]
        A --> A3[Line Processor]
        
        B[Writer Pattern] --> B1[Batch Writer]
        B --> B2[Streaming Writer]
        B --> B3[Atomic Writer]
        
        C[Processor Pattern] --> C1[Filter]
        C --> C2[Transform]
        C --> C3[Aggregate]
        
        D[Manager Pattern] --> D1[File Pool]
        D --> D2[Resource Manager]
        D --> D3[Transaction Manager]
        
        E[Factory Pattern] --> E1[Format Handlers]
        E --> E2[Encoding Handlers]
        E --> E3[Compression Handlers]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#ffeaa7
    style D fill:#fd79a8
    style E fill:#a29bfe
```

## 🔧 Лучшие практики

```mermaid
mindmap
  root((File Best Practices))
    Context Managers
      Always use with
      Auto cleanup
      Exception safety
    Encoding
      Explicit UTF-8
      Handle errors
      Detect encoding
    Paths
      Use pathlib
      Validate inputs
      Cross-platform
    Performance
      Streaming for large files
      Appropriate buffering
      Avoid unnecessary seeks
    Security
      Validate paths
      Check permissions
      Atomic writes
    Error Handling
      Specific exceptions
      Graceful degradation
      Logging
``` 