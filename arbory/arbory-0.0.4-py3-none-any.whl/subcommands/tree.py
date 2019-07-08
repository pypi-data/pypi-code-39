"""Defines tree command functionality.
"""

import os

import click


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_obj
@click.argument('dirpath', type=click.Path(exists=True, file_okay=False))
@click.option('-f', '--include-files', default=True, type=bool,
    show_default=True)
def tree(obj, dirpath, include_files):
    """Make file tree.

    The specified path must be an existing directory.
    """
    cfg = obj['config']
    for root, dirs, files in os.walk(dirpath):
        level = root.replace(dirpath, '').count(os.sep)
        indent = ' ' * 4 * level
        d_str = os.path.basename(root) + '/'
        fg_col = cfg['dir_color_fg']
        bg_col = cfg['dir_color_bg']
        click.echo(indent + click.style(d_str, fg=fg_col, bg=bg_col))
        if include_files:
            subindent = ' ' * 4 * (level + 1)
            for f_str in files:
                fg_col = cfg['file_color_fg']
                click.echo(subindent + click.style(f_str, fg=fg_col))
