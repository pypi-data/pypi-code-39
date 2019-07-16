import argparse
from .core import summary, bump

COMMANDS = {
    'summary': summary,
    'bump': bump,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=COMMANDS)
    args = parser.parse_args()
    func = COMMANDS[args.command]
    return func()

from invoke import Program
program = Program(version='0.1.0')