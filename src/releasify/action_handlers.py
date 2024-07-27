from collections.abc import Iterable
from typing import Optional, Callable
from .errors import ReleasifyError, NotHandlerError

NAMES_ATTR = '__action_names__'
__action_handlers__: dict[tuple[str], Callable] = {}


def is_action_handler(func: Callable) -> bool:
    return hasattr(func, NAMES_ATTR)


def names_of(handler: Callable) -> Iterable[str]:
    if not is_action_handler(handler):
        raise NotHandlerError(f'Function {handler} was not handler')
    return getattr(handler, NAMES_ATTR)


def action_handlers() -> dict[tuple[str], Callable]:
    return __action_handlers__


def find_action(name: str) -> Optional[Callable]:
    for names, handler in action_handlers().items():
        if name in names:
            return handler
    return None


def new_action_handler(func: Callable, names: Optional[tuple[str, ...] | str] = None) -> Callable:
    if names is None:
        names = tuple()
    if isinstance(names, str):
        names: tuple[str] = (names,)
    elif len(names) == 0:
        names = (func.__name__,)

    if any(find_action(name) for name in names):
        raise ReleasifyError(f'One of names {names} is already in use')
    __action_handlers__[names] = func
    setattr(func, NAMES_ATTR, names)
    return func


def action_handler(names: Optional[tuple[str, ...] | str] = None) -> Callable[[Callable], Callable]:
    return lambda func: new_action_handler(func, names)
