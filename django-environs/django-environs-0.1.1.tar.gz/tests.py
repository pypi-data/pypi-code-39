"""
This file is meant to be copied into project created with `django-environs startproject`
and run with env variables from tox.ini
"""
import os
from pathlib import Path

from django.conf import settings
from django.test import TestCase

ENV_SETTINGS = (
    ("BASE_DIR", Path("/")),
    ("SECRET_KEY", "secret"),
    ("DEBUG", False),
    ("ALLOWED_HOSTS", ["test", "testserver"]),
    ("LANGUAGE_CODE", "en-gb"),
    ("TIME_ZONE", "Africa/Abidjan"),
    ("USE_I18N", False),
    ("USE_L10N", False),
    ("USE_TZ", False),
    ("STATIC_URL", "/test/"),
)


class SettingsTestCase(TestCase):
    def test_settings(self):
        for name, value in ENV_SETTINGS:
            self.assertEqual(getattr(settings, name), value)
