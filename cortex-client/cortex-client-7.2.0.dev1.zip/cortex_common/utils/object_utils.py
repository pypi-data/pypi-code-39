"""
Copyright 2019 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import copy
import itertools
import uuid
from collections import defaultdict
from enum import Enum
from typing import List, Optional, Any, Tuple, Callable, Union, Mapping, Iterable, Set

import pandas as pd
import pydash

__all__ = [
    "unique_id",
    "head",
    "tail",
    "flatten_list_recursively",
    "flatmap",
    "append_to_list",
    "partition_list",
    "dervie_set_by_element_id",
    "filter_empty_records",
    "search_for_values_in_list",
    "nan_to_none",
    "tuples_with_nans_to_tuples_with_nones",
    "split_list_of_tuples",
    "merge_dicts",
    "assign_to_dict",
    "map_object",
    "nest_values_under",
    "append_key_to_values_as",
    "drop_from_dict",
    "join_inner_arrays",
    "invert_dict_lookup",
    "pluck",
    "group_by_key",
    "group_objects_by",
    "reverse_index_dictionary",
    "map_key",
    "merge_unique_objects_on",
    "convert_to_string_dict",
    "negate_dict_of_numbers",
    "merge_enum_values",
    "EnumWithCamelCasedNamesAsDefaultValue",
    "EnumWithNamesAsDefaultValue",
]


def unique_id() -> str:
    """
    Returns a unique id.
    """
    return str(uuid.uuid4())


# ------------------------------------------- List Utils ------------------------------------------------


def head(l:Optional[List[Any]]) -> Optional[Any]:
    """
    Gets the head of a list if its not empty.
    If its empty, None is returned ...
    :param l:
    :return:
    """
    if l is None:
        return None
    list_with_first_elem = l[0:1]
    return list_with_first_elem[0] if list_with_first_elem else None


def tail(l:List) -> List:
    return None if l is None else l[1:]


def flatten_list_recursively(l: Union[List[Any], Any], remove_empty_lists=False):
    if l is None:
        return []
    if not isinstance(l, list):
        return [l]
    # THIS DOES WEIRD STUFF WITH TUPLES!
    return list(itertools.chain(*[flatten_list_recursively(x) for x in l if (not remove_empty_lists or x)]))



def flatmap(listToItterate: List, inputToAppendTo: List, function: Callable) -> List :
    if not listToItterate:
        return []
    head = listToItterate[0]
    tail = listToItterate[1:]
    return flatmap(tail, function(inputToAppendTo, head), function)


def append_to_list(l:List, thing_to_append:Optional[object]) -> List:
    return l + [thing_to_append] if thing_to_append else l


def partition_list(l:List, partitions:int) -> List[List]:
    assert partitions >= 1, "Partitions must be >= 1"
    size_of_each_parition = int(len(l) / partitions)
    partitions = zip([x for x in range(0, partitions)], [x for x in range(1, partitions)] + [None])
    return [
        l[start*size_of_each_parition:None if end is None else end*size_of_each_parition]
        for start, end in partitions
    ]


def dervie_set_by_element_id(l:List[Any], identifier:Callable[[Any], str]=lambda x: x) -> Set[Any]:
    # from itertools import combinations
    # combinations(l, 2)
    return set({identifier(x): x for x in l}.values())


def filter_empty_records(l:List) -> List:
    return [x for x in l if x]


def search_for_values_in_list(list_to_search:Iterable, search_query:callable) -> List:
    return list(filter(search_query, list_to_search))


# ------------------------------------------- Tuple Utils ------------------------------------------------


def nan_to_none(value:Any) -> Optional[Any]:
    """
    Turns NaNs to Nones ...
    :return: 
    """
    return None if isinstance(value, float) and pd.isna(value) else value


def tuples_with_nans_to_tuples_with_nones(iter:List[Tuple[Any, ...]]) -> List[Tuple[Optional[Any], ...]]:
    """
    Replaces NaNs within a tuple into Nones.

    # ... I only want to check for NaNs on primitives... and replace them with None ... not Lists ...
        # Unfortunately python has no way of saying "isPrimitive"
        # Luckily, NaNs are floats ...!

    :param iter:
    :return:
    """
    return [
        tuple([
            nan_to_none(x) for x in tup
        ])
        for tup in iter
    ]


def split_list_of_tuples(l:List[Tuple[Any, ...]]) -> Optional[Tuple[List[Any], ...]]:
    """
    NOTE: No python way of specifying that the return type ... the number of List[Any] in it depends on the size of the tuple passed in ...
    :param l:
    :return:
    """
    if not l:
        return None
    lengths_of_each_tuple = list(map(lambda x: len(list(x)), l))
    # We know there is at least one item ...
    all_tuples_same_length =  all(map(
        lambda x: x == lengths_of_each_tuple[0],
        lengths_of_each_tuple
    ))
    assert all_tuples_same_length, "All tuples must be of the same length: {}".format(lengths_of_each_tuple[0])
    return tuple(*[[tupe[i] for tupe in l] for i in range(0, lengths_of_each_tuple[0])])


# ------------------------------------------- Object Utils ------------------------------------------------


def merge_dicts(a:dict, b:dict) -> dict:
    c = copy.deepcopy(a)
    c.update(b)
    return c


def assign_to_dict(dictionary:dict, key:str, value:object) -> dict:
    return merge_dicts(dictionary, {key: value})


def map_object(object:Optional[Any], method:Callable[[Any], Any], default:Optional[Any]=None) -> Any:
    return method(object) if object is not None else default


def nest_values_under(d:dict, under:str) -> dict:
    return {k: {under: v} for k, v in d.items()}


def append_key_to_values_as(d:dict, key_title:str) -> List[dict]:
    return [pydash.merge(value, {key_title: key}) for key, value in d.items()]


def _drop_from_dict(d: dict, skip: List[object]) -> dict:
    if d is None:
        d = None
    if isinstance(d, list):
        return [drop_from_dict(e, skip) for e in d]
    if isinstance(d, dict):
        return {
            k: drop_from_dict(v, skip) for k, v in d.items() if k not in skip
        }
    return d


def drop_from_dict(d: dict, skip: List[object]) -> dict:
    return _drop_from_dict(d, skip)


def join_inner_arrays(_dict:dict, caster=lambda x: x) -> dict:
    return {
        k: ",".join(map(caster, v)) if isinstance(v, list) else v
        for (k, v) in _dict.items()
    }

def invert_dict_lookup(d:dict) -> dict:
    return {v: k for k, v in d.items()}


def pluck(path, d, default={}):
    split_path = [x for x in path.split('.') if x]
    if len(split_path) > 0:
        return pluck('.'.join(split_path[1:]), d.get(split_path[0], default))
    return d


def group_by_key(l:List[Any], key:Callable[[Any], str]) -> Mapping[str, List[Any]]:
    key_deriver = key if callable(key) else lambda x: x[key]
    returnVal = defaultdict(list)
    for x in l:
        returnVal[key_deriver(x)].append(x)
    return returnVal


def group_objects_by(l:List[Any], group_by:Callable[[Any], str]) -> Mapping[str, List[Any]]:
    unique_groups = set(map(group_by, l))
    return {
        g: list(filter(lambda x: group_by(x) == g, l))
        for g in unique_groups
    }


def reverse_index_dictionary(d:dict) -> dict:
    new_keys = list(set(flatten_list_recursively(list(d.values()))))
    return {
        new_key: [old_key for old_key in list(d.keys()) if new_key in d[old_key]] for new_key in new_keys
    }


def map_key(o:dict, key:str, mapper:Callable) -> dict:
    return pydash.set_(o, key, mapper(pydash.get(o, key)))


def merge_unique_objects_on(objects: List[Any], identifier:Callable, reducer:Callable=head) -> List[Any]:
    groups = group_by_key(objects, identifier)
    return list({
        groupId: reducer(values) for groupId, values in groups.items()
    }.values())


def convert_to_string_dict(d:dict) -> dict:
    return {str(k): str(v) for k, v in d.items()}


def negate_dict_of_numbers(d:dict) -> dict:
    return {
        k: -1 * v for k, v in d.items()
    }

# ------------------------------------------ ENUM Utils ------------------------------------------


class EnumWithCamelCasedNamesAsDefaultValue(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return pydash.strings.camel_case(name)


class EnumWithNamesAsDefaultValue(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


def merge_enum_values(values:List[Enum], merger:Callable[[list], object]=lambda values: ".".join(values)) -> object:
    return merger(list(map(lambda x: x.value, values)))
