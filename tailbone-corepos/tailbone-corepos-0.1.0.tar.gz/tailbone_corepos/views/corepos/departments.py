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
CORE-POS department views
"""

from corepos.db import model as corepos

from .master import CoreOfficeMasterView


class DepartmentView(CoreOfficeMasterView):
    """
    Base class for department views.
    """
    model_class = corepos.Department
    model_title = "CORE-POS Department"
    url_prefix = '/core-pos/departments'
    route_prefix = 'corepos.departments'

    labels = {
        'dept_no': "Number",
        'dept_name': "Name",
        'dept_tax': "Tax",
        'dept_fs': "FS",
        'dept_limit': "Limit",
        'dept_minimum': "Minimum",
        'dept_discount': "Discount",
        'dept_see_id': "See ID",
        'modifiedby': "Modified by",
        'salesCode': "Sales Code",
        'memberOnly': "Member Only",
    }

    grid_columns = [
        'dept_no',
        'dept_name',
        'dept_tax',
        'dept_fs',
        'dept_limit',
        'dept_minimum',
        'dept_discount',
        'dept_see_id',
        'modified',
        'modifiedby',
        'margin',
        'salesCode',
        'memberOnly',
    ]

    def configure_grid(self, g):
        super(DepartmentView, self).configure_grid(g)

        g.filters['dept_no'].default_active = True
        g.filters['dept_no'].default_verb = 'equal'

        g.filters['dept_name'].default_active = True
        g.filters['dept_name'].default_verb = 'contains'

        g.set_type('modified', 'datetime_local')

        g.set_sort_defaults('dept_no')

        g.set_link('dept_no')
        g.set_link('dept_name')


def includeme(config):
    DepartmentView.defaults(config)
