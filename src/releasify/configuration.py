from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import re
from os import listdir, getcwd
from .parsing import parse_in, parse_out
from .action_handlers import find_action
from .builtin_actions import *


@dataclass
class Configuration:
    # noinspection SpellCheckingInspection
    DEFAULT_FILE_RE = r'releas(e|ify).(json|yaml|yml)'

    work_in: str = field(default_factory=lambda: './')
    retries: int = field(default=0)
    silently_continue: bool = field(default=False)
    actions: list[dict] = field(default_factory=lambda: [])
    log_file: str = field(default_factory=str)

    @staticmethod
    def load_default() -> Optional[Configuration]:
        for file in listdir(getcwd()):
            if re.match(Configuration.DEFAULT_FILE_RE, file):
                return Configuration(**parse_in(Path(file)))
        return None

    def __post_init__(self) -> None:
        self._logs: list[str] = []

    def _log_out(self, text: str) -> None:
        self._logs.append(text)
        print(text)

    def save_logs(self) -> None:
        if self.log_file:
            parse_out(Path(self.log_file), self._logs)

    def perform(self, action_data: dict, retries_left: int):
        name: str = ''
        try:
            if 'action' not in action_data:
                raise RuntimeError(f'All action data requires `action` key data: {action_data}.')

            name: str = action_data.pop('action')
            handler = find_action(name)
            if handler is None:
                raise RuntimeError(f'Action {name} does not exist.')

            self._log_out(f'{name} -> {handler(**action_data)}')
            return True
        except ReleasifyError as err:
            action_data['action'] = name
            self._log_out(f'An error occurred: {err}')

            if not self.silently_continue and input(
                    f'Retry action {action_data} or continue? (retry/continue):') == 'retry':
                retries_left -= 1
                if retries_left <= 0:
                    self._log_out(f'No retries left for {action_data}')
                    return False
                self._log_out(f'Retrying ({retries_left} left) {action_data}')
                return self.perform(action_data, retries_left)

            self._log_out(f'Skipping {action_data}')
            return True
        except Exception as err:
            action_data['action'] = name
            self._log_out(f'An exception was thrown running action {action_data}: {err}')
            return False

    def releasify(self) -> None:
        def log_wrapped() -> None:
            if not self.actions:
                self._log_out('No actions!')
                return

            for action_data in self.actions:
                if not self.perform(action_data, self.retries):
                    break

        try:
            log_wrapped()
        except Exception as e:
            self.save_logs()
            raise e
        self.save_logs()
