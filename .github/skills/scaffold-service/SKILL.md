---
name: scaffold-service
description: Autonomous workflow to scaffold a new Service module. Orchestrates business logic, manages dependencies, and implements the Command Pattern for high testability.
---

# Service Scaffolding Workflow

Scaffold a service module by creating a modular, testable service with a clear separation between orchestration and business logic through a specific implementation of the Command Pattern separating the orchestrator (Service) from the business logic (Operations).

## When to Use

- User requests a new service (e.g., "Create a Task Service to handle reports" or "Add a User Management Service").
- User needs to implement business logic that requires orchestration of multiple dependencies.
- User wants to create modular, testable code using the Command Pattern.
- User is building domain-specific operations that should be decoupled from the service orchestrator.
- User needs to add new operations to an existing service without modifying the service class itself.

## Input Requirements

The agent must extract the following from the user's prompt:

1.  **Service Name:** (e.g., `Task`, `User`, `Notification`) -> Becomes `<Name>Service`.
2.  **Dependencies:** (e.g., `ResourceRepository`, `EmailUtility`) -> Attributes injected into the Service.
3.  **Key Operations:** (e.g., `GenerateReport`, `OnboardUser`) -> Become the operation classes.

## Stage 1: Contract Definition (The Interface)

**Location:** `app/services/<name>/interface.py`
**Goal:** Define the generic contract and declare dependencies abstractly.

1.  **Service ABC:**
    - Name: `<Name>ServiceABC`
    - Attributes: Declare abstract dependencies (e.g., `repository: RepositoryABC`).
    - Method: `abstractmethod async def execute(self, operation: ServiceOperationABC[T]) -> T`
2.  **Operation ABC:**
    - Name: `<Name>OperationABC[T]`
    - Method: `abstractmethod async def execute(self, service: <Name>ServiceABC) -> T`

### Interface Example

```python
# app/services/task_service/interface.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from app.repositories.resource_repository.interface import ResourceRepositoryABC

T = TypeVar("T")

class TaskServiceABC(ABC):
    repository: ResourceRepositoryABC

    @abstractmethod
    async def execute(self, operation: "TaskOperationABC[T]") -> T:
        pass

class TaskOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, service: TaskServiceABC) -> T:
        pass
```

## Stage 2: Implementation Scaffolding (The Orchestrator)

**Location**: app/services/<name>/**init**.py
**Goal**: Create the concrete service that holds the dependencies.

1. **Class Name**: <Name>Service.
2. **Dependency Injection**: Use constructor-based injection with Optional types.
3. **Default Implementation**: Provide a default fallback for dependencies (convenience for production use).
4. **Execute**: Delegate to the operation, passing self.

### Implementation Example

```python
# app/services/task_service/__init__.py
from typing import Optional, TypeVar
from ...repositories.resource_repository.implementations.aws import AwsResourceRepository
from .interface import TaskServiceABC, TaskOperationABC, ResourceRepositoryABC

T = TypeVar("T")

class TaskService(TaskServiceABC):
    repository: ResourceRepositoryABC

    def __init__(self, repository: Optional[ResourceRepositoryABC] = None):
        # Default to concrete implementation if not injected
        self.repository = repository or AwsResourceRepository()

    async def execute(self, operation: TaskOperationABC[T]) -> T:
        return await operation.execute(self)
```

## Stage 3: Operation Scaffolding (The Logic)

**Location**: app/services/<name>/operations/<op_name>.py
**Goal**: Implement the business logic.

1. **Inheritance**: Inherit from <Name>OperationABC[ReturnType].
2. **Dependency Access**: Use the service argument to access repositories or utilities (e.g., `await service.repository.get_by_id(id)`).
3. **Statelessness**: Store request parameters (like query strings or IDs) in self via **init**, but do not store them in the Service class.

### Operation Example

```python
# app/services/task_service/operations/generate_report.py
from ..interface import TaskOperationABC

class GenerateReport(TaskOperationABC[str]):
    def __init__(self, query: str):
        self.query = query

    async def execute(self, service) -> str:
        # Service acts as the orchestrator to access the repository
        # Call repository method directly
        payload = await service.repository.get_report(self.query)

        # Add business logic/transformation here
        return f"Report generated: {payload}"
```

## Stage 4: Exception Strategy

**Location**: app/services/<name>/exceptions/
**Goal**: Handle business rule violations.

1. Create base.py with <Name>ServiceException.
2. Create specific errors like InvalidRequestError or BusinessLogicError.
3. **Constraint**: Catch Repository exceptions here and wrap/re-raise them if they require business context.

## Stage 5: Architecture Verification

Before outputting, verify:

1. Directory Structure:

```
app/services/<name>/
├── __init__.py
├── interface.py
├── models/
├── exceptions/
│   ├── __init__.py
│   └── base.py
└── operations/
    ├── __init__.py
    └── <op_name>.py
```

2. DI Pattern: Does **init** use Optional and provide a default implementation?
3. Imports: Are imports relative where possible?
