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
import collections


class Module:
    def __init__(
        self,
        name,
        description="",
        parameters=None,
        ports=None,
        wires=None,
        body_parts=None,
    ):
        self.name = name
        self.description = description
        self.timescale_reference = "1ns"
        self.timescale_precision = "1ps"
        self.parameters = parameters if parameters is not None else []
        self.ports = ports if ports is not None else []
        self.wires = wires if wires is not None else []
        self.body_parts = body_parts if body_parts is not None else []

    def add_port(self, port):
        self.ports.append(port)

    def add_wire(self, wire):
        self.wires.append(wire)

    def add_body_part(self, body_part):
        self.body_parts.append(body_part)

    def write(self, f):
        f.write(
            "`timescale {} / {}\n".format(
                self.timescale_reference, self.timescale_precision
            )
        )
        f.write("\n")

        f.write("/**\n")

        if self.description:
            f.write(" * {}\n".format(self.description))

        for parameter in self.parameters:
            f.write(
                " * @tparam {}: {}\n".format(
                    parameter.name, parameter.description
                )
            )

        for port in self.ports:
            port.write_description(f)
        f.write(" */\n")

        f.write("module {}(".format(self.name))
        if self.ports:
            f.write("\n")
            for i, port in enumerate(self.ports):
                f.write("    ")
                f.write(port.name)
                if i < len(self.ports) - 1:
                    f.write(",")
                f.write("\n")
        f.write(");\n")

        if self.parameters:
            for parameter in self.parameters:
                f.write(
                    "    parameter {} = {};\n".format(
                        parameter.name, parameter.value
                    )
                )
            f.write("\n")

        for port in self.ports:
            port.write_definition(f)

        if self.wires:
            f.write("\n")
            for wire in self.wires:
                wire.write(f)

        for body_part in self.body_parts:
            body_part.write(f)
        f.write("endmodule\n")


class Port:
    def __init__(
        self, name, direction, width=1, description="", range_descriptions=None
    ):
        self.name = name
        self.direction = direction
        self.width = width
        self.description = description
        self.range_descriptions = (
            range_descriptions if range_descriptions is not None else []
        )

    def add_range_description(self, range_description):
        self.range_descriptions.append(range_description)

    def write_description(self, f):
        f.write(" * @param {}: {}\n".format(self.name, self.description))

        for range_description in self.range_descriptions:
            if range_description.begin == range_description.end:
                f.write(
                    " *        {}[{}]: {}\n".format(
                        self.name,
                        range_description.end,
                        range_description.description,
                    )
                )
            else:
                f.write(
                    " *        {}[{}:{}]: {}\n".format(
                        self.name,
                        range_description.end,
                        range_description.begin,
                        range_description.description,
                    )
                )

    def write_definition(self, f):
        f.write("    {}".format(self.direction))
        if isinstance(self.width, str):
            f.write(" [{}:0]".format(self.width))
        elif self.width > 1:
            f.write(" [{}:0]".format(self.width - 1))
        f.write(" {};\n".format(self.name))


class Wire:
    def __init__(self, name, width=1):
        self.name = name
        self.width = width

    def write(self, f):
        f.write("    wire ")
        if isinstance(self.width, str):
            f.write("[{}:0] ".format(self.width))
        elif self.width > 1:
            f.write("[{}:0] ".format(self.width - 1))
        f.write(self.name)
        f.write(";\n")


class Assign:
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source

    def write(self, f):
        f.write("    assign {} = {};\n".format(self.destination, self.source))


class Comment:
    def __init__(self, value):
        self.value = value

    def write(self, f):
        f.write("    // {}\n".format(self.value))


class ModuleInstantiation:
    def __init__(
        self,
        module_name,
        instance_name,
        port_connections=None,
        parameters=None,
    ):
        self.module_name = module_name
        self.instance_name = instance_name
        self.port_connections = (
            port_connections if port_connections is not None else []
        )
        self.parameters = parameters if parameters is not None else []

    def add_port_connection(self, port_connection):
        self.port_connections.append(port_connection)

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def write(self, f):
        f.write("    ")
        f.write(self.module_name)
        if self.parameters:
            f.write(" #(\n")
            for i, parameter in enumerate(self.parameters):
                f.write(
                    "        .{}({})".format(parameter.name, parameter.value)
                )
                if i < len(self.parameters) - 1:
                    f.write(",")
                f.write("\n")
            f.write("    )")
        f.write(" ")
        f.write(self.instance_name)
        f.write(" (")

        if self.port_connections:
            f.write("\n    ")
            for i, port_connection in enumerate(self.port_connections):
                f.write(
                    "    .{}({})".format(
                        port_connection.port, port_connection.net
                    )
                )
                if i < len(self.port_connections) - 1:
                    f.write(",")
                f.write("\n    ")

        f.write(");\n")


class NewLine:
    def write(self, f):
        f.write("\n")


class Verbatim:
    def __init__(self, value):
        self.value = value

    def write(self, f):
        f.write(self.value)


RangeDescription = collections.namedtuple(
    "RangeDescription", ["begin", "end", "description"]
)

PortConnection = collections.namedtuple("PortConnection", ["port", "net"])


class Parameter:
    def __init__(self, name, value, description=""):
        self.name = name
        self.value = value
        self.description = description
