import os
from colorconsole import terminal

from jt64common import __qt_version_dict__

from colorconsole import terminal
from subprocess import PIPE
from subprocess import run


def clear():
    """Clear Screen Function"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Simple pause command"""
    os.system("pause")


def cmd(command):
    """Default Subprocess Command
    Input
        str("command as string")
    Returns
        Output from shell command
    """
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

