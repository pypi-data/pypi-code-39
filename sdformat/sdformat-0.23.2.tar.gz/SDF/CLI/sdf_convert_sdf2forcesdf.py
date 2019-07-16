#! python

"""
Command line tool to convert SDF to FORCE.SDF files.
------------------------------------------------------------------------------
    Copyright (C) 2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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

"""
Command line tool to convert SDF to FORCE.SDF files.

Usage:
    $ sdf-convert-sdf2forcesdf [options] <sdf-input-file> <sdf-output-file>

Options:

    -h, --help
      Display help text / docstring and exit.
"""

import click
from SDF.convert.sdf2forcesdf import sdf2forcesdf

@click.command()
@click.argument('sdf-input-file')
@click.argument('forcesdf-output-file')
@click.option('--hex/--no-hex', default=True)
def main(sdf_input_file, forcesdf_output_file, hex):
    sdf2forcesdf(sdf_input_file, forcesdf_output_file, hex)


if __name__ == "__main__":
    main()
