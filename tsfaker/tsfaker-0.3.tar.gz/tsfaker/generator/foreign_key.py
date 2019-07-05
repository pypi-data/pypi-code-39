import os
from typing import List, Union, Dict

import numpy as np
from tableschema import Table, Schema

from tsfaker.exceptions import ResourceMissing


class ForeignKeyGenerator:
    def __init__(self, nrows: int, fields: Union[str, List[str]], reference: Dict, *args, **kwargs):
        self.nrows = nrows
        self.fields = self.to_list(fields)
        self.resource_path = reference['resource']
        self.resource_fields = self.to_list(reference['fields'])

        self.foreign_key_values = self.read_foreign_key_values()
        self.array_2d = self.random_choice_2d(self.foreign_key_values, self.nrows)

    @staticmethod
    def to_list(str_or_list: Union[str, List[str]]) -> List[str]:
        return (str_or_list,) if isinstance(str_or_list, str) else str_or_list

    def read_foreign_key_values(self) -> np.ndarray:
        if not os.path.exists(self.resource_path):
            raise ResourceMissing("Resource csv file is missing '{}'. This should not happen. "
                                  "This file either existed when tsfaker was started, "
                                  "or it should have been generated before.".format(self.resource_path))
        table = Table(self.resource_path)
        foreign_key_values = []
        for keyed_row in table.iter(keyed=True):
            foreign_key_values.append([keyed_row[key] for key in self.resource_fields])
        return np.array(foreign_key_values)

    @staticmethod
    def random_choice_2d(array: np.ndarray, size: int) -> np.ndarray:
        random_indices = np.random.randint(array.shape[0], size=size)
        return array[random_indices, :]

    def get_column(self, field) -> np.ndarray:
        field_index = self.fields.index(field)
        return self.array_2d[:, field_index]


def replace_foreign_key_by_enum(schema: Schema, ressource_name_to_path: Dict[str, str]) -> None:
    for foreign_key in schema.foreign_keys():
        ressource_path = ressource_name_to_path[foreign_key['ressource']]
        # foreign_key_values = read_foreign_key_values(ressource_path, foreign_key[])
    pass
