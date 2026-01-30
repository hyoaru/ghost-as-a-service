"""Shared test fixtures for the Excuse Generator Service tests."""

import pytest
from unittest.mock import AsyncMock

from app.repositories.excuse_repository import ExcuseRepositoryABC
from app.services.excuse_generator import ExcuseGeneratorService


@pytest.fixture
def mock_excuse_repository():
    """Mock repository for testing the service layer."""
    mock = AsyncMock(spec=ExcuseRepositoryABC)
    mock.execute.return_value = (
        "Sorry, I'm swamped with a massive data migration project right now."
    )
    return mock


@pytest.fixture
def excuse_generator_service(mock_excuse_repository):
    """Excuse generator service with mocked dependencies."""
    return ExcuseGeneratorService(repository=mock_excuse_repository)


@pytest.fixture
def sample_request():
    """Sample request for testing."""
    return "Can you help me move this weekend?"


@pytest.fixture(
    params=[
        "Can you help me move this weekend?",
        "Want to grab coffee tomorrow?",
        "Are you free for a quick call?",
        "Can you review my code?",
    ]
)
def various_requests(request):
    """Provides multiple request variations for parametrized testing."""
    return request.param
