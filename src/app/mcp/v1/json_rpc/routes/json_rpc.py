import json
import uuid
from typing import List

from fastapi import APIRouter
import dataclasses

from starlette.requests import Request
from starlette.responses import Response
from wireup import Injected

from app.mcp.v1.json_rpc.responses.get_prompt import (
    MessageResponse,
    MessageContentResponse,
    GetPromptResponse,
)
from app.mcp.v1.json_rpc.responses.json_rpc import JsonRpcResponse
from app.mcp.v1.json_rpc.responses.list_prompts import (
    PromptResource,
    ListPromptsResponse,
)
from core.mcp.operations.get_prompt_by_name import GetPromptByNameOperation
from core.mcp.operations.initialize_operation import InitializeOperation
from core.mcp.operations.list_prompts_operation import ListPromptsOperation, PromptModel

router = APIRouter()


# todo this needs to be cleaned up.
@router.post("/handle")
async def prompts_jsonrpc(
    request: Request,
    response: Response,
    list_prompts_operation: Injected[ListPromptsOperation],
    get_prompt_operation: Injected[GetPromptByNameOperation],
    initialize_operation: Injected[InitializeOperation],
):
    body = await request.body()
    request_json = json.loads(body)

    if request_json["method"] == "initialize":
        session_id = str(uuid.uuid4())

        model = await initialize_operation.execute_async(
            session_id, request_json["params"]["clientInfo"]["name"]
        )
        result = dataclasses.asdict(model)
        resp = JsonRpcResponse(result=result, id=request_json["id"], jsonrpc="2.0")

        response.headers["Mcp-Session-Id"] = session_id

        return resp.model_dump(exclude_none=True)
    elif request_json["method"] == "notifications/initialized":
        return Response(status_code=202)
    elif request_json["method"] == "prompts/list":
        try:
            session_id = request.headers.get("Mcp-Session-Id")
            prompts: List[PromptModel] = await list_prompts_operation.execute_async(
                session_id
            )
            prompt_resources: List[PromptResource] = []
            for prompt in prompts:
                prompt_resources.append(
                    PromptResource(
                        name=prompt.name,
                        title=prompt.title,
                        description=prompt.description,
                        arguments=[],
                    )
                )

            list_resp = ListPromptsResponse(
                prompts=prompt_resources, next_cursor="next_cursor"
            ).model_dump(exclude_none=True)
            resp = JsonRpcResponse(
                result=list_resp, error=None, id=request_json["id"], jsonrpc="2.0"
            )
            return resp.model_dump(exclude_none=True)
        except ValueError:
            return JsonRpcResponse(
                error={"code": -32000, "message": "Session is invalid or expired"},
                id=request_json["id"],
                jsonrpc="2.0",
            )
    elif request_json["method"] == "prompts/get":
        try:
            models = await get_prompt_operation.execute_async(
                prompt_name=request_json["params"]["name"]
            )
            if models is None:
                error_obj = {"code": -32004, "message": "Prompt not found"}
                resp = JsonRpcResponse(
                    error=error_obj, id=request_json["id"], jsonrpc="2.0"
                )
                return resp.model_dump(exclude_none=True)
            prompt_resources: List[MessageResponse] = []
            for model in models:
                prompt_resources.append(
                    MessageResponse(
                        role="user",
                        content=MessageContentResponse(text=model.content, type="text"),
                    )
                )

            result = GetPromptResponse(
                messages=prompt_resources, description=models[0].description
            )

            return JsonRpcResponse(
                result=result.model_dump(exclude_none=True),
                error=None,
                id=request_json["id"],
                jsonrpc="2.0",
            ).model_dump(exclude_none=True)
        except ValueError:
            return JsonRpcResponse(
                error={"code": -32000, "message": "Session is invalid or expired"},
                id=request_json["id"],
                jsonrpc="2.0",
            )

    # For method not found we MUST return an error object and NOT include `result` per JSON-RPC 2.0
    error_obj = {"code": -32601, "message": "Method not found"}
    resp = JsonRpcResponse(error=error_obj, id=request_json["id"], jsonrpc="2.0")
    return resp.model_dump(exclude_none=True)
