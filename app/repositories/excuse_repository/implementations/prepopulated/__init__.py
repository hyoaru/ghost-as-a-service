"""Prepopulated implementation of the Excuse Repository.

This implementation returns excuses from a predefined list without making
external API calls. Useful for testing, development, or rate-limited scenarios.
"""

import random
from typing import Optional, TypeVar

from ...interface import ExcuseRepositoryABC, ExcuseRepositoryOperationABC
from .settings import Settings

T = TypeVar("T")


class PrepopulatedExcuseRepository(ExcuseRepositoryABC):
    """Prepopulated excuse repository using a static list of excuses.

    This repository implementation provides fast, deterministic excuse
    retrieval without requiring external LLM API calls.
    """

    def __init__(self, settings: Optional[Settings] = None):
        """Initialize the prepopulated repository.

        Args:
            settings: Optional Settings instance. If not provided,
                loads from environment.
        """
        self.settings = settings or Settings()
        self.excuses = self.settings.PREPOPULATED_EXCUSES
        random.seed()

    async def execute(self, operation: ExcuseRepositoryOperationABC[T]) -> T:
        """Execute a repository operation.

        Args:
            operation: The operation to execute.

        Returns:
            The result of the operation execution.
        """
        return await operation.execute(self)
