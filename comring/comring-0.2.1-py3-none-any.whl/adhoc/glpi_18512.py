#!/usr/bin/env python3

# Ad Hoc script for GLPI 18512 - Request data korporat

import os
import csv
import re

from comring.lib import odoo

ODOO_URL = 'https://odoo.pti-cosmetics.com'

data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'glpi_18512.csv')

invoice_list = []
with open(data_path, 'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:
        invoice_list.append({'number': row['number']})

server = odoo.Odoo(ODOO_URL)
client = server.login('paragon', 'it-agustianes', 'aghi2kaisa6G')

for inv in invoice_list:
    oinv = client.search_read_one('account.invoice', [('number', '=', inv['number'])], ['id', 'number', 'name'])
    if oinv:
        inv['id'] = oinv['id']
        inv['name'] = oinv['name']

pattern = re.compile(r'([A-Z]+) / ([A-Z0-9]+) / ([A-Z ]+)')
by_dc_by_unit = {}
for inv in invoice_list:
    ref = inv.get('name', '')
    match = pattern.match(ref)
    dc_alias = korporat_ref = korporat_unit = ''
    if match:
        dc_alias = match.group(1)
        korporat_ref = match.group(2)
        korporat_unit = match.group(3)
    if korporat_unit == 'MAKE OVER':
        korporat_unit = 'mo'

    if dc_alias and korporat_ref and korporat_unit:
        key = (dc_alias, korporat_unit)
        numbers = by_dc_by_unit.setdefault(key, [])
        numbers.append(korporat_ref)

for dc, unit in by_dc_by_unit:
    numbers = by_dc_by_unit.get((dc, unit))
    print(dc, unit, numbers)
