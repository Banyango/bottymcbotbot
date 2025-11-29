from abc import ABC, abstractmethod


class Tool(ABC):
    description: str

    @abstractmethod
    async def execute_async(self, *args, **kwargs) -> str:
        pass
