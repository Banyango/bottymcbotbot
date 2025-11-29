import os

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
        service_modules=[
            core,
            libs,
        ]
    )

    chat_client = await headless_app.get(ChatClient)

    _sut = CreateAgentResponseOperation(client=chat_client, container=headless_app)

    # Act
    response = await _sut.execute_async(
        f"Please add a file named test.py to {os.curdir} with a hello world python script in it."
    )

    # Assert
    assert response is not None
    print(response)
