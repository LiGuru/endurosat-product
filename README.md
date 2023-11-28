Project Structure

```markdown
.
├── application
│   ├── services
│   └── use_cases
├── docs
├── domain
│   └── model
├── external_services
│   └── http
├── infrastructure
│   ├── commons
│   ├── helpers
│   └── logging
├── logs
└── tests
    ├── application
    │   ├── tests_services
    │   └── tests_use_cases
    ├── domain
    │   └── test_model
    ├── external_services
    │   └── http
    └── infrastructure


```

```bash
mkdir -p application/use_cases/../services docs domain/model external_services/http infrastructure/logging/../commons/../helpers logs tests/application/tests_use_cases/../tests_services tests/domain/test_model tests/infrastructure/ tests/external_services/http
touch application/__init__.py domain/__init__.py external_services/__init__.py infrastructure/__init__.py tests/__init__.py
touch application/services/__init__.py application/use_cases/__init__.py domain/model/__init__.py external_services/http/__init__.py infrastructure/helpers/__init__.py infrastructure/logging/__init__.py infrastructure/commons/__init__.py tests/__init__.py
```