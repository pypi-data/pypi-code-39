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
import itertools
from ..direction import Direction
from ..module import (
    Comment,
    Module,
    ModuleInstantiation,
    NewLine,
    Port,
    PortConnection,
    Wire,
)
from .logic_tile import get_lt_name
from ..side import Side, sides


def get_core_module(
    width,
    height,
    io_pairs_count,
    interconnect_width,
    clocks_count,
    sets_count,
    resets_count,
    enables_count,
    le_count,
    lut_size,
):
    module = Module("kFPGACore", description="A kFPGA core")

    for side in sides:
        module.add_port(
            Port(
                "i_{}_data".format(side),
                Direction.INPUT,
                width=io_pairs_count
                * (
                    width if side & Side.NORTH or side & Side.SOUTH else height
                ),
                description="Input data for the {} side".format(side),
            )
        )

    for side in sides:
        module.add_port(
            Port(
                "o_{}_data".format(side),
                Direction.OUTPUT,
                width=io_pairs_count
                * (
                    width if side & Side.NORTH or side & Side.SOUTH else height
                ),
                description="Output data for the {} side".format(side),
            )
        )

    port = Port(
        "i_clks",
        Direction.INPUT,
        width=clocks_count,
        description="Clock signal(s)",
    )
    module.add_port(port)

    port = Port(
        "i_sets",
        Direction.INPUT,
        width=sets_count,
        description="Set signal(s)",
    )
    module.add_port(port)

    port = Port(
        "i_nresets",
        Direction.INPUT,
        width=resets_count,
        description="Reset signal(s), active low",
    )
    module.add_port(port)

    port = Port(
        "i_enables",
        Direction.INPUT,
        width=enables_count,
        description="Enable signal(s)",
    )
    module.add_port(port)

    port = Port(
        "i_config_in",
        Direction.INPUT,
        description="Input for the config storage shift register",
    )
    module.add_port(port)

    port = Port(
        "o_config_out",
        Direction.OUTPUT,
        description="Output of the config storage shift register",
    )
    module.add_port(port)

    port = Port(
        "i_config_clk",
        Direction.INPUT,
        description="Clock signal for the configuration",
    )
    module.add_port(port)

    port = Port(
        "i_config_enable",
        Direction.INPUT,
        description="Enable signal for the configuration",
    )
    module.add_port(port)

    for y, x in itertools.product(range(height), range(width)):
        io_sides = Side.NONE
        if x == 0:
            io_sides |= Side.WEST
        if x == width - 1:
            io_sides |= Side.EAST
        if y == 0:
            io_sides |= Side.SOUTH
        if y == height - 1:
            io_sides |= Side.NORTH

        for side in sides:
            if not io_sides & side:
                module.add_wire(
                    Wire(
                        "w_data_from_{}_of_tile_x{}_y{}".format(side, x, y),
                        width=interconnect_width,
                    )
                )

        if not io_sides & Side.EAST:
            module.add_wire(Wire("w_config_from_tile_x{}_y{}".format(x, y)))

    for y, x in itertools.product(range(height), range(width)):
        module.add_body_part(NewLine())
        module.add_body_part(Comment("Logic tile ({}, {})".format(x, y)))

        io_sides = Side.NONE
        if x == 0:
            io_sides |= Side.WEST
        if x == width - 1:
            io_sides |= Side.EAST
        if y == 0:
            io_sides |= Side.SOUTH
        if y == height - 1:
            io_sides |= Side.NORTH

        module_inst = ModuleInstantiation(
            get_lt_name(io_sides), "c_tile_x{}_y{}".format(x, y)
        )

        for side in sides:
            if io_sides & side:
                if side == Side.NORTH or side == Side.SOUTH:
                    i = x
                else:
                    i = y
                module_inst.add_port_connection(
                    PortConnection(
                        "i_data_from_{}_io".format(side),
                        (
                            "i_{}_data[{}:{}]".format(
                                side,
                                io_pairs_count * (i + 1) - 1,
                                io_pairs_count * i,
                            )
                            if io_pairs_count > 1
                            else "i_{}_data".format(side)
                        ),
                    )
                )

        for side in sides:
            if not io_sides & side:
                if side & Side.NORTH:
                    y_ = y + 1
                elif side & Side.SOUTH:
                    y_ = y - 1
                else:
                    y_ = y

                if side & Side.EAST:
                    x_ = x + 1
                elif side & Side.WEST:
                    x_ = x - 1
                else:
                    x_ = x

                module_inst.add_port_connection(
                    PortConnection(
                        "i_data_from_{}_interconnect".format(side),
                        "w_data_from_{}_of_tile_x{}_y{}".format(
                            side.opposite, x_, y_
                        ),
                    )
                )

        for side in sides:
            if io_sides & side:
                if side == Side.NORTH or side == Side.SOUTH:
                    i = x
                else:
                    i = y
                module_inst.add_port_connection(
                    PortConnection(
                        "o_data_to_{}_io".format(side),
                        (
                            "o_{}_data[{}:{}]".format(
                                side,
                                io_pairs_count * (i + 1) - 1,
                                io_pairs_count * i,
                            )
                            if io_pairs_count > 1
                            else "o_{}_data".format(side)
                        ),
                    )
                )

        for side in sides:
            if not io_sides & side:
                module_inst.add_port_connection(
                    PortConnection(
                        "o_data_to_{}_interconnect".format(side),
                        "w_data_from_{}_of_tile_x{}_y{}".format(side, x, y),
                    )
                )

        module_inst.add_port_connection(PortConnection("i_clks", "i_clks"))
        module_inst.add_port_connection(PortConnection("i_sets", "i_sets"))
        module_inst.add_port_connection(
            PortConnection("i_nresets", "i_nresets")
        )
        module_inst.add_port_connection(
            PortConnection("i_enables", "i_enables")
        )

        if io_sides & Side.SOUTH and io_sides & Side.WEST:
            module_inst.add_port_connection(
                PortConnection("i_config_in", "i_config_in")
            )
        else:
            if y > 0:
                x_ = x
                y_ = y - 1
            else:
                x_ = x - 1
                y_ = height - 1
            module_inst.add_port_connection(
                PortConnection(
                    "i_config_in", "w_config_from_tile_x{}_y{}".format(x_, y_)
                )
            )

        if io_sides & Side.NORTH and io_sides & Side.EAST:
            module_inst.add_port_connection(
                PortConnection("o_config_out", "o_config_out")
            )
        else:
            module_inst.add_port_connection(
                PortConnection(
                    "o_config_out", "w_config_from_tile_x{}_y{}".format(x, y)
                )
            )

        module_inst.add_port_connection(
            PortConnection("i_config_clk", "i_config_clk")
        )
        module_inst.add_port_connection(
            PortConnection("i_config_enable", "i_config_enable")
        )

        module.add_body_part(module_inst)

    return module
