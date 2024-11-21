import asyncio
from typing import NoReturn

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.params import Depends

from src.logger import logger
from src.utils.validators.stream_validators import CompositeStreamValidator
from src.dependencies import get_stream_validator

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
) -> NoReturn:
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            validation_result, validation_msg = stream_validator.validate(message)
            if not validation_result:
                await websocket.send_text(validation_msg)
                continue

            async for text in generate_messages(message):
                await websocket.send_text(text)
    except WebSocketDisconnect:
        logger.debug("Connection Closed")
