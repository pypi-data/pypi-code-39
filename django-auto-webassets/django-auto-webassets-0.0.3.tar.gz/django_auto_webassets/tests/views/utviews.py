
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

import django.views.generic
import django_auto_webassets.views.mixins


class EmptyView(django.views.generic.TemplateView):
    """Test View showing a simple template."""

    template_name = 'generic.html'


class FunctionalTestView(django.views.generic.TemplateView):
    """Test View showing a simple template."""

    template_name = 'simple_functional.html'


class FunctionViewWithMixin(
        django_auto_webassets.views.mixins.AutoWebassetsJSMixin,
        django.views.generic.TemplateView):
    """Test View including a webasset_js_file."""

    template_name = 'simple_functional.html'
    webasset_js_file = 'simple_functional_alt.js'
