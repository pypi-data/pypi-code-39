import click
import os
import dong
import pkg_resources 

version_number = pkg_resources.require("dong")[0].version
@click.command(help='Print version and exit.', add_help_option=False)
def version():
    click.secho("dong " + version_number, fg='green')
