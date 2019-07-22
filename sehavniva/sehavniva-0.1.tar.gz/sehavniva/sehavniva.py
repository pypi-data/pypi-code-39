import requests
import xmltodict

""" python client towards the norwegian mapping authority's water level api """

DATATYPE = "tab"
REFCODE = "cd"
TIDE_REQUEST = "locationdata"
TZONE = 0


class KartverketClient(object):
    __KARTVERKET_API_URL = "http://api.sehavniva.no/tideapi.php"

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
                    
        r = requests.get(self.__KARTVERKET_API_URL, params=_payload)

        data = xmltodict.parse(r.text)

        for tideevent in data["tide"]["locationdata"]["data"]["waterlevel"]:
            events.append(
                {"value": float(tideevent['@value']),
                 "flag": tideevent['@flag'],
                 "time": tideevent['@time']}
            )

        return events
