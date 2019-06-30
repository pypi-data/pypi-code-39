import uuid
import json
from geopy.geocoders import Nominatim


def averageCoordinate(coords):
    av = [sum(x)/len(x) for x in zip(*coords)]
    return av


def retrieveAddress(longitude, latitude):
    geolocator = Nominatim(user_agent="in-the-pocket")
    q = f"{latitude}, {longitude}"
    location = geolocator.reverse(q)
    return location.raw


class Address:
    def __init__(self, data, verbose):

        print("===> ✨ NEW ADDRESS***\n")

        if(data["address"].get("house_number")):
            self.unit = data["address"]["house_number"]

        else:
            self.unit = None

        self.uid = str(uuid.uuid4())
        self.locality = data["address"]["city"]
        self.address = data["address"]["road"]
        self.country = data["address"]["country_code"].upper()
        self.postal_code = data["address"]["postcode"]
        self.dictionary = self.as_dict(verbose)

    def as_dict(self, verbose):
        add = {
            "id": self.uid,
            "type": "Feature",
            "feature_type": "address",
            "geometry": None,
            "properties": {
                "address": self.address,
                "unit": self.unit,
                "locality": self.locality,
                # TODO: fix hardcoded provinces
                "province": "BE-VOV",
                "country": self.country,
                "postal_code": self.postal_code,
                "postal_code_ext": None
            }
        }
        if(verbose):
            print(json.dumps(add, sort_keys=False, indent=4))
            print("\n")
        return add


class Unit():
    def __init__(self, data, level, verbose):

        self.uid = str(uuid.uuid4())
        self.name = data["features"][0]["properties"]["name"]
        self.coordinates = data["features"][0]["geometry"]["coordinates"][0]
        self.average = averageCoordinate(self.coordinates[0])
        # print(self.coordinates)
        self.level = level
        self.dictionary = self.as_dict(verbose)
        print(f"==> ✨ NEW UNIT {self.name} FOR LEVEL {self.level}\n")

    def as_dict(self, verbose):
        unit = {
            "id": self.uid,
            "type": "Feature",
            "feature_type": "unit",
            "geometry": {
                "type": "Polygon",
                "coordinates": self.coordinates
            },
            "properties": {
                "category": "room",
                "restriction": None,
                "accessibility": None,
                "name": {
                    "en": self.name
                },
                "alt_name": None,
                "display_point": {
                    "type": "Point",
                    "coordinates": [self.average[0], self.average[1]],
                },
                "level_id": self.level
            }
        }
        if(verbose):
            print(json.dumps(unit, sort_keys=False, indent=4))
            print("\n")
        return unit


class Level():
    def __init__(self, data, building, verbose):

        self.uid = str(uuid.uuid4())
        self.name = data["name"]
        self.ordinal = int(self.name)
        self.coordinates = data["features"][0]["geometry"]["coordinates"][0]
        self.average = averageCoordinate(self.coordinates[0])
        self.building = building
        self.dictionary = self.as_dict(verbose)
        print(
            f"===> ✨ NEW LEVEL: {self.ordinal} FOR BUILDING {self.building}\n")

        # BAD HAXXX
        if(self.ordinal == -1):
            self.dictionary["properties"]["category"] = "parking"
        # DELETE EVENTUALLY

    def as_dict(self, verbose):
        level = {
            "id": self.uid,
            "type": "Feature",
            "feature_type": "level",
            "geometry":
            {
                "type": "Polygon",
                "coordinates": self.coordinates
            },
            "properties": {
                "category": "parking",
                "restriction": None,
                "ordinal": self.ordinal,
                "outdoor": False,
                "name":
                {"en": self.name},
                "short_name":
                {
                    "en": self.name
                },
                "display_point": {
                    "type": "Point",
                    "coordinates": [self.average[0], self.average[1]],
                },
                "address_id": None,
                "building_ids": [self.building]
            }
        }
        if(verbose):
            print(json.dumps(level, sort_keys=False, indent=4))
            print("\n")
        return level


class Footprint:
    def __init__(self, data, verbose):
        self.uid = str(uuid.uuid4())
        self.geometry = data["features"][0]["geometry"]["coordinates"][0]
        self.name = data["features"][0]["properties"]["name"]
        self.category = data["features"][0]["properties"]["category"]
        self.average = averageCoordinate(self.geometry[0])
        self.buildings = []
        print(f"===>  ✨ NEW FOOTPRINT: {self.uid} ***\n")
        self.dictionary = self.as_dict(verbose)

    def assignBuilding(self, id):

        self.buildings.append(id)

    def as_dict(self, verbose):
        footprint_collection = {
            "type": "FeatureCollection",
            "features": []
        }

        footprint = {
            "id": self.uid,
            "type": "Feature",
            "feature_type": "footprint",
            "geometry":
            {
                "type": "Polygon",
                "coordinates": self.geometry
            },
            "properties": {
                "category": self.category,
                "name":
                {"en": self.name},
                "building_ids": self.buildings
            }
        }

        footprint_collection["features"].append(footprint)

        if(verbose):
            print(json.dumps(footprint_collection, sort_keys=False, indent=4))
            print("\n")
        return footprint_collection

    def toFile(self):
        dict = self.as_dict(False)
        with open('output/footprint.geojson', 'w+') as outfile:
            json.dump(dict, outfile, indent=4)


class Building():
    def __init__(self, footprint, venue, verbose):
        self.uid = str(uuid.uuid4())

        print(f"===> ✨ NEW BUILDING 🏛  FROM FOOTPRINT: {footprint.uid}\n")
        footprint.assignBuilding(self.uid)
        venue.assignBuilding(self.uid)
        self.name = footprint.name
        self.coordinates = footprint.average
        self.dictionary = self.as_dict(verbose)

    def as_dict(self, verbose):
        building = {
            "id": self.uid,
            "type": "Feature",
            "feature_type": "building",
            "properties":
            {
                "category": "unspecified",
                "restriction": None,
                "name":
                {
                    "en": self.name,
                },
                "alt_name": None,
                "display_point":
                {
                    "type": "Point",
                    "coordinates": self.coordinates
                },
                "address_id": None,
            },
            "geometry": None,
        }
        if(verbose):
            print(json.dumps(building, sort_keys=False, indent=4))
            print("\n")

        return building


class Venue:
    def __init__(self, data, verbose):
        self.uid = str(uuid.uuid4())

        print(f"===> ✨ NEW VENUE: {self.uid} ***\n")
        self.props = data["features"][0]["properties"]
        self.geometry = data["features"][0]["geometry"]["coordinates"][0]
        self.average = averageCoordinate(self.geometry[0])
        self.address = None
        self.buildings = []
        self.dictionary = self.as_dict(verbose)

    def assignBuilding(self, uid):
        self.buildings.append(uid)

    def assignAddressID(self, uid):
        # print(f"assigning address {uid} to  {self.uid}")
        self.address = uid

    def as_dict(self, verbose):
        dict = {
            "type": "FeatureCollection",
            "features": [
                {
                    "id": self.uid,
                    "type": "Feature",
                    "feature_type": "",
                    "geometry":
                    {
                        "type": "Polygon",
                        "coordinates": self.geometry
                    },
                    "properties":
                    {
                        "category": self.props["category"],
                        "restriction": self.props["restrictio"],
                        "name":
                        {"en": self.props["name"]},
                        "alt_name":
                        {
                            "en": self.props["alt_name"]
                        },
                        "hours": self.props["hours"],
                        "website": self.props["website"],
                        "phone": self.props["phone"],
                        "display_point": {
                            "type": "Point",
                            "coordinates": [self.average[0], self.average[1]],
                        },

                        "address_id": self.address,

                    }
                }
            ]
        }

        if(verbose):
            print(json.dumps(dict))
            print("\n")
        return dict

    def toFile(self):
        dict = self.as_dict(False)
        with open('output/.geojson', 'w') as outfile:
            json.dump(dict, outfile, indent=4)
