#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

from json_dict import JsonDict

logger = logging.getLogger("plug_in_django")
CONFIG = None

def run(*args):
    try:
        if __name__ == "__main__":
            from plug_in_django import settings
        else:
            from .plug_in_django import settings
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",settings.__name__
        )
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(args)
    except Exception as e:
        logger.exception(e)
        raise e


if __name__ == "__main__":
    run(*sys.argv)
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plug_in_django.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def plug_in(appconfig,config=None):
    #plugin app
    global CONFIG
    if CONFIG is None:
        if config is not None:
           CONFIG = config.getsubdict(preamble=['plug_in_django_server'])
        else:
            CONFIG = JsonDict(os.path.join(os.path.join(os.path.expanduser("~"), ".plug_in_django_server"), "plug_in_django_server_config.json"))

    if config is not None:
        appconfig.config = config.getsubdict(preamble=[appconfig.name])
    else:
        if appconfig.config is None:
            appconfig.config = CONFIG.getsubdict(preamble=[appconfig.name])
    logger.info("plug in {} with the config-path:'{}'".format(appconfig.name,appconfig.config.file))

    apps = CONFIG.get("django_settings", "apps", "additional", default=[])
    apps.append(appconfig.name)
    CONFIG.put("django_settings", "apps", "additional", value=list(set(apps)))


if __name__ == '__main__':
    main()
