import tempfile
from pathlib import Path

from core.code.services import FileService


def test_is_path_within_dir_returns_true_for_directory_inside_base():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        sub = base / "sub"
        sub.mkdir()

        assert FileService.is_path_within_dir(str(base), str(sub)) is True


def test_is_path_within_dir_treat_target_as_file_with_nonexistent_file_inside_base():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        # target includes a filename that does not (yet) exist
        target_file = base / "some" / "new.txt"

        assert FileService.is_path_within_dir(str(base), str(target_file), treat_target_as_file=True) is True


def test_is_path_within_dir_returns_false_for_outside_path():
    with tempfile.TemporaryDirectory() as base_tmp:
        base = Path(base_tmp)
        with tempfile.TemporaryDirectory() as other_tmp:
            other = Path(other_tmp)
            # other temporary directory is not inside base
            assert FileService.is_path_within_dir(str(base), str(other)) is False


def test_is_path_within_dir_same_path_returns_true():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        # same path should be considered within
        assert FileService.is_path_within_dir(str(base), str(base)) is True

