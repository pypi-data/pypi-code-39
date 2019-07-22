import argparse
import ast
from math import sqrt

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

    def _walk(self):
        dictionary = {}
        for node in ast.walk(self.tree):
            cl = isinstance(node, ast.ClassDef)
            fn = isinstance(node, ast.FunctionDef)
            if cl or fn:
                dictionary[node.lineno] = node
        return dictionary

    def print_list(self, list):
        for element in list:
            print(element)

    def names(self):
        dictionary = self._walk()
        list = []
        for key in sorted(dictionary):
            if isinstance(dictionary[key], ast.ClassDef):
                list.append("CLASS " + dictionary[key].name)
            if isinstance(dictionary[key], ast.FunctionDef):
                list.append(dictionary[key].name)
        return list

    def sizes(self):
        dictionary = self._walk()
        list = []
        last_key = 0
        for key in sorted(dictionary):
            if last_key > 0:
                list.append(str(key - last_key))
            last_key = key
        list.append(str(self.size - last_key))
        return list

    def doc(self):
        dictionary = self._walk()
        list = []
        for key in sorted(dictionary):
            doc_str = ast.get_docstring(dictionary[key])
            list.append("YES" if doc_str else "NO")
        return list

    def locations(self):
        dictionary = self._walk()
        list = []
        for key in sorted(dictionary):
            list.append(key)
        return list

    def stats(self):
        list = []
        sizes = self.sizes()
        minimum = min(map(int, sizes))
        list.append("MINIMUM " + str(minimum))
        avg = sum(map(int, sizes)) / len(sizes)
        list.append("AVERAGE " + str(round(avg, 2)))
        maximum = max(map(int, sizes))
        list.append("MAXIMUM " + str(maximum))
        sum_variance = 0
        for x in sizes:
            sum_variance += (int(x) - avg) * (int(x) - avg)
        variance = sum_variance / (len(sizes) - 1)
        std_dev = sqrt(variance)
        list.append("STD DEV " + str(round(std_dev, 2)))
        return list

def _analyze(args):
    astspy = ASTSPY()
    astspy.read_code(args.file_name)
    list = []
    if args.lines_of_code:
        list = astspy.sizes()
    elif args.locations:
        list = astspy.locations()
    elif args.has_docstring:
        list = astspy.doc()
    elif args.stats:
        list = astspy.stats()
    else:
        list = astspy.names()
    astspy.print_list(list)

parent_parser = argparse.ArgumentParser(add_help=False)

group = parent_parser.add_mutually_exclusive_group()

group.add_argument("-l", "--lines-of-code", action="store_true",
                   help="""show sizes in approximate lines of code""")

group.add_argument("-d", "--has-docstring", action="store_true",
                   help="""'YES' if it has, 'NO' if it doesn't""")

group.add_argument("-L", "--locations", action="store_true",
                   help="""show locations in the file (line numbers)""")

group.add_argument("-s", "--stats", action="store_true",
                   help="""show statistics""")

parser = argparse.ArgumentParser(prog="astspy", parents=[parent_parser])

parser.add_argument("--version", action="version",
                    version="%(prog)s version 0.0.3",
                    help="""print version number on screen and exit""")

parser.add_argument("file_name",
                    help="""python file to analyze""")
parser.set_defaults(func=_analyze)

args = parser.parse_args()
args.func(args)

def main():
    pass
