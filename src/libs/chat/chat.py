from dataclasses import asdict
from typing import Iterable, AsyncIterator, List

from wireup import service

from core.chat.client import ChatClient
from core.chat.models import ChatMessageModel, ChatOptionsModel, FunctionCallToolModel
from libs.chat.ollama.client import OllamaClient
from libs.chat.types import ChatResponse


@service
class MultiModelChatClient(ChatClient):
    def __init__(self, client: OllamaClient):
        self._client = client

    async def chat(
            self,
            messages: Iterable[ChatMessageModel],
            options: ChatOptionsModel,
            tools: List[FunctionCallToolModel],
    ) -> ChatResponse:
        payload_messages = [asdict(m) | {"content": m.content} for m in messages]
        response = await self._client.chat_create(messages=payload_messages, tools=tools)
        return response

    async def stream(
            self, messages: Iterable[ChatMessageModel], options: ChatOptionsModel,
            tools: List[FunctionCallToolModel],
    ) -> AsyncIterator[str]:
        payload_messages = [asdict(m) | {"content": m.content} for m in messages]
        async with self._client.chat_with_streaming_response(
                messages=payload_messages, tools=tools
        ) as stream:
            for event in stream.iter_lines():
                yield event
