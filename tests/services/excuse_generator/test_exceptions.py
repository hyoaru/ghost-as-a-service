"""Tests for Excuse Generator Service exceptions."""

import pytest

from app.services.excuse_generator.exceptions import (
    ExcuseGeneratorServiceException,
    InvalidRequestError,
    ServiceGenerationError,
)


class TestExcuseGeneratorServiceExceptions:
    """Test suite for service exception hierarchy."""

    def test_base_exception_inheritance(self):
        """Test base exception inherits from Exception."""
        # Arrange & Act
        exception = ExcuseGeneratorServiceException("test message")

        # Assert
        assert isinstance(exception, Exception)
        assert str(exception) == "test message"

    def test_invalid_request_error_inheritance(self):
        """Test InvalidRequestError inherits from base service exception."""
        # Arrange & Act
        exception = InvalidRequestError("invalid request")

        # Assert
        assert isinstance(exception, ExcuseGeneratorServiceException)
        assert isinstance(exception, Exception)
        assert str(exception) == "invalid request"

    def test_service_generation_error_inheritance(self):
        """Test ServiceGenerationError inherits from base service exception."""
        # Arrange & Act
        exception = ServiceGenerationError("generation failed")

        # Assert
        assert isinstance(exception, ExcuseGeneratorServiceException)
        assert isinstance(exception, Exception)
        assert str(exception) == "generation failed"

    def test_exceptions_can_be_caught_by_base_class(self):
        """Test all service exceptions can be caught by base class."""
        # Arrange
        exceptions = [
            InvalidRequestError("test1"),
            ServiceGenerationError("test2"),
        ]

        # Act & Assert
        for exc in exceptions:
            with pytest.raises(ExcuseGeneratorServiceException):
                raise exc
