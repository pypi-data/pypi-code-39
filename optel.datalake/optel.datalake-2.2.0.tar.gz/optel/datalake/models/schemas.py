from abc import ABC, abstractmethod
from typing import Dict, Iterable, Union

from pyspark.sql import DataFrame


class BaseSchema(ABC):  # pragma: no cover

    @abstractmethod
    def apply(self, df: DataFrame) -> DataFrame:
        ...


class SelectNoRename(BaseSchema):
    def __init__(self, names: Iterable[str]):
        self.names = names

    def apply(self, df: DataFrame) -> DataFrame:
        return df.select(*self.names)


class RenameNoSelect(BaseSchema):
    def __init__(self, name_map: Dict[str, str]):
        self.name_map = name_map

    def apply(self, df: DataFrame) -> DataFrame:
        new_cols = [
            df[old].alias(new) for old, new in self.name_map.items()
        ]

        old_cols = [
            df[old].alias(old)
            for old in set(df.columns).difference(set(self.name_map.keys()))
        ]

        return df.select(*old_cols, *new_cols)


class RenameAndSelect(BaseSchema):
    def __init__(self, name_map: Dict[str, str]):
        self.name_map = name_map

    @classmethod
    def from_nested(cls, nested_name_map: Dict[str, Union[Dict, str]]):
        def resolve_nested_schema(schema: Dict, name=None) -> Dict[str, str]:
            new_schema = {}
            for key, value in schema.items():
                new_name = name + "." + key if name else key

                if isinstance(value, Dict):
                    sub_schema = resolve_nested_schema(value, name=new_name)
                    new_schema.update(sub_schema)
                else:
                    new_schema[new_name] = value

            return new_schema

        return cls(resolve_nested_schema(nested_name_map))

    def apply(self, df: DataFrame) -> DataFrame:
        new_cols = [
            df[old].alias(new) for old, new in self.name_map.items()
        ]
        return df.select(new_cols)
