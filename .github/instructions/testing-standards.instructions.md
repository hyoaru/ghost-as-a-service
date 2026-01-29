---
name: Testing Standards
description: This file describes the testing standards for the project.
applyTo: "tests/**/*.py"
---

# Testing Standards

## General Principles

- Use pytest fixtures for test setup
- Mock external dependencies using pytest-mock
- Follow AAA pattern: Arrange, Act, Assert
- Write descriptive test names that explain what is being tested
- Test both happy paths and error cases
- Aim for high test coverage (80%+ recommended)

## Fixture Organization and Scope

### Fixture Scopes

- **function**: Default scope, creates new fixture for each test (use for most fixtures)
- **class**: Creates fixture once per test class
- **module**: Creates fixture once per module
- **session**: Creates fixture once for entire test session

```python
# tests/services/excuse_generator/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture  # function scope by default
def mock_excuse_repository():
    """Mock repository for each test."""
    return AsyncMock(ExcuseRepositoryABC)

@pytest.fixture(scope="module")
def test_config():
    """Shared configuration for all tests in module."""
    return {"max_retries": 3, "timeout": 30}

@pytest.fixture
def excuse_generator(mock_excuse_repository):
    """Fixture that depends on another fixture."""
    return ExcuseGenerator(excuse_repository=mock_excuse_repository)
```

### Organizing Fixtures in conftest.py

Place fixtures at the appropriate directory level:

```
tests/
├── conftest.py                    # Project-wide fixtures
└── services/
    ├── conftest.py               # Service-level fixtures
    └── excuse_generator/
        ├── conftest.py           # Service-specific fixtures
        └── operations/
            └── test_generate_vague.py
```

```python
# tests/conftest.py (project-wide)
@pytest.fixture
def sample_request():
    """Common test request used across multiple test suites."""
    return "Can you help me move this weekend?"

# tests/services/excuse_generator/conftest.py (service-specific)
@pytest.fixture
def mock_excuse_repository():
    return AsyncMock(ExcuseRepositoryABC)

@pytest.fixture
def excuse_generator(mock_excuse_repository):
    return ExcuseGenerator(excuse_repository=mock_excuse_repository)
```

### Parametrized Fixtures

Use parametrized fixtures to test multiple scenarios:

```python
@pytest.fixture(params=[
    "Can you help me move?",
    "Want to grab coffee tomorrow?",
    "Are you free this weekend?",
])
def sample_requests(request):
    """Provides multiple request variations for testing."""
    return request.param

async def test_generate_excuse_various_requests(excuse_generator, sample_requests):
    operation = GenerateVague(sample_requests)
    result = await excuse_generator.execute(operation)
    assert isinstance(result, str)
    assert len(result) > 0
```

## Mock Patterns and Best Practices

### Using AsyncMock for Async Dependencies

```python
from unittest.mock import AsyncMock

@pytest.fixture
def mock_excuse_repository():
    """Mock async repository."""
    mock = AsyncMock(ExcuseRepositoryABC)
    # Configure default behavior
    mock.execute.return_value = "default excuse"
    return mock
```

### Configuring Mock Return Values and Side Effects

```python
async def test_generate_vague_success(excuse_generator, mock_excuse_repository):
    # Arrange
    expected_excuse = "I'd love to help, but I'm swamped with a critical project."
    mock_excuse_repository.execute.return_value = expected_excuse
    operation = GenerateVague("Can you help me move?")

    # Act
    result = await excuse_generator.execute(operation)

    # Assert
    assert result == expected_excuse

async def test_repository_failure(excuse_generator, mock_excuse_repository):
    # Arrange - mock raises exception
    mock_excuse_repository.execute.side_effect = ExcuseGenerationError("API failed")
    operation = GenerateVague("Can you help?")

    # Act & Assert
    with pytest.raises(ExcuseGenerationError):
        await excuse_generator.execute(operation)
```

### Asserting on Mock Calls

```python
async def test_repository_called_correctly(excuse_generator, mock_excuse_repository):
    # Arrange
    request = "Can you help me move?"
    mock_excuse_repository.execute.return_value = "excuse"
    operation = GenerateVague(request)

    # Act
    await excuse_generator.execute(operation)

    # Assert - verify mock was called
    mock_excuse_repository.execute.assert_awaited_once()

    # Assert - verify mock was called with specific arguments
    call_args = mock_excuse_repository.execute.call_args
    assert isinstance(call_args[0][0], GetVague)

    # Assert - check call count
    assert mock_excuse_repository.execute.await_count == 1
```

### When to Use pytest-mock vs unittest.mock

```python
# Use unittest.mock for creating mock objects
from unittest.mock import AsyncMock, Mock

@pytest.fixture
def mock_repository():
    return AsyncMock(ExcuseRepositoryABC)

# Use pytest-mock (mocker fixture) for patching
def test_with_patching(mocker):
    # Patch a module-level function or class
    mock_logger = mocker.patch('app.services.excuse_generator.logger')

    # Verify logger was called
    mock_logger.info.assert_called_once()
```

## Test Organization

### Grouping Tests in Classes

```python
# tests/services/excuse_generator/operations/test_generate_vague.py
class TestGenerateVague:
    """Test suite for GenerateVague operation."""

    async def test_success_with_simple_request(
        self, excuse_generator, mock_excuse_repository
    ):
        # Arrange
        request = "Can you help me move?"
        expected = "Sorry, I'm in the middle of a massive data migration."
        mock_excuse_repository.execute.return_value = expected
        operation = GenerateVague(request)

        # Act
        result = await excuse_generator.execute(operation)

        # Assert
        assert result == expected

    async def test_success_with_complex_request(
        self, excuse_generator, mock_excuse_repository
    ):
        # Arrange
        request = "Can you help me move this weekend and also babysit?"
        expected = "My bandwidth is currently throttled by legacy infrastructure."
        mock_excuse_repository.execute.return_value = expected
        operation = GenerateVague(request)

        # Act
        result = await excuse_generator.execute(operation)

        # Assert
        assert result == expected

    async def test_failure_when_repository_raises_error(
        self, excuse_generator, mock_excuse_repository
    ):
        # Arrange
        mock_excuse_repository.execute.side_effect = ExcuseGenerationError("Failed")
        operation = GenerateVague("Can you help?")

        # Act & Assert
        with pytest.raises(ExcuseGenerationError):
            await excuse_generator.execute(operation)
```

### Naming Conventions

```python
# Test file naming: test_{module_name}.py
# tests/services/excuse_generator/operations/test_generate_vague.py

# Test class naming: Test{ClassName}
class TestGenerateVague:
    pass

# Test method naming: test_{what_is_being_tested}_{expected_outcome}
async def test_generate_vague_returns_excuse_when_valid_request(self):
    pass

async def test_generate_vague_raises_error_when_invalid_request(self):
    pass

async def test_repository_execute_called_once_when_operation_succeeds(self):
    pass
```

## Async Testing

### Using pytest-asyncio

```python
# Mark async tests - done automatically by pytest-asyncio
async def test_async_operation(excuse_generator):
    # Arrange
    operation = GenerateVague("Can you help?")

    # Act
    result = await excuse_generator.execute(operation)

    # Assert
    assert isinstance(result, str)

# Test multiple async operations
async def test_multiple_operations(excuse_generator, mock_excuse_repository):
    # Arrange
    mock_excuse_repository.execute.return_value = "excuse"
    operation1 = GenerateVague("Request 1")
    operation2 = GenerateVague("Request 2")

    # Act
    result1 = await excuse_generator.execute(operation1)
    result2 = await excuse_generator.execute(operation2)

    # Assert
    assert result1 == "excuse"
    assert result2 == "excuse"
    assert mock_excuse_repository.execute.await_count == 2
```

## Test Data Management

### Creating Test Fixtures for Sample Data

```python
# tests/services/excuse_generator/conftest.py
@pytest.fixture
def sample_request():
    return "Can you help me move this weekend?"

@pytest.fixture
def sample_excuse():
    return "I'd love to help, but I'm swamped with a critical project deadline."

@pytest.fixture
def complex_request():
    return {
        "message": "Can you help me move?",
        "urgency": "high",
        "sender": "friend"
    }
```

### Using Factories for Complex Test Objects

```python
# tests/utilities/factories.py
class ExcuseFactory:
    @staticmethod
    def create_vague_excuse(request: str = "default request") -> str:
        return f"Sorry, I'm busy with {request}"

    @staticmethod
    def create_technical_excuse(request: str = "default request") -> str:
        return f"My bandwidth is throttled due to {request}"

# tests/services/excuse_generator/operations/test_generate_vague.py
from tests.utilities.factories import ExcuseFactory

async def test_with_factory(excuse_generator, mock_excuse_repository):
    # Arrange
    expected = ExcuseFactory.create_vague_excuse("data migration")
    mock_excuse_repository.execute.return_value = expected
    operation = GenerateVague("Can you help?")

    # Act
    result = await excuse_generator.execute(operation)

    # Assert
    assert result == expected
```

### Avoiding Hardcoded Test Data

```python
# Bad - hardcoded values scattered throughout tests
async def test_bad_example(excuse_generator):
    operation = GenerateVague("Can you help me move this weekend?")
    result = await excuse_generator.execute(operation)
    assert "data migration" in result

# Good - use fixtures and factories
@pytest.fixture
def sample_request():
    return "Can you help me move this weekend?"

async def test_good_example(excuse_generator, mock_excuse_repository, sample_request):
    # Arrange
    expected = ExcuseFactory.create_vague_excuse()
    mock_excuse_repository.execute.return_value = expected
    operation = GenerateVague(sample_request)

    # Act
    result = await excuse_generator.execute(operation)

    # Assert
    assert result == expected
```

## Assertion Best Practices

### Using Specific Assertions

```python
async def test_with_specific_assertions(excuse_generator, mock_excuse_repository):
    # Arrange
    mock_excuse_repository.execute.return_value = "excuse"
    operation = GenerateVague("Can you help?")

    # Act
    result = await excuse_generator.execute(operation)

    # Assert - use specific assertions
    assert isinstance(result, str)
    assert len(result) > 0
    assert result == "excuse"
    assert "excuse" in result

    # Not just generic assertions
    # Bad: assert result  # Too generic
    # Good: assert isinstance(result, str)
```

### Testing Exception Handling

```python
async def test_raises_specific_exception(excuse_generator, mock_excuse_repository):
    # Arrange
    mock_excuse_repository.execute.side_effect = ExcuseGenerationError(
        "API rate limit exceeded"
    )
    operation = GenerateVague("Can you help?")

    # Act & Assert
    with pytest.raises(ExcuseGenerationError) as exc_info:
        await excuse_generator.execute(operation)

    # Assert on exception details
    assert "rate limit" in str(exc_info.value)

async def test_handles_invalid_request(excuse_generator):
    # Arrange
    operation = GenerateVague("")  # Empty request

    # Act & Assert
    with pytest.raises(InvalidRequestError) as exc_info:
        await excuse_generator.execute(operation)

    assert "Request cannot be empty" in str(exc_info.value)
```

### Asserting on Multiple Conditions

```python
async def test_multiple_assertions(excuse_generator, mock_excuse_repository):
    # Arrange
    expected_excuse = "I'm swamped with a critical project deadline."
    mock_excuse_repository.execute.return_value = expected_excuse
    operation = GenerateVague("Can you help me move?")

    # Act
    result = await excuse_generator.execute(operation)

    # Assert - multiple related assertions grouped logically
    assert isinstance(result, str), "Result should be a string"
    assert len(result) > 10, "Excuse should be meaningful length"
    assert result == expected_excuse, "Result should match expected excuse"

    # Assert on mock calls
    mock_excuse_repository.execute.assert_awaited_once()
    call_args = mock_excuse_repository.execute.call_args[0][0]
    assert isinstance(call_args, GetVague)
```

## Test Coverage Guidelines

### Running Coverage Reports

```bash
# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

### Coverage Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=app",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80"
]
```

### Identifying Untested Code

```python
# When coverage shows untested paths, add tests:

class GenerateVague(ExcuseGeneratorOperationABC[str]):
    async def execute(self, service: ExcuseGeneratorABC) -> str:
        if not self.request:  # This branch needs testing
            raise InvalidRequestError("Request cannot be empty")

        try:
            result = await service.excuse_repository.execute(GetVague(self.request))
            return result
        except Exception as e:  # This exception path needs testing
            raise ExcuseGenerationError(f"Failed to generate excuse: {e}")

# Add tests for uncovered branches
async def test_empty_request_raises_error(excuse_generator):
    with pytest.raises(InvalidRequestError):
        operation = GenerateVague("")
        await excuse_generator.execute(operation)

async def test_repository_error_handling(excuse_generator, mock_excuse_repository):
    mock_excuse_repository.execute.side_effect = Exception("Connection failed")
    with pytest.raises(ExcuseGenerationError):
        operation = GenerateVague("Can you help?")
        await excuse_generator.execute(operation)
```

## Integration vs Unit Testing

### Unit Tests - Testing Operations in Isolation

```python
# tests/services/excuse_generator/operations/test_generate_vague.py
class TestGenerateVague:
    """Unit tests for GenerateVague operation."""

    async def test_execute_calls_repository_with_correct_operation(
        self, excuse_generator, mock_excuse_repository
    ):
        # Arrange
        request = "Can you help me move?"
        mock_excuse_repository.execute.return_value = "excuse"
        operation = GenerateVague(request)

        # Act
        await excuse_generator.execute(operation)

        # Assert
        mock_excuse_repository.execute.assert_awaited_once()
        call_args = mock_excuse_repository.execute.call_args[0][0]
        assert isinstance(call_args, GetVague)
        assert call_args.prompt == request
```

### Mocking Boundaries for Unit Tests

```python
# Mock at service boundaries, not internal implementation
class TestExcuseGenerator:
    async def test_generate_excuse(self, mock_excuse_repository):
        # Arrange - mock external dependency (repository)
        mock_excuse_repository.execute.return_value = "excuse"
        service = ExcuseGenerator(excuse_repository=mock_excuse_repository)
        operation = GenerateVague("Can you help?")

        # Act
        result = await service.execute(operation)

        # Assert
        assert result == "excuse"
        # Don't mock internal operation logic, test it directly
```

### Testing Command Pattern Operations Independently

```python
# Test operation logic independently when it has complex business logic
class TestGenerateVagueOperationLogic:
    async def test_operation_validates_request(self):
        # Test operation's validation logic
        with pytest.raises(InvalidRequestError):
            operation = GenerateVague("")

    async def test_operation_formats_request(self):
        # Test operation's formatting logic
        operation = GenerateVague("  Can you help?  ")
        assert operation.request == "Can you help?"  # Trimmed

    async def test_operation_interacts_with_service(
        self, excuse_generator, mock_excuse_repository
    ):
        # Test operation's interaction with service
        mock_excuse_repository.execute.return_value = "excuse"
        operation = GenerateVague("Can you help?")

        result = await operation.execute(excuse_generator)

        assert result == "excuse"
        mock_excuse_repository.execute.assert_awaited_once()
```

## Example: Complete Test Suite

```python
# tests/services/excuse_generator/operations/test_generate_vague.py
import pytest
from unittest.mock import AsyncMock
from app.services.excuse_generator import ExcuseGenerator
from app.services.excuse_generator.operations import GenerateVague
from app.repositories.excuse_repository.operations import GetVague
from app.exceptions import ExcuseGenerationError, InvalidRequestError


class TestGenerateVague:
    """Test suite for GenerateVague operation."""

    async def test_success_returns_excuse_when_valid_request(
        self, excuse_generator, mock_excuse_repository
    ):
        # Arrange
        request = "Can you help me move this weekend?"
        expected_excuse = "I'd love to help, but I'm swamped with a critical project."
        mock_excuse_repository.execute.return_value = expected_excuse
        operation = GenerateVague(request)

        # Act
        result = await excuse_generator.execute(operation)

        # Assert
        assert result == expected_excuse
        assert isinstance(result, str)
        assert len(result) > 0

    async def test_calls_repository_with_correct_operation(
        self, excuse_generator, mock_excuse_repository
    ):
        # Arrange
        request = "Can you help?"
        mock_excuse_repository.execute.return_value = "excuse"
        operation = GenerateVague(request)

        # Act
        await excuse_generator.execute(operation)

        # Assert
        mock_excuse_repository.execute.assert_awaited_once()
        call_args = mock_excuse_repository.execute.call_args[0][0]
        assert isinstance(call_args, GetVague)

    async def test_raises_error_when_request_is_empty(self, excuse_generator):
        # Arrange
        operation = GenerateVague("")

        # Act & Assert
        with pytest.raises(InvalidRequestError) as exc_info:
            await excuse_generator.execute(operation)

        assert "Request cannot be empty" in str(exc_info.value)

    async def test_raises_error_when_repository_fails(
        self, excuse_generator, mock_excuse_repository
    ):
        # Arrange
        mock_excuse_repository.execute.side_effect = ExcuseGenerationError(
            "API failed"
        )
        operation = GenerateVague("Can you help?")

        # Act & Assert
        with pytest.raises(ExcuseGenerationError) as exc_info:
            await excuse_generator.execute(operation)

        assert "API failed" in str(exc_info.value)

    @pytest.mark.parametrize("request", [
        "Can you help me move?",
        "Want to grab coffee?",
        "Are you free this weekend?",
    ])
    async def test_handles_various_request_formats(
        self, excuse_generator, mock_excuse_repository, request
    ):
        # Arrange
        mock_excuse_repository.execute.return_value = "excuse"
        operation = GenerateVague(request)

        # Act
        result = await excuse_generator.execute(operation)

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0
        mock_excuse_repository.execute.assert_awaited_once()
```
