
from systematic.shell import ScriptCommand

from oodi.codecs.base import Codecs
from oodi.library.base import Libraries, LibraryError
from oodi.library.tree import IterableTrackPaths


class Command(ScriptCommand):
    """
    Common base class for Oodi CLI commands
    """

    @property
    def codecs(self):
        """
        Return codecs with current configurtion
        """
        return Codecs(configuration=self.script.configuration)

    @property
    def libraries(self):
        return Libraries(configuration=self.script.configuration)

    def get_tracks(self, paths):
        iterators = []
        for path in paths:
            try:
                iterators.append(IterableTrackPaths(path, self.script.configuration))
            except LibraryError as e:
                self.error(e)
        return iterators

    def run(self, args):
        if getattr(args, 'func', None) is None:
            self.exit(1, 'No command selected')
        args.func(args)
