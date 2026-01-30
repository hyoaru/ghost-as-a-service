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
# services/task_service/__init__.py
class TaskService(TaskServiceABC):
    repository: ResourceRepositoryABC

    async def execute(self, operation: TaskOperationABC[T]) -> T:
        return await operation.execute(self)

# services/task_service/interface.py
class TaskServiceABC(ABC):
    repository: ResourceRepositoryABC

    @abstractmethod
    async def execute(self, operation: TaskOperationABC[T]) -> T:
        pass

# services/task_service/operations/interface.py
class TaskOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, service: TaskServiceABC) -> T:
        pass

# services/task_service/operations/generate_report.py
class GenerateReport(TaskOperationABC[str]):
    def __init__(self, query: str):
        self.query = query

    async def execute(self, service) -> str:
        payload = await service.repository.execute(FetchReport(self.query))
        # ...
```

## Dependency Injection

- Use constructor-based dependency injection with optional parameters
- Provide default implementations when dependencies are not injected
- Inject abstractions (ABCs) rather than concrete implementations
- Define dependencies as class attributes with type hints

```python
from typing import Optional

class TaskService(TaskServiceABC):
    repository: ResourceRepositoryABC

    def __init__(self, repository: Optional[ResourceRepositoryABC] = None):
        self.repository = repository or ResourceRepository()
```

This pattern allows for:
- Easy dependency injection for testing (pass mock/stub)
- Convenient instantiation in production (uses default implementation)
- Clear dependency declaration through type hints

## Interface/ABC Design

- Create abstract base classes (ABCs) for all services and repositories
- Use `@abstractmethod` decorator for methods that must be implemented
- Keep interfaces focused and cohesive (Interface Segregation Principle)
- Name interfaces with `ABC` suffix (e.g., `TaskServiceABC`)

```python
# repositories/resource/repository_interface.py
class ResourceRepositoryABC(ABC):
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

class TaskOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, service: TaskServiceABC) -> T:
        pass
```

## Async/Await Patterns

- Use `async def` for all I/O-bound operations (database, API calls, file operations)
- Always `await` async operations
- Use `AsyncMock` for mocking async methods in tests
- Keep async operations at the appropriate level (don't make sync code async unnecessarily)

```python
async def execute(self, service: TaskServiceABC) -> str:
    result = await service.repository.execute(operation)
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
# services/task_service/__init__.py
T = TypeVar('T')

__all__ = ["TaskServiceABC", "TaskService"]

class TaskService(TaskServiceABC):
    repository: ResourceRepositoryABC

    def __init__(self, repository: Optional[ResourceRepositoryABC] = None):
        self.repository = repository or ResourceRepository()

    async def execute(self, operation: TaskOperationABC[T]) -> T:
        return await operation.execute(self)
```

### Pattern 2: Separate Files with Exports

Keep implementation in separate files and export through `__init__.py`:

```python
# services/task_service/operations/__init__.py
from .interface import TaskOperationABC
from .generate_report import GenerateReport
from .generate_summary import GenerateSummary

__all__ = [
    "TaskOperationABC",
    "GenerateReport",
    "GenerateSummary",
]
```

**Use Pattern 1** for:
- Main module implementations that are straightforward like services or utilities

**Use Pattern 2** for:
- Implementation directories that need to export multiple implementations like repositories or commands
- When you need to maintain a list of available implementations
- When implementations are organized in separate files

## Naming Conventions

### Commands
- Name commands with action verbs describing what they do
- Be specific and descriptive (e.g., `GetResources`, `CreateUserSession`)

### Services
- Name services after their domain responsibility
- Use noun phrases (e.g., `TaskService`, `UserManagementService`)

### Repositories
- Name repositories after the entity they manage plus `Repository`
- Use singular form (e.g., `ExcuseRepository`, not `ExcusesRepository`)

## Repository Pattern

- Repositories handle all data access logic
- Use the same Command pattern for repository operations
- Keep repositories focused on a single entity or aggregate
- Return domain models, not database records

```python
# repositories/resource/repository_interface.py
class ResourceRepositoryABC(ABC):
    @abstractmethod
    async def execute(self, operation: RepositoryOperationABC[T]) -> T:
        pass

# repositories/resource/operation_interface.py
class ResourceRepositoryOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, repository: ResourceRepositoryABC) -> T:
        pass

# repositories/resource/implementations/aws/__init__.py
class AwsResourceRepository(ResourceRepositoryABC):
    session: Session

    async def execute(self, operation: RepositoryOperationABC[T]) -> T:
        return await operation.execute(self)

# repositories/resource/implementations/aws/operations/get_resources.py
class GetResources(ResourceRepositoryOperationABC[List[Resource]]):
    @abstractmethod
    async def execute(self, repository: ResourceRepositoryABC) -> T:
        if not instance(repository, AwsResourceRepository):
            raise TypeError("Expected AwsResourceRepository")
        # AWS-specific logic here
```

## Service Layer Architecture

- Services contain business logic and orchestration
- Services coordinate between repositories and other services
- Keep services stateless (dependencies only)
- Use operations to encapsulate business logic variations

## Custom Exceptions

- Create domain-specific exceptions for business rule violations
- Inherit from appropriate base exceptions
- Include meaningful error messages and context
- Place exceptions in `exceptions/` directory within each service module

```python
# services/excuse_generator/exceptions/base.py
class ExcuseGeneratorException(Exception):
    """Base exception for excuse generator service."""
    pass

# services/excuse_generator/exceptions/excuse_generation_error.py
class ExcuseGenerationError(ExcuseGeneratorException):
    """Raised when excuse generation fails."""
    pass

# services/excuse_generator/exceptions/invalid_request_error.py
class InvalidRequestError(ExcuseGeneratorException, ValueError):
    """Raised when request validation fails."""
    pass
```

### Exception Organization

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