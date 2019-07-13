
from .base import Command


class Tags(Command):
    """
    Tags information
    """

    name = 'tags'
    short_description = 'Audio file tags processing'

    def __register_arguments__(self, parser):
        subparsers = parser.add_subparsers()

        p = subparsers.add_parser('list', help='List tags in files')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.list_tags)

        p = subparsers.add_parser('magic', help='Show file magic strings')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.list_magic_strings)

        p = subparsers.add_parser('set', help='List tags in files')
        p.add_argument('-t', '--tags', action='append', help='Tags to set as key=value')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.set_tags)

        p = subparsers.add_parser('fix-itunes-containers', help='Fix old itunes container')
        p.add_argument('paths', nargs='*', help='Paths to process')
        p.set_defaults(func=self.fix_itunes_containers)

    def set_tags(self, args):
        updated_tags = {}
        for arg in args.tags:
            try:
                tag, value = arg.split('=', 1)
                updated_tags[tag] = value
            except Exception:
                self.exit(1, 'Error parsing tag {}'.format(arg))

        for arg in self.get_tracks(args.paths):
            for track in arg:
                tags = track.tags
                if tags:
                    tags.update(**updated_tags)

    def list_tags(self, args):
        """
        List file tags
        """
        for arg in self.get_tracks(args.paths):
            for track in arg:
                tags = track.tags
                if tags:
                    for tag, value in tags:
                        self.message('{:20} {}'.format(tag, value))

    def list_magic_strings(self, args):
        for arg in self.get_tracks(args.paths):
            for track in arg:
                self.message('{}: {}'.format(track.path, track.magic))

    def fix_itunes_containers(self, args):
        for arg in self.get_tracks(args.paths):
            for track in arg:
                if track.requires_aac_itunes_fix():
                    self.message('FIX   {}'.format(track))
                    track.fix_aac_for_itunes()
                else:
                    self.message('OK    {}'.format(track))
