from typing import Callable, Any
from functools import wraps
import glob
import os
from pathlib import Path

PATH_DELIMITER, OTHER_PATH_DELIMITER = ('\\', '/') if os.name == 'nt' else ('/', '\\')


def rreplace(string: str, old: str, new: str) -> str:
    return new.join(string.rsplit(old))


def glob_source_to_destination(source: str, destination: str) -> list[tuple[Path, Path]]:
    source = source.replace(OTHER_PATH_DELIMITER, PATH_DELIMITER)
    source_folder: str = source.rsplit(PATH_DELIMITER, 1)[0] + PATH_DELIMITER

    if destination[-1] != PATH_DELIMITER:
        destination += PATH_DELIMITER

    return [
        (source_file, rreplace(source_file, source_folder, destination))
        for source_file in glob.glob(source, recursive=source.count('*') > 1)
    ]


def auto_glob(source_parameter: tuple[int, str], destination_parameter: tuple[int, str]) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            args: list = list(args)
            if source_parameter[1] in kwargs:
                source: str = kwargs[source_parameter[1]]
                def set_source_path(path: str) -> None:
                    kwargs[source_parameter[1]] = path
            else:
                source: str = args[source_parameter[0]]
                def set_sourec_path(path: str) -> None:
                    args[source_parameter[0]] = path

            if destination_parameter[1] in kwargs:
                destination: str = kwargs[destination_parameter[1]]
                del kwargs[destination_parameter[1]]
                def set_destination_path(path: str) -> None:
                    kwargs[destination_parameter[1]] = path
            else:
                destination: str = args[destination_parameter[0]]
                def set_destination_path(path: str) -> None:
                    args[destination_parameter[0]] = path

            result: str = ''
            for source_path, destination_path in glob_source_to_destination(source, destination):
                set_source_path(source_path)
                set_destination_path(destination_path)
                result += f'{func(*args, **kwargs)}\t'
            if result:
                result = result[:-1]
            return result

        return wrapper

    return decorator
