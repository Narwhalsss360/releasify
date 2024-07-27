import subprocess
from .auto_parse_str import auto_parse_str
from .kwarg_aliasing import alias_kwargs
from .pathops import Path, copy_path, move_path, delete_path
from .action_handlers import action_handler
from .errors import ReleasifyError


@action_handler(('copy', 'cp'))
@alias_kwargs({'source': ('src',), 'destination': ('dst',)})
@auto_parse_str({(0, 'source'): Path, (1, 'destination'): Path})
def copy_action(source: Path, destination: Path) -> str:
    try:
        copy_path(source, destination)
        return f'Copied {source} to {destination}'
    except Exception as e:
        raise ReleasifyError(f'Error occurred running copy: {e}') from e


@action_handler(('move', 'mv'))
@alias_kwargs({'source': ('src',), 'destination': ('dst',)})
@auto_parse_str({(0, 'source'): Path, (1, 'destination'): Path})
def move_action(source: Path, destination: Path) -> str:
    try:
        move_path(source, destination)
        return f'Moved {source} to {destination}'
    except Exception as e:
        raise ReleasifyError(f'Error occurred running move: {e}') from e


@action_handler(('delete', 'del', 'remove', 'rm'))
@alias_kwargs({'path': ('source', 'src')})
@auto_parse_str({(0, 'path'): Path})
def delete_action(path: Path) -> str:
    try:
        delete_path(path)
        return f'Deleted {path}'
    except Exception as e:
        raise ReleasifyError(f'Error occurred running delete: {e}') from e


@action_handler(('script',))
@alias_kwargs({'source': ('src',)})
@auto_parse_str({(0, 'source'): Path})
def script_action(source: Path) -> str:
    if not source.is_file():
        raise ReleasifyError(f'script {source}: File does not exist')
    script_globals = {'script_eval': None}
    with open(source, 'r', encoding='utf-8') as source_file:
        exec(source_file.read(), script_globals, locals())
    return f'Script {source} executed{script_globals["script_eval"] or ""}'


@action_handler(('subprocess',))
def subprocess_action(args: list[str]) -> str:
    return f'{args[0]} returned {subprocess.run(args, shell=True, check=True).returncode}'
