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
CORE-POS product views
"""

from corepos.db import model as corepos

from .master import CoreOfficeMasterView


class ProductView(CoreOfficeMasterView):
    """
    Base class for product views.
    """
    model_class = corepos.Product
    model_title = "CORE-POS Product"
    url_prefix = '/core-pos/products'
    route_prefix = 'corepos.products'

    labels = {
        'id': "ID",
        'upc': "UPC",
        'pricemethod': "Price Method",
        'groupprice': "Group Price",
        'specialpricemethod': "Special Price Method",
        'specialgroupprice': "Special Group Price",
        'specialquantity': "Special Quantity",
        'dept_no': "Dept. No.",
        'foodstamp': "Food Stamp",
        'scaleprice': "Scale Price",
        'mixmatchcode': "Mix Match Code",
        'tareweight': "Tare Weight",
        'discounttype': "Discount Type",
        'unitofmeasure': "Unit of Measure",
        'qttyEnforced': "Qty. Enforced",
        'idEnforced': "ID Enforced",
        'inUse': "In Use",
        'numflag': "Num. Flag",
        'subdept': "Subdept. No.",
        'default_vendor_id': "Default Vendor ID",
        'current_origin_id': "Current Origin ID",
    }

    grid_columns = [
        'upc',
        'brand',
        'description',
        'size',
        'department',
        'vendor',
        'normal_price',
        'cost',
    ]

    def configure_grid(self, g):
        super(ProductView, self).configure_grid(g)

        g.set_joiner('department', lambda q: q.outerjoin(corepos.Department))
        g.set_sorter('department', corepos.Department.dept_name)

        g.set_joiner('vendor', lambda q: q.outerjoin(corepos.Vendor))
        g.set_sorter('vendor', corepos.Vendor.vendorName)

        g.filters['upc'].default_active = True
        g.filters['upc'].default_verb = 'equal'

        g.set_type('cost', 'currency')
        g.set_type('normal_price', 'currency')

        g.set_sort_defaults('upc')

        g.set_link('upc')
        g.set_link('brand')
        g.set_link('description')

    def configure_form(self, f):
        super(ProductView, self).configure_form(f)

        f.set_type('start_date', 'datetime_local')
        f.set_type('end_date', 'datetime_local')
        f.set_type('modified', 'datetime_local')

        f.set_type('normal_price', 'currency')
        f.set_type('groupprice', 'currency')
        f.set_type('special_price', 'currency')
        f.set_type('specialgroupprice', 'currency')
        f.set_type('cost', 'currency')
        f.set_type('deposit', 'currency')


def includeme(config):
    ProductView.defaults(config)
