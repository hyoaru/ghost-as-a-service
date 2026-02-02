"""Prepopulated implementation of the Excuse Repository.

This implementation returns excuses from a predefined list without making
external API calls. Useful for testing, development, or rate-limited scenarios.
"""

import random
from typing import Optional

from ...interface import ExcuseRepositoryABC
from ...exceptions import ExcuseGenerationError, InvalidExcuseRequestError
from .settings import Settings


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

    async def get_excuse(self, request: str) -> str:
        """Get an excuse for the given request.

        Args:
            request: The invitation or request text (validated but not used for selection).

        Returns:
            A randomly selected excuse from the prepopulated list.

        Raises:
            InvalidExcuseRequestError: If the request is empty or invalid.
            ExcuseGenerationError: If the excuse list is empty or selection fails.
        """
        if not request or not request.strip():
            raise InvalidExcuseRequestError("Request text cannot be empty")

        if not self.excuses:
            raise ExcuseGenerationError("No excuses available in prepopulated list")

        try:
            return random.choice(self.excuses)
        except Exception as e:
            raise ExcuseGenerationError(f"Failed to select excuse: {e}") from e
