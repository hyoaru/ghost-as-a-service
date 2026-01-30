"""Excuse Generator Service module exports.

This module provides the core service for generating excuses based on
incoming requests. It orchestrates the repository layer to generate
appropriate, contextually vague excuses.

Example usage:
    from app.services.excuse_generator import (
        ExcuseGeneratorService,
        ExcuseGeneratorServiceABC,
    )
    from app.services.excuse_generator.operations import GenerateExcuse

    # Create service with default repository
    service = ExcuseGeneratorService()

    # Generate an excuse
    operation = GenerateExcuse(request="Can you help me move this weekend?")
    excuse = await service.execute(operation)
"""

from typing import Optional, TypeVar

from app.repositories.excuse_repository import AgentExcuseRepository, ExcuseRepositoryABC

from .interface import ExcuseGeneratorOperationABC, ExcuseGeneratorServiceABC

T = TypeVar("T")


class ExcuseGeneratorService(ExcuseGeneratorServiceABC):
    """Service for orchestrating excuse generation.

    This service coordinates the business logic for generating excuses,
    managing dependencies and delegating to the appropriate repository
    implementation.
    """

    repository: ExcuseRepositoryABC

    def __init__(self, repository: Optional[ExcuseRepositoryABC] = None):
        """Initialize the service with optional dependency injection.

        Args:
            repository: Optional repository instance. If not provided,
                defaults to AgentExcuseRepository for dynamic generation.
        """
        self.repository = repository or AgentExcuseRepository()

    async def execute(self, operation: ExcuseGeneratorOperationABC[T]) -> T:
        """Execute a service operation.

        Args:
            operation: The operation to execute.

        Returns:
            The result of the operation execution.
        """
        return await operation.execute(self)


__all__ = [
    "ExcuseGeneratorService",
    "ExcuseGeneratorServiceABC",
    "ExcuseGeneratorOperationABC",
]
