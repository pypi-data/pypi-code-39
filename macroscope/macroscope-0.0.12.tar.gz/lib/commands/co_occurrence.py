# External libraries
import click

# Local libraries
from lib.plotCooccurrence import plot_co_occurence


#  macroscope co-occurrence -w hello -c there -c hi
@click.command()
@click.option("-w", "--word", required=True)
@click.option("-c", "--context-words", required=True, multiple=True)
def co_occurrence(word, context_words):
    """Returns co-occurrence between target word and context words for every year."""

    normalize = False
    result = plot_co_occurence(word, context_words, normalize)
    click.echo(result)
