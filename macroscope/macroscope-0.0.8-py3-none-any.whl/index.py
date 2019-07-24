# External libraries
import click

# Local libraries
from lib.jsonfs import getJsonFromFile, writeJsonToFile

from lib.commands.closest import closest
from lib.commands.context_change import context_change
from lib.commands.cooccurrence import cooccurrence
from lib.commands.drift import drift
from lib.commands.emotion import emotion
from lib.commands.frequency import frequency
from lib.commands.network import network
from lib.commands.synonym_network import synonym_network

#  TODO: document every command """COMMENT""" for help tool

# This is to remove the warning in plotNetwork - TODO: remove this if possible! ------------
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
# ------------------------------------------------------------------------------------------


def setConfigValues(data_dir: str):
    configFileName = 'macroscope-config.json'
    dataDirPropName = 'dataDirectoryAbsolutePath'

    # Get config from file. If the file is not found then we create one and write "{}"
    fileConfig = {}
    try:
        fileConfig = getJsonFromFile(configFileName)
    except FileNotFoundError:
        writeJsonToFile(configFileName, fileConfig)

    if data_dir is not None and len(data_dir) > 0:
        fileConfig[dataDirPropName] = data_dir
        writeJsonToFile(configFileName, fileConfig)

    dataDirectoryAbsolutePath = fileConfig.get(dataDirPropName)
    if not dataDirectoryAbsolutePath:
        value = click.prompt('Please specify the absolute path of the Macroscope data directory', type=str)
        fileConfig[dataDirPropName] = value
        writeJsonToFile(configFileName, fileConfig)


@click.group()
@click.option('--data-dir', help='The absolute path of the Macroscope data directory.')
def cli(data_dir):
    setConfigValues(data_dir)


@cli.command()
def health():
    """Returns 'Healthy!' if macroscope is healthy."""
    click.echo("Healthy!")


cli.add_command(health)
cli.add_command(closest)
cli.add_command(context_change)
cli.add_command(cooccurrence)
cli.add_command(drift)
cli.add_command(emotion)
cli.add_command(frequency)
cli.add_command(network)
cli.add_command(synonym_network)
