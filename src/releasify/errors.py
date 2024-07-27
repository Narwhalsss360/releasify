from typing import Optional, Callable


class ReleasifyError(Exception):
    def __init__(self, *args, performing: Optional[Callable] = None) -> None:
        super(ReleasifyError, self).__init__(*args)
        self.performing: Optional[Callable] = performing


class NotHandlerError(ReleasifyError):
    def __init__(self, *args, performing: Optional[Callable] = None) -> None:
        super(NotHandlerError, self).__init__(*args, performing=performing)
