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
import json


class CoreProject:
    """A kFPGA core project"""

    def __init__(self, name, core_parameters=None, rtl_files=None):
        """Construct a new project
        :param name: Name of the project
        :param core_parameters: Parameters of the core
        """
        self.name = name

        if core_parameters is None:
            core_parameters = CoreParameters()
        self.core_parameters = core_parameters

        if rtl_files is None:
            rtl_files = []
        self.rtl_files = rtl_files

    def save(self, file_path):
        """Save the project
        :param f: Writable file handler
        """
        data = self.to_dict()
        with open(file_path, "w") as f:
            json.dump(data, f, indent="    ")

    @classmethod
    def load(cls, file_path):
        """Load a project from a file
        :param file_path: Path of the file
        :return: The project
        """
        with open(file_path, "r") as f:
            return cls.loads(f)

    @classmethod
    def loads(cls, f):
        """Load a project from a readable file handler
        :param f: The file handler
        :return: The project
        """
        data = json.load(f)

        return cls.from_dict(data)

    def to_dict(self):
        """Create a dict representation of the project
        :return: A dict
        """
        data = {"name": self.name, "rtl_files": self.rtl_files}
        if self.core_parameters is not None:
            data["core_parameters"] = self.core_parameters.to_dict()

        return data

    @classmethod
    def from_dict(cls, data):
        """Create a project from a dict data
        :param data: The data
        :return: The project
        """
        return cls(
            data["name"],
            rtl_files=data["rtl_files"],
            core_parameters=CoreParameters.from_data(data["core_parameters"]),
        )


class CoreParameters:
    """Parameters of an kFPGA core"""

    def __init__(
        self,
        width=1,
        height=1,
        io_pairs_count=1,
        clocks_count=0,
        sets_count=0,
        resets_count=0,
        enables_count=0,
        interconnect_width=0,
        le_count=1,
        lut_size=2,
    ):
        """Construct a new core parameters object
        :param width: Width of the core, in number of tiles. 
            Minimum 1 tile
        :param height: Height of the core, in number of tiles. 
            Minimum 1 tile
        :param io_pairs_count: Number of IO pairs per side of border tiles. 
            Minimun 1 pair
        :param clocks_count: Number of clock signals
        :param sets_count: Nubmer of set signals
        :param resets_count: Number of reset signals
        :param enables_count: Number of enable signals
        :param interconnect_width: Width of the interconnect between two tiles. 
            Minimun 1, except for the core of size 1x1 which doesn't have 
            interconnect
        :param le_count: Number of Logic Elements per Logic Tiles.
            Minimum 1
        :param lut_size: Size of the LUT
            Minimum 1
        """
        if width < 1:
            raise ValueError("The minimal width is 1")
        self.width = width

        if height < 1:
            raise ValueError("The minimal height is 1")
        self.height = height

        if io_pairs_count < 1:
            raise ValueError("The minimal io count is 1")
        self.io_pairs_count = io_pairs_count

        self.clocks_count = clocks_count
        self.sets_count = sets_count
        self.resets_count = resets_count
        self.enables_count = enables_count

        if width * height == 1:
            # No interconnect in a 1x1 core
            interconnect_width = 0
        elif interconnect_width < 1:
            raise ValueError("The minimal interconnect width is 1")
        self.interconnect_width = interconnect_width

        if le_count < 1:
            raise ValueError("The minimal number of LE is 1")
        self.le_count = le_count

        if lut_size < 1:
            raise ValueError("The minimal LUT size is 1")
        self.lut_size = lut_size

    def to_dict(self):
        """Create a dict representation of the parameters
        :return: A dict
        """
        return {
            "width": self.width,
            "height": self.height,
            "io_pairs_count": self.io_pairs_count,
            "clocks_count": self.clocks_count,
            "sets_count": self.sets_count,
            "resets_count": self.resets_count,
            "enables_count": self.enables_count,
            "interconnect_width": self.interconnect_width,
            "le_count": self.le_count,
            "lut_size": self.lut_size,
        }

    @classmethod
    def from_data(cls, data):
        """Create a core parameters from a dict data
        :param data: The data
        :return: The core parameters
        """
        return cls(
            int(data["width"]),
            int(data["height"]),
            int(data["io_pairs_count"]),
            int(data["clocks_count"]),
            int(data["sets_count"]),
            int(data["resets_count"]),
            int(data["enables_count"]),
            int(data["interconnect_width"]),
            int(data["le_count"]),
            int(data["lut_size"]),
        )
