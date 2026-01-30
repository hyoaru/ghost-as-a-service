"""Shared test fixtures for excuse repository tests."""

import pytest
from unittest.mock import AsyncMock

from app.repositories.excuse_repository import (
    AgentExcuseRepository,
    PrepopulatedExcuseRepository,
)
from app.repositories.excuse_repository.implementations.prepopulated.settings import (
    Settings as PrepopulatedSettings,
)
from app.utilities.excuse_agent import ExcuseAgent


@pytest.fixture
def mock_excuse_agent():
    """Mock ExcuseAgent for testing."""
    mock = AsyncMock(spec=ExcuseAgent)
    mock.execute = AsyncMock(return_value="Mocked vague excuse")
    return mock


@pytest.fixture
def agent_repository(mock_excuse_agent):
    """Agent-based repository with mocked agent."""
    return AgentExcuseRepository(excuse_agent=mock_excuse_agent)


@pytest.fixture
def prepopulated_settings():
    """Settings with custom excuse list for testing."""
    return PrepopulatedSettings(
        PREPOPULATED_EXCUSES=[
            "Test excuse 1",
            "Test excuse 2",
            "Test excuse 3",
        ]
    )


@pytest.fixture
def prepopulated_repository(prepopulated_settings):
    """Prepopulated repository with custom excuses."""
    return PrepopulatedExcuseRepository(settings=prepopulated_settings)


@pytest.fixture
def empty_prepopulated_repository():
    """Prepopulated repository with empty excuse list."""
    settings = PrepopulatedSettings(PREPOPULATED_EXCUSES=[])
    return PrepopulatedExcuseRepository(settings=settings)
