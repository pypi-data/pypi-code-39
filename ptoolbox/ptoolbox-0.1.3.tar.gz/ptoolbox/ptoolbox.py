import click
from dsa import dsa
from hackerrank import hackerrank


@click.group()
def cli():
    """
    Problem Toolbox - Problem CLI tools by Thuc Nguyen (https://github.com/thucnc)
    """
    click.echo("Problem Toolbox - Problem CLI tools by Thuc Nguyen (https://github.com/thucnc)")


@cli.group(name='dsa')
def dsa_group():
    """
    DSA problem tools
    """
    click.echo("Common DSA tools")


@cli.group(name='hackerrank')
def hackerrank_group():
    """
    Hackerrank tools
    """
    click.echo("hackerrank.com tools")


@dsa_group.command()
@click.option('-d', '--dir', default='.',
              type=click.Path(file_okay=False),
              prompt='Base directory for the problem', help='Base folder for the problem')
@click.option('--overwrite/--no-overwrite', default=False, help='Overwrite existing folder, default - No')
@click.argument('problem', metavar='{problem}')
def create_problem(dir, overwrite, problem):
    """
    Create a problem boilerplate

    Syntax:
    ptoolbox dsa create-problem -d {folder} {problem-code} [--overwrite]

    Ex.:
    ptoolbox dsa create-problem -d problems/ prob2 --overwrite

    """
    dsa.create_problem(dir, problem, overwrite=overwrite)


@hackerrank_group.command()
@click.option('--keep-zip-file-only/--keep-intermediate-files', default=True, help='Remove intermediate files, default - Yes')
@click.argument('problem_folder', metavar='{problem_folder}')
def prepare_testcases(keep_zip_file_only, problem_folder):
    """
    Convert testcases to hackerrank format, and compress into .zip file, ready for upload

    Syntax:
    ptoolbox hackerrank prepare-testcases  {problem-folder} [--keep-zip-file-only/--keep-intermediate-files]

    Ex.:
    ptoolbox hackerrank prepare-testcases problems/prob2

    """
    hackerrank.prepare_testcases(problem_folder, keep_zip_file_only=keep_zip_file_only)
