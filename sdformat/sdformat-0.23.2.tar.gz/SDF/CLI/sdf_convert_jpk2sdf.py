#! python

## @author Ilyas Kuhlemann
# @mail ilyasp.ku@gmail.com
# @date 27.10.16

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
Command line tool to convert JPK to SDF files.

Usage:
    $ sdf-convert-jpk2sdf [options] <input-files>

Arguments:

    <input-files>
      Can be one or multiple files (or a file name pattern like *.jpk-force
      on UNIX systems). Converted files are created with same file name but
      extension `.sdf`. If you don't specify option --no-force, an additional
      file with extension `.force.sdf` will be created.
      In Windows Power Shell, you can use a cmdlet (a small program) to
      expand the * wildcard. E.g. to select all files in folder my_files
      with extension .jpk-force, call the converter like this:
       $ sdf-convert-jpk2sdf  (get-item .\\my_files\\*.jpk-force)

Options:

    -h, --help
      Display help text / docstring and exit.

    -v, --verbose
      Print some status messages on the conversion progress.

    -o, --output-folder
      Writes the converted files to the specified folder, instead of putting
      them into the same folder as the input files.
"""

import click
import os
from SDF.convert.jpk2sdf import jpk2sdf


@click.command()
@click.argument('input-files', nargs=-1,
                type=click.Path(exists=True, dir_okay=False),
                required=True)
@click.option('--output-folder', '-o', default='',
              help='Writes the converted files to the specified folder, instead of ' +
                   'putting them into the same folder as the input files.')
@click.option('--force/--no-force', default=True,
              help='Disable to skip conversion from sdf to forcesdf (a special layout ' +
                   'of SDF files for force distance curves)')
@click.option('--mat', is_flag=True,
              help='In addition to SDF and SDF Force files, create a MATLAB data file.')
@click.option('--verbose', '-v', is_flag=True,
              help='Print some status messages on the conversion progress.')
def main(input_files, output_folder, force, mat, verbose):
    """
    Command line tool to convert JPK to SDF files.

    Input files can be one or multiple files, or a file name pattern like
    *.jpk-force on UNIX systems. Converted files are created with same file name
    but extension `.sdf`. If you don't specify option --no-force, an additional
    file with extension `.force.sdf` will be created.

    In Windows Power Shell, you can use a cmdlet (a small program) to
    expand the * wildcard. E.g. to select all files in folder my_files
    with extension .jpk-force, call the converter like this:
      $ sdf-convert-jpk2sdf  (get-item .\\my_files\\*.jpk-force)
    """
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    for jpk_input_file in input_files:
        if output_folder:
            fname = os.path.splitext(os.path.split(jpk_input_file)[1])[0] + '.sdf'
            sdf_output_file = os.path.join(output_folder, fname)
        else:
            sdf_output_file = ''
        if verbose:
            print('converting {} to {}'.format(jpk_input_file, sdf_output_file))
        try:
            jpk2sdf(jpk_input_file, sdf_output_file,
                    create_force_sdf=force, create_mat=mat, verbose=verbose)
        except KeyError as ke:
            print("unable to convert file {}!".format(jpk_input_file))
            print("aborted due to KeyError: {}".format(ke))
    

if __name__ == "__main__":
    main()
