"""
Utilities for the AquaCropOS codebase for the WAVES lab at UCSB
"""


class ParamFile:
    """Dynamic class which is instantiated according to the contents of the
    file that is provided as input"""
    def __init__(self, input_file):
        self._read_file(input_file)

    def _read_file(self, input_file):
        """Reads lines of an input file that are not comments"""
        for raw_line in open(input_file):
            line = raw_line.strip()
            if not line.startswith("%"):
                self._readline(raw_line.strip())

    def _readline(self, line):
        """Sets attributes of a dynamic class (guessing the type)"""
        line_items = [x.strip() for x in line.split(":", 1)]

        if line.endswith("True") or line.endswith("False"):
            setattr(self, line_items[0], bool(line_items[1]))
        elif line.endswith(".txt"):
            pass  # some files contain references to other filenames
        elif "/" in line:
            setattr(self, line_items[0], str(line_items[1]))
        else:
            setattr(self, line_items[0], float(line_items[1]))

def keyword_value(line):
    """ strips a line to extract the value"""
    return line.split(":")[1].strip()
