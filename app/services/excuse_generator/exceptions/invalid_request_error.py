"""Invalid request error for the Excuse Generator Service."""

from .base import ExcuseGeneratorServiceException


class InvalidRequestError(ExcuseGeneratorServiceException):
    """Raised when the request is invalid or cannot be processed.

    This typically occurs when:
    - The request text is empty or malformed
    - The request violates business rules
    - Required parameters are missing
    """

    pass
