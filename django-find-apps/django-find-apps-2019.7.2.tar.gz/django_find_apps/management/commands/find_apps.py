from django.core.management.base import BaseCommand
from django_find_apps import find_apps

"""
python manage.py find_apps > settings/apps.txt

settings:
PROJECT_APPS = open("settings/apps.txt").read().splitlines()
INSTALLED_APPS = PROJECT_APPS + [
    "django_find_apps"
]
"""

class Command(BaseCommand):
    help = 'print list of project apps'

    def handle(self, *args, **options):
        apps = find_apps('.')
        if find_apps:
            print("\n".join(apps))
