"""
fritz.cli.project
~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

import click
import fritz
from fritz.cli import print_utils
from fritz.cli.config import update_config


@click.group()
def project():
    """Commands for working with Fritz Projects."""
    from fritz.cli import FritzNotConfiguredError

    try:
        fritz.configure()
    except fritz.errors.InvalidFritzConfigError:
        raise FritzNotConfiguredError()


@project.command()
@click.argument("ID", required=False)
def details(id=None):
    """Get details of project.

    Args:
        id: Optional Project ID. If not specified, will use project ID
            specified in Fritz Config.
    """
    project = fritz.Project.get(project_id=id)
    project.summary()


@project.command()
def list():
    """List all Projects for current account."""

    row_format = [
        ("name", "{name:%s}", "Project Name"),
        ("created", "{created:%s}", "Created"),
        ("project_id", "{project_id:%s}", "Project ID"),
    ]
    rows = []

    projects = fritz.Project.list()
    projects_name = print_utils.make_plural(len(projects), "project")
    print_utils.notice(
        "\n {num_projects} {projects_name}\n".format(
            num_projects=len(projects), projects_name=projects_name
        )
    )

    for project in projects:
        row = {
            "name": project.name,
            "created": project.created_date,
            "project_id": project.id,
        }
        rows.append(row)

    rows.sort(key=lambda x: x["created"], reverse=True)
    print_utils.formatted_table(row_format, rows)


@project.command()
@click.argument("project_id")
def set_active(project_id):
    """Set Project ID as the active project in fritz config."""
    update_config(project_id=project_id)
