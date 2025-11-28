from typing import Optional


class PromptEmbedded:
    def __init__(
        self,
        category_id: str,
        category_name: str,
        created_by_name: Optional[str] = None,
        created_by_id: Optional[str] = None,
    ):
        self.category_id = category_id
        self.category_name = category_name
        self.created_by_name: str = created_by_name
        self.created_by_id: str = created_by_id


class Prompt:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        description: str = "",
        category: str = "",
        prompt: str = "",
        model: str = "",
        created_by: str = "",
        readme: Optional[str] = None,
        embedded: Optional[PromptEmbedded] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.readme = readme
        self.prompt = prompt
        self.model = model
        self.created_by = created_by
        self.embedded = embedded
