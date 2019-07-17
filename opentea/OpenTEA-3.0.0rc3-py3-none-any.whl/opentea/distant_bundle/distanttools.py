""" Module that is used on a distant machine for scripts """

__all__ = ["DistantTools"]

import sys
import os
import logging
import shlex
import time
import subprocess
from path_tools import PathTools


class DistantTools(PathTools):
    """ Distant tools """

    def __init__(self, debug_level):
        self.timestamp = time.time()
        self.log = logging.getLogger(__name__)
        self.debug_level = debug_level

    def execute(self, command):
        """
        This procedure searches for the specified
        executable in the script directory,
        if not, it tries to execute the command itself.
        The command is then executed and
        its output is printed in standard output
        """
        # Need some work to handle long run and reading of the output on the
        # fly !
        scriptdir = os.path.dirname(
            os.path.abspath(
                sys.modules['__main__'].__file__))
        if os.path.exists(os.path.join(scriptdir, command)):
            command = os.path.join(scriptdir, command)

        self.log.info("Command " + command)

        command = shlex.split(command)
        self.log.info(
            repr(command) +
            ' in ' +
            repr(
                os.getcwd()) +
            ':\n' +
            50 *
            '-' +
            '\n')
        read_from = None
        if "<" in command:
            read_from = command[-1]
            command = command[:-2]
        subp = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        if read_from:
            subp.stdin.write(open(read_from, "r").read())

        stdout_data = []
        self.log.info("     =============StdOut=================\n")
        while True:
            line = subp.stdout.readline()
            if not line:
                break
            self.log.info('     ' + line.rstrip())
            sys.stdout.flush()
            stdout_data.append(line)
        returncode = subp.wait()
        stderr_data = subp.stderr.read()

        if (self.debug_level > 0) and not returncode:
            self.log.debug("\n     =============StdErr=================\n")
            self.log.debug("\n    ".join(stderr_data.split('\n')))
        # if traite "None" "0" False" "" Comme des retours negatif
        if returncode:
            self.log.error("Problem while running command :"
                           + " ".join(command)
                           +"\n=============StdErr=================\n"
                           + stderr_data)
            raise RuntimeError
        return "".join(stdout_data)
