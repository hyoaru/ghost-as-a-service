"""
Pytest configuration and shared fixtures for utility tests.
"""

import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_pydantic_agent():
    """
    Mock PydanticAI Agent for testing.

    Returns:
        AsyncMock: Mocked Agent instance.
    """
    mock = AsyncMock()
    mock.run.return_value.output = "Mocked excuse response"
    return mock
