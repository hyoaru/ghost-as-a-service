"""Tests for the Prepopulated Excuse Repository implementation."""

import pytest

from app.repositories.excuse_repository import PrepopulatedExcuseRepository
from app.repositories.excuse_repository.exceptions import (
    ExcuseGenerationError,
    InvalidExcuseRequestError,
)
from app.repositories.excuse_repository.implementations.prepopulated.operations import (
    GetExcuse,
)


@pytest.mark.asyncio
async def test_get_excuse_success(prepopulated_repository):
    """Test successful excuse retrieval from prepopulated repository."""
    operation = GetExcuse(request="Can you help me move this weekend?")
    result = await prepopulated_repository.execute(operation)

    assert isinstance(result, str)
    assert len(result) > 0
    assert result in ["Test excuse 1", "Test excuse 2", "Test excuse 3"]


@pytest.mark.asyncio
async def test_get_excuse_returns_different_excuses(prepopulated_repository):
    """Test that multiple calls can return different excuses."""
    operation = GetExcuse(request="Can you help?")
    results = set()

    for _ in range(20):
        result = await prepopulated_repository.execute(operation)
        results.add(result)

    assert len(results) >= 1


@pytest.mark.asyncio
async def test_get_excuse_with_empty_request_raises_error():
    """Test that empty request raises InvalidExcuseRequestError."""
    with pytest.raises(InvalidExcuseRequestError) as exc_info:
        GetExcuse(request="")

    assert "cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_excuse_with_whitespace_request_raises_error():
    """Test that whitespace-only request raises InvalidExcuseRequestError."""
    with pytest.raises(InvalidExcuseRequestError):
        GetExcuse(request="   ")


@pytest.mark.asyncio
async def test_get_excuse_with_empty_list_raises_error(empty_prepopulated_repository):
    """Test that empty excuse list raises ExcuseGenerationError."""
    operation = GetExcuse(request="Can you help?")

    with pytest.raises(ExcuseGenerationError) as exc_info:
        await empty_prepopulated_repository.execute(operation)

    assert "No excuses available" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_excuse_with_wrong_repository_type():
    """Test that operation rejects wrong repository type."""
    from app.repositories.excuse_repository import AgentExcuseRepository
    from unittest.mock import AsyncMock

    wrong_repo = AgentExcuseRepository(excuse_agent=AsyncMock())
    operation = GetExcuse(request="Can you help?")

    with pytest.raises(TypeError) as exc_info:
        await operation.execute(wrong_repo)

    assert "Expected PrepopulatedExcuseRepository" in str(exc_info.value)


def test_repository_initialization_with_defaults():
    """Test that repository can be initialized with default settings."""
    repo = PrepopulatedExcuseRepository()

    assert repo.settings is not None
    assert len(repo.excuses) > 0


def test_repository_initialization_with_custom_settings(prepopulated_settings):
    """Test that repository accepts custom settings."""
    repo = PrepopulatedExcuseRepository(settings=prepopulated_settings)

    assert repo.settings is prepopulated_settings
    assert repo.excuses == prepopulated_settings.PREPOPULATED_EXCUSES
