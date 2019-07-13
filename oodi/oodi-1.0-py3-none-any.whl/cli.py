
import time

from subprocess import Popen, PIPE
from systematic.shell import ShellCommandParser, CommandPathCache, ScriptError


__command_lookup__ = CommandPathCache()


class OodiShellCommandParser(ShellCommandParser):
    """
    Generic shell command parser with linked configuration
    """
    argument_parsers = {}

    def __init__(self, configuration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configuration = configuration
        self.__cmd_cache__ = __command_lookup__

    def __find_command_pattern__(self):
        """
        Find first available processor command pattern
        """
        for command in self.commands():
            try:
                command_name, args = command.split(None, 1)
                if self.__cmd_cache__.which(command_name):
                    return command
            except Exception:
                continue

        return None

    def __lookup_pattern_arguments__(self, command):
        """
        Lookup extra pattern arguments for detected command
        """
        try:
            return self.argument_parsers[command](self)
        except KeyError:
            return {}

    def __parse_command__(self, **kwargs):
        """
        Parse command to run from pattern and arguments
        """
        pattern = self.__find_command_pattern__()
        if pattern:

            # Load default kwargs for encoder, override only if not specified already
            default_kwargs = self.__lookup_pattern_arguments__(pattern.split()[0])
            for key, value in default_kwargs.items():
                if key not in kwargs:
                    kwargs[key] = value

            try:
                return list(field % kwargs for field in pattern.split())
            except KeyError as e:
                raise ScriptError('Missing required arguments for command pattern {}: {}'.format(
                    pattern,
                    e,
                ))
        else:
            raise ScriptError('No valid commands available for {}'.format(self.__class__))

    def execute(self, args):
        """
        Execute shell command collecting output
        """

        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        rval = None
        while rval is None:
            while True:
                line = p.stdout.readline()
                error = p.stderr.readline()
                if line:
                    print(line)
                if error:
                    print(error)
                if line == b'' and error == b'':
                    break
            time.sleep(1)
            rval = p.poll()

        return rval
