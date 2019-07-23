from influxdb import InfluxDBClient, SeriesHelper
import os
from datetime import datetime


def _create_client():
    """
    returns a InfluxDBClient object. Always tests connectivity before returning.
    """
    client = InfluxDBClient(
        host=os.getenv("INFLUX_HOST", "localhost"),
        port=int(os.getenv("INFLUX_PORT", 8086)),
        username=os.getenv("INFLUX_USER", ""),
        password=os.getenv("INFLUX_PASSWORD", ""),
        database=os.getenv("INFLUX_DB"),
    )

    # Check if client is available
    try:
        client.ping()
    except Exception:
        raise ConnectionError("Could not connect to InfluxDB")
    return client


def _create_series_helper(custom_tags={}):
    """
    Create a custom InfluxDB Series Helper, dynamically adding custom_tags
    """
    custom_tags_list = list(custom_tags.keys())

    class SensorSeriesHelper(SeriesHelper):
        class Meta:
            client = _create_client()
            series_name = "thermostat"
            fields = ["time", "temperature"]
            tags = [
                "user",
                "home_name",
                "home_id",
                "room_name",
                "room_id",
            ] + custom_tags_list
            bulk_size = 512
            autocommit = True

    return SensorSeriesHelper


def store_measurements(
    user: str,
    home_id: str,
    home_name: str,
    room_id: str,
    room_name: str,
    room_data: dict,
    custom_tags: dict,
):
    """
    Stores measurements Netatmo-data in InfluxDB
    """
    series_helper = _create_series_helper(custom_tags)

    # TODO: Allow for custom_tags to be logically assigned, rather than fixed

    # Loop over room_data and add to series_helper
    for key, value in room_data.items():
        series_helper(
            user=user,
            home_name=home_name,
            home_id=home_id,
            room_name=room_name,
            room_id=room_id,
            time=_parse_timestamp(int(key)),
            temperature=float(
                round(value[0], 1)
            ),  # For influxdb the type should always be float
            **custom_tags  # Unpack custom_tags dict
        )

    # Commit remainder
    series_helper.commit()


def _parse_timestamp(ts: int):
    """
    Creates UTC-timestamp from Epoch ts
    """
    return datetime.utcfromtimestamp(ts).isoformat()
