from typing import Callable, Any
from pathlib import Path
import yaml
import json


def load_json(text: str) -> dict | list:
    return json.loads(text)


def load_yaml(text: str) -> dict | list:
    return yaml.load(text, yaml.CLoader)


def dump_json(obj: list | dict, **kwargs) -> str:
    return json.dumps(obj, indent=4, **kwargs)


def dump_yaml(obj: list | dict, **kwargs) -> str:
    return yaml.dump(obj, **kwargs)


DEFAULT_DUMPER = dump_yaml


def parse_in(file: Path) -> dict | list:
    parser: Callable[[str], dict | list]
    if file.suffix.lower() in ('.yaml', '.yml'):
        parser: Callable[[str], dict | list] = load_yaml
    elif file.suffix.lower() == '.json':
        parser: Callable[[str], dict | list] = load_json
    else:
        raise RuntimeError(f'Cannot parse file {file}: Unknown type')
    with open(file, 'r', encoding='utf-8') as fstream:
        return parser(fstream.read())


# noinspection PyTypeChecker
def parse_out(file: Path, obj: list | dict, **kwargs: Any) -> int:
    dumper: Callable[[list | dict, dict[str, Any]], str]
    if file.suffix.lower() in ('.yaml', '.yml'):
        dumper: Callable[[list | dict, dict[str, Any]], str] = dump_yaml
    elif file.suffix.lower() == '.json':
        dumper: Callable[[list | dict, dict[str, Any]], str] = dump_json
    else:
        dumper: Callable[[list | dict, dict[str, Any]], str] = DEFAULT_DUMPER
    with open(file, 'w', encoding='utf-8') as fstream:
        return fstream.write(dumper(obj, **kwargs))
