---
name: scaffold-repository
description: Autonomous workflow to scaffold a new Repository module. Handles the creation of the abstract interface and concrete provider implementations (e.g., AWS, Postgres).
---

# Repository Scaffolding Workflow

Scaffold a repository module by defining an abstract interface contract and implementing concrete provider-specific logic that cleanly separates data access concerns from business logic.

## When to Use

- User requests a new repository (e.g., "Create a User Repository backed by Postgres" or "Add an AWS implementation for Documents").
- User needs to add data access logic for a new domain entity.
- User wants to implement a new provider backend (e.g., Redis, DynamoDB) for an existing repository.
- User is setting up the persistence layer for a service that doesn't yet have repository infrastructure.

## Input Requirements

The agent must extract the following from the user's prompt:

1.  **Entity Name:** (e.g., `User`, `Resource`, `Order`) -> Becomes `<Entity>Repository`.
2.  **Provider Name:** (e.g., `Aws`, `Postgres`, `Redis`, `Mock`) -> Becomes the implementation sub-module.
3.  **Key Operations:** (e.g., `GetById`, `Save`, `List`) -> Become the operation classes.

## Stage 1: Contract Definition (The Interface)

**Location:** `app/repositories/<entity>_repository/interface.py`
**Goal:** Define the generic contract that the Service layer will rely on.

1.  **Repository ABC:**
    - Name: `<Entity>RepositoryABC`
    - Method: `abstractmethod async def execute(self, operation: RepositoryOperationABC[T]) -> T`
2.  **Operation ABC:**
    - Name: `<Entity>RepositoryOperationABC[T]`
    - Method: `abstractmethod async def execute(self, repository: <Entity>RepositoryABC) -> T`

### Interface Example

```python
# app/repositories/resource_repository/interface.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")

class ResourceRepositoryABC(ABC):
    @abstractmethod
    async def execute(self, operation: "ResourceRepositoryOperationABC[T]") -> T:
        pass

class ResourceRepositoryOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, repository: ResourceRepositoryABC) -> T:
        pass
```

## Stage 2: Implementation Scaffolding (The Provider)

**Location**: app/repositories/<entity>\_repository/implementations/<provider>/**init**.py
**Goal**: Create the concrete repository that holds the specific infrastructure state.

1. **Class Name**: <Provider><Entity>Repository (e.g., AwsResourceRepository).

2. **State**: Initialize the specific client/session (e.g., self.session or self.db).

3. **Execute**: Delegate to the operation, passing self.

### Implementation Example

```python
# app/repositories/resource_repository/implementations/aws/__init__.py
from boto3.session import Session
from ...interface import ResourceRepositoryABC, ResourceRepositoryOperationABC

class AwsResourceRepository(ResourceRepositoryABC):
    def __init__(self):
        self.session = Session()

    async def execute(self, operation: ResourceRepositoryOperationABC[T]) -> T:
        return await operation.execute(self)
```

## Stage 3: Operation Scaffolding (The Logic)

**Location**: app/repositories/<entity>\_repository/implementations/<provider>/operations/<op_name>.py
**Goal**: Implement the logic using the specific provider.

1. **Inheritance**: Inherit from <Entity>RepositoryOperationABC[ReturnType].
2. **Runtime Guard**: CRITICAL STEP. The operation receives the abstract RepositoryABC. You must check isinstance to ensure it is the expected concrete class (e.g., AwsResourceRepository) before accessing specific state (like .session).
3. **Return Type**: Ensure it returns Domain Models, not raw DB cursors/responses.

### Operation Example

```python
# app/repositories/resource_repository/implementations/aws/operations/get_resources.py
from typing import List
from ...interface import ResourceRepositoryABC, ResourceRepositoryOperationABC
from .. import AwsResourceRepository

class GetResources(ResourceRepositoryOperationABC[List[str]]):
    async def execute(self, repository: ResourceRepositoryABC) -> List[str]:
        # Runtime Guard: Ensure we are running on the correct provider
        if not isinstance(repository, AwsResourceRepository):
            raise TypeError(f"Expected AwsResourceRepository, got {type(repository)}")

        # Access provider-specific state
        client = repository.session.client('s3')
        # ... logic ...
        return ["resource1", "resource2"]
```

## Stage 4: Exception Strategy

**Location**: app/repositories/<entity>\_repository/exceptions/
**Goal**: Isolate DB errors from the Service layer.

1. Create base.py with <Entity>RepositoryException.
2. Create specific errors like EntityNotFoundError or StorageError.
3. **Constraint**: Operations should catch provider-specific errors (e.g., ClientError, SQLAlchemyError) and re-raise them as Repository Exceptions.

## Stage 5: Architecture Verification

Before outputting, verify:

1. **Directory Structure**:

```plaintext
app/repositories/<entity>_repository/
├── interface.py
└── implementations/
    └── <provider>/
        ├── __init__.py
        └── operations/
            ├── __init__.py
            └── <op_name>.py
```

1. **Runtime Safety**: Does the concrete operation include the isinstance check?
2. **Imports**: Are imports relative? (e.g., from ...interface import ...).
