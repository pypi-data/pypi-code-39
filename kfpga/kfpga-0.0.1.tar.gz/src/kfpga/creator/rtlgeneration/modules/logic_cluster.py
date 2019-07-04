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
from ..config import AggregateConfig
from .logic_element import LEConfig
from ..direction import Direction
from ..module import (
    Module,
    Port,
    RangeDescription,
    NewLine,
    Comment,
    ModuleInstantiation,
    PortConnection,
)


class LCConfig(AggregateConfig):
    def __init__(self, le_count, lut_size):
        self.les = [LEConfig(lut_size) for i in range(le_count)]

        super().__init__(self.les)


def get_lc_module(le_count, lut_size):
    config = LCConfig(le_count, lut_size)
    module = Module(
        "LogicCluster",
        "Multiple logic elements",
        ports=[
            Port(
                "i_data_in",
                Direction.INPUT,
                width=le_count * lut_size,
                description="The input data",
            ),
            Port(
                "o_data_out",
                Direction.OUTPUT,
                width=le_count,
                description="The output data",
            ),
            Port("i_clk", Direction.INPUT, description="Clock signal"),
            Port(
                "i_set", Direction.INPUT, description="Synchronous set signal"
            ),
            Port(
                "i_nreset",
                Direction.INPUT,
                description="Synchronous reset signal, active low",
            ),
            Port("i_enable", Direction.INPUT, description="Enable signal"),
            Port(
                "i_config",
                Direction.INPUT,
                width=config.width,
                description="Configuration",
                range_descriptions=[
                    RangeDescription(
                        *config.get_range(config.les[i]),
                        description="Configuration of the LE{}".format(i),
                    )
                    for i in range(le_count)
                ],
            ),
        ],
        body_parts=list(
            itertools.chain(
                *[
                    [
                        NewLine(),
                        Comment("Instantiate the logic element {}".format(i)),
                        ModuleInstantiation(
                            "LogicElement",
                            "c_le_{}".format(i),
                            port_connections=[
                                PortConnection(
                                    "i_data_in",
                                    "i_data_in[{}:{}]".format(
                                        lut_size * (i + 1) - 1, lut_size * i
                                    ),
                                ),
                                PortConnection(
                                    "o_data_out",
                                    "o_data_out[{}]".format(i)
                                    if le_count > 1
                                    else "o_data_out",
                                ),
                                PortConnection("i_clk", "i_clk"),
                                PortConnection("i_set", "i_set"),
                                PortConnection("i_nreset", "i_nreset"),
                                PortConnection("i_enable", "i_enable"),
                                PortConnection(
                                    "i_config",
                                    "i_config[{}:{}]".format(
                                        config.les[i].width * (i + 1) - 1,
                                        config.les[i].width * i,
                                    ),
                                ),
                            ],
                        ),
                    ]
                    for i in range(le_count)
                ]
            )
        ),
    )

    return module
