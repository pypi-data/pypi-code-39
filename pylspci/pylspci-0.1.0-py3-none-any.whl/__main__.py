#!/usr/bin/env python3
from pylspci import lspci
import json


if __name__ == '__main__':
    print(json.dumps(
        list(map(lambda d: d._asdict(), lspci())),
        indent=4,
        default=vars,
    ))
