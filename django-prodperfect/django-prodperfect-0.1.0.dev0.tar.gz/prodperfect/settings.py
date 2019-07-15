"""
prodperfect.settings
Created by Lemuel Boyce on 2019-07-15
"""
from django.conf import settings as app_settings

DEFAULT_OPTIONS = {
    'ignoreDisabledFormFields': False,
    'recordClicks': True,
    'recordFormSubmits': True,
    'recordInputChanges': True,
    'recordPageViews': True,
    'recordPageUnloads': True,
    'recordScrollState': True
}

_PRODPERFECT = app_settings.PRODPERFECT


class Setting:
    def __init__(self):
        for k, v in _PRODPERFECT.items():
            setattr(self, k, v)
        self._set_defaults()

    def _set_defaults(self):
        if 'REQUEST_TYPE' not in _PRODPERFECT:
            setattr(self, 'REQUEST_TYPE', 'beacon')
        if 'OPTIONS' not in _PRODPERFECT:
            setattr(self, 'OPTIONS', DEFAULT_OPTIONS)
        else:
            user_options = _PRODPERFECT['OPTIONS']
            DEFAULT_OPTIONS.update(user_options)
            setattr(self, 'OPTIONS', DEFAULT_OPTIONS)

    def __getattr__(self, item):
        return getattr(self, item)


settings = Setting()
