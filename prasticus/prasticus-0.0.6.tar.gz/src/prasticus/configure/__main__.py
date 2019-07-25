import argparse
from importlib import import_module
import sys


class Commander(object):

    def __init__(self):
        self.parser = parser = argparse.ArgumentParser(
            prog='python3 -m "prasticus.configure"',
            description='run various commands relative to prasticus.configure',
            usage='''configure <command> [<args>]

Available commands are:
   path         Writes the configuration path to stdout.
   random-key   Writes a random module identifier to stdout.
   get-root     Writes the configuration root directory to stdout.
   set-root     Sets the configuration root directory.
   find-config  Writes the path to the configuration file of a module.
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        command = args.command.replace('-', '_')
        if not hasattr(self, command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, command)()

    def path(self):
        parser = argparse.ArgumentParser(
        prog=self.parser.prog + ' path',
            description='Writes the configuration path to stdout')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        configure = import_module(__package__)
        print(configure.path)

    def random_key(self):
        parser = argparse.ArgumentParser(
        prog=self.parser.prog + ' random-key',
        description='Writes a random module identifier to stdout')
        args = parser.parse_args(sys.argv[2:])
        util = import_module('.util', __package__)
        print(util.random_module_name())
        
    def get_root(self):
        parser = argparse.ArgumentParser(
        prog=self.parser.prog + ' get-root',
        description='Writes the configure root directory to stdout')
        args = parser.parse_args(sys.argv[2:])
        from .autoconfig.manageroot import get_root_dir
        print(get_root_dir())
        
    def set_root(self):
        parser = argparse.ArgumentParser(
        prog=self.parser.prog + ' set-root',
        description='Sets the configure root directory')
        parser.add_argument('dir', help="directory to set as root")
        parser.add_argument(
            '-c', '--create',
            action='store_true', dest='create',
            help='Create directory if it does not exist')
        args = parser.parse_args(sys.argv[2:])
        from .autoconfig.manageroot import set_root_dir
        set_root_dir(args.dir, create=args.create, create_config=args.create)

    def find_config(self):
        parser = argparse.ArgumentParser(
            prog=self.parser.prog + ' find-config',
            description= (
                'Writes path to the configuration'
                ' file of a module to stdout'))
        parser.add_argument('modname', help="qualified name of module")
        parser.add_argument(
            '-c', '--cat', '--content',
            action='store_true', dest='cat',
            help="Print configuration file's content instead of file name")
        parser.add_argument(
            '-r', '--resolve',
            action='store_true', dest='resolve',
            help="Print absolute file name")
        parser.add_argument(
            '-e', '--edit',
            action='store_true', dest='edit',
            help="Launch editor and open the configuration file")
        args = parser.parse_args(sys.argv[2:])
        m = import_module(args.modname)
        filename = m._configure_agent.static_module.__file__
        from pathlib import Path
        if args.cat:
            if filename.endswith('.pyc'):
                filename = filename[:-1]
            print(Path(filename).read_text(), end='')
        elif args.resolve:
            print(Path(filename).resolve())
        else:
            print(filename)
        if args.edit:
            import os
            import shutil
            import subprocess as sp
            if hasattr(os, 'startfile'):
                os.startfile(filename)
            elif shutil.which('xdg-open'):
                sp.Popen(['xdg-open', filename],
                        stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            elif sys.platform() == 'darwin':
                sp.Popen(['open', filename],
                        stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            else:
                pass

if __name__ == '__main__':
    pass
    Commander()
    