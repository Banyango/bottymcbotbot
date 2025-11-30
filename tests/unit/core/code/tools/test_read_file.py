from unittest.mock import MagicMock
import tempfile
from pathlib import Path

import pytest

from core.code.tools.read_file import ReadFile


@pytest.mark.asyncio
async def test_execute_returns_file_contents_when_input_is_valid():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = True
    tool = ReadFile(file_service=mock_fs)

    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        file_name = "sample.txt"
        content = "hello world\nthis is a test"
        (base / file_name).write_text(content, encoding="utf-8")

        file_path = tmpdir
        context = {"project_root": tmpdir}

        # Act
        result = await tool.execute_async(file_path, file_name, context)

        # Assert
        assert result == content


@pytest.mark.asyncio
async def test_execute_returns_error_when_path_outside_project_root():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = False
    tool = ReadFile(file_service=mock_fs)

    # Act
    result = await tool.execute_async("/irrelevant", "sample.txt", {"project_root": "/project"})

    # Assert
    assert "outside of project root" in result

