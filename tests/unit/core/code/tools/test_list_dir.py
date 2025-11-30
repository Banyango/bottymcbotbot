from pathlib import Path
from unittest.mock import MagicMock
import tempfile

import pytest

from core.code.tools.list_dir import ListDir


@pytest.mark.asyncio
async def test_execute_lists_directory_entries_when_input_is_valid():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = True
    tool = ListDir(file_service=mock_fs)

    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        sub = base / "subdir"
        sub.mkdir()
        # create files
        files = [sub / "a.txt", sub / "b.txt", sub / "c.md"]
        for f in files:
            f.write_text("content")

        file_path = tmpdir
        file_name = "subdir"
        context = {"project_root": tmpdir}

        # Act
        result = await tool.execute_async(file_path, file_name, context)

        # Assert
        returned = {line for line in result.splitlines() if line}
        expected = {f.name for f in files}
        assert returned == expected


@pytest.mark.asyncio
async def test_execute_returns_error_when_path_outside_project_root():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = False
    tool = ListDir(file_service=mock_fs)

    # Act
    result = await tool.execute_async(
        "/irrelevant", "subdir", {"project_root": "/project"}
    )

    # Assert
    assert "outside of project root" in result
