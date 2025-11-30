from pathlib import Path

from wireup import service


@service
class FileService:
    @staticmethod
    def is_path_within_dir(base_dir: str, target_path: str, treat_target_as_file=False) -> bool:
        """
        Return True if `target_path` is inside `base_dir`.
        Use `treat_target_as_file=True` if `target_path` includes a filename that may not exist yet.
        """
        base = Path(base_dir).resolve()
        target = Path(target_path)
        # if target is a file that may not exist, check its parent directory
        candidate = target.parent.resolve(strict=False) if treat_target_as_file else target.resolve(strict=False)
        try:
            candidate.relative_to(base)
            return True
        except ValueError:
            return False
