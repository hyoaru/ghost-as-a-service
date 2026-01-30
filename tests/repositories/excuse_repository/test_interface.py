"""Tests for the Excuse Repository interface."""

import pytest

from app.repositories.excuse_repository import (
    ExcuseRepositoryABC,
    ExcuseRepositoryOperationABC,
)


def test_repository_abc_is_abstract():
    """Verify that ExcuseRepositoryABC cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ExcuseRepositoryABC()


def test_operation_abc_is_abstract():
    """Verify that ExcuseRepositoryOperationABC cannot be instantiated directly."""
    with pytest.raises(TypeError):
        ExcuseRepositoryOperationABC()
