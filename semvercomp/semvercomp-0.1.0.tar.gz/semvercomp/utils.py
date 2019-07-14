from semvercomp.Version import Version

def to_version_list(iterable):
	"""
		Parses a iterable of version strings to Version object
		and returns an array of version objects
	"""
	coll = []

	for v in iterable:
		ver = Version()
		ver.parse_version_number(v)
		coll.append(ver)

	return coll

def __normalize(ver):
	"""
		Parse to Version object a value of version
	"""
	if isinstance(ver, str):
		v = Version()
		v.parse_version_number(ver)
		return v
	
	if isinstance(ver, Version):
		return ver
