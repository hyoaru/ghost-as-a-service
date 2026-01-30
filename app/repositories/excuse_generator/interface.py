"""
Abstract base classes for the excuse generator repository layer.

This module defines the interfaces that all repository implementations
must follow, implementing the Command pattern for operations.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class RepositoryOperationABC(ABC, Generic[T]):
    """
    Abstract base class for repository operations using the Command pattern.

    Operations encapsulate the logic to execute against a repository,
    allowing for modular and testable code.

    Type Parameters:
        T: The return type of the operation.
    """

    @abstractmethod
    async def execute(self, repository: "ExcuseRepositoryABC") -> T:
        """
        Execute the operation against the given repository.

        Args:
            repository: The repository instance to execute against.

        Returns:
            T: The result of the operation.
        """
        pass


class ExcuseRepositoryABC(ABC):
    """
    Abstract base class for excuse generator repository.

    This repository handles interactions with PydanticAI for generating
    vague excuses from prompts.
    """

    @abstractmethod
    async def execute(self, operation: RepositoryOperationABC[T]) -> T:
        """
        Execute a repository operation following the Command pattern.

        Args:
            operation: The repository operation to execute.

        Returns:
            T: The result of the operation.
        """
        pass
