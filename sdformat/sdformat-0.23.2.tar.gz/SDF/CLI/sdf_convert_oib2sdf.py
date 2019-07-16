#! python

"""
Command line tool to convert OIB to SDF files.
It converts OIB file to temporary oif file and tiff images,
then applies oif2sdf.
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
Command line tool to convert OIB to SDF files.
It converts OIB file to temporary oif file and tiff images, 
then applies oif2sdf.

Usage:
    $ sdf-convert-oib2sdf [options] <oib-input-file> <sdf-output-file>

Options:

    -h, --help
      Display help text / docstring.

    -v, --verbose
      Print some status messages on the conversion progess.
"""

import os
import shutil
import click
from SDF.convert.oif2sdf import oif2sdf, oiffile

@click.command()
@click.argument('oib-input-file')
@click.argument('sdf-output-file')
@click.option('--verbose', '-v', is_flag=True)
def main(oib_input_file, sdf_output_file, verbose):    

    folder, fname = os.path.split(oib_input_file)

    if folder:
        tmp_folder = folder + "/.tmp_oif"
    else:
        tmp_folder = ".tmp_oif"

    tmp_ifname = tmp_folder + "/" + fname.rsplit('.', 1)[0] + ".oif"
    if verbose:
        print("creating temporary oif file and tiff images in '%s'" % tmp_folder)

    os.mkdir(tmp_folder)
    oiffile.oib2oif(oib_input_file, tmp_folder + "/")
    if verbose:
        print("converting %s to sdf file" % tmp_ifname)

    oif, list_of_elementary_parameters, ws = oif2sdf(tmp_ifname, sdf_output_file,
                                                     verbose, debug=False)

    shutil.rmtree(tmp_folder)
    if verbose:
        print("removed temporary folder '%s'" % tmp_folder)

 
if __name__ == "__main__":
    main()
