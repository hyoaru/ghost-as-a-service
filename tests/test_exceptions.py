"""
Tests for custom exception classes.
"""

import pytest
from app.exceptions import ExcuseGenerationError


def test_excuse_generation_error_initialization():
    """
    Test that ExcuseGenerationError can be initialized with a message.

    Verifies:
        - Exception can be created with custom message
        - Message is accessible via str()
        - Exception is instance of Exception base class
    """
    # Arrange
    error_message = "Failed to generate excuse due to AI error"

    # Act
    error = ExcuseGenerationError(error_message)

    # Assert
    assert isinstance(error, Exception)
    assert str(error) == error_message


def test_invalid_request_error_initialization():
    """
    Test that InvalidRequestError can be initialized with a message.

    Verifies:
        - Exception can be created with validation message
        - Message is accessible
    """
    # Arrange
    error_message = "Request field cannot be empty"

    # Act
    from app.exceptions import InvalidRequestError

    error = InvalidRequestError(error_message)

    # Assert
    assert isinstance(error, Exception)
    assert str(error) == error_message


def test_ai_service_error_initialization():
    """
    Test that AIServiceError can be initialized with a message.

    Verifies:
        - Exception can be created for PydanticAI errors
        - Message is accessible
    """
    # Arrange
    error_message = "PydanticAI service is unavailable"

    # Act
    from app.exceptions import AIServiceError

    error = AIServiceError(error_message)

    # Assert
    assert isinstance(error, Exception)
    assert str(error) == error_message


def test_configuration_error_initialization():
    """
    Test that ConfigurationError can be initialized with a message.

    Verifies:
        - Exception can be created for config issues
        - Message is accessible
    """
    # Arrange
    error_message = "GOOGLE_API_KEY is not configured"

    # Act
    from app.exceptions import ConfigurationError

    error = ConfigurationError(error_message)

    # Assert
    assert isinstance(error, Exception)
    assert str(error) == error_message


def test_exception_can_be_raised_and_caught():
    """
    Test that custom exceptions can be raised and caught.

    Verifies:
        - Exceptions can be raised in try/except blocks
        - Exception type is preserved
        - Message is accessible after catching
    """
    # Arrange
    from app.exceptions import ExcuseGenerationError

    # Act & Assert
    with pytest.raises(ExcuseGenerationError) as exc_info:
        raise ExcuseGenerationError("Test error message")

    assert str(exc_info.value) == "Test error message"


def test_exception_inheritance():
    """
    Test that all custom exceptions inherit from Exception.

    Verifies:
        - All custom exceptions can be caught as Exception
        - Exception hierarchy is correct
    """
    # Arrange & Act
    from app.exceptions import (
        ExcuseGenerationError,
        InvalidRequestError,
        AIServiceError,
        ConfigurationError,
    )

    # Assert
    assert issubclass(ExcuseGenerationError, Exception)
    assert issubclass(InvalidRequestError, Exception)
    assert issubclass(AIServiceError, Exception)
    assert issubclass(ConfigurationError, Exception)
