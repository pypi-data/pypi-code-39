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
from ..config import AggregateConfig
from ..direction import Direction
from ..side import Side, sides
from ..module import (
    Assign,
    Module,
    Port,
    RangeDescription,
    NewLine,
    Comment,
    Wire,
    ModuleInstantiation,
    Parameter,
    PortConnection,
)
from .mux import MuxConfig
from .logic_cluster import LCConfig
from .switch_box import get_sb_name, SBConfig
import functools
import operator


class LTConfig(AggregateConfig):
    def __init__(
        self,
        io_pairs_count,
        io_sides,
        interconnect_width,
        clocks_count,
        sets_count,
        resets_count,
        enables_count,
        le_count,
        lut_size,
    ):
        interconnect_sides = Side.NONE
        for side in sides:
            if not io_sides & side:
                interconnect_sides |= side

        self.sb = SBConfig(
            io_pairs_count,
            io_sides,
            interconnect_width,
            interconnect_sides,
            le_count,
            lut_size * le_count,
        )
        self.lc = LCConfig(le_count, lut_size)
        self.clks_selector = MuxConfig(clocks_count)
        self.sets_selector = MuxConfig(sets_count)
        self.resets_selector = MuxConfig(resets_count)
        self.enables_selector = MuxConfig(enables_count)

        super().__init__(
            [
                self.sb,
                self.lc,
                self.clks_selector,
                self.sets_selector,
                self.resets_selector,
                self.enables_selector,
            ]
        )


def get_lt_name(io_sides):
    name = "LogicTile"
    if io_sides ^ Side.NONE:
        if io_sides & Side.NORTH:
            name += "North"

        if io_sides & Side.EAST:
            name += "East"

        if io_sides & Side.SOUTH:
            name += "South"

        if io_sides & Side.WEST:
            name += "West"
    else:
        name += "Center"

    return name


def get_lt_module(
    io_pairs_count,
    io_sides,
    interconnect_width,
    clocks_count,
    sets_count,
    resets_count,
    enables_count,
    le_count,
    lut_size,
):
    name = get_lt_name(io_sides)
    module = Module(name, description="A logic tile")

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
        if not io_sides & side:
            port = Port(
                "i_data_from_{}_interconnect".format(side),
                Direction.INPUT,
                width=interconnect_width,
                description="Data incoming from the {} interconnect".format(
                    side
                ),
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
        if not io_sides & side:
            port = Port(
                "o_data_to_{}_interconnect".format(side),
                Direction.OUTPUT,
                width=interconnect_width,
                description="Data outgoing to the {} interconnect".format(
                    side
                ),
            )
            module.add_port(port)

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

    config = LTConfig(
        io_pairs_count,
        io_sides,
        interconnect_width,
        clocks_count,
        sets_count,
        resets_count,
        enables_count,
        le_count,
        lut_size,
    )

    interconnect_sides = functools.reduce(
        operator.or_,
        (side for side in sides if not side & io_sides),
        Side.NONE,
    )

    port = Port(
        "i_config_in",
        Direction.INPUT,
        description="Input for the config storage shift register",
    )
    port.add_range_description(
        RangeDescription(
            *config.get_range(config.sb), "Configuration of the switch box"
        )
    )
    port.add_range_description(
        RangeDescription(
            *config.get_range(config.lc), "Configuration of the logic cluster"
        )
    )

    port.add_range_description(
        RangeDescription(
            *config.get_range(config.clks_selector),
            "Configuration of the clocks selector",
        )
    )

    port.add_range_description(
        RangeDescription(
            *config.get_range(config.sets_selector),
            "Configuration of the sets selector",
        )
    )

    port.add_range_description(
        RangeDescription(
            *config.get_range(config.resets_selector),
            "Configuration of the resets selector",
        )
    )

    port.add_range_description(
        RangeDescription(
            *config.get_range(config.enables_selector),
            "Configuration of the enables selector",
        )
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

    module.add_body_part(NewLine())
    module.add_body_part(Comment("Configuration storage"))
    module.add_body_part(Wire("w_config", width=config.width))
    module.add_body_part(
        ModuleInstantiation(
            "ShiftRegister",
            "c_configuration_storage",
            parameters=[Parameter("LENGTH", config.width)],
            port_connections=[
                PortConnection("i_data_in", "i_config_in"),
                PortConnection("o_data_out", "o_config_out"),
                PortConnection("o_data", "w_config"),
                PortConnection("i_clk", "i_config_clk"),
                PortConnection("i_set", "{1'b0}"),
                PortConnection("i_nreset", "{1'b1}"),
                PortConnection("i_enable", "i_config_enable"),
            ],
        )
    )

    module.add_body_part(NewLine())
    module.add_body_part(Comment("Clock selector"))
    module.add_body_part(Wire("w_clk"))
    if clocks_count == 1:
        module.add_body_part(Assign("w_clk", "i_clks"))
    else:
        module.add_body_part(
            ModuleInstantiation(
                "Mux",
                "c_clock_selector",
                parameters=[
                    Parameter("DATA_WIDTH", config.clks_selector.input_width),
                    Parameter("SELECTOR_WIDTH", config.clks_selector.width),
                ],
                port_connections=[
                    PortConnection("i_data_in", "i_clks"),
                    PortConnection("o_data_out", "w_clk"),
                    PortConnection(
                        "i_selector",
                        "w_config[{1}:{0}]".format(
                            *config.get_range(config.clks_selector)
                        ),
                    ),
                ],
            )
        )

    module.add_body_part(NewLine())
    module.add_body_part(Comment("Set selector"))
    module.add_body_part(Wire("w_set"))
    if sets_count == 1:
        module.add_body_part(Assign("w_set", "i_sets"))
    else:
        module.add_body_part(
            ModuleInstantiation(
                "Mux",
                "c_set_selector",
                parameters=[
                    Parameter("DATA_WIDTH", config.sets_selector.input_width),
                    Parameter("SELECTOR_WIDTH", config.sets_selector.width),
                ],
                port_connections=[
                    PortConnection("i_data_in", "i_sets"),
                    PortConnection("o_data_out", "w_set"),
                    PortConnection(
                        "i_selector",
                        "w_config[{1}:{0}]".format(
                            *config.get_range(config.sets_selector)
                        ),
                    ),
                ],
            )
        )

    module.add_body_part(NewLine())
    module.add_body_part(Comment("Reset selector"))
    module.add_body_part(Wire("w_nreset"))
    if resets_count == 1:
        module.add_body_part(Assign("w_nreset", "i_nresets"))
    else:
        module.add_body_part(
            ModuleInstantiation(
                "Mux",
                "c_nreset_selector",
                parameters=[
                    Parameter(
                        "DATA_WIDTH", config.resets_selector.input_width
                    ),
                    Parameter("SELECTOR_WIDTH", config.resets_selector.width),
                ],
                port_connections=[
                    PortConnection("i_data_in", "i_nresets"),
                    PortConnection("o_data_out", "w_nreset"),
                    PortConnection(
                        "i_selector",
                        "w_config[{1}:{0}]".format(
                            *config.get_range(config.resets_selector)
                        ),
                    ),
                ],
            )
        )

    module.add_body_part(NewLine())
    module.add_body_part(Comment("Enable selector"))
    module.add_body_part(Wire("w_enable"))
    if enables_count == 1:
        module.add_body_part(Assign("w_enable", "i_enables"))
    else:
        module.add_body_part(
            ModuleInstantiation(
                "Mux",
                "c_enable_selector",
                parameters=[
                    Parameter(
                        "DATA_WIDTH", config.enables_selector.input_width
                    ),
                    Parameter("SELECTOR_WIDTH", config.enables_selector.width),
                ],
                port_connections=[
                    PortConnection("i_data_in", "i_enables"),
                    PortConnection("o_data_out", "w_enable"),
                    PortConnection(
                        "i_selector",
                        "w_config[{1}:{0}]".format(
                            *config.get_range(config.enables_selector)
                        ),
                    ),
                ],
            )
        )

    module.add_body_part(NewLine())
    module.add_body_part(Comment("The switch box"))
    module.add_body_part(
        Wire("w_data_to_logic_cluster", width=le_count * lut_size)
    )
    module.add_body_part(Wire("w_data_from_logic_cluster", width=le_count))
    module_inst = ModuleInstantiation(
        get_sb_name(
            io_pairs_count,
            io_sides,
            interconnect_width,
            interconnect_sides,
            le_count,
            le_count * lut_size,
        ),
        "c_switch_box",
    )
    for side in sides:
        if side & io_sides:
            port_name = "i_data_from_{}_io".format(side)
            module_inst.add_port_connection(
                PortConnection(port_name, port_name)
            )
    for side in sides:
        if side & interconnect_sides:
            port_name = "i_data_from_{}_interconnect".format(side)
            module_inst.add_port_connection(
                PortConnection(port_name, port_name)
            )
    module_inst.add_port_connection(
        PortConnection(
            "i_data_from_local_interconnect", "w_data_from_logic_cluster"
        )
    )

    for side in sides:
        if side & io_sides:
            port_name = "o_data_to_{}_io".format(side)
            module_inst.add_port_connection(
                PortConnection(port_name, port_name)
            )
    for side in sides:
        if side & interconnect_sides:
            port_name = "o_data_to_{}_interconnect".format(side)
            module_inst.add_port_connection(
                PortConnection(port_name, port_name)
            )
    module_inst.add_port_connection(
        PortConnection(
            "o_data_to_local_interconnect", "w_data_to_logic_cluster"
        )
    )
    module_inst.add_port_connection(
        PortConnection(
            "i_config",
            "w_config[{1}:{0}]".format(*config.get_range(config.sb)),
        )
    )

    module.add_body_part(module_inst)

    module.add_body_part(NewLine())
    module.add_body_part(Comment("The logic cluster"))
    module.add_body_part(
        ModuleInstantiation(
            "LogicCluster",
            "c_logic_cluster",
            port_connections=[
                PortConnection("i_data_in", "w_data_to_logic_cluster"),
                PortConnection("o_data_out", "w_data_from_logic_cluster"),
                PortConnection("i_clk", "w_clk"),
                PortConnection("i_set", "w_set"),
                PortConnection("i_nreset", "w_nreset"),
                PortConnection("i_enable", "w_enable"),
                PortConnection(
                    "i_config",
                    "w_config[{1}:{0}]".format(*config.get_range(config.lc)),
                ),
            ],
        )
    )

    return module
