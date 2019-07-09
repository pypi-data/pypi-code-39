# -*- coding: utf-8 -*-

"""Console script for odut."""

import sys
import click
import sys
from pathlib import Path
# The search path can be manipulated from within 
# a Python program as the variable sys.path.<-> PYTHONPATH env variables.
sys.path.append(Path(__file__).parent) 

from .utils import resolve_dependencies
import re


class BadInput(Exception):
    pass 

PAT = re.compile(r'\["?.*\]')

@click.command()
@click.option('--modules', default=[], 
            help="""input modules in a list, e.g --modules "['a', 'b', 'c']"
            """)
@click.option('--file',
             default=None,
             help="resolve dependency issues from the first line of the file.")
@click.option('--base_dir', default='.')
def main(modules=None, file=None, base_dir=None):
    """
    Safely remove dependencies of the Odoo modules...
    you can pass modules in a list from the cmd line, or you can just use a file
    with the modules listed in the first line of the file.

    -----------------------------------------------------------

    Usage:
    Windows:
        python cli.py --modules "['account', 'crm']" --base_dir '/Users/yinet/Desktop/ls/odoo/addons'

    Macos/Linx
        python3 cli.py --modules "['account', 'crm']" --base_dir '/Users/yinet/Desktop/ls/odoo/addons'
    ----------------------------------------------------------
    """
    # resolve_dependencies(modules, file, base_dir)
    if not PAT.search(modules):
        raise BadInput("""\
            Provide  --modules in this format "['a', 'b', 'c']"\
            """) 

    m = [i.strip(" '") for i in modules[2:-2].split(',')]
    resolve_dependencies(modules=m, base_dir=base_dir)


if __name__ == "__main__": 
    main()
