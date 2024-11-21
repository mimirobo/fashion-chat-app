from fastapi import WebSocket

from src.clients.openai_client import OpenAIStreamingClient


class WebSocketConnectionManager:
    def __init__(self):
        # A dictionary to store WebSocket connections mapped to OpenAIStreamingClient instances
        self.active_connections: dict[WebSocket, OpenAIStreamingClient] = {}

    async def connect(self, websocket: WebSocket, ai_client: OpenAIStreamingClient):
        """
        Accept a new WebSocket connection and associate it with a new OpenAIStreamingClient instance.
        """
        await websocket.accept()
        self.active_connections[websocket] = ai_client

    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection and its associated OpenAIStreamingClient instance.
        """
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def send_message(self, websocket: WebSocket, message: str):
        """
        Send a message to a specific WebSocket client.
        """
        if websocket in self.active_connections:
            await websocket.send_text(message)

    def get_ai_client(self, websocket: WebSocket) -> OpenAIStreamingClient:
        """
        Retrieve the OpenAIStreamingClient instance associated with a WebSocket.
        """
        return self.active_connections.get(websocket)
