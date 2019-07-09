import click

@click.command()
@click.pass_context
def help(ctx):
    """Show this message and exit."""
    print(ctx.parent.get_help())
