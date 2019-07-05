
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

from django.core.management import call_command
from .helpers.functions import product_dict
import itertools
import pytest

ALL_SETTINGS = {
    'ASSETS_DEBUG': (True, False),
    'WEBASSETS_OPTIMIZE': (True, False),
    'WEBASSETS_SCRAMBLE_OUT_JS': (True, False)
}

ALL_SETTINGS_PRODUCT = list(product_dict(**ALL_SETTINGS))
USE_BUNDLES = [True, False]

ALL_PARAMS_PRODUCT = itertools.product(ALL_SETTINGS_PRODUCT, USE_BUNDLES)


def _idfn(val):
    if isinstance(val, dict):
        val = str(val)
    return val


@pytest.mark.parametrize('override_settings, make_bundle',
                         ALL_PARAMS_PRODUCT, ids=_idfn)
def test_functional(selenium, live_server, settings,
                    override_settings, make_bundle):
    """Functional test for all possible config values."""
    for key, value in override_settings.items():
        setattr(settings, key, value)
    call_command('assets', 'clean')
    if make_bundle:
        call_command('webassetsrequirejs')

    selenium.open(live_server.url + '/test_functional/')
    selenium.assert_text('Changed', '.test_class')
    selenium.open(live_server.url + '/test_mixin/')
    selenium.assert_text('This is new', '.test_class')
    selenium.open(live_server.url + '/test_other/test_functional/')
    selenium.assert_text('Changed', '.test_class')
    selenium.open(live_server.url + '/test_other/test_mixin/')
    selenium.assert_text('This is new', '.test_class')
    selenium.open(live_server.url + '/test_namespace/test_functional/')
    selenium.assert_text('Changed', '.test_class')
    selenium.open(live_server.url + '/test_namespace/test_mixin/')
    selenium.assert_text('This is new', '.test_class')
