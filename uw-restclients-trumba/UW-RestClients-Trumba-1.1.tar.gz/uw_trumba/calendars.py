"""
Interfacing with Trumba Calendars' service, this module
provides methods to obtain calendar info and
user calendar permissions in Trumba
The underline http requests and responses will be logged.
Be sure to set the logging configuration if you use the LiveDao!
"""

import logging
import re
from uw_trumba.models import TrumbaCalendar, is_bot, is_sea, is_tac
from uw_trumba import post_bot_resource, post_sea_resource, post_tac_resource
from uw_trumba.permissions import load_json, get_cal_permissions


logger = logging.getLogger(__name__)
calendarlist_url = "/service/calendars.asmx/GetCalendarList"
re_cal_id = re.compile(r'[1-9]\d*')


class Calendars:

    def __init__(self):
        """
        Build a dictionary of {calenderid, TrumbaCalendar} for each campus
        """
        self.campus_calendars = {}
        self.load(TrumbaCalendar.BOT_CAMPUS_CODE)
        self.load(TrumbaCalendar.SEA_CAMPUS_CODE)
        self.load(TrumbaCalendar.TAC_CAMPUS_CODE)

    def load(self, campus):
        """
        :except: DataFailureException if the underline request failed.
        """
        if is_bot(campus):
            resp = post_bot_resource(calendarlist_url, "{}")
        elif is_tac(campus):
            resp = post_tac_resource(calendarlist_url, "{}")
        else:
            resp = post_sea_resource(calendarlist_url, "{}")
        self.process_resp(resp, campus)

    def process_resp(self, response, campus):
        """
        Load a dictionary of {calenderid, TrumbaCalendar} to
        the self.campus_calendars[campus]
        """
        request_id = "{0} {1}".format(campus, calendarlist_url)
        calendar_dict = {}
        data = load_json(request_id, response)
        if (data['d']['Calendars'] is not None and
                len(data['d']['Calendars']) > 0):
            _extract_cals(campus, data['d']['Calendars'], calendar_dict, None)

        self.campus_calendars[campus] = calendar_dict


def _extract_cals(campus, resp_fragment, calendar_dict, parent):
    """
    Extract calendars and load permissions. Update calendar_dict.
    """
    for record in resp_fragment:
        if (re.match(r'Internal Event Actions', record['Name']) or
                re.match(r'Migrated .*', record['Name'])):
            continue

        if not _is_valid_calendarid(record.get('ID')):
            logger.warn(
                "InvalidCalendarId, {0} skipped!".format(record))
            continue

        trumba_cal = TrumbaCalendar(calendarid=int(record['ID']),
                                    campus=campus)
        if parent is None:
            trumba_cal.name = record.get('Name')
        else:
            trumba_cal.name = "{0} >> {1}".format(parent, record.get('Name'))

        get_cal_permissions(trumba_cal)
        calendar_dict[trumba_cal.calendarid] = trumba_cal

        if (record.get('ChildCalendars') is not None and
                len(record['ChildCalendars']) > 0):
            _extract_cals(campus,
                          record['ChildCalendars'],
                          calendar_dict,
                          trumba_cal.name)


def _is_valid_calendarid(calendarid):
    return re_cal_id.match(str(calendarid)) is not None
