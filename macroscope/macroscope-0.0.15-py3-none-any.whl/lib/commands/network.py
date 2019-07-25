# External libraries
import click

# Local libraries
from lib.plotNetwork import plotNetwork_new
from lib.enums import NetworkMethod
from lib.globals import network_year_range


#  macroscope network -w hello -y 1990 -n 300 -r 0.7 -c 0.7 -f 3.5 -e 5 -d 70
@click.command()
@click.option("-w", "--word", required=True)
@click.option("-y", "--year", type=network_year_range, required=True)
@click.option("-n", "--maximum-nodes", type=click.IntRange(10, 400), required=True)
@click.option("-r", "--context-relevance", type=click.FloatRange(0, 1), required=True)
@click.option("-c", "--context-cohesiveness", type=click.FloatRange(0, 1), required=True)
@click.option("-f", "--word-relevance", type=click.FloatRange(2, 4), required=True)  # -f for fitness
@click.option("-e", "--minimum-edges", type=click.IntRange(4, 6), required=True)
@click.option("-d", "--display-nodes", type=click.IntRange(20, 200), required=True)
# @click.option("-m", "--method", type=click.Choice(['PMI', 'COR']), required=True) #  TODO: needed?
def network(
    word,
    year,
    context_relevance,
    maximum_nodes,
    context_cohesiveness,
    word_relevance,
    minimum_edges,
    display_nodes
):
    result = plotNetwork_new(
        word,
        year,
        context_relevance,
        maximum_nodes,
        context_cohesiveness,
        word_relevance,
        minimum_edges,
        display_nodes,
        NetworkMethod.PMI
    )
    click.echo(result)
