"""Abstract interface for the Excuse Generator Service."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.repositories.excuse_repository.interface import ExcuseRepositoryABC

T = TypeVar("T")


class ExcuseGeneratorServiceABC(ABC):
    """Abstract base class defining the Excuse Generator Service contract.

    Implements the Command Pattern for orchestrating excuse generation
    business logic across repositories and utilities.
    """

    repository: ExcuseRepositoryABC

    @abstractmethod
    async def execute(self, operation: "ExcuseGeneratorOperationABC[T]") -> T:
        """Execute a service operation.

        Args:
            operation: The operation to execute.

        Returns:
            The result of the operation execution.
        """
        pass


class ExcuseGeneratorOperationABC(ABC, Generic[T]):
    """Abstract base class for service operations.

    All service operations must inherit from this class and implement
    the execute method with the appropriate return type.
    """

    @abstractmethod
    async def execute(self, service: ExcuseGeneratorServiceABC) -> T:
        """Execute the operation against a service instance.

        Args:
            service: The service instance providing orchestration context.

        Returns:
            The operation result with type T.
        """
        pass
