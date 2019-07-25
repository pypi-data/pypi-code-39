# External libraries
import click

# Local libraries
from lib.jsonfs import getJsonFromFile, writeJsonToFile
from lib.globals import configFileAbsolutePath, dataDirPropName, parentDir

from lib.commands.closest import closest
from lib.commands.context_change import context_change
from lib.commands.co_occurrence import co_occurrence
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
    # Get config from file. If the file is not found then we create one and write "{}"
    fileConfig = {}
    try:
        fileConfig = getJsonFromFile(configFileAbsolutePath)
    except FileNotFoundError:
        writeJsonToFile(configFileAbsolutePath, fileConfig)

    if data_dir is not None and len(data_dir) > 0:
        fileConfig[dataDirPropName] = data_dir
        writeJsonToFile(configFileAbsolutePath, fileConfig)

    dataDirectoryAbsolutePath = fileConfig.get(dataDirPropName)
    if not dataDirectoryAbsolutePath:
        value = click.prompt('Please specify the absolute path of the Macroscope data directory', type=str)
        fileConfig[dataDirPropName] = value
        writeJsonToFile(configFileAbsolutePath, fileConfig)


@click.group()
@click.option('--data-dir', help='The absolute path of the Macroscope data directory.')
def cli(data_dir):
    setConfigValues(data_dir)


@cli.command()
def health():
    """Returns 'Healthy!' if macroscope is healthy."""
    click.echo("Healthy!")


# @cli.command()
# def set_data_dir():
#     """Sets the absolute path where macroscope will look for the data."""
#     click.echo("Not implemented")


cli.add_command(health)
cli.add_command(closest)
cli.add_command(context_change)
cli.add_command(co_occurrence)
cli.add_command(drift)
cli.add_command(emotion)
cli.add_command(frequency)
cli.add_command(network)
cli.add_command(synonym_network)
