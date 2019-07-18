# External libraries
import click

# Standard library
import json

# Local libraries
from lib.enums import ClosestSearchMethod, Reduce, NetworkMethod
from lib.closestSynonyms import closest_synonyms
from lib.changeOfContext import change_of_contextW
from lib.plotCooccurrence import plot_co_occurence
from lib.plotSemanticDrift import plot_semantic_drift_path
from lib.plot import plot, PlotType
from lib.wrapperFreq import wrapper_freq
from lib.plotNetwork import plotNetwork_new
from lib.plotSynonymStructure import plot_synonym_structure


#  TODO: document every function in comments with """COMMENT""" for help tool

# This is to remove the warning in plotNetwork - TODO: remove this if possible!
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


class Config(object):
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def cli(config, verbose):
    config.verbose = verbose


@cli.command()
def health():
    """Returns 'Healthy!' if macroscope is healthy"""
    click.echo("Healthy!")


# @cli.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet")
# @pass_config
# def hello(config, count, name):
#     """Simple program that greets NAME for a total of COUNT times."""

#     if config.verbose:
#         click.echo('verbose mode')

#     for _ in range(count):
#         click.echo("Hello, %s!" % name)


#  Ranges - from default settings in api
#  TODO: try to get everything to work for years between 1800 and 2000
closest_year_range = click.IntRange(1800, 1990)
context_change_year_range = click.IntRange(1800, 2000)
drift_year_range = click.IntRange(1800, 2000)
emotion_year_range = click.IntRange(1800, 2009)
frequency_year_range = click.IntRange(1800, 2009)
network_year_range = click.IntRange(1800, 2000)
synonym_network_year_range = click.IntRange(1800, 1990)


#  macroscope closest -w hello -y 1990
@cli.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-y", "--year", type=closest_year_range, required=True)
def closest(word, year):
    """Returns closest synonyms to word for a given year"""

    closestJson = closest_synonyms(word, year, 10, ClosestSearchMethod.SVD)

    words = closestJson[1][0]
    scores = closestJson[2][0]

    result = json.dumps({
        "words": words,
        "score": scores
    }, indent=4)
    click.echo(result)


#  macroscope context-change -w hello -y 1990 -y 2000
@cli.command()
@click.option("-w", "--word", required=True)
@click.option("-y", "--years", type=context_change_year_range, required=True, multiple=True)
def context_change(word, years):
    """Returns context change of search term over given period of years"""

    # TODO: pass k parameter as a none required parameter
    result = change_of_contextW(word, years, 40, True)
    click.echo(result)


#  macroscope cooccurrence -w hello -c there -c hi
@cli.command()
@click.option("-w", "--word", required=True)
@click.option("-c", "--context-words", required=True, multiple=True)
def cooccurrence(word, context_words):
    """Returns cooccurrence between target word and context words for every year"""

    normalize = False
    result = plot_co_occurence(word, context_words, normalize)
    click.echo(result)


#  macroscope drift -w hello -w there -s 1880 -e 1990
# TODO: this needs to be fixed for certain years and intervals - see plot_semantic_drift_path function for more info
@cli.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-s", "--start-year", type=drift_year_range, required=True)
@click.option("-e", "--end-year", type=drift_year_range, required=True)
def drift(word, start_year, end_year):
    """Returns drift of words over a given period"""

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


#  macroscope emotion -w hello -w there -s 1800 -e 2009 -t v
# TODO: only works if start year is 1800 AND end year is 2009
@cli.command()
@click.option("-w", "--word", required=True)  # TODO: should take multiple words?
@click.option("-s", "--start-year", type=emotion_year_range, required=True)
@click.option("-e", "--end-year", type=emotion_year_range, required=True)
@click.option("-t", "--type", required=True, type=click.Choice(['v', 'a', 'c']))
def emotion(word, start_year, end_year, type):
    click.echo(word)
    click.echo(start_year)
    click.echo(end_year)
    click.echo(type)

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

    result = plot(plotType, (word,), start_year, end_year)
    click.echo(result)

#  macroscope frequency -w hello -w there -s 1800 -e 2009
#  TODO: entire frequeny function needs to be looked at
#  TODO: only works if start year is 1800 AND end year is 2009
@cli.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-s", "--start-year", type=frequency_year_range, required=True)
@click.option("-e", "--end-year", type=frequency_year_range, required=True)
def frequency(word, start_year, end_year):
    click.echo(word)
    click.echo(start_year)
    click.echo(end_year)

    result = wrapper_freq(word, start_year, end_year)
    click.echo(result)


#  macroscope network -w hello -y 1990 -n 300 -r 0.7 -c 0.7 -f 3.5 -e 5 -d 70
@cli.command()
@click.option("-w", "--word", required=True)
@click.option("-y", "--year", type=network_year_range, required=True)
@click.option("-n", "--maximum-nodes", type=click.IntRange(10, 400), required=True)
@click.option("-r", "--context-relevance", type=click.FloatRange(0, 1), required=True)
@click.option("-c", "--context-cohesiveness", type=click.FloatRange(0, 1), required=True)
@click.option("-f", "--word-relevance", type=click.FloatRange(2, 4), required=True)  # -f for fitness
@click.option("-e", "--minimum-edges", type=click.IntRange(4, 6), required=True)
@click.option("-d", "--display-nodes", type=click.IntRange(20, 200), required=True)
# @click.option("-m", "--method", type=click.Choice(['PMI', 'COR']), required=True)
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


#  macroscope synonym-network -w hello -y 1990 -s 5 -t 0.72
@cli.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-y", "--year", type=synonym_network_year_range, required=True)
@click.option("-s", "--synonyms-per-target", type=click.IntRange(3, 10), required=True)
@click.option("-t", "--similarity-threshold", type=click.FloatRange(0.5, 1), required=True)
def synonym_network(word, year, synonyms_per_target, similarity_threshold):
    result = plot_synonym_structure(word, year, synonyms_per_target, similarity_threshold)
    click.echo(result)
