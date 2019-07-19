# -*- coding: utf-8 -*-

import requests


def converter(amount=1.0, frm="eur", to="usd"):

	frm = frm.upper()
	to = to.upper()

	url = "https://api.exchangeratesapi.io/latest?base=%s" % frm

	resp = requests.get(url=url)

	data = resp.json()

	try:
		rate = data['rates'].get(to, -1)
		if rate >= 0:
			return amount * rate
		else:
			return 0
	except:
		return 0
