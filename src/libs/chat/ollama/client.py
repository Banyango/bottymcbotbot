from typing import Union, Sequence, Mapping, Any, List

import ollama

from wireup import service

from core.chat.models import FunctionCallToolModel
from libs.chat.types import ChatResponse, Message
from dataclasses import asdict, is_dataclass


@service
class OllamaAISettings:
    base_url: str = "http://localhost:11434/"
    model: str = "gpt-oss:20b"


@service
class OllamaClient:
    def __init__(self, config: OllamaAISettings):
        self.client = ollama.AsyncClient(config.base_url)
        self.model = config.model

    async def chat_create(
            self,
            messages: Sequence[Union[Mapping[str, Any], Message]],
            tools: List[FunctionCallToolModel]
    ) -> ChatResponse:
        """
        Create a chat completion

        Args:
            messages (Sequence[Union[Mapping[str, Any], Message]]): The messages to send to the chat model.
            tools (List[FunctionCallToolModel]): The tools available for function calling.
        """
        prepared_messages = [asdict(m) if is_dataclass(m) else m for m in messages]
        prepared_tools = [asdict(t) if is_dataclass(t) else t for t in tools]

        response = await self.client.chat(model=self.model, messages=prepared_messages, tools=prepared_tools)

        return ChatResponse(
            message=Message(
                role=response.message.role,
                content=response.message.content,
                thinking=response.message.thinking,
                tool_name=response.message.tool_name,
                tool_calls=response.message.tool_calls
            ),
            done=response.done
        )

    async def chat_with_streaming_response(
            self,
            messages: Sequence[Union[Mapping[str, Any], Message]],
            tools: List[FunctionCallToolModel]
    ):
        """
        Chat with streaming response

        Args:
            messages (Sequence[Union[Mapping[str, Any], Message]]): The messages to send to the chat model.
            tools (List[FunctionCallToolModel]): The tools available for function calling.
        """
        prepared_messages = [asdict(m) if is_dataclass(m) else m for m in messages]
        prepared_tools = [asdict(t) if is_dataclass(t) else t for t in tools]

        return self.client.chat(stream=True, model=self.model, messages=prepared_messages, tools=prepared_tools)
