import argparse
from argparse import ArgumentParser

class _CLI(object):
    def __init__(self, args):
        # Parse the command and create the parser casement will use
        parser = ArgumentParser()
        parser.add_argument('command')
        args = parser.parse_args(args)
        # This will be added to args passed to the run command
        self.command = args.command
        # Create self.parser by calling the requested function
        getattr(self, args.command)()

    def echo(self):
        """ Creates a ArgumentParser to handle the echo command as self.parser """
        self.parser = ArgumentParser(
            usage='casement shortcut test [-h] [-v] text',
        )
        self.parser.add_argument('text', nargs=argparse.REMAINDER)

    def run(self, args):
        """ Do something with the arguments parsed from self.parser """
        if args.command == 'echo':
            print('ECHO: {}'.format(' '.join(args.text)))