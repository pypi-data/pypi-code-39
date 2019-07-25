# External libraries
import click

# Local libraries
from lib.plot import plot
from lib.enums import PlotType
from lib.globals import emotion_year_range

#  macroscope emotion -w hello -w there -s 1800 -e 2009 -t v
# TODO: only works if start year is 1800 AND end year is 2009
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-s", "--start-year", type=emotion_year_range, required=True)
@click.option("-e", "--end-year", type=emotion_year_range, required=True)
@click.option("-t", "--type", required=True, type=click.Choice(['v', 'a', 'c']))
def emotion(word, start_year, end_year, type):
    lowercase_type = type.lower()
    plotType = None

    if lowercase_type == 'v':
        plotType = PlotType.V
    elif lowercase_type == 'a':
        plotType = PlotType.A
    elif lowercase_type == 'c':
        plotType = PlotType.C
    else:
        raise NotImplementedError("No handler implemented for type " + type.upper())

    result = plot(plotType, word, start_year, end_year)
    click.echo(result)
