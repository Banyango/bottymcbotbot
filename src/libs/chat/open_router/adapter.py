import json
from typing import Union, Sequence, Mapping, Any, List, Optional, Literal

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolUnionParam, \
    ChatCompletionFunctionToolParam
from openai.types.shared_params import FunctionDefinition, ResponseFormatJSONSchema
from openai.types.shared_params.response_format_json_schema import JSONSchema
from pydantic.json_schema import JsonSchemaValue

from wireup import service

from core.chat.models import FunctionCallToolModel

from libs.chat.model_adapter import ModelAdapter
from libs.chat.open_router.config import OpenRouterSettings
from libs.chat.types import ChatResponse, Message, ToolCall, Function

from dataclasses import asdict, is_dataclass


@service
class OpenRouterAdapter(ModelAdapter):
    def __init__(self, config: OpenRouterSettings):
        self.client = AsyncOpenAI(base_url=config.base_url, api_key=config.api_key)
        self.model = config.model

    async def chat_create(
        self,
        messages: Sequence[Union[Mapping[str, Any], Message]],
        tools: List[FunctionCallToolModel],
        format: Optional[Union[Literal["", "json"], JsonSchemaValue]],
        think: Optional[bool] = None,
    ) -> ChatResponse:
        """
        Create a chat completion

        Args:
            messages (Sequence[Union[Mapping[str, Any], Message]]): The messages to send to the chat model.
            tools (List[FunctionCallToolModel]): The tools available for function calling.
            format (Optional[Union[Literal['', 'json'], JsonSchemaValue]]): The format for the response.
            think (Optional[bool]): Whether to enable thinking mode.
        """
        if tools is None:
            tools = []

        prepared_messages = [ChatCompletionMessageParam(content=m.content, tool_calls=m.tool_calls, role=m.role).model_dump_json() if is_dataclass(m) else m for m in messages]
        prepared_tools = [ChatCompletionFunctionToolParam(
            function=FunctionDefinition(name=t.function.name, description=t.function.description, parameters=asdict(t.function.parameters)), type=t.type) if is_dataclass(t) else t for t in tools]

        response = await self.client.chat.completions.create(
            messages=prepared_messages,
            model=self.model,
            tools=prepared_tools,
            extra_body={"reasoning": {"enabled": True}},
        )

        parsed_tool_calls = []
        for tool_call in response.choices[0].message.tool_calls or []:
            parsed_tool_calls.append(ToolCall(
                id=tool_call.id,
                function=Function(
                    name=tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments)
                )
            ))

        return ChatResponse(
            message=Message(
                role=response.choices[0].message.role,
                content=response.choices[0].message.content,
                tool_calls=parsed_tool_calls,
            ),
            done=response.choices[0].finish_reason == "stop",
        )

    async def chat_with_streaming_response(
        self,
        messages: Sequence[Union[Mapping[str, Any], Message]],
        tools: List[FunctionCallToolModel],
        format: Optional[Union[Literal["", "json"], JsonSchemaValue]] = None,
        think: Optional[bool] = None,
    ):
        """
        Chat with streaming response

        Args:
            messages (Sequence[Union[Mapping[str, Any], Message]]): The messages to send to the chat model.
            tools (List[FunctionCallToolModel]): The tools available for function calling.
            format (Optional[Union[Literal['', 'json'], JsonSchemaValue]]): The format for the response.
            think (Optional[bool]): Whether to enable thinking mode.
        """
        prepared_messages = [asdict(m) if is_dataclass(m) else m for m in messages]
        prepared_tools = [asdict(t) if is_dataclass(t) else t for t in tools]

        return None
