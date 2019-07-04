from django.utils.six.moves.urllib.parse import (urlparse, parse_qsl, urlunparse, urlencode)

# Using six module to simplify the longer alternative.
# try:
#     # Python 2
#     from urlparse import (urlparse, parse_qsl, urlunparse)
#     from urllib import urlencode
# except ImportError:
#     # Python3
#     from urllib.parse import (urlparse, parse_qsl, urlunparse, urlencode)


def add_version_to_url(url, version):
    url_parts = urlparse(url)
    query = parse_qsl(url_parts.query)
    query.append(('v', version))
    return urlunparse(url_parts[:4] + (urlencode(query),) + url_parts[5:])
