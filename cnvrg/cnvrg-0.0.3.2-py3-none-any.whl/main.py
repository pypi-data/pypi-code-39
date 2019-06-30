import click
import os
import cnvrg.actions.project_actions  as project_actions
import cnvrg.helpers.cli_helper as cli_helper
from cnvrg.modules.library import Library
from cnvrg.helpers.logger_helper import log_message
import json
@click.group()
@click.option("--log-level", default="INFO", help="log level")
def cli(log_level):
    pass

@cli.command()
@click.option('--working_dir', '-w', default=os.getcwd(), help='working dir')
@click.option('--commit', '-c', default="latest", help='commit to clone')
@click.argument("project_path")
def clone(project_path, **kwargs):
    project_actions.clone(project_path)

@cli.command()
def download():
    project_actions.download()


@cli.command()
def upload():
    project_actions.upload()


@cli.group("library")
def library():
    pass

@library.command()
@click.argument("library_title")
def info(library_title):
    l = Library(library_title)
    cli_helper.print_object(l.info())


@library.command()
@click.argument("library_title")
@click.option('--working_dir', '-w', default=os.getcwd(), help='working dir')
def clone(library_title, working_dir):
    l = Library(library_title)
    library_path = l.load(working_dir=working_dir)
    log_message("You can find the library in {path}".format(path=library_path), fg='green')



@library.command()
@click.argument("library_title")
@click.option("--local/--remote", default=False)
@click.option("--arg", multiple=True)
@click.option("--dataset", multiple=True)
@click.option("--compute", multiple=True)
@click.option("--working_dir", help="directory to run from")
def run(library_title, local, arg, dataset, working_dir, compute):
    arguments = cli_helper.parse_args(arg)
    datasets = cli_helper.parse_datasets(dataset)
    l = Library(library_title)
    if local:
        l.load(working_dir=working_dir)
        l.run_local(args=arguments)
        return
    l.run(arguments=arguments, datasets=datasets, computes=compute)











