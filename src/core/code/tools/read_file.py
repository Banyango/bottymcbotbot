import asyncio
from pathlib import Path

from loguru import logger
from wireup import service

from core.agent.interfaces import Tool


@service
class ReadFile(Tool):
    description = "Reads the contents of a specified file."

    async def execute_async(self, file_path: str, file_name: str) -> str:
        """Read and return the contents of the specified file.

        This implementation uses pathlib.Path.read_text executed in a thread to avoid
        blocking the event loop on filesystem IO.
        """
        target = Path(file_path) / file_name
        try:
            # Run the blocking read_text in a thread
            content = await asyncio.to_thread(target.read_text, encoding="utf-8")
            return content
        except Exception as exc:
            logger.error(f"Failed to read file {file_name} at {file_path}: {exc}")
            return f"Failed to read file {file_name} at {file_path}: {exc}"
