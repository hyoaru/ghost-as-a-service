---
name: Development Standards
description: This file describes the development standards for the project.
applyTo: "{app/utilities,app/repositories,app/services}/**/*.py"
---

# Development Standards

## Architecture Principles

- Follow the SOLID (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion) principle
- Implement the Command pattern for classes to create modular and highly testable code

## Command Pattern Implementation

```python
# __init__.py
class ExcuseGenerator(ExcuseGeneratorABC):
    excuse_repository: ExcuseRepositoryABC

    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        return await operation.execute(self)

# interface.py
class ExcuseGeneratorABC(ABC):
    excuse_repository: ExcuseRepositoryABC

    @abstractmethod
    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        pass

# operations/interface.py
class ExcuseGeneratorOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, service: ExcuseGeneratorABC) -> T:
        pass

# operations/generate_vague.py
class GenerateVagueExcuse(ExcuseGeneratorOperationABC[str]):
    def __init__(self, request: str):
        self.request = request

    async def execute(self, service) -> str:
      result = await service.excuse_repository.execute(GetVague(self.request))
      # ...
```

## Dependency Injection

- Use constructor-based dependency injection with optional parameters
- Provide default implementations when dependencies are not injected
- Inject abstractions (ABCs) rather than concrete implementations
- Define dependencies as class attributes with type hints

```python
from typing import Optional

class ExcuseGenerator(ExcuseGeneratorABC):
    excuse_repository: ExcuseRepositoryABC

    def __init__(self, excuse_repository: Optional[ExcuseRepositoryABC] = None):
        self.excuse_repository = excuse_repository or ExcuseRepository()
```

This pattern allows for:
- Easy dependency injection for testing (pass mock/stub)
- Convenient instantiation in production (uses default implementation)
- Clear dependency declaration through type hints

## Interface/ABC Design

- Create abstract base classes (ABCs) for all services and repositories
- Use `@abstractmethod` decorator for methods that must be implemented
- Keep interfaces focused and cohesive (Interface Segregation Principle)
- Name interfaces with `ABC` suffix (e.g., `ExcuseGeneratorABC`)

```python
from abc import ABC, abstractmethod

class ExcuseRepositoryABC(ABC):
    @abstractmethod
    async def execute(self, operation: RepositoryOperationABC[T]) -> T:
        pass
```

## Type Hints and Generics

- Use `Generic[T]` for operations that return different types
- Always specify return types for operations
- Use `TypeVar` for complex generic patterns
- Prefer explicit type hints over `Any`

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class ExcuseGeneratorOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, service: ExcuseGeneratorABC) -> T:
        pass
```

## Async/Await Patterns

- Use `async def` for all I/O-bound operations (database, API calls, file operations)
- Always `await` async operations
- Use `AsyncMock` for mocking async methods in tests
- Keep async operations at the appropriate level (don't make sync code async unnecessarily)

```python
async def execute(self, service: ExcuseGeneratorABC) -> str:
    result = await service.excuse_repository.execute(operation)
    return result
```

## Module Initialization

- Use `__init__.py` to control module exports
- Export only public interfaces and concrete classes
- Keep `__init__.py` clean and minimal
- Import classes in `__init__.py` for cleaner external imports

### Pattern 1: Module as Entry Point

Place the main implementation directly in `__init__.py`:

```python
# services/excuse_generator/__init__.py
from typing import Optional
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

__all__ = ["ExcuseGeneratorABC", "ExcuseGenerator"]

class ExcuseGenerator(ExcuseGeneratorABC):
    excuse_repository: ExcuseRepositoryABC

    def __init__(self, excuse_repository: Optional[ExcuseRepositoryABC] = None):
        self.excuse_repository = excuse_repository or ExcuseRepository()

    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        return await operation.execute(self)
```

### Pattern 2: Separate Files with Exports

Keep implementation in separate files and export through `__init__.py`:

```python
# services/excuse_generator/operations/__init__.py
from .interface import ExcuseGeneratorOperationABC
from .generate_vague import GenerateVague
from .generate_technical import GenerateTechnical

__all__ = [
    "ExcuseGeneratorOperationABC",
    "GenerateVague",
    "GenerateTechnical",
]
```

**Use Pattern 1** for:
- Main module implementations
- Single-file modules

**Use Pattern 2** for:
- Implementation directories that need to export multiple implementations
- When you need to maintain a list of available implementations
- When implementations are organized in separate files

## Naming Conventions

### Commands
- Name commands with action verbs describing what they do
- Be specific and descriptive (e.g., `GenerateVague`)

### Services
- Name services after their domain responsibility
- Use noun phrases (e.g., `ExcuseGenerator`, `UserAuthenticator`)

### Repositories
- Name repositories after the entity they manage plus `Repository`
- Use singular form (e.g., `ExcuseRepository`, not `ExcusesRepository`)

## Repository Pattern

- Repositories handle all data access logic
- Use the same Command pattern for repository operations
- Keep repositories focused on a single entity or aggregate
- Return domain models, not database records

```python
class ExcuseRepository(ExcuseRepositoryABC):
    async def execute(self, operation: RepositoryOperationABC[T]) -> T:
        return await operation.execute(self)

class GetVague(RepositoryOperationABC[str]):
    def __init__(self, prompt: str):
        self.prompt = prompt

    async def execute(self, repository: ExcuseRepositoryABC) -> str:
        # Data access logic here
        pass
```

## Service Layer Architecture

- Services contain business logic and orchestration
- Services coordinate between repositories and other services
- Keep services stateless (dependencies only)
- Use operations to encapsulate business logic variations

```python
class ExcuseGenerator(ExcuseGeneratorABC):
    excuse_repository: ExcuseRepositoryABC

    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        return await operation.execute(self)
```

## Custom Exceptions

- Create domain-specific exceptions for business rule violations
- Inherit from appropriate base exceptions
- Include meaningful error messages and context

```python
class ExcuseGenerationError(Exception):
    """Raised when excuse generation fails."""
    pass

class InvalidRequestError(ValueError):
    """Raised when request validation fails."""
    pass
```