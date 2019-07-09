import click
from inputHandler import *
from metricConverter import *


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
    oFile = open(pathname, 'r+')
    handler = InputHandler()
    units = handler.parseInput(oFile.read())
    converter = MetricConverter()
    convertedUnits = converter.convert(units)
    handler.writeToFile(writepath, convertedUnits)


if __name__ == '__main__':
    main()
