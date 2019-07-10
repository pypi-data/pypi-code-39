import click
import importlib
from universal_translator import inputHandler
from universal_translator import metricConverter


@click.command()
@click.option('--pathname', help="path to file that will be read", default='')
@click.option('--writepath', help="path to file that will get written", default='output.txt')
def main(pathname: str, writepath: str):
    if pathname == '':
        print('please specify a path to read from.')
        return
    if writepath == '':
        print('please specify a path to write to.')
        return
    oFile = open(pathname, 'r+', encoding="utf-8")
    handler = inputHandler.InputHandler()
    units = handler.parseInput(oFile.read())
    converter = metricConverter.MetricConverter()
    convertedUnits = converter.convert(units)
    handler.writeToFile(writepath, convertedUnits)
    print('Done! :)')
