# Диаграммы: Структуры данных Python

## 🏗️ Общая архитектура структур данных

```mermaid
graph TD
    A[Python Objects] --> B[Sequence Types]
    A --> C[Mapping Types]
    A --> D[Set Types]
    
    B --> E[Mutable Sequences]
    B --> F[Immutable Sequences]
    
    E --> G[list]
    E --> H[bytearray]
    E --> I[collections.deque]
    
    F --> J[tuple]
    F --> K[str]
    F --> L[bytes]
    F --> M[range]
    
    C --> N[dict]
    C --> O[collections.defaultdict]
    C --> P[collections.OrderedDict]
    C --> Q[collections.Counter]
    
    D --> R[set]
    D --> S[frozenset]
    
    style E fill:#ffeaa7
    style F fill:#e8f5e8
    style C fill:#74b9ff
    style D fill:#fd79a8
```

## 📋 Внутренняя структура списка

```mermaid
graph LR
    subgraph "Python List Internal Structure"
        A[PyListObject] --> B[ob_size: 3]
        A --> C[allocated: 4]
        A --> D[ob_item**]
        
        D --> E[PyObject* 0]
        D --> F[PyObject* 1] 
        D --> G[PyObject* 2]
        D --> H[NULL]
        
        E --> I[int: 10]
        F --> J["str: hello"]
        G --> K[float: 3.14]
    end
    
    style A fill:#74b9ff
    style D fill:#ffeaa7
    style I fill:#00b894
    style J fill:#e17055
    style K fill:#a29bfe
```

## 🔄 Операции со списками - сложность

```mermaid
graph TB
    subgraph "List Operations Complexity"
        A[list operations] --> B[O<1>]
        A --> C[O<n>]
        
        B --> D["list[i] - доступ по индексу"]
        B --> E["list.append(x) - добавление в конец"]
        B --> F["list.pop() - удаление с конца"]
        
        C --> G["list.insert(i,x) - вставка по индексу"]
        C --> H["list.remove(x) - удаление по значению"]
        C --> I["x in list - поиск элемента"]
        C --> J["list.sort() - сортировка"]
    end
    
    style B fill:#00b894
    style C fill:#e17055
```

## 🎯 Сравнение структур данных

```mermaid
quadrantChart
    title "Выбор структуры данных"
    x-axis "Производительность" --> "Высокая"
    y-axis "Функциональность" --> "Богатая"
    
    quadrant-1 "Оптимальный выбор"
    quadrant-2 "Избыточная функциональность"
    quadrant-3 "Базовые решения"
    quadrant-4 "Высокая производительность"
    
    list: [0.3, 0.8]
    tuple: [0.7, 0.4] 
    dict: [0.8, 0.9]
    set: [0.9, 0.6]
    deque: [0.6, 0.7]
    frozenset: [0.8, 0.3]
```

## 🔗 Жизненный цикл кортежа

```mermaid
stateDiagram-v2
    [*] --> Created: Создание кортежа
    Created --> Accessed: Доступ к элементам
    Accessed --> Accessed: Индексация/итерация
    Accessed --> Unpacked: Распаковка
    Unpacked --> Used: Использование значений
    Used --> [*]: Удаление из памяти
    
    Created --> Hashed: Хеширование
    Hashed --> DictKey: Использование как ключ
    DictKey --> [*]
    
    note right of Created
        tuple((1, 2, 3))
        Неизменяемый объект
    end note
    
    note left of Unpacked
        x, y, z = tuple
        Множественное присваивание
    end note
```

## 📖 Архитектура словаря (Python 3.7+)

```mermaid
graph TB
    subgraph "Modern Dict Structure (Compact Dict)"
        A[Hash Table] --> B[Indices Array]
        A --> C[Entries Array]
        
        B --> D[Index 0: 1]
        B --> E[Index 1: -1]
        B --> F[Index 2: 0]
        B --> G[Index 3: 2]
        
        C --> H[Entry 0: <br/>hash=12345<br/>key='name'<br/>value='Alice']
        C --> I[Entry 1: <br/>hash=67890<br/>key='age'<br/>value=25]
        C --> J[Entry 2: <br/>hash=54321<br/>key='city'<br/>value='Moscow']
    end
    
    style A fill:#74b9ff
    style B fill:#ffeaa7
    style C fill:#fd79a8
```

## 🎯 Операции с множествами

```mermaid
graph LR
    subgraph "Set Operations"
        A["Set A: {1,2,3,4}"]
        B["Set B: {3,4,5,6}"]
        
        A --> C["Union: {1,2,3,4,5,6}"]
        B --> C
        
        A --> D["Intersection: {3,4}"]
        B --> D
        
        A --> E["Difference A-B: {1,2}"]
        B --> F["Difference B-A: {5,6}"]
        
        A --> G["Symmetric Diff: {1,2,5,6}"]
        B --> G
    end
    
    style C fill:#00b894
    style D fill:#74b9ff
    style E fill:#ffeaa7
    style F fill:#ffeaa7
    style G fill:#fd79a8
```

## 🔄 Процесс хеширования в множествах и словарях

```mermaid
flowchart TD
    A[Объект] --> B{Хешируемый?}
    B -->|Да| C[hash<object>]
    B -->|Нет| D[TypeError]
    
    C --> E[Хеш-код]
    E --> F[Индекс = hash % table_size]
    F --> G{Коллизия?}
    
    G -->|Нет| H[Сохранить в слот]
    G -->|Да| I[Разрешение коллизий]
    I --> J[Поиск свободного слота]
    J --> H
    
    H --> K[Успешно сохранено]
    
    style B fill:#74b9ff
    style G fill:#ffeaa7
    style K fill:#00b894
    style D fill:#e17055
```

## 📊 Производительность операций

```mermaid
graph TB
    subgraph "Time Complexity Comparison"
        A[Data Structure] --> B[Access]
        A --> C[Search] 
        A --> D[Insertion]
        A --> E[Deletion]
        
        B --> F[List: O<1> by index]
        B --> G[Tuple: O<1> by index]
        B --> H[Dict: O<1> by key]
        B --> I[Set: N/A]
        
        C --> J[List: O<n>]
        C --> K[Tuple: O<n>]
        C --> L[Dict: O<1> avg]
        C --> M[Set: O<1> avg]
        
        D --> N[List: O<n> insert, O<1> append]
        D --> O[Tuple: Immutable]
        D --> P[Dict: O<1> avg]
        D --> Q[Set: O<1> avg]
        
        E --> R[List: O<n>]
        E --> S[Tuple: Immutable]
        E --> T[Dict: O<1> avg]
        E --> U[Set: O<1> avg]
    end
    
    style F fill:#00b894
    style G fill:#00b894  
    style H fill:#00b894
    style L fill:#00b894
    style M fill:#00b894
    style P fill:#00b894
    style Q fill:#00b894
    style T fill:#00b894
    style U fill:#00b894
```

## 🧠 Схема выбора структуры данных

```mermaid
flowchart TD
    A[Нужна структура данных] --> B{Нужен порядок?}
    
    B -->|Да| C{Данные изменяются?}
    B -->|Нет| D{Нужны уникальные элементы?}
    
    C -->|Да| E{Нужен доступ по ключу?}
    C -->|Нет| F[tuple<br/>Кортеж]
    
    E -->|Да| G[dict<br/>Словарь]
    E -->|Нет| H[list<br/>Список]
    
    D -->|Да| I{Данные изменяются?}
    D -->|Нет| J[list<br/>Список]
    
    I -->|Да| K[set<br/>Множество]
    I -->|Нет| L[frozenset<br/>Замороженное множество]
    
    style F fill:#e8f5e8
    style G fill:#74b9ff
    style H fill:#ffeaa7
    style J fill:#ffeaa7
    style K fill:#fd79a8
    style L fill:#fd79a8
```

## 🔄 Пример работы со срезами

```mermaid
graph LR
    subgraph "List Slicing: [0,1,2,3,4,5,6,7,8,9]"
        A[Original List] --> B["[2:7] → [2,3,4,5,6]"]
        A --> C["[:5] → [0,1,2,3,4]"] 
        A --> D["[5:] → [5,6,7,8,9]"]
        A --> E["[::2] → [0,2,4,6,8]"]
        A --> F["[::-1] → [9,8,7,6,5,4,3,2,1,0]"]
        A --> G["[-3:] → [7,8,9]"]
    end
    
    style A fill:#74b9ff
    style B fill:#00b894
    style C fill:#00b894
    style D fill:#00b894
    style E fill:#ffeaa7
    style F fill:#fd79a8
    style G fill:#a29bfe
```

## 📈 Рост динамического массива (список)

```mermaid
graph TD
    subgraph "Dynamic Array Growth Strategy"
        A[Initial: capacity=4, size=0] --> B[Add elements: size=4]
        B --> C{Need more space?}
        C -->|Yes| D[Reallocate: new_capacity = old * 1.5]
        C -->|No| E[Continue adding]
        D --> F[Copy existing elements]
        F --> G[capacity=6, size=4]
        G --> H[Add new element: size=5]
        H --> I[Continue until next resize]
    end
    
    style A fill:#74b9ff
    style D fill:#ffeaa7
    style F fill:#e17055
    style G fill:#00b894
```

## 🎭 Паттерны использования коллекций

```mermaid
mindmap
  root((Структуры данных))
    Списки
      Последовательности
      Стеки (append/pop)
      Очереди (deque)
      Матрицы
    Кортежи  
      Координаты
      Записи БД
      Возврат значений
      Ключи словарей
    Словари
      Кеширование
      Индексы
      Конфигурации
      JSON данные
    Множества
      Фильтрация дубликатов
      Математические операции
      Быстрый поиск
      Пересечения данных
```

## 🔄 Жизненный цикл объектов в коллекциях

```mermaid
journey
    title Жизненный цикл объекта в списке
    section Создание
      Создать объект: 5: Разработчик
      Добавить в список: 4: Python
      Увеличить refcount: 3: Python
    section Использование  
      Доступ по индексу: 5: Разработчик
      Итерация: 4: Разработчик
      Передача в функцию: 3: Python
    section Модификация
      Изменение элемента: 4: Разработчик
      Удаление из списка: 3: Python
      Уменьшение refcount: 2: Python
    section Очистка
      Проверка refcount: 2: GC
      Освобождение памяти: 1: GC
```

## 🏛️ Архитектура collections.deque

```mermaid
graph LR
    subgraph "Deque Internal Structure"
        A[deque] --> B[Left Block]
        A --> C[Center Blocks]
        A --> D[Right Block]
        
        B --> E[leftindex]
        B --> F[data array]
        
        C --> G[Block 1]
        C --> H[Block 2]
        C --> I[Block N]
        
        D --> J[rightindex]
        D --> K[data array]
        
        L[appendleft O<1>] --> B
        M[append O<1>] --> D
        N[popleft O<1>] --> B  
        O[pop O<1>] --> D
    end
    
    style A fill:#74b9ff
    style L fill:#00b894
    style M fill:#00b894
    style N fill:#00b894
    style O fill:#00b894
```

## 🎯 Оптимизация выбора коллекций

```mermaid
flowchart TD
    A[Анализ требований] --> B{Размер данных}
    
    B -->|Маленький <100| C{Тип операций}
    B -->|Средний 100-10K| D{Частота доступа}  
    B -->|Большой >10K| E{Производительность критична?}
    
    C -->|Простые| F[list/tuple]
    C -->|Поиск| G[dict/set]
    
    D -->|Частый доступ| H[dict для O<1> поиска]
    D -->|Редкий доступ| I[list для экономии памяти]
    
    E -->|Да| J[Специализированные<br/>numpy/pandas]
    E -->|Нет| K[Стандартные коллекции]
    
    style F fill:#e8f5e8
    style G fill:#74b9ff
    style H fill:#74b9ff
    style I fill:#ffeaa7
    style J fill:#fd79a8
    style K fill:#00b894
``` 