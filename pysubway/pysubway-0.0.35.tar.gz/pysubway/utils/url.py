from collections import OrderedDict
from typing import Any
from typing import Dict
from urllib import parse


def urlencode(data: Dict[str, Any], safe: bool = True, sorted_by_ascii: bool = False) -> str:
    if safe:
        return parse.urlencode(data)
    else:
        may_sorted = data.copy()
        if sorted_by_ascii:
            may_sorted = OrderedDict()
            for k in sorted(data):
                may_sorted[k] = data[k]
        return "&".join((f'{k}={v}' for k, v in may_sorted.items()))


if __name__ == '__main__':
    s = urlencode({'a': 1, '2': 3}, sorted_by_ascii=True)
    print(s)
