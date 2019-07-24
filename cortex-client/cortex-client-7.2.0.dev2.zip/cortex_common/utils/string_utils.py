import itertools
import re
from typing import List

from cortex_common.utils.object_utils import head, tail

__all__ = [
    "split_camel_case",
    "split_string_into_parts",
]


def split_camel_case(string:str) -> List[str]:
    """
    Turns "CLevelChangeInsights" into ['C', 'Level', 'Change ', 'Insights']
    :param string:
    :return:
    """
    l = [x for x in re.split(r'([A-Z])', string) if x]
    if not l:
        return l
    if not tail(l):
        return l

    upper_case_chrs = list(map(chr, range(ord("A"), ord("Z") + 1)))
    lower_case_chrs = list(map(chr, range(ord("a"), ord("z") + 1)))
    if head(l) in upper_case_chrs and head(head(tail(l))) in upper_case_chrs:
        return [head(l)] + split_camel_case("".join(tail(l)))
    elif head(l) in upper_case_chrs and head(head(tail(l))) in lower_case_chrs:
        return ["{}{}".format(head(l), head(tail(l)))] + split_camel_case("".join(tail(tail(l))))
    else:
        return [head(l), head(tail(l))] + split_camel_case("".join(tail(tail(l))))


def split_string_into_parts(string:str, num_of_parts:int) -> List:
    l = len(string)
    splittings = list(zip(
        [0] + list(map(lambda x: int(x * l / num_of_parts), range(1, num_of_parts))),
        list(map(lambda x: int(x * l / num_of_parts), range(1, num_of_parts))) + [None]
    ))
    return [
        "".join(list(itertools.islice(string, x, y))) for x, y in splittings
    ]
