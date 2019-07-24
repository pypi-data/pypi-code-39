from typing import List, Callable, Any

import pandas as pd

__all__ = [
    "is_not_none_or_nan",
    "all_values_in_list_are_not_nones_or_nans",
    "all_values_in_list_pass",
    "first_arg_is_type_wrapper",
]

def is_not_none_or_nan(v:object) -> bool:
    return (True if v else False) if not isinstance(v,float) else (not pd.isna(v) if v else False)


def all_values_in_list_are_not_nones_or_nans(l:List) -> bool:
    return all_values_in_list_pass(l, is_not_none_or_nan)


def all_values_in_list_pass(l:List, validity_filter:callable) -> bool:
    return all(map(validity_filter, l))


def first_arg_is_type_wrapper(_callable, tuple_of_types) -> Callable[[Any], bool]:
    return lambda x: x if not isinstance(x, tuple_of_types) else _callable(x)
