from typing import Callable, Any
from functools import wraps


def auto_parse_str(parsers: dict[tuple[int, str], Callable[[str], Any]]) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            args = list(args)
            for (position, name), parser in parsers.items():
                if position < len(args):
                    args[position] = parser(args[position])
                elif name in kwargs:
                    kwargs[name] = parser(kwargs[name])
            return func(*args, **kwargs)

        return wrapper

    return decorator
