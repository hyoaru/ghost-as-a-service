"""
Abstract base class for service operations.

This module defines the interface that all service operations must follow,
implementing the Command pattern.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from app.services.excuse_generator.interface import ExcuseGeneratorABC

T = TypeVar("T")


class ExcuseGeneratorOperationABC(ABC, Generic[T]):
    """
    Abstract base class for excuse generator operations using the Command pattern.

    Operations encapsulate the logic to execute against a service,
    allowing for modular and testable code.

    Type Parameters:
        T: The return type of the operation.
    """

    @abstractmethod
    async def execute(self, service: "ExcuseGeneratorABC") -> T:
        """
        Execute the operation against the given service.

        Args:
            service: The service instance to execute against.

        Returns:
            T: The result of the operation.
        """
        pass
