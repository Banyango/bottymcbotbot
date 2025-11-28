from typing import List, Dict

from app.pydantic import BaseSchema


class PromptResource(BaseSchema):
    name: str
    title: str
    description: str
    arguments: List[dict]


class ListPromptsResponse(BaseSchema):
    prompts: List[PromptResource]
    next_cursor: str | None
