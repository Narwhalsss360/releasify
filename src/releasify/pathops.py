from typing import Callable, Any
from os import remove
from shutil import copytree, copy, rmtree, move
from pathlib import Path
from .errors import ReleasifyError


def copier(path: Path) -> Callable[[str, str], Any | None]:
    if not path.exists():
        raise ReleasifyError(f'Path {path} does not exist')
    return copytree if path.is_dir() else copy


def deleter(path: Path):
    if not path.exists():
        raise ReleasifyError(f'Path {path} does not exist')
    return rmtree if path.is_dir() else remove


def copy_path(source: Path, destination: Path) -> Any:
    return copier(source)(str(source), str(destination))


def move_path(source: Path, destination: Path) -> Any:
    return move(str(source), str(destination), copier(source))


def delete_path(path: Path) -> Any:
    return deleter(path)(str(path))
