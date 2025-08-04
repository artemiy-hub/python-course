# Диаграммы: Регулярные выражения в Python

## 🎯 Основы регулярных выражений

### Архитектура регулярных выражений

```mermaid
graph TD
    A[Regular Expressions] --> B[Pattern]
    A --> C[Engine]
    A --> D[Flags]
    A --> E[Methods]
    
    B --> B1[Literals]
    B --> B2[Metacharacters]
    B --> B3[Character Classes]
    B --> B4[Quantifiers]
    B --> B5[Anchors]
    B --> B6[Groups]
    
    C --> C1[Finite Automaton]
    C --> C2[Backtracking]
    C --> C3[Compilation]
    C --> C4[Matching Process]
    
    D --> D1["re.IGNORECASE"]
    D --> D2["re.MULTILINE"]
    D --> D3["re.DOTALL"]
    D --> D4["re.VERBOSE"]
    
    E --> E1["re.search()"]
    E --> E2["re.match()"]
    E --> E3["re.findall()"]
    E --> E4["re.sub()"]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Metacharacters и их назначение

```mermaid
graph TD
    A[Metacharacters] --> B[Character Classes]
    A --> C[Quantifiers]
    A --> D[Anchors]
    A --> E[Groups]
    A --> F[Alternation]
    
    B --> B1[". - Any character"]
    B --> B2["\\d - Digits"]
    B --> B3["\\w - Word characters"]
    B --> B4["\\s - Whitespace"]
    B --> B5["[...] - Custom class"]
    
    C --> C1["* - Zero or more"]
    C --> C2["+ - One or more"]
    C --> C3["? - Zero or one"]
    C --> C4["{n} - Exactly n"]
    C --> C5["{n,m} - Between n and m"]
    
    D --> D1["^ - Start of string"]
    D --> D2["$ - End of string"]
    D --> D3["\\b - Word boundary"]
    D --> D4["\\A - Start of string"]
    D --> D5["\\Z - End of string"]
    
    E --> E1["(...) - Capturing group"]
    E --> E2["(?:...) - Non-capturing"]
    E --> E3["(?P<name>...) - Named group"]
    E --> E4["(?=...) - Lookahead"]
    E --> E5["(?!...) - Negative lookahead"]
    
    F --> F1["| - OR operator"]
    F --> F2[Multiple patterns]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fce4ec
```

### Regex Engine Processing

```mermaid
sequenceDiagram
    participant Input as Input String
    participant Engine as Regex Engine
    participant Pattern as Compiled Pattern
    participant Result as Match Result
    
    Note over Input,Result: Regex Matching Process
    
    Input->>Engine: "Hello World 123"
    Engine->>Pattern: Compile pattern: \w+\s+\w+\s+\d+
    Pattern-->>Engine: Compiled regex object
    
    Engine->>Engine: Start matching from position 0
    Engine->>Engine: Match "Hello" with \w+
    Engine->>Engine: Match " " with \s+
    Engine->>Engine: Match "World" with \w+
    Engine->>Engine: Match " " with \s+
    Engine->>Engine: Match "123" with \d+
    
    Engine->>Result: Create Match object
    Result-->>Engine: Match found at position 0-13
    
    Note over Engine: Success: Full string matched
```

## 🔍 Методы поиска и сопоставления

### re Module Methods Comparison

```mermaid
graph TD
    A[re Module Methods] --> B["re.search()"]
    A --> C["re.match()"]
    A --> D["re.findall()"]
    A --> E["re.finditer()"]
    A --> F["re.sub()"]
    A --> G["re.split()"]
    
    B --> B1[🔍 Find first occurrence]
    B --> B2[📍 Search entire string]
    B --> B3[↩️ Returns Match object]
    B --> B4[✅ Most flexible]
    
    C --> C1[🎯 Match from beginning]
    C --> C2[📍 Start of string only]
    C --> C3[↩️ Returns Match object]
    C --> C4[⚠️ Strict positioning]
    
    D --> D1[📋 Find all occurrences]
    D --> D2[📍 Search entire string]
    D --> D3[↩️ Returns list of strings]
    D --> D4[🚀 Fast for simple patterns]
    
    E --> E1[🔄 Iterator of matches]
    E --> E2[📍 Search entire string]
    E --> E3[↩️ Returns Match objects]
    E --> E4[�� Memory efficient]
    
    F --> F1[🔄 Replace occurrences]
    F --> F2[📍 Search entire string]
    F --> F3[↩️ Returns modified string]
    F --> F4[⚙️ Supports replacement functions]
    
    G --> G1[✂️ Split string]
    G --> G2[📍 Search entire string]
    G --> G3[↩️ Returns list of strings]
    G --> G4[🔧 Regex-based splitting]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fce4ec
    style G fill:#e1f5fe
```

### Match Object Attributes

```mermaid
graph TD
    A[Match Object] --> B[Position Methods]
    A --> C[Content Methods]
    A --> D[Group Methods]
    A --> E[Span Methods]
    
    B --> B1[".start()"]
    B --> B2[".end()"]
    B --> B3[.pos]
    B --> B4[.endpos]
    
    C --> C1[.string]
    C --> C2[.re]
    C --> C3[.lastindex]
    C --> C4[.lastgroup]
    
    D --> D1[".group()"]
    D --> D2[".groups()"]
    D --> D3[".groupdict()"]
    D --> D4[".expand()"]
    
    E --> E1[".span()"]
    E --> E2[Individual group spans]
    E --> E3[Named group spans]
    
    F[Example Usage] --> G["match.group(0) - Full match"]
    F --> H["match.group(1) - First group"]
    F --> I["match.start() - Start position"]
    F --> J["match.end() - End position"]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fce4ec
```

## 🎭 Группы и захват

### Group Types and Behavior

```mermaid
graph TD
    A[Group Types] --> B[Capturing Groups]
    A --> C[Non-Capturing Groups]
    A --> D[Named Groups]
    A --> E[Lookahead/Lookbehind]
    
    B --> B1["(...) - Basic group"]
    B --> B2[📊 Numbered: \1, \2, etc.]
    B --> B3[💾 Stored in memory]
    B --> B4[🔄 Available in replacement]
    
    C --> C1["(?:...) - Non-capturing"]
    C --> C2[🚫 Not numbered]
    C --> C3[💨 Not stored]
    C --> C4[⚡ Better performance]
    
    D --> D1["(?P<name>...) - Named"]
    D --> D2[📝 Accessible by name]
    D --> D3[💾 Also numbered]
    D --> D4[📖 Self-documenting]
    
    E --> E1["(?=...) - Positive lookahead"]
    E --> E2["(?!...) - Negative lookahead"]
    E --> E3["(?<=...) - Positive lookbehind"]
    E --> E4["(?<!...) - Negative lookbehind"]
    
    F[Group Numbering] --> G[Groups numbered left to right]
    F --> H[Nested groups get higher numbers]
    F --> I[Named groups also get numbers]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fce4ec
```

### Group Matching Flow

```mermaid
sequenceDiagram
    participant Input as Input: "John: 25, Jane: 30"
    participant Engine as Regex Engine
    participant Groups as Group Capture
    participant Result as Result
    
    Note over Input,Result: Pattern: (\w+): (\d+)
    
    Input->>Engine: Start matching
    Engine->>Groups: Create group 1 for (\w+)
    Engine->>Groups: Create group 2 for (\d+)
    
    Engine->>Engine: Match "John" with \w+
    Groups->>Groups: Capture "John" in group 1
    
    Engine->>Engine: Match ":" literally
    Engine->>Engine: Match " " literally (if pattern includes)
    
    Engine->>Engine: Match "25" with \d+
    Groups->>Groups: Capture "25" in group 2
    
    Groups->>Result: group(0) = "John: 25"
    Groups->>Result: group(1) = "John"
    Groups->>Result: group(2) = "25"
    
    Note over Engine: Continue for next match if using findall/finditer
```

## ⚡ Производительность и оптимизация

### Regex Performance Factors

```mermaid
graph TD
    A[Regex Performance] --> B[Pattern Complexity]
    A --> C[Input Size]
    A --> D[Backtracking]
    A --> E[Compilation]
    A --> F[Engine Type]
    
    B --> B1["Simple patterns: O(n)"]
    B --> B2["Complex patterns: O(n²) or worse"]
    B --> B3["Catastrophic backtracking: O(2ⁿ)"]
    
    C --> C1[Linear growth for good patterns]
    C --> C2[Exponential for bad patterns]
    C --> C3[Memory usage increases]
    
    D --> D1[Occurs with alternation]
    D --> D2[Nested quantifiers problem]
    D --> D3[Solution: atomic groups]
    D --> D4[Solution: possessive quantifiers]
    
    E --> E1[One-time cost]
    E --> E2[Cache compiled patterns]
    E --> E3["Use re.compile()"]
    
    F --> F1["NFA (backtracking)"]
    F --> F2["DFA (no backtracking)"]
    F --> F3[Hybrid approaches]
    
    G[Optimization Tips] --> H[Anchor patterns]
    G --> I[Use non-capturing groups]
    G --> J[Avoid nested quantifiers]
    G --> K[Compile patterns once]
    
    style A fill:#e3f2fd
    style B fill:#ffcdd2
    style G fill:#c8e6c9
```

### Catastrophic Backtracking Example

```mermaid
graph TD
    A["Pattern: (a+)+b"] --> B["Input: aaaaaaaaac"]
    
    B --> C["Try (a+)+ first"]
    C --> D[a+ matches 'aaaaaaaaа']
    D --> E[Try to match 'b']
    E --> F[Fails at 'c']
    
    F --> G[Backtrack: try a+ = 'aaaaaaaa']
    G --> H[Second a+ = 'a']
    H --> I[Try to match 'b']
    I --> J[Fails at 'c']
    
    J --> K[Continue backtracking...]
    K --> L[Try all combinations]
    L --> M["2ⁿ possible combinations"]
    
    M --> N[💥 Exponential time complexity]
    
    O["Better Pattern: a+b"] --> P[Linear time complexity]
    O --> Q[No catastrophic backtracking]
    
    style A fill:#ffcdd2
    style N fill:#f44336
    style O fill:#c8e6c9
    style P fill:#4caf50
```

## 📝 Практические применения

### Common Regex Use Cases

```mermaid
graph TD
    A[Regex Applications] --> B[Validation]
    A --> C[Extraction]
    A --> D[Replacement]
    A --> E[Parsing]
    A --> F[Cleaning]
    
    B --> B1[Email validation]
    B --> B2[Phone number format]
    B --> B3[URL validation]
    B --> B4[Password strength]
    B --> B5[Credit card numbers]
    
    C --> C1[Extract URLs from text]
    C --> C2[Extract email addresses]
    C --> C3[Extract dates/times]
    C --> C4[Extract code patterns]
    C --> C5[Extract structured data]
    
    D --> D1[Replace text patterns]
    D --> D2[Format phone numbers]
    D --> D3[Normalize whitespace]
    D --> D4[Replace HTML tags]
    D --> D5[Template processing]
    
    E --> E1[Log file parsing]
    E --> E2[CSV processing]
    E --> E3[Configuration files]
    E --> E4[Protocol parsing]
    E --> E5[Code analysis]
    
    F --> F1[Remove extra spaces]
    F --> F2[Standardize formats]
    F --> F3[Remove special chars]
    F --> F4[Data normalization]
    F --> F5[Input sanitization]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fce4ec
```

### Email Validation Pattern Evolution

```mermaid
graph LR
    A[Email Validation Evolution] --> B[Basic Pattern]
    A --> C[Improved Pattern]
    A --> D[RFC-compliant Pattern]
    A --> E[Practical Pattern]
    
    B --> B1["❌ \\w+@\\w+\\.\\w+"]
    B --> B2[Too restrictive]
    B --> B3[Missing many valid emails]
    
    C --> C1["⚠️ [^@]+@[^@]+\\.[^@]+"]
    C --> C2[Better but still incomplete]
    C --> C3[Allows some invalid emails]
    
    D --> D1[�� RFC 5322 pattern]
    D --> D2[Extremely complex]
    D --> D3[Thousands of characters]
    D --> D4[Theoretical correctness]
    
    E --> E1[✅ Balanced approach]
    E --> E2[Practical validation]
    E --> E3[Good enough for most cases]
    E --> E4[Combined with verification]
    
    F[Recommendation] --> G[Basic regex validation]
    F --> H[+ Email verification]
    F --> I[+ Domain validation]
    
    style B fill:#ffcdd2
    style C fill:#ff9800
    style D fill:#9c27b0
    style E fill:#4caf50
    style F fill:#e3f2fd
```

## 🔧 Advanced Regex Features

### Lookahead and Lookbehind

```mermaid
graph TD
    A[Assertions] --> B[Lookahead]
    A --> C[Lookbehind]
    
    B --> B1["Positive Lookahead (?=...)"]
    B --> B2["Negative Lookahead (?!...)"]
    
    C --> C1["Positive Lookbehind (?<=...)"]
    C --> C2["Negative Lookbehind (?<!...)"]
    
    B1 --> B3[Match if followed by pattern]
    B1 --> B4["Example: \\d+(?=px)"]
    B1 --> B5[Matches digits before 'px']
    
    B2 --> B6[Match if NOT followed by pattern]
    B2 --> B7["Example: \\d+(?!px)"]
    B2 --> B8[Matches digits NOT before 'px']
    
    C1 --> C3[Match if preceded by pattern]
    C1 --> C4["Example: (?<=\\$)\\d+"]
    C1 --> C5[Matches digits after '$']
    
    C2 --> C6[Match if NOT preceded by pattern]
    C2 --> C7["Example: (?<!\\$)\\d+"]
    C2 --> C8[Matches digits NOT after '$']
    
    D[Use Cases] --> E[Password validation]
    D --> F[Extract specific context]
    D --> G[Conditional matching]
    D --> H[Complex replacements]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

### Regex Flags and Modifiers

```mermaid
graph TD
    A[Regex Flags] --> B["re.IGNORECASE / re.I"]
    A --> C["re.MULTILINE / re.M"]
    A --> D["re.DOTALL / re.S"]
    A --> E["re.VERBOSE / re.X"]
    A --> F["re.ASCII / re.A"]
    A --> G["re.UNICODE / re.U"]
    
    B --> B1[Case-insensitive matching]
    B --> B2[Example: 'Hello' matches 'HELLO']
    B --> B3[Good for user input]
    
    C --> C1[^ and $ match line boundaries]
    C --> C2[Not just string boundaries]
    C --> C3[Useful for multiline text]
    
    D --> D1[. matches newlines too]
    D --> D2["By default . doesn't match \\n"]
    D --> D3[Useful for multiline patterns]
    
    E --> E1[Allows whitespace and comments]
    E --> E2[Makes complex patterns readable]
    E --> E3[Ignores whitespace in pattern]
    
    F --> F1[ASCII-only matching]
    F --> F2["\\w, \\d, \\s only match ASCII"]
    F --> F3[Python 3 default behavior]
    
    G --> G1[Unicode support]
    G --> G2["\\w includes Unicode letters"]
    G --> G3[Python 2 compatibility]
    
    H[Flag Combination] --> I["Multiple flags with |"]
    H --> J["Example: re.I | re.M"]
    H --> K["Inline flags: (?im)"]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fce4ec
    style G fill:#e1f5fe
    style H fill:#f8bbd9
```

## 🚀 Alternatives to Regex

### When NOT to Use Regex

```mermaid
graph TD
    A[Regex Limitations] --> B[Complex Parsing]
    A --> C[Performance Critical]
    A --> D[Maintainability]
    A --> E[Nested Structures]
    
    B --> B1[❌ HTML/XML parsing]
    B --> B2[❌ Programming languages]
    B --> B3[❌ Complex protocols]
    B --> B4[✅ Use dedicated parsers]
    
    C --> C1[❌ Large data processing]
    C --> C2[❌ Real-time systems]
    C --> C3[❌ Repeated operations]
    C --> C4[✅ Use compiled solutions]
    
    D --> D1[❌ Complex business logic]
    D --> D2[❌ Team comprehension]
    D --> D3[❌ Future modifications]
    D --> D4[✅ Use clear algorithms]
    
    E --> E1[❌ Balanced parentheses]
    E --> E2[❌ JSON parsing]
    E --> E3[❌ Mathematical expressions]
    E --> E4[✅ Use recursive parsers]
    
    F[Better Alternatives] --> G[Parsing Libraries]
    F --> H[String Methods]
    F --> I[Specialized Tools]
    F --> J[State Machines]
    
    G --> G1[BeautifulSoup for HTML]
    G --> G2[json module for JSON]
    G --> G3[csv module for CSV]
    
    H --> H1["str.split()"]
    H --> H2["str.replace()"]
    H --> H3["str.startswith()"]
    
    style A fill:#e3f2fd
    style B fill:#ffcdd2
    style F fill:#c8e6c9
```

### Performance Comparison

```mermaid
graph LR
    A[String Processing Methods] --> B[Regular Expressions]
    A --> C[String Methods]
    A --> D[Parser Libraries]
    A --> E[Compiled Solutions]
    
    B --> B1[🐌 Moderate speed]
    B --> B2[🧠 High memory for complex patterns]
    B --> B3[⚡ Good for pattern matching]
    B --> B4[📝 Concise for simple tasks]
    
    C --> C1[🚀 Very fast]
    C --> C2[💾 Low memory]
    C --> C3[⚡ Best for simple operations]
    C --> C4[📝 Very readable]
    
    D --> D1[🐌 Slower setup]
    D --> D2[🧠 Higher memory]
    D --> D3[⚡ Fast for complex parsing]
    D --> D4[📚 Feature-rich]
    
    E --> E1[🚀 Fastest execution]
    E --> E2[💾 Optimized memory]
    E --> E3[⚡ Best for repeated operations]
    E --> E4[⚙️ Requires compilation]
    
    F[Use Case Guidelines] --> G[Simple patterns: String methods]
    F --> H[Complex patterns: Regex]
    F --> I[Structured data: Parsers]
    F --> J[Performance critical: Compiled]
    
    style B fill:#ff9800
    style C fill:#4caf50
    style D fill:#2196f3
    style E fill:#9c27b0
    style F fill:#e3f2fd
```

Эти диаграммы показывают полную картину регулярных выражений в Python от основ до продвинутых техник и альтернативных решений. 