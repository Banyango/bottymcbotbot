import json
from typing import List

import aiofiles
from wireup import service

from core.interfaces.memory import AgentMemoryService
from core.chat.models import ChatMessageModel
from libs.disk.config import MemoryConfig


@service
class DebuggingAgentMemoryService(AgentMemoryService):
    def __init__(self, config: MemoryConfig):
        self._use_memory = config.use_memory

    async def load_messages(self) -> List[ChatMessageModel] | None:
        if not self._use_memory:
            return None

        try:
            async with aiofiles.open("agent_memory.json", "r", encoding="utf-8") as f:
                content = await f.read()
                memory = json.loads(content)
                messages = [
                    ChatMessageModel(**message_dict)
                    for message_dict in memory.get("messages", [])
                ]
                return messages
        except FileNotFoundError:
            return None

    async def save_messages(self, messages: List[ChatMessageModel]):
        if not self._use_memory:
            return

        memory = {"messages": [message.model_dump() for message in messages]}

        async with aiofiles.open("agent_memory.json", "w", encoding="utf-8") as f:
            # json.dumps is synchronous but small; write asynchronously
            serialized = json.dumps(memory, ensure_ascii=False, indent=2) + "\n"
            await f.write(serialized)
