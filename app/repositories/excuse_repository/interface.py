"""Abstract interface for the Excuse Repository."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class ExcuseRepositoryABC(ABC):
    """Abstract base class defining the Excuse Repository contract.

    Implements the Command Pattern for executing operations against
    excuse data sources.
    """

    @abstractmethod
    async def execute(self, operation: "ExcuseRepositoryOperationABC[T]") -> T:
        """Execute a repository operation.

        Args:
            operation: The operation to execute.

        Returns:
            The result of the operation execution.
        """
        pass


class ExcuseRepositoryOperationABC(ABC, Generic[T]):
    """Abstract base class for repository operations.

    All repository operations must inherit from this class and implement
    the execute method with the appropriate return type.
    """

    @abstractmethod
    async def execute(self, repository: ExcuseRepositoryABC) -> T:
        """Execute the operation against a repository instance.

        Args:
            repository: The repository instance to execute against.

        Returns:
            The operation result with type T.
        """
        pass
