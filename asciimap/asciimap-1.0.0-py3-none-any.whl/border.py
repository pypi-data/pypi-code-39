# asciimap - print countries in ascii art
# Copyright (C) 2019  MaelStor <maelstor@posteo.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# pylint: disable=invalid-name,bad-continuation,missing-docstring,chained-comparison


class Boundary:
    VERTICAL = 0
    HORIZONTAL = 1
    CORNER = 2

    def __init__(self, model):
        """Use instance() to initialize Boundary"""
        self.model = model

    @staticmethod
    def factory(matrix, max_height, line_num, row, col, fill_char, outside_char):
        """Instantiates a Boundary if it is a valid boundary else return None"""
        width = matrix.shape[1]
        if matrix[row][col] == fill_char:
            if line_num in (0, max_height - 1):
                if col in (0, width - 1) and matrix[row, col] == fill_char:
                    return Boundary(Boundary.CORNER)

                if (
                    col not in (0, width - 1)
                    and matrix[row, col - 1] == outside_char
                    or matrix[row, col + 1] == outside_char
                ):
                    return Boundary(Boundary.CORNER)

                return Boundary(Boundary.HORIZONTAL)

            if col in (0, width - 1):
                if (
                    row not in (0, max_height - 1)
                    and matrix[row - 1, col] == outside_char
                    or matrix[row + 1, col] == outside_char
                ):
                    return Boundary(Boundary.CORNER)

                return Boundary(Boundary.VERTICAL)

        return None


class BorderRaster:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, matrix, row, col):
        """Use instance() to initialize BorderRaster"""
        self.nw = matrix[row - 1][col - 1]
        self.no = matrix[row - 1][col]
        self.ne = matrix[row - 1][col + 1]
        self.we = matrix[row][col - 1]
        self.ce = matrix[row][col]
        self.ea = matrix[row][col + 1]
        self.sw = matrix[row + 1][col - 1]
        self.so = matrix[row + 1][col]
        self.se = matrix[row + 1][col - 1]

    @staticmethod
    def instance(matrix, row, col, fill_char):
        """Return an instance of BorderRaster if current row and col are
        not edges else return None."""
        height, width = matrix.shape
        if (
            row > 0
            and row < height - 1
            and col > 0
            and col < width - 1
            and matrix[row][col] == fill_char
        ):
            return BorderRaster(matrix, row, col)
        return None

    def print_raster(self):
        """Print the raster. Used for debugging."""
        print("".join((self.nw, self.no, self.ne)))
        print("".join((self.we, self.ce, self.ea)))
        print("".join((self.sw, self.so, self.se)))


class Border:

    NONE = 0
    DOWN_CORNER = 1
    UP_CORNER = 2
    VERTICAL = 3
    LEFT_VERTICAL = 4
    RIGHT_VERTICAL = 5
    HORIZONTAL = 6
    UP_HORIZONTAL = 7
    DOWN_HORIZONTAL = 8
    NEGATIVE_DIAG = 9  # \
    DOWN_NEGATIVE_DIAG = 10
    UP_NEGATIVE_DIAG = 11
    NEGATIVE_DIAG_LEFT_CORNER = 12
    NEGATIVE_DIAG_RIGHT_CORNER = 13
    NEGATIVE_DIAG_UP_CORNER = 14
    NEGATIVE_DIAG_DOWN_CORNER = 15
    POSITIVE_DIAG = 16  # /
    DOWN_POSITIVE_DIAG = 17
    UP_POSITIVE_DIAG = 18
    POSITIVE_DIAG_LEFT_CORNER = 19
    POSITIVE_DIAG_RIGHT_CORNER = 20
    POSITIVE_DIAG_UP_CORNER = 21
    POSITIVE_DIAG_DOWN_CORNER = 22

    def __init__(self, raster, fill_char, outside_char, no_char):
        self.no_char = no_char
        self.outside_char = outside_char
        self.fill_char = fill_char

        self.b_raster = raster
        self.model = self._get_border_model()

    # pylint: disable=too-many-arguments
    @staticmethod
    def factory(matrix, row, col, fill_char, no_char, outside_char, is_negative):
        raster = BorderRaster.instance(matrix, row, col, fill_char)
        if raster:
            # if raster is a not a border return None else the individual Border
            if (
                fill_char in (raster.no, raster.so, raster.we, raster.ea)
                and is_negative
                or outside_char not in (raster.no, raster.so, raster.we, raster.ea)
            ):
                return None

            return Border(raster, fill_char, outside_char, no_char)

        return None

    # pylint: disable=too-many-branches
    def _get_border_model(self):
        """Calculate and return the border model.

        The order of the function may matter, depending on the verification
        of the individual model. As a rule of thumb: All the more inside and outside
        checks a model verification has, so safer it is to call the function earlier.
        """
        model = self.NONE
        if self._is_positive_diagonal_up_corner():
            model = self.POSITIVE_DIAG_UP_CORNER
        elif self._is_positive_diagonal_down_corner():
            model = self.POSITIVE_DIAG_DOWN_CORNER
        elif self._is_negative_diagonal_up_corner():
            model = self.NEGATIVE_DIAG_UP_CORNER
        elif self._is_negative_diagonal_down_corner():
            model = self.NEGATIVE_DIAG_DOWN_CORNER
        elif self._is_down_corner():
            model = self.DOWN_CORNER
        elif self._is_up_corner():
            model = self.UP_CORNER
        elif self._is_negative_diagonal():
            model = self.NEGATIVE_DIAG
        elif self._is_negative_diagonal_right_corner():
            model = self.NEGATIVE_DIAG_RIGHT_CORNER
        elif self._is_negative_diagonal_left_corner():
            model = self.NEGATIVE_DIAG_LEFT_CORNER
        elif self._is_positive_diagonal():
            model = self.POSITIVE_DIAG
        elif self._is_positive_diagonal_right_corner():
            model = self.POSITIVE_DIAG_RIGHT_CORNER
        elif self._is_positive_diagonal_left_corner():
            model = self.POSITIVE_DIAG_LEFT_CORNER
        elif self._is_vertical():
            model = self.VERTICAL
        elif self._is_horizontal():
            model = self.HORIZONTAL

        return model

    def _check_inside(self, *args):
        """Return True if all args equal the fill char else False"""

        for arg in args:
            if not self.fill_char == arg:
                return False

        return True

    def _check_outside(self, *args):
        """Return True if all args equal the outside char else False"""
        for arg in args:
            if not self.outside_char == arg:
                return False

        return True

    def _is_down_corner(self):
        """x o x
           x x x
           x x x"""
        raster = self.b_raster
        inside = self._check_inside(
            raster.nw, raster.ne, raster.we, raster.ea, raster.sw, raster.so, raster.se
        )
        outside = self._check_outside(raster.no)
        return inside and outside

    def _is_up_corner(self):
        """x x x
           x x x
           x o x"""
        raster = self.b_raster
        inside = self._check_inside(
            raster.sw, raster.se, raster.we, raster.ea, raster.nw, raster.no, raster.ne
        )
        outside = self._check_outside(raster.so)
        return inside and outside

    def _is_vertical(self):
        """. x .
           . x .
           . x ."""
        raster = self.b_raster
        return self._check_inside(raster.no, raster.so)

    def _is_left_vertical(self):
        """x x .
           x x .
           x x ."""
        raster = self.b_raster
        return self._check_inside(raster.no, raster.so, raster.nw, raster.we, raster.sw)

    def _is_right_vertical(self):
        """. x x
           . x x
           . x x"""
        raster = self.b_raster
        return self._check_inside(raster.no, raster.so, raster.ne, raster.ea, raster.se)

    def _is_horizontal(self):
        """. . .
           x x x
           . . ."""
        raster = self.b_raster
        return self._check_inside(raster.we, raster.ea)

    def _is_up_horizontal(self):
        """x x x
           x x x
           . . ."""
        raster = self.b_raster
        return self._check_inside(raster.we, raster.ea, raster.nw, raster.no, raster.ne)

    def _is_down_horizontal(self):
        """. . .
           x x x
           x x x"""
        raster = self.b_raster
        return self._check_inside(raster.we, raster.ea, raster.sw, raster.so, raster.se)

    def _is_negative_diagonal(self):
        """x o .    x x .
           x x o or o x x
           . x x    . o x"""
        return self._is_negative_diagonal_up() or self._is_negative_diagonal_down()

    def _is_negative_diagonal_up(self):
        """x x .
           o x x
           . o x"""
        raster = self.b_raster
        inside = self._check_inside(raster.nw, raster.se, raster.ea, raster.no)
        outside = self._check_outside(raster.so, raster.we)
        return inside and outside

    def _is_negative_diagonal_down(self):
        """x o .
           x x o
           . x x"""
        raster = self.b_raster
        inside = self._check_inside(raster.nw, raster.se, raster.we, raster.so)
        outside = self._check_outside(raster.no, raster.ea)
        return inside and outside

    def _is_negative_diagonal_right_corner(self):
        """x x x
           . x x
           . . ."""
        raster = self.b_raster
        inside = self._check_inside(raster.nw, raster.no, raster.ne, raster.ea)
        outside = self._check_outside(raster.we, raster.sw, raster.so, raster.se)
        return inside and outside

    def _is_negative_diagonal_left_corner(self):
        """. . .
           x x .
           x x x"""
        raster = self.b_raster
        inside = self._check_inside(raster.sw, raster.so, raster.se, raster.we)
        outside = self._check_outside(raster.ea, raster.nw, raster.no, raster.ne)
        return inside and outside

    def _is_negative_diagonal_down_corner(self):
        """x o .
           x x o
           . x o"""
        raster = self.b_raster
        inside = self._check_inside(raster.nw, raster.we, raster.so)
        outside = self._check_outside(raster.no, raster.ea, raster.se)
        return inside and outside

    def _is_negative_diagonal_up_corner(self):
        """o x .
           o x x
           . o x"""
        raster = self.b_raster
        inside = self._check_inside(raster.no, raster.ea, raster.se)
        outside = self._check_outside(raster.nw, raster.we, raster.so)
        return inside and outside

    def _is_positive_diagonal(self):
        """. o x    . x x
           o x x or x x o
           x x .    x o ."""
        return self._is_positive_diagonal_up() or self._is_positive_diagonal_down()

    def _is_positive_diagonal_right_corner(self):
        """o o o
           o x x
           x x x"""
        raster = self.b_raster
        inside = self._check_inside(raster.sw, raster.so, raster.se, raster.ea)
        outside = self._check_outside(raster.we, raster.nw, raster.no, raster.ne)
        return inside and outside

    def _is_positive_diagonal_left_corner(self):
        """x x x
           x x o
           o o o"""
        raster = self.b_raster
        inside = self._check_inside(raster.nw, raster.no, raster.ne, raster.we)
        outside = self._check_outside(raster.ea, raster.sw, raster.so, raster.se)
        return inside and outside

    def _is_positive_diagonal_down_corner(self):
        """. o x
           o x x
           o x ."""
        raster = self.b_raster
        inside = self._check_inside(raster.ne, raster.ea, raster.so)
        outside = self._check_outside(raster.no, raster.we, raster.sw)
        return inside and outside

    def _is_positive_diagonal_up_corner(self):
        """. x o
           x x o
           x o ."""
        raster = self.b_raster
        inside = self._check_inside(raster.we, raster.sw, raster.so)
        outside = self._check_outside(raster.no, raster.ne, raster.ea)
        return inside and outside

    def _is_positive_diagonal_down(self):
        """. o x
           o x x
           x x ."""
        raster = self.b_raster
        inside = self._check_inside(raster.ne, raster.sw, raster.so, raster.ea)
        outside = self._check_outside(raster.no, raster.we)
        return inside and outside

    def _is_positive_diagonal_up(self):
        """. o x
           o x x
           x x ."""
        raster = self.b_raster
        inside = self._check_inside(raster.ne, raster.sw, raster.no, raster.we)
        outside = self._check_outside(raster.so, raster.ea)
        return inside and outside
