# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import sys

from ruamel.std.argparse import ProgramBase, option, CountAction, \
    SmartFormatter, sub_parser, version
from ruamel.appconfig import AppConfig
from . import __version__
from .client import Client


def to_stdout(*args):
    sys.stdout.write(' '.join(args))


class ClientCmd(ProgramBase):
    def __init__(self):
        super(ClientCmd, self).__init__(
            formatter_class=SmartFormatter,
            # aliases=True,
            # usage="""""",
        )

    # you can put these on __init__, but subclassing ClientCmd
    # will cause that to break
    @option('--verbose', '-v',
            help='increase verbosity level', action=CountAction,
            const=1, nargs=0, default=0, global_option=True)
    @option('--port', type=int, default=5402,
            help='port to send to (default %(default)s)')
    @option('--host', default='localhost',
            help='host to send to (default %(default)s)')
    @version('version: ' + __version__)
    def _pb_init(self):
        # special name for which attribs are included in help
        pass

    def run(self):
        self.client = Client(self._args.port, self._args.host)
        if hasattr(self._args, 'func'):  # not there if subparser selected
            return self._args.func()
        self._parse_args(['--help'])     # replace if you use not subparsers

    def parse_args(self):
        self._config = AppConfig(
            'ruamel_browser_client',
            filename=AppConfig.check,
            parser=self._parser,  # sets --config option
            warning=to_stdout,
            add_save=False,  # add a --save-defaults (to config) option
        )
        # self._config._file_name can be handed to objects that need
        # to get other information from the configuration directory
        self._config.set_defaults()
        self._parse_args(
            default_sub_parser="send",
        )

    @sub_parser(help='some command specific help')
    # @option('--session-name', default='abc')
    @option('args', nargs='+')
    def send(self):
        print(self.client.send_recv(u' '.join(self._args.args)))


def main():
    n = ClientCmd()
    n.parse_args()
    sys.exit(n.run())

if __name__ == '__main__':
    main()
