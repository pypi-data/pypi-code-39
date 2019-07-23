class Command:
    name = None

    @staticmethod
    def initialize_parser(parser):
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def main(args):
        raise NotImplementedError  # pragma: no cover


# class ShowConfig(Command):
#     """ Output as YAML string the configuration that would be passed to a
#     service.
#
#     Useful for viewing config files that load values from environement
#     variables.
#     """
#
#     name = 'show-config'
#
#     @staticmethod
#     def initialize_parser(parser):
#         parser.add_argument('--config', default='config.yml', help='The YAML configuration file')
#         return parser
#
#     @staticmethod
#     def main(args):
#         from .show_config import main
#         main(args)


class Start(Command):
    """Run nameko services.  Given a python path to a module containing one or
    more nameko services, will host and run them. By default this will try to
    find classes that look like services (anything with nameko entrypoints),
    but a specific service can be specified via
    ``nameko run module:ServiceClass``.
    """

    name = 'start'

    @staticmethod
    def initialize_parser(parser):
        parser.add_argument('path', help='Python path to one or more service classes to run')
        parser.add_argument('--config', default='', help='The YAML configuration file')
        parser.add_argument('--rabbit', default='pyamqp://guest:guest@localhost', help='RabbitMQ url')
        return parser

    @staticmethod
    def main(args):
        from .rpc.cluster import main
        main(args)


class Shell(Command):
    """Launch an interactive python shell for working with remote nameko
    services.

    This is a regular interactive interpreter, with a special module ``n``
    added to the built-in namespace, providing ``n.rpc`` and
    ``n.dispatch_event``.
    """

    name = 'shell'

    SHELLS = ['bpython', 'ipython', 'plain']

    @classmethod
    def initialize_parser(cls, parser):
        parser.add_argument(
            '--broker', default='pyamqp://guest:guest@localhost',
            help='RabbitMQ broker url')
        parser.add_argument(
            '--interface', choices=cls.SHELLS,
            help='Specify an interactive interpreter interface.'
                 ' (Ignored if not in TTY mode)')
        parser.add_argument(
            '--config', default='',
            help='The YAML configuration file')
        return parser

    @staticmethod
    def main(args):
        from .shell import main
        main(args)


commands = Command.__subclasses__()
