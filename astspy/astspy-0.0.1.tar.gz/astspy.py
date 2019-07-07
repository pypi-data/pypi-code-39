import argparse
import ast


class ASTSPY:
    def __init__(self):
        self.code = ""
        self.size = 0
        self.tree = None

    def read_code(self, path):
        file = open(path)
        self.code = file.read()
        self.size = sum(1 for line in open(path))
        self.tree = ast.parse(self.code)

    def print_analysis(self, loc=False):
        dictionary = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                dictionary[node.lineno] = "CLASS " + node.name
            if isinstance(node, ast.FunctionDef):
                dictionary[node.lineno] = node.name
        last_key = 0
        for key in sorted(dictionary):
            if last_key > 0 and loc:
                print(str(key - last_key) + " loc\n")
            last_key = key
            print(dictionary[key])
        print(str(self.size - last_key) + " loc\n") if loc else None

def _analyze(args):
    astspy = ASTSPY()
    astspy.read_code(args.file_name)
    astspy.print_analysis(loc=args.lines_of_code)

parent_parser = argparse.ArgumentParser(add_help=False)

parent_parser.add_argument("-l", "--lines-of-code", action="store_true",
                           help="""show approximate lines of code""")

parser = argparse.ArgumentParser(prog="astspy", parents=[parent_parser])

# Version
parser.add_argument("--version", action="version",
                    version="%(prog)s version 0.0.1",
                    help="""print version number on screen and exit""")

parser.add_argument("file_name",
                    help="""python file to analyze""")
parser.set_defaults(func=_analyze)

args = parser.parse_args()
args.func(args)

def main():
    None
