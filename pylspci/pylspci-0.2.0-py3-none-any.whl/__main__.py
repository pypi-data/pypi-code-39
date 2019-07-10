#!/usr/bin/env python3
from pylspci.parsers.simple import SimpleParser
import json


if __name__ == '__main__':
    print(json.dumps(
        list(map(lambda d: d._asdict(), SimpleParser().run())),
        indent=4,
        default=vars,
    ))
