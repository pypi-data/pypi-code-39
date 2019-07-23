from typing import Dict, Tuple, Union, Any


def search_in_tuple(key, value, t: Tuple) -> Union[Dict[str, Any], None]:
    for e in t:
        if type(e) is dict and key in e and e[key] == value:
            return e
    return None



