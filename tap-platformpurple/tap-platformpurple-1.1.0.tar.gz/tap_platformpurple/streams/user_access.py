from tap_platformpurple.streams.base import BaseDatePaginatedPlatformPurpleStream
from dateutil.parser import parse


class UserAccessStream(BaseDatePaginatedPlatformPurpleStream):
    TABLE = "user_access"
    KEY_PROPERTIES = ["userEmail", "productID", "startDateTime"]
    API_METHOD = "POST"

    def get_stream_data(self, data):
        return [self.transform_record(item) for item in data.get("data")]

    def get_time_for_state(self, item):
        return parse(item.get("startDateTime"))

    def get_url(self):
        return "https://api-v4-staging.platformpurple.com/api/stats/userAccess4Org"

    def get_filters(self):
        return None
