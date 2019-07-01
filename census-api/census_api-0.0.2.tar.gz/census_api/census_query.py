#####################################
##### Class to Query Census API #####
#####################################

import requests
import json
import pandas as pd
import datascience as ds
from .utils import *

class CensusQuery:
	"""Object to query US Census API"""

	_url_endings = {
		"acs5" : "acs/acs5",
		"acs1" : "acs/acs1",
		"sf1" : "dec/sf1"
	}

	def __init__(self, api_key, dataset, year=None, out="pd"):
		"""
		Initializes the CensusQuery object to start API requests

		Args:

		* api_key (`str`): User's API key
		* dataset (`str`): The dataset to be queried; `"acs5"`, `"acs1"`, or `"sf1"`

		Kwargs:

		* year (`int`): The year to query data for; can be overwritten in `CensusQuery.query`
		* out (`str`): Whether output should be `pandas.DataFrame` or `datascience.tables.Table`; `"pd"` or `"ds"`

		Returns:

		* `CensusQuery`. The `CensusQuery` instance to be used to query the API
		"""
		assert dataset in CensusQuery._url_endings.keys(), "{} is not a valid dataset".format(dataset)

		self._dataset = CensusQuery._url_endings[dataset]
		if year:
			assert type(year) == int, "{} not a valid year".format(year)
		self._year = year

		self._api_key = api_key
		assert out in ["pd", "ds"], """out argument must be \"pd\" or \"ds\""""
		self._out = out

	def _make_params(self, variables, state, county, tract, year):
		"""
		Creates parameters dict for requests

		Args:

		* `variables` (`list`): List of variables to extract
		* `state` (`str`): Abbreviation for state from which to query data
		* `county` (`str`): County name for localized queries
		* `tract` (`str`): FIPS code for tract to query data from
		* `year` (`int`): Year for which to query data

		Returns:

		* `dict`. A dict of parameters for the API query
		"""
		assert type(variables) == list, "variables must be a list"
		assert len(state) == 2, "state must be an abbreviation"
		params = {}
		params["get"] = ",".join(variables)
		params["for"] = "tract:{}".format(tract)

		state_fips = zero_pad_state(state)
		params["in"] = "state:{}".format(state_fips)

		if county:
			county_fips = get_county_fips(county, state)
			params["in"] += "+county:{}".format(county_fips)
		params["key"] = self._api_key
		return params

	def _send_request(self, variables, state, county, tract, year):
		"""
		Sends request to API through `requests` package

		Args:

		* `variables` (`list`): List of variables to extract
		* `state` (`str`): Abbreviation for state from which to query data
		* `county` (`str`): County name for localized queries
		* `tract` (`str`): FIPS code for tract to query data from
		* `year` (`int`): Year for which to query data

		Returns:

		* `pandas.DataFrame`. The data retrieved from the query
		"""
		params = self._make_params(variables, state, county, tract, year)

		url = "https://api.census.gov/data/{}/{}".format(year, self._dataset)
		response = requests.get(url, params)
		try:
			text = json.loads(response.text)
		except json.JSONDecodeError:
			return response.text
		cols = text[0]

		response_df = pd.DataFrame(text[1:], columns=cols)
		return response_df

	def query(self, variables, state, county=None, tract="*", year=None):
		"""
		Queries Census API to get data regarding listed variables; if `year` provided, ignores `CensusData` instance year

		Args:

		* `variables` (`list`): List of variables to extract
		* `state` (`str`): Abbreviation for state from which to query data
		* `county` (`str`): County name for localized queries
		* `tract` (`str`): FIPS code for tract to query data from
		* `year` (`int`): Year for which to query data; if provided, ignores instance `year`

		Returns:

		* `pandas.DataFrame` or `datascience.tables.Table`. The data retrieved from the query
		"""
		if not self._year:
			assert year != None, "Year must be defined"
			assert type(year) == int, "{} not a valid year".format(year)
		response_df = self._send_request(variables, state, county, tract, year)
		if self._out == "ds":
			return ds.Table.from_df(response_df)
		return response_df