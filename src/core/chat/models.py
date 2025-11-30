from dataclasses import dataclass
from typing import Literal, Optional, Dict, Any, List, Union

from pydantic.json_schema import JsonSchemaValue

Role = Literal["system", "user", "assistant", "tool"]


@dataclass
class ChatMessageModel:
    role: Role
    content: str
    thinking: Optional[str] = None
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tool_name: Optional[str] = None


@dataclass
class ChatOptionsModel:
    model: str
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    format: Optional[Union[Literal["", "json"], JsonSchemaValue]] = None
    think: Optional[bool] = None
    stop: Optional[List[str]] = None


@dataclass
class PropertyModel:
    type: str
    description: Optional[str]


@dataclass
class ParametersModel:
    type: Literal["object"]
    required: List[str]
    properties: Dict[str, PropertyModel]


@dataclass
class FunctionModel:
    name: str
    description: Optional[str]
    parameters: ParametersModel


@dataclass
class FunctionCallToolModel:
    type: Literal["function"]
    function: FunctionModel
