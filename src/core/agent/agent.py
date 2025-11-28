from wireup import AsyncContainer

from core.agent.tool_cache import ToolCache
from core.chat.client import ChatClient
from core.chat.models import ChatMessageModel, ChatOptionsModel


class Agent:
    def __init__(
        self, chat_client: ChatClient, container: AsyncContainer, tools: ToolCache
    ):
        self.chat_client = chat_client
        self.container = container
        self.tools = tools

    async def run_async(self, message_input: str) -> str:
        """
        Run the agent with the given message_input.

        Args:
            message_input (str): The input string to process.
        """
        messages = [ChatMessageModel(role="user", content=message_input)]
        while True:
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

                    klass = await self.container.get(self.tools.get_tool_by_name(function_name))

                    tool_response = await klass.execute_async(**function_args)

                    if tool_response is None:
                        tool_response = ""

                    messages.append(ChatMessageModel(role="tool", content=tool_response or "", tool_name=function_name))
            else:
                return response.message.content or ""

        return "No response generated."
