import click
import webbrowser
import os
from dong import utils

@click.group()
def local():
    """Local test."""
    pass

@local.command()
@click.option('--package-path', default=None, help='Path to the training program python package. Default to ./PROJECT_NAME and PROJECT_NAME got from ./setup.py')
@click.argument('args', nargs=-1, metavar='[-- [ARGS]]')
@click.pass_context
def train(ctx, package_path, args):
    """Execute local training test with [ARGS].
    """

    setup_py_path = './setup.py' if package_path is None else os.path.join(os.path.dirname(package_path),
                                                                           'setup.py')
    module_name = utils.get_project_name(setup_py_path)
    if module_name == '' or len(module_name.split('/')) > 1:
        click.secho('setup.py not found under ' + ('current working directory' if package_path is None else os.path.dirname(package_path)),
                    fg='red',
                    err=True)
        ctx.exit(1)
        return

    if package_path is None:
        package_path = './' + module_name        

    print('Only support HELP message for local train for now')
    print('Use dong ML project: ' + module_name)
    print('Project path: ' + os.path.abspath(os.path.dirname(package_path)))
    print('Opening target project homepage......')
    webbrowser.open(utils.get_project_url(setup_py_path), new=2)
    
