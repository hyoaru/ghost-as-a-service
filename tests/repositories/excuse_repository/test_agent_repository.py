"""Tests for the Agent Excuse Repository implementation."""

import pytest
from unittest.mock import AsyncMock

from app.repositories.excuse_repository import AgentExcuseRepository
from app.repositories.excuse_repository.exceptions import ExcuseGenerationError
from app.repositories.excuse_repository.implementations.agent.operations import (
    GetExcuse,
)


@pytest.mark.asyncio
async def test_get_excuse_success(agent_repository, mock_excuse_agent):
    """Test successful excuse retrieval from agent repository."""
    operation = GetExcuse(request="Can you help me move this weekend?")
    result = await agent_repository.execute(operation)

    assert result == "Mocked vague excuse"
    mock_excuse_agent.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_excuse_with_empty_request_raises_error():
    """Test that empty request raises InvalidExcuseRequestError."""
    from app.repositories.excuse_repository.exceptions import InvalidExcuseRequestError

    with pytest.raises(InvalidExcuseRequestError) as exc_info:
        GetExcuse(request="")

    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_excuse_with_whitespace_request_raises_error():
    """Test that whitespace-only request raises InvalidExcuseRequestError."""
    from app.repositories.excuse_repository.exceptions import InvalidExcuseRequestError

    with pytest.raises(InvalidExcuseRequestError):
        GetExcuse(request="   ")


@pytest.mark.asyncio
async def test_get_excuse_handles_agent_failure(agent_repository, mock_excuse_agent):
    """Test that agent failures are wrapped in ExcuseGenerationError."""
    mock_excuse_agent.execute.side_effect = Exception("Agent failed")

    operation = GetExcuse(request="Can you help me?")

    with pytest.raises(ExcuseGenerationError) as exc_info:
        await agent_repository.execute(operation)

    assert "Failed to generate excuse" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_excuse_with_wrong_repository_type():
    """Test that operation rejects wrong repository type."""
    from app.repositories.excuse_repository import PrepopulatedExcuseRepository

    wrong_repo = PrepopulatedExcuseRepository()
    operation = GetExcuse(request="Can you help?")

    with pytest.raises(TypeError) as exc_info:
        await operation.execute(wrong_repo)

    assert "Expected AgentExcuseRepository" in str(exc_info.value)


def test_repository_initialization_with_defaults(mock_excuse_agent):
    """Test that repository can be initialized with custom agent."""
    repo = AgentExcuseRepository(excuse_agent=mock_excuse_agent)

    assert repo.excuse_agent is not None
    assert repo.settings is not None


def test_repository_initialization_with_custom_agent(mock_excuse_agent):
    """Test that repository accepts custom ExcuseAgent."""
    repo = AgentExcuseRepository(excuse_agent=mock_excuse_agent)

    assert repo.excuse_agent is mock_excuse_agent
