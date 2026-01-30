"""Exception raised when excuse generation fails."""

from .base import ExcuseRepositoryException


class ExcuseGenerationError(ExcuseRepositoryException):
    """Raised when the repository fails to generate or retrieve an excuse.

    This can occur when:
    - The agent fails to generate a response
    - The prepopulated list is empty
    - Network or API errors occur
    """

    pass
