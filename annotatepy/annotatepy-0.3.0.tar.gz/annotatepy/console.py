import argparse
import json
import logging
import os
import sys

from annotatepy.annotate import generate_annotations

logger = logging.getLogger("annotatepy")


def make_parser():
    parser = argparse.ArgumentParser(
        description="Generate sourcehut annotations",
        epilog="https://git.sr.ht/~ihabunek/annotatepy/",
    )

    parser.add_argument(
        "-r", "--root",
        type=str,
        default=os.getcwd(),
        help="project root (defaults to working dir)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="enable verbose logging"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="disable logging"
    )

    parser.add_argument(
        "source_paths",
        type=str,
        nargs="*",
        help="one or more paths within the project containing the code to be "
             "annotated (defaults to project root)"
    )

    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    project_root = os.path.abspath(args.root)
    source_paths = [os.path.join(project_root, p) for p in args.source_paths]

    if not args.quiet:
        level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(level=level)

    annotations = generate_annotations(project_root, source_paths)

    json.dump(annotations, sys.stdout, indent=2)
