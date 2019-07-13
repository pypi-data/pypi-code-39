
from .base import Command


class Libraries(Command):
    """
    Codec information
    """

    name = 'libraries'
    short_description = 'Music libraries in oodi'

    def __register_arguments__(self, parser):
        subparsers = parser.add_subparsers()

        p = subparsers.add_parser('list', help='List libraries')
        p.set_defaults(func=self.list_libraries)

    def list_libraries(self, args):
        for library in self.libraries:
            self.message(library)
