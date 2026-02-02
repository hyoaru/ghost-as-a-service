"""Abstract interface for the Excuse Repository."""

from abc import ABC, abstractmethod


class ExcuseRepositoryABC(ABC):
    """Abstract base class defining the Excuse Repository contract.

    Repositories provide direct methods for data access operations.
    """

    @abstractmethod
    async def get_excuse(self, request: str) -> str:
        """Get an excuse for the given request.

        Args:
            request: The invitation or request text to generate an excuse for.

        Returns:
            A generated or retrieved excuse string.

        Raises:
            InvalidExcuseRequestError: If the request is empty or invalid.
            ExcuseGenerationError: If excuse retrieval fails.
        """
        pass
