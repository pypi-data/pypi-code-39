from .core import *

import click
from idottie import tools

def ls(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    tools.translate.hello()
    ctx.exit()

@click.command()
@click.option('--hello', is_flag=True, callback=ls, expose_value=False, is_eager=True, help='list files')
@click.option('-e', help='to english')
@click.option('-c', help='to chinese')
def cli(e, c):
    if e:
        tools.translate.toEnglish(e)
        click.echo("Hello {}!".format(e))
    elif c:
        tools.translate.toChinese(c)
        click.echo("Hello {}!".format(c))
