import asyncio


class ModifyFile:
    @staticmethod
    async def execute_async(file_path: str, file_name: str) -> None:
        proc = await asyncio.create_subprocess_exec(
            f"touch {file_name}",
            cwd=file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        if proc.returncode != 0:
            raise Exception(f"Failed to add file {file_name} at {file_path}")
