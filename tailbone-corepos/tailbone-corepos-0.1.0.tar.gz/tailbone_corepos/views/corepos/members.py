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
CORE-POS member views
"""

from corepos.db import model as corepos

from .master import CoreOfficeMasterView


class MemberTypeView(CoreOfficeMasterView):
    """
    Master view for member types
    """
    model_class = corepos.MemberType
    model_title = "CORE-POS Member Type"
    url_prefix = '/core-pos/member-types'
    route_prefix = 'corepos.member_types'

    labels = {
        'memtype': "Type",
        'memDesc': "Description",
        'custdataType': "Cust. Data Type",
        'ssi': "SSI",
        'salesCode': "Sales Code",
    }

    def configure_grid(self, g):
        super(MemberTypeView, self).configure_grid(g)

        g.set_link('memtype')
        g.set_link('memDesc')


class MemberView(CoreOfficeMasterView):
    """
    Master view for members
    """
    model_class = corepos.MemberInfo
    model_title = "CORE-POS Member"
    url_prefix = '/core-pos/members'
    route_prefix = 'corepos.members'


def includeme(config):
    MemberTypeView.defaults(config)
    MemberView.defaults(config)
