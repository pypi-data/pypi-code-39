import pytest

import semvercomp.validators as validators

def test_validate_version_returns_True():
	version = "v1.0.0"
	(parts, is_ok) = validators.validate_version(version)
	assert is_ok == True
	assert parts != None

def test_validate_version_returns_parts():
	version = "v30.11.22-beta+20190713"
	(parts, is_ok) = validators.validate_version(version)

	assert is_ok == True
	assert parts['has_v'] == True
	assert parts['major'] == 30
	assert parts['minor'] == 11
	assert parts['patch'] == 22
	assert parts['pre_release'] == 'beta'
	assert parts['build'] == '20190713'

def test_validate_version_find_error():
	version = "v022.22.11"
	(parts, is_ok) = validators.validate_version(version)

	assert is_ok == False
	assert parts == None
