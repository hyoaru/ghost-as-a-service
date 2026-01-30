"""Operation to get an excuse using the prepopulated implementation."""

import random

from ....exceptions import ExcuseGenerationError, InvalidExcuseRequestError
from ....interface import ExcuseRepositoryABC, ExcuseRepositoryOperationABC
from .. import PrepopulatedExcuseRepository


class GetExcuse(ExcuseRepositoryOperationABC[str]):
    """Get an excuse from the prepopulated repository.

    This operation randomly selects an excuse from the prepopulated list.
    The request text is validated but not used in selection.
    """

    def __init__(self, request: str):
        """Initialize the operation.

        Args:
            request: The invitation or request text (validated but not used).

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
            A randomly selected excuse from the prepopulated list.

        Raises:
            TypeError: If the repository is not a PrepopulatedExcuseRepository.
            ExcuseGenerationError: If the excuse list is empty or selection fails.
        """
        if not isinstance(repository, PrepopulatedExcuseRepository):
            raise TypeError(
                f"Expected PrepopulatedExcuseRepository, got {type(repository).__name__}"
            )

        if not repository.excuses:
            raise ExcuseGenerationError("No excuses available in prepopulated list")

        try:
            excuse = random.choice(repository.excuses)
            return excuse
        except Exception as e:
            raise ExcuseGenerationError(f"Failed to retrieve excuse: {str(e)}") from e
