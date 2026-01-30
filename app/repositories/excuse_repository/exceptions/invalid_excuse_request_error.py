"""Exception raised for invalid excuse requests."""

from .base import ExcuseRepositoryException


class InvalidExcuseRequestError(ExcuseRepositoryException):
    """Raised when an excuse request is invalid.

    This can occur when:
    - Required parameters are missing
    - Request text is empty or malformed
    - Invalid configuration is provided
    """

    pass
