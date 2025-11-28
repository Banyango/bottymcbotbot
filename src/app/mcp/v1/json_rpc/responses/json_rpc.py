from typing import Optional

from app.pydantic import BaseSchema


class JsonRpcResponse(BaseSchema):
    jsonrpc: str
    id: Optional[int | str] = None
    error: Optional[dict] = None
    result: Optional[dict] = None
