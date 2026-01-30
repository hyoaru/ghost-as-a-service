"""
GenerateVague service operation.

This operation generates a vague excuse from a user request using the
excuse generator repository.
"""

from typing import TYPE_CHECKING

from app.exceptions import InvalidRequestError
from app.repositories.excuse_generator import GetVague
from app.services.excuse_generator.operations.interface import (
    ExcuseGeneratorOperationABC,
)

if TYPE_CHECKING:
    from app.services.excuse_generator.interface import ExcuseGeneratorABC


class GenerateVague(ExcuseGeneratorOperationABC[str]):
    """
    Service operation to generate a vague excuse from a user request.

    This operation takes a user request (e.g., a social obligation),
    validates it, and uses the excuse repository to generate a plausible
    but meaningless excuse filled with corporate jargon.

    Raises:
        InvalidRequestError: If request is empty or whitespace-only.
    """

    def __init__(self, request: str):
        """
        Initialize the GenerateVague operation.

        Args:
            request: The user request or social obligation to generate
                    an excuse for.

        Raises:
            InvalidRequestError: If request is empty or whitespace-only.
        """
        if not request or not request.strip():
            raise InvalidRequestError("Request cannot be empty")

        self.request = request.strip()

    async def execute(self, service: "ExcuseGeneratorABC") -> str:
        """
        Execute the operation to generate a vague excuse.

        Args:
            service: The excuse generator service instance.

        Returns:
            str: The generated vague excuse.

        Raises:
            AIServiceError: If AI service fails to generate excuse.
            ConfigurationError: If required API key is not configured.
        """
        get_vague_operation = GetVague(self.request)
        result = await service.excuse_repository.execute(get_vague_operation)
        return result
