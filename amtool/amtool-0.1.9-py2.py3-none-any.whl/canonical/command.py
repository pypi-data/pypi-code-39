import click
from amt import canonical as canon


@click.command()
@click.argument('PATH')
def canonical(path):
    """
    Enforces the canonical representation.
    """
    canon(path)
    return 0
