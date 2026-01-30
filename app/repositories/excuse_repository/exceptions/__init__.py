"""Exception exports for the Excuse Repository."""

from .base import ExcuseRepositoryException
from .excuse_generation_error import ExcuseGenerationError
from .invalid_excuse_request_error import InvalidExcuseRequestError

__all__ = [
    "ExcuseRepositoryException",
    "ExcuseGenerationError",
    "InvalidExcuseRequestError",
]
