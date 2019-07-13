import json
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
    setting = Setting(title=title, key=key, type=type_, group=group, allowed_values=json.dumps(allowed_values))
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
        setting.value = json.loads(setting.value)
        setting.allowed_values = json.loads(setting.allowed_values)
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
    return json.loads(setting.value)


def save_setting(key, value):
    setting = Setting.query.get(key)
    if not setting:
        raise Exception('Cannot save setting without running add_setting: {}'.format(key))
    setting.value = json.dumps(value)
    db.session.add(setting)
    db.session.commit()
