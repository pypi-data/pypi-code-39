
from .base import Command


class Codecs(Command):
    """
    Codec information
    """

    name = 'codecs'
    short_description = 'Codecs in oodi'

    def __register_arguments__(self, parser):
        subparsers = parser.add_subparsers()

        p = subparsers.add_parser('list', help='List codecs')
        p.set_defaults(func=self.list_codecs)

        p = subparsers.add_parser('show', help='Show codec details')
        p.set_defaults(func=self.show_codec_details)

    def list_codecs(self, args):
        for codec in self.codecs:
            self.message(codec)

    def show_codec_details(self, args):
        self.codecs
