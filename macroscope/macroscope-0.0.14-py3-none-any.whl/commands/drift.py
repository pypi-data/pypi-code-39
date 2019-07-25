# External libraries
import click

# Local libraries
from lib.plotSemanticDrift import plot_semantic_drift_path
from lib.enums import Reduce, ClosestSearchMethod
from lib.globals import drift_year_range

#  macroscope drift -w hello -w there -s 1880 -e 1990
# TODO: this needs to be fixed for certain years and intervals - see plot_semantic_drift_path function for more info
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-s", "--start-year", type=drift_year_range, required=True)
@click.option("-e", "--end-year", type=drift_year_range, required=True)
def drift(word, start_year, end_year):
    """Returns drift of words over a given period."""

    result = plot_semantic_drift_path(
        word,
        start_year,
        end_year,
        yearInterval=40,
        k=15,
        components=2,
        reduce=Reduce.PCA,
        method=ClosestSearchMethod.SVD,
        addinBetween=True,
        size=18,
        align=True
    )
    click.echo(result)
