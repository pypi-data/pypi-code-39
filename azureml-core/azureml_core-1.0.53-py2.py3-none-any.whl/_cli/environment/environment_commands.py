# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


from azureml._cli.environment.environment_subgroup import EnvironmentSubGroup
from azureml._cli.cli_command import command
from azureml._cli import argument

from azureml.core.environment import Environment

ENVIRONMENT_NAME = argument.Argument(
    "environment_name", "--name", "-n", required=True,
    help="Name of the environment")
ENVIRONMENT_VERSION = argument.Argument(
    "environment_version", "--version", "-v", required=False,
    help="Version of the environment")


@command(
    subgroup_type=EnvironmentSubGroup,
    command="list",
    short_description="List environments in a workspace")
def list_environments(
        workspace=None,
        # We should enforce a logger
        logger=None):
    return list(workspace.environments.values())


@command(
    subgroup_type=EnvironmentSubGroup,
    command="show",
    short_description="Show an environment by name and optionally version",
    argument_list=[
        ENVIRONMENT_NAME,
        ENVIRONMENT_VERSION
    ])
def show_environment(
        workspace=None,
        environment_name=None,
        environment_version=None,
        # We should enforce a logger
        logger=None):
    return Environment.get(workspace, environment_name, environment_version)
