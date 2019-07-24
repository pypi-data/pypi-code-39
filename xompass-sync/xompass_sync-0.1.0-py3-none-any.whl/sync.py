import requests
from shapely.geometry.polygon import Polygon


class InvalidResponse(Exception):
    def __init__(self, res):
        super().__init__(f'Invalid response: {res.status_code}')
        self.res = res


class InvalidSensorData(Exception):
    def __init__(self, msg):
        super().__init__(f'Invalid sensor data: {msg}')


class Sensor:
    def __init__(self, sensor_datum):
        self.id = sensor_datum['id']
        self.name = sensor_datum['name']
        self.type = sensor_datum['type']
        self.parameters = sensor_datum['parameters']


class ConcentrationAlert(Sensor):
    def __init__(self, sensor_datum):
        super().__init__(sensor_datum)

        def tpoint(point):
            return (point['x'], point['y'])
        self.polygon = Polygon([tpoint(p) for p in self.parameters['points']])

    def __repr__(self):
        return f'ConcentrationAlert: {self.polygon}'


class ObjectRecognition(Sensor):
    def __init__(self, sensor_datum):
        super().__init__(sensor_datum)

    def __repr__(self):
        return f'ObjectRecognition({self.id})'


class CrossLineMultiRecognition(Sensor):
    def __init__(self, sensor_datum):
        super().__init__(sensor_datum)

        if not 'points' in self.parameters:
            raise InvalidSensorData('Expecting "points" in CLMR')
        if not type(self.parameters['points']) is list:
            raise InvalidSensorData('Expecting "points" to be list in CLMR')
        if len(self.parameters['points']) < 2:
            raise InvalidSensorData(
                'Expecting len("points") to be at least 2 in CLMR')

    def clr(self):
        return {
            'id': self.id,
            'x1': self.parameters['points'][0]['x'],
            'y1': self.parameters['points'][0]['y'],
            'x2': self.parameters['points'][1]['x'],
            'y2': self.parameters['points'][0]['y'],
            'multi': True
        }

    def __repr__(self):
        return f'CLMR {self.clr()}'


class Asset:
    def __init__(self, asset_id, sensors_data):
        self.id = asset_id

        def mksensor(datum):
            if datum['type'] == 'ConcentrationAlert':
                return ConcentrationAlert(datum)
            elif datum['type'] == 'ObjectRecognition':
                return ObjectRecognition(datum)
            elif datum['type'] == 'CrossLineMultiRecognition':
                return CrossLineMultiRecognition(datum)
        self.sensors = [mksensor(s) for s in sensors_data if s['enabled']]


def download_asset(asset_id, api_key):
    url = f'https://bridge-staging.xompass.com/api/Assets/{asset_id}/Sensors?api_key={api_key}'
    res = requests.get(url)
    if res.status_code != 200:
        raise InvalidResponse(res)
    return Asset(asset_id, res.json())
