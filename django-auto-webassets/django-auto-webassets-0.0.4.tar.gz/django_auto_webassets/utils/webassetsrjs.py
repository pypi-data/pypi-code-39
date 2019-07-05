
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

import os.path
import uuid

import django.contrib.staticfiles.finders
import django.template
import django.template.library
import django_assets
import django_assets.loaders
import webassets.env
from django.conf import settings

from ..settings import DJANGO_AUTO_WEBASSETS_Settings


def make_bundle(full_webasset_path, output_name, bundle_name, register=True):
    """Make bundle for a javascript file and register it.

    Parameters
    ----------
    full_webasset_path: str
        Full path to the javascript file.
    output_name: str
        Name of the output js file.
    bundle_name: str
        Name of the bundle
    register: bool
        Register the bundle with webassets.

    Returns
    -------
    django_assets.Bundle: The generated bundle.

    """
    these_settings = DJANGO_AUTO_WEBASSETS_Settings()

    if settings.DEBUG or not these_settings.WEBASSETS_OPTIMIZE:
        filters = None
    else:
        filters = 'requirejs'
        os.environ['REQUIREJS_BIN'] = \
            os.path.join(settings.BASE_DIR, these_settings.WEBASSETS_R_JS)
        os.environ[
            'REQUIREJS_CONFIG'] = django.contrib.staticfiles.finders.find(
            these_settings.WEBASSETS_PATH_TO_REQUIREJS_CFG)

    try:
        my_bundle = django_assets.Bundle(
            these_settings.WEBASSETS_PATH_TO_REQUIREJS,
            these_settings.WEBASSETS_PATH_TO_REQUIREJS_CFG, full_webasset_path,
            output=output_name, filters=filters)
        if register:
            django_assets.register(bundle_name, my_bundle)

        return my_bundle
    except webassets.env.RegisterError:
        pass


class WebassetsRjsLoader(django_assets.loaders.DjangoLoader):
    """Webassets Loader for the generated bundles."""

    def _parse(self, filename, contents):
        try:
            t = django.template.Template(str(contents, 'utf-8'))
        except django.template.TemplateSyntaxError:
            pass
        else:
            result = []

            def _recurse_node(node):
                # depending on whether the template tag is added to
                # builtins, or loaded via {% load %}, it will be
                # available in a different module
                # see Django #7430
                if node is not None and \
                        isinstance(node,
                                   django.template.library.InclusionNode) \
                        and node.filename == 'webassets_tag.html':
                    bundle = make_bundle(str(node.args[0].var),
                                         '%s.js' % (str(uuid.uuid4()),),
                                         str(uuid.uuid4()))
                    result.append(bundle)
                for subnode in hasattr(node, 'nodelist') \
                        and node.nodelist or []:
                    _recurse_node(subnode)

            for node in t:
                _recurse_node(node)
            return result
