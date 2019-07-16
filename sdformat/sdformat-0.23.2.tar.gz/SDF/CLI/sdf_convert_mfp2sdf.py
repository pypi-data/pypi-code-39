#! python

"""
Command line tool to convert MFP to SDF files. MFP devices store
data in files with extendion .ibw (igor binary wave).
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
Command line tool to convert MFP to SDF files. MFP devices store
data in files with extendion .ibw (igor binary wave).

Usage:
    $ sdf-convert-mfp2sdf [options] <ibw-input-file> <sdf-output-file>

Options:

    -h, --help
      Display help text / docstring and exit.

    -v, --verbose
      Print some status messages on the conversion progress.
"""

import click
from SDF.convert.mfp2sdf import mfp2sdf


@click.command()
@click.argument('ibw-input-file')
@click.argument('sdf-output-file')
@click.option('--verbose', '-v', is_flag=True)
def main(ibw_input_file, sdf_output_file, verbose):
    mfp2sdf(ibw_input_file, sdf_output_file, verbose)

    
if __name__ == "__main__":
    main()
