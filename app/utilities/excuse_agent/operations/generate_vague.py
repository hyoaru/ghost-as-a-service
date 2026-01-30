"""Operation to generate vague technical excuses."""

from .interface import ExcuseAgentOperationABC


class GenerateVague(ExcuseAgentOperationABC[str]):
    """Generates vague, corporate-sounding technical excuses.

    Uses heavy jargon to create plausible-sounding but meaningless
    reasons for unavailability.
    """

    def __init__(self, request: str):
        """Initialize the operation with the request context.

        Args:
            request: The original request or invitation to respond to.
        """
        self.request = request

    async def execute(self, utility) -> str:
        """Generate a vague technical excuse.

        Args:
            utility: The Excuse Agent instance.

        Returns:
            A vague technical excuse string.
        """
        prompt = (
            f"I received this request: '{self.request}'. "
            + "Generate a SHORT, funny excuse (2-3 sentences max) using absurd technical jargon. "
            + "Make it sound urgent and important but hilariously vague. "
            + "Return ONLY the excuse text, no commentary."
        )

        response = await utility.agent.run(prompt)
        return response.output
