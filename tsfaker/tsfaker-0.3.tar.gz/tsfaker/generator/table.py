import os
from typing import Optional, Dict

import numpy as np
import pandas as pd
from tableschema import Field
from tableschema import Schema

from tsfaker.exceptions import TypeNotImplementedError, ResourceMissing
from tsfaker.generator import column
from tsfaker.generator.foreign_key import ForeignKeyGenerator
from tsfaker.io.schema import INPUT_DESCRIPTOR, OUTPUT_FILE, NAME
from tsfaker.io.utils import smart_open_write, replace_dash


class TableGenerator:
    def __init__(self, schema: Schema, nrows: int, resource_name_to_path_or_schema: Dict[str, str] = None):
        self.schema = schema
        self.input_descriptor = self.schema.descriptor.get(INPUT_DESCRIPTOR)
        self.output_file = self.schema.descriptor.get(OUTPUT_FILE)
        self.name = self.schema.descriptor.get(NAME)
        self.nrows = nrows
        self.resource_name_to_path_or_schema = resource_name_to_path_or_schema or dict()
        self.foreign_key_columns = dict()
        self.foreign_key_columns = self.get_foreign_keys_columns()

    def generate_output_csv(self, dry_run: bool, pretty: bool, overwrite: bool):
        self.resource_name_to_path_or_schema[self.name] = self.output_file

        if self.output_file and self.output_file != '-':
            if os.path.exists(self.output_file) and not overwrite:
                print("WARNING: Output file '{}' already exists. Use '--overwrite' option if you want to.".format(
                    self.output_file))
                return

        print("Data generated from descriptor '{}' will be written on '{}'"
              .format(replace_dash(self.input_descriptor, 'STDIN'), replace_dash(self.output_file, 'STDOUT')))

        if dry_run:
            return

        table_string = self.get_string(pretty)

        with smart_open_write(self.output_file) as f:
            f.write(table_string)

    def get_string(self, pretty, **kwargs) -> Optional[str]:
        df = self.get_dataframe()
        if pretty:
            return df.to_string(**kwargs)
        else:
            index = kwargs.pop('index', False)
            return df.to_csv(index=index, **kwargs)

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(data=self.get_array(), columns=self.schema.field_names)

    def get_array(self) -> np.array:
        columns = []
        for field in self.schema.fields:
            column_array = self.get_column_array(field)
            columns.append(column_array)

        if len(columns) == 1:
            return columns[0]
        else:
            return np.concatenate(columns, axis=1)

    def get_column_array(self, field: Field) -> np.ndarray:
        if field.name in self.foreign_key_columns:
            return self.foreign_key_columns[field.name]

        if 'enum' in field.constraints:
            generator = column.Enum(self.nrows, type=field.type, **field.constraints)
            return generator.get_2d_array()

        field_type = field.type.lower()
        generator_class = column.tstype_to_generator_class.get(field_type, None)
        if generator_class is None:
            raise TypeNotImplementedError("Type '{}' is not implemented yet.".format(field.type))
        generator = generator_class(self.nrows, **field.constraints)
        return generator.get_2d_array()

    def get_foreign_keys_columns(self) -> Dict[str, np.ndarray]:
        foreign_key_columns = {}
        for foreign_key in self.schema.foreign_keys:
            resource_name = foreign_key['reference']['resource']
            if resource_name not in self.resource_name_to_path_or_schema:
                raise ResourceMissing("'{}' resource not found for descriptor '{}'. Use --resources option.".
                                      format(resource_name, self.schema))

            foreign_key['reference']['resource'] = self.resource_name_to_path_or_schema[resource_name]

            foreign_key_generator = ForeignKeyGenerator(self.nrows, **foreign_key)
            for field in foreign_key_generator.fields:
                generator = column.ForeignKey(field, foreign_key_generator)
                foreign_key_columns[field] = generator.get_2d_array()
        return foreign_key_columns
