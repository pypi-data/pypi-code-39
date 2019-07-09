import click

from dong.project import init_project

@click.command()
@click.argument('project', required = True)
def new(project):
    """Create a new ML project"""
    init_project(project)
