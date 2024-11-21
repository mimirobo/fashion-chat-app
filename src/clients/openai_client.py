from openai import AsyncOpenAI

from src.app_settings import OpenAISettings


class OpenAIStreamingClient:
    def __init__(self, settings: OpenAISettings):
        self.ai_client = AsyncOpenAI()
        self.settings = settings

    async def stream_responses(self, messages: list):
        stream = await self.ai_client.chat.completions.create(
            model=self.settings.model,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    def stop_streaming(self):
        pass
