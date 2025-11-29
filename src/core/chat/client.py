from abc import ABC, abstractmethod
from typing import Iterable, AsyncIterator, List

from wireup import abstract

from core.chat.models import ChatOptionsModel, ChatMessageModel, FunctionCallToolModel
from libs.chat.types import ChatResponse


@abstract
class ChatClient(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: Iterable[ChatMessageModel],
        options: ChatOptionsModel,
        tools: List[FunctionCallToolModel],
    ) -> ChatResponse:
        pass

    @abstractmethod
    async def stream(
        self,
        messages: Iterable[ChatMessageModel],
        options: ChatOptionsModel,
        tools: List[FunctionCallToolModel],
    ) -> AsyncIterator[str]:
        pass
