import argparse
import json
import logging
import os

from annotatepy.annotate import generate_annotations

logger = logging.getLogger("annotatepy")


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Generate sourcehut annotations",
        epilog="https://git.sr.ht/~ihabunek/annotatepy/",
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="annotations.json",
        help="output file (default: annotations.json)"
    )

    parser.add_argument(
        "-r", "--root",
        type=str,
        default=os.getcwd(),
        help="project root (defaults to working dir)"
    )

    parser.add_argument(
        "source_paths",
        type=str,
        nargs="*",
        help="one or more paths within the project containing the code to be "
             "annotated (defaults to project root)"
    )

    args = parser.parse_args()
    project_root = os.path.abspath(args.root)
    source_paths = [os.path.join(project_root, p) for p in args.source_paths]

    logger.info(f"Project: {project_root}")

    annotations = generate_annotations(project_root, source_paths)

    logger.info(f"Saving annotations to: {args.output}")
    with open(args.output, "w") as f:
        json.dump(annotations, f, indent=2)
