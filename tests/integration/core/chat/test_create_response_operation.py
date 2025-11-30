import os

import pytest
import wireup

import core
import libs
from core.agent.memory import MemoryService
from core.chat.client import ChatClient
from core.agent.operations.create_response_operation import CreateAgentResponseOperation
from libs.disk.services import DebuggingMemoryService


@pytest.mark.asyncio
async def test_create_response_operation():
    # Arrange
    headless_app = wireup.create_async_container(
        service_modules=[
            core,
            libs,
        ]
    )

    chat_client = await headless_app.get(ChatClient)
    memory_service = await headless_app.get(MemoryService)

    _sut = CreateAgentResponseOperation(client=chat_client, container=headless_app, memory_service=memory_service)

    # Act
    response = await _sut.execute_async(
        """
        Fix the following error in the code:
         /src/libs/chat/chat.py:29:15 - error: Method "stream" overrides class "ChatClient" in an incompatible manner
  Return type mismatch: base method returns type "CoroutineType[Any, Any, AsyncIterator[str]]", override returns type "AsyncIterator[str]"
  "AsyncIterator[str]" is not assignable to "CoroutineType[Any, Any, AsyncIterator[str]]" (reportIncompatibleMethodOverride)
        """,
        context={"project_root": os.path.abspath(".")}
    )

    # Assert
    assert response is not None
    print(response)
