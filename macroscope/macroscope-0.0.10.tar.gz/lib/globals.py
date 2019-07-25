import os
import click

# TODO: remove
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
dataDir = parentDir + '/data'
# ----------

configFileName = 'macroscope-config.json'
dataDirPropName = 'dataDirectoryAbsolutePath'

#  Ranges - from default settings in api
#  TODO: try to get everything to work for years between 1800 and 2000
closest_year_range = click.IntRange(1800, 1990)
context_change_year_range = click.IntRange(1800, 2000)
drift_year_range = click.IntRange(1800, 2000)
emotion_year_range = click.IntRange(1800, 2009)
frequency_year_range = click.IntRange(1800, 2009)
network_year_range = click.IntRange(1800, 2000)
synonym_network_year_range = click.IntRange(1800, 1990)
