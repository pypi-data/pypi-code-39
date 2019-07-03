#!/usr/bin/env python

import os
import sys
from django.test.runner import DiscoverRunner

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_settings')
parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, parent)


def runtests():
    return DiscoverRunner().run_tests([
        # 'country_dialcode.CountryDialcodeAdminView',
        'tests.CountryDialcodeModel',
    ], verbosity=1, interactive=True)


if __name__ == '__main__':
    if runtests():
        sys.exit(1)
