from unittest.mock import MagicMock
import tempfile
from pathlib import Path

import pytest

from core.code.tools.modify_file import ModifyFile


@pytest.mark.asyncio
async def test_execute_modifies_file_when_input_is_valid():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = True
    tool = ModifyFile(file_service=mock_fs)

    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        # create initial file
        file_path = base / "dir" / "file.txt"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("old")

        new_content = "new content"

        # Act
        result = await tool.execute_async(str(file_path), new_content, {"project_root": tmpdir})

        # Assert
        assert "modified" in result
        assert file_path.read_text(encoding="utf-8") == new_content


@pytest.mark.asyncio
async def test_execute_creates_parent_and_writes_when_parent_missing():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = True
    tool = ModifyFile(file_service=mock_fs)

    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        file_path = base / "non" / "existent" / "file.txt"
        new_content = "created content"

        # Act
        result = await tool.execute_async(str(file_path), new_content, {"project_root": tmpdir})

        # Assert
        assert "modified" in result
        assert file_path.exists()
        assert file_path.read_text(encoding="utf-8") == new_content


@pytest.mark.asyncio
async def test_execute_returns_error_when_path_outside_project_root():
    # Arrange
    mock_fs = MagicMock()
    mock_fs.is_path_within_dir.return_value = False
    tool = ModifyFile(file_service=mock_fs)

    # Act
    result = await tool.execute_async("/tmp/file.txt", "x", {"project_root": "/project"})

    # Assert
    assert "outside of project root" in result

