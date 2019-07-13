
from .base import Command
from ...metadata.albumart import AlbumArt, default_album_art, detect_album_art


class AlbumartCommand(Command):
    """
    Album art information
    """

    name = 'albumart'
    short_description = 'Audio file album art processing'

    def __register_arguments__(self, parser):
        subparsers = parser.add_subparsers()

        p = subparsers.add_parser('extract', help='Extract albumart from files')
        p.add_argument('-a', '--albumart', help='Album art file to extract')
        p.add_argument('-f', '--force', action='store_true', help='Force updating existing albumart')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.extract_albumart)

        p = subparsers.add_parser('embed', help='Embed albumart in files')
        p.add_argument('-a', '--albumart', help='File path to album art file to embed')
        p.add_argument('-u', '--url', help='URL for album art image to embed')
        p.add_argument('-f', '--force', action='store_true', help='Force updating existing albumart')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.embed_albumart)

    def extract_albumart(self, args):
        for arg in self.get_tracks(args.paths):
            for track in arg:
                try:
                    tags = track.tags
                except Exception as e:
                    self.error(e)
                    tags = None
                if tags:
                    if args.albumart:
                        albumart = AlbumArt(self.script.configuration, track.path)
                    else:
                        albumart = default_album_art(self.script.configuration, track.path)
                    if albumart.exists:
                        self.message('EXISTS  {}'.format(albumart))
                        break
                    elif tags.has_albumart():
                        self.message('EXTRACT {}'.format(albumart))
                        tags.save_albumart(albumart.path)

    def embed_albumart(self, args):
        albumart_from_args = False
        if args.url:
            albumart = AlbumArt(self.script.configuration)
            albumart.fetch(args.url)
            albumart_from_args = True
        elif args.albumart:
            albumart = AlbumArt(self.script.configuration, args.albumart)
            albumart_from_args = True

        for arg in self.get_tracks(args.paths):
            for track in arg:
                try:
                    tags = track.tags
                except Exception as e:
                    self.error(e)
                    tags = None
                if tags:
                    if not albumart_from_args:
                        albumart = detect_album_art(self.script.configuration, track.path)
                        if albumart is None:
                            self.message('N/A      {}'.format(track.path))
                            break
                    if not tags.has_albumart() or args.force:
                        self.message('ADD      {}'.format(track))
                        try:
                            tags.set_albumart(albumart)
                        except Exception as e:
                            self.error(e)
                    else:
                        self.message('TAGGED   {}'.format(track))
