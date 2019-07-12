import dateutil.parser


class Pin(object):
    def __init__(self, id, lock_id, user_id, state, pin, slot,
                 access_type, created_at, updated_at, loaded_date,
                 first_name, last_name, unverified, access_start_time=None,
                 access_end_time=None, access_times=None):
        self.id = id
        self.lock_id = lock_id
        self.user_id = user_id
        self.state = state
        self.pin = pin
        self.slot = slot
        self.access_type = access_type
        self.first_name = first_name
        self.last_name = last_name
        self.unverified = unverified

        self.created_at = created_at
        self.updated_at = updated_at
        self.loaded_date = loaded_date
        self.access_start_time = access_start_time
        self.access_end_time = access_end_time
        self.access_times = access_times

    @property
    def createdAt(self):
        return dateutil.parser.parse(self.created_at)

    @property
    def updatedAt(self):
        return dateutil.parser.parse(self.updated_at)

    @property
    def loadedDate(self):
        return dateutil.parser.parse(self.loaded_date)

    @property
    def accessStartTime(self):
        if not self.access_start_time:
            return None
        return dateutil.parser.parse(self.access_start_time)

    @property
    def accessEndTime(self):
        if not self.access_end_time:
            return None
        return dateutil.parser.parse(self.access_end_time)

    @property
    def accessTimes(self):
        if not self.access_times:
            return None
        return dateutil.parser.parse(self.access_times)

    def __repr__(self):
        return "Pin(id={} firstName={}, lastName={})".format(
            self.id,
            self.first_name,
            self.last_name
        )
