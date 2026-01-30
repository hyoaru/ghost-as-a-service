# Ghost-as-a-Service

> An API that generates vague, professional-sounding excuses to help you gracefully decline social obligations.

## Overview

**Ghost as a Service** takes a request or invitation as input and returns a plausible-sounding excuse filled with corporate jargon and technical mumbo-jumbo that sounds busy but is actually meaningless.

### Example Usage

**Input:** "Hey, are you free to help with the move this weekend?"

**Output:** "Hey! So sorry, I'm actually in the middle of a massive data migration and my bandwidth is currently throttled by some legacy infrastructure issues. Let's circle back in Q3?"

---

## ⚡ Vibe-Coded Architecture

> **This project is intentionally vibe-coded** — built with strong architectural opinions, opinionated patterns, and a personal philosophy about what "good code" means.

This isn't generic boilerplate. It's a manifestation of specific beliefs about software architecture, testability, and maintainability. If you're looking for flexible, loosely-structured code, this isn't it. If you want to see a real-world implementation of SOLID principles, Command Pattern, and TDD-first development with zero compromises, you're in the right place.

### The Vibe

**Core Philosophy:**

- **Command Pattern Everywhere**: Every service, repository, and utility follows a strict Command Pattern implementation. Operations are decoupled from invokers, making every piece of logic independently testable and composable.
- **Type Safety is Non-Negotiable**: Full type hints throughout. If it doesn't type-check, it doesn't ship.
- **SOLID or Nothing**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion — these aren't guidelines, they're requirements.
- **Test-Driven, Always**: Features don't exist until tests exist. 80%+ coverage isn't a goal, it's a baseline.
- **Explicit Over Implicit**: No magic. No hidden behavior. Dependencies are injected, interfaces are explicit, and every contract is documented through abstract base classes.

**What Makes This "Vibe-Coded":**

1. **Architectural Scaffolding System**: Custom "skills" that generate entire layers of the application (services, repositories, utilities) following consistent patterns. See [.github/skills/](.github/skills/) for the autonomous workflows.

2. **Three-Layer Separation of Concerns**:
   - **Services**: Orchestrators that hold dependencies and coordinate business logic
   - **Repositories**: Data access gateways with provider-specific implementations (AWS, Postgres, Mock)
   - **Utilities**: Infrastructure wrappers (stateful clients) or atomic helpers (pure functions)

3. **Universal Command Pattern Contract**:
   - Every component has an ABC (Abstract Base Class) defining its interface
   - Every concrete implementation has an `async def execute(operation)` method
   - Every operation is Generic[T] with explicit return types
   - Operations receive their invoker as context (enabling DI and testing)

4. **Two-Track Pattern Selection**:
   - **Stateful Utilities** (Infrastructure Wrappers): Pass `self` to operations (e.g., AWS clients, Redis clients)
   - **Stateless Utilities** (Atomic Helpers): Operations are self-contained (e.g., password hashers, formatters)

5. **Opinionated Testing Standards**:
   - AAA pattern (Arrange, Act, Assert) religiously
   - Fixtures organized by scope (function, module, session)
   - All external dependencies mocked with `AsyncMock`
   - Tests mirror source structure exactly

### How the Vibe System Works

The vibe isn't just philosophy — it's codified into scaffolding workflows:

**Skill-Based Generation**: Instead of manually creating boilerplate, use autonomous "skills" that generate entire modules following the architectural patterns:

```bash
# Example: Generate a new service with full Command Pattern structure
# See: .github/skills/scaffold-service/SKILL.md
#
# Input: "Create a Notification Service with SendEmail operation"
# Output:
#   - app/services/notification_service/interface.py (ABCs)
#   - app/services/notification_service/__init__.py (Concrete service)
#   - app/services/notification_service/operations/send_email.py
#   - tests/services/notification_service/test_notification_service.py
```

**Three Scaffolding Skills Available**:

1. **[scaffold-service](.github/skills/scaffold-service/SKILL.md)**: Generates service layer (orchestration + business logic)
2. **[scaffold-repository](.github/skills/scaffold-repository/SKILL.md)**: Generates repository layer (data access + provider implementations)
3. **[scaffold-utility](.github/skills/scaffold-utility/SKILL.md)**: Auto-selects between stateful wrapper or stateless helper pattern

**Pattern Enforcement Through Instructions**:

- [Core Standards](.github/instructions/core-standards.instructions.md): Python style, naming conventions, code organization
- [Architectural Standards](.github/instructions/architectural-standards.instructions.md): Command Pattern rules, SOLID principles, layer contracts
- [Testing Standards](.github/instructions/testing-standards.instructions.md): Fixture organization, mocking patterns, test structure

**Living Documentation**: The architecture documents itself through:

- Abstract base classes define contracts
- Type hints specify data flow
- Operations encapsulate single responsibilities
- Tests demonstrate usage patterns

---

## Technology Stack

- **Python 3.12+**: Primary programming language
- **Pydantic**: Data validation and settings management
- **PydanticAI**: AI integration framework wrapping Google Gemini
- **AWS Lambda**: Serverless compute platform
- **AWS Lambda Powertools**: Structured logging, tracing, and metrics
- **Google Gemini**: AI model for creative text generation
- **pytest**: Testing framework with async support
- **pytest-mock**: Mocking utilities for dependency injection testing
- **Docker**: Containerization for local development
- **Docker Compose**: Multi-container orchestration with hot-reload
- **uv**: Fast Python package manager and environment resolver

## Project Structure

```
ghost-as-a-service/
├── .github/
│   ├── instructions/                    # Architectural rules and standards
│   │   ├── architectural-standards.instructions.md
│   │   ├── core-standards.instructions.md
│   │   ├── testing-standards.instructions.md
│   │   └── skill.instructions.md
│   └── skills/                          # Autonomous scaffolding workflows
│       ├── scaffold-service/
│       ├── scaffold-repository/
│       └── scaffold-utility/
├── app/
│   ├── __init__.py                      # Lambda handler entry point
│   ├── models.py                        # Pydantic models (EventModel, ExcuseResponse)
│   ├── services/                        # Business logic orchestrators
│   │   └── excuse_generator/
│   │       ├── interface.py            # ABCs: ExcuseGeneratorABC, OperationABC
│   │       ├── __init__.py             # Concrete ExcuseGenerator service
│   │       ├── exceptions/             # Domain-specific exceptions
│   │       └── operations/             # Business logic operations
│   │           └── generate_excuse.py
│   ├── repositories/                    # Data access gateways
│   │   └── excuse_repository/
│   │       ├── interface.py            # ABCs: RepositoryABC, OperationABC
│   │       ├── exceptions/             # Repository-specific exceptions
│   │       └── implementations/        # Provider-specific implementations
│   │           ├── agent/              # AI-powered excuse generation
│   │           │   ├── __init__.py
│   │           │   ├── settings.py
│   │           │   └── operations/
│   │           │       └── get_excuse.py
│   │           └── prepopulated/       # Static excuse bank
│   │               ├── __init__.py
│   │               ├── settings.py
│   │               └── operations/
│   │                   └── get_excuse.py
│   └── utilities/                       # Infrastructure wrappers & helpers
│       └── excuse_agent/
│           ├── interface.py            # ABCs: AgentABC, OperationABC
│           ├── __init__.py             # Concrete PydanticAI wrapper
│           ├── settings.py             # Agent configuration
│           ├── instructions.md         # AI agent system prompt
│           └── operations/
│               ├── interface.py        # Operation contracts
│               └── generate_vague.py   # AI generation logic
├── tests/
│   ├── conftest.py                      # Project-wide fixtures
│   ├── test_lambda_handler.py
│   ├── test_models.py
│   ├── services/                        # Mirror app/services structure
│   │   └── excuse_generator/
│   │       ├── conftest.py
│   │       ├── test_excuse_generator_service.py
│   │       └── operations/
│   ├── repositories/                    # Mirror app/repositories structure
│   │   └── excuse_repository/
│   │       ├── conftest.py
│   │       ├── test_interface.py
│   │       ├── test_agent_repository.py
│   │       └── test_prepopulated_repository.py
│   └── utilities/                       # Mirror app/utilities structure
│       └── excuse_agent/
│           ├── conftest.py
│           ├── test_excuse_agent.py
│           └── operations/
├── .env.example                         # Environment variables template
├── Dockerfile                           # Container image for AWS Lambda
├── docker-compose.yml                   # Local development orchestration
├── pyproject.toml                       # Dependencies and project metadata
├── uv.lock                              # Lockfile for reproducible builds
└── README.md                            # This file
```

## Architecture

### Design Principles

- **Command Pattern**: Services, repositories, and utilities all implement the Command Pattern with strict contracts
- **Dependency Injection**: Constructor-based injection with optional defaults for convenience
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Type Safety**: Full type hints with Generic[T] for operation return types
- **Test-Driven Development**: All features developed with TDD approach
- **Self-Documenting Code**: Clear naming, type hints, and logical structure over comments

### Architectural Layers

#### 1. Service Layer (Orchestrators)

**Purpose**: Coordinate business logic and manage dependencies.

**Pattern**: Services hold dependencies (repositories, utilities) and delegate to operations.

```python
# app/services/excuse_generator/interface.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from ...repositories.excuse_repository.interface import ExcuseRepositoryABC

T = TypeVar("T")

class ExcuseGeneratorABC(ABC):
    excuse_repository: ExcuseRepositoryABC

    @abstractmethod
    async def execute(self, operation: "ExcuseGeneratorOperationABC[T]") -> T:
        """Universal invoker contract."""
        pass

class ExcuseGeneratorOperationABC(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, service: ExcuseGeneratorABC) -> T:
        """Operations receive service context for dependency access."""
        pass
```

**Key Rules**:

- Operations receive the service instance as context
- Service provides access to repositories and utilities
- No business logic in the service class itself — it's all in operations
- Services remain stateless; state belongs to operations

#### 2. Repository Layer (Data Access Gateways)

**Purpose**: Abstract data access with provider-specific implementations.

**Pattern**: Repository interface defines contracts, implementations provide provider-specific logic (AWS, Postgres, Mock).

```python
# app/repositories/excuse_repository/implementations/agent/__init__.py
from ....interface import ExcuseRepositoryABC, ExcuseRepositoryOperationABC
from ....utilities.excuse_agent import ExcuseAgent

class AgentExcuseRepository(ExcuseRepositoryABC):
    """AI-powered excuse generation via PydanticAI."""

    def __init__(self, agent: ExcuseAgent):
        self.agent = agent  # Infrastructure dependency

    async def execute(self, operation: ExcuseRepositoryOperationABC[T]) -> T:
        return await operation.execute(self)
```

**Key Rules**:

- Operations perform runtime `isinstance` checks to access provider-specific state
- Strictly I/O and data transformation — no business logic
- Return domain models, not raw API responses
- Multiple implementations can coexist (agent, prepopulated, etc.)

#### 3. Utility Layer (Infrastructure & Helpers)

**Purpose**: Reusable infrastructure wrappers and atomic helpers.

**Two Patterns**:

**Type A: Infrastructure Utilities (Stateful)**

- Hold connection state (sessions, clients)
- Operations receive `self` to access state
- Examples: `AwsClient`, `RedisClient`, `ExcuseAgent`

```python
# Type A: Stateful - passes self to operation
class ExcuseAgent(ExcuseAgentABC):
    def __init__(self):
        self.agent = Agent(model="gemini-1.5-flash")

    async def execute(self, operation: ExcuseAgentOperationABC[T]) -> T:
        return await operation.execute(self)  # Operation accesses self.agent
```

**Type B: Atomic Utilities (Stateless)**

- Pure functions, no state
- Operations are self-contained, receive no context
- Examples: `PasswordHasher`, `TokenGenerator`, `HtmlSanitizer`

```python
# Type B: Stateless - operation is self-contained
class PasswordHasher(PasswordHasherABC):
    async def execute(self, operation: PasswordHasherOperationABC[T]) -> T:
        return await operation.execute()  # No self passed
```

### Dependency Flow

```
Lambda Handler
    ↓
Service Layer (ExcuseGenerator)
    ↓
Repository Layer (ExcuseRepository)
    ↓ [AgentExcuseRepository]
Utility Layer (ExcuseAgent → PydanticAI)
```

**Each layer**:

1. Defines an ABC interface (`interface.py`)
2. Implements concrete classes (`__init__.py`)
3. Delegates to operations (`operations/`)
4. Has corresponding tests (`tests/`)
5. Defines custom exceptions (`exceptions/`)

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose (for local development)
- Google API key for Gemini (AI model)
- `uv` package manager (recommended)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd ghost-as-a-service
   ```

2. **Install dependencies using uv:**

   ```bash
   uv sync
   ```

3. **Configure environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Run tests:**
   ```bash
   uv run pytest
   ```

## Configuration

All configuration is managed through Pydantic Settings with environment variables. No hardcoded secrets, ever.

Create a `.env` file based on `.env.example`:

```env
# AWS Lambda Powertools Configuration
POWERTOOLS_SERVICE_NAME=excuse-generator
POWERTOOLS_LOG_LEVEL=INFO
POWERTOOLS_LOGGER_LOG_EVENT=true

# AI Configuration (PydanticAI + Google Gemini)
GEMINI_API_KEY=your-google-api-key-here
```

#### Configuration Options

| Variable                      | Required | Description                                       | Default |
| ----------------------------- | -------- | ------------------------------------------------- | ------- |
| `POWERTOOLS_SERVICE_NAME`     | Yes      | Name of the Lambda service for Powertools logging | N/A     |
| `POWERTOOLS_LOG_LEVEL`        | Yes      | Logging level (DEBUG, INFO, WARNING, ERROR)       | INFO    |
| `POWERTOOLS_LOGGER_LOG_EVENT` | Yes      | Whether to log the incoming event                 | true    |
| `GEMINI_API_KEY`              | Yes      | API key for Google AI (Gemini) via PydanticAI     | N/A     |

**Settings Pattern**: Each module (service, repository, utility) can define its own `settings.py` using Pydantic Settings with environment variable loading:

```python
# app/utilities/excuse_agent/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class ExcuseAgentSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    GEMINI_API_KEY: str = Field(..., description="Google Gemini API key")
    MODEL_NAME: str = Field(default="gemini-1.5-flash")
```

## Development

### Running Locally with Docker

The Lambda function can be run locally using Docker Compose with hot-reload support:

```bash
# Start the Lambda function locally with hot-reload
docker compose up --watch

# The Lambda will be available at http://localhost:9000
```

Once running, you can invoke the Lambda using curl:

```bash
# Test the excuse generator
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -H "Content-Type: application/json" \
  -d '{"request": "Can you help me move this weekend?"}'
```

**Example Response:**

```json
{
  "excuse": "Hey! So sorry, I'm actually in the middle of a massive data migration and my bandwidth is currently throttled by some legacy infrastructure issues. Let's circle back in Q3?"
}
```

The `--watch` flag enables hot-reload, automatically syncing changes from the `./app` directory and restarting the container when Python files are modified.

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=app --cov-report=term-missing

# Run specific test file
uv run pytest tests/services/excuse_generator/test_excuse_generator_service.py

# Run specific test pattern
uv run pytest -k "test_generate"

# Run with verbose output
uv run pytest -v

# Run tests for a specific layer
uv run pytest tests/services/        # Service layer
uv run pytest tests/repositories/    # Repository layer
uv run pytest tests/utilities/       # Utility layer
```

**Expected Output**: All tests should pass with 80%+ coverage. If they don't, something's broken (or you haven't finished implementing yet).

### Code Quality

This project uses `ruff` for linting and formatting:

```bash
# Check for linting issues
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Testing Standards

The testing approach is as opinionated as the architecture:

**TDD-First**: Tests define behavior before implementation exists. Coverage below 80% means incomplete features.

**Fixture Organization**: Fixtures are scoped and placed at the appropriate level (project-wide, service-specific, operation-specific). See [tests/conftest.py](tests/conftest.py) hierarchy.

**Mocking Strategy**:

- All external dependencies mocked with `AsyncMock`
- Repository implementations tested independently
- Service tests use mocked repositories
- End-to-end tests verify full integration

**Test Structure (AAA Pattern)**:

```python
async def test_generate_excuse_success(excuse_generator, mock_excuse_repository):
    # Arrange: Set up test data and mock behavior
    expected_excuse = "I'm swamped with a critical project."
    mock_excuse_repository.execute.return_value = expected_excuse
    operation = GenerateExcuse(request="Help me move?")

    # Act: Execute the operation
    result = await excuse_generator.execute(operation)

    # Assert: Verify the outcome
    assert result == expected_excuse
    mock_excuse_repository.execute.assert_called_once()
```

**Test Mirroring**: The `tests/` directory exactly mirrors `app/` structure. Finding tests is never a guessing game.

See [.github/instructions/testing-standards.instructions.md](.github/instructions/testing-standards.instructions.md) for comprehensive guidelines.

## API Usage

### Lambda Event Format

The Lambda handler expects a JSON event with a `request` field:

**Input:**

```json
{
  "request": "Can you help me move this weekend?"
}
```

**Output:**

```json
{
  "excuse": "Hey! So sorry, I'm actually in the middle of a massive data migration and my bandwidth is currently throttled by some legacy infrastructure issues. Let's circle back in Q3?"
}
```

### Error Handling

The service uses domain-specific exceptions at each layer:

**Service Layer** (`app/services/excuse_generator/exceptions/`):

- `InvalidRequestError`: Input validation failures
- `ServiceGenerationError`: Service orchestration failures

**Repository Layer** (`app/repositories/excuse_repository/exceptions/`):

- `InvalidExcuseRequestError`: Repository-level validation failures
- `ExcuseGenerationError`: Data access failures

**All exceptions** inherit from layer-specific base exceptions, which inherit from a common `AppException`. This provides:

- Clear error boundaries between layers
- Structured error handling
- Consistent error messages
- Proper HTTP status code mapping

```python
# Example error flow
try:
    result = await excuse_generator.execute(operation)
except InvalidRequestError as e:
    # 400 Bad Request
    logger.error(f"Invalid request: {e}")
except ServiceGenerationError as e:
    # 500 Internal Server Error
    logger.error(f"Service error: {e}")
```

## Deployment

### AWS Lambda Deployment

1. **Build the deployment package:**

   ```bash
   uv export --no-hashes -o requirements.txt
   pip install -r requirements.txt -t package/
   cd package && zip -r ../lambda.zip . && cd ..
   zip -g lambda.zip app/*.py
   ```

2. **Deploy to AWS Lambda:**
   - Upload `lambda.zip` to AWS Lambda
   - Set environment variables from `.env`
   - Configure handler as `app.handler`
   - Set runtime to Python 3.12

3. **Configure Lambda:**
   - Memory: 512 MB (recommended)
   - Timeout: 30 seconds
   - Environment variables: Set from `.env`

## Contributing

This project follows strict architectural patterns. Before contributing:

1. **Read the Standards**:
   - [Core Standards](.github/instructions/core-standards.instructions.md) - Coding style and organization
   - [Architectural Standards](.github/instructions/architectural-standards.instructions.md) - SOLID principles and Command Pattern
   - [Testing Standards](.github/instructions/testing-standards.instructions.md) - TDD approach and test structure

2. **Use the Scaffolding Skills**:
   - Don't manually create boilerplate
   - Use [scaffold-service](.github/skills/scaffold-service/SKILL.md) for new services
   - Use [scaffold-repository](.github/skills/scaffold-repository/SKILL.md) for new repositories
   - Use [scaffold-utility](.github/skills/scaffold-utility/SKILL.md) for new utilities

3. **Follow TDD**:
   - Write tests first
   - Implement to make tests pass
   - Refactor while keeping tests green
   - Ensure 80%+ coverage

4. **Maintain Type Safety**:
   - All functions must have type hints
   - Use Generic[T] for operation return types
   - No `Any` types unless absolutely necessary

5. **Before Submitting PR**:

   ```bash
   # Run all tests
   uv run pytest

   # Check code quality
   uv run ruff check .
   uv run ruff format .

   # Ensure coverage
   uv run pytest --cov=app --cov-report=term-missing
   ```

**Philosophy Check**: If your contribution doesn't follow the Command Pattern, uses inheritance instead of composition, or lacks comprehensive tests, it won't be merged. This isn't flexibility — it's intentional rigidity to maintain architectural consistency.

---

## Why This Architecture Matters

### The Problem This Solves

Most codebases suffer from:

- **Tightly coupled dependencies**: Services directly instantiate their dependencies, making testing painful
- **Mixed concerns**: Business logic, data access, and infrastructure code intermingled
- **Fragile tests**: Mocking requires monkey-patching or complex setup
- **Inconsistent patterns**: Every developer has their own style
- **Hidden dependencies**: Magic imports and global state

### The Solution

**Command Pattern + Dependency Injection** creates:

- **Perfect testability**: Every operation can be tested in isolation with mocked dependencies
- **Clear boundaries**: Each layer has explicit contracts (ABCs) defining its interface
- **Composability**: Operations are small, single-purpose, and combinable
- **Type safety**: Generic[T] ensures return types flow through the entire stack
- **Predictability**: Every module follows the same structure

### Real-World Benefits

**Adding a New Feature**:

```bash
# Traditional approach: 30+ minutes of boilerplate, inconsistent patterns
# Vibe-coded approach: 5 minutes using scaffold-service skill
```

**Writing Tests**:

```python
# Traditional approach: Mock every import, patch global state
# Vibe-coded approach: Inject mocked dependencies in constructor

@pytest.fixture
def service(mock_repository):
    return ExcuseGenerator(excuse_repository=mock_repository)

# That's it. Service is ready to test.
```

**Refactoring**:

- Change repository implementation? No service changes needed (interface unchanged)
- Add new operation? No changes to service class (just add operation file)
- Switch AI providers? No business logic changes (utility layer abstraction)

**Onboarding New Developers**:

- Read one instruction file
- See the pattern once
- Apply it everywhere
- No guessing, no inconsistency

### The Trade-offs

**What You Gain**:

- Testability, maintainability, predictability, scalability
- Clear mental model of system structure
- Confidence when refactoring
- Fast feature development once patterns are learned

**What You Give Up**:

- Flexibility to "just hack something together"
- Ability to cut corners on tests
- Freedom to organize code however you feel
- Shortcut of throwing everything in one file

**The Vibe**: If you value long-term code quality over short-term speed, structured thinking over ad-hoc solutions, and explicit contracts over implicit assumptions, this architecture will feel like home. If you prefer "move fast and break things" over "move steadily and maintain quality," this might feel constraining.

---

## Implementation Deep-Dive

### How a Request Flows Through the System

Let's trace a request through all layers to see the vibe architecture in action:

**1. Lambda Entry Point** ([app/**init**.py](app/__init__.py))

```python
@logger.inject_lambda_context
@event_parser(model=EventModel)
def handler(event: EventModel, context: LambdaContext) -> dict:
    # Parse and validate input
    excuse_service = ExcuseGenerator()  # DI with defaults
    operation = GenerateExcuse(request=event.request)

    # Execute through service layer
    excuse = await excuse_service.execute(operation)
    return ExcuseResponse(excuse=excuse, metadata={...})
```

**2. Service Layer** ([app/services/excuse_generator/](app/services/excuse_generator/))

```python
# interface.py - Define contracts
class ExcuseGeneratorABC(ABC):
    excuse_repository: ExcuseRepositoryABC

    @abstractmethod
    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        pass

# __init__.py - Implement orchestrator
class ExcuseGenerator(ExcuseGeneratorABC):
    def __init__(self, excuse_repository: Optional[ExcuseRepositoryABC] = None):
        self.excuse_repository = excuse_repository or AgentExcuseRepository()

    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        return await operation.execute(self)

# operations/generate_excuse.py - Implement business logic
class GenerateExcuse(ExcuseGeneratorOperationABC[str]):
    def __init__(self, request: str):
        self.request = request

    async def execute(self, service: ExcuseGeneratorABC) -> str:
        # Access injected repository through service
        repo_operation = GetExcuse(request=self.request)
        excuse = await service.excuse_repository.execute(repo_operation)
        return excuse
```

**3. Repository Layer** ([app/repositories/excuse_repository/](app/repositories/excuse_repository/))

```python
# implementations/agent/__init__.py
class AgentExcuseRepository(ExcuseRepositoryABC):
    def __init__(self):
        self.agent = ExcuseAgent()  # Infrastructure dependency

    async def execute(self, operation: ExcuseRepositoryOperationABC[T]) -> T:
        return await operation.execute(self)

# implementations/agent/operations/get_excuse.py
class GetExcuse(ExcuseRepositoryOperationABC[str]):
    def __init__(self, request: str):
        self.request = request

    async def execute(self, repository: ExcuseRepositoryABC) -> str:
        # Runtime type check (pattern for provider-specific access)
        if not isinstance(repository, AgentExcuseRepository):
            raise TypeError("GetExcuse requires AgentExcuseRepository")

        # Access repository's agent
        agent_operation = GenerateVague(prompt=self.request)
        excuse = await repository.agent.execute(agent_operation)
        return excuse
```

**4. Utility Layer** ([app/utilities/excuse_agent/](app/utilities/excuse_agent/))

```python
# __init__.py - Infrastructure wrapper (stateful)
class ExcuseAgent(ExcuseAgentABC):
    def __init__(self):
        settings = ExcuseAgentSettings()
        self.agent = Agent(
            model=settings.MODEL_NAME,
            system_prompt=Path("instructions.md").read_text()
        )

    async def execute(self, operation: ExcuseAgentOperationABC[T]) -> T:
        return await operation.execute(self)  # Passes self for agent access

# operations/generate_vague.py
class GenerateVague(ExcuseAgentOperationABC[str]):
    def __init__(self, prompt: str):
        self.prompt = prompt

    async def execute(self, utility: ExcuseAgentABC) -> str:
        # Access stateful agent connection
        result = await utility.agent.run(self.prompt)
        return result.data
```

**Flow Summary**:

```
Handler → Service (orchestrates) → Repository (data access) → Utility (infrastructure) → PydanticAI → Gemini API
   ↓            ↓                      ↓                           ↓
 Models     Operations            Operations                  Operations
```

### Testing the Flow

Because of dependency injection, testing at any layer is trivial:

```python
# Test service in isolation (mock repository)
@pytest.fixture
def mock_repository():
    return AsyncMock(ExcuseRepositoryABC)

async def test_service(mock_repository):
    service = ExcuseGenerator(excuse_repository=mock_repository)
    mock_repository.execute.return_value = "test excuse"

    result = await service.execute(GenerateExcuse("help me move"))
    assert result == "test excuse"

# Test repository in isolation (mock utility)
@pytest.fixture
def mock_agent():
    return AsyncMock(ExcuseAgentABC)

async def test_repository(mock_agent):
    repo = AgentExcuseRepository()
    repo.agent = mock_agent  # Inject mock
    mock_agent.execute.return_value = "test excuse"

    result = await repo.execute(GetExcuse("help me move"))
    assert result == "test excuse"

# Test utility in isolation (mock PydanticAI agent)
async def test_utility():
    agent = ExcuseAgent()
    agent.agent = AsyncMock()  # Mock PydanticAI
    agent.agent.run.return_value = MockResult(data="test excuse")

    result = await agent.execute(GenerateVague("help me move"))
    assert result == "test excuse"
```

**Every layer is independently testable. Every dependency is mockable. Zero coupling.**

## Acknowledgments

This project represents a personal philosophy about software architecture. The patterns here are intentionally opinionated, prioritizing:

- Long-term maintainability over short-term convenience
- Explicit contracts over implicit understanding
- Testability over simplicity
- Consistency over flexibility

The "vibe" is that good code is **predictable code**. When every module follows the same pattern, onboarding is easier, bugs are rarer, and refactoring is safer.

If you find this approach useful, feel free to adapt it to your own projects. If you think it's overkill, that's okay too — architecture is about making trade-offs that align with your values.

**Built with**:

- Strong opinions, loosely held
- Test-driven paranoia
- Architectural zealotry
- A belief that code should be boring (in a good way)
- **Author Notes**: I did not write any of these docs forgive me

**Inspired by**:

- [AgentSkills.io](https://agentskills.io/) - Skill-based AI agent workflows
- [Anthropic Skills](https://github.com/anthropics/skills) - Agent skill patterns and best practices
- [Awesome Copilot](https://github.com/github/awesome-copilot) - GitHub Copilot resources and patterns
- [Copilot Orchestra](https://github.com/ShepAlderson/copilot-orchestra) - Multi-agent orchestration patterns

**Last Updated**: January 2026
