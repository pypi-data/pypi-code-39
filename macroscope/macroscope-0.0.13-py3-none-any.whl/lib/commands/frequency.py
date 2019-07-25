# External libraries
import click

# Local libraries
from lib.wrapperFreq import wrapper_freq
from lib.globals import frequency_year_range


#  macroscope frequency -w hello -w there -s 1800 -e 2009
#  TODO: entire frequeny function needs to be looked at
#  TODO: only works if start year is 1800 AND end year is 2009
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-s", "--start-year", type=frequency_year_range, required=True)
@click.option("-e", "--end-year", type=frequency_year_range, required=True)
def frequency(word, start_year, end_year):
    click.echo(word)
    click.echo(start_year)
    click.echo(end_year)

    result = wrapper_freq(word, start_year, end_year)
    click.echo(result)
