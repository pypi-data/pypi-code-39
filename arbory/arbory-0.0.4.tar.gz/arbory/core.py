"""Defines core commands.
"""

import click

from .__version__ import __version__
from .config_spec import config_spec
from .subcommands import config, tree


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
@click.version_option(version=__version__, prog_name='arbory')
def arb(ctx):
    """Utilities for file tree generation."""
    # Get configuration specifications and add to context.
    ctx.ensure_object(dict)
    ctx.obj['config'] = config_spec()


arb.add_command(tree)
arb.add_command(config)
