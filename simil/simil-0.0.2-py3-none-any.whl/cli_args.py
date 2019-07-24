import argparse

parser = argparse.ArgumentParser(description="Semantic string simularity.", prog="sim")

parser.add_argument(
    "--server",
    help="just start the server, without comparing any strings",
    action="store_true",
)

parser.add_argument("-S", "--socket", help="alternate path to the server socket")
parser.add_argument(
    "-t",
    "--timeout",
    default=600,
    help="timeout (in seconds) for the server, if one is started",
    type=int,
)

parser.add_argument(
    "file", nargs="*", help="files to compare (or compare strings with --strings)"
)

parser.add_argument(
    "-s",
    "--strings",
    help="compare arguments as constant strings, not files",
    action="store_true",
)

parser.add_argument("-k", "--kill", help="kill sim server", action="store_true")

args = parser.parse_args()
