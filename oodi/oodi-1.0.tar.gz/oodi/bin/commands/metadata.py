
import json

from .base import Command


class Metadata(Command):
    """
    Track metadata information
    """

    name = 'metadata'
    short_description = 'Track metadata exports'

    def __register_arguments__(self, parser):
        subparsers = parser.add_subparsers()

        p = subparsers.add_parser('update', help='Update metadata for library')
        p.add_argument('path', help='Library path')
        p.set_defaults(func=self.update_library_metadata)

        p = subparsers.add_parser('show', help='Show track metadata')
        p.add_argument('paths', nargs='*', help='Paths to process')
        p.set_defaults(func=self.show_metadata)

    def update_library_metadata(self, args):

        library = self.libraries.find_tree_by_prefix(args.path)
        self.message('load metadata for {}'.format(args.path))
        library.metadata.load()
        self.message('update metadata')
        library.metadata.update()
        self.message('save metadata for {}'.format(args.path))
        library.metadata.save()

    def show_metadata(self, args):
        for arg in self.get_tracks(args.paths):
            for track in arg:
                self.message(json.dumps(track.metadata.data, indent=2))
