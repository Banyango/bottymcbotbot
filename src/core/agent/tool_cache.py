from typing import List, Dict, Type
import inspect

from core.agent.interfaces import Tool
from core.chat.models import FunctionCallToolModel, FunctionModel, ParametersModel, PropertyModel


def get_json_type_from_python_type(kind: str) -> str:
    if kind == int:
        return "integer"
    elif kind == float:
        return "number"
    elif kind == str:
        return "string"
    elif kind == bool:
        return "boolean"
    elif kind == list:
        return "array"
    elif kind == dict:
        return "object"
    else:
        return "string"


def serialize_tool(tool: Type[Tool]) -> FunctionCallToolModel:
    """
    Serialize a Tool into a FunctionCallToolModel.

    Args:
        tool (Tool): The tool to serialize.
    """
    signature = inspect.signature(tool.execute_async)

    params = {}
    required = []
    for name, parameter in signature.parameters.items():
        name = parameter.name
        kind = parameter.annotation

        if name == "self":
            continue

        if parameter.default == inspect.Parameter.empty:
            required.append(name)

        params[name] = PropertyModel(
            type=get_json_type_from_python_type(kind),
            description=f"The {name} parameter"
        )

    return FunctionCallToolModel(
        type="function",
        function=FunctionModel(
            name=type(tool).__name__,
            description=tool.description,
            parameters=ParametersModel(
                type="object",
                required=required,
                properties=params
            ),
        ),
    )


class ToolCache:
    def __init__(self, tools: List[Type[Tool]]):
        self._str_to_tool_map: Dict[str, Type[Tool]] = {
            type(tool).__name__: tool for tool in tools
        }
        self._serialized_tools: List[FunctionCallToolModel] = [
            serialize_tool(tool) for tool in tools
        ]

    def get_tools(self) -> List[FunctionCallToolModel]:
        return self._serialized_tools

    def get_tool_by_name(self, name: str) -> Type[Tool]:
        return self._str_to_tool_map[name]
