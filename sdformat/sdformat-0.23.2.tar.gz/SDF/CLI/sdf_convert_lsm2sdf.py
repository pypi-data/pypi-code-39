
"""
Command line tool to convert JPK to SDF files.
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

""" 
Command line tool to convert LSM to SDF files.

Usage:
    $ sdf-convert-lsm2sdf [options] <lsm-input-file> <sdf-output-file>

Options:

    -h, --help
      Display help text / docstring and exit.

    -v, --verbose
      Print some status messages on the conversion progess.
"""

import click
from SDF.convert.lsm2sdf import lsm2sdf

@click.command()
@click.argument('lsm-input-file')
@click.argument('sdf-output-file')
@click.option('--verbose', '-v', is_flag=True)
def main(lsm_input_file, sdf_output_file, verbose):        
    lsm2sdf(lsm_input_file, sdf_output_file, verbose, False)


if __name__ == "__main__":
    main()
