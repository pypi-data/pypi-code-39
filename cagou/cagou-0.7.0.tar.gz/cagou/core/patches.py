#!/usr//bin/env python2
# -*- coding: utf-8 -*-

# Cagou: desktop/mobile frontend for Salut à Toi XMPP client
# Copyright (C) 2016-2019 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib2
import ssl


def apply():
    # allow to disable certificate validation
    ctx_no_verify = ssl.create_default_context()
    ctx_no_verify.check_hostname = False
    ctx_no_verify.verify_mode = ssl.CERT_NONE

    class HTTPSHandler(urllib2.HTTPSHandler):
        no_certificate_check = False

        def __init__(self, *args, **kwargs):
            urllib2._HTTPSHandler_ori.__init__(self, *args, **kwargs)
            if self.no_certificate_check:
                self._context = ctx_no_verify

    urllib2._HTTPSHandler_ori = urllib2.HTTPSHandler
    urllib2.HTTPSHandler = HTTPSHandler
    urllib2.HTTPSHandler.no_certificate_check = True
