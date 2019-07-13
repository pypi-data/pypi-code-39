# test ietf test vectors

import re
from io import StringIO
from precis_i18n import get_profile
from precis_i18n.profile import Profile

_DELIM_REGEX = re.compile(r'\s*|\s*')

_BASIC = '''
                      | 65cc81cc9f | c3a9cc9f |     |
'''

_CONTEXT_RULE_1 = '''
   | e2808c                       |                              | ctx |
   | e2808c61                     |                              | ctx |
   | 61e2808c                     |                              | ctx |
   | e2808cd8a7                   |                              | ctx |
   | d8ace2808c                   |                              | ctx |
   | d890e2808cd890d8a7           |                              | ctx |
   | d8acd890e2808cd890           |                              | ctx |
   | d8ace2808cd8a7               | d8ace2808cd8a7               |     |
   | d8acd890e2808cd890d8a7       | d8acd890e2808cd890d8a7       |     |
   | d8acd890d890e2808cd890d890d8 | d8acd890d890e2808cd890d890d8 |     |
   | a7                           | a7                           |     |
   | d8acd890e2808cd8a7           | d8acd890e2808cd8a7           |     |
   | d8ace2808cd890d8a7           | d8ace2808cd890d8a7           |     |
   | eaa1b2e2808cd8ac             | eaa1b2e2808cd8ac             |     |
   | eaa1b2d890e2808cd890d8ac     | eaa1b2d890e2808cd890d8ac     |     |
   | eaa1b2d890d890e2808cd890d890 | eaa1b2d890d890e2808cd890d890 |     |
   | d8ac                         | d8ac                         |     |
   | eaa1b2d890e2808cd8ac         | eaa1b2d890e2808cd8ac         |     |
   | eaa1b2e2808cd890d8ac         | eaa1b2e2808cd890d8ac         |     |
   | e0a98de2808c                 | e0a98de2808c                 |     |
   | eaa1b2e0a98de2808c           | eaa1b2e0a98de2808c           |     |
   | eaa1b2e0a98dd890e2808c       |                              | ctx |
   | eaa1b2e0a98dd890e2808c       |                              | ctx |
   | e0ab8de2808c                 | e0ab8de2808c                 |     |
   | eaa1b2e0ab8de2808c           | eaa1b2e0ab8de2808c           |     |
   | eaa1b2e0ab8dd890e2808c       |                              | ctx |
   | eaa1b2e0ab8dd890e2808c       |                              | ctx |
   | eaa1b2e0ab8de2808cd8ac       | eaa1b2e0ab8de2808cd8ac       |     |
   | eaa1b2e2808ce0ab8dd8ac       | eaa1b2e2808ce0ab8dd8ac       |     |
'''

def _parse_rows(text):
    for line in StringIO(text):
        line = line.strip()
        if not line:
            continue
        row = [s.strip() for s in line.split('|')[1:-1]]
        yield row


class FreeForm(Profile):
    def __init__(self, ucd, name, casemap=None):
        super().__init__(FreeFormClass(ucd), name, casemap)


def _test_row(input, output, precis_codec):
    profile = get_profile(precis_codec)
    input = bytes.fromhex(row[0]).decode('utf-8')
    output = bytes.fromhex(row[1]).decode('utf-8')

    result = profile.enforce(input)
    print(result, output)
    assert result == output


for row in _parse_rows(_BASIC):
    _test_row(row[0], row[1], 'FreeformClass')
