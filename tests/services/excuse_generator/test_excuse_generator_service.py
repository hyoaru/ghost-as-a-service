"""Tests for the Excuse Generator Service interface and implementation."""

import pytest
from unittest.mock import AsyncMock

from app.repositories.excuse_repository import AgentExcuseRepository, ExcuseRepositoryABC
from app.services.excuse_generator import (
    ExcuseGeneratorService,
    ExcuseGeneratorServiceABC,
)
from app.services.excuse_generator.operations import GenerateExcuse


class TestExcuseGeneratorService:
    """Test suite for ExcuseGeneratorService implementation."""

    def test_service_initialization_with_repository(self, mock_excuse_repository):
        """Test service initializes correctly with provided repository."""
        # Arrange & Act
        service = ExcuseGeneratorService(repository=mock_excuse_repository)

        # Assert
        assert isinstance(service, ExcuseGeneratorServiceABC)
        assert service.repository is mock_excuse_repository

    def test_service_initialization_with_default_repository(self, mocker):
        """Test service initializes with default AgentExcuseRepository."""
        # Arrange
        mock_agent_repo = mocker.patch("app.services.excuse_generator.AgentExcuseRepository")

        # Act
        service = ExcuseGeneratorService()

        # Assert
        assert isinstance(service, ExcuseGeneratorServiceABC)
        mock_agent_repo.assert_called_once()

    async def test_execute_delegates_to_operation(
        self, excuse_generator_service, mock_excuse_repository, sample_request
    ):
        """Test service execute method delegates to operation correctly."""
        # Arrange
        expected_excuse = "Sorry, I'm dealing with some critical infrastructure issues."
        mock_excuse_repository.execute.return_value = expected_excuse
        operation = GenerateExcuse(request=sample_request)

        # Act
        result = await excuse_generator_service.execute(operation)

        # Assert
        assert result == expected_excuse
        mock_excuse_repository.execute.assert_awaited_once()

    async def test_execute_passes_service_context_to_operation(
        self, excuse_generator_service, sample_request
    ):
        """Test operation receives service context for dependency access."""
        # Arrange
        operation = AsyncMock(spec=GenerateExcuse)
        operation.execute.return_value = "test excuse"

        # Act
        await excuse_generator_service.execute(operation)

        # Assert
        operation.execute.assert_awaited_once_with(excuse_generator_service)

    async def test_execute_with_various_requests(
        self, excuse_generator_service, various_requests, mock_excuse_repository
    ):
        """Test service handles various request types correctly."""
        # Arrange
        operation = GenerateExcuse(request=various_requests)

        # Act
        result = await excuse_generator_service.execute(operation)

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0
        mock_excuse_repository.execute.assert_awaited_once()
