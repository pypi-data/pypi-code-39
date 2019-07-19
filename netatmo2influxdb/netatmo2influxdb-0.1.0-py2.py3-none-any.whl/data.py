import json
import os

from logger import logger
import requests

import db
import tokens

from datetime import datetime

NETATMO_BASE = os.getenv("NETATMO_BASE")


def get_home(username):
    """
    Get all home and room info. Returns a dict with the following strucuture

    ```
    {
     "home_id_1":
        {"name": str,
         "rooms": [
             {"id": str,
              "name": str
             }, ...
         ]
        },
     "home_id_2": ...
    }
    ```
    """
    logger.debug(f"Retrieving home information for user {username}")
    url = NETATMO_BASE + "api/homesdata"
    params = {"access_token": tokens.get_access_token(username)}
    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        logger.critical(f"Retrieving home information for user {username} failed")
        raise ConnectionError(f"Failed getting data: {resp.content}")

    parsed_resp = json.loads(resp.content)
    homes = {}
    logger.debug("Parsing home information")
    for home in parsed_resp["body"]["homes"]:
        homes[home["id"]] = {"name": home["name"], "rooms": []}
        for room in home["rooms"]:
            homes[home["id"]]["rooms"].append({"id": room["id"], "name": room["name"]})
    return homes


def get_measurements(username, homes, dry):
    """
    Retrieve thermostat measurements for all homes and rooms
    """
    logger.debug(f"Starting retrieval of measurements for user {username}")
    measurements = {}
    for home_id in homes.keys():  # Every home
        home = homes[home_id]
        home_name = home["name"]
        logger.debug(f"Retrieving data for home {home_name} ({home_id})")
        measurements[home_id] = {"id": home_id, "name": home_name, "rooms": {}}
        for room in home["rooms"]:  # Every room in home
            room_id = room["id"]
            room_name = room["name"]
            logger.debug(
                f"Preparing retrieval of data for room {room_name} ({room_id})"
            )
            measurements[home_id]["rooms"][room_id] = {
                "id": room_id,
                "name": room_name,
                "data": {},
            }
            # Get last requested object
            last_record = db.get_last_record(username, home_id, room_id)
            # Add 30 minutes to that last record or use None as start date
            start_date = last_record["end_ts"] + 1800 if last_record else None

            while True:  # Keep requesting data until last page is reached
                # Parse date for logger
                parsed_start_date = (
                    "scratch"
                    if start_date is None
                    else datetime.utcfromtimestamp(int(start_date)).isoformat()
                )
                logger.debug(
                    f"Retrieving data for room {room_name} ({room_id}) from {parsed_start_date}"  # noqa: E501
                )

                # Start collecting data
                collection = collect(
                    start_date, username, home_id=home_id, room_id=room_id, dry=dry
                )
                if collection:
                    measurements[home_id]["rooms"][room_id]["data"].update(
                        collection["data"]
                    )
                    start_date = (
                        collection["end_ts"] + 1800
                    )  # Add thirty minute after last record
                    count = collection["count"]
                    logger.debug(
                        f"Retrieved {count} records for room {room_name} ({room_id})"
                    )
                    if count < 1024:  # Last page
                        break
                else:  # No data
                    logger.debug(f"No data for for room {room_name} ({room_id})")
                    break

    return measurements


def collect(start_date, username, home_id, room_id, dry):
    url = NETATMO_BASE + "api/getroommeasure"
    params = {
        "access_token": tokens.get_access_token(username),
        "home_id": home_id,
        "room_id": room_id,
        "scale": "30min",
        "type": "temperature",
        "date_begin": str(start_date),
        "real_time": True,
        "optimize": False,
    }
    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        raise ConnectionError(f"Failed getting data: {resp.content}")

    parsed_resp = json.loads(resp.content)
    data = parsed_resp["body"]
    count = len(parsed_resp["body"])
    if count > 0 and not dry:
        start_ts = int(min(parsed_resp["body"].keys()))
        end_ts = int(max(parsed_resp["body"].keys()))
        db.create_record(username, home_id, room_id, start_ts, end_ts, count)
        return {"data": data, "start_ts": start_ts, "end_ts": end_ts, "count": count}

    return None
