---
name: Core Standards
description: This file describes the core coding standards for the project.
applyTo: "**"
---

# Standards

## General Principles

- Write clean, readable, easily testable, and maintainable code
- Use meaningful variable and function names that describe their purpose
- Prefer the Command pattern for classes to create modular and highly testable code
- Keep functions small and focused on a single responsibility
- Write code that is easy to test and mock

## Python Standards

- Follow PEP 8 style guide for Python code
- Use type hints for all function parameters and return values
- Use `snake_case` for functions and variables
- Use `PascalCase` for class names
- Use `UPPER_CASE` for constants
- Maximum line length: 100 characters
- Use docstrings for all public modules, functions, classes, and methods
- Prefer f-strings for string formatting
- Use explicit imports rather than wildcard imports

## Code Organization

- Keep related functionality together in modules

```
services/
└── excuse_generator/
    ├── __init__.py
    ├── interface.py
    ├── exceptions/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── invalid_request_error.py
    │   └── excuse_generation_error.py
    └── operations/
        ├── __init__.py
        └── generate_excuse.py

repositories/
└── excuse_repository/
    ├── __init__.py
    ├── interface.py            # ABC with abstract methods (get_excuse, etc.)
    ├── exceptions/
    │   ├── __init__.py
    │   ├── base.py
    │   └── excuse_generation_error.py
    └── implementations/
        ├── agent/
        │   ├── __init__.py      # AgentExcuseRepository.get_excuse() method
        │   └── settings.py
        └── prepopulated/
            ├── __init__.py      # PrepopulatedExcuseRepository.get_excuse() method
            └── settings.py
```

- Use clear separation of concerns (models, services, repositories, utilities)
- Place business logic in service operations
- Keep data access logic in repository methods (direct method calls)
- The `tests/` directory should mirror the structure of the `app/` directory

```
app/
├── __init__.py
├── models.py
├── utilities/
├── repositories/
│   └── excuse_repository/
│       ├── interface.py         # ABC with abstract methods
│       └── implementations/     # Each implements the methods
│           ├── agent/
│           └── prepopulated/
└── services/
    └── excuse_generator/
        ├── interface.py
        └── operations/
            └── generate_excuse.py

tests/
├── test_models.py
├── utilities/
├── repositories/
│   └── excuse_repository/
│       ├── test_interface.py
│       ├── test_agent_repository.py      # Test agent implementation
│       └── test_prepopulated_repository.py  # Test prepopulated implementation
└── services/
    └── excuse_generator/
        └── operations/
            └── test_generate_excuse.py
```

- Use Pydantic models for data validation and serialization

## Error Handling

- Use specific exception types rather than generic `Exception`
- Log errors with appropriate context using Lambda Powertools logger
- Provide meaningful error messages
- Handle exceptions at appropriate levels
- Use custom exceptions for domain-specific errors

## Testing

- Write unit tests for all business logic
- Aim for high test coverage (80%+ recommended)
- Use descriptive test names that explain what is being tested
- Test both happy paths and error cases

## Configuration

- Use Pydantic Settings for configuration management

```python
# utilities/excuse_agent/settings.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    BASE_URL: str = Field(default=...)
```

- Never hardcode secrets or sensitive data
- Use environment variables for configuration
- Provide sensible defaults where appropriate
- Document all configuration options

```
# .env.example
# Application Configuration
BASE_URL=http://localhost:8000
```

## Logging and Observability

- Use Lambda Powertools logger for structured logging
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
- Include relevant context in log messages
- Add metrics for key operations

## Dependencies

- Use `uv` for package management
- Keep dependencies up to date
- Specify version constraints in `pyproject.toml`
- Document why each dependency is needed
- Avoid unnecessary dependencies

## Code Style

- Self-Documenting Code: Prioritize clear variable names, type hints, and logical structure over comments. Code should explain itself.
- Minimal Documentation: Avoid redundant docstrings or comments. Only document complex algorithms or non-obvious business logic that cannot be simplified.
