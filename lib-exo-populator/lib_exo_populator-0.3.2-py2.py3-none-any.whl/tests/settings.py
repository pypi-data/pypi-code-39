# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "!wp4(eoxkjo%70^83j4b@(e*s_*%&&s@^6^3hl+)$z=w6y4-km"

if 'TRAVIS' in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "travis_ci_test",
            "USER": "postgres",
            "PASSWORD": "",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "local_ci_test",
            "USER": "exolever",
            "PASSWORD": "exolever",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "populate",
]

SITE_ID = 1

MIDDLEWARE = ()
