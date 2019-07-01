"""
cli.project
~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

import click
import fritz
from cli import print_utils
from cli.config import update_config


@click.command()
def projects():
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


@click.group()
def project():
    """Commands for working with Fritz Projects."""


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
@click.argument("project_id", required=False)
def set_active(project_id):
    """Set Project ID as the active project in fritz config."""
    if project_id:
        update_config(project_id=project_id)
        return

    projects = fritz.Project.list()

    row_format = [
        ("index", "{index:%s}", "Index"),
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
    projects.sort(key=lambda x: x.created_at, reverse=True)

    for i, project in enumerate(projects):
        row = {
            "index": "[" + str(i + 1) + "]",
            "name": project.name,
            "created": project.created_date,
            "project_id": project.id,
        }
        rows.append(row)

    print_utils.formatted_table(row_format, rows)

    index = click.prompt("Choose a project index to set as active", type=int)
    index = index - 1

    update_config(project_id=projects[index].id)
