"""Operation to generate an excuse using the Excuse Generator Service."""

from app.repositories.excuse_repository.exceptions import (
    ExcuseGenerationError,
    InvalidExcuseRequestError,
)

from ..exceptions import InvalidRequestError, ServiceGenerationError
from ..interface import ExcuseGeneratorOperationABC, ExcuseGeneratorServiceABC


class GenerateExcuse(ExcuseGeneratorOperationABC[str]):
    """Generate a vague, professional excuse for a given request.

    This operation coordinates with the repository layer to generate
    contextually appropriate excuses that are plausible yet deliberately vague.
    """

    def __init__(self, request: str):
        """Initialize the operation with a request.

        Args:
            request: The invitation or request text to generate an excuse for.

        Raises:
            InvalidRequestError: If the request is empty or invalid.
        """
        if not request or not request.strip():
            raise InvalidRequestError("Request text cannot be empty")

        self.request = request.strip()

    async def execute(self, service: ExcuseGeneratorServiceABC) -> str:
        """Execute the operation to generate an excuse.

        Args:
            service: The service instance providing orchestration context.

        Returns:
            A generated excuse string.

        Raises:
            ServiceGenerationError: If excuse generation fails at any layer.
        """
        try:
            excuse = await service.repository.get_excuse(self.request)
            return excuse

        except InvalidExcuseRequestError as e:
            raise InvalidRequestError(f"Invalid request: {str(e)}") from e

        except ExcuseGenerationError as e:
            raise ServiceGenerationError(f"Failed to generate excuse: {str(e)}") from e

        except Exception as e:
            raise ServiceGenerationError(
                f"Unexpected error during excuse generation: {str(e)}"
            ) from e
