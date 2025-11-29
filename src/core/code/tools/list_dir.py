import asyncio
from pathlib import Path

from loguru import logger
from wireup import service

from core.agent.interfaces import Tool


@service
class ListDir(Tool):
    description = "Lists the contents of a specified directory."

    async def execute_async(self, file_path: str, file_name: str) -> str:
        """List and return the contents of the specified directory.

        This implementation uses pathlib.Path.iterdir executed in a thread to avoid
        blocking the event loop on filesystem IO.
        """
        target = Path(file_path) / file_name
        try:
            # Run the blocking iterdir in a thread
            entries = await asyncio.to_thread(
                lambda: [p.name for p in target.iterdir()]
            )
            return "\n".join(entries)
        except Exception as exc:
            logger.error(f"Failed to list directory {file_name} at {file_path}: {exc}")
            return f"Failed to list directory {file_name} at {file_path}: {exc}"
