from app.pydantic import BaseSchema


class PromptsJsonRpc(BaseSchema):
    jsonrpc: str
    id: int | str | None
    method: str
    params: dict | None
