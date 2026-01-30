"""
Excuse generator service.

This module exports the excuse generator service interface and concrete
implementation.
"""

from typing import Optional, TypeVar

from app.repositories.excuse_generator import ExcuseRepository, ExcuseRepositoryABC
from app.services.excuse_generator.interface import ExcuseGeneratorABC
from app.services.excuse_generator.operations.interface import (
    ExcuseGeneratorOperationABC,
)

T = TypeVar("T")


class ExcuseGenerator(ExcuseGeneratorABC):
    """
    Concrete implementation of the excuse generator service.

    This service coordinates the business logic for generating excuses,
    managing the excuse repository and executing operations following
    the Command pattern.

    Attributes:
        excuse_repository: The repository for generating excuses.
    """

    excuse_repository: ExcuseRepositoryABC

    def __init__(self, excuse_repository: Optional[ExcuseRepositoryABC] = None):
        """
        Initialize the ExcuseGenerator service.

        Args:
            excuse_repository: The repository instance. If None, creates
                              a default ExcuseRepository.
        """
        self.excuse_repository = excuse_repository or ExcuseRepository()

    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        """
        Execute a service operation following the Command pattern.

        Args:
            operation: The operation to execute.

        Returns:
            T: The result of the operation.
        """
        return await operation.execute(self)


__all__ = ["ExcuseGeneratorABC", "ExcuseGenerator"]
