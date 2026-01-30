"""
Custom exception classes for the excuse generator application.
"""


class ExcuseGenerationError(Exception):
    """
    Raised when AI generation fails to produce a valid excuse.

    This exception is raised when the PydanticAI model encounters an error
    during excuse generation or produces invalid output.
    """

    pass


class InvalidRequestError(Exception):
    """
    Raised when input validation fails.

    This exception is raised when the request data does not meet
    validation requirements (e.g., empty request, invalid format).
    """

    pass


class AIServiceError(Exception):
    """
    Raised when PydanticAI encounters service issues.

    This exception is raised when there are problems communicating with
    the AI service, such as network errors, API errors, or rate limiting.
    """

    pass


class ConfigurationError(Exception):
    """
    Raised when required configuration is missing or invalid.

    This exception is raised when environment variables or settings
    required for the application to function are not properly configured.
    """

    pass
