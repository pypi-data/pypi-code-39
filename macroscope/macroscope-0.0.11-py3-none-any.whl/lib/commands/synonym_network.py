# External libraries
import click

# Local libraries
from lib.plotSynonymStructure import plot_synonym_structure
from lib.globals import synonym_network_year_range


#  macroscope synonym-network -w hello -y 1990 -s 5 -t 0.72
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-y", "--year", type=synonym_network_year_range, required=True)
@click.option("-s", "--synonyms-per-target", type=click.IntRange(3, 10), required=True)
@click.option("-t", "--similarity-threshold", type=click.FloatRange(0.5, 1), required=True)
def synonym_network(word, year, synonyms_per_target, similarity_threshold):
    result = plot_synonym_structure(word, year, synonyms_per_target, similarity_threshold)
    click.echo(result)
