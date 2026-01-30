"""Service generation error for the Excuse Generator Service."""

from .base import ExcuseGeneratorServiceException


class ServiceGenerationError(ExcuseGeneratorServiceException):
    """Raised when excuse generation fails at the service layer.

    This typically occurs when:
    - Repository operations fail
    - Business logic validation fails
    - Unexpected errors during orchestration
    """

    pass
