#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging

import ovirtsdk4 as sdk
import ovirtsdk4.types as types

logging.basicConfig(level=logging.DEBUG, filename='example.log')

# This example will connect to the server and print the names and identifiers of all the virtual machines:

# Create the connection to the server:
connection = sdk.Connection(
    url='https://she-test-09.rhev.lab.eng.brq.redhat.com/ovirt-engine/api',
    username='admin@internal',
    password='123456',
    #ca_file='ca.pem',
    insecure=True,
    debug=True,
    log=logging.getLogger(),
)

# Get the reference to the "domains" service:
domains_service = connection.system_service().domains_service()

# Use the "list" method of the "domains" service to list all the AAA domains of the system:
domains = domains_service.list()

# Print the virtual machine names and identifiers:
for domain in domains:
  print("%s: %s" % (domain.name, domain.id))

# Close the connection to the server:
connection.close()
