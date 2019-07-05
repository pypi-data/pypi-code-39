
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

import inspect
import uuid
import os.path

from ..settings import DJANGO_AUTO_WEBASSETS_Settings
from ..utils.webassetsrjs import make_bundle


class AutoWebassetsJSMixin:
    """View Mixin to specify view-specific javascript bundle."""

    webasset_bundle_name = None
    webasset_js_file = None

    @classmethod
    def _get_complete_classname(cls):
        return '.'.join([inspect.getmodule(cls).__name__, cls.__name__])

    @classmethod
    def _get_webasset_output_name(cls):
        these_settings = DJANGO_AUTO_WEBASSETS_Settings()

        if these_settings.WEBASSETS_SCRAMBLE_OUT_JS:
            return '.'.join([str(uuid.uuid4()), 'js'])
        else:
            return '.'.join([cls._get_complete_classname(), 'js'])

    @classmethod
    def get_webasset_bundle_name(cls):
        """Return the name of the webasset bundle."""
        if cls.webasset_bundle_name:
            return cls.webasset_bundle_name
        else:
            return cls._get_complete_classname()

    @classmethod
    def get_webasset_js_file(cls):
        """Return the filename of the javascript file."""
        if cls.webasset_js_file:
            return cls.webasset_js_file

    @property
    def full_webasset_path(self):
        """Return the full path to the javascript file."""
        these_settings = DJANGO_AUTO_WEBASSETS_Settings()
        js_path = these_settings.WEBASSETS_JS_FOLDER

        if self.get_webasset_js_file():
            return os.path.join(js_path, self.get_webasset_js_file())
        else:
            return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.full_webasset_path:
            make_bundle(self.full_webasset_path,
                        self._get_webasset_output_name(),
                        self.get_webasset_bundle_name())
