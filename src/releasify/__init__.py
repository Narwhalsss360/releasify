import sys
import typing
import os.path
from pathlib import Path
from . import configuration
from . import parsing


def main() -> None:
    sys.argv.pop(0)
    if not len(sys.argv):
        config: typing.Optional[configuration.Configuration] = configuration.Configuration.load_default()
        if config is None:
            print(f'Could not find default file: {configuration.Configuration.DEFAULT_FILE_RE}')
            return
    elif os.path.isfile(sys.argv[0]):
        config: configuration.Configuration = configuration.Configuration(**parsing.parse_in(Path(sys.argv[0])))
    else:
        print(f'File {sys.argv[0]} not found')
        return

    config.releasify()


if __name__ == '__main__':
    main()
