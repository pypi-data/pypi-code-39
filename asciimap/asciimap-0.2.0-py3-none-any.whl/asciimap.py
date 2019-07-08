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


def timeit(func_=None, *, super_func=None, worker_count=1):
    def decorator_timeit(func):
        @functools.wraps(func)
        def timed(*args, **kwargs):
            ts = time.time()
            result = func(*args, **kwargs)
            te = time.time()

            if super_func:
                name = func.__name__ + " ({})".format(super_func)
            else:
                name = func.__name__

            if name in times:
                times[name]["time"] += (te - ts) / worker_count
                times[name]["calls"] += 1
            else:
                times[name] = {}
                times[name]["time"] = (te - ts) / worker_count
                times[name]["calls"] = 1

            return result

        return timed

    if func_ is None:
        return decorator_timeit

    return decorator_timeit(func_)


# pylint: disable=too-many-instance-attributes,too-many-arguments
class Map:
    """The Map"""

    # pylint: disable=too-many-locals,too-many-branches
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
        self.surface = surface if surface is not None else "all"
        self.is_negative = bool(negative)

        if self.is_negative and self.outside_char == " ":
            self.outside_char = "."

        geom = feature.GetGeometryRef()
        self.geom = geom.Buffer(distance=self.blur)
        json_d = json.loads(self.geom.ExportToJson())

        if self.surface != "all":
            if len(json_d["coordinates"]) > self.surface:
                json_d["coordinates"] = [json_d["coordinates"][self.surface]]
                self.geom = ogr.CreateGeometryFromJson(json.dumps(json_d))
            else:
                self.surface = "all"

        self.centroid = self.geom.Centroid()

        self.name = feature.NAME_EN

        self.lowest_lon, self.lowest_lat, self.highest_lon, self.highest_lat = self._get_boundaries(
            json_d
        )

        self.lat_diff = self.highest_lat - self.lowest_lat
        self.lon_diff = self.highest_lon - self.lowest_lon

        h_res = self.lat_diff / self.max_height
        w_res = self.lon_diff / self.max_width

        self._apply_rendering_method(h_res, w_res, max_height, max_width)

        self.worker_count = cpu_count() + 1

        self.matrix = numpy.full((self.max_height, self.max_width), self.no_char)

    @staticmethod
    def _distance_haversine(lat1, lat2, lon1, lon2):
        R = 6371e3
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lam = math.radians(lon1 - lon2)

        a = (
            math.sin(d_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        d = R * c
        return d

    def _apply_rendering_method(self, h_res, w_res, max_height, max_width):
        if self.method in ("d", "dynamic"):
            if h_res > w_res:
                self.h_res, self.w_res = (h_res, h_res)
                if not max_width:
                    self.max_width = math.ceil(self.lon_diff / self.w_res)
            else:
                self.h_res, self.w_res = (w_res, w_res)
                if not max_height:
                    self.max_height = math.ceil(self.lat_diff / self.h_res)
        elif self.method in ("h", "height"):
            self.h_res, self.w_res = (h_res, h_res)
            if not max_width:
                self.max_width = math.ceil(self.lon_diff / self.w_res)
        elif self.method in ("w", "width"):
            self.h_res, self.w_res = (w_res, w_res)
            if not max_height:
                self.max_height = math.ceil(self.lat_diff / self.h_res)
        elif self.method in ("f", "full"):
            self.h_res, self.w_res = (h_res, w_res)

    @timeit
    def _get_boundaries(self, json_d):
        lowest_lat = 180.0
        lowest_lon = 180.0
        highest_lat = -180.0
        highest_lon = -180.0

        num_points = 0
        num_poly = 0
        for shape in json_d["coordinates"]:
            for sub in shape:
                if json_d["type"] == "MultiPolygon":
                    for lon, lat in sub:
                        lowest_lon = lon if lon < lowest_lon else lowest_lon
                        lowest_lat = lat if lat < lowest_lat else lowest_lat
                        highest_lon = lon if lon > highest_lon else highest_lon
                        highest_lat = lat if lat > highest_lat else highest_lat
                        num_points += 1
                else:
                    lon, lat = sub
                    lowest_lon = lon if lon < lowest_lon else lowest_lon
                    lowest_lat = lat if lat < lowest_lat else lowest_lat
                    highest_lon = lon if lon > highest_lon else highest_lon
                    highest_lat = lat if lat > highest_lat else highest_lat
                    num_points += 1

            num_poly += 1

        setattr(self, "num_points", num_points)
        setattr(self, "num_poly", num_poly)
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

    @timeit(super_func="render")
    def _sum_h_step(self, processed_rows, row):
        return self.lowest_lat + (processed_rows * self.h_res) + (row * self.h_res)

    @timeit(super_func="render")
    def _sum_w_step(self, col):
        return self.lowest_lon + (col * self.w_res)

    @timeit(super_func="render")
    def _contains(self, intersection_d, point):
        lon, _ = point
        if intersection_d["type"] == "LineString":
            if intersection_d["coordinates"]:
                east = intersection_d["coordinates"][0][0]
                west = intersection_d["coordinates"][1][0]
                multiline = False
            else:
                return False

        elif intersection_d["type"] == "MultiLineString":
            if intersection_d["coordinates"]:
                east = intersection_d["coordinates"][0][0][0]
                west = intersection_d["coordinates"][0][1][0]
                multiline = True
            else:
                return False
        else:
            return False

        if lon < east:
            return False

        if lon >= east and lon <= west:
            return True

        if multiline:
            intersection_d["coordinates"] = intersection_d["coordinates"][1:]
        else:
            intersection_d["coordinates"] = []

        return False

    @timeit(super_func="render")
    def _create_intersection(self, mv):
        line = ogr.Geometry(ogr.wkbLineString)
        line.AddPoint_2D(self.lowest_lon, mv)
        line.AddPoint_2D(self.highest_lon, mv)

        return self.geom.Intersection(line)

    # pylint: disable=too-many-locals,too-many-branches
    @timeit(super_func="render_parallel")
    def render(self, matrix, worker_num, processed_rows):
        rows = len(matrix)
        cols = len(matrix[0])

        cent_lon, cent_lat = json.loads(self.centroid.ExportToJson())["coordinates"]
        lowest_lat = self._sum_h_step(processed_rows, 0)
        highest_lat = self._sum_h_step(processed_rows, rows)

        if cent_lat >= lowest_lat and cent_lat <= highest_lat:
            name_written = False
            cent_lat_match = int((cent_lat - lowest_lat) / self.h_res)
            cent_lon_match = int((cent_lon - self.lowest_lon) / self.w_res)
        else:
            name_written = True
            cent_lat_match = math.inf
            cent_lon_match = math.inf

        for row in range(0, rows):
            h_step = self._sum_h_step(processed_rows, row)
            mv = h_step + (self.h_res / 2)
            intersection = self._create_intersection(mv)
            intersection_d = json.loads(intersection.ExportToJson())
            mh = self.w_res / 2
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

                point = (w_step + mh, mv)
                is_surface = self._contains(intersection_d, point)
                if is_surface and matrix[row][col] == self.no_char:
                    matrix[row][col] = self.fill_char
                elif not is_surface and matrix[row][col] == self.no_char:
                    matrix[row][col] = self.outside_char

        return {str(worker_num): matrix}

    @timeit
    def render_parallel(self):
        matrix_chunks = numpy.array_split(self.matrix, self.worker_count)

        rows = 0
        with ThreadPool(processes=self.worker_count) as pool:
            results_l = []
            for num, matrix in enumerate(matrix_chunks):
                results_l.append(pool.apply_async(self.render, (matrix, num, rows)))
                rows += len(matrix)

            results_d = {}
            for result in results_l:
                results_d.update(result.get())

        matrix = results_d["0"]
        for i in range(1, self.worker_count):
            key = str(i)
            matrix = numpy.append(matrix, results_d[key], axis=0)

        self.matrix = matrix

    @timeit
    def print_map(self):
        for i in range(0, self.max_height):
            line = numpy.empty(self.max_width, dtype="U1")
            for j in range(0, self.max_width):
                k = self.max_height - i - 1
                if self.is_border(self.matrix, k, j):
                    if self.is_vertical(self.matrix, k, j):
                        line[j] = "|"
                    elif self.is_horizontal(self.matrix, k, j):
                        line[j] = "-"
                    elif self.is_negativ_diagonal(self.matrix, k, j):
                        line[j] = "/"
                    elif self.is_positiv_diagonal(self.matrix, k, j):
                        line[j] = "\\"
                    else:
                        if self.matrix[k][j] == self.fill_char:
                            line[j] = self.fill_char
                        else:
                            line[j] = self.matrix[k][j]
                elif self.matrix[k][j] == self.fill_char:
                    line[j] = self.no_char
                else:
                    line[j] = self.matrix[k][j]

            print("".join(line))


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
    description = "Print countries in ASCII Art"
    epilog = "List all countries and ISO 3166-1 alpha-2 codes with 'list'"
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument(
        "country",
        type=CountryType(),
        help=(
            "Select country by ISO 3166-1 alpha-2 codes. For a complete list "
            "of ISO A2 codes use 'list' as argument"
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
        "--height", "-i", type=DimensionType(), help="Height of the map as integer"
    )
    parser.add_argument(
        "--width", "-w", type=DimensionType(), help="Width of the map as integer"
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
        action="count",
        help=(
            "Print execution times of methods along with the map. Can be give "
            "multiple times to increase verbosity."
        ),
    )
    parser.add_argument("--stats", "-x", action="store_true", help="Print statistics")

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

        if args.stats:
            print()
            print("{:30} {:23.20f}".format("vertical resolution", country.h_res))
            print("{:30} {:23.20f}".format("horizontal resolution", country.h_res))
            print("{:30} {:23d}".format("Height", country.max_height))
            print("{:30} {:23d}".format("Width", country.max_width))
            print(
                "{:30} {:23d}".format(
                    "number of points", getattr(country, "num_points")
                )
            )
            print(
                "{:30} {:23d}".format(
                    "number of polygons", getattr(country, "num_poly")
                )
            )
            print(
                "{:30} {:23d}".format(
                    "number of parallel processes", country.worker_count
                )
            )

    else:
        process_list_cmd()

    if args.benchmark:
        verbose = bool(args.benchmark == 2)

        print()
        total = 0.0
        for name, values in times.items():
            time_ = values["time"]
            if name != "main" and "(" not in name:
                total += time_
                print("{:30}{:>10.4f} s".format(name, time_))
            else:
                print("{:30}{:>10.4f}ps".format(name, time_))

            if verbose:
                calls = values["calls"]
                print("{:30}{:>10d}".format("  calls", calls))
                print("{:30}{:>10.6f}ms".format("  ms/call", time_ / calls * 1000))

        print("{}".format(42 * "-"))
        print("{:30}{:>10.4f} s".format("Sum", total))


if __name__ == "__main__":
    main()
