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

    def print_class_fn(self):
        dictionary = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                dictionary[node.lineno] = "CLASS " + node.name
            if isinstance(node, ast.FunctionDef):
                dictionary[node.lineno] = node.name
        for key in sorted(dictionary):
            print(dictionary[key])

    def print_loc(self):
        dictionary = {}
        for node in ast.walk(self.tree):
            cl = isinstance(node, ast.ClassDef)
            fn = isinstance(node, ast.FunctionDef)
            if cl or fn:
                dictionary[node.lineno] = node.name
        last_key = 0
        for key in sorted(dictionary):
            if last_key > 0:
                print(str(key - last_key))
            last_key = key
        print(str(self.size - last_key))

    def print_doc(self):
        dictionary = {}
        for node in ast.walk(self.tree):
            cl = isinstance(node, ast.ClassDef)
            fn = isinstance(node, ast.FunctionDef)
            if cl or fn:
                dictionary[node.lineno] = node
        last_key = 0
        for key in sorted(dictionary):
            doc_str = ast.get_docstring(dictionary[key])
            print("YES" if doc_str else "NO")


def _analyze(args):
    astspy = ASTSPY()
    astspy.read_code(args.file_name)
    if args.lines_of_code:
        astspy.print_loc()
    elif args.has_docstring:
        astspy.print_doc()
    else:
        astspy.print_class_fn()

parent_parser = argparse.ArgumentParser(add_help=False)

group_l_d = parent_parser.add_mutually_exclusive_group()

group_l_d.add_argument("-l", "--lines-of-code", action="store_true",
                           help="""show approximate lines of code""")

group_l_d.add_argument("-d", "--has-docstring", action="store_true",
                           help="""'YES' if it has, 'NO' if it doesn't""")

parser = argparse.ArgumentParser(prog="astspy", parents=[parent_parser])

parser.add_argument("--version", action="version",
                    version="%(prog)s version 0.0.2",
                    help="""print version number on screen and exit""")

parser.add_argument("file_name",
                    help="""python file to analyze""")
parser.set_defaults(func=_analyze)

args = parser.parse_args()
args.func(args)

def main():
    pass
