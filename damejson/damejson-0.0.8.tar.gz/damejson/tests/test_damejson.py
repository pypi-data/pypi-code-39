#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with damejson; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import unittest
import json

class TestDameJson(unittest.TestCase):

    def test_damejson_load(self):
        # using read and loads to open
        jsondata = open('files/exer1-interface-data.json').read()
        json_object = json.loads(jsondata)
        self.assertEqual(int(json_object['totalCount']), 400)
        # using open and load to open
        with open('files/exer1-interface-data.json') as json_data:
            d = json.load(json_data)
        self.assertEqual(int(d['totalCount']), 400)

    def test_damejson_dumps(self):
        self.assertEqual('["foo", {"bar": ["baz", 1.0, 2]}]', json.dumps(['foo', {'bar': ('baz', 1.0, 2)}]))
        self.assertEqual(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True), '{"a": 0, "b": 0, "c": 0}')
        tup1 = 'Red', 'Black', 'White';
        self.assertEqual(json.dumps(tup1), '["Red", "Black", "White"]')

if __name__ == '__main__':
    unittest.main()
