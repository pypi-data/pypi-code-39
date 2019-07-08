"""Define functionality for manipulating the configuration.
"""

import click


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_obj
def config(obj):
    """Manipulate arbory configuration."""
    cfg = obj['config']
    click.echo(cfg['selected'])
