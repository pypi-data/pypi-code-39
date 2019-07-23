import click
from lib.fact import factorial


@click.group()
def cli():
    pass


@cli.command()
def health():
    click.echo("Healthy!")
    click.echo(factorial(4))
