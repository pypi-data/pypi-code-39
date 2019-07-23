#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi


c = cdsapi.Client(full_stack=True, url='https://cds-test.climate.copernicus.eu/api/v2',key='1:0698258a-5875-4a0a-b1be-57230eed83ca')

r = c.retrieve(
"sis-water-quality-swicca",
{
    "time_aggregation": "month_average", 
    "variable": "total_phosphorous_concentrations", 
    "emissions_scenario": "rcp_4_5", 
    "period": "2071_2100", 
    "format": "zip"
}
)

r.download("x.grib")


"""
+ echo 'Current working directory: /home/ma/max'
+ /home/ma/mab/git/cds-forms/scripts/cds-load-test.py sis-water-quality-swicca /home/ma/mab/git/cds-forms/sis-water-quality-swicca/load_tests.json 3 https://cds-test.climate.copernicus.eu/api/v2 /home/ma/mab/git/cds-forms/ecflow/cds-test.climate.copernicus.eu.keys
2018-09-05 16:09:06,560 DEBUG CDSAPI {'full_stack': True, 'timeout': 86400, 'url': 'https://cds-test.climate.copernicus.eu/api/v2', 'verify': False, 'retry_max': 500, 'quiet': False, 'key': '18863:486a511e-511b-4f4e-b575-63b9bed3949a', 'sleep_max': 120, 'delete': True}
2018-09-05 16:09:06,560 INFO Sending request to https://cds-test.climate.copernicus.eu/api/v2/resources/sis-water-quality-swicca
2018-09-05 16:09:06,560 DEBUG POST https://cds-test.climate.copernicus.eu/api/v2/resources/sis-water-quality-swicca {"time_aggregation": "month_average", "variable": "total_phosphorous_concentrations", "emissions_scenario": "rcp_4_5", "period": "2071_2100", "format": "zip"}
2018-09-05 16:09:06,565 DEBUG Starting new HTTPS connection (1): cds-test.climate.copernicus.eu
/usr/local/apps/python/2.7.12-01/lib/python2.7/site-packages/requests/packages/urllib3/connectionpool.py:843: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
2018-09-05 16:09:06,581 DEBUG https://cds-test.climate.copernicus.eu:443 "POST /api/v2/resources/sis-water-quality-swicca HTTP/1.1" 202 70
2018-09-05 16:09:06,581 DEBUG REPLY {u'state': u'queued', u'request_id': u'8b3b2781-340d-4c52-a18b-5d7e5a88c3b8'}
2018-09-05 16:09:06,581 INFO Request is queued
2018-09-05 16:09:06,581 DEBUG Request ID is 8b3b2781-340d-4c52-a18b-5d7e5a88c3b8, sleep 1
2018-09-05 16:09:07,582 DEBUG GET https://cds-test.climate.copernicus.eu/api/v2/tasks/8b3b2781-340d-4c52-a18b-5d7e5a88c3b8
/usr/local/apps/python/2.7.12-01/lib/python2.7/site-packages/requests/packages/urllib3/connectionpool.py:843: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
2018-09-05 16:09:07,587 DEBUG https://cds-test.climate.copernicus.eu:443 "GET /api/v2/tasks/8b3b2781-340d-4c52-a18b-5d7e5a88c3b8 HTTP/1.1" 200 None
2018-09-05 16:09:07,588 DEBUG REPLY {u'state': u'failed', u'error': {u'url': u'http://copernicus-climate.eu/exc/url-adaptor-no-urls-available', u'who': u'client', u'reason': u'an internal error occurred processing your request', u'permanent': True, u'context': {u'traceback': u'Short traceback (most recent call last):\n  File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 46, in handle_request\n    return super().handle_request(cdsinf, data_request, config)\n  File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 92, in handle_retrieve\n    dis = self._fetch_list(valid_requests)\n  File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 194, in _fetch_list\n    "http://copernicus-climate.eu/exc/url-adaptor-no-urls-available")\ncdsclient.exceptions.DataProviderFileNotFoundError: an internal error occurred processing your request\n\n\n\nFull traceback:\n===============\nTraceback (most recent call last):\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 325, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 348, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>\n    lambda: self.handle_exception(context, e),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception\n    raise exception\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume\n    result = handle_locally()\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 192, in <lambda>\n    lambda: self.handle_request(context, request_data),\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 404, in handle_request\n    handlercdsinf, request_data, context.get("method_config", None))\n  File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 46, in handle_request\n    return super().handle_request(cdsinf, data_request, config)\n  File "/opt/cds/cdsinf/python/lib/cdsinf/runner/requesthandler.py", line 110, in handle_request\n    return handler(cdsinf, request, config)\n  File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 92, in handle_retrieve\n    dis = self._fetch_list(valid_requests)\n  File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 194, in _fetch_list\n    "http://copernicus-climate.eu/exc/url-adaptor-no-urls-available")\ncdsclient.exceptions.DataProviderFileNotFoundError: an internal error occurred processing your request\n'}, u'message': u'No URLs retrieved from a possible 1 URL(s)\nftp://ftp.smhi.se/cds/Water-Quality/concTP_periodmonavg/catchments/concTP-periodmonavg_rel_EUR-44_rcp45_IMPACT2C_QM-EOBS_2071-2100_1971-2000_remap215.nc'}, u'request_id': u'8b3b2781-340d-4c52-a18b-5d7e5a88c3b8'}
2018-09-05 16:09:07,588 INFO Request is failed
2018-09-05 16:09:07,588 ERROR Message: No URLs retrieved from a possible 1 URL(s)
ftp://ftp.smhi.se/cds/Water-Quality/concTP_periodmonavg/catchments/concTP-periodmonavg_rel_EUR-44_rcp45_IMPACT2C_QM-EOBS_2071-2100_1971-2000_remap215.nc
2018-09-05 16:09:07,588 ERROR Reason:  an internal error occurred processing your request
2018-09-05 16:09:07,588 ERROR   Short traceback (most recent call last):
2018-09-05 16:09:07,588 ERROR     File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 46, in handle_request
2018-09-05 16:09:07,588 ERROR       return super().handle_request(cdsinf, data_request, config)
2018-09-05 16:09:07,588 ERROR     File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 92, in handle_retrieve
2018-09-05 16:09:07,588 ERROR       dis = self._fetch_list(valid_requests)
2018-09-05 16:09:07,588 ERROR     File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 194, in _fetch_list
2018-09-05 16:09:07,588 ERROR       "http://copernicus-climate.eu/exc/url-adaptor-no-urls-available")
2018-09-05 16:09:07,588 ERROR   cdsclient.exceptions.DataProviderFileNotFoundError: an internal error occurred processing your request
2018-09-05 16:09:07,588 ERROR   
2018-09-05 16:09:07,588 ERROR   
2018-09-05 16:09:07,588 ERROR   
2018-09-05 16:09:07,588 ERROR   Full traceback:
2018-09-05 16:09:07,588 ERROR   ===============
2018-09-05 16:09:07,588 ERROR   Traceback (most recent call last):
2018-09-05 16:09:07,588 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,588 ERROR       result = handle_locally()
2018-09-05 16:09:07,588 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,588 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,588 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 325, in handle_exception
2018-09-05 16:09:07,588 ERROR       raise exception
2018-09-05 16:09:07,588 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,588 ERROR       result = handle_locally()
2018-09-05 16:09:07,588 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,589 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,589 ERROR       raise exception
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,589 ERROR       result = handle_locally()
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,589 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 348, in handle_exception
2018-09-05 16:09:07,589 ERROR       raise exception
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,589 ERROR       result = handle_locally()
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,589 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,589 ERROR       raise exception
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,589 ERROR       result = handle_locally()
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,589 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,589 ERROR       raise exception
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,589 ERROR       result = handle_locally()
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,589 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,589 ERROR       raise exception
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,589 ERROR       result = handle_locally()
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,589 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,589 ERROR       raise exception
2018-09-05 16:09:07,589 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,589 ERROR       result = handle_locally()
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,590 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,590 ERROR       raise exception
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,590 ERROR       result = handle_locally()
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,590 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,590 ERROR       raise exception
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,590 ERROR       result = handle_locally()
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,590 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,590 ERROR       raise exception
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,590 ERROR       result = handle_locally()
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 232, in <lambda>
2018-09-05 16:09:07,590 ERROR       lambda: self.handle_exception(context, e),
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 125, in handle_exception
2018-09-05 16:09:07,590 ERROR       raise exception
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 152, in _consume
2018-09-05 16:09:07,590 ERROR       result = handle_locally()
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 192, in <lambda>
2018-09-05 16:09:07,590 ERROR       lambda: self.handle_request(context, request_data),
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/dispatcher.py", line 404, in handle_request
2018-09-05 16:09:07,590 ERROR       handlercdsinf, request_data, context.get("method_config", None))
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 46, in handle_request
2018-09-05 16:09:07,590 ERROR       return super().handle_request(cdsinf, data_request, config)
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/cdsinf/python/lib/cdsinf/runner/requesthandler.py", line 110, in handle_request
2018-09-05 16:09:07,590 ERROR       return handler(cdsinf, request, config)
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 92, in handle_retrieve
2018-09-05 16:09:07,590 ERROR       dis = self._fetch_list(valid_requests)
2018-09-05 16:09:07,590 ERROR     File "/opt/cds/adaptor/cdshandlers/url/handler.py", line 194, in _fetch_list
2018-09-05 16:09:07,590 ERROR       "http://copernicus-climate.eu/exc/url-adaptor-no-urls-available")
2018-09-05 16:09:07,591 ERROR   cdsclient.exceptions.DataProviderFileNotFoundError: an internal error occurred processing your request
2018-09-05 16:09:07,591 ERROR   
{
    "time_aggregation": "month_average", 
    "variable": "total_phosphorous_concentrations", 
    "emissions_scenario": "rcp_4_5", 
    "period": "2071_2100", 
    "format": "zip"
}
Traceback (most recent call last):
  File "/home/ma/mab/git/cds-forms/scripts/cds-load-test.py", line 50, in <module>
    s = c.retrieve(dataset, r)
  File "/home/ma/mab/git/cdsapi/cdsapi/api.py", line 229, in retrieve
    result = self._api('%s/resources/%s' % (self.url, name), request)
  File "/home/ma/mab/git/cdsapi/cdsapi/api.py", line 312, in _api
    raise Exception("%s. %s." % (reply['error'].get('message'), reply['error'].get('reason')))
Exception: No URLs retrieved from a possible 1 URL(s)
ftp://ftp.smhi.se/cds/Water-Quality/concTP_periodmonavg/catchments/concTP-periodmonavg_rel_EUR-44_rcp45_IMPACT2C_QM-EOBS_2071-2100_1971-2000_remap215.nc. an internal error occurred processing your request.
+ ERROR
+ export PATH=/usr/local/apps/ecflow/4.9.0/bin:/usr/local/apps/ecflow/4.9.0/bin:/home/ma/max/bin/linux:/usr/local/apps/sniff.4.01/bin:/usr/local/apps/ecaccess/4.0.2/bin:/usr/local/apps/metview/5.0.3/bin:/usr/local/apps/eccodes/2.7.3/GNU/6.3.0/bin:/usr/local/apps/ecfs/2.2.4/bin:/usr/local/apps/sms/4.4.14/bin:/usr/local/apps/python/2.7.12-01/bin:/usr/local/apps/gcc/6.3.0/bin:/home/ma/max/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/bin/X11:/usr/games:/opt/bin:/usr/lib/mit/bin:/usr/lib/qt3/bin:/home/ma/max/bin/linux:/usr/local/apps/mysql/bin:/usr/local/apps/tn3270/lbin:/usr/local/apps/Zmail/bin:/usr/java/bin/
+ PATH=/usr/local/apps/ecflow/4.9.0/bin:/usr/local/apps/ecflow/4.9.0/bin:/home/ma/max/bin/linux:/usr/local/apps/sniff.4.01/bin:/usr/local/apps/ecaccess/4.0.2/bin:/usr/local/apps/metview/5.0.3/bin:/usr/local/apps/eccodes/2.7.3/GNU/6.3.0/bin:/usr/local/apps/ecfs/2.2.4/bin:/usr/local/apps/sms/4.4.14/bin:/usr/local/apps/python/2.7.12-01/bin:/usr/local/apps/gcc/6.3.0/bin:/home/ma/max/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/bin/X11:/usr/games:/opt/bin:/usr/lib/mit/bin:/usr/lib/qt3/bin:/home/ma/max/bin/linux:/usr/local/apps/mysql/bin:/usr/local/apps/tn3270/lbin:/usr/local/apps/Zmail/bin:/usr/java/bin/
+ set +e
+ wait
+ ecflow_client --abort=trap
+ trap 0
+ exit 0
debug1: client_input_channel_req: channel 0 rtype exit-status reply 0
debug1: channel 0: free: client-session, nchannels 1
debug1: fd 0 clearing O_NONBLOCK
debug1: fd 1 clearing O_NONBLOCK
Transferred: sent 4112, received 30240 bytes, in 2.9 seconds
Bytes per second: sent 1422.5, received 10461.1
debug1: Exit status 0
"""
