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
CORE POS customer views
"""

from corepos.db import model as corepos

from .master import CoreOfficeMasterView


class CustomerView(CoreOfficeMasterView):
    """
    Base class for customer views.
    """
    model_class = corepos.Customer
    model_title = "CORE-POS Customer"
    url_prefix = '/core-pos/customers'
    route_prefix = 'corepos.customers'

    labels = {
        'id': "ID",
        'CardNo': "Card No.",
        'personNum': "Person No.",
        'LastName': "Last Name",
        'FirstName': "First Name",
        'CashBack': "Cash Back",
        'MemDiscountLimit': "Member Discount Limit",
        'ChargeLimit': "Charge Limit",
        'ChargeOk': "Charge OK",
        'WriteChecks': "Write Checks",
        'StoreCoupons': "Store Coupons",
        'memType': "Member Type No.",
        'NumberOfChecks': "Number of Checks",
        'memCoupons': "Member Coupons",
        'blueLine': "Blue Line",
        'LastChange': "Last Change",
    }

    grid_columns = [
        'CardNo',
        'FirstName',
        'LastName',
        'ChargeOk',
        'ChargeLimit',
        'Balance',
        'WriteChecks',
        'Purchases',
    ]

    def configure_grid(self, g):
        super(CustomerView, self).configure_grid(g)

        g.filters['FirstName'].default_active = True
        g.filters['FirstName'].default_verb = 'contains'

        g.filters['LastName'].default_active = True
        g.filters['LastName'].default_verb = 'contains'

        g.set_type('ChargeLimit', 'currency')
        g.set_type('Balance', 'currency')
        g.set_type('Purchases', 'currency')

        g.set_sort_defaults('CardNo')

        g.set_link('CardNo')
        g.set_link('FirstName')
        g.set_link('LastName')


def includeme(config):
    CustomerView.defaults(config)
