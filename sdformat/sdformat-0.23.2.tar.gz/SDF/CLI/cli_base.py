"""
    Some useful functions to help building command line programs.
    Will be obsolete, once we switched to click for all command line programs.
------------------------------------------------------------------------------
    Copyright (C) 2017-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import sys
import os


def execute_convert_command(convert_method, arguments,
                            doc_string, argument_parse_extensions={}):
    arguments_dict = _parse_arguments(arguments, argument_parse_extensions)
    if arguments_dict.pop("help"):
        sys.stdout.write("=" * 80 + "\n")
        sys.stdout.write(doc_string + "\n")
        sys.stdout.write("=" * 80 + "\n")
        sys.exit(0)    
    infile = arguments_dict.pop("infile")
    outfile = arguments_dict.pop("outfile")
    convert_method(infile, outfile, **arguments_dict)


def _parse_arguments(arguments, argument_parse_extensions):
    if arguments.count("-h") or arguments.count("--help"):
        return {"help": True}
    if len(arguments) < 2:
        msg = "\n\nERROR: This command requires at least two arguments:"
        msg += " an input and an output file name.\n"
        msg += "    Or, to display additional information and list all options,"
        msg += " provide '-h' or '--help' as parameter!\n\n\n\n"
        sys.stderr.write(msg)
        sys.exit(1)
    arguments_dict = {"help": False,
                      "infile": os.path.abspath(arguments[-2]),
                      "outfile": os.path.abspath(arguments[-1])}
    if not os.path.exists(arguments_dict["infile"]):
        msg = "Input file \"%s\" does not exist" % arguments_dict["infile"]
        raise IOError(msg)
    if not os.path.isdir(os.path.dirname(arguments_dict["outfile"])):
        msg = "Directory \"%s\" " % os.path.dirname(arguments_dict["outfile"])
        msg += "to save the output file in does not exist"
        raise IOError(msg)
    if arguments.count("-v") or arguments.count("--verbose"):
        arguments_dict["verbose"] = True
    else:
        arguments_dict["verbose"] = False            
    return arguments_dict
