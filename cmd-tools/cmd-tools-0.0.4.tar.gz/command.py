import click


@click.command()
def hello():
    click.echo('hello world', nl=False)
