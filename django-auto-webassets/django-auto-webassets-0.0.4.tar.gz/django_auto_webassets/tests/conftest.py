
# django-auto-webassets - Automatic webassets javascript bundles for django
# Copyright (C) 2019 Thomas Hartmann <thomas.hartmann@th-ht.de>
#
# This file is part of django-auto-webassets.
#
# django-auto-webassets is free software: you can redistribute it and/or
# modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-auto-webassets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-auto-webassets.  If not, see
# <http://www.gnu.org/licenses/>.

import pytest
from django.core.management import call_command
from django.conf import settings
import subprocess
import shutil
import os
import seleniumbase


@pytest.fixture(scope='session', autouse=True)
def init_tests(tmpdir_factory):
    """General init fixture for all pytests."""
    settings.STATIC_ROOT = str(tmpdir_factory.mktemp('static'))
    node_modules_dir = str(tmpdir_factory.mktemp('node_modules'))
    shutil.copy(os.path.join(settings.BASE_DIR,
                             'django_auto_webassets/tests/package.json'),
                os.path.join(node_modules_dir))
    subprocess.run(['npm', 'update'], cwd=node_modules_dir)
    settings.STATICFILES_DIRS.append(
        os.path.join(node_modules_dir, 'node_modules'))
    settings.WEBASSETS_R_JS = os.path.join(
        node_modules_dir, 'node_modules', '.bin', 'r.js')
    call_command('collectstatic', interactive=False)
    yield


@pytest.fixture(scope='module')
def selenium():
    """Fixture returning a seleniumbase."""
    this_sel = seleniumbase.BaseCase('__init__')
    this_sel.setUp()
    yield this_sel
    this_sel.tearDown()
