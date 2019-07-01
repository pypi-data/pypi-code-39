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
import os
from pathlib import Path
import configparser

import click
from termcolor import colored

import fritz
from fritz import configuration

_HOME = str(Path.home())
CONFIG_PATH = os.path.join(_HOME, ".fritz")


class FritzNotConfiguredError(click.UsageError):
    """Error raised when Fritz CLI has not been configured."""

    def __init__(self, ctx=None):
        message = (
            "Please configure Fritz API Key and Project ID:\n"
            "\n  $ fritz config\n"
        )
        super().__init__(message, ctx=ctx)


def update_config(path: str = CONFIG_PATH, **updates):
    """Update Fritz configuration file, creating if it does not exist.

    Args:
        path (str): Path of config file.
        updates (dict): Optional keys to update specified by CLI options.

    Return: ConfigParser
    """
    fritz_config = configuration.load_config_file(path=path)

    if updates:
        try:
            defaults = configuration.get_credentials(fritz_config)
        except configparser.NoSectionError:
            defaults = {}

        changes = []
        for key in ["api_key", "project_id"]:
            if key not in updates:
                continue

            original = defaults.get(key)
            new = updates[key]
            changes.append(f"{key}: {original} -> {new}")

        print(
            "\n".join(["Updating config with provided variables.", *changes])
        )

        fritz_config = configuration.update_credentials(
            fritz_config, **updates
        )
        configuration.write_config_file(fritz_config, path=path)
        return fritz_config

    print(
        f"""
    Configure the Fritz CLI.
    ------------------------

    This command will add a ~/.fritz configuration file with your API Key
    and default Project ID.

    The API Key is used to authenticate with the Fritz servers, and the
    Project ID is used to determine whcih project to use when creating and
    benchmarking new models.

    To find your API Key and Project ID, log in to Fritz (https://app.fritz.ai)
    and go to the "Training" tab in you project. Enter the listed API Key and
    Project ID in the following prompts:

    """
    )
    api_key = click.prompt("Fritz API Key", type=str)
    project_id = click.prompt("Fritz Project ID", type=str)

    updates = {"api_key": api_key, "project_id": project_id}
    configuration.update_credentials(fritz_config, **updates)
    configuration.write_config_file(fritz_config, path=path)
    return fritz_config


def _get_config_key(key):
    if key not in ["api_key", "project_id"]:
        return None

    configuration.init_config()
    return getattr(fritz, key, None)


@click.group()
def main():
    """Fritz CLI."""


@main.group(invoke_without_command=True)
@click.pass_context
def config(ctx):
    """Fritz configuration settings.

    Args:
        update: Optional flag to update config file.
    """
    if ctx.invoked_subcommand is not None:
        # Don't want to run default flow if specifically trying to update.
        return

    try:
        configuration.init_config()
    except fritz.errors.InvalidFritzConfigError:
        update_config()

    message = "Fritz Configuration"
    print(message)
    print("=" * len(message))
    print(f"API Key: {fritz.api_key}")
    print(f"Project ID: {fritz.project_id}")


@config.command()
@click.option("--api-key", help="Fritz API Key", default=None)
@click.option("--project-id", help="Fritz Project ID", default=None)
def update(api_key, project_id):
    """Fritz configuration settings.

    Args:
        update: Optional flag to update config file.
    """
    updates = {"api_key": api_key, "project_id": project_id}
    updates = {key: value for key, value in updates.items() if value}
    update_config(**updates)
    fritz.configure()

    message = "Fritz Configuration"
    print(message)
    print("=" * len(message))
    print(f"API Key: {fritz.api_key}")
    print(f"Project ID: {fritz.project_id}")


@main.group()
def model():
    """Commands for working with Fritz Models."""
    try:
        fritz.configure()
    except fritz.errors.InvalidFritzConfigError:
        raise FritzNotConfiguredError()


@model.command()
@click.option("--model-id", default=None)
@click.option("--deploy", is_flag=True, flag_value=True)
@click.option("--api-key", help="Fritz API Key")
@click.option("--project-id", help="Fritz Project ID")
@click.argument("path")
def upload(path, model_id=None, deploy=False, api_key=None, project_id=None):
    """Upload model version to Fritz API.

    Args:
        path: Path to model file.
        model_id: Model ID of existing model.
        deploy: If True, will deploy newly uploaded model.
    """
    filename = os.path.basename(path)
    model_file = fritz.frameworks.build_framework_file(path)
    version, snapshot, fritz_model = fritz.ModelVersion.create(
        filename=filename,
        data=model_file.to_bytes(),
        model_id=model_id,
        set_active=deploy,
        api_key=api_key,
        project_id=project_id,
    )

    print("\nModel Details")
    print("=============")
    print(f"Model ID:       {fritz_model.id}")
    print(f"Model Name:      {fritz_model.name}")
    print(f"Active version:  {fritz_model.active_version}")

    print("\nModel Version Details")
    print("=====================")
    print(f"Model Version ID:  {version.id}")
    print(f"Version Number:     {version.version_number}")

    return version, snapshot, model


@model.command()
@click.option("--version-id", help="Existing model version.")
@click.option("--api-key", help="Fritz API Key")
@click.argument("path", required=False)
@click.pass_context
def benchmark(ctx, version_id=None, path=None, api_key=None):
    """Get model grader report for a model version or Keras file.

    Args:
        version_id: Optional ModelVersion ID.
        path: Optional Path to model
    """
    if not version_id and not path:
        print(colored("Version ID or path to model required.", "yellow"))
        return
    if not version_id:
        version, _, _ = ctx.invoke(upload, path=path)
    else:
        version = fritz.ModelVersion.get(version_id, api_key=api_key)

    report = version.benchmark()
    report.summary()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
