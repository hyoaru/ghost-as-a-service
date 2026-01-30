"""Tests for the GenerateExcuse operation."""

import pytest
from unittest.mock import AsyncMock

from app.repositories.excuse_repository.exceptions import (
    ExcuseGenerationError,
    InvalidExcuseRequestError,
)
from app.services.excuse_generator.exceptions import (
    InvalidRequestError,
    ServiceGenerationError,
)
from app.services.excuse_generator.operations import GenerateExcuse


class TestGenerateExcuse:
    """Test suite for GenerateExcuse operation."""

    def test_initialization_with_valid_request(self, sample_request):
        """Test operation initializes correctly with valid request."""
        # Arrange & Act
        operation = GenerateExcuse(request=sample_request)

        # Assert
        assert operation.request == sample_request

    def test_initialization_strips_whitespace(self):
        """Test operation strips leading/trailing whitespace from request."""
        # Arrange
        request_with_whitespace = "  Can you help me?  \n"

        # Act
        operation = GenerateExcuse(request=request_with_whitespace)

        # Assert
        assert operation.request == "Can you help me?"

    def test_initialization_raises_error_for_empty_request(self):
        """Test operation raises InvalidRequestError for empty request."""
        # Arrange & Act & Assert
        with pytest.raises(InvalidRequestError, match="Request text cannot be empty"):
            GenerateExcuse(request="")

    def test_initialization_raises_error_for_whitespace_only_request(self):
        """Test operation raises InvalidRequestError for whitespace-only request."""
        # Arrange & Act & Assert
        with pytest.raises(InvalidRequestError, match="Request text cannot be empty"):
            GenerateExcuse(request="   \n\t  ")

    async def test_execute_success(
        self, excuse_generator_service, mock_excuse_repository, sample_request
    ):
        """Test successful excuse generation."""
        # Arrange
        expected_excuse = "Sorry, I'm in the middle of a critical deployment cycle."
        mock_excuse_repository.execute.return_value = expected_excuse
        operation = GenerateExcuse(request=sample_request)

        # Act
        result = await operation.execute(excuse_generator_service)

        # Assert
        assert result == expected_excuse
        mock_excuse_repository.execute.assert_awaited_once()

    async def test_execute_calls_repository_with_correct_operation(
        self, excuse_generator_service, mock_excuse_repository, sample_request
    ):
        """Test operation calls repository with GetExcuse operation."""
        # Arrange
        operation = GenerateExcuse(request=sample_request)

        # Act
        await operation.execute(excuse_generator_service)

        # Assert
        mock_excuse_repository.execute.assert_awaited_once()
        call_args = mock_excuse_repository.execute.call_args[0][0]
        assert hasattr(call_args, "request")
        assert call_args.request == sample_request

    async def test_execute_wraps_invalid_excuse_request_error(
        self, excuse_generator_service, mock_excuse_repository, sample_request
    ):
        """Test InvalidExcuseRequestError is wrapped as InvalidRequestError."""
        # Arrange
        mock_excuse_repository.execute.side_effect = InvalidExcuseRequestError(
            "Invalid request format"
        )
        operation = GenerateExcuse(request=sample_request)

        # Act & Assert
        with pytest.raises(InvalidRequestError, match="Invalid request"):
            await operation.execute(excuse_generator_service)

    async def test_execute_wraps_excuse_generation_error(
        self, excuse_generator_service, mock_excuse_repository, sample_request
    ):
        """Test ExcuseGenerationError is wrapped as ServiceGenerationError."""
        # Arrange
        mock_excuse_repository.execute.side_effect = ExcuseGenerationError("API failed")
        operation = GenerateExcuse(request=sample_request)

        # Act & Assert
        with pytest.raises(ServiceGenerationError, match="Failed to generate excuse"):
            await operation.execute(excuse_generator_service)

    async def test_execute_wraps_unexpected_error(
        self, excuse_generator_service, mock_excuse_repository, sample_request
    ):
        """Test unexpected errors are wrapped as ServiceGenerationError."""
        # Arrange
        mock_excuse_repository.execute.side_effect = RuntimeError("Unexpected error")
        operation = GenerateExcuse(request=sample_request)

        # Act & Assert
        with pytest.raises(ServiceGenerationError, match="Unexpected error"):
            await operation.execute(excuse_generator_service)

    async def test_execute_preserves_original_exception_chain(
        self, excuse_generator_service, mock_excuse_repository, sample_request
    ):
        """Test exception chaining is preserved for debugging."""
        # Arrange
        original_error = ExcuseGenerationError("Original error")
        mock_excuse_repository.execute.side_effect = original_error
        operation = GenerateExcuse(request=sample_request)

        # Act & Assert
        with pytest.raises(ServiceGenerationError) as exc_info:
            await operation.execute(excuse_generator_service)

        assert exc_info.value.__cause__ is original_error
