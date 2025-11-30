import asyncio
from pathlib import Path
from typing import Dict, Any

from loguru import logger
from wireup import service

from core.agent.interfaces import Tool
from core.code.services import FileService


@service
class ListDir(Tool):
    description = "Lists the contents of a specified directory."

    async def execute_async(self, file_path: str, context: Dict[str, Any]) -> str:
        """List and return the contents of the specified directory.

        Args:
            file_path (str): The directory path where the target directory is located.
            context (Dict[str, Any]): Additional context for the operation.
        """
        target = Path(context["project_root"]) / Path(file_path)

        if not target.is_dir():
            return f"The path {file_path} is not a directory. You might need to add a trailing slash."

        try:
            # Run the blocking iterdir in a thread
            entries = await asyncio.to_thread(
                lambda: [p.name for p in target.iterdir()]
            )
            return "\n".join(entries)
        except Exception as exc:
            logger.error(f"Failed to list directory at {file_path}: {exc}")
            return f"Failed to list directory at {file_path}: {exc}"
