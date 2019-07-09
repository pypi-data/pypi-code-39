# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2019 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
CORE POS master view
"""

# import six

# from corepos.util import catapult_time

# from rattail.time import localtime
# from rattail.util import NOTSET

from tailbone.views import MasterView
# from tailbone.util import raw_datetime
from tailbone_corepos.db import CoreOfficeSession


class CoreOfficeMasterView(MasterView):
    """
    Master base class for Catapult views
    """
    Session = CoreOfficeSession
    # model_key = 'pk'
    creatable = False
    editable = False
    deletable = False

    # # TODO: would be nice to find a way around this somehow
    # # must encode all search values as utf-8
    # use_byte_string_filters = True

    # def get_action_route_kwargs(self, row):
    #     return {'pk': six.text_type(row.pk)}

    # def render_catapult_datetime(self, record, field, value=NOTSET):
    #     if value is NOTSET:
    #         value = getattr(record, field)
    #     if not value:
    #         return ""
    #     value = catapult_time(value)
    #     value = localtime(self.rattail_config, value)
    #     return raw_datetime(self.rattail_config, value)
