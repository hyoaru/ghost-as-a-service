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
    from app.models import ExcuseResponse
    from app.services.excuse_generator import ExcuseGeneratorService
    from app.services.excuse_generator.operations import GenerateExcuse
    from app.services.excuse_generator.exceptions import (
        InvalidRequestError,
        ServiceGenerationError,
    )

    logger.info("Processing excuse generation request", extra={"request": event.request})

    try:
        # Initialize service with default repository (AgentExcuseRepository)
        service = ExcuseGeneratorService()

        # Create and execute operation
        operation = GenerateExcuse(request=event.request)
        excuse_text = await service.execute(operation)

        # Build response
        response = ExcuseResponse(excuse=excuse_text)

        logger.info(
            "Successfully generated excuse",
            extra={"request_id": context.request_id, "excuse_length": len(excuse_text)},
        )

        return response.model_dump()

    except InvalidRequestError as e:
        logger.error(
            "Invalid request error",
            extra={"error": str(e), "request_id": context.request_id},
        )
        return {
            "statusCode": 400,
            "body": {"error": "Invalid request", "message": str(e)},
        }

    except ServiceGenerationError as e:
        logger.error(
            "Service generation error",
            extra={"error": str(e), "request_id": context.request_id},
        )
        return {
            "statusCode": 500,
            "body": {"error": "Excuse generation failed", "message": str(e)},
        }

    except Exception as e:
        logger.exception(
            "Unexpected error during excuse generation",
            extra={"error": str(e), "request_id": context.request_id},
        )
        return {
            "statusCode": 500,
            "body": {"error": "Internal server error", "message": "An unexpected error occurred"},
        }
