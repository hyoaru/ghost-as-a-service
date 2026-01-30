"""
GetVague repository operation.

This operation generates a vague excuse from a prompt using PydanticAI.
"""

from typing import TYPE_CHECKING

from app.exceptions import AIServiceError, ConfigurationError, InvalidRequestError
from app.repositories.excuse_generator.interface import RepositoryOperationABC

if TYPE_CHECKING:
    from app.repositories.excuse_generator.interface import ExcuseRepositoryABC


class GetVague(RepositoryOperationABC[str]):
    """
    Repository operation to generate a vague excuse from a prompt.

    This operation validates the input prompt and calls the PydanticAI agent
    to generate a plausible but meaningless excuse using corporate jargon.

    Raises:
        InvalidRequestError: If prompt is empty or whitespace-only.
        AIServiceError: If AI service fails to generate excuse.
        ConfigurationError: If required API key is not configured.
    """

    def __init__(self, prompt: str):
        """
        Initialize the GetVague operation.

        Args:
            prompt: The request or invitation to generate an excuse for.

        Raises:
            InvalidRequestError: If prompt is empty or whitespace-only.
        """
        if not prompt or not prompt.strip():
            raise InvalidRequestError("Prompt cannot be empty or whitespace-only")

        self.prompt = prompt.strip()

    async def execute(self, repository: "ExcuseRepositoryABC") -> str:
        """
        Execute the operation to generate a vague excuse.

        Args:
            repository: The repository instance with PydanticAI agent.

        Returns:
            str: The generated vague excuse.

        Raises:
            ConfigurationError: If API key is not configured.
            AIServiceError: If AI service fails.
        """
        # Check if API key is configured
        if not repository.settings.GOOGLE_API_KEY:
            raise ConfigurationError("API key is not configured")

        # Call PydanticAI agent to generate excuse
        try:
            result = await repository.agent.run(
                self.prompt,
                model_settings={
                    "api_key": repository.settings.GOOGLE_API_KEY,
                    "temperature": 0.7,
                },
            )
            return result.data
        except Exception as e:
            raise AIServiceError(f"Failed to generate excuse: {str(e)}") from e
