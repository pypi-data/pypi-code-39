"""Build the documentation for a package."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess

from ..utils import CONFIGS


BASE_DIR = CONFIGS["base_dir"]
PACKAGE_NAME = CONFIGS["package_name"]
DOC_BUILD_TYPES = CONFIGS["doc_build_types"]

DOCS_OUTPUT_DIRECTORY = "docs"
DOCS_WORKING_DIRECTORY = "_docs"


def _api():
    sphinx_apidoc_cmd = [
        "poetry",
        "run",
        "sphinx-apidoc",
        "--output-dir",
        DOCS_WORKING_DIRECTORY,
        "--no-toc",
        "--force",
        "--module-first",
    ]
    print(f"Building {PACKAGE_NAME} API docs")
    subprocess.check_call(sphinx_apidoc_cmd + [PACKAGE_NAME], cwd=BASE_DIR)


BUILDERS = {"api": _api}


def build():
    """Build the docs."""
    # Setup environment variables
    commit_id = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=BASE_DIR, universal_newlines=True
    )
    os.environ["GIT_COMMIT_ID"] = commit_id.rstrip("\n")

    origin_url = subprocess.check_output(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=BASE_DIR,
        universal_newlines=True,
    )
    os.environ["GIT_ORIGIN_URL"] = origin_url.rstrip("\n")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dirty",
        action="store_true",
        help="Leave the output directory untouched before starting to build documents",
    )
    args = parser.parse_args()

    if not args.dirty:
        shutil.rmtree(str(BASE_DIR / DOCS_OUTPUT_DIRECTORY), ignore_errors=True)
        shutil.rmtree(str(BASE_DIR / DOCS_WORKING_DIRECTORY), ignore_errors=True)

    for builder in DOC_BUILD_TYPES:
        if builder not in BUILDERS:
            print(f'No builder for value "{builder}" defined!')
            exit(1)
        BUILDERS[builder]()

    # Copy over all the top level rST files so we don't
    # have to keep a duplicate list here.
    for filename in Path().glob("*.rst"):
        shutil.copy(filename, DOCS_WORKING_DIRECTORY)

    for filename in Path("sphinx_docs").glob("*"):
        shutil.copy(filename, DOCS_WORKING_DIRECTORY)

    os.environ["PYTHONPATH"] = str(Path.cwd())
    subprocess.check_call(
        [
            "poetry",
            "run",
            "sphinx-build",
            "-c",
            DOCS_WORKING_DIRECTORY,
            "-aEW",
            DOCS_WORKING_DIRECTORY,
            DOCS_OUTPUT_DIRECTORY,
        ],
        cwd=BASE_DIR,
    )


def push():
    """Push docs to github-pages."""
    subprocess.check_call(["poetry", "run", "ghp-import", "-p", "docs/"])


def build_and_push():
    """Build docs then publish."""
    build()
    push()
