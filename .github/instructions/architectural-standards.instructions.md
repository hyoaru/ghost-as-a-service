---
name: Architectural Standards
description: Codebase structuring, design patterns, and archictectural principles adhering to SOLID principles.
applyTo: "app/**"
---

# Architectural Standards

## Universal Command Pattern Rules

All structural components (Services, Repositories, Utilities) must adhere to the Command Pattern to decouple execution logic from the Invoker.

- **The Invoker Contract:** Every Service, Repository, and Utility class must implement a single public `async def execute` method.
- **The Operation Contract:** The `execute` method must accept a strongly-typed Operation object inheriting from a domain-specific `OperationABC`.
- **Generics:** All Operations must use `Generic[T]` to define their return type, ensuring type safety flows through the Invoker.

## 1. Service Layer Implementation

Services act as **Orchestrators**. They hold dependencies (Repositories, Loggers) and coordinate business logic.

- **Context Injection:** Service Operations **must** accept the Service instance as an argument in their `execute` method.
  - _Signature Logic:_ `operation.execute(service_instance)`
- **Dependency Access:** Operations should use the passed Service instance to access Repositories or other injected dependencies.
- **State:** Services must remain stateless regarding the request; state belongs in the Operation.

## 2. Repository Layer Implementation

Repositories act as **Data Access Gateways**. They handle specific implementation details (e.g., AWS Boto3 sessions, SQL Alchemy sessions).

- **Context Injection:** Repository Operations **must** accept the Repository instance as an argument in their `execute` method.
  - _Signature Logic:_ `operation.execute(repository_instance)`
- **Implementation Enforcement:** Concrete Operations are permitted to perform runtime checks (e.g., `isinstance`) to ensure they are running against the correct concrete Repository implementation (e.g., checking for `AwsResourceRepository` to access the `boto3` session).
- **Scope:** Operations here must be strictly limited to I/O and data transformation. No business logic.

## 3. Utility Layer Implementation

**Role:** Infrastructure Wrappers & Functional Helpers.
Utilities support two implementation patterns depending on whether they hold state.

### Type A: Infrastructure Utilities (Stateful)

Use this for clients that wrap external connections (e.g., `AwsClient`, `SmtpClient`, `RedisClient`).

- **State:** The Utility class holds the session or connection object.
- **Delegation:** The `execute` method **must** pass `self` to the operation so it can access the session.
  - _Logic:_ `return await operation.execute(self)`

### Type B: Standard Utilities (Atomic)

Use this for self-contained logic (e.g., `PasswordHasher`, `TokenGenerator`, `HtmlSanitizer`).

- **State:** The Utility class is purely a standardized runner; it holds no state.
- **Delegation:** The `execute` method **does not** pass `self`. The Operation is fully self-contained.
  - _Logic:_ `return await operation.execute()`
- **Configuration:** Any necessary data or configuration must be passed to the Operation's `__init__` constructor, not stored in the Utility class.