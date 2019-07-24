from django.apps import AppConfig

from .finder import find_datahook_commands


class DataHooksConfig(AppConfig):
    name = "django_datahooks"

    def ready(self):
        find_datahook_commands()
