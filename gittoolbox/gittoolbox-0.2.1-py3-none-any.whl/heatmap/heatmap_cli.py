from datetime import datetime, timedelta
import logging
import json
import re

import click

from gittoolbox.git.git_repo import GitRepo
from gittoolbox.heatmap.heatmap import Heatmap


def display_row(heatmap):
    """
    Display the information for one source file.

    :param heatmap: test files mapping
    """
    print(", ".join([f"{k}: {heatmap[k]}" for k in sorted(heatmap, key=heatmap.get, reverse=True)]))


@click.command('git-heatmap')
@click.option('--repo-location', required=True, help='Repository to analyze.')
@click.option('-t', '--test-regex', required=True, help='Regex to match test files.')
@click.option('-s', '--source-regex', required=True, help='Regex to match source files.')
@click.option('--months-back', default=None, type=int, help='Number of months to analyze.')
@click.option('--json', 'write_json', is_flag=True, help='Write output in json.')
@click.option('--normalize', is_flag=True, help='Normalize how often test files are seen.')
@click.option('--verbose', is_flag=True, help='Enable verbose logging.')
@click.option('--to-commit', default=None, help='Compute to the given commit.')
def create(repo_location, test_regex, source_regex, months_back, write_json, normalize, verbose,
           to_commit):
    """
    Create a heat map of which test files have been changed in the same commit as source files.

    This can then be used to help determine which tests would be good to run when a source
    file changes.
    \f

    :param repo_location: Location of git repository.
    :param test_regex: Regex to match test files.
    :param source_regex: Regex to match source files.
    :param months_back: How far back to look.
    :param write_json: Should output be written in json.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level)

    look_until = None
    if months_back:
        look_until = datetime.now() - timedelta(weeks=(4 * months_back))
    repo = GitRepo.local_repo(repo_location)
    test_re = re.compile(test_regex)
    source_re = re.compile(source_regex)

    heatmap = Heatmap.create_heatmap(repo, test_re, source_re, look_until, to_commit)
    if write_json:
        print(json.dumps(heatmap.get_heatmap(normalize), indent=4))
    else:
        heatmap_dict = heatmap.get_heatmap(normalize)
        for src in heatmap_dict:
            print(f'{src}: ', end='')
            display_row(heatmap_dict[src])

        print(f"Looked at {heatmap.commit_count} commits.")
