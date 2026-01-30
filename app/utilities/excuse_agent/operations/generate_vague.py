"""Operation to generate vague technical excuses."""

from .interface import ExcuseAgentOperationABC


class GenerateVague(ExcuseAgentOperationABC[str]):
    """Generates vague, corporate-sounding technical excuses.

    Uses heavy jargon to create plausible-sounding but meaningless
    reasons for unavailability.
    """

    async def execute(self, utility) -> str:
        """Generate a vague technical excuse.

        Args:
            utility: The Excuse Agent instance.

        Returns:
            A vague technical excuse string.
        """
        prompt = (
            "I need an immensely vague 'Technical Fog' excuse." 
            + "Use heavy, confusing jargon so that the recipient doesn't understand the problem but feels it's too critical to question. "
            + "Make me sound stressed, professional, and too busy to explain further."
        )

        response = await utility.agent.run(prompt)
        return response
