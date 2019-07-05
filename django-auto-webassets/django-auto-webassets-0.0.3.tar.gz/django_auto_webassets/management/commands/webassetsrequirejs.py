
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

import importlib
import logging
import os.path
import sys

from django.core.management.base import BaseCommand, CommandError
from django.urls import URLPattern, URLResolver, get_resolver
from django.conf import settings
from django_assets.env import get_env, reset as env_reset
from webassets.script import (CommandError as AssetCommandError,
                              GenericArgparseImplementation)

from ...utils.webassetsrjs import WebassetsRjsLoader
from ...views.mixins import AutoWebassetsJSMixin


class Command(BaseCommand):
    """Implement the webassetsrequirejs command."""

    help = 'Build assets defined by the AutoWebassetsJSMixin mixin.'
    requires_system_checks = True

    def handle(self, *args, **options):
        """
        Build all assets defined by django_auto_webassets.

        Parameters
        ----------
        args : list
            Not used
        options : dict
            Not used

        """
        log = logging.getLogger('th_utils-assets')
        log.setLevel({0: logging.WARNING,
                      1: logging.INFO,
                      2: logging.DEBUG}[int(options.get('verbosity', 1))])
        log.addHandler(logging.StreamHandler())

        env_reset()
        dummy = get_resolver().url_patterns
        view_class_names = self._parse_urls(dummy).keys()
        for cur_class_name in view_class_names:
            (cur_package, cur_module) = cur_class_name.rsplit('.', 1)
            cur_class = getattr(importlib.import_module(cur_package),
                                cur_module)
            if issubclass(cur_class, AutoWebassetsJSMixin):
                cur_class()

        get_env().add(*[b for b in self._load_from_templates()
                        if not b.is_container])

        prog = "%s assets" % os.path.basename(sys.argv[0])
        impl = GenericArgparseImplementation(
            env=get_env(), log=log, no_global_options=True, prog=prog)
        try:
            # The webassets script runner may either return None on success (so
            # map that to zero) or a return code on build failure (so raise
            # a Django CommandError exception when that happens)
            if settings.ASSETS_DEBUG:
                return

            impl.run_with_argv(('clean',)) or 0
            retval = impl.run_with_argv(('build',)) or 0
            if retval != 0:
                raise CommandError('The webassets build script exited with '
                                   'a non-zero exit code (%d).' % retval)
        except AssetCommandError as e:
            raise CommandError(e)

    def _load_from_templates(self):
        # Using the Django loader
        bundles = WebassetsRjsLoader().load_bundles()

        return bundles

    def _parse_urls(self, patterns):
        all_patterns = {}
        if isinstance(patterns, list):
            for cur_pattern in patterns:
                all_patterns.update(self._parse_urls(cur_pattern))

        if isinstance(patterns, URLResolver):
            cur_namespace = patterns.namespace
            all_items = {}
            for cur_pattern in patterns.url_patterns:
                all_items.update(self._parse_urls(cur_pattern))

            for cur_key, cur_item in all_items.items():
                if not cur_namespace:
                    all_items[cur_key] = '%s' % (cur_item,)
                else:
                    all_items[cur_key] = '%s:%s' % (cur_namespace, cur_item)

            return all_items

        if isinstance(patterns, URLPattern):
            return {patterns.lookup_str: patterns.name}

        return all_patterns
