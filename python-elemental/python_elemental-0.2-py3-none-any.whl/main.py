import time
from client import ElementalLive
from urllib.parse import urlparse, quote
import hashlib
import requests
from jinja2 import Template
# from client import etree_to_dict
import json
import xml.etree.ElementTree as ET

USER = "admin"
API_KEY = "zsMYZ-Rp7-B4b4FvSvWt"
# API_KEY = ""
# Generate template
# template_path = "./templates/qvbr_mediastore.xml"
# options = { 'username': 'AKIAX3GU2745IRM7YRTZ', 'password': 'ZF/yjHCSvgCkmM69hf6NJKOgm0Hp61xBVZaT8I6I',
#             'mediastore_container_master': 'https://hu5n3jjiyi2jev.data.mediastore.us-east-1.amazonaws.com/master',
#             'mediastore_container_backup': 'https://hu5n3jjiyi2jev.data.mediastore.us-east-1.amazonaws.com/backup',
#             'channel': "1", 'device_number': "0"}
client = ElementalLive("http://elemental.dev.cbsivideo.com", USER, API_KEY)
# response = client.create_event(options)
# response = client.get_input_devices()
# with open('index.text', 'w') as file:
#     file.write(str(response))
# print(response)
# print(json.dumps(response, indent=4))

resp = client.get_input_devices_by_id(1)
print(resp)
# sample_xml = '    <device_input> ' \
#              '<device_type>AJA</device_type> ' \
#              '<device_number>0</device_number> ' \
#              '<channel>1</channel> ' \
#              '<channel_type>HD-SDI</channel_type>' \
#              '<device_name>HD-SDI 1</device_name>' \
#              '<name nil="true"/>' \
#              '<sdi_settings>' \
#              '<input_format>Auto</input_format>' \
#              '<scte104_offset>0</scte104_offset>' \
#              '</sdi_settings>' \
#              '</device_input>'
# root = ET.fromstring(sample_xml)
# root_dict = etree_to_dict(root)

# print(root_dict)