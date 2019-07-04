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
import enum


class Side(enum.Flag):
    """Represent a side"""

    NONE = enum.auto()
    NORTH = enum.auto()
    EAST = enum.auto()
    SOUTH = enum.auto()
    WEST = enum.auto()
    CENTER = enum.auto()
    NORTH_EAST = NORTH | EAST
    NORTH_SOUTH = NORTH | SOUTH
    NORTH_WEST = NORTH | WEST
    EAST_SOUTH = EAST | SOUTH
    EAST_WEST = EAST | WEST
    SOUTH_WEST = SOUTH | WEST
    NORTH_EAST_SOUTH = NORTH | EAST | SOUTH
    NORTH_EAST_WEST = NORTH | EAST | WEST
    NORTH_SOUTH_WEST = NORTH | SOUTH | WEST
    EAST_SOUTH_WEST = EAST | SOUTH | WEST
    ALL = NORTH | EAST | SOUTH | WEST

    def __str__(self):
        return {
            Side.NORTH: "north",
            Side.EAST: "east",
            Side.SOUTH: "south",
            Side.WEST: "west",
        }[self]

    @property
    def left(self):
        return {
            Side.NORTH: Side.EAST,
            Side.EAST: Side.SOUTH,
            Side.SOUTH: Side.WEST,
            Side.WEST: Side.NORTH,
        }[self]

    @property
    def opposite(self):
        return {
            Side.NORTH: Side.SOUTH,
            Side.EAST: Side.WEST,
            Side.SOUTH: Side.NORTH,
            Side.WEST: Side.EAST,
        }[self]

    @property
    def right(self):
        return {
            Side.NORTH: Side.WEST,
            Side.EAST: Side.NORTH,
            Side.SOUTH: Side.EAST,
            Side.WEST: Side.SOUTH,
        }[self]


# Iterable of all sides
sides = (Side.NORTH, Side.EAST, Side.SOUTH, Side.WEST)
