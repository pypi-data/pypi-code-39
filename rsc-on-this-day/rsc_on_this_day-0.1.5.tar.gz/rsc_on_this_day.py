#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  rsc_on_this+day.py
"""Docstring Goes Here"""
#
#  Copyright 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

__author__ = "Dominic Davis-Foster"
__copyright__ = "2019 Dominic Davis-Foster"

__license__ = "GPL"
__version__ = "0.1.5"
__email__ = "dominic@davis-foster.co.uk"


import requests
from bs4 import BeautifulSoup
#from datetime import datetime as dt
import datetime
import requests_cache
from cashier import cache


# Initialise requests-cache
expire_after = datetime.timedelta(hours=5)
requests_cache.install_cache(expire_after=expire_after)
requests_cache.remove_expired_responses()

# -----------------------------------------

# TODO: custom dates

@cache(cache_file="cache.db", cache_time=18000, retry_if_blank=True)
def query_website():
	page = requests.get("http://www.rsc.org/learn-chemistry/collections/chemistry-calendar")
	
	soup = BeautifulSoup(page.content, "html.parser")
	
	# print(datetime.datetime.today().strftime('%d %B'))
	
	header = soup.find("div", {"class": "description"}).previousSibling.previousSibling.get_text().strip()
	body = soup.find("div", {"class": "description"}).get_text().strip()
	
	return header, body

def main():
	header, body = query_website()
	print(header)
	print(body)

	
if __name__ == "__main__":
	main()

# TODO: Timeout