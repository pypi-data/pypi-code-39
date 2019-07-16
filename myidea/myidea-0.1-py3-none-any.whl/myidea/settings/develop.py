from .base import * # NOQA

DEBUG = False

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': 'myidea_db',
      'USER': 'root',
      'PASSWORD': 'iso*help',
      'HOST': '127.0.0.1',
      'PORT': '3306',
      'CONN_MAX_AGE': 5 * 60,
      'OPTIONS': {'charset': 'utf8mb4'},
    },
}

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# DEBUG_TOOLBAR_PANELS = [
#     'djdt_flamegraph.FlamegraphPanel',
# ]

INTERNAL_IPS = ['127.0.0.1']