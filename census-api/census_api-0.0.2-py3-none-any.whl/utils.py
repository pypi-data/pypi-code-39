####################################
##### Utilities for census_api #####
####################################

import addfips

af = addfips.AddFIPS()

states = {'AL': 1, 'AK': 2, 'AZ': 4, 'AR': 5, 'CA': 6, 'CO': 8, 'CT': 9, 'DE': 10, 'DC': 11, 'FL': 12, 'GA': 13, 'HI': 15, 'ID': 16, 'IL': 17, 'IN': 18, 'IA': 19, 'KS': 20, 'KY': 21, 'LA': 22, 'ME': 23, 'MD': 24, 'MA': 25, 'MI': 26, 'MN': 27, 'MS': 28, 'MO': 29, 'MT': 30, 'NE': 31, 'NV': 32, 'NH': 33, 'NJ': 34, 'NM': 35, 'NY': 36, 'NC': 37, 'ND': 38, 'OH': 39, 'OK': 40, 'OR': 41, 'PA': 42, 'RI': 44, 'SC': 45, 'SD': 46, 'TN': 47, 'TX': 48, 'UT': 49, 'VT': 50, 'VA': 51, 'WA': 53, 'WV': 54, 'WI': 55, 'WY': 56, 'AS': 60, 'GU': 66, 'MP': 69, 'PR': 72, 'UM': 74, 'VI': 78}

def get_county_fips(county, state):
	"""
	Uses `addfips` library to get FIPS codes for counties

	Args:

	* `county` (`str`): County to get FIPS code for
	* `state` (`str`): Abbreviation for state that contains `county`
	
	Returns:

	* `str`. The FIPS code of `county`
	"""
	return af.get_county_fips(county, state=state)[2:]

def zero_pad_state(state):
	"""
	Returns state FIPS code zero-padded to 2 digits

	Args:

	* `state` (`str`): The state to get FIPS code for

	Returns:

	* `str`. The FIPS code for `state`
	"""
	n = states[state]
	if n >= 10:
		return str(n)
	else:
		return "0" + str(n)