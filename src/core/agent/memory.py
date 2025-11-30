from abc import ABC, abstractmethod
from typing import List, Dict, Any

from wireup import abstract

from core.chat.models import ChatMessageModel

@abstract
class MemoryService(ABC):
    @abstractmethod
    async def save_messages(self, messages: List[ChatMessageModel]):
        pass

    @abstractmethod
    async def create_initial_messages(self, message_input: str, system_prompt: str, context: Dict[str, Any]) -> List[ChatMessageModel]:
        pass