from django.conf import settings

def setting(name, default):
    @property
    def fn(self):
        return getattr(settings, name, default)
    return fn

class AppSettings(object):
    # Required
    SUBDOMAINS = setting('SUBDOMAINS', ())
    DEFAULT_SUBDOMAIN = setting('DEFAULT_SUBDOMAIN', None)


app_settings = AppSettings()
