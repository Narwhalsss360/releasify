from typing import Callable, Any
from functools import wraps

ALIASES_ATTR = '__kwarg_aliases__'


def attach_kwarg_aliases(func: Callable, aliases: dict[str, tuple[str, ...]]) -> Callable:
    setattr(func, ALIASES_ATTR, aliases)
    return func


def get_kwarg_aliases(func: Callable) -> dict[str, tuple[str, ...]]:
    if hasattr(func, ALIASES_ATTR):
        return getattr(func, ALIASES_ATTR)
    return {}


def parse_kwarg_aliases(kwargs: dict[str, Any], aliases: dict[str, tuple[str, ...]]) -> dict[str, Any]:
    parsed_kwargs = {}
    for kwarg, value in kwargs.items():
        for original_kwarg, original_kwarg_aliases in aliases.items():
            if kwarg in original_kwarg_aliases:
                parsed_kwargs[original_kwarg] = value
            else:
                parsed_kwargs[kwarg] = value
    return parsed_kwargs


def alias_kwargs(aliases: dict[str, tuple[str, ...]]) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        attach_kwarg_aliases(func, aliases)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **parse_kwarg_aliases(kwargs, aliases))

        return wrapper

    return decorator
