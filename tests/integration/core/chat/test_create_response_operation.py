import pytest
import wireup

import core
import libs
from core.chat.client import ChatClient
from core.agent.operations.create_response_operation import CreateAgentResponseOperation


@pytest.mark.asyncio
async def test_create_response_operation():
    # Arrange
    headless_app = wireup.create_async_container(
        # Add service modules
        service_modules=[
            # Top level module containing service registrations.
            core,
            libs,
        ]
    )

    chat_client = await headless_app.get(ChatClient)

    _sut = CreateAgentResponseOperation(client=chat_client, container=headless_app)

    # Act
    response = await _sut.execute_async("Please add a file named test.py to /home/kyle/Development/bottymcbotbot")

    # Assert
    assert response is not None
    print(response)
