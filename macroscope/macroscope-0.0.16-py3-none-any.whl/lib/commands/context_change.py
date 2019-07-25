# External libraries
import click

# Local libraries
from lib.changeOfContext import change_of_contextW
from lib.globals import context_change_year_range

#  macroscope context-change -w hello -y 1990 -y 2000
@click.command()
@click.option("-w", "--word", required=True)
@click.option("-y", "--year", type=context_change_year_range, required=True, multiple=True)
def context_change(word, year):
    """Returns context change of search term over given period of years."""

    # TODO: pass k parameter as a none required parameter
    result = change_of_contextW(word, year, 40, True)
    click.echo(result)
