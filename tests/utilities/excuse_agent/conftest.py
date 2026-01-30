"""
Pytest configuration and shared fixtures for excuse_agent tests.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock, Mock

import pytest

from app.utilities.excuse_agent import ExcuseAgent
from app.utilities.excuse_agent.settings import Settings


@pytest.fixture
def mock_settings() -> Generator[Settings, None, None]:
    """
    Mock Settings with fake API key.

    Returns:
        Settings: Settings instance with test configuration.
    """
    # Set environment variable for testing
    import os
    os.environ["GEMINI_API_KEY"] = "test_api_key_12345"
    yield Settings()
    # Cleanup
    os.environ.pop("GEMINI_API_KEY", None)


@pytest.fixture
def mock_agent():
    """
    Mock PydanticAI Agent instance.

    Returns:
        AsyncMock: Mocked Agent with default behavior.
    """
    mock = AsyncMock()
    # Configure default successful response
    mock.run.return_value.output = "I'm swamped with a critical infrastructure migration."
    return mock


@pytest.fixture
def excuse_agent(mock_agent, mock_settings):
    """
    ExcuseAgent instance with mocked dependencies.

    Args:
        mock_agent: Mocked PydanticAI Agent.
        mock_settings: Mocked Settings.

    Returns:
        ExcuseAgent: Fully configured test instance.
    """
    return ExcuseAgent(agent=mock_agent, settings=mock_settings)
