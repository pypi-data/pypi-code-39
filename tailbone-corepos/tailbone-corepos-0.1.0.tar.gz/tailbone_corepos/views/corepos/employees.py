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
CORE-POS employee views
"""

from corepos.db import model as corepos

from .master import CoreOfficeMasterView


class EmployeeView(CoreOfficeMasterView):
    """
    Base class for employee views.
    """
    model_class = corepos.Employee
    model_title = "CORE-POS Employee"
    url_prefix = '/core-pos/employees'
    route_prefix = 'corepos.employees'

    labels = {
        'emp_no': "Number",
        'CashierPassword': "Cashier Password",
        'AdminPassword': "Admin Password",
        'FirstName': "First Name",
        'LastName': "Last Name",
        'JobTitle': "Job Title",
        'EmpActive': "Active",
        'frontendsecurity': "Frontend Security",
        'backendsecurity': "Backend Security",
        'birthdate': "Birth Date",
    }

    grid_columns = [
        'emp_no',
        'FirstName',
        'LastName',
        'JobTitle',
        'EmpActive',
        'birthdate',
    ]

    def configure_grid(self, g):
        super(EmployeeView, self).configure_grid(g)

        g.filters['EmpActive'].default_active = True
        g.filters['EmpActive'].default_verb = 'is_true'

        g.filters['FirstName'].default_active = True
        g.filters['FirstName'].default_verb = 'contains'

        g.filters['LastName'].default_active = True
        g.filters['LastName'].default_verb = 'contains'

        g.set_sort_defaults('emp_no')

        g.set_link('emp_no')
        g.set_link('FirstName')
        g.set_link('LastName')

    def grid_extra_class(self, employee, i):
        if not employee.EmpActive:
            return 'warning'


def includeme(config):
    EmployeeView.defaults(config)
