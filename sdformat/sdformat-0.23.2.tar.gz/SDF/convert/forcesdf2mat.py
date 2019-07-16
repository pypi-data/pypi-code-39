"""
Convert a .force.sdf file into a .mat file, translating its contents into
a matlab struct.
------------------------------------------------------------------------------
    Copyright (C) 2016-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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
from ..sdf_wrapper.sdf_force import sdf_force
from scipy.io import savemat


def forcesdf2mat(forcesdf_fname, mat_filename=None):
    """
    Convert a .force.sdf file into a .mat file, translating its contents into
    a matlab struct.
    """
    
    # Check types and stuff
    if not isinstance(forcesdf_fname, str):
        msg = "forcesdf_fname must be string."
        raise TypeError(msg)
        
    if mat_filename is None:
        mat_filename = forcesdf_fname.replace(".force.sdf", ".mat")
    else:
        if not isinstance(mat_filename, str):
            msg = "mat_filename must be string."
            raise TypeError(msg)
    
    # Open the .force.sdf file
    curve = sdf_force(forcesdf_fname)
    
    # Translate to mat
    mat = {}
    
    # Global pars
    mat["spring_constant"] = curve.spring_constant
    mat["sensitivity"]     = curve.sensitivity
    
    # For all segments:
    for nseg in range(curve.GetSegmentNumber()):

        seg_name = "segment_%d" % nseg
        
        mat[seg_name] = {}

        if curve.segment[nseg].position_index is not None:
            mat[seg_name]["position_index"] = curve.segment[nseg].position_index

        if curve.segment[nseg].x is not None:
            mat[seg_name]["x"] = curve.segment[nseg].x

        if curve.segment[nseg].y is not None:
            mat[seg_name]["y"] = curve.segment[nseg].y

        # Data lines
        for d_name in curve.segment[nseg]._getter_dict:

            mat[seg_name][d_name] = curve.segment[nseg]._getter_dict[d_name]()[0]

        # Other pars:
        for p_name in curve.segment[nseg]._par_dict:

            if curve.segment[nseg]._par_dict[p_name] is not None:
                mat[seg_name][p_name] = curve.segment[nseg]._par_dict[p_name]


    # Save as .dat
    savemat(mat_filename, mat)
        
