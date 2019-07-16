import contextlib

from django.urls import set_urlconf, NoReverseMatch
from django.utils.six.moves.urllib.parse import urlsplit

from .app_settings import app_settings

@contextlib.contextmanager
def set_urlconf_from_host(host):
    # Find best match, falling back to DEFAULT_SUBDOMAIN
    for subdomain in app_settings.SUBDOMAINS:
        match = subdomain['_regex'].match(host)
        if match:
            kwargs = match.groupdict()
            break
    else:
        kwargs = {}
        subdomain = get_subdomain(app_settings.DEFAULT_SUBDOMAIN)

    set_urlconf(subdomain['urlconf'])

    try:
        yield subdomain, kwargs
    finally:
        set_urlconf(None)

def get_subdomain(name):
    try:
        return {x['name']: x for x in app_settings.SUBDOMAINS}[name]
    except KeyError:
        raise NoReverseMatch("No subdomain called %s exists" % name)

def noop(*args, **kwargs):
    return
