import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from core.code.tools.add_file import AddFile


@pytest.mark.asyncio
async def test_execute_adds_file_when_input_is_valid():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = True
    tool = AddFile(file_service=mock_fs)

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = tmpdir
        file_name = "test.txt"
        context = {"project_root": tmpdir}

        # Act
        result = await tool.execute_async(file_path, file_name, context)

        # Assert
        target = Path(file_path) / file_name
        assert target.exists(), "Expected the file to be created on disk"
        assert result == f"File {file_name} added at {file_path}"


@pytest.mark.asyncio
async def test_execute_returns_error_when_path_outside_project_root():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = False
    tool = AddFile(file_service=mock_fs)

    # Act
    result = await tool.execute_async("/some/path", "file.txt", {"project_root": "/project"})

    # Assert
    assert "outside of project root" in result

