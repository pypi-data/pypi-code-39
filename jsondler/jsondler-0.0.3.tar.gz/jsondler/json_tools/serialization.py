import datetime


def serialize_field(fd):
    if isinstance(fd, datetime.datetime):
        return fd.__str__()
    else:
        return str(fd)
