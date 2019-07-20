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
import argparse

try:
    import yappi

    has_benchmark = True
except ImportError:
    has_benchmark = False


from asciimap.maps import DRIVER, SHAPEFILE, parse_undefined_countries, Map
from asciimap import RenderConfig, MapConfig, PrinterConfig, Config

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
        type=CharType(),
        help="Single character marking the edges of the land surface",
    )
    parser.add_argument(
        "--empty",
        "-e",
        type=CharType(),
        help="The character to use for the land surface",
    )
    parser.add_argument(
        "--outside",
        "-o",
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
        type=BlurType(),
        help="Add blur to radius and inflate the surface by double value",
    )
    parser.add_argument(
        "--method",
        "-m",
        choices=["full", "f", "dynamic", "d", "height", "h", "width", "w"],
        help="Change rendering method",
    )
    parser.add_argument(
        "--surface",
        "-s",
        type=SurfaceType(),
        help="Choose a surface by number or 'all'",
    )
    parser.add_argument(
        "--negative", "-n", action="store_true", help="Print the negative"
    )
    parser.add_argument("--unicode", "-u", action="store_true", help="Print in unicode")
    parser.add_argument(
        "--benchmark",
        "-t",
        action="store_true",
        help=(
            "Print execution times of methods with 'yappi' along with the map."
            "'yappi' needs to be installed to show benchmarks."
        ),
    )

    parser.add_argument("--wall", action="store_true", help="Benchmark wall times")

    parser.add_argument("--stats", "-x", action="store_true", help="Print statistics")

    return parser.parse_args(argv)


def print_config(config):
    if isinstance(config, Config):
        print(config.__class__.__name__)
        for k, v in config.config.items():
            print("  {}: {!r}".format(k, v))


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

    if has_benchmark and args.benchmark:
        if args.wall:
            yappi.set_clock_type("wall")

        yappi.start()

    if args.country != "list":
        mapper = Map(
            max_height=args.height,
            max_width=args.width,
            fill_char=args.fill,
            no_char=args.empty,
            outside_char=args.outside,
            blur=args.blur,
            method=args.method,
            surface=args.surface,
            negative=args.negative,
            is_unicode=args.unicode,
        )

        render = mapper.Render(args.country)
        render.render_parallel()

        if args.stats:
            print()
            print_config(MapConfig())
            print_config(PrinterConfig())
            print_config(RenderConfig())

    else:
        process_list_cmd()

    if has_benchmark and args.benchmark:
        yappi.get_func_stats().sort("ttot", "asc").print_all(
            columns={
                0: ("name", 120),
                1: ("ncall", 5),
                2: ("tsub", 8),
                3: ("ttot", 8),
                4: ("tavg", 8),
            }
        )
        yappi.get_thread_stats().print_all()


if __name__ == "__main__":
    main()
