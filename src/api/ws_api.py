from typing import NoReturn

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.params import Depends

from src.logger import logger
from src.services.client_manager import WebSocketConnectionManager
from src.services.intent_classifier import IntentClassifierService
from src.utils.openai_query_build import OpenAIQueryBuild
from src.utils.validators.stream_validators import CompositeStreamValidator
from src.dependencies import (
    get_stream_validator,
    get_connection_manager,
    get_openai_client,
    get_openai_query_builder,
    get_intent_classifier,
    get_app_settings,
)

router = APIRouter()
settings = get_app_settings()


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    stream_validator: CompositeStreamValidator = Depends(get_stream_validator),
    connection_manager: WebSocketConnectionManager = Depends(get_connection_manager),
    query_builder: OpenAIQueryBuild = Depends(get_openai_query_builder),
    intent_classifier: IntentClassifierService = Depends(get_intent_classifier),
) -> NoReturn:
    # generate a new openai client
    ai_client = get_openai_client()
    # cache the client
    await connection_manager.connect(websocket, ai_client)
    try:
        while True:
            user_query = await websocket.receive_text()
            # validate the stream for security
            validation_result, validation_msg = stream_validator.validate(user_query)
            if not validation_result:
                await websocket.send_text(validation_msg)
                continue

            # validate if the indent of the user's query align with the topics of the app i.e. fashion
            intent_result, _ = await intent_classifier.is_text_pertinent(
                user_query, settings.intent_classifier.candidate_labels
            )
            if not intent_result:
                logger.warning("irrelevant intent")
                await websocket.send_text(
                    "It looks like the topic you are talking about is irrelevant to fashion!"
                )
                continue

            # build the openai query
            openai_query = query_builder.build(user_query)
            # Get the OpenAI client associated with this WebSocket
            openai_client = connection_manager.get_ai_client(websocket)

            # Stream responses from OpenAI and send them to the client
            async for chunk in openai_client.stream_responses(openai_query):
                if chunk:  # Only send non-empty chunks
                    await connection_manager.send_message(websocket, chunk)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        logger.debug("Connection Closed")
    except Exception:
        logger.error("Error in websocket!", exc_info=True)
        await websocket.send_text("Sorry! There's a problem from our side.")
