
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

from django import template

import django_assets.env
from ..views.mixins import AutoWebassetsJSMixin

from ..utils.webassetsrjs import make_bundle

register = template.Library()


def _get_complete_classname(cls):
    return '.'.join([inspect.getmodule(cls).__name__, cls.__name__])


@register.inclusion_tag('webassets_tag.html', takes_context=True)
def webassets_js(context, default_js=None):
    """Template Tag for auto webassets."""
    view_class = context['view'].__class__
    view_class_name = _get_complete_classname(view_class)
    if isinstance(context['view'],
                  AutoWebassetsJSMixin) \
            and view_class_name in django_assets.env.get_env():
        return {'full_class_name': view_class_name}
    elif default_js:
        make_bundle(default_js, '.'.join([view_class_name, 'js']),
                    view_class_name)
        return {'full_class_name': view_class_name}
