from typing import List

from app.pydantic import BaseSchema


class MessageContentResponse(BaseSchema):
    type: str
    text: str


class MessageResponse(BaseSchema):
    role: str
    content: MessageContentResponse


class GetPromptResponse(BaseSchema):
    messages: List[MessageResponse]
    description: str
