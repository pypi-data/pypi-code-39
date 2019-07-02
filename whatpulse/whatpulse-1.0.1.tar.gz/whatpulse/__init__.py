import requests
import json
from urllib.parse import urljoin


class InvalidIPError(Exception):
    pass


class RealTime:

    def __init__(self, clicks_pressed, keys_typed, download_speed, upload_speed):
        self.clicks_typed = float(clicks_pressed)
        self.keys_typed = float(keys_typed)
        self.download_speed = download_speed
        self.upload_speed = upload_speed


class Rank:

    def __init__(self, clicks_pressed, keys_typed, upload, download, uptime):
        self.clicks_pressed = int(clicks_pressed)
        self.keys_typed = int(keys_typed)
        self.upload = int(upload)
        self.download = int(download)
        self.uptime = int(uptime)


class AccountTotals:

    def __init__(self, clicks_pressed, keys_typed, uptime, download, upload, rank):
        self.clicks_pressed = int(clicks_pressed)
        self.keys_typed = int(keys_typed)
        self.uptime = int(uptime)
        self.download = int(download)
        self.upload = int(upload)
        self.rank = rank


class UnPulsed:

    def __init__(self, clicks_pressed, keys_typed, download, upload, uptime):
        self.clicks_pressed = int(clicks_pressed)
        self.keys_typed = int(keys_typed)
        self.download = int(download)
        self.upload = int(upload)
        self.uptime = int(uptime)


class WhatPulse:

    def __init__(self, ip='localhost', port=3490):
        self.requests_session = requests.Session()
        self.ip = ip
        self.port = port
        self.uri = 'http://' + ip + ':' + str(port)

    @staticmethod
    def __check_status_code(r):
        if r.status_code == 200:
            return True
        elif r.status_code == 401:
            raise InvalidIPError('Connecting IP address not allowed in the client settings')

    def pulse(self):
        url = urljoin(self.uri, '/v1/pulse')
        r = self.requests_session.post(url)
        return WhatPulse.__check_status_code(r)

    def get_realtime_statistics(self):
        url = urljoin(self.uri, '/v1/realtime')
        r =  self.requests_session.get(url)
        WhatPulse.__check_status_code(r)
        realtime_json =r.content.decode()
        realtime_json = json.loads(realtime_json)
        return RealTime(
            clicks_pressed=realtime_json['clicks'],
            keys_typed=realtime_json['keys'],
            download_speed=realtime_json['download'],
            upload_speed=realtime_json['upload']
        )

    def get_account_total_statistics(self):
        url = urljoin(self.uri, '/v1/account-totals')
        r = self.requests_session.get(url)
        WhatPulse.__check_status_code(r)
        d = r.content.decode()
        d = json.loads(d)
        dr = d['ranks']
        return AccountTotals(
            clicks_pressed=d['clicks'],
            keys_typed=d['keys'],
            download=d['download'],
            upload=d['upload'],
            uptime=d['uptime'],
            rank=Rank(
                clicks_pressed=dr['rank_clicks'],
                keys_typed=dr['rank_keys'],
                upload=dr['rank_upload'],
                download=dr['rank_download'],
                uptime=dr['rank_uptime']
            )
        )

    def get_unpulsed_stats(self):
        url = urljoin(self.uri, 'http://localhost:3490/v1/unpulsed')
        r = self.requests_session.get(url)
        WhatPulse.__check_status_code(r)
        unpulsed_json = r.content.decode()
        unpulsed_json = json.loads(unpulsed_json)
        return UnPulsed(
            clicks_pressed=unpulsed_json['clicks'],
            keys_typed=unpulsed_json['keys'],
            upload=unpulsed_json['upload'],
            download=unpulsed_json['download'],
            uptime=unpulsed_json['uptime']
        )
