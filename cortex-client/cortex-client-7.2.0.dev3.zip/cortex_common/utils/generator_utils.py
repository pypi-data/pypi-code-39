import itertools
import re
from typing import Callable, Any, List, Optional

from .object_utils import assign_to_dict
from .string_utils import split_string_into_parts

ToYeild = Any

__all__ = [
    "get_until",
    "get_unique_cortex_objects",
    "label_generator",
]

def get_until(
        yielder:Callable[[], Any],
        appender:Callable[[Any, ToYeild], Any],
        ignore_condition:Callable[[Any, ToYeild], bool],
        stop_condition:Callable[[ToYeild], bool],
        to_yield:List) -> ToYeild:
    ignored = 0
    returnVal = to_yield
    while not stop_condition(returnVal):
        next_item = yielder()
        if ignore_condition(next_item, returnVal):
            ignored += 1
        else:
            returnVal = appender(next_item, returnVal)
    # print(ignored, len(returnVal))
    return returnVal


def get_unique_cortex_objects(yielder, limit:int) -> List:
    return list(
        get_until(
            yielder,
            appender=lambda obj, dictionary: assign_to_dict(dictionary, obj["id"], obj),
            ignore_condition=lambda obj, dictionary: obj["id"] in dictionary,
            stop_condition=lambda dictionary: len(dictionary) >= limit,
            to_yield={}
        ).values()
    )


def label_generator(word:str, used_labels:List[str], label_length:int=3) -> Optional[str]:
    """
    Right now, labels are only three letters long!
    :param word:
    :param used_labels:
    :return:
    """
    words = re.split(r'[^a-zA-Z0-9]', word)
    if len(words) != label_length:
        word = "".join(words)
        words = split_string_into_parts(word, label_length)
    try:
        return "".join(next(filter(lambda x: "".join(x).upper() not in used_labels, itertools.product(*words)))).upper()
    except StopIteration as e:
        print("Failed to generate label")
        return None

    # longest_word = max(map(len, words))
    # extended_words = [
    #     list(word) + ['']*(longest_word-len(word)) for word in words
    # ]
    # list(itertools.combinations((itertools.chain(*list(zip(*extended_words)))), 3))

