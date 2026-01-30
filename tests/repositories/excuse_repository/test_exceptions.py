"""Tests for repository exceptions."""

import pytest

from app.repositories.excuse_repository.exceptions import (
    ExcuseGenerationError,
    ExcuseRepositoryException,
    InvalidExcuseRequestError,
)


def test_base_exception_inheritance():
    """Verify ExcuseRepositoryException inherits from Exception."""
    assert issubclass(ExcuseRepositoryException, Exception)


def test_excuse_generation_error_inheritance():
    """Verify ExcuseGenerationError inherits from base exception."""
    assert issubclass(ExcuseGenerationError, ExcuseRepositoryException)


def test_invalid_excuse_request_error_inheritance():
    """Verify InvalidExcuseRequestError inherits from base exception."""
    assert issubclass(InvalidExcuseRequestError, ExcuseRepositoryException)


def test_excuse_generation_error_can_be_raised():
    """Verify ExcuseGenerationError can be raised and caught."""
    with pytest.raises(ExcuseGenerationError) as exc_info:
        raise ExcuseGenerationError("Test error message")

    assert str(exc_info.value) == "Test error message"


def test_invalid_excuse_request_error_can_be_raised():
    """Verify InvalidExcuseRequestError can be raised and caught."""
    with pytest.raises(InvalidExcuseRequestError) as exc_info:
        raise InvalidExcuseRequestError("Invalid request")

    assert str(exc_info.value) == "Invalid request"
