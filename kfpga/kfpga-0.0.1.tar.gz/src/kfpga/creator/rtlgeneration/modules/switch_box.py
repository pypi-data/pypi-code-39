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
from ..side import Side, sides
from ..config import AggregateConfig
from ..module import (
    Assign,
    Comment,
    Module,
    ModuleInstantiation,
    NewLine,
    Port,
    Parameter,
    PortConnection,
    RangeDescription,
)

from .mux import MuxConfig


def get_sb_connections(interconnect_width):
    """Get the connections for a Wilton SB"""
    connections = {
        side: [{} for i in range(interconnect_width)] for side in sides
    }

    for i in range(interconnect_width):
        # NORTH <-> SOUTH
        side_1 = Side.NORTH
        side_2 = Side.SOUTH
        side_2_i = i
        connections[side_1][i][side_2] = side_2_i
        connections[side_2][side_2_i][side_1] = i

        # EAST <-> WEST
        side_1 = Side.EAST
        side_2 = Side.WEST
        side_2_i = i
        connections[side_1][i][side_2] = side_2_i
        connections[side_2][side_2_i][side_1] = i

        # NORTH <-> EAST
        side_1 = Side.NORTH
        side_2 = Side.EAST
        side_2_i = (interconnect_width - i) % interconnect_width
        connections[side_1][i][side_2] = side_2_i
        connections[side_2][side_2_i][side_1] = i

        # EAST <-> SOUTH
        side_1 = Side.EAST
        side_2 = Side.SOUTH
        side_2_i = (i + 1) % interconnect_width
        connections[side_1][i][side_2] = side_2_i
        connections[side_2][side_2_i][side_1] = i

        # SOUTH <-> WEST
        side_1 = Side.SOUTH
        side_2 = Side.WEST
        side_2_i = (2 * interconnect_width - 2 - i) % interconnect_width
        connections[side_1][i][side_2] = side_2_i
        connections[side_2][side_2_i][side_1] = i

        # WEST <-> NORTH
        side_1 = Side.WEST
        side_2 = Side.NORTH
        side_2_i = (i + 1) % interconnect_width
        connections[side_1][i][side_2] = side_2_i
        connections[side_2][side_2_i][side_1] = i

    return connections


class SBConfig(AggregateConfig):
    def __init__(
        self,
        io_pairs_count,
        io_sides,
        interconnect_width,
        interconnect_sides,
        local_interconnect_input_width,
        local_interconnect_output_width,
    ):
        io_sides_count = sum(1 for side in sides if side & io_sides)
        ic_sides_count = sum(1 for side in sides if side & interconnect_sides)

        # IO output pins are connected to all interconnect inputs and all local
        # interconnect inputs
        io_sides_sources_count = (
            ic_sides_count * interconnect_width
            + local_interconnect_input_width
        )
        self.io = {
            side: (
                [
                    MuxConfig(io_sides_sources_count)
                    for i in range(io_pairs_count)
                ]
                if side in io_sides
                else []
            )
            for side in sides
        }

        # Interconnect output pins are connected to all IO inputs, one input of
        # each other ic side and all local interconnect inputs
        ic_sides_sources_count = (
            # IO inputs
            io_sides_count * io_pairs_count
            # One input of each other IC side inputs
            + (ic_sides_count - 1)
            # LIC inputs
            + local_interconnect_input_width
        )
        self.ic = {
            side: (
                [
                    MuxConfig(ic_sides_sources_count)
                    for i in range(interconnect_width)
                ]
                if side in interconnect_sides
                else []
            )
            for side in sides
        }

        # Interconnect output pins are connected to all IO inputs, all
        # interconnect inputs and all local interconnect inputs
        lic_sources_count = (
            # All IO ipnuts
            io_sides_count * io_pairs_count
            # All IC inputs
            + ic_sides_count * interconnect_width
            # All LIC inputs
            + local_interconnect_input_width
        )
        self.lic = [
            MuxConfig(lic_sources_count)
            for i in range(local_interconnect_output_width)
        ]

        super().__init__(
            [
                *list(itertools.chain(*self.io.values())),
                *list(itertools.chain(*self.ic.values())),
                *self.lic,
            ]
        )


def get_sb_name(
    io_pairs_count,
    io_sides,
    interconnect_width,
    interconnect_sides,
    local_interconnect_input_width,
    local_interconnect_output_width,
):
    name = "SwitchBox"
    if io_sides != Side.NONE:
        name += "_io"
        for side in sides:
            if io_sides & side:
                name += str(side)[0].upper()

    if interconnect_sides != Side.NONE:
        name += "_ic"
        for side in sides:
            if interconnect_sides & side:
                name += str(side)[0].upper()

    if (
        local_interconnect_input_width > 0
        or local_interconnect_output_width > 0
    ):
        name += "_lic"
        if local_interconnect_input_width > 0:
            name += "I{}".format(local_interconnect_input_width)

        if local_interconnect_output_width > 0:
            name += "O{}".format(local_interconnect_output_width)

    return name


def get_sb_module(
    io_pairs_count,
    io_sides,
    interconnect_width,
    interconnect_sides,
    local_interconnect_input_width,
    local_interconnect_output_width,
):
    name = get_sb_name(
        io_pairs_count,
        io_sides,
        interconnect_width,
        interconnect_sides,
        local_interconnect_input_width,
        local_interconnect_output_width,
    )

    module = Module(name, description="A Wilton switch box")

    for side in sides:
        if io_sides & side:
            port = Port(
                "i_data_from_{}_io".format(side),
                Direction.INPUT,
                width=io_pairs_count,
                description="Data incoming from the {} io".format(side),
            )
            module.add_port(port)

    for side in sides:
        if interconnect_sides & side:
            port = Port(
                "i_data_from_{}_interconnect".format(side),
                Direction.INPUT,
                width=interconnect_width,
                description="Data incoming from the {} interconnect".format(
                    side
                ),
            )
            module.add_port(port)

    if local_interconnect_input_width > 0:
        port = Port(
            "i_data_from_local_interconnect",
            Direction.INPUT,
            width=local_interconnect_input_width,
            description="Data incoming from the local interconnect",
        )
        module.add_port(port)

    for side in sides:
        if io_sides & side:
            port = Port(
                "o_data_to_{}_io".format(side),
                Direction.OUTPUT,
                width=io_pairs_count,
                description="Data outgoing to the {} io".format(side),
            )
            module.add_port(port)

    for side in sides:
        if interconnect_sides & side:
            port = Port(
                "o_data_to_{}_interconnect".format(side),
                Direction.OUTPUT,
                width=interconnect_width,
                description="Data outgoing to the {} interconnect".format(
                    side
                ),
            )
            module.add_port(port)

    if local_interconnect_input_width > 0:
        port = Port(
            "o_data_to_local_interconnect",
            Direction.OUTPUT,
            width=local_interconnect_output_width,
            description="Data outgoing to the local interconnect",
        )
        module.add_port(port)

    config = SBConfig(
        io_pairs_count,
        io_sides,
        interconnect_width,
        interconnect_sides,
        local_interconnect_input_width,
        local_interconnect_output_width,
    )

    port = Port(
        "i_config",
        Direction.INPUT,
        width=config.width,
        description="Configuration",
    )
    for side in sides:
        if side in io_sides:
            for i in range(io_pairs_count):
                if config.io[side][i].input_width > 1:
                    port.add_range_description(
                        RangeDescription(
                            *config.get_range(config.io[side][i]),
                            "Output o_data_to_{}_io[{}]".format(side, i),
                        )
                    )
    for side in sides:
        if side in interconnect_sides:
            for i in range(interconnect_width):
                port.add_range_description(
                    RangeDescription(
                        *config.get_range(config.ic[side][i]),
                        "Output o_data_to_{}_interconnect[{}]".format(side, i),
                    )
                )

    for i in range(local_interconnect_output_width):
        port.add_range_description(
            RangeDescription(
                *config.get_range(config.lic[i]),
                "Output o_data_to_local_interconnect[{}]".format(i),
            )
        )

    module.add_port(port)

    for side in sides:
        if side in io_sides:
            for i in range(io_pairs_count):

                module.add_body_part(NewLine())
                module.add_body_part(
                    Comment(
                        "Select source for o_data_to_{}_io[{}]".format(side, i)
                    )
                )

                mux_config = config.io[side][i]
                if mux_config.input_width == 1:
                    if local_interconnect_input_width > 0:
                        module.add_body_part(
                            Assign(
                                "o_data_to_{}_io".format(side),
                                "i_data_from_local_interconnect",
                            )
                        )
                else:
                    mux = ModuleInstantiation(
                        "Mux",
                        "c_mux_{}_io_{}".format(side, i),
                        parameters=[
                            Parameter("DATA_WIDTH", mux_config.input_width),
                            Parameter("SELECTOR_WIDTH", mux_config.width),
                        ],
                    )

                    connection = "{"
                    is_first = True
                    if local_interconnect_input_width > 0:
                        connection += "i_data_from_local_interconnect"
                        is_first = False

                    for side_ in (side.right, side.opposite, side.left):
                        if interconnect_sides & side_:
                            if not is_first:
                                connection += ", "
                                is_first = False
                            connection += "i_data_from_{}_interconnect".format(
                                side_
                            )

                    connection += "}"
                    mux.add_port_connection(
                        PortConnection("i_data_in", connection)
                    )

                    if io_pairs_count == 1:
                        mux.add_port_connection(
                            PortConnection(
                                "o_data_out", "o_data_to_{}_io".format(side)
                            )
                        )
                    else:
                        mux.add_port_connection(
                            PortConnection(
                                "o_data_out",
                                "o_data_to_{}_io[{}]".format(side, i),
                            )
                        )
                    if mux_config.input_width == 1:
                        mux.add_port_connection(
                            PortConnection("i_selector", "{}")
                        )
                    else:
                        mux.add_port_connection(
                            PortConnection(
                                "i_selector",
                                "i_config[{1}:{0}]".format(
                                    *config.get_range(mux_config)
                                ),
                            )
                        )

                    module.add_body_part(mux)

    connections = get_sb_connections(interconnect_width)

    for side in sides:
        if side in interconnect_sides:
            for i in range(interconnect_width):
                module.add_body_part(NewLine())
                module.add_body_part(
                    Comment(
                        "Select source for o_data_to_{}_interconnect[{}]".format(
                            side, i
                        )
                    )
                )

                mux_config = config.ic[side][i]

                mux = ModuleInstantiation(
                    "Mux",
                    "c_mux_{}_ic_{}".format(side, i),
                    parameters=[
                        Parameter("DATA_WIDTH", mux_config.input_width),
                        Parameter("SELECTOR_WIDTH", mux_config.width),
                    ],
                )

                connection = "{"
                is_first = True
                if local_interconnect_input_width > 0:
                    connection += "i_data_from_local_interconnect"
                    is_first = False

                for side_ in (side.right, side.opposite, side.left):
                    if interconnect_sides & side_:
                        if not is_first:
                            connection += ", "
                            is_first = False
                        connection += "i_data_from_{}_interconnect[{}]".format(
                            side_, connections[side][i][side_]
                        )

                for side_ in (side.right, side.opposite, side.left):
                    if io_sides & side_:
                        if not is_first:
                            connection += ", "
                            is_first = False
                        connection += "i_data_from_{}_io".format(side_)

                connection += "}"
                mux.add_port_connection(
                    PortConnection("i_data_in", connection)
                )
                mux.add_port_connection(
                    PortConnection(
                        "o_data_out",
                        "o_data_to_{}_interconnect[{}]".format(side, i),
                    )
                )
                mux.add_port_connection(
                    PortConnection(
                        "i_selector",
                        "i_config[{1}:{0}]".format(
                            *config.get_range(mux_config)
                        ),
                    )
                )

                module.add_body_part(mux)

    for i in range(local_interconnect_output_width):
        module.add_body_part(NewLine())
        module.add_body_part(
            Comment("Select source o_data_to_local_interconnect[{}]".format(i))
        )

        mux_config = config.lic[i]

        mux = ModuleInstantiation(
            "Mux",
            "c_mux_{}_lic_{}".format(side, i),
            parameters=[
                Parameter("DATA_WIDTH", mux_config.input_width),
                Parameter("SELECTOR_WIDTH", mux_config.width),
            ],
        )

        connection = "{"
        is_first = True
        if local_interconnect_input_width > 0:
            connection += "i_data_from_local_interconnect"
            is_first = False

        for side in reversed(sides):
            if interconnect_sides & side:
                if not is_first:
                    connection += ", "
                    is_first = False
                connection += "i_data_from_{}_interconnect".format(side)

        for side in reversed(sides):
            if io_sides & side:
                if not is_first:
                    connection += ", "
                    is_first = False
                connection += "i_data_from_{}_io".format(side)

        connection += "}"
        mux.add_port_connection(PortConnection("i_data_in", connection))
        mux.add_port_connection(
            PortConnection(
                "o_data_out", "o_data_to_local_interconnect[{}]".format(i)
            )
        )
        mux.add_port_connection(
            PortConnection(
                "i_selector",
                "i_config[{1}:{0}]".format(*config.get_range(mux_config)),
            )
        )

        module.add_body_part(mux)

    return module
