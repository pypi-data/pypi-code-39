import requests
import re


class _base(dict):
    def _read_time(self, raw: str) -> int:
        """
        Given a string describing how much time remains until availability, return how many minutes are actually left.
        :param raw: string describing time remaining.
        :return: number of minutes remaining.
        """
        if raw == 'available':
            return 0
        digits_only = [c for c in raw if c.isdigit()]
        if digits_only:
            return int(digits_only)

    def __init__(self, raw, api):
        self.update(raw)
        self.update(self.__dict__)
        self.__dict__ = self
        self.api = api

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, dict.__repr__(self))


class Room(_base):
    def __init__(self, raw, api):
        super().__init__(raw, api)

        self.campus_name = raw['campus_name']
        self.name = raw['laundry_room_name']
        self.id = raw['location']
        self.status = raw['status']
        self.online = (self.status == 'online')
        self.offline = not self.online

    @property
    def availability(self):
        return self.api.availability(self.id)

    @property
    def totals(self):
        return self.api.totals(self.id)


class Availability(_base):
    def _int(self, raw):
        if raw == 'undefined':
            return None
        else:
            return int(raw)

    def __init__(self, raw, api):
        super().__init__(raw, api)

        self.dryer = self._int(raw['dryer'])
        self.washer = self._int(raw['washer'])


class Totals(Availability):
    pass


class Status(_base):
    def __init__(self, raw, api):
        super().__init__(raw, api)

        self.time_remaining_raw = raw['time_remaining']
        self.time_remaining = self._read_time(self.time_remaining_raw)
        self.change_time = int(raw['status_change_time'])
        self.out_of_service = bool(int(raw['out_of_service']))
        self.status_raw = raw['status']
        self.available = (self.status == 'Available')
        self.in_use = (self.status == 'In Use')


class Appliance(_base):
    def __init__(self, raw, api):
        super().__init__(raw, api)

        self.key = raw['appliance_desc_key']
        self.time_remaining_raw = raw['time_remaining']
        self.time_remaining = self._read_time(self.time_remaining_raw)
        self.avg_cycle_time = int(raw['avg_cycle_time'])
        self.out_of_service = bool(int(raw['out_of_service']))
        self.in_service = not self.out_of_service
        self.lrm_status = raw['lrm_status']
        self.online = (self.lrm_status == 'Online')
        self.offline = not self.online
        self.label = raw['label']
        self.type = raw['appliance_type']
        self.washer = (self.type == 'WASHER')
        self.dryer = (self.type == 'DRYER')
        self.status_raw = raw['status']
        self.available = (self.status == 'Available')
        self.in_use = (self.status == 'In Use')
        # TODO: there are probably more statuses

    @property
    def status(self):
        return self.api.status(self.key)


class YaleLaundry:
    API_ROOT = 'https://gw.its.yale.edu/soa-gateway/laundry/'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, endpoint: str, method: str, params: dict = {}):
        """
        Make a GET request to the API.

        :param params: dictionary of custom params to add to request.
        """
        params.update({
            'apikey': self.api_key,
            'type': 'json',
            'method': method,
        })
        request = requests.get(self.API_ROOT + endpoint, params=params)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed. Data returned: ' + request.text)

    def rooms(self):
        return [Room(raw, self) for raw in
                self.get('school', 'getRoomData')['school']['laundry_rooms']['laundryroom']]

    def availability(self, location):
        return Availability(self.get('room', 'getNumAvailable', {'location': location})['laundry_room'], self)

    def totals(self, location):
        return Totals(self.get('room', 'getTotal', {'location': location})['laundry_room'], self)

    def status(self, key):
        return Status(self.get('appliance', 'getStatus', {'appliance_desc_key': key})['appliance'], self)

    def appliances(self, location):
        return [Appliance(raw, self) for raw in
                self.get('room', 'getAppliances', {'location': location})['laundry_room']['appliances']['appliance']]
