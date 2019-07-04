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
from ..direction import Direction
from ..module import (
    Module,
    Parameter,
    Port,
    NewLine,
    Comment,
    ModuleInstantiation,
    PortConnection,
)


class LUTConfig:
    def __init__(self, lut_size):
        self.lut_size = lut_size

    @property
    def width(self):
        return 2 ** self.lut_size


def get_lut_module():
    module = Module(
        "LookUpTable",
        "A LookUp Table",
        parameters=[Parameter("SIZE", 6, description="Size of the LUT")],
        ports=[
            Port(
                "i_data_in",
                Direction.INPUT,
                width="SIZE - 1",
                description="Input data of the LUT",
            ),
            Port(
                "o_data_out", Direction.OUTPUT, description="The computed data"
            ),
            Port(
                "i_config",
                Direction.INPUT,
                width="2 ** SIZE - 1",
                description="Configuration",
            ),
        ],
        body_parts=[
            NewLine(),
            Comment("Implement the LUT with a multiplexer"),
            ModuleInstantiation(
                "Mux",
                "c_mux",
                parameters=[
                    Parameter("DATA_WIDTH", "2 ** SIZE"),
                    Parameter("SELECTOR_WIDTH", "SIZE"),
                ],
                port_connections=[
                    PortConnection("i_data_in", "i_config"),
                    PortConnection("o_data_out", "o_data_out"),
                    PortConnection("i_selector", "i_data_in"),
                ],
            ),
        ],
    )

    return module
