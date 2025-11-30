import json
from string import Template
from typing import List, Dict, Any

import aiofiles
from wireup import service

from core.agent.memory import MemoryService
from core.chat.models import ChatMessageModel


@service
class DebuggingMemoryService(MemoryService):
    async def create_initial_messages(self, message_input: str, system_prompt: str, context: Dict[str, Any]) -> List[ChatMessageModel]:
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
            return [
                ChatMessageModel(role="system", content=Template(system_prompt).substitute(context)),
                ChatMessageModel(role="user", content=message_input)
            ]

    async def save_messages(self, messages: List[ChatMessageModel]):
        memory = {
            "messages": [message.__dict__ for message in messages]
        }

        async with aiofiles.open("agent_memory.json", "w", encoding="utf-8") as f:
            # json.dumps is synchronous but small; write asynchronously
            serialized = json.dumps(memory, ensure_ascii=False, indent=2) + "\n"
            await f.write(serialized)
