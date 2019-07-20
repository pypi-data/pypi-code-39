"""Logic for asciimap or for usage as API"""

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

import json
import math

from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count, Queue
from osgeo import ogr, gdal
import numpy
from pkg_resources import resource_filename

from asciimap import RenderConfig, PrinterConfig, MapConfig
from asciimap.border import Border, Boundary


class OgrErrorHandler:
    def __init__(self):
        self.err_level = gdal.CE_None
        self.err_no = 0
        self.err_msg = ""

    def handler(self, err_level, err_no, err_msg):
        self.err_level = err_level
        self.err_no = err_no
        self.err_msg = err_msg


gdal.PushErrorHandler(OgrErrorHandler().handler)
ogr.UseExceptions()
SHAPEFILE = resource_filename(__name__, "data/ne_110m_admin_0_countries.shp")
DRIVER = ogr.GetDriverByName("ESRI Shapefile")


class RenderError(BaseException):
    """Raised during rendering errors"""


class MapError(BaseException):
    """Raise during map errors"""


def _add_point_lon_translated(ring, point, trans):
    lon, lat = point
    new_lon = math.fsum((lon, -trans))
    if new_lon < -180.0 or math.isclose(new_lon, -180.0, abs_tol=1e-9):
        new_lon = math.fsum((new_lon, 360.0))
        ring.AddPoint_2D(new_lon, lat)
    elif new_lon > 180.0 or math.isclose(new_lon, 180.0, abs_tol=1e-9):
        new_lon = math.fsum((new_lon, -360.0))
        ring.AddPoint_2D(new_lon, lat)
    else:
        ring.AddPoint_2D(new_lon, lat)


def _fix_geometry(geom):
    if not geom.IsValid():
        return geom.Buffer(0.0)

    return geom


def translate_lon(shape, trans):
    ring = ogr.Geometry(ogr.wkbLinearRing)

    for point in shape.GetPoints():
        _add_point_lon_translated(ring, point, trans)

    ring.CloseRings()
    return ring


def _add_polygon_to_multipolygon(geom, polygon):
    polygon = _fix_geometry(polygon)  # may result in a multipolygon

    if geom.Intersects(polygon):
        geom = geom.Union(polygon)
    else:
        if polygon.GetGeometryType() == ogr.wkbMultiPolygon:
            for i in range(polygon.GetGeometryCount()):
                geom.AddGeometry(polygon.GetGeometryRef(i))
        else:
            geom.AddGeometry(polygon)

    geom = _fix_geometry(geom)


def center_geom_around_centroid(geom):
    lon_trans = geom.Centroid().GetX()
    if geom.GetGeometryType() == ogr.wkbMultiPolygon:
        new_geom = ogr.Geometry(ogr.wkbMultiPolygon)
    else:
        new_geom = ogr.Geometry(ogr.wkbPolygon)

    if geom.GetGeometryType() == ogr.wkbMultiPolygon:
        for j in range(geom.GetGeometryCount()):
            for shape in geom.GetGeometryRef(j):
                ring = translate_lon(shape, lon_trans)

                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(ring)

                _add_polygon_to_multipolygon(new_geom, polygon)

    else:  # wkbPolygon
        shape = geom.GetGeometryRef(0)
        ring = translate_lon(shape, lon_trans)

        new_geom.AddGeometry(ring)
        new_geom = _fix_geometry(new_geom)

    return new_geom


def distance_haversine(lat1, lat2, lon1, lon2):
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


class Render:
    def __init__(self, feature):
        config = MapConfig()
        r_config = RenderConfig()

        geom = feature.GetGeometryRef()

        self.geom = geom.Buffer(distance=config["blur"])
        json_d = json.loads(self.geom.ExportToJson())

        if config["surface"] != "all":
            if len(json_d["coordinates"]) > config["surface"]:
                json_d["coordinates"] = [json_d["coordinates"][config["surface"]]]
                self.geom = ogr.CreateGeometryFromJson(json.dumps(json_d))
            else:
                config["surface"] = "all"

        r_config["name"] = feature.NAME_EN

        r_config["geom"] = self.geom
        centroid = r_config["geom"].Centroid()
        r_config["centroid"] = centroid.GetPoint_2D()

        geom_d = json.loads(r_config["geom"].ExportToJson())
        r_config["lowest_lon"], r_config["lowest_lat"], r_config[
            "highest_lon"
        ], r_config["highest_lat"] = self._get_boundaries(geom_d)

        r_config["lat_diff"] = math.fsum(
            (r_config["highest_lat"], -r_config["lowest_lat"])
        )
        r_config["lon_diff"] = math.fsum(
            (r_config["highest_lon"], -r_config["lowest_lon"])
        )

        h_res = r_config["lat_diff"] / config["max_height"]
        w_res = r_config["lon_diff"] / config["max_width"]

        r_config["worker_count"] = cpu_count()
        self.r_config = r_config

        self._apply_rendering_method(h_res, w_res)

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

        return (lowest_lon, lowest_lat, highest_lon, highest_lat)

    @staticmethod
    def _apply_rendering_method(h_res, w_res):
        r_config = RenderConfig()
        config = MapConfig()
        lon_diff = r_config["lon_diff"]
        lat_diff = r_config["lat_diff"]

        method = config["method"]
        if method in ("d", "dynamic"):
            if h_res > w_res:
                method = "height"
            else:
                method = "width"

        if method in ("h", "height"):
            r_config.update({"h_res": h_res, "w_res": h_res})
            if not config["width"]:
                r_config["max_width"] = math.ceil(lon_diff / r_config["w_res"])
            else:
                r_config["max_width"] = config["width"]
            r_config["max_height"] = config["max_height"]

        elif method in ("w", "width"):
            r_config.update({"h_res": w_res, "w_res": w_res})
            if not config["height"]:
                r_config["max_height"] = math.ceil(lat_diff / r_config["h_res"])
            else:
                r_config["max_height"] = config["height"]
            r_config["max_width"] = config["max_width"]

        elif method in ("f", "full"):
            r_config.update({"h_res": h_res, "w_res": w_res})
            r_config["max_height"] = (
                config["height"] if config["height"] else config["max_height"]
            )
            r_config["max_width"] = (
                config["width"] if config["width"] else config["max_width"]
            )
        else:
            raise ValueError(
                "Rendering Method '{}' is not implemented.".format(config["method"])
            )

    def _sum_h_step(self, processed_rows, row):
        r_config = self.r_config
        return math.fsum(
            (
                r_config["highest_lat"],
                -(processed_rows * r_config["h_res"]),
                -(row * r_config["h_res"]),
            )
        )

    def _sum_w_step(self, col):
        r_config = self.r_config
        return math.fsum((r_config["lowest_lon"], (col * r_config["w_res"])))

    @staticmethod
    def _contains(intersection_d, point):
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

        if (lon > east or math.isclose(lon, east, abs_tol=1e-9)) and (
            lon < west or math.isclose(lon, west, abs_tol=1e-9)
        ):
            return True

        if multiline:
            intersection_d["coordinates"] = intersection_d["coordinates"][1:]
        else:
            intersection_d["coordinates"] = []

        return False

    def _create_intersection(self, mv):
        r_config = self.r_config
        line = ogr.Geometry(ogr.wkbLineString)
        line.AddPoint_2D(r_config["lowest_lon"], mv)
        line.AddPoint_2D(r_config["highest_lon"], mv)

        return r_config["geom"].Intersection(line)

    # pylint: disable=too-many-locals,too-many-branches
    def _worker(self, line_num):
        r_config = self.r_config
        h_res = r_config["h_res"]
        w_res = r_config["w_res"]
        cent_lon, cent_lat = r_config["centroid"]
        name = r_config["name"]
        max_width = r_config["max_width"]

        config = MapConfig()
        no_char = config["no_char"]
        fill_char = config["fill_char"]
        outside_char = config["outside_char"]

        lowest_lat = self._sum_h_step(line_num, 1)
        highest_lat = self._sum_h_step(line_num, 0)

        if (
            cent_lat > lowest_lat or math.isclose(cent_lat, lowest_lat, abs_tol=1e-9)
        ) and (
            cent_lat < highest_lat or math.isclose(cent_lat, highest_lat, abs_tol=1e-9)
        ):
            name_written = False
            cent_lon_match = int(
                (math.fsum((cent_lon, -r_config["lowest_lon"]))) / w_res
            )
        else:
            name_written = True
            cent_lon_match = math.inf

        h_step = highest_lat
        mv = math.fsum((h_step, -(h_res / 2)))
        intersection = self._create_intersection(mv)
        if not intersection:
            raise RenderError("Could not create intersection.")

        intersection_d = json.loads(intersection.ExportToJson())
        mh = w_res / 2
        line = numpy.full(max_width, fill_value=no_char)
        for col in range(0, line.shape[0]):
            w_step = self._sum_w_step(col)

            if not name_written and col == cent_lon_match:
                if col + len(name) > max_width - 1:
                    bias = max_width - col - 1 - len(name)
                else:
                    bias = 0

                for k, char in enumerate(name):
                    line[col + k + bias] = char

                name_written = True

            point = (math.fsum((w_step, mh)), mv)
            is_surface = self._contains(intersection_d, point)
            if is_surface and line[col] == no_char:
                line[col] = fill_char
            elif not is_surface and line[col] == no_char:
                line[col] = outside_char

        return line

    def render_parallel(self):
        r_config = self.r_config
        if r_config["max_height"] < r_config["worker_count"]:
            worker_count = r_config["max_height"]
        else:
            worker_count = r_config["worker_count"]

        printer = Printer()

        with ThreadPool(processes=worker_count) as pool:
            for line_num in range(0, r_config["max_height"], worker_count - 1):
                results_l = []
                for _ in range(worker_count - 1):
                    results_l.append(pool.apply_async(self._worker, (line_num,)))
                    line_num += 1
                    if line_num >= r_config["max_height"]:
                        break

                for result in results_l:
                    line = result.get()
                    printer.queue.put(line)

                if line_num <= worker_count - 1:
                    pool.apply_async(printer.print_queue)

                if line_num >= r_config["max_height"]:
                    break

        printer.queue.close()
        printer.queue.join_thread()

        pool.join()


class Printer:
    def __init__(self, is_unicode=False):
        p_config = PrinterConfig()
        config = MapConfig()
        r_config = RenderConfig()
        p_config["fill_char"] = config["fill_char"]
        p_config["no_char"] = config["no_char"]
        p_config["outside_char"] = config["outside_char"]
        p_config["is_negative"] = config["is_negative"]
        p_config["is_unicode"] = is_unicode
        self.fill_char = p_config["fill_char"]
        self.no_char = p_config["no_char"]
        self.outside_char = p_config["outside_char"]
        self.is_negative = p_config["is_negative"]
        self.is_unicode = p_config["is_unicode"]

        r_height = r_config["max_height"]
        r_width = r_config["max_width"]
        if config["height"]:
            p_height = config["height"]
        else:
            if r_height >= config["max_height"]:
                p_height = r_height
            else:
                p_height = config["max_height"]

        if config["width"]:
            p_width = config["width"]
        else:
            if r_width >= config["max_width"]:
                p_width = r_width
            else:
                p_width = config["max_width"]

        padding_bottom, padding_top = self._get_slice(p_height, r_height)
        padding_left, padding_right = self._get_slice(p_width, r_width)

        p_config["padding"] = (padding_top, padding_right, padding_bottom, padding_left)

        p_config.update({"max_width": p_width, "max_height": p_height})
        self.p_config = p_config
        self.queue = Queue()

    @staticmethod
    def _get_slice(length, other):
        lower = (length // 2) - (other // 2)
        upper = lower - ((length - other) % 2)

        return (lower, upper)

    @staticmethod
    def get_boundary_char(boundary):
        model = boundary.model
        char = ""
        if model == boundary.VERTICAL:
            char = "|"
        elif model == boundary.HORIZONTAL:
            char = "-"
        elif model == boundary.CORNER:
            char = "·"

        return char

    # pylint: disable=too-many-branches
    @staticmethod
    def get_border_char(border):
        char = ""
        model = border.model
        if model == border.DOWN_CORNER:
            char = "`"
        elif model == border.UP_CORNER:
            char = ","
        elif model == border.NEGATIVE_DIAG:
            char = "\\"
        elif model == border.NEGATIVE_DIAG_RIGHT_CORNER:
            char = "`"
        elif model == border.NEGATIVE_DIAG_LEFT_CORNER:
            char = "."
        elif model == border.NEGATIVE_DIAG_UP_CORNER:
            char = "`"
        elif model == border.NEGATIVE_DIAG_DOWN_CORNER:
            char = "\\"
        elif model == border.POSITIVE_DIAG:
            char = "/"
        elif model == border.POSITIVE_DIAG_RIGHT_CORNER:
            char = ","
        elif model == border.POSITIVE_DIAG_LEFT_CORNER:
            char = "´"
        elif model == border.POSITIVE_DIAG_UP_CORNER:
            char = "·"
        elif model == border.POSITIVE_DIAG_DOWN_CORNER:
            char = "´"
        elif model == border.VERTICAL:
            char = "|"
        elif model == border.HORIZONTAL:
            char = "-"
        elif model == border.NONE:
            char = "·"

        return char

    # TODO: Adapt to new border models
    @staticmethod
    def get_border_char_unicode(border):
        char = ""
        model = border.model
        if model == border.DOWN_CORNER:
            char = "▙"
        elif model == border.UP_CORNER:
            char = "▜"
        elif model == border.DOWN_NEGATIVE_DIAG:
            char = "▗"
        elif model == border.UP_NEGATIVE_DIAG:
            char = "▘"
        elif model == border.DOWN_POSITIVE_DIAG:
            char = "▖"
        elif model == border.UP_POSITIVE_DIAG:
            char = "▝"
        elif model == border.LEFT_VERTICAL:
            char = "▎"
        elif model == border.RIGHT_VERTICAL:
            char = "▕"
        elif model == border.UP_HORIZONTAL:
            char = "▔"
        elif model == border.DOWN_HORIZONTAL:
            char = "▁"

        return char

    def _get_char(self, matrix, max_height, row, col, line_num):
        fallback_char = "·"

        boundary = Boundary.factory(
            matrix, max_height, line_num, row, col, self.fill_char, self.outside_char
        )
        if boundary:
            char = fallback_char
            if self.is_negative:
                char = self.no_char

            boundary_char = self.get_boundary_char(boundary)
            if boundary_char:
                char = boundary_char

            return char

        border = Border.factory(
            matrix,
            row,
            col,
            self.fill_char,
            self.no_char,
            self.outside_char,
            self.is_negative,
        )

        orig_char = matrix[row][col]
        if border:
            if self.is_unicode:
                border_char = self.get_border_char_unicode(border)
            else:
                border_char = self.get_border_char(border)

            if border_char:
                orig_char = border_char

            if orig_char == self.fill_char:
                orig_char = fallback_char

            return orig_char

        if orig_char == self.fill_char:
            return self.no_char

        return orig_char

    def print_queue(self):
        r_config = RenderConfig()
        matrix = numpy.full((3, r_config["max_width"]), fill_value="X")
        line_num = 0
        max_height = r_config["max_height"]
        pad_top, pad_right, pad_bottom, pad_left = self.p_config["padding"]
        if pad_top:
            print("\n" * pad_top, end="")

        while True:
            line = self.queue.get()

            matrix[0] = matrix[1]
            matrix[1] = matrix[2]
            matrix[2] = line

            if line_num == max_height - 1:
                result = self.process_line(matrix, max_height, 1, line_num - 1)
                string = "{}{}{}".format(
                    pad_left * self.outside_char,
                    "".join(result),
                    pad_right * self.outside_char,
                )
                print(string)
                result = self.process_line(matrix, max_height, 2, line_num)
                string = "{}{}{}".format(
                    pad_left * self.outside_char,
                    "".join(result),
                    pad_right * self.outside_char,
                )
                print(string)
                break
            elif line_num > 2:
                result = self.process_line(matrix, max_height, 1, line_num - 1)
                string = "{}{}{}".format(
                    pad_left * self.outside_char,
                    "".join(result),
                    pad_right * self.outside_char,
                )
                print(string)
            elif line_num == 2:
                result = self.process_line(matrix, max_height, 0, line_num - 2)
                string = "{}{}{}".format(
                    pad_left * self.outside_char,
                    "".join(result),
                    pad_right * self.outside_char,
                )
                print(string)
                result = self.process_line(matrix, max_height, 1, line_num - 1)
                string = "{}{}{}".format(
                    pad_left * self.outside_char,
                    "".join(result),
                    pad_right * self.outside_char,
                )
                print(string)

            line_num += 1

        if pad_bottom:
            print("\n" * pad_bottom, end="")

    def process_line(self, matrix, max_height, row, line_num):
        r_config = RenderConfig()
        max_width = r_config["max_width"]

        line = numpy.empty(max_width, dtype="U1")
        for j in range(0, max_width):
            line[j] = self._get_char(matrix, max_height, row, j, line_num)

        return line


# pylint: disable=too-many-instance-attributes,too-many-arguments
class Map:
    """The Map"""

    # pylint: disable=too-many-locals,too-many-branches
    def __init__(
        self,
        max_height=None,
        max_width=None,
        fill_char=None,
        no_char=None,
        outside_char=None,
        blur=None,
        method=None,
        surface=None,
        negative=None,
        is_unicode=None,
    ):

        config = MapConfig()

        config["max_height"] = max_height if max_height else 40
        config["height"] = max_height
        config["max_width"] = max_width if max_width else 80
        config["width"] = max_width
        config["fill_char"] = fill_char if fill_char else "*"
        config["no_char"] = no_char if no_char else "."
        config["outside_char"] = outside_char if outside_char else " "
        config["blur"] = blur if blur else 0.0
        config["method"] = method if method else "dynamic"
        config["surface"] = surface if surface is not None else "all"
        config["is_negative"] = bool(negative)

        if config["is_negative"]:
            config["outside_char"] = "."
            config["no_char"] = " "

        self.is_unicode = bool(is_unicode)

    @staticmethod
    def Render(feature):
        """Convenience function which returns a Render object"""
        if not feature:
            raise MapError("feature may not be None")

        return Render(feature)
