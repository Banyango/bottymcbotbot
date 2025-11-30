from typing import List, Dict, Type, Optional
import inspect

from core.agent.interfaces import Tool
from core.chat.models import (
    FunctionCallToolModel,
    FunctionModel,
    ParametersModel,
    PropertyModel,
)


def get_json_type_from_python_type(kind: str) -> str:
    """
    Map Python types to JSON schema types.

    Args:
        kind (str): The Python type.

    Returns:
        str: The corresponding JSON schema type.
    """
    if kind is int:
        return "integer"
    elif kind is float:
        return "number"
    elif kind is str:
        return "string"
    elif kind is bool:
        return "boolean"
    elif kind is list:
        return "array"
    elif kind is dict:
        return "object"
    else:
        return "string"


def serialize_tool(tool: Type[Tool]) -> FunctionCallToolModel:
    """Serialize a Tool into a FunctionCallToolModel.

    Args:
        tool (Tool): The tool to serialize.

    Returns:
        FunctionCallToolModel: The serialized tool.
    """
    signature = inspect.signature(tool.execute_async)

    params = {}
    required = []
    for name, parameter in signature.parameters.items():
        name = parameter.name
        kind = parameter.annotation

        if name == "self" or name == "context":
            continue

        if parameter.default == inspect.Parameter.empty:
            required.append(name)

        params[name] = PropertyModel(
            type=get_json_type_from_python_type(kind),
            description=f"The {name} parameter",
        )

    return FunctionCallToolModel(
        type="function",
        function=FunctionModel(
            name=tool.__name__,
            description=tool.description,
            parameters=ParametersModel(
                type="object", required=required, properties=params
            ),
        ),
    )


class ToolsProvider:
    def __init__(self, tools: List[Type[Tool]]):
        self._str_to_tool_map: Dict[str, Type[Tool]] = {
            tool.__name__: tool for tool in tools
        }
        self._serialized_tools: List[FunctionCallToolModel] = [
            serialize_tool(tool) for tool in tools
        ]

    def get_tools(self) -> List[FunctionCallToolModel]:
        """Get the serialized tools.

        Returns:
            List[FunctionCallToolModel]: The list of serialized tools.
        """
        return self._serialized_tools

    def get_tool_by_name(self, name: str) -> Optional[Type[Tool]]:
        """Get a tool class by its name

        Args:
            name (str): The name of the tool.

        Returns:
            Optional[Type[Tool]]: The tool class if found, else None.
        """
        if name not in self._str_to_tool_map:
            return None

        return self._str_to_tool_map[name]
