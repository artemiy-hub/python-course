# Диаграммы: Тестирование в Python

## 🧪 Архитектура тестирования

### Пирамида тестирования

```mermaid
graph TD
    A[Test Pyramid] --> B[Unit Tests<br/>70%]
    A --> C[Integration Tests<br/>20%]
    A --> D[E2E/UI Tests<br/>10%]
    
    B --> B1[✅ Fast execution]
    B --> B2[✅ Isolated components]
    B --> B3[✅ Easy to maintain]
    B --> B4[✅ Quick feedback]
    
    C --> C1[🔄 Module interaction]
    C --> C2[🔄 Database integration]
    C --> C3[🔄 API testing]
    C --> C4[🔄 Service communication]
    
    D --> D1[🌐 Full user workflows]
    D --> D2[🌐 Browser automation]
    D --> D3[🌐 End-to-end scenarios]
    D --> D4[🌐 Production-like environment]
    
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#ffcdd2
```

### Типы тестирования

```mermaid
graph LR
    A[Testing Types] --> B[Functional Testing]
    A --> C[Non-Functional Testing]
    A --> D[Structural Testing]
    
    B --> B1[Unit Testing]
    B --> B2[Integration Testing]
    B --> B3[System Testing]
    B --> B4[Acceptance Testing]
    
    C --> C1[Performance Testing]
    C --> C2[Security Testing]
    C --> C3[Usability Testing]
    C --> C4[Compatibility Testing]
    
    D --> D1[White Box Testing]
    D --> D2[Black Box Testing]
    D --> D3[Gray Box Testing]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

## 🏗️ Фреймворки тестирования Python

### unittest vs pytest сравнение

```mermaid
graph TD
    A[Python Testing Frameworks] --> B[unittest<br/>Built-in]
    A --> C[pytest<br/>Third-party]
    
    B --> B1[✅ No dependencies]
    B --> B2[✅ Standard library]
    B --> B3[❌ Verbose syntax]
    B --> B4[❌ Limited fixtures]
    B --> B5[❌ Class-based structure]
    
    C --> C1[✅ Simple syntax]
    C --> C2[✅ Powerful fixtures]
    C --> C3[✅ Plugin ecosystem]
    C --> C4[✅ Parametrization]
    C --> C5[❌ External dependency]
    
    style B fill:#ffeb3b
    style C fill:#4caf50
```

### pytest архитектура

```mermaid
graph TD
    A[pytest Framework] --> B[Test Discovery]
    A --> C[Test Execution]
    A --> D[Fixtures System]
    A --> E[Plugin System]
    A --> F[Reporting]
    
    B --> B1[test_*.py files]
    B --> B2[*_test.py files]
    B --> B3[Test* classes]
    B --> B4[test_* functions]
    
    C --> C1[Setup/Teardown]
    C --> C2[Parallel execution]
    C --> C3[Selective running]
    C --> C4[Failure handling]
    
    D --> D1[Function scope]
    D --> D2[Class scope]
    D --> D3[Module scope]
    D --> D4[Session scope]
    
    E --> E1[pytest-cov]
    E --> E2[pytest-mock]
    E --> E3[pytest-xdist]
    E --> E4[pytest-django]
    
    F --> F1[Console output]
    F --> F2[HTML reports]
    F --> F3[XML reports]
    F --> F4[Coverage reports]
    
    style A fill:#e3f2fd
    style D fill:#c8e6c9
    style E fill:#fff3e0
    style F fill:#f3e5f5
```

## 🔧 Fixtures и Setup/Teardown

### Жизненный цикл fixtures

```mermaid
sequenceDiagram
    participant Test as Test Function
    participant Session as Session Fixture
    participant Module as Module Fixture
    participant Class as Class Fixture
    participant Function as Function Fixture
    
    Note over Session,Function: Test Session Start
    Session->>Session: Setup (once per session)
    
    Note over Module,Function: Module Start
    Module->>Module: Setup (once per module)
    
    Note over Class,Function: Class Start
    Class->>Class: Setup (once per class)
    
    Note over Function,Function: Test 1
    Function->>Function: Setup
    Test->>Function: Execute test_example_1()
    Function->>Function: Teardown
    
    Note over Function,Function: Test 2
    Function->>Function: Setup
    Test->>Function: Execute test_example_2()
    Function->>Function: Teardown
    
    Note over Class,Function: Class End
    Class->>Class: Teardown
    
    Note over Module,Function: Module End
    Module->>Module: Teardown
    
    Note over Session,Function: Test Session End
    Session->>Session: Teardown
```

### Dependency Injection в pytest

```mermaid
graph TD
    A[Test Function] --> B[Direct Dependencies]
    A --> C[Indirect Dependencies]
    
    B --> B1[db_session]
    B --> B2[api_client]
    B --> B3[temp_file]
    
    C --> C1[database_engine]
    C --> C2[config_settings]
    C --> C3[temp_directory]
    
    B1 --> C1
    B2 --> C2
    B3 --> C3
    
    D[pytest] --> E[Fixture Resolution]
    E --> F[Dependency Graph]
    F --> G[Execution Order]
    
    style A fill:#e3f2fd
    style D fill:#c8e6c9
    style E fill:#fff3e0
```

## 🎭 Mocking и Test Doubles

### Типы Test Doubles

```mermaid
graph TD
    A[Test Doubles] --> B[Dummy]
    A --> C[Fake]
    A --> D[Stub]
    A --> E[Spy]
    A --> F[Mock]
    
    B --> B1[Placeholder objects]
    B --> B2[No real implementation]
    B --> B3[Just to fill parameters]
    
    C --> C1[Working implementation]
    C --> C2[Simplified version]
    C --> C3[In-memory database]
    
    D --> D1[Predefined responses]
    D --> D2[Controlled behavior]
    D --> D3[Method return values]
    
    E --> E1[Records method calls]
    E --> E2[Verifies interactions]
    E --> E3[Partial real object]
    
    F --> F1[Full behavior simulation]
    F --> F2[Expectation verification]
    F --> F3[Complete replacement]
    
    style A fill:#e3f2fd
    style B fill:#ffcdd2
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#f3e5f5
    style F fill:#c8e6c9
```

### Mock объекты в Python

```mermaid
graph LR
    A[Python Mocking] --> B[unittest.mock]
    A --> C[pytest-mock]
    A --> D[Third-party]
    
    B --> B1["Mock()"]
    B --> B2["MagicMock()"]
    B --> B3["@patch decorator"]
    B --> B4["patch() context manager"]
    
    C --> C1[mocker fixture]
    C --> C2[Automatic cleanup]
    C --> C3[pytest integration]
    
    D --> D1[responses]
    D --> D2[httpretty]
    D --> D3[freezegun]
    D --> D4[factory_boy]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

## 📊 Покрытие кода и метрики

### Типы покрытия кода

```mermaid
graph TD
    A[Code Coverage Types] --> B[Line Coverage]
    A --> C[Branch Coverage]
    A --> D[Function Coverage]
    A --> E[Statement Coverage]
    
    B --> B1[Executed lines / Total lines]
    B --> B2[Most common metric]
    B --> B3[Easy to measure]
    
    C --> C1[Executed branches / Total branches]
    C --> C2[if/else, loops, exceptions]
    C --> C3[More thorough than line coverage]
    
    D --> D1[Called functions / Total functions]
    D --> D2[Function-level granularity]
    D --> D3[API coverage verification]
    
    E --> E1[Executed statements / Total statements]
    E --> E2[Similar to line coverage]
    E --> E3[Language-specific]
    
    F[Coverage Quality] --> G[90-95%: Excellent]
    F --> H[80-90%: Good]
    F --> I[70-80%: Acceptable]
    F --> J[<70%: Needs improvement]
    
    style G fill:#4caf50
    style H fill:#8bc34a
    style I fill:#ffeb3b
    style J fill:#ff5722
```

### Coverage.py архитектура

```mermaid
graph TD
    A[coverage.py] --> B[Data Collection]
    A --> C[Data Analysis]
    A --> D[Report Generation]
    
    B --> B1[Trace function]
    B --> B2[Line execution tracking]
    B --> B3[Branch tracking]
    B --> B4[Coverage database]
    
    C --> C1[Source code analysis]
    C --> C2[Executable line detection]
    C --> C3[Branch analysis]
    C --> C4[Exclusion patterns]
    
    D --> D1[Console report]
    D --> D2[HTML report]
    D --> D3[XML report]
    D --> D4[JSON report]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

## 🚀 TDD и BDD методологии

### TDD цикл (Red-Green-Refactor)

```mermaid
graph LR
    A[Red<br/>Write failing test] --> B[Green<br/>Make test pass]
    B --> C[Refactor<br/>Improve code]
    C --> A
    
    A --> A1[❌ Test fails]
    A --> A2[Define requirements]
    A --> A3[Minimal test code]
    
    B --> B1[✅ Test passes]
    B --> B2[Minimal implementation]
    B --> B3[Quick solution]
    
    C --> C1[🔧 Clean code]
    C --> C2[Remove duplication]
    C --> C3[Improve design]
    
    style A fill:#ffcdd2
    style B fill:#c8e6c9
    style C fill:#fff3e0
```

### BDD процесс (Behavior-Driven Development)

```mermaid
graph TD
    A[BDD Process] --> B[Discovery]
    A --> C[Formulation]
    A --> D[Automation]
    
    B --> B1[Stakeholder collaboration]
    B --> B2[User story analysis]
    B --> B3[Example identification]
    
    C --> C1[Given-When-Then scenarios]
    C --> C2[Concrete examples]
    C --> C3[Acceptance criteria]
    
    D --> D1[Executable specifications]
    D --> D2[Step definitions]
    D --> D3[Test automation]
    
    E[BDD Tools] --> F[behave]
    E --> G[pytest-bdd]
    E --> H[lettuce]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

## 🔄 Параметризация и Data-Driven тестирование

### pytest параметризация

```mermaid
graph TD
    A[Parametrization Types] --> B["@pytest.mark.parametrize"]
    A --> C[pytest.param]
    A --> D[Fixture parametrization]
    A --> E[External data sources]
    
    B --> B1[Simple values]
    B --> B2[Multiple parameters]
    B --> B3[Test ID generation]
    
    C --> C1[Custom test IDs]
    C --> C2[Conditional skipping]
    C --> C3[Expected failures]
    
    D --> D1[Indirect parametrization]
    D --> D2[Fixture combinations]
    D --> D3[Setup variations]
    
    E --> E1[CSV files]
    E --> E2[JSON data]
    E --> E3[Database queries]
    E --> E4[API responses]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### Data-Driven Testing Flow

```mermaid
sequenceDiagram
    participant TestRunner as Test Runner
    participant DataSource as Data Source
    participant TestCase as Test Case
    participant SUT as System Under Test
    
    TestRunner->>DataSource: Load test data
    DataSource-->>TestRunner: Return data sets
    
    loop For each data set
        TestRunner->>TestCase: Execute with data
        TestCase->>SUT: Call with input data
        SUT-->>TestCase: Return result
        TestCase->>TestCase: Assert expected result
        TestCase-->>TestRunner: Test result
    end
    
    TestRunner->>TestRunner: Aggregate results
    TestRunner-->>TestRunner: Generate report
```

## 🏭 Integration и E2E тестирование

### Уровни интеграционного тестирования

```mermaid
graph TD
    A[Integration Testing Levels] --> B[Component Integration]
    A --> C[System Integration]
    A --> D[External Integration]
    
    B --> B1[Module-to-module]
    B --> B2[Class interactions]
    B --> B3[Package interfaces]
    
    C --> C1[Database integration]
    C --> C2[File system access]
    C --> C3[Configuration loading]
    
    D --> D1[External APIs]
    D --> D2[Third-party services]
    D --> D3[Message queues]
    
    E[Testing Strategies] --> F[Big Bang]
    E --> G[Incremental]
    E --> H[Top-down]
    E --> I[Bottom-up]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

### E2E Testing Architecture

```mermaid
graph TD
    A[E2E Testing Stack] --> B[Test Framework]
    A --> C[Browser Automation]
    A --> D[Page Objects]
    A --> E[Test Data Management]
    A --> F[Environment Setup]
    
    B --> B1[pytest]
    B --> B2[unittest]
    B --> B3["behave (BDD)"]
    
    C --> C1[Selenium WebDriver]
    C --> C2[Playwright]
    C --> C3["Requests (API)"]
    
    D --> D1[Page Object Model]
    D --> D2[Component Objects]
    D --> D3[API Clients]
    
    E --> E1[Test databases]
    E --> E2[Mock services]
    E --> E3[Data factories]
    
    F --> F1[Docker containers]
    F --> F2[Test environments]
    F --> F3[CI/CD pipelines]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fce4ec
```

## 📈 Тестирование производительности

### Типы performance тестов

```mermaid
graph TD
    A[Performance Testing Types] --> B[Load Testing]
    A --> C[Stress Testing]
    A --> D[Volume Testing]
    A --> E[Spike Testing]
    A --> F[Endurance Testing]
    
    B --> B1[Normal expected load]
    B --> B2[Response time verification]
    B --> B3[Throughput measurement]
    
    C --> C1[Beyond normal capacity]
    C --> C2[Breaking point discovery]
    C --> C3[System stability under stress]
    
    D --> D1[Large amounts of data]
    D --> D2[Database performance]
    D --> D3[Memory usage]
    
    E --> E1[Sudden load increases]
    E --> E2[Auto-scaling testing]
    E --> E3[Traffic spikes]
    
    F --> F1[Extended periods]
    F --> F2[Memory leaks detection]
    F --> F3[Long-term stability]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#ffcdd2
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#e8f5e8
```

### Performance Testing Tools

```mermaid
graph LR
    A[Python Performance Testing] --> B[Load Testing]
    A --> C[Profiling]
    A --> D[Benchmarking]
    
    B --> B1[locust]
    B --> B2[pytest-benchmark]
    B --> B3["Artillery (external)"]
    
    C --> C1[cProfile]
    C --> C2[line_profiler]
    C --> C3[memory_profiler]
    C --> C4[py-spy]
    
    D --> D1[pytest-benchmark]
    D --> D2[timeit]
    D --> D3[perfplot]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

## 🔧 CI/CD и автоматизация тестирования

### CI/CD Testing Pipeline

```mermaid
graph LR
    A[Code Commit] --> B[Unit Tests]
    B --> C[Integration Tests]
    C --> D[Code Quality]
    D --> E[Security Tests]
    E --> F[Build & Package]
    F --> G[Deploy to Staging]
    G --> H[E2E Tests]
    H --> I[Performance Tests]
    I --> J[Deploy to Production]
    
    B --> B1[✅ Fast feedback]
    C --> C1[🔄 Component interaction]
    D --> D1[📊 Coverage, linting]
    E --> E1[🔒 Vulnerability scanning]
    H --> H1[🌐 User workflows]
    I --> I1[⚡ Load testing]
    
    style A fill:#e3f2fd
    style J fill:#4caf50
    style B1 fill:#c8e6c9
    style C1 fill:#fff3e0
    style D1 fill:#f3e5f5
    style E1 fill:#ffcdd2
    style H1 fill:#e8f5e8
    style I1 fill:#fce4ec
```

### Test Automation Pyramid в CI/CD

```mermaid
graph TD
    A[Test Automation in CI/CD] --> B[Pre-commit Hooks]
    A --> C[Continuous Testing]
    A --> D[Test Reporting]
    A --> E[Quality Gates]
    
    B --> B1[Linting]
    B --> B2[Unit tests]
    B --> B3[Type checking]
    
    C --> C1[Parallel execution]
    C --> C2[Test selection]
    C --> C3[Flaky test detection]
    
    D --> D1[Test results aggregation]
    D --> D2[Coverage reporting]
    D --> D3[Failure analysis]
    
    E --> E1[Coverage thresholds]
    E --> E2[Test pass rates]
    E --> E3[Performance benchmarks]
    
    style A fill:#e3f2fd
    style B fill:#c8e6c9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#ffcdd2
```

Эти диаграммы показывают полную картину тестирования в Python от базовых концепций до продвинутых техник и интеграции с CI/CD. 