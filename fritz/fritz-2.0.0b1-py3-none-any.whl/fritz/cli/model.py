"""
fritz.api_resources.model_version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""
import os

import click
from termcolor import colored

import fritz
from fritz.cli import print_utils


@click.group()
@click.pass_context
def model(ctx):
    """Commands for working with Fritz Models."""
    from fritz.cli import FritzNotConfiguredError

    try:
        fritz.configure()
    except fritz.errors.InvalidFritzConfigError:
        raise FritzNotConfiguredError()


@model.command()
@click.argument("model-id")
@click.option("--description", help="Updated model description")
@click.option("--active-version", type=int, help="Active model version.")
@click.option("--name", help="Name of model")
@click.option(
    "--is-global", help="If true, all projects and accounts can access model."
)
def update(model_id, **updates):
    updates = {
        key: value for key, value in updates.items() if value is not None
    }
    model = fritz.Model.get(model_id)
    model.update(**updates)


@model.command()
@click.argument("model-id")
@click.option(
    "--version-number",
    help="Specific version number. If not specified, uses latest",
)
def download(model_id, version_number=None):
    """Upload model version to Fritz API.

    Args:
        path: Path to model file.
        model_id: Model ID of existing model.
        deploy: If True, will deploy newly uploaded model.
    """
    model = fritz.Model.get(model_id)
    version, downloaded_path = model.download(version_number=version_number)
    print_utils.ack(
        (
            "Successfully downloaded {model_name} - {version_number} "
            "to {downloaded_path}"
        ).format(
            model_name=model.name,
            version_number=version.version_number,
            downloaded_path=downloaded_path,
        )
    )


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

    print_utils.message(fritz_model.summary())
    print_utils.message(version.summary())

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


@model.command()
@click.argument("model-id")
@click.pass_context
def details(ctx, model_id):
    """Get details about specific model.

    Args:
        id: Model ID to query.
    """

    model = fritz.Model.get(model_id)
    print_utils.message(model.summary())
    print()
    ctx.forward(list_versions)


@model.command()
@click.option("--project-id", help="Restrict results to Project ID")
@click.option(
    "--all-projects", help="List models from all projects", is_flag=True
)
def list(project_id=None, all_projects=False):
    """List all models."""
    row_format = [
        ("name", "{name:%s}", "Model Name"),
        ("framework", "{framework:%s}", "Framework"),
        ("version", "{version:%s}", "Active Version"),
        ("created", "{created:%s}", "Created"),
        ("model_id", "{model_id:%s}", "Model ID"),
    ]
    rows = []

    models = fritz.Model.list(project_id=project_id, all_projects=all_projects)

    if all_projects:
        project_message = "all projects."
    else:
        project = fritz.Project.get(project_id or fritz.project_id)
        project_message = project.name + " project."

    print_utils.notice(
        "\n{num_models} models in {project_message}\n".format(
            num_models=len(models), project_message=project_message
        )
    )

    for model in models:
        row = {
            "name": model.name,
            "framework": model.framework.name,
            "version": model.active_version,
            "created": model.created_date,
            "model_id": model.id,
        }
        rows.append(row)

    rows.sort(key=lambda x: x["created"], reverse=True)
    print_utils.formatted_table(row_format, rows)


@model.group()
def version():
    """Model version group."""


@version.command("list")
@click.argument("model_id")
def list_versions(model_id):
    """List Model Versions for a specific model_id."""
    versions = fritz.ModelVersion.list(model_id)
    model = fritz.Model.get(model_id)
    versions_name = print_utils.make_plural(len(versions), "version")
    print_utils.notice(
        "\n{num_versions} model {versions_name} in {model_name}\n".format(
            num_versions=len(versions),
            versions_name=versions_name,
            model_name=model.name,
        )
    )

    row_format = [
        ("filename", "{filename:%s}", "Provided Filename"),
        ("version", "{version:%s}", "Version"),
        ("created", "{created:%s}", "Created"),
        ("model_size", "{model_size:>%s}", "Model Size"),
        ("version_id", "{version_id:%s}", "Version ID"),
        ("loss", "{loss:%s.4}", "Loss"),
    ]
    rows = []

    for version in versions:
        row = {
            "filename": version.provided_filename,
            "version": version.version_number,
            "created": version.created_date,
            "model_size": version.model_size,
            "version_id": version.id,
            "loss": version.loss or "",
        }
        rows.append(row)

    rows.sort(key=lambda x: x["version"], reverse=True)
    print_utils.formatted_table(row_format, rows)


@version.command("details")
@click.argument("version_id")
def version_details(version_id):
    """Get Details for a specific Model Version.

    Args:
        version_id: Version ID to query.
    """
    version = fritz.ModelVersion.get(version_id)
    print_utils.message(version.summary())
