"""
cli.app
~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""
import os

from termcolor import colored

import click

import fritz
from cli.app import ios_setup, android_setup
from cli import print_utils
from cli import file_utils


# A decorator to pass the model to the currennt command.
# This searches the context command tree to
pass_app = click.make_pass_decorator(fritz.App)  # pylint: disable=invalid-name


@click.command()
@click.option("--project-id", help="Restrict results to specific project.")
@click.option("--apk-id", help="Restrict results to APK ID or Bundle ID.")
@click.option("--platform", help="Restrict results to specific platform.")
@click.option(
    "--all-projects", is_flag=True, help="Return results from all projects"
)
def apps(project_id=None, apk_id=None, platform=None, all_projects=False):
    """List all apps."""
    click.echo("")
    apps = fritz.App.list(
        project_id=project_id,
        apk_id=apk_id,
        platform=platform,
        all_projects=all_projects,
    )
    if all_projects:
        project_message = "all projects."
    else:
        project = fritz.Project.get(project_id or fritz.project_id)
        project_message = "{project_name} project.".format(
            project_name=project.name
        )

    apps_name = print_utils.make_plural(len(apps), "app")
    print_utils.notice(
        "{num_apps} {apps_name} in {project_message}\n".format(
            num_apps=len(apps),
            apps_name=apps_name,
            project_message=project_message,
        )
    )

    row_format = [
        ("name", "{name:%s}", "App Name"),
        ("apk_id", "{apk_id:%s}", "APK ID"),
        ("platform", "{platform:%s}", "Platform"),
        ("created", "{created:%s}", "Created"),
        ("project_name", "{project_name:%s}", "Project Name"),
        ("api_key", "{api_key:%s}", "API Key"),
        ("app_id", "{app_id:%s}", "App ID"),
    ]
    rows = []
    projects = {}
    for app in apps:
        project = projects.setdefault(
            app.project_uid, fritz.Project.get(app.project_uid)
        )
        row = {
            "name": app.app_name,
            "apk_id": app.apk_id,
            "platform": app.platform,
            "created": app.created_date,
            "project_name": project.name,
            "api_key": app.api_key,
            "app_id": app.id,
        }
        rows.append(row)

    rows.sort(key=lambda x: x["created"], reverse=True)
    print_utils.formatted_table(row_format, rows)


@click.group("app")
@click.argument("app-id", required=False)
@click.pass_context
def app_group(ctx, app_id=None):
    """Commands for working with Fritz Apps."""
    if app_id:
        ctx.obj = fritz.App.get(app_id=app_id)

    if ctx.obj and not ctx.invoked_subcommand:
        ctx.invoke(details)
        click.echo("")
        click.echo(ctx.command.get_help(ctx))


@app_group.command()
@pass_app
def details(app):
    """Get details of a specific app."""
    print_utils.message(app.summary())


@app_group.command()
def setup():
    """Get model grader report for a model version or Keras file.

    Args:
        version_id: Optional ModelVersion ID.
        path: Optional Path to model
    """
    cwd = os.getcwd()

    manifest_file_paths = file_utils.find_all("AndroidManifest.xml", cwd)
    info_file_paths = file_utils.find_all("Info.plist", cwd)

    if manifest_file_paths:
        print(colored("Setting up an Android app with Fritz...", "yellow"))
        android_setup.show_android_setup_steps(cwd)
        return

    if info_file_paths:
        print(colored("Setting up an iOS app with Fritz...", "yellow"))
        ios_setup.setup_ios_app()


@app_group.group()
def pod():
    """Commands for working with Fritz cocoapods."""


@pod.command()
@click.option("--clean", is_flag=True)
def install(clean):
    """Install the Fritz Cocoapod.

    Args:
        clean (bool): if present, delete cached cocoapods and update the
            repo as well.
    """
    commands = []
    if clean:
        commands.extend(
            [
                "pod repo update --verbose",
                "pod clean --verbose",
                "pod cache clean --all --verbose",
            ]
        )
    commands.append("pod install --verbose")
    for command in commands:
        print(command)
        os.system(command)
