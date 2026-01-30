"""Excuse Repository module exports.

This module provides two implementations of the Excuse Repository:
1. AgentExcuseRepository - Uses LLM to dynamically generate excuses
2. PrepopulatedExcuseRepository - Returns excuses from a static list

Example usage:
    from app.repositories.excuse_repository import (
        ExcuseRepositoryABC,
        AgentExcuseRepository,
        PrepopulatedExcuseRepository,
    )
    from app.repositories.excuse_repository.implementations.agent.operations import GetExcuse

    # Using agent-based repository
    repository = AgentExcuseRepository()
    operation = GetExcuse(request="Can you help me move?")
    excuse = await repository.execute(operation)

    # Using prepopulated repository
    repository = PrepopulatedExcuseRepository()
    operation = GetExcuse(request="Can you help me move?")
    excuse = await repository.execute(operation)
"""

from .exceptions import (
    ExcuseGenerationError,
    ExcuseRepositoryException,
    InvalidExcuseRequestError,
)
from .implementations import AgentExcuseRepository, PrepopulatedExcuseRepository
from .interface import ExcuseRepositoryABC, ExcuseRepositoryOperationABC

__all__ = [
    "ExcuseRepositoryABC",
    "ExcuseRepositoryOperationABC",
    "AgentExcuseRepository",
    "PrepopulatedExcuseRepository",
    "ExcuseRepositoryException",
    "ExcuseGenerationError",
    "InvalidExcuseRequestError",
]
