# Ghost-as-a-Service

## Project Overview

**Ghost as a Service** is an API that generates vague, professional-sounding excuses to help users gracefully decline social obligations. This takes a request or invitation as input and returns a plausible-sounding excuse filled with corporate jargon and technical mumbo-jumbo that sounds busy but is actually meaningless.

### Example Usage

**Input:** "Hey, are you free to help with the move this weekend?"

**Output:** "Hey! So sorry, I'm actually in the middle of a massive data migration and my bandwidth is currently throttled by some legacy infrastructure issues. Let's circle back in Q3?"

## Technology Stack

- **python**: Primary programming language
- **pydantic**: Data validation and settings management
- **pydantic-ai**: AI integration for generating responses
- **pydantic-settings**: Configuration management
- **pytest**: Testing framework
- **pytest-mock**: Mocking utilities for tests
- **lambda-powertools**: AWS Lambda utilities for logging, tracing, and metrics
- **docker**: Containerization for local development and testing
- **docker-compose**: Multi-container orchestration
- **uv**: Fast Python package installer and resolver

## Project Architecture

### Overview

- This is an AWS Lambda function designed to be serverless
- Uses PydanticAI for generating creative, contextually appropriate excuses
- Leverages Lambda Powertools for observability and best practices
- Configuration managed via Pydantic Settings for environment-based configs
- Docker/Docker Compose for local development and testing

### Project Structure
```
project/
├── app/
│   ├── __init__.py    # Lambda function entry point
│   ├── models.py    # Pydantic models for request/response
│   ├── utilities/    # Helper functions and utilities
│   ├── repositories/   # Data access layer
│   └── services/    # Core service logic for excuse generation
├── tests/
│   ├── utilities/    # Unit tests for the Lambda function
│   ├── repositories/    # Unit tests for data access layer
│   └── services/    # Unit tests for service logic
├── Dockerfile    # Dockerfile for local development
├── docker-compose.yml    # Docker Compose configuration
├── pyproject.toml    # Project dependencies and settings
├── uv.lock    # Lock file for dependencies    
└── README.md    # Project documentation
```
