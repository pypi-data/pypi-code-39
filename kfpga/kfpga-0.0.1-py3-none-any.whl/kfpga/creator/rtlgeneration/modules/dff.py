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
from ..module import Module, Port, Verbatim


def get_dff_module():
    module = Module(
        "DFFSRE",
        description="A data Flip-Flop",
        ports=[
            Port("i_data_in", Direction.INPUT, description="The input data"),
            Port(
                "o_data_out",
                Direction.OUTPUT,
                description="The sequential output data",
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
        ],
        body_parts=[
            Verbatim(
                """\

    reg r_data;
    always @(posedge i_clk) begin
        if (!i_nreset) begin
            r_data <= 0;
        end else if (i_set) begin
            r_data <= 1;
        end if (i_enable) begin
            r_data <= i_data_in;
        end
    end
    assign o_data_out = r_data;"""
            )
        ],
    )

    return module
