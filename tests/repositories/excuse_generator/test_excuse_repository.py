"""
Unit tests for ExcuseRepository implementation.
"""

from typing import TypeVar
from unittest.mock import AsyncMock, patch

import pytest

from app.repositories.excuse_generator import (
    ExcuseRepository,
    ExcuseRepositoryABC,
)
from app.repositories.excuse_generator.interface import RepositoryOperationABC
from app.settings import Settings

T = TypeVar("T")


class TestExcuseRepositoryABCInterface:
    """Test suite for ExcuseRepositoryABC interface definition."""

    def test_excuse_repository_abc_has_execute_method(self):
        """Verify ExcuseRepositoryABC defines execute abstract method."""
        # Arrange & Act
        abstract_methods = ExcuseRepositoryABC.__abstractmethods__

        # Assert
        assert "execute" in abstract_methods


class TestExcuseRepositoryInitialization:
    """Test suite for ExcuseRepository initialization."""

    @patch("app.repositories.excuse_generator.excuse_repository.Agent")
    def test_excuse_repository_initialization_default_settings(
        self, mock_agent_class, monkeypatch
    ):
        """Test ExcuseRepository initializes with default Settings when none provided."""
        # Arrange - Set environment variables for Settings
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "test-service")
        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("POWERTOOLS_INJECT_LOG_CONTEXT", "true")
        monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key")

        # Act
        repository = ExcuseRepository()

        # Assert
        assert repository is not None
        assert isinstance(repository, ExcuseRepositoryABC)
        assert hasattr(repository, "settings")
        assert isinstance(repository.settings, Settings)
        mock_agent_class.assert_called_once()

    @patch("app.repositories.excuse_generator.excuse_repository.Agent")
    def test_excuse_repository_initialization_with_settings(self, mock_agent_class):
        """Test ExcuseRepository initializes with provided Settings instance."""
        # Arrange
        test_settings = Settings(
            POWERTOOLS_SERVICE_NAME="test-service",
            POWERTOOLS_LOG_LEVEL="DEBUG",
            POWERTOOLS_INJECT_LOG_CONTEXT=True,
            GOOGLE_API_KEY="custom-api-key",
        )

        # Act
        repository = ExcuseRepository(settings=test_settings)

        # Assert
        assert repository is not None
        assert repository.settings is test_settings
        assert repository.settings.GOOGLE_API_KEY == "custom-api-key"
        mock_agent_class.assert_called_once()


class TestExcuseRepositoryExecute:
    """Test suite for ExcuseRepository execute method."""

    @pytest.fixture
    def mock_settings(self):
        """Fixture providing mock Settings."""
        return Settings(
            POWERTOOLS_SERVICE_NAME="test-service",
            POWERTOOLS_LOG_LEVEL="INFO",
            POWERTOOLS_INJECT_LOG_CONTEXT=False,
            GOOGLE_API_KEY="test-api-key",
        )

    @pytest.fixture
    @patch("app.repositories.excuse_generator.excuse_repository.Agent")
    def repository(self, mock_agent_class, mock_settings):
        """Fixture providing ExcuseRepository instance."""
        return ExcuseRepository(settings=mock_settings)

    @pytest.mark.anyio
    async def test_excuse_repository_execute_delegates_to_operation(self, repository):
        """Test that execute method delegates to operation.execute()."""
        # Arrange
        mock_operation = AsyncMock(spec=RepositoryOperationABC)
        mock_operation.execute.return_value = "test result"

        # Act
        result = await repository.execute(mock_operation)

        # Assert
        assert result == "test result"
        mock_operation.execute.assert_awaited_once_with(repository)

    @pytest.mark.anyio
    async def test_excuse_repository_execute_with_different_return_type(self, repository):
        """Test execute method works with operations returning different types."""
        # Arrange
        mock_operation = AsyncMock(spec=RepositoryOperationABC)
        expected_data = {"key": "value", "count": 42}
        mock_operation.execute.return_value = expected_data

        # Act
        result = await repository.execute(mock_operation)

        # Assert
        assert result == expected_data
        assert isinstance(result, dict)
        mock_operation.execute.assert_awaited_once_with(repository)

    @pytest.mark.anyio
    async def test_excuse_repository_execute_propagates_exceptions(self, repository):
        """Test that execute method propagates exceptions from operations."""
        # Arrange
        mock_operation = AsyncMock(spec=RepositoryOperationABC)
        mock_operation.execute.side_effect = ValueError("Test error")

        # Act & Assert
        with pytest.raises(ValueError, match="Test error"):
            await repository.execute(mock_operation)

