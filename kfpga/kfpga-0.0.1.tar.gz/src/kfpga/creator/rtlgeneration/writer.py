# Copyright Jonathan Tremesaygues (2019)
#
# Jonathan Tremesaygues <jonathan.tremesaygues@slaanesh.org>
#
# This software is a computer program whose purpose is to [describe
# functionalities and technical features of your software].
#
# This software is governed by the CeCILL-B license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL-B
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
import os.path
from .side import Side
from .modules.shift_register import get_sr_module
from .modules.mux import get_mux_module
from .modules.lut import get_lut_module
from .modules.dff import get_dff_module
from .modules.logic_element import get_le_module
from .modules.logic_cluster import get_lc_module
from .modules.switch_box import get_sb_module
from .modules.logic_tile import get_lt_module
from .modules.core import get_core_module


def write_core_rtl_into_dir(output_dir, core_parameters):
    """Write the RTL of a core
    :param output_dir: Dir in which the RTL is writen
    :param core_parameters: The parameters of the core
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    modules = [
        get_sr_module(),
        get_mux_module(),
        get_lut_module(),
        get_dff_module(),
        get_le_module(core_parameters.lut_size),
        get_lc_module(core_parameters.le_count, core_parameters.lut_size),
        get_core_module(
            core_parameters.width,
            core_parameters.height,
            core_parameters.io_pairs_count,
            core_parameters.interconnect_width,
            core_parameters.clocks_count,
            core_parameters.sets_count,
            core_parameters.resets_count,
            core_parameters.enables_count,
            core_parameters.le_count,
            core_parameters.lut_size,
        ),
    ]

    io_sides = {
        0: {0: tuple(), 1: tuple(), 2: tuple(), 3: tuple()},
        1: {
            0: tuple(),
            1: ((Side.ALL, Side.NONE),),
            2: (
                (Side.EAST_SOUTH_WEST, Side.NORTH),
                (Side.NORTH_EAST_WEST, Side.SOUTH),
            ),
            3: (
                (Side.EAST_SOUTH_WEST, Side.NORTH),
                (Side.EAST_WEST, Side.NORTH_SOUTH),
                (Side.NORTH_EAST_WEST, Side.SOUTH),
            ),
        },
        2: {
            0: tuple(),
            1: (
                (Side.NORTH_SOUTH_WEST, Side.EAST),
                (Side.NORTH_EAST_SOUTH, Side.WEST),
            ),
            2: (
                (Side.SOUTH_WEST, Side.NORTH_EAST),
                (Side.EAST_SOUTH, Side.NORTH_WEST),
                (Side.NORTH_WEST, Side.EAST_SOUTH),
                (Side.NORTH_EAST, Side.SOUTH_WEST),
            ),
            3: {
                (Side.SOUTH_WEST, Side.NORTH_EAST),
                (Side.EAST_SOUTH, Side.NORTH_WEST),
                (Side.WEST, Side.NORTH_EAST_SOUTH),
                (Side.EAST, Side.NORTH_SOUTH_WEST),
                (Side.NORTH_WEST, Side.EAST_SOUTH),
                (Side.NORTH_EAST, Side.SOUTH_WEST),
            },
        },
        3: {
            0: tuple(),
            1: (
                (Side.NORTH_SOUTH_WEST, Side.EAST),
                (Side.NORTH_SOUTH, Side.EAST_WEST),
                (Side.NORTH_EAST_SOUTH, Side.WEST),
            ),
            2: (
                (Side.SOUTH_WEST, Side.NORTH_EAST),
                (Side.SOUTH, Side.NORTH_EAST_WEST),
                (Side.EAST_SOUTH, Side.NORTH_WEST),
                (Side.NORTH_WEST, Side.EAST_SOUTH),
                (Side.NORTH, Side.EAST_SOUTH_WEST),
                (Side.NORTH_EAST, Side.SOUTH_WEST),
            ),
            3: {
                (Side.SOUTH_WEST, Side.NORTH_EAST),
                (Side.SOUTH, Side.NORTH_EAST_WEST),
                (Side.EAST_SOUTH, Side.NORTH_WEST),
                (Side.WEST, Side.NORTH_EAST_SOUTH),
                (Side.NONE, Side.ALL),
                (Side.EAST, Side.NORTH_SOUTH_WEST),
                (Side.NORTH_WEST, Side.EAST_SOUTH),
                (Side.NORTH, Side.EAST_SOUTH_WEST),
                (Side.NORTH_EAST, Side.SOUTH_WEST),
            },
        },
    }

    for io_sides, ic_sides in io_sides[
        0
        if core_parameters.width < 0
        else 3
        if core_parameters.width > 3
        else core_parameters.width
    ][
        0
        if core_parameters.height < 0
        else 3
        if core_parameters.height > 3
        else core_parameters.height
    ]:
        modules.append(
            get_sb_module(
                core_parameters.io_pairs_count,
                io_sides,
                core_parameters.interconnect_width,
                ic_sides,
                core_parameters.le_count,
                core_parameters.le_count * core_parameters.lut_size,
            )
        )
        modules.append(
            get_lt_module(
                core_parameters.io_pairs_count,
                io_sides,
                core_parameters.interconnect_width,
                core_parameters.clocks_count,
                core_parameters.sets_count,
                core_parameters.resets_count,
                core_parameters.enables_count,
                core_parameters.le_count,
                core_parameters.lut_size,
            )
        )

    output_files = []
    for module in modules:
        output_file = os.path.join(output_dir, module.name + ".v")
        output_files.append(output_file)
        with open(output_file, "w") as f:
            module.write(f)

    return output_files
