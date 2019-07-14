import pytest

import semvercomp.utils as utils
from semvercomp.Version import Version

def test_utils_to_version_list():
	versions = [
		'v1.0.1',
		'2.0.0',
		'0.0.0',
		'v12.3.0-beta+2010',
		'v1.0.3-alpha',
		'v11.2.33'
	]

	version_list = utils.to_version_list(versions)

	for index, version in enumerate(versions):
		ver = Version()
		ver.parse_version_number(version)
		assert ver == version_list[index]

def test_utils__normalize_str():
	v_str = 'v1.0.1-beta+201351'
	v_obj = utils.__normalize(v_str)
	expect = Version(1, 0, 1, 'beta', '201351', True)
	assert v_obj == expect

def test_utils__normalize_obj():
	expect = Version(1, 0, 1, 'beta', '201351', True)
	normalized = utils.__normalize(expect)
	assert normalized == expect
