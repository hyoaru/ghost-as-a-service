# Ghost-as-a-Service

> An API that generates vague, professional-sounding excuses to help you gracefully decline social obligations.

## Overview

**Ghost as a Service** takes a request or invitation as input and returns a plausible-sounding excuse filled with corporate jargon and technical mumbo-jumbo that sounds busy but is actually meaningless.

### Example Usage

**Input:** "Hey, are you free to help with the move this weekend?"

**Output:** "Hey! So sorry, I'm actually in the middle of a massive data migration and my bandwidth is currently throttled by some legacy infrastructure issues. Let's circle back in Q3?"

## Technology Stack

- **Python 3.12+**: Primary programming language
- **Pydantic**: Data validation and settings management
- **PydanticAI**: AI integration for generating creative responses
- **AWS Lambda**: Serverless compute platform
- **AWS Lambda Powertools**: Logging, tracing, and metrics utilities
- **Google Gemini**: AI model via PydanticAI
- **pytest**: Testing framework
- **Docker**: Containerization for local development
- **uv**: Fast Python package installer and resolver

## Project Structure

```
ghost-as-a-service/
├── app/
│   ├── __init__.py          # Lambda handler entry point
│   ├── models.py            # Pydantic models (EventModel, ExcuseResponse)
│   ├── settings.py          # Configuration management
│   ├── exceptions.py        # Custom exception classes
│   ├── utilities/           # Helper functions and utilities
│   ├── repositories/        # Data access layer
│   └── services/            # Business logic (excuse generation)
├── tests/
│   ├── conftest.py          # Shared pytest fixtures
│   ├── test_models.py       # Model validation tests
│   ├── test_settings.py     # Settings configuration tests
│   ├── test_exceptions.py   # Exception tests
│   ├── utilities/           # Utility tests
│   ├── repositories/        # Repository tests
│   └── services/            # Service logic tests
├── .env.example             # Example environment configuration
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration
├── pyproject.toml           # Project dependencies and settings
└── README.md                # This file
```

## Architecture

### Design Principles

- **Command Pattern**: Services use the Command pattern for modular, testable operations
- **Dependency Injection**: Constructor-based injection with optional defaults
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Type Safety**: Full type hints throughout the codebase
- **Test-Driven Development**: All features developed with TDD approach

### Key Components

1. **Lambda Handler** ([app/**init**.py](app/__init__.py))
   - Entry point for AWS Lambda
   - Uses Lambda Powertools for logging and parsing
   - Delegates to service layer for business logic

2. **Models** ([app/models.py](app/models.py))
   - `EventModel`: Input validation for Lambda events
   - `ExcuseResponse`: Structured response with excuse and metadata

3. **Settings** ([app/settings.py](app/settings.py))
   - Centralized configuration management
   - Environment variable loading via Pydantic Settings
   - Type-safe configuration with validation

4. **Exceptions** ([app/exceptions.py](app/exceptions.py))
   - Custom exception types for different error scenarios
   - Clear error handling and messaging

5. **Services** (app/services/)
   - Business logic for excuse generation
   - Uses PydanticAI for AI-powered text generation
   - Command pattern for operation-based execution

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
   # Edit .env and add your GOOGLE_API_KEY
   ```

4. **Run tests:**
   ```bash
   uv run pytest
   ```

### Configuration

Create a `.env` file based on `.env.example`:

```env
# AWS Lambda Powertools Configuration
POWERTOOLS_SERVICE_NAME=excuse-generator
POWERTOOLS_LOG_LEVEL=INFO
POWERTOOLS_INJECT_LOG_CONTEXT=true

# AI Configuration
GOOGLE_API_KEY=your-google-api-key-here
```

#### Configuration Options

| Variable                        | Required | Description                                       |
| ------------------------------- | -------- | ------------------------------------------------- |
| `POWERTOOLS_SERVICE_NAME`       | Yes      | Name of the Lambda service for Powertools logging |
| `POWERTOOLS_LOG_LEVEL`          | Yes      | Logging level (DEBUG, INFO, WARNING, ERROR)       |
| `POWERTOOLS_INJECT_LOG_CONTEXT` | Yes      | Whether to inject Lambda context into logs        |
| `GOOGLE_API_KEY`                | Yes      | API key for Google AI (Gemini) via PydanticAI     |

## Development

### Running Locally with Docker

```bash
# Start the development environment
docker-compose up

# Run tests in Docker
docker-compose run app pytest

# Run linting
docker-compose run app ruff check .

# Format code
docker-compose run app ruff format .
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_models.py

# Run with verbose output
uv run pytest -v
```

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

- Follow Test-Driven Development (TDD) principles
- Write tests before implementing features
- Aim for 80%+ test coverage
- Use AAA pattern: Arrange, Act, Assert
- Mock external dependencies
- Use descriptive test names

See [.github/instructions/testing-standards.instructions.md](.github/instructions/testing-standards.instructions.md) for detailed guidelines.

## API Usage

### Lambda Event Format

**Input:**

```json
{
  "request": "Can you help me move this weekend?"
}
```

**Output:**

```json
{
  "excuse": "Hey! So sorry, I'm actually in the middle of a massive data migration and my bandwidth is currently throttled by some legacy infrastructure issues. Let's circle back in Q3?",
  "metadata": {
    "model": "gemini-1.5-flash",
    "tokens": 150
  }
}
```

### Error Handling

The service uses custom exceptions for different error scenarios:

- `ExcuseGenerationError`: When AI generation fails
- `InvalidRequestError`: When input validation fails
- `AIServiceError`: When PydanticAI encounters issues
- `ConfigurationError`: When required configuration is missing

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

1. Follow the coding standards in `.github/instructions/core-standards.instructions.md`
2. Write tests for all new features (TDD approach)
3. Ensure all tests pass before submitting PR
4. Run linting and formatting checks
5. Update documentation as needed

## License

[Add your license here]

## Support

For issues, questions, or contributions, please [open an issue](https://github.com/your-repo/issues) on GitHub.
