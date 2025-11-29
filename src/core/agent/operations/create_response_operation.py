from wireup import AsyncContainer

from core.agent.agent import Agent
from core.agent.tool_cache import ToolCache

from core.chat.client import ChatClient

from core.code.tools.add_file import AddFile
from core.code.tools.list_dir import ListDir
from core.code.tools.modify_file import ModifyFile
from core.code.tools.read_file import ReadFile


class CreateAgentResponseOperation:
    def __init__(self, client: ChatClient, container: AsyncContainer):
        self.client = client
        self.container = container

    async def execute_async(self, message: str) -> str:
        """
        Execute the operation to create an agent response.

        Args:
            message (str): The input message for the agent.
        """
        agent = Agent(
            chat_client=self.client,
            tools=ToolCache([AddFile, ModifyFile, ReadFile, ListDir]),
            container=self.container,
        )

        return await agent.run_async(message)
