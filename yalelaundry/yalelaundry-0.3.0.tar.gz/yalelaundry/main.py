import requests
import re


class _base(dict):
    def _read_time(self, raw: str) -> int:
        """
        Given a string describing how much time remains until available, return how many minutes are actually left.
        :param raw: string describing time remaining.
        :return: number of minutes remaining, or 0 if the machine is not in operation.
        """
        digits_only = [c for c in raw if c.isdigit()]
        if digits_only:
            return int(''.join(digits_only))
        return 0

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
    def available(self):
        return self.api.available(self.id)

    @property
    def total(self):
        return self.api.total(self.id)

    @property
    def use(self):
        return self.api.use(self.id)

    @property
    def appliances(self):
        return self.api.appliances(self.id)


class Available(_base):
    def _int(self, raw):
        if raw == 'undefined':
            return None
        else:
            return int(raw)

    def __init__(self, raw, api):
        super().__init__(raw, api)

        self.dryers = self._int(raw['dryer'])
        self.washers = self._int(raw['washer'])


class Total(Available):
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
        self.idle = (self.status == 'Idle')


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
        self.number = int(self.label)
        self.type = raw['appliance_type']
        self.washer = (self.type == 'WASHER')
        self.dryer = (self.type == 'DRYER')
        self.status_raw = raw['status']
        self.available = (self.status == 'Available')
        self.in_use = (self.status == 'In Use')
        self.idle = (self.status == 'Idle')
        # TODO: there are probably more statuses

    @property
    def status(self):
        return self.api.status(self.key)


class Use:
    def __init__(self, available, total):
        self.available = available
        self.total = total


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

    def room(self, identifier):
        rooms = self.rooms()
        try:
            return next(room for room in rooms if room.id == identifier or room.name == identifier.upper())
        except StopIteration:
            return None

    def available(self, location):
        return Available(self.get('room', 'getNumAvailable', {'location': location})['laundry_room'], self)

    def total(self, location):
        return Total(self.get('room', 'getTotal', {'location': location})['laundry_room'], self)

    def use(self, location):
        """
        Helper method to get both available and total for a given location.
        """
        return Use(self.available(location),
                   self.total(location))

    def status(self, key):
        return Status(self.get('appliance', 'getStatus', {'appliance_desc_key': key})['appliance'], self)

    def appliances(self, location):
        return [Appliance(raw, self) for raw in
                self.get('room', 'getAppliances', {'location': location})['laundry_room']['appliances']['appliance']]
