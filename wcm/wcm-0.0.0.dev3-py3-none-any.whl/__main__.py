# -*- coding: utf-8 -*-
"""
wcm.

:license: Apache 2.0
"""

import logging
import sys
from pathlib import Path

import click

import wcm
from wcm import _component, _utils


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()


@cli.command(help="Show wcm version.")
def version():
    click.echo(f"{Path(sys.argv[0]).name} v{wcm.__version__}")


@cli.command(help="Initialize a directory for a new package.")
@click.argument(
    "package",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, exists=True),
    default=".",
)
def init(package):
    click.secho(f"Success", fg="green")


@cli.command(help="Deploy the pacakge to the wcm.")
@click.option("--debug", "-d", is_flag=True, type=bool, default=False)
@click.option("--dry-run", "-n", is_flag=True, type=bool, default=False)
@click.argument(
    "package",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, exists=True),
    default=".",
)
def publish(package, debug=False, dry_run=False):
    logging.info("Create transformation catalog")
    _component.deploy_component(package, "./config.ini", debug=debug, dry_run=dry_run)
    click.secho(f"Success", fg="green")
