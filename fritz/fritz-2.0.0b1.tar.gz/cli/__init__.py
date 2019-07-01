"""
Fritz CLI

usage:
   $ fritz model upload my_keras_file.h5
   $ Model Details
     =============
     Model ID:       6bd0fbb59f264a3c8b79e963558848e2
     Model Name:      multi_person_mobilenet_v1_075_float
     Active version:  1

     Model Version Details
     ======================
     Model Version ID:  420fd0b3ef5e4fc48a5b535244d0c0a3
     Version Number:     1
   $ fritz model benchmark --version-id 420fd0b3ef5e4fc48a5b535244d0c0a3
     ------------------------
     Fritz Model Grade Report
     ------------------------
     Core ML Compatible:              True
     Predicted Runtime (iPhone X):    31.4 ms (31.9 fps)
     Total MFLOPS:                    686.90
     Total Parameters:                1,258,580

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

import sys
from pkg_resources import iter_entry_points
import click
from termcolor import colored
from click_plugins import with_plugins
import fritz
from cli.config import config
from cli.model import model
from cli.model import models
from cli.app import app_group
from cli.app import apps
from cli import project as project_cli


class FritzNotConfiguredError(click.UsageError):
    """Error raised when Fritz CLI has not been configured."""

    def __init__(self, ctx=None):
        message = (
            "Please configure Fritz API Key and Project ID:\n"
            "\n  $ fritz config\n"
        )
        super().__init__(message, ctx=ctx)


@click.group()
@click.pass_context
def main(ctx):
    """Fritz CLI."""
    # fritz config subcommand will enable fritz.configure() to work.
    # If that is the subcommand, don't call fritz.configure().
    if ctx.invoked_subcommand == "config":
        return

    fritz.configure()


@with_plugins(iter_entry_points("fritz.plugins"))
@main.group()
@click.argument("feature", type=click.Choice(["style_transfer"]))
def train(feature):
    """Commands for using Fritz training tools."""
    print(colored("Feature: %s" % feature, "green"))


main.add_command(config)
main.add_command(models)
main.add_command(model)
main.add_command(apps)
main.add_command(app_group)
main.add_command(project_cli.project)
main.add_command(project_cli.projects)
