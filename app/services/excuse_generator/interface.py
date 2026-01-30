"""
Abstract base classes for the excuse generator service layer.

This module defines the interfaces that all service implementations
must follow, implementing the Command pattern for operations.
"""

from abc import ABC, abstractmethod
from typing import TypeVar

from app.repositories.excuse_generator import ExcuseRepositoryABC
from app.services.excuse_generator.operations.interface import (
    ExcuseGeneratorOperationABC,
)

T = TypeVar("T")


class ExcuseGeneratorABC(ABC):
    """
    Abstract base class for excuse generator service.

    This service handles the business logic for generating excuses,
    coordinating between operations and repositories.
    """

    excuse_repository: ExcuseRepositoryABC

    @abstractmethod
    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        """
        Execute a service operation following the Command pattern.

        Args:
            operation: The operation to execute.

        Returns:
            T: The result of the operation.
        """
        pass
