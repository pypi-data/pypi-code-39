import click
import gitlab
from xml.etree import ElementTree as ET


@click.command()
@click.option("--auth")
@click.argument('user')
def create_manifest(auth, user):
    if auth:
        gl = gitlab.Gitlab.from_config(auth)
    else:
        gl = gitlab.Gitlab("https://gitlab.com")

    if user == "*":
        projects = gl.projects.list(as_list=False, per_page=25)
    else:
        user = gl.users.list(username=user)[0]
        projects = user.projects.list(as_list=False, per_page=25)

    root = ET.Element("manifest")
    projects_element = ET.SubElement(root, "projects")

    for project in projects:
        ET.SubElement(projects_element, "project", attrib={
            "name": project.name,
            "remote": project.ssh_url_to_repo,
            "path": project.path_with_namespace
        })
    contents = ET.tostring(root)
    click.echo(contents)


@click.command()
@click.argument("manifest_file", default=".jiri_manifest", type=click.Path(exists=True, dir_okay=False))
def list_projects(manifest_file):
    root = ET.parse(manifest_file)
    for project in root.findall('./projects/project'):
        click.echo(project.attrib['path'])


if __name__ == '__main__':
    create_manifest()
