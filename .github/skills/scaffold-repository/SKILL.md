---
name: scaffold-repository
description: Autonomous workflow to scaffold a new Repository module with direct methods for data access.
---

# Repository Scaffolding Workflow

Scaffold a repository module with direct methods for straightforward data access.

## When to Use

- User requests a new repository (e.g., "Create a User Repository backed by Postgres" or "Add an AWS implementation for Documents").
- User needs to add data access logic for a new domain entity.
- User wants to implement a new provider backend (e.g., Redis, DynamoDB) for an existing repository.
- User is setting up the persistence layer for a service that doesn't yet have repository infrastructure.

## Input Requirements

The agent must extract the following from the user's prompt:

1.  **Entity Name:** (e.g., `User`, `Resource`, `Order`) -> Becomes `<Entity>Repository`.
2.  **Provider Names:** (e.g., `Aws`, `Postgres`, `Redis`, `Mock`) -> Become implementation sub-modules.
3.  **Key Methods:** (e.g., `get_by_id`, `save`, `delete`, `list_all`) -> Become abstract methods.

## Stage 1: Contract Definition (The Interface)

**Location:** `app/repositories/<entity>/interface.py`
**Goal:** Define abstract methods that ALL implementations must provide.

1.  **Repository ABC:**
    - Name: `<Entity>RepositoryABC`
    - Methods: Abstract methods for data access (e.g., `async def get_by_id(self, id: str)`, `async def save(self, entity)`, etc.)
    - Methods should be specific to the data operations needed

### Interface Example

```python
# app/repositories/resource_repository/interface.py
from abc import ABC, abstractmethod
from typing import List, Optional

class ResourceRepositoryABC(ABC):
    """Repository interface defining data access methods."""

    @abstractmethod
    async def get_by_id(self, resource_id: str) -> Optional[Resource]:
        """Get a resource by ID."""
        pass

    @abstractmethod
    async def list_all(self, filter_type: str = None) -> List[Resource]:
        """List all resources, optionally filtered."""
        pass

    @abstractmethod
    async def save(self, resource: Resource) -> Resource:
        """Save or update a resource."""
        pass

    @abstractmethod
    async def delete(self, resource_id: str) -> bool:
        """Delete a resource by ID."""
        pass
```

## Stage 2: Implementation Scaffolding (Provider-Specific)

**Location**: `app/repositories/<entity>/implementations/<provider>/__init__.py`
**Goal**: Implement the abstract methods using provider-specific logic.

1. **Class Name**: `<Provider><Entity>Repository` (e.g., `AwsResourceRepository`, `PostgresResourceRepository`).
2. **Initialization**: Set up provider-specific dependencies (sessions, connections, etc.).
3. **Methods**: Implement each abstract method from the interface.

### Implementation Examples

```python
# app/repositories/resource_repository/implementations/aws/__init__.py
from boto3.session import Session
from typing import List, Optional
from ...interface import ResourceRepositoryABC
from .settings import Settings

class AwsResourceRepository(ResourceRepositoryABC):
    """AWS S3-backed resource repository."""

    def __init__(self, session: Session = None, settings: Settings = None):
        self.session = session or Session()
        self.settings = settings or Settings()
        self.bucket = self.settings.S3_BUCKET_NAME

    async def get_by_id(self, resource_id: str) -> Optional[Resource]:
        """Get resource from S3."""
        client = self.session.client('s3')
        try:
            response = client.get_object(Bucket=self.bucket, Key=resource_id)
            # Parse and return Resource
            return Resource.from_json(response['Body'].read())
        except client.exceptions.NoSuchKey:
            return None

    async def list_all(self, filter_type: str = None) -> List[Resource]:
        """List resources from S3."""
        client = self.session.client('s3')
        response = client.list_objects_v2(Bucket=self.bucket)
        resources = [Resource.from_key(obj['Key']) for obj in response.get('Contents', [])]

        if filter_type:
            resources = [r for r in resources if r.type == filter_type]

        return resources

    async def save(self, resource: Resource) -> Resource:
        """Save resource to S3."""
        client = self.session.client('s3')
        client.put_object(
            Bucket=self.bucket,
            Key=resource.id,
            Body=resource.to_json()
        )
        return resource

    async def delete(self, resource_id: str) -> bool:
        """Delete resource from S3."""
        client = self.session.client('s3')
        client.delete_object(Bucket=self.bucket, Key=resource_id)
        return True
```

```python
# app/repositories/resource_repository/implementations/postgres/__init__.py
from typing import List, Optional
from ...interface import ResourceRepositoryABC
from .settings import Settings

class PostgresResourceRepository(ResourceRepositoryABC):
    """Postgres-backed resource repository."""

    def __init__(self, db_connection, settings: Settings = None):
        self.db = db_connection
        self.settings = settings or Settings()

    async def get_by_id(self, resource_id: str) -> Optional[Resource]:
        """Get resource from Postgres."""
        query = "SELECT * FROM resources WHERE id = ?"
        result = await self.db.fetch_one(query, (resource_id,))
        return Resource.from_row(result) if result else None

    async def list_all(self, filter_type: str = None) -> List[Resource]:
        """List resources from Postgres."""
        if filter_type:
            query = "SELECT * FROM resources WHERE type = ?"
            results = await self.db.fetch_all(query, (filter_type,))
        else:
            query = "SELECT * FROM resources"
            results = await self.db.fetch_all(query)

        return [Resource.from_row(row) for row in results]

    async def save(self, resource: Resource) -> Resource:
        """Save resource to Postgres."""
        query = """
            INSERT INTO resources (id, name, type, data)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (id) DO UPDATE SET name = ?, type = ?, data = ?
        """
        await self.db.execute(query, (
            resource.id, resource.name, resource.type, resource.data,
            resource.name, resource.type, resource.data
        ))
        return resource

    async def delete(self, resource_id: str) -> bool:
        """Delete resource from Postgres."""
        query = "DELETE FROM resources WHERE id = ?"
        await self.db.execute(query, (resource_id,))
        return True
```

## Stage 3: Exception Strategy

**Location**: `app/repositories/<entity>/exceptions/`
**Goal**: Isolate data access errors from the Service layer.

1. Create `base.py` with `<Entity>RepositoryException`.
2. Create specific errors like `EntityNotFoundError` or `StorageError`.
3. **Constraint**: Repository methods should catch provider-specific errors (e.g., `ClientError`, `SQLAlchemyError`) and re-raise them as Repository Exceptions.

### Exception Examples

```python
# app/repositories/resource_repository/exceptions/base.py
class ResourceRepositoryException(Exception):
    """Base exception for all Resource Repository errors."""
    pass

# app/repositories/resource_repository/exceptions/resource_not_found_error.py
from .base import ResourceRepositoryException

class ResourceNotFoundError(ResourceRepositoryException):
    """Raised when a resource cannot be found."""
    pass

# app/repositories/resource_repository/exceptions/storage_error.py
from .base import ResourceRepositoryException

class StorageError(ResourceRepositoryException):
    """Raised when storage operations fail."""
    pass
```

## Stage 4: Configuration Strategy

**Location**: `app/repositories/<entity>/implementations/<provider>/settings.py`
**Goal**: Encapsulate provider-specific configuration using Pydantic.

1. **Class Name**: `Settings`
2. **Inheritance**: Inherit from `pydantic_settings.BaseSettings`
3. **Scope**: Configuration specific to this provider (table names, connection strings, static data, etc.)

### Settings Examples

```python
# app/repositories/resource_repository/implementations/aws/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    AWS_REGION: str = Field(default="us-east-1")
    S3_BUCKET_NAME: str = Field(...)
```

```python
# app/repositories/resource_repository/implementations/prepopulated/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PREPOPULATED_RESOURCES: List[str] = [
        "resource1",
        "resource2",
        "resource3"
    ]
```

## Stage 5: Architecture Verification

Before outputting, verify:

1. **Directory Structure**:

```plaintext
app/repositories/<entity>/
├── interface.py              # ABC with abstract methods
├── exceptions/               # Repository-specific exceptions
│   ├── __init__.py
│   └── base.py
└── implementations/          # Provider-specific implementations
    ├── <provider1>/
    │   ├── __init__.py       # Repository class with methods
    │   └── settings.py       # Provider-specific config
    └── <provider2>/
        ├── __init__.py       # Repository class with methods
        └── settings.py       # Provider-specific config
```

2. **Direct Methods**: Does the interface define abstract methods (NOT `execute()`)?
3. **No Command Pattern**: Do implementations have direct method implementations (NO operations)?
4. **Imports**: Are imports relative? (e.g., `from ...interface import ...`).
5. **Testing**: Can each implementation be tested by calling methods directly?

## Key Principles

- **Direct Methods**: Repositories are classes with specific data access methods
- **No Command Pattern**: No `execute()` method, no operations - just straightforward methods
- **Polymorphism**: Service layer depends on interface, any implementation can be swapped
- **Clean separation**: Each provider has its own implementation with its own logic
- **Direct calls**: Service calls repository methods directly: `await repository.get_by_id(id)`
