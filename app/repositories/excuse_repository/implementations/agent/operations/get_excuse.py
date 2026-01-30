"""Operation to get an excuse using the agent implementation."""

from app.utilities.excuse_agent.operations.generate_vague import GenerateVague

from ....exceptions import ExcuseGenerationError, InvalidExcuseRequestError
from ....interface import ExcuseRepositoryABC, ExcuseRepositoryOperationABC
from .. import AgentExcuseRepository


class GetExcuse(ExcuseRepositoryOperationABC[str]):
    """Get an excuse from the agent-based repository.

    This operation uses the ExcuseAgent to generate a contextually
    appropriate vague excuse based on the provided request.
    """

    def __init__(self, request: str):
        """Initialize the operation.

        Args:
            request: The invitation or request text to generate an excuse for.

        Raises:
            InvalidExcuseRequestError: If the request is empty or invalid.
        """
        if not request or not request.strip():
            raise InvalidExcuseRequestError("Request text cannot be empty")

        self.request = request.strip()

    async def execute(self, repository: ExcuseRepositoryABC) -> str:
        """Execute the operation to get an excuse.

        Args:
            repository: The repository instance to execute against.

        Returns:
            A generated excuse string.

        Raises:
            TypeError: If the repository is not an AgentExcuseRepository.
            ExcuseGenerationError: If excuse generation fails.
        """
        if not isinstance(repository, AgentExcuseRepository):
            raise TypeError(f"Expected AgentExcuseRepository, got {type(repository).__name__}")

        try:
            operation = GenerateVague()
            excuse = await repository.excuse_agent.execute(operation)
            return excuse
        except Exception as e:
            raise ExcuseGenerationError(f"Failed to generate excuse: {str(e)}") from e
