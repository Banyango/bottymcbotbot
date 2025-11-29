import asyncio
from pathlib import Path

from loguru import logger
from wireup import service

from core.agent.interfaces import Tool
import os
import tempfile


@service
class ModifyFile(Tool):
    description = "Modify a file."

    @staticmethod
    def _write_atomic(path: Path, new_content: str) -> None:
        parent = path.parent
        # Create a temp file in the same directory so os.replace is atomic
        fd, tmp_path = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(parent))
        try:
            # Write text using the file descriptor and ensure it's flushed to disk
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(new_content)
                f.flush()
                os.fsync(f.fileno())

            # Atomically replace the target file with the temp file
            os.replace(tmp_path, str(path))
        finally:
            # If something went wrong and the temp still exists, try to remove it
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    async def execute_async(self, file_path: str, new_content: str) -> str:
        """Atomically replace the contents of `file_path` with `new_content`.

        Creates parent directories if they don't exist. The actual file write is
        performed in a thread to avoid blocking the event loop. A temporary file
        is created in the same directory and then atomically moved into place
        using os.replace.
        """
        path = Path(file_path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            await asyncio.to_thread(self._write_atomic, path, new_content)
            return f"File {file_path} modified"
        except Exception as exc:
            logger.error(f"Failed to modify file {file_path}: {exc}")
            return f"Failed to modify file {file_path}: {exc}"
