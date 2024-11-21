import asyncio
from typing import NoReturn

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.params import Depends

from src.logger import logger
from src.services.client_manager import WebSocketConnectionManager
from src.utils.openai_query_build import OpenAIQueryBuild
from src.utils.validators.stream_validators import CompositeStreamValidator
from src.dependencies import (
    get_stream_validator,
    get_connection_manager,
    get_openai_client,
    get_openai_query_builder,
)

router = APIRouter()


async def generate_messages(message):
    messages = ["you", "said", message]
    for message in messages:
        await asyncio.sleep(0.1)  # Simulate asynchronous operation
        yield message


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    stream_validator: CompositeStreamValidator = Depends(get_stream_validator),
    connection_manager: WebSocketConnectionManager = Depends(get_connection_manager),
    query_builder: OpenAIQueryBuild = Depends(get_openai_query_builder),
) -> NoReturn:
    ai_client = get_openai_client()
    await connection_manager.connect(websocket, ai_client)
    try:
        while True:
            user_query = await websocket.receive_text()
            validation_result, validation_msg = stream_validator.validate(user_query)
            if not validation_result:
                await websocket.send_text(validation_msg)
                continue

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
    except Exception as e:
        logger.error("Error in websocket!", exc_info=e)
        await websocket.send_text("Sorry! There's a problem from our side.")
