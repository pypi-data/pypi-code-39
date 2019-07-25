# External libraries
import click

# Standard library
import json

# Local libraries
from lib.closestSynonyms import closest_synonyms
from lib.enums import ClosestSearchMethod
from lib.globals import closest_year_range

#  macroscope closest -w hello -y 1990
@click.command()
@click.option("-w", "--word", required=True, multiple=True)
@click.option("-y", "--year", type=closest_year_range, required=True)
def closest(word, year):
    """Returns closest synonyms to word for a given year."""

    closestJson = closest_synonyms(word, year, 10, ClosestSearchMethod.SVD)

    words = closestJson[1][0]
    scores = closestJson[2][0]

    result = json.dumps({
        "words": words,
        "score": scores
    }, indent=4)
    click.echo(result)
