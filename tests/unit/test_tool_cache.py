from core.agent.tool_cache import ToolCache
from core.agent.interfaces import Tool


class FakeTool(Tool):
    description = "A fake tool for testing"

    async def execute_async(
        self,
        count: int,
        name: str = "bob",
        active: bool = True,
        data: dict = None,
        items: list = None,
    ):
        """A simple async method used to test signature serialization."""
        return None


def test_get_tools_should_return_serialized_tool():
    # Arrange
    tool_cache = ToolCache([FakeTool])

    # Act
    tools = tool_cache.get_tools()

    # Assert
    assert tools[0].function is not None
    assert tools[0].function.name == "FakeTool"
    assert tools[0].function.description == "A fake tool for testing"
    assert tools[0].function.parameters is not None
    assert tools[0].function.parameters.type == "object"

    assert set(tools[0].function.parameters.required) == {"count"}

    assert len(tools[0].function.parameters.properties) == 5

    assert tools[0].function.parameters.properties["count"].type == "integer"
    assert tools[0].function.parameters.properties["name"].type == "string"
    assert tools[0].function.parameters.properties["active"].type == "boolean"
    assert tools[0].function.parameters.properties["data"].type == "object"
    assert tools[0].function.parameters.properties["items"].type == "array"


def test_get_tool_by_name_should_return_tool_when_name_is_valid():
    # Arrange
    tool_cache = ToolCache([FakeTool])

    # Act
    tools = tool_cache.get_tool_by_name("FakeTool")

    # Assert
    assert tools == FakeTool


def test_get_tool_by_name_should_raise_key_error_when_name_is_invalid():
    # Arrange
    tool_cache = ToolCache([FakeTool])

    # Act / Assert
    try:
        tool_cache.get_tool_by_name("NonExistentTool")
        assert False, "Expected KeyError was not raised"
    except KeyError:
        pass
