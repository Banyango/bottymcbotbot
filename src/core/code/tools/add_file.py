import asyncio
from pathlib import Path

from loguru import logger
from wireup import service

from core.agent.interfaces import Tool


@service
class AddFile(Tool):
    description = "Adds a file to the specified directory."

    async def execute_async(self, file_path: str, file_name: str) -> str:
        """Create the directory (if needed) and touch the target file.

        This implementation uses pathlib.Path.touch executed in a thread to avoid
        blocking the event loop on filesystem IO.
        """
        dir_path = Path(file_path)
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            target = dir_path / file_name
            # Run the blocking touch in a thread
            await asyncio.to_thread(target.touch, True)

            return f"File {file_name} added at {file_path}"
        except Exception as exc:
            logger.error(f"Failed to add file {file_name} at {file_path}: {exc}")
            return f"Failed to add file {file_name} at {file_path}: {exc}"
