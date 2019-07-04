"""
Interfacing with Trumba Calendars' service, this module
provides methods to obtain calendar info and
user calendar permissions in Trumba
The underline http requests and responses will be logged.
Be sure to set the logging configuration if you use the LiveDao!
"""

import json
import logging
import re
from restclients_core.exceptions import DataFailureException
from uw_trumba.models import Permission
from uw_trumba import (
    post_bot_resource, post_sea_resource, post_tac_resource)
from uw_trumba.exceptions import (
    CalendarOwnByDiffAccount, CalendarNotExist, NoDataReturned,
    UnknownError, UnexpectedError)


logger = logging.getLogger(__name__)
re_email = re.compile(r'[a-z][a-z0-9\-\_\.]{,127}@washington.edu')
permissions_url = "/service/calendars.asmx/GetPermissions"


def get_cal_permissions(calendar):
    """
    :param calendar: a TrumbaCalendar object
    Set the calendar.permissions attribute with a list of Permission objects.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    try:
        calendar.permissions = _process_resp(
            _get_post_response(calendar), calendar)
    except Exception as ex:
        logger.error("get_cal_permissions on {0} ==> {1}".format(
                calendar, str(ex)))


def _process_resp(post_response, calendar):
    """
    :return: a list of trumba.Permission objects
             sorted by descending level and ascending uwnetid
             None if error, [] if not exists
    If the response is successful, process the response data
    and load into the return objects
    otherwise raise DataFailureException
    """
    request_id = "{0} {1} CalendarID:{2}".format(calendar.campus,
                                                 permissions_url,
                                                 calendar.calendarid)
    data = load_json(request_id, post_response)

    permission_list = []
    if (data.get('d') is not None and data['d'].get('Users') is not None and
            len(data['d']['Users']) > 0):
        _load_permissions(calendar, data['d']['Users'], permission_list)

    return sorted(permission_list)


def load_json(request_id, post_response):
    if post_response.status != 200:
        raise DataFailureException(request_id,
                                   post_response.status,
                                   post_response.reason)
    if post_response.data is None:
        raise NoDataReturned()
    data = json.loads(post_response.data)
    _check_err(data)
    return data


def _create_get_perm_body(calendar_id):
    return json.dumps({'CalendarID': calendar_id})


def _get_post_response(calendar):
    if calendar.is_bot():
        return post_bot_resource(
            permissions_url, _create_get_perm_body(calendar.calendarid))
    elif calendar.is_tac():
        return post_tac_resource(
            permissions_url, _create_get_perm_body(calendar.calendarid))
    else:
        return post_sea_resource(
            permissions_url, _create_get_perm_body(calendar.calendarid))


def _is_valid_email(email):
    return re_email.match(email) is not None


def _extract_uwnetid(email):
    return re.sub("@washington.edu", "", email)


def _load_permissions(calendar, resp_fragment, permission_list):
    for record in resp_fragment:
        if not _is_valid_email(record.get('Email')):
            continue
            # skip the non UW users
        perm = Permission(calendar=calendar,
                          uwnetid=_extract_uwnetid(record['Email']),
                          level=record.get('Level'),
                          name=record.get('Name'))
        permission_list.append(perm)


def _check_err(data):
    """
    :param data: response json data (must be not None).
    Check possible error code returned in the response body
    raise the coresponding exceptions
    """
    if data.get('d') is None:
        raise NoDataReturned()

    if data['d'].get('Messages') is None:
        return

    msg = data['d']['Messages']
    if len(msg) == 0 or msg[0].get('Code') is None:
        raise UnknownError()

    code = int(msg[0]['Code'])
    if code == 3006:
        raise CalendarNotExist()
    elif code == 3007:
        raise CalendarOwnByDiffAccount()
    else:
        logger.warn("Unexpected Error Code: {0} {1}".format(
                code, msg[0].get('Description')))
        raise UnexpectedError()
