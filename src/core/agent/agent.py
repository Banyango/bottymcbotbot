import inspect
from typing import Dict, Any

from wireup import AsyncContainer

from core.agent.memory import MemoryService
from core.agent.tool_cache import ToolCache
from core.chat.client import ChatClient
from core.chat.models import ChatMessageModel, ChatOptionsModel


class Agent:
    def __init__(
        self,
            chat_client: ChatClient,
            container: AsyncContainer,
            tools: ToolCache,
            system_prompt: str,
            memory: MemoryService,
    ):
        self.chat_client = chat_client
        self.container = container
        self.tools = tools
        self.system_prompt = system_prompt
        self.memory = memory

    async def run_async(self, message_input: str, context: Dict[str, Any]) -> str:
        """
        Run the agent with the given message_input.

        Args:
            message_input (str): The input string to process.
            context (Dict[str, Any]): Additional context for the agent that will be passed to all tools.
        """
        messages = await self.memory.create_initial_messages(message_input, self.system_prompt, context)

        while True:
            await self.memory.save_messages(messages)

            response = await self.chat_client.chat(
                messages=messages,
                tools=self.tools.get_tools(),
                options=ChatOptionsModel(
                    model="gpt-os:20b",
                    temperature=0.7,
                ),
            )

            if response is None:
                break

            if response.message.tool_calls is not None:
                for tool_call in response.message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = tool_call.function.arguments

                    klass_name = self.tools.get_tool_by_name(function_name)
                    if klass_name is None:
                        messages.append(
                            ChatMessageModel(
                                role="tool",
                                content=f"Tool {function_name} not found.",
                                tool_name=function_name,
                            )
                        )
                        continue

                    klass = await self.container.get(klass_name)

                    sig = inspect.signature(klass.execute_async)
                    parameters = sig.parameters
                    filtered_function_args = {}
                    for arg_name, arg_value in function_args.items():
                        if arg_name in parameters.keys():
                            filtered_function_args[arg_name] = arg_value

                    tool_response = await klass.execute_async(context=context, **filtered_function_args)

                    if tool_response is None:
                        tool_response = ""

                    messages.append(
                        ChatMessageModel(
                            role="tool",
                            content=tool_response or "",
                            tool_name=function_name,
                        )
                    )
            else:
                return response.message.content or ""

        return "No response generated."
