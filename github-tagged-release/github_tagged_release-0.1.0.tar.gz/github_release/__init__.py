from __future__ import absolute_import
from argparse import ArgumentParser

__version__ = VERSION = "0.1.0"

from .github_release import GitHubRelease


def main():
    parser = ArgumentParser()
    parser.add_argument("--changelog", action="store_true", dest="changelog", help="Show changelog only (skip release)")
    parser.add_argument("--git-dir", dest="git_dir", help="Override GIT_DIR (default: '.')")
    parser.add_argument("--tag", dest="tag", help="Changelog for specific tag (default: CIRCLE_TAG)")
    parser.add_argument("--version", action="version", version=VERSION)

    options = vars(parser.parse_args())
    ghr = GitHubRelease(options)

    if options["changelog"]:
        ghr.changelog()
    else:
        ghr.create_release_from_tag()


if __name__ == "__main__":
    main()
