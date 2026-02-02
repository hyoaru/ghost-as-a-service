"""Agent-based implementation of the Excuse Repository.

This implementation uses the ExcuseAgent utility to dynamically generate
excuses via LLM on demand.
"""

from typing import Optional

from app.utilities.excuse_agent import ExcuseAgent
from app.utilities.excuse_agent.operations.generate_vague import GenerateVague

from ...interface import ExcuseRepositoryABC
from ...exceptions import ExcuseGenerationError, InvalidExcuseRequestError
from .settings import Settings


class AgentExcuseRepository(ExcuseRepositoryABC):
    """Agent-based excuse repository using LLM for dynamic generation.

    This repository implementation leverages the ExcuseAgent utility
    to generate contextually appropriate excuses in real-time.
    """

    def __init__(
        self,
        excuse_agent: Optional[ExcuseAgent] = None,
        settings: Optional[Settings] = None,
    ):
        """Initialize the agent-based repository.

        Args:
            excuse_agent: Optional ExcuseAgent instance. If not provided,
                creates a new one with default configuration.
            settings: Optional Settings instance. If not provided,
                loads from environment.
        """
        self.excuse_agent = excuse_agent or ExcuseAgent()
        self.settings = settings or Settings()

    async def get_excuse(self, request: str) -> str:
        """Get an excuse for the given request.

        Args:
            request: The invitation or request text to generate an excuse for.

        Returns:
            A generated excuse string.

        Raises:
            InvalidExcuseRequestError: If the request is empty or invalid.
            ExcuseGenerationError: If excuse generation fails.
        """
        if not request or not request.strip():
            raise InvalidExcuseRequestError("Request text cannot be empty")

        try:
            operation = GenerateVague(request=request.strip())
            excuse = await self.excuse_agent.execute(operation)
            return excuse
        except InvalidExcuseRequestError:
            raise
        except Exception as e:
            raise ExcuseGenerationError(f"Failed to generate excuse: {e}") from e
