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

    # Using agent-based repository
    repository = AgentExcuseRepository()
    excuse = await repository.get_excuse("Can you help me move?")

    # Using prepopulated repository
    repository = PrepopulatedExcuseRepository()
    excuse = await repository.get_excuse("Can you help me move?")
"""

from .exceptions import (
    ExcuseGenerationError,
    ExcuseRepositoryException,
    InvalidExcuseRequestError,
)
from .implementations import AgentExcuseRepository, PrepopulatedExcuseRepository
from .interface import ExcuseRepositoryABC

__all__ = [
    "ExcuseRepositoryABC",
    "AgentExcuseRepository",
    "PrepopulatedExcuseRepository",
    "ExcuseRepositoryException",
    "ExcuseGenerationError",
    "InvalidExcuseRequestError",
]
