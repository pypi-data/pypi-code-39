#!/usr/bin/python3
from .git_values import GitValues
from .meta import __version__
from .reckoner_file_updater import ReckonerFileUpdater
from .reckoner_file_creator import ReckonerFileCreator
from .s3_values import S3Values
from pathlib import Path
import click
import coloredlogs
import json
import os


@click.group()
@click.option('--debug/--no-debug', default=False)
def cmd(debug):
    pass

@cmd.command()
@click.option('--namespace', default="default", help='The namespace for the release')
@click.option('--chart', required=True, help='The name of the chart')
@click.option('--app', required=True, help='The app name for the release')
@click.option('--extrafiles', help='Extra file names to search for')
@click.option('--extravalues', help='Full paths to extra values files')
@click.option('--destination', default="/tmp", help='The destination for downloaded values files')
@click.option('--output', required=True, default='json', help='The output type (helm, json)', type=click.Choice(['json', 'helm']))
@click.option('--region', default=False, help='The target region')
@click.option('--colour', default=os.getenv('COLOUR'), help='The cluster colour')
@click.option('--envname', default=os.getenv('ENVNAME'), help='The cluster env name')
@click.option('--download-once/--always-download', 'download_once', default=False, help="Only download values if they don't already exist locally")
def values(namespace, chart, app, extrafiles, extravalues, destination, output, region, colour, envname, download_once):
    """Build all possible s3 paths for values files"""
    if extrafiles == None:
        extrafiles = []
    else:
        extrafiles = extrafiles.split(',')
    if extravalues == None:
        extravalues = []
    else:
        extravalues = extravalues.split(',')

    bp = GitValues(namespace=namespace,
            chart=chart,
            app=app,
            colour=colour,
            envname=envname,
            region=region,
            extra_files=extrafiles,
            extra_values=extravalues,
            download_once=download_once
    )

    downloaded = bp.download_values(destination)

    if output == 'json':
        print(json.dumps(downloaded))
    elif output == 'helm':
        helm_args = ''
        for file in downloaded:
            helm_args = helm_args + ' --values ' + file
        print(helm_args)

@cmd.command()
@click.option('--namespace', default="default", help='The namespace for the release')
@click.option('--chart', required=True, help='The name of the chart')
@click.option('--app', required=True, help='The app name for the release')
@click.option('--extrafiles', help='Extra file names to search for')
@click.option('--extravalues', help='Full paths to extra values files')
@click.option('--destination', default="/tmp", help='The destination for downloaded values files')
@click.option('--output', required=True, default='json', help='The output type (helm, json)', type=click.Choice(['json', 'helm']))
@click.option('--region', default=False, help='The target region')
@click.option('--colour', default=os.getenv('COLOUR'), help='The cluster colour')
@click.option('--envname', default=os.getenv('ENVNAME'), help='The cluster env name')
@click.option('--download-once/--always-download', 'download_once', default=False, help="Only download values if they don't already exist locally")
def possible_values(namespace, chart, app, extrafiles, extravalues, destination, output, region, colour, envname, download_once):
    """Build all possible s3 paths for values files"""
    if extrafiles == None:
        extrafiles = []
    else:
        extrafiles = extrafiles.split(',')
    if extravalues == None:
        extravalues = []
    else:
        extravalues = extravalues.split(',')

    bp = GitValues(namespace=namespace,
            chart=chart,
            app=app,
            colour=colour,
            envname=envname,
            region=region,
            extra_files=extrafiles,
            extra_values=extravalues,
            download_once=download_once
    )

    possible = bp.get_required_files()

    print(json.dumps(possible))

@cmd.command()
def version():
    """ Takes no arguments, outputs version info"""
    print(__version__)

@cmd.command()
@click.option('--source', required=True, help='The source autohelm file', type=click.Path(exists=True))
@click.option('--dest', required=True, help='The destination autohelm file')
@click.option('--region', required=True, help='The target region')
@click.option('--values', required=True, help='Path to the values files')
#@click.option('--values-prefix', required=True, help='Prefix to add to the values files in the autohelm file.')
def update_reckoner_file(source, dest, region, values):
    rfu = ReckonerFileUpdater(source=source, dest=dest, region=region, download_path=values)
    rfu.update()

@cmd.command()
@click.option('--namespace', required=True, help='The source namespace')
@click.option('--region', default="eu-west-2", required=True, help='The target region')
@click.option('--values', required=True, help='Path to the values files')
@click.option('--repository', multiple=True)
@click.option('--colour', required=True)
@click.option('--envname', required=True)
@click.option('--use-latest-chart-version', default=False)
@click.option('--output-file', required=True)
def create_reckoner_file(namespace, region, values, repository, colour, envname, use_latest_chart_version, output_file):
    repositories = {}
    for repository_item in repository:
        repository_item = repository_item.split(',', 2)
        repositories[repository_item[0]] = repository_item[1]

    rfc = ReckonerFileCreator(
        namespace=namespace,
        region=region,
        download_path=values,
        repositories=repositories,
        envname=envname,
        colour=colour,
        use_latest_chart_version=use_latest_chart_version,
        output_file=output_file
    )
    rfc.create()

if __name__ == '__main__':
    cmd()
