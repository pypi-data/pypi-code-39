from django.conf import settings
from django.utils.module_loading import import_string
from django.test.signals import setting_changed


DEFAULT_SETTINGS = {
    'ATTRIBUTE_NAME': '_requestlog',
    'ENTRY_CLASS': 'requestlogs.entries.RequestLogEntry',
    'STORAGE_CLASS': 'requestlogs.storages.LoggingStorage',
    'SECRETS': ['password', 'token'],
}


def populate_settings(_settings):
    for k, v in DEFAULT_SETTINGS.items():
        _settings[k] = v
    for k, v in getattr(settings, 'REQUESTLOGS', {}).items():
        _settings[k] = v
    _settings['ENTRY_CLASS'] = import_string(_settings['ENTRY_CLASS'])
    _settings['STORAGE_CLASS'] = import_string(_settings['STORAGE_CLASS'])


SETTINGS = {}
populate_settings(SETTINGS)


def get_requestlog_entry(request=None, view_func=None):
    try:
        entry = getattr(request, SETTINGS['ATTRIBUTE_NAME'])
        # `existing` should be something else than `None`
        assert entry
        return entry
    except AttributeError:
        pass

    entry = SETTINGS['ENTRY_CLASS'](request, view_func)
    setattr(request, SETTINGS['ATTRIBUTE_NAME'], entry)
    return entry


def reload_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'REQUESTLOGS':
        global SETTINGS
        SETTINGS.clear()
        populate_settings(SETTINGS)


setting_changed.connect(reload_settings)
