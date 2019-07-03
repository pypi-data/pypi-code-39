#!/usr/bin/env python3

"""
Generate a resource file template from a Table Schema JSON file.
"""

import argparse
import locale
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import iso8601
import tableschema
from tableschema import Schema

XLSX_FORMAT = "xlsx"
FORMATS = [XLSX_FORMAT]


def generate_xlsx(schema: Schema, output_file: Path, created_date: Optional[datetime] = None,
                  modified_date: Optional[datetime] = None):
    import xlsxwriter
    with xlsxwriter.Workbook(str(output_file)) as workbook:
        properties = {}
        if created_date:
            properties['created'] = created_date
        if modified_date:
            properties['modified'] = modified_date
        if properties:
            workbook.set_properties(properties)
        worksheet = workbook.add_worksheet()
        for index, field in enumerate(schema.fields):
            worksheet.write(0, index, field.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('table_schema_json', help='path or URL of Table Schema JSON file')
    parser.add_argument('output', type=Path, help='path of output file')
    parser.add_argument('-f', '--format', default=XLSX_FORMAT, help='format of output file')
    parser.add_argument('--created-date', type=valid_iso_datetime,
                        help='force created date metadata (format: iso 8601, example: "2019-07-02T22:55:56Z")')
    parser.add_argument('--modified-date', type=valid_iso_datetime,
                        help='force modified date metadata (format: iso 8601, example: "2019-07-02T22:55:56Z")')
    args = parser.parse_args()

    if args.format not in FORMATS:
        parser.error("Format \"{}\" not supported. Supported formats: {}".format(
            args.format, ", ".join(map(lambda s: '"{}"'.format(s), FORMATS))))

    try:
        schema = Schema(args.table_schema_json)
    except tableschema.exceptions.LoadError:
        parser.error("Can't load schema from \"{}\"".format(args.table_schema_json))

    if args.format == XLSX_FORMAT:
        generate_xlsx(schema=schema, output_file=args.output,
                      created_date=args.created_date, modified_date=args.modified_date)


def valid_iso_datetime(s):
    try:
        return iso8601.parse_date(s)
    except iso8601.ParseError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    sys.exit(main())
