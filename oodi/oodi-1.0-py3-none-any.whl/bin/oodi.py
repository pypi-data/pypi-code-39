
from systematic.shell import Script

from oodi.configuration import Configuration, ConfigurationError
from oodi.constants import DEFAULT_CONFIG_PATH

from .commands.albumart import AlbumartCommand
from .commands.codecs import Codecs
from .commands.libraries import Libraries
from .commands.metadata import Metadata
from .commands.tags import Tags

USAGE = """Oodi music library management tool

"""


class OodiScript(Script):
    """
    Custom script for oodi
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument('-c', '--config', default=DEFAULT_CONFIG_PATH, help='Configuration file')

    def __process_args__(self, args):
        try:
            self.configuration = Configuration(args.config)
        except ConfigurationError as e:
            self.exit(1, e)
        return super().__process_args__(args)


def main():
    script = OodiScript(USAGE)

    script.add_subcommand(Codecs())
    script.add_subcommand(Libraries())
    script.add_subcommand(AlbumartCommand())
    script.add_subcommand(Metadata())
    script.add_subcommand(Tags())

    script.run()


if __name__ == '__main__':
    main()
