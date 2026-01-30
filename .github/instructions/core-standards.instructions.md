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
        ├── interface.py
        └── generate_vague.py
```

- Use clear separation of concerns (models, services, repositories, utilities)
- Place business logic in service classes
- Keep data access logic in repository classes
- The `tests/` directory should mirror the structure of the `app/` directory

```
app/
├── __init__.py
├── models.py
├── utilities/
├── repositories/
└── services/
    ├── __init__.py
    └── excuse_generator/
        ├── __init__.py
        ├── interface.py
        └── operations/
            ├── __init__.py
            └── generate_vague.py

tests/
├── test_models.py
├── utilities/
├── repositories/
└── services/
    ├── __init__.py
    └── test_excuse_generator/
      └── operations/
          └── test_generate_vague.py
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

## Documentation

- Write clear and concise docstrings
- Keep README.md up to date
- Only add inline comments for code that is not self-documenting or is complex
- Provide usage examples in documentation
- Document API endpoints and their expected inputs/outputs
