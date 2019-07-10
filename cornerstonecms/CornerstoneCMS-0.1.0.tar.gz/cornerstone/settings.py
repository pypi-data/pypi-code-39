from serpent import dumps, loads
from cornerstone.models import Setting, db


def has_setting(key):
    """
    Check if a setting exists

    :param key: The key of the setting
    """
    return Setting.query.get(key) is not None


def add_setting(title, key, type_, group='core', allowed_values=None):
    """
    Add a setting

    :param title: The visible title of the setting
    :param key: The unique key used to look up the setting in the database
    :param type_: The type of this setting. Can be one of "bool", "int", "str".
    :param allowed_values: Restrict values to only those in this list (renders as a dropdown)
    """
    setting = Setting(title=title, key=key, type=type_, group=group, allowed_values=dumps(allowed_values))
    db.session.add(setting)
    db.session.commit()
    return setting


def get_all_settings():
    """
    Get all the settings
    """
    grouped_settings = {}
    settings = Setting.query.all()
    for setting in settings:
        setting.value = loads(setting.value if isinstance(setting.value, bytes) else setting.value.encode('utf8'))
        setting.allowed_values = loads(setting.allowed_values if isinstance(setting.allowed_values, bytes)
                                       else setting.allowed_values.encode('utf8'))
        try:
            grouped_settings[setting.group].append(setting)
        except KeyError:
            grouped_settings[setting.group] = [setting]
    return grouped_settings


def get_setting(key, default=None):
    """
    Get a setting
    """
    setting = Setting.query.get(key)
    if not setting:
        return default
    return loads(setting.value if isinstance(setting.value, bytes) else setting.value.encode('utf8'))


def save_setting(key, value):
    setting = Setting.query.get(key)
    if not setting:
        raise Exception('Cannot save setting without running add_setting: {}'.format(key))
    setting.value = dumps(value)
    db.session.add(setting)
    db.session.commit()
