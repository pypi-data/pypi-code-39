import os
from pathlib import Path

import click
import yaml
from loguru import logger

from helper import HermesDataPoster

FROM_FILE = 10001
CONFIG_PATH = os.path.join(Path(__file__).parent.absolute(), 'config.yml')

config = None
try:
    with open(CONFIG_PATH) as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
        stream.close()
        del stream
except Exception as e:
    logger.error(e)
    raise e


@click.command()
@click.option('--gpx', prompt='Enter gpx file name', help='gpx file name')
@click.option('--tt', prompt='Enter transport type', help='transport type:\n0 - fleet,\n1- trade agent')
@click.option('--trid', default=FROM_FILE, help='Transport item identifier')
def export(gpx: str, tt, trid):
    """Simple program that greets NAME for a total of COUNT times."""
    if(trid == FROM_FILE):
        date, id = gpx.split('.')[0].split('_')
        cfg = {
            'file': gpx,
            'transport-type': tt,
            'transport-id': id,
            'event_date': date,
            'config': config
        }
    else:
        cfg = {
            'file': gpx,
            'transport-type': tt,
            'transport-id': trid,
            'event_date': 131977014053907839,
            'config': config
        }
    helper = HermesDataPoster(**cfg)
    helper.export()


if __name__ == '__main__':
    export()
