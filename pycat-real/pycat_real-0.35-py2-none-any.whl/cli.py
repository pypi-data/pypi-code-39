from pycat import show
from pycat import config
import click

@click.command()
@click.argument('path')
@click.option('--imgprotocol/--no-imgprotocol', default=True)
def pycat(path, imgprotocol):
    config.set_img_protocol_support(imgprotocol)
    show(path)