"""
    Misc utils for Runbook
"""
import json
from datetime import datetime, timezone

class RunbookReturn:
    """ The return values from executing a runbook """
    def __init__(self):
        self._status = None
        self._error = None
        self._resource = None
        self._body = None
        self._logs = []

    def _struct(self):
        return {
            'Status'  : self._status,
            'Error'   : self._error,
            'Resource': self._resource,
            'Body'    : self._body,
            'Logs'    : self._logs
        }

    def log(self, message):
        """ Append the log message """
        now = datetime.now(timezone.utc).isoformat(timespec='seconds')
        self._logs.append(f'{now} {message}')


    def generate_error(self, val, body=None):
        """ Set runbook status to fail and log details if given """
        self._status = 'fail'
        self._error = val
        if body:
            self._body = body
        self.log(val)


    @property
    def json(self):
        """ Return the runbook output details as JSON """
        return json.dumps(self._struct())

    @property
    def status(self):
        """ return the status of the runbook """
        return self._status

    @status.setter
    def status(self, val):
        if val in ('ok', 'fail'):
            self._status = val
        else:
            raise ValueError('status should be \'ok\' or \'error\'')

    @property
    def error(self):
        """ return error message """
        return self._error

    @property
    def resource(self):
        """ return resource """
        return self._resource

    @resource.setter
    def resource(self, val):
        self._resource = val

    @property
    def body(self):
        """ return body"""
        return self._body

    @body.setter
    def body(self, val):
        self._body = val
