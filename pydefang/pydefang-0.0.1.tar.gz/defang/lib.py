#!/usr/bin/env python3

import re

mappings = [
    ('.', '[.]'),
    (':', '[:]'),
    ('http', 'hxxp'),
    ('ftp', 'fxp'),
]

def defang(url):
    for k, v in mappings:
        url = re.sub(re.escape(k), v, url, flags=re.I)

    return url

def refang(url):
    for k, v in mappings:
        url = re.sub(re.escape(v), k, url, flags=re.I)

    return url
