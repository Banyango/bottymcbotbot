import asyncio
from pathlib import Path
from typing import Dict, Any

from loguru import logger
from wireup import service

from core.agent.interfaces import Tool


@service
class ReadFile(Tool):
    description = "Reads the contents of a specified file."

    async def execute_async(self, file_path: str, context: Dict[str, Any]) -> str:
        """Read and return the contents of the specified file.

        Args:
            file_path (str): The directory path where the file is located.
            context (Dict[str, Any]): Additional context for the operation.
        """
        target = Path(context["project_root"]) / Path(file_path)
        try:
            content = await asyncio.to_thread(target.read_text, encoding="utf-8")
            return f"""
ReadFile - file_path: {file_path}
{content}"""
        except Exception as exc:
            logger.error(f"Failed to read file {file_path}: {exc}")
            return f"Failed to read file {file_path}: {exc}"
