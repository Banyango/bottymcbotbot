from typing import List

from entities.models.prompt_reference import PromptReference


class Collection:
    def __init__(
        self,
        id: str,
        name: str,
        user_id: str,
        client_id: str | None = None,
        prompt_references: List[PromptReference] | None = None,
    ):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.client_id = client_id
        self.prompt_references: List[PromptReference] = (
            prompt_references if prompt_references is not None else []
        )

    @property
    def prompt_ids(self) -> List[str]:
        """Return a list of prompt IDs from the prompt references."""
        return [ref.prompt_id for ref in self.prompt_references]
