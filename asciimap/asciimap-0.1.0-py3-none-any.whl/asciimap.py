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
import time
import functools
import json
import math
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import argparse
from osgeo import ogr
import numpy
from pkg_resources import resource_filename

SHAPEFILE = resource_filename(__name__, "data/ne_110m_admin_0_countries.shp")
DRIVER = ogr.GetDriverByName("ESRI Shapefile")

times = {}


def timeit(method):
    @functools.wraps(method)
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()

        name = method.__name__

        if name in times:
            times[name] += te - ts
        else:
            times[name] = te - ts

        return result

    return timed


# pylint: disable=too-many-instance-attributes,too-many-arguments
class Map:
    """The Map"""

    @timeit
    def __init__(
        self,
        feature,
        max_height=None,
        max_width=None,
        fill_char=None,
        no_char=None,
        outside_char=None,
        blur=None,
        method=None,
        surface=None,
        negative=None,
    ):
        self.max_height = max_height if max_height else 40
        self.max_width = max_width if max_width else 80
        self.fill_char = fill_char if fill_char else "*"
        self.no_char = no_char if no_char else " "
        self.outside_char = outside_char if outside_char else " "
        self.blur = blur if blur else 0.0
        self.method = method if method else "dynamic"
        self.surface = surface if surface else "all"
        self.is_negative = bool(negative)

        if self.is_negative and self.outside_char == " ":
            self.outside_char = "."

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

        if self.method in ("d", "dynamic"):
            self.h_res, self.w_res = (
                (self.h_res, self.h_res)
                if self.h_res > self.w_res
                else (self.w_res, self.w_res)
            )
        elif self.method in ("h", "height"):
            self.h_res, self.w_res = (self.h_res, self.h_res)
        elif self.method in ("w", "width"):
            self.h_res, self.w_res = (self.w_res, self.w_res)
        elif self.method in ("f", "full"):
            pass
            # self.h_res, self.w_res = (self.h_res, self.w_res)

    @timeit
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

    @timeit
    def is_border(self, matrix, h, w):
        if h > 0 and h < self.max_height - 1 and w > 0 and w < self.max_width - 1:
            if (
                self.no_char
                not in (
                    matrix[h - 1][w],
                    matrix[h + 1][w],
                    matrix[h][w - 1],
                    matrix[h][w + 1],
                )
                and self.is_negative
                or self.outside_char
                not in (
                    matrix[h - 1][w],
                    matrix[h + 1][w],
                    matrix[h][w - 1],
                    matrix[h][w + 1],
                )
            ):
                return False

        return True

    @timeit
    def is_vertical(self, matrix, h, w):
        if h > 0 and h < self.max_height - 1 and self.fill_char == matrix[h, w]:
            if (
                self.fill_char == matrix[h - 1][w]
                and self.fill_char == matrix[h + 1][w]
            ):
                return True

        return False

    @timeit
    def is_horizontal(self, matrix, h, w):
        if w > 0 and w < self.max_width - 1 and self.fill_char == matrix[h, w]:
            if (
                self.fill_char == matrix[h][w - 1]
                and self.fill_char == matrix[h][w + 1]
            ):
                return True

        return False

    @timeit
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

    @timeit
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

    def _sum_h_step(self, rows, worker_num, row):
        return self.lowest_lat + (worker_num * rows * self.h_res) + (row * self.h_res)

    def _sum_w_step(self, col):
        return self.lowest_lon + (col * self.w_res)

    # pylint: disable=too-many-locals,too-many-branches
    def render(self, matrix, worker_num):
        rows = len(matrix)
        cols = len(matrix[0])

        cent_lon, cent_lat = json.loads(self.centroid.ExportToJson())["coordinates"]
        lowest_lat = self._sum_h_step(rows, worker_num, 0)
        highest_lat = self._sum_h_step(rows, worker_num, rows)

        if cent_lat >= lowest_lat and cent_lat <= highest_lat:
            name_written = False
            cent_lat_match = int((cent_lat - lowest_lat) / self.h_res)
            cent_lon_match = int((cent_lon - self.lowest_lon) / self.w_res)
        else:
            name_written = True
            cent_lat_match = math.inf
            cent_lon_match = math.inf

        for row in range(0, rows):
            h_step = self._sum_h_step(rows, worker_num, row)
            for col in range(0, cols):
                w_step = self._sum_w_step(col)

                if not name_written and row == cent_lat_match and col == cent_lon_match:
                    if col + len(self.name) > self.max_width - 1:
                        bias = self.max_width - col - 1 - len(self.name)
                    else:
                        bias = 0

                    for k, char in enumerate(self.name):
                        matrix[row][col + k + bias] = char

                    name_written = True

                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(w_step + (self.w_res / 2), h_step + (self.h_res / 2))
                is_surface = self.geom.Contains(point)
                if is_surface and matrix[row][col] == self.no_char:
                    matrix[row][col] = self.fill_char
                elif not is_surface and matrix[row][col] == self.no_char:
                    matrix[row][col] = self.outside_char

        return {str(worker_num): matrix}

    @timeit
    def render_parallel(self):
        worker_count = cpu_count() + 1
        matrix_chunks = numpy.array_split(self.matrix, worker_count)

        with ThreadPool(processes=worker_count) as pool:
            results_l = []
            for num, matrix in enumerate(matrix_chunks):
                results_l.append(pool.apply_async(self.render, (matrix, num)))

            results_d = {}
            for result in results_l:
                results_d.update(result.get())

        matrix = results_d["0"]
        for i in range(1, worker_count):
            key = str(i)
            matrix = numpy.append(matrix, results_d[key], axis=0)

        self.matrix = matrix

    @timeit
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


@timeit
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


class CharType:
    def __call__(self, value):
        if len(str(value)) > 1:
            raise argparse.ArgumentTypeError("Argument must be a single character")

        return str(value)


def parse_args(argv):
    description = "Print countres in ASCII Art"
    epilog = "List all countries and ISO 3166-1 alpha-2 codes with 'list'"
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument(
        "country",
        type=CountryType(),
        help=(
            "Select country by ISO 3166-1 alpha-2 codes. For a complete list "
            "of ISA A2 codes use 'list' as argument"
        ),
    )
    parser.add_argument(
        "--fill",
        "-f",
        default="*",
        type=CharType(),
        help="Single character marking the edges of the land surface",
    )
    parser.add_argument(
        "--empty",
        "-e",
        default=" ",
        type=CharType(),
        help="The character to use for the land surface",
    )
    parser.add_argument(
        "--outside",
        "-o",
        default=" ",
        type=CharType(),
        help="Single character marking the outside surface",
    )
    parser.add_argument(
        "--height",
        "-i",
        default=40,
        type=DimensionType(),
        help="Height of the map as integer",
    )
    parser.add_argument(
        "--width",
        "-w",
        default=80,
        type=DimensionType(),
        help="Width of the map as integer",
    )
    parser.add_argument(
        "--blur",
        "-b",
        default=0,
        type=BlurType(),
        help="Add blur to radius and inflate the surface by double value",
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
        help="Choose a surface by number or 'all'",
    )
    parser.add_argument(
        "--negative", "-n", action="store_true", help="Print the negative"
    )
    parser.add_argument(
        "--benchmark",
        "-t",
        action="store_true",
        help="Print execution times of methods along with the map",
    )

    return parser.parse_args(argv)


@timeit
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
            outside_char=args.outside,
            blur=args.blur,
            method=args.method,
            surface=args.surface,
            negative=args.negative,
        )

        country.render_parallel()
        country.print_map()

    else:
        process_list_cmd()

    if args.benchmark:
        total = 0.0
        for name, time_ in times.items():
            if name != "main":
                total += time_

            print("{:25}{:>10.4f} s".format(name, time_))

        print("{}".format(37 * "-"))
        print("{:25}{:>10.4f} s".format("Sum", total))


if __name__ == "__main__":
    main()
