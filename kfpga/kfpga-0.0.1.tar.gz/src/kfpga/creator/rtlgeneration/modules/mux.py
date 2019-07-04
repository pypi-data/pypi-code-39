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
import math
from ..direction import Direction
from ..module import Module, Port, Parameter, NewLine, Assign


class MuxConfig:
    def __init__(self, input_width, selected_input=0):
        self.input_width = input_width
        self.selected_input = selected_input

    @property
    def width(self):
        return math.ceil(math.log2(self.input_width))


def get_mux_module():
    module = Module(
        "Mux",
        description="A multiplexer",
        parameters=[
            Parameter("DATA_WIDTH", 2, description="Width of the input data"),
            Parameter(
                "SELECTOR_WIDTH", 1, description="Width of the selector"
            ),
        ],
        ports=[
            Port(
                "i_data_in",
                Direction.INPUT,
                width="DATA_WIDTH - 1",
                description="Input data",
            ),
            Port(
                "o_data_out", Direction.OUTPUT, description="The selected data"
            ),
            Port(
                "i_selector",
                Direction.INPUT,
                width="SELECTOR_WIDTH - 1",
                description="The selector",
            ),
        ],
        body_parts=[NewLine(), Assign("o_data_out", "i_data_in[i_selector]")],
    )

    return module
