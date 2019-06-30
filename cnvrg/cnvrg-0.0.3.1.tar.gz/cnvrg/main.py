from cnvrg.subcommands.library import main as lib_cli
from cnvrg.subcommands.project import main as project_cli
from cnvrg.subcommands.cnvrg import main as cnvrg_cli
import click




cli = click.CommandCollection(sources=[lib_cli, project_cli, cnvrg_cli])



if __name__ == '__main__':
    cli()
















