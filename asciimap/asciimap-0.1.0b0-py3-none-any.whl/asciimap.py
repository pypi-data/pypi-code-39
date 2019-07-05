#!/usr/bin/python

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
import sys
import json
import argparse
from osgeo import ogr
import numpy
from pkg_resources import resource_filename

SHAPEFILE = resource_filename(__name__, "data/ne_110m_admin_0_countries.shp")
DRIVER = ogr.GetDriverByName("ESRI Shapefile")


# pylint: disable=too-many-instance-attributes,too-many-arguments
class Map:
    """The Map"""

    def __init__(
        self,
        feature,
        max_height=None,
        max_width=None,
        fill_char=None,
        no_char=None,
        blur=None,
        method=None,
        surface=None,
    ):
        self.max_height = max_height if max_height else 40
        self.max_width = max_width if max_width else 80
        self.fill_char = fill_char if fill_char else "*"
        self.no_char = no_char if no_char else " "
        self.blur = blur if blur else 0.0
        self.method = method if method else "dynamic"
        self.surface = surface if surface else "all"

        geom = feature.GetGeometryRef()
        self.geom = geom.Buffer(distance=self.blur)
        self.centroid = self.geom.Centroid()

        self.name = feature.NAME_EN

        self.matrix = numpy.full((self.max_height, self.max_width), self.no_char)

        json_d = json.loads(self.geom.ExportToJson())
        self.lowest_lon, self.lowest_lat, self.highest_lon, self.highest_lat = self._get_boundaries(
            json_d
        )

        self.lat_diff = self.highest_lat - self.lowest_lat
        self.lon_diff = self.highest_lon - self.lowest_lon

        self.h_res = self.lat_diff / self.max_height
        self.w_res = self.lon_diff / self.max_width

    def _get_boundaries(self, json_d):
        lowest_lat = 180.0
        lowest_lon = 180.0
        highest_lat = -180.0
        highest_lon = -180.0

        for i, shape in enumerate(json_d["coordinates"]):
            if self.surface != "all":
                if i != self.surface:
                    continue
            for sub in shape:
                if isinstance(sub[0], list):
                    for point in sub:
                        lon = point[0]
                        lat = point[1]
                        lowest_lon = lon if lon < lowest_lon else lowest_lon
                        lowest_lat = lat if lat < lowest_lat else lowest_lat
                        highest_lon = lon if lon > highest_lon else highest_lon
                        highest_lat = lat if lat > highest_lat else highest_lat
                else:
                    lon = sub[0]
                    lat = sub[1]
                    lowest_lon = lon if lon < lowest_lon else lowest_lon
                    lowest_lat = lat if lat < lowest_lat else lowest_lat
                    highest_lon = lon if lon > highest_lon else highest_lon
                    highest_lat = lat if lat > highest_lat else highest_lat

        return (lowest_lon, lowest_lat, highest_lon, highest_lat)

    def is_border(self, matrix, h, w):
        if h > 0 and h < self.max_height - 1 and w > 0 and w < self.max_width - 1:
            if self.no_char not in (
                matrix[h - 1][w],
                matrix[h + 1][w],
                matrix[h][w - 1],
                matrix[h][w + 1],
            ):
                return False

        return True

    def is_vertical(self, matrix, h, w):
        if h > 0 and h < self.max_height - 1 and self.fill_char == matrix[h, w]:
            if (
                self.fill_char == matrix[h - 1][w]
                and self.fill_char == matrix[h + 1][w]
            ):
                return True

        return False

    def is_horizontal(self, matrix, h, w):
        if w > 0 and w < self.max_width - 1 and self.fill_char == matrix[h, w]:
            if (
                self.fill_char == matrix[h][w - 1]
                and self.fill_char == matrix[h][w + 1]
            ):
                return True

        return False

    def is_negativ_diagonal(self, matrix, h, w):
        if (
            h > 0
            and h < self.max_height - 1
            and w > 0
            and w < self.max_width - 1
            and self.fill_char == matrix[h, w]
        ):
            if (
                self.fill_char == matrix[h - 1][w - 1]
                and self.fill_char == matrix[h + 1][w + 1]
            ):
                return True

        return False

    def is_positiv_diagonal(self, matrix, h, w):
        if (
            h > 0
            and h < self.max_height - 1
            and w > 0
            and w < self.max_width - 1
            and self.fill_char == matrix[h, w]
        ):
            if (
                self.fill_char == matrix[h - 1][w + 1]
                and self.fill_char == matrix[h + 1][w - 1]
            ):
                return True

        return False

    # pylint: disable=too-many-locals,too-many-branches
    def render(self):
        if self.method in ("d", "dynamic"):
            h_res, w_res = (
                (self.h_res, self.h_res)
                if self.h_res > self.w_res
                else (self.w_res, self.w_res)
            )
        elif self.method in ("h", "height"):
            h_res, w_res = (self.h_res, self.h_res)
        elif self.method in ("w", "width"):
            h_res, w_res = (self.w_res, self.w_res)
        elif self.method in ("f", "full"):
            h_res, w_res = (self.h_res, self.w_res)

        name_written = False
        for i in range(0, self.max_height):
            h_step = self.lowest_lat + (i * h_res)
            for j in range(0, self.max_width):
                w_step = self.lowest_lon + (j * w_res)
                if not name_written:
                    ring = ogr.Geometry(ogr.wkbLinearRing)
                    ring.AddPoint(w_step, h_step)
                    ring.AddPoint(w_step + w_res, h_step)
                    ring.AddPoint(w_step + w_res, h_step + h_res)
                    ring.AddPoint(w_step, h_step + h_res)
                    ring.CloseRings()

                    box = ogr.Geometry(ogr.wkbPolygon)
                    box.AddGeometry(ring)

                    if box.Contains(self.centroid):
                        if j + len(self.name) > self.max_width - 1:
                            bias = self.max_width - j - 1 - len(self.name)
                        else:
                            bias = 0

                        for k, char in enumerate(self.name):
                            self.matrix[i][j + k + bias] = char

                        name_written = True

                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(w_step, h_step)
                if self.geom.Contains(point) and self.matrix[i][j] == self.no_char:
                    self.matrix[i][j] = self.fill_char

    def print_map(self):
        B = self.matrix.copy()
        for i in range(0, self.max_height):
            for j in range(0, self.max_width):
                k = self.max_height - i - 1
                if self.is_border(self.matrix, k, j):
                    B[k][j] = self.matrix[k][j]
                elif self.matrix[k][j] == self.fill_char:
                    B[k][j] = self.no_char
                else:
                    B[k][j] = self.matrix[k][j]

        for i in range(0, self.max_height):
            for j in range(0, self.max_width):
                k = self.max_height - i - 1
                if self.is_border(self.matrix, k, j):
                    if self.is_vertical(B, k, j):
                        print("|", end="")
                    elif self.is_horizontal(B, k, j):
                        print("-", end="")
                    elif self.is_negativ_diagonal(B, k, j):
                        print("/", end="")
                    elif self.is_positiv_diagonal(B, k, j):
                        print("\\", end="")
                    else:
                        if B[k][j] == self.fill_char:
                            print(self.fill_char, end="")
                        else:
                            print(B[k][j], end="")
                elif B[k][j] == self.fill_char:
                    print(self.no_char, end="")
                else:
                    print(B[k][j], end="")

            print()


def parse_undefined_countries(feature):
    if feature.NAME_EN == "France":
        return "fr"
    if feature.NAME_EN == "Somaliland":
        return "xb"
    if feature.NAME_EN == "Turkish Republic of Northern Cyprus":
        return "xa"
    if feature.NAME_EN == "Norway":
        return "no"

    return None


# pylint: disable=too-few-public-methods
class CountryType:
    def __call__(self, value):
        data = DRIVER.Open(SHAPEFILE, 0)
        layer = data.GetLayer()
        feature = ""
        if value == "list":
            return value

        for feat in layer:
            if feat.ISO_A2.lower() == value.lower():
                return feat

            if feat.ISO_A2 == "-99":
                country_code = parse_undefined_countries(feat)
                if country_code == value:
                    return feat

        raise argparse.ArgumentTypeError("Country not found: '{}'".format(value))


class DimensionType:
    def __call__(self, value):
        try:
            integer = int(value)
        except Exception:
            raise argparse.ArgumentTypeError(
                "Dimension must be a valid integer: Found '{}'".format(value)
            )

        if integer <= 0:
            raise argparse.ArgumentTypeError("Dimension must be greater than 0")

        return integer


class BlurType:
    def __call__(self, value):
        try:
            double = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError("Blur must be of type 'float'")

        return double


class SurfaceType:
    def __call__(self, value):
        if value != "all":
            try:
                return int(value)
            except ValueError:
                raise argparse.ArgumentTypeError(
                    "Surface must be of type 'int' or 'all'"
                )

        return value


def parse_args(argv):
    description = "Print countres in ASCII Art"
    epilog = "List all countries and ISO 3166-1 alpha-2 codes with 'list'"
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument(
        "country", type=CountryType(), help="Select country by ISO 3166-1 alpha-2 codes"
    )
    parser.add_argument("--fill", "-f", help="Single character")
    parser.add_argument(
        "--height", "-i", type=DimensionType(), help="Height of the map"
    )
    parser.add_argument("--width", "-w", type=DimensionType(), help="Width of the map")
    parser.add_argument("--empty", "-e", help="The character to use for empty space")
    parser.add_argument(
        "--blur", "-b", type=BlurType(), help="Add blur to radius and inflate the map"
    )
    parser.add_argument(
        "--method",
        "-m",
        choices=["full", "f", "dynamic", "d", "height", "h", "width", "w"],
        default="dynamic",
        help="Change rendering method",
    )
    parser.add_argument(
        "--surface",
        "-s",
        type=SurfaceType(),
        default="all",
        help="Choose a surface or 'all'",
    )

    return parser.parse_args(argv)


def process_list_cmd():
    data = DRIVER.Open(SHAPEFILE, 0)
    layer = data.GetLayer()
    for feat in layer:
        lower_country_code = feat.ISO_A2.lower()
        if lower_country_code == "-99":
            country_code = parse_undefined_countries(feat)
            if country_code:
                lower_country_code = country_code.lower()

        print(lower_country_code, feat.NAME_EN)


def main():

    if not sys.argv[1:]:
        sys.argv.extend(["-h"])

    args = parse_args(sys.argv[1:])

    if args.country != "list":
        country = Map(
            args.country,
            max_height=args.height,
            max_width=args.width,
            fill_char=args.fill,
            no_char=args.empty,
            blur=args.blur,
            method=args.method,
            surface=args.surface,
        )
        country.render()
        country.print_map()
    else:
        process_list_cmd()


if __name__ == "__main__":
    main()
