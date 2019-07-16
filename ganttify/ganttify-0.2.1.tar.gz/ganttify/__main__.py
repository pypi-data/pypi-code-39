# -*- coding: utf-8 -*-

"""CLI entrypoint for ganttify."""
import sys

from ganttify import cli


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    # potentially modify this to a more complicated context object if necessary
    cli.cli()


if __name__ == '__main__':
    main()
