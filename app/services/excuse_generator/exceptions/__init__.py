"""Exception classes for the Excuse Generator Service."""

from .base import ExcuseGeneratorServiceException
from .invalid_request_error import InvalidRequestError
from .service_generation_error import ServiceGenerationError

__all__ = [
    "ExcuseGeneratorServiceException",
    "InvalidRequestError",
    "ServiceGenerationError",
]
