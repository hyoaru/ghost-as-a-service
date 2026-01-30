"""Base exception class for the Excuse Generator Service."""


class ExcuseGeneratorServiceException(Exception):
    """Base exception for all excuse generator service errors.

    All service-specific exceptions should inherit from this class
    to enable consistent error handling across the service layer.
    """

    pass
