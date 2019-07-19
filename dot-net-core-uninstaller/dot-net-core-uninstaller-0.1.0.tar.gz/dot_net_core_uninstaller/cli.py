import click

from . import __version__, Uninstaller


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('v' + __version__)
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help="Show version and exit.")
def cli():
    pass


@cli.command(help="Remove the version of .Net Core.")
@click.option('--no-input', is_flag=True, help='Deletes the files without asking the user')
@click.argument('version')
def remove(no_input, version):
    if not no_input:
        click.confirm('Do you want to continue?', abort=True)
    Uninstaller().delete(version)


@cli.command('list', help="List all the version of .Net Core installed.")
def list_dotnet():
    Uninstaller().list_dotnet()
