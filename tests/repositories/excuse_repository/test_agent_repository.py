"""Tests for the Agent Excuse Repository implementation."""

import pytest
from unittest.mock import AsyncMock

from app.repositories.excuse_repository import AgentExcuseRepository
from app.repositories.excuse_repository.exceptions import (
    ExcuseGenerationError,
    InvalidExcuseRequestError,
)


@pytest.mark.asyncio
async def test_get_excuse_success(agent_repository, mock_excuse_agent):
    """Test successful excuse retrieval from agent repository."""
    result = await agent_repository.get_excuse("Can you help me move this weekend?")

    assert result == "Mocked vague excuse"
    mock_excuse_agent.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_excuse_with_empty_request_raises_error(agent_repository):
    """Test that empty request raises InvalidExcuseRequestError."""
    with pytest.raises(InvalidExcuseRequestError) as exc_info:
        await agent_repository.get_excuse("")

    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_excuse_with_whitespace_request_raises_error(agent_repository):
    """Test that whitespace-only request raises InvalidExcuseRequestError."""
    with pytest.raises(InvalidExcuseRequestError):
        await agent_repository.get_excuse("   ")


@pytest.mark.asyncio
async def test_get_excuse_handles_agent_failure(agent_repository, mock_excuse_agent):
    """Test that agent failures are wrapped in ExcuseGenerationError."""
    mock_excuse_agent.execute.side_effect = Exception("Agent failed")

    with pytest.raises(ExcuseGenerationError) as exc_info:
        await agent_repository.get_excuse("Can you help me?")
        await agent_repository.get_excuse("Can you help me?")

    assert "Failed to generate excuse" in str(exc_info.value)


def test_repository_initialization_with_defaults(mock_excuse_agent):
    """Test that repository can be initialized with custom agent."""
    repo = AgentExcuseRepository(excuse_agent=mock_excuse_agent)

    assert repo.excuse_agent is not None
    assert repo.settings is not None


def test_repository_initialization_with_custom_agent(mock_excuse_agent):
    """Test that repository accepts custom ExcuseAgent."""
    repo = AgentExcuseRepository(excuse_agent=mock_excuse_agent)

    assert repo.excuse_agent is mock_excuse_agent
