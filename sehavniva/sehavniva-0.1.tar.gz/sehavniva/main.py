# -*- coding: utf-8 -*-

import requests
import xmltodict

""" python client for the norwegian mapping authority's water level api """

from .const import (
    DATATYPE,
    REFCODE,
    TIDE_REQUEST,
    TZONE,
    API_URL,
    )


class SehavnivaClient():

    def __init__(self):
        pass

    # this will get the next tide event inside the fromtime to totime interval
    def get_tide_events(self, lat, lon, fromtime, totime):

        events = []
        
        _payload = {"lat": lat,
                    "lon": lon,
                    "datatype": DATATYPE,
                    "refcode": REFCODE,
                    "fromtime": fromtime,
                    "totime": totime,
                    "tide_request": TIDE_REQUEST,
                    "tzone": TZONE
                    }
                    
        r = requests.get(API_URL, params=_payload)

        data = xmltodict.parse(r.text)

        for tideevent in data["tide"]["locationdata"]["data"]["waterlevel"]:
            events.append(
                {"value": float(tideevent['@value']),
                 "flag": tideevent['@flag'],
                 "time": tideevent['@time']}
            )

        return events
