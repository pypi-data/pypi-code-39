import re

def validate_version(ver):
	"""
		Validates the version tag as string to check if
		it is a valid semver version number
	"""
	parts = dict()
	regexp_str = r'(v)?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
	results = re.match(regexp_str, ver)

	try:
		if len(results.groups()) > 0:
			parts['has_v'] = results.group(1) == 'v' or results.group(1) == 'V'
			parts['major'] = int(results.group(2))
			parts['minor'] = int(results.group(3))
			parts['patch'] = int(results.group(4))
			parts['pre_release'] = results.group(5)
			parts['build'] = results.group(6)

		return (parts, True)
	except:
		return (None, False)
