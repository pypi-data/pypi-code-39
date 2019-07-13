import datetime
import unicodedata
import pickle
from os.path import exists
from os.path import expanduser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


class GCalender():
    def __init__(self, maxResults=10):
        # OAuth
        self.credential = None
        self._make_credential()
        self.service = build('calendar', 'v3', credentials=self.credential)
        self.events = []
        self.get_cal_events(30, maxResults)

    def _make_credential(self):
        if exists(expanduser('~/.pyoklock/token.pickle')):
            with open(expanduser('~/.pyoklock/token.pickle'), 'rb') as token:
                self.credential = pickle.load(token)
        if not self.credential or not self.credential.valid:
            if self.credential and\
                    self.credential.expired and self.credential.refresh_token:
                self.credential.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    expanduser('~/.pyoklock/credentials.json'), SCOPES)
                self.credential = flow.run_local_server()
            with open(expanduser('~/.pyoklock/token.pickle'), 'wb') as token:
                pickle.dump(self.credential, token)

    def get_cal_events(self, dminutes, maxResults):
        now = datetime.datetime.utcnow() - datetime.timedelta(minutes=dminutes)
        now = now.isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=maxResults,
            singleEvents=True,
            orderBy='startTime').execute()
        self.events = events_result.get('items', [])

    def get_calender_text(self):
        if not self.events:
            return 'No upcoming events found.'

        # make text
        text = ''
        for event in self.events:
            d = event['start'].get('dateTime', None)
            if d is None:
                t = '     '
                d = event['start'].get('date', '     ')
                if ' ' not in d:
                    d = datetime.datetime.strptime(d, "%Y-%m-%d")
                    d = '{:2d}/{:02}'.format(d.month, d.day)
            else:
                # 2017-08-07T07:09:31+00:00 -> 2017-08-07T07:09:31+0000
                d = d.split('+')
                d[1] = d[1].replace(':', '')
                d = datetime.datetime.strptime('+'.join(d),
                                               "%Y-%m-%dT%H:%M:%S%z")
                t = '{:2d}:{:02}'.format(d.hour, d.minute)
                d = '{:2d}/{:02}'.format(d.month, d.day)

            text += f"{d} {t} > {event['summary']}\n"
        return text

    def get_max_length(self):
        return max([
            get_east_asian_width_count(x)
            for x in self.get_calender_text().split('\n')
        ])
