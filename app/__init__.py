import asyncio
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext


from app.models import EventModel

logger = Logger()


@logger.inject_lambda_context
@event_parser(model=EventModel)
def handler(event: EventModel, context: LambdaContext) -> dict:
    """
    Lambda handler for excuse generator.

    Args:
        event (EventModel): The validated event model.
        context (LambdaContext): Lambda context object.

    Returns:
        dict: The generated excuse response.
    """
    return asyncio.run(main(event, context))


async def main(event: EventModel, context: LambdaContext) -> dict:
    """
    Main async function for excuse generation Lambda.

    Args:
        event (EventModel): The validated event model.
        context (LambdaContext): Lambda context object.

    Returns:
        dict: The generated excuse response.
    """
    logger.info("Processing request", extra={"request": event.request})
    # TODO: Implement excuse generation logic
    return {"excuse": "Not implemented yet."}
