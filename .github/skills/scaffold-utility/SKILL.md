---
name: scaffold-utility
description: Autonomous workflow to scaffold a new Utility module. Analyzes requirements to automatically select between "Infrastructure Wrapper" (Stateful) or "Atomic Helper" (Stateless) patterns.
---

# Utility Scaffolding Workflow

Scaffold a utility module by analyzing requirements and selecting a specific implementation of the Command Pattern based on the nature of the utility.

## When to Use

- User requests a new utility (e.g., "Create a PDF Generator" or "Add a Redis Client").
- A new helper function or service wrapper is needed for repeated tasks across the codebase.
- The utility encapsulates external dependencies or complex logic that should be reusable.
- You need to standardize how the codebase interacts with third-party libraries or APIs.

## Input Requirements

The agent must extract the following from the user's prompt:

1.  **Utility Name:** (e.g., `AwsClient`, `PasswordHasher`)
2.  **Responsibility:** What does this utility do?
3.  **External Dependencies:** Does it need `boto3`, `requests`, `hashlib`, etc?

## Stage 1: Pattern Resolution

**Logic:** Do not ask the user. Analyze the requirements to determine the pattern.

- **IF** requirements mention: "Client," "Session," "Connection," "Database," "API Key," "Socket," or "External Service."
  - **DECISION:** Use **Type A (Infrastructure/Stateful)**.
  - _Reasoning:_ The utility needs to hold the state of the connection.

- **IF** requirements mention: "Parser," "Formatter," "Calculator," "Hasher," "Converter," or "Validator."
  - **DECISION:** Use **Type B (Standard/Atomic)**.
  - _Reasoning:_ The utility is a functional runner; logic is self-contained.

### Examples

#### Type A (Stateful) Example

```python
# app/utilities/aws_client/interface.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from boto3.session import Session

T = TypeVar("T")

class AwsClientABC(ABC):
    session: Session  # State is defined here

    @abstractmethod
    async def execute(self, operation: "AwsClientOperationABC[T]") -> T:
        pass

class AwsClientOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, utility: AwsClientABC) -> T:
        pass  # MUST accept utility to access session
```

#### Type B (Standard/Atomic) Example

```python
# app/utilities/password_hasher/interface.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")

class PasswordHasherABC(ABC):
    @abstractmethod
    async def execute(self, operation: "PasswordHasherOperationABC[T]") -> T:
        pass

class PasswordHasherOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self) -> T:
        pass  # MUST NOT accept arguments
```

## Stage 2: Interface Generation (`interface.py`)

Generate the ABCs based on the decision in Stage 1.

1.  **Invoker ABC:**
    - Define `async def execute(self, operation: <Name>OperationABC[T]) -> T`.
2.  **Operation ABC:**
    - **Type A (Stateful):**
      - `@abstractmethod async def execute(self, utility: <Name>ABC) -> T:`
      - _Note:_ Must accept the utility instance to access state.
    - **Type B (Atomic):**
      - `@abstractmethod async def execute(self) -> T:`
      - _Note:_ Must NOT accept arguments; operation is self-contained.

## Stage 3: Implementation Generation (`__init__.py`)

Generate the concrete Invoker class.

1.  **Type A (Stateful):**
    - `__init__`: Initialize the client/session (e.g., `self.session = boto3.client(...)`).
    - `execute`: Delegate with self: `return await operation.execute(self)`.
2.  **Type B (Atomic):**
    - `__init__`: Pass (or empty).
    - `execute`: Delegate without self: `return await operation.execute()`.

## Stage 4: Operation Scaffolding (`operations/`)

Generate a sample operation to validate the pattern.

1.  **Class Structure:** Inherit from the new `OperationABC` defined in Stage 2.
2.  **Injection Logic:**
    - **Type A:** Use the `utility` argument in `execute` to access `utility.session`.
    - **Type B:** Perform all logic using only attributes set in `__init__`.

### Examples

#### Type A (Stateful) Example

```python
# app/utilities/aws_client/operations/upload_file.py
from ..interface import AwsClientABC, AwsClientOperationABC

class UploadFile(AwsClientOperationABC[bool]):
    def __init__(self, file_path: str, bucket: str):
        self.file_path = file_path
        self.bucket = bucket

    async def execute(self, utility: AwsClientABC) -> bool:
        # Access state via the passed utility instance
        utility.session.client('s3').upload_file(self.file_path, self.bucket)
        return True
```

#### Type B (Standard/Atomic) Example

```python
# app/utilities/password_hasher/operations/hash_string.py
import hashlib
from ..interface import PasswordHasherOperationABC

class HashString(PasswordHasherOperationABC[str]):
    def __init__(self, text: str, salt: str):
        self.text = text
        self.salt = salt

    async def execute(self) -> str:
        # Self-contained logic using only init attributes
        return hashlib.sha256((self.text + self.salt).encode()).hexdigest()
```

## Stage 5: Architecture Verification

Before outputting, verify:

1.  Does the directory structure match `app/utilities/<name>/`?
2.  Are `interface.py`, `__init__.py`, and `operations/` present?
3.  Are Type Hints strictly using `Generic[T]`?
