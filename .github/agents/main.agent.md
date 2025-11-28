---
description: 'Description of the custom chat mode.'
tools: []
---
# Agents Guide

This document describes the standards and conventions for implementing agents and related components in this project.

## Architecture Overview

This project follows **Clean Architecture** with the following directory structure:

```
src/
├── app/          # Application layer: API endpoints, configurations, containers
├── core/         # Core layer: Business logic, commands, interfaces, models
├── entities/     # Domain entities
└── libs/         # Infrastructure layer: Database repositories, external services
```

### Layer Responsibilities

- **app/**: Application entry points, API routers, FastAPI configuration, and dependency injection
- **core/**: Business logic including commands, queries, interfaces (repositories), and domain models
- **entities/**: Plain domain objects representing core business concepts
- **libs/**: External infrastructure implementations (PostgreSQL repositories, Supabase, sessions)

## Test Naming Convention

Tests should be named following the pattern:

```
function_should_do_when
```

### Examples

- `execute_should_raise_error_when_name_is_missing`
- `list_prompts_should_return_empty_when_no_prompts_exist`
- `create_prompt_should_succeed_when_valid_input_provided`

## Test Structure: Arrange-Act-Assert (AAA)

All tests must follow the Arrange-Act-Assert pattern:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

from core.prompts.commands.add_prompt_command import AddPromptCommand
from core.prompts.models import ModelTypes
from core.exceptions import MissingParameterError


@pytest.mark.asyncio
async def test_execute_should_raise_error_when_name_is_missing():
    # Arrange
    mock_repository = MagicMock()
    command = AddPromptCommand(prompt_repository=mock_repository)

    # Act & Assert
    with pytest.raises(MissingParameterError):
        await command.execute(
            id="123",
            name="",
            description="A test prompt",
            prompt="Test content",
            model=ModelTypes.GPT_4O,
            category_id="cat-1",
        )


@pytest.mark.asyncio
async def test_execute_should_create_prompt_when_valid_input_provided():
    # Arrange
    mock_repository = MagicMock()
    mock_repository.get_prompt_by_name = AsyncMock(return_value=None)
    mock_repository.create_prompt_async = AsyncMock()
    command = AddPromptCommand(prompt_repository=mock_repository)

    # Act
    await command.execute(
        id="123",
        name="My Prompt",
        description="A test prompt",
        prompt="Test content",
        model=ModelTypes.GPT_4O,
        category_id="cat-1",
    )

    # Assert
    mock_repository.create_prompt_async.assert_called_once()
```

### AAA Pattern Guidelines

1. **Arrange**: Set up test fixtures, mocks, and input data
2. **Act**: Execute the code under test
3. **Assert**: Verify the expected outcomes

Use comments to clearly separate these sections for readability.

## Typing Guidelines

Always add type annotations where possible. This project uses Python typing with Pydantic for data validation.

### Interface Definitions

Define interfaces using abstract base classes with the `@abstract` decorator from `wireup`:

```python
from abc import ABC, abstractmethod
from wireup import abstract

from core.collection_model import ItemCollectionModel
from entities.prompt import Prompt


@abstract
class PromptRepository(ABC):
    @abstractmethod
    async def list_prompts(
        self,
        ids: list[str] | None = None,
        names: list[str] | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> ItemCollectionModel[Prompt]:
        """
        List prompts with optional filtering.

        Args:
            ids (list[str] | None): Filter by prompt IDs.
            names (list[str] | None): Filter by prompt names.
            limit (int): Maximum number of results to return.
            offset (int): Number of results to skip.

        Returns:
            ItemCollectionModel[Prompt]: Collection of prompts.
        """
        pass

    @abstractmethod
    async def get_prompt_by_id(self, prompt_id: str) -> Prompt | None:
        """
        Get a prompt by its ID.

        Args:
            prompt_id (str): The unique identifier of the prompt.

        Returns:
            Prompt | None: The prompt if found, None otherwise.
        """
        pass

    @abstractmethod
    async def create_prompt_async(self, prompt: Prompt) -> None:
        """
        Create a new prompt.

        Args:
            prompt (Prompt): The prompt to create.
        """
        pass
```

### Domain Entities

Use type annotations for all class attributes and method parameters:

```python
from typing import Optional


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
    ):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.readme = readme
        self.prompt = prompt
        self.model = model
        self.created_by = created_by
```

### Pydantic Models

Use Pydantic `BaseModel` for API request/response models:

```python
from pydantic import BaseModel


class ListPromptsModel(BaseModel):
    id: str
    name: str
    description: str
    category_id: str
    category_name: str
    model: str
    created_by_id: str
    created_by_name: str


class PagedPromptModel(BaseModel):
    items: list[ListPromptsModel]
    total: int
    offset: int
```

### Type Annotations Best Practices

- Use `str | None` or `Optional[str]` for nullable types
- Use `list[str]` for list types (Python 3.9+ syntax)
- Avoid `Any` - prefer specific types or `object`
- Use generics for container types: `ItemCollectionModel[Prompt]`

## Documentation Style

Follow the docstring conventions used in this project:

```python
class AddPromptCommand:
    """
    Command to add a new prompt to the repository.
    """

    def __init__(self, prompt_repository: PromptRepository):
        self.prompt_repository = prompt_repository

    async def execute(
        self,
        id: str,
        name: str,
        description: str,
        prompt: str,
        model: ModelTypes,
        category_id: str,
        readme: Optional[str] = None,
    ):
        """
        Adds a new prompt to the repository.

        Args:
            id (str): The unique identifier for the prompt.
            name (str): The name of the prompt.
            description (str): The description of the prompt.
            prompt (str): The content of the prompt.
            model (ModelTypes): The model type associated with the prompt.
            category_id (str): The category ID associated with the prompt.
            readme (str | None): The readme content for the prompt.
        """
        # Implementation
```

### Documentation Guidelines

- Use triple-quoted docstrings for classes and methods
- Include an `Args:` section listing all parameters with types and descriptions
- Keep descriptions concise and actionable
- Document public methods; private methods are optional

## File Layout Template

When creating a new feature, follow this structure:

```
src/
├── core/
│   └── {feature}/
│       ├── __init__.py
│       ├── commands/
│       │   ├── __init__.py
│       │   └── add_{feature}_command.py
│       ├── interfaces/
│       │   ├── __init__.py
│       │   └── repository.py
│       ├── models.py
│       └── queries.py
├── entities/
│   └── {feature}.py
├── libs/
│   └── postgres/
│       └── repositories/
│           └── {feature}.py
└── app/
    └── api/
        └── v1/
            └── {feature}/
                ├── __init__.py
                ├── models/
                ├── requests/
                ├── resources/
                └── routers/

tests/
└── core/
    └── {feature}/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── test_add_{feature}_command.py
```

## Linting and Type Checking

Run the following commands to validate code:

```bash
# Format code
make format

# Run linter and type checker
make lint
```

This project uses:
- **ruff**: For linting and formatting
- **pyright**: For static type checking

## Example: Creating a New Agent

### 1. Define the Entity

```python
# src/entities/agent.py
from typing import Optional


class Agent:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        description: str = "",
        config: Optional[dict] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.config = config or {}
```

### 2. Define the Interface

```python
# src/core/agents/interfaces/repository.py
from abc import ABC, abstractmethod
from wireup import abstract

from entities.agent import Agent


@abstract
class AgentRepository(ABC):
    @abstractmethod
    async def get_agent_by_id(self, agent_id: str) -> Agent | None:
        pass

    @abstractmethod
    async def create_agent(self, agent: Agent) -> None:
        pass
```

### 3. Create the Command

```python
# src/core/agents/commands/create_agent_command.py
from typing import Optional

from core.exceptions import MissingParameterError
from core.agents.interfaces.repository import AgentRepository
from entities.agent import Agent


class CreateAgentCommand:
    """
    Command to create a new agent.
    """

    def __init__(self, agent_repository: AgentRepository):
        self.agent_repository = agent_repository

    async def execute(
        self,
        id: str,
        name: str,
        description: str,
        config: Optional[dict] = None,
    ) -> None:
        """
        Creates a new agent in the repository.

        Args:
            id (str): The unique identifier for the agent.
            name (str): The name of the agent.
            description (str): The description of the agent.
            config (dict | None): Optional configuration for the agent.
        """
        if not id:
            raise MissingParameterError("ID parameter is required.")
        if not name:
            raise MissingParameterError("Name parameter is required.")

        agent = Agent(
            id=id,
            name=name,
            description=description,
            config=config,
        )

        await self.agent_repository.create_agent(agent)
```

### 4. Write Tests

```python
# tests/core/agents/commands/test_create_agent_command.py
import pytest
from unittest.mock import AsyncMock, MagicMock

from core.agents.commands.create_agent_command import CreateAgentCommand
from core.exceptions import MissingParameterError


@pytest.mark.asyncio
async def test_execute_should_raise_error_when_id_is_missing():
    # Arrange
    mock_repository = MagicMock()
    command = CreateAgentCommand(agent_repository=mock_repository)

    # Act & Assert
    with pytest.raises(MissingParameterError):
        await command.execute(
            id="",
            name="Test Agent",
            description="A test agent",
        )


@pytest.mark.asyncio
async def test_execute_should_raise_error_when_name_is_missing():
    # Arrange
    mock_repository = MagicMock()
    command = CreateAgentCommand(agent_repository=mock_repository)

    # Act & Assert
    with pytest.raises(MissingParameterError):
        await command.execute(
            id="agent-123",
            name="",
            description="A test agent",
        )


@pytest.mark.asyncio
async def test_execute_should_create_agent_when_valid_input_provided():
    # Arrange
    mock_repository = MagicMock()
    mock_repository.create_agent = AsyncMock()
    command = CreateAgentCommand(agent_repository=mock_repository)

    # Act
    await command.execute(
        id="agent-123",
        name="Test Agent",
        description="A test agent",
        config={"key": "value"},
    )

    # Assert
    mock_repository.create_agent.assert_called_once()
    call_args = mock_repository.create_agent.call_args[0][0]
    assert call_args.id == "agent-123"
    assert call_args.name == "Test Agent"
    assert call_args.config == {"key": "value"}
```

## Common Pitfalls

1. **Missing type annotations**: Always add types to function parameters and return values
2. **Skipping AAA comments**: Include Arrange/Act/Assert comments for test readability
3. **Using `Any` type**: Prefer specific types or `object` over `Any`
4. **Missing docstrings**: Document public classes and methods with Args sections
5. **Incorrect test naming**: Follow `function_should_do_when` pattern

## Related Resources

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
