from datetime import datetime, timezone
from decimal import Decimal


def cents_to_decimal(amount: str) -> Decimal:
    return Decimal(amount) / 100


def decimal_to_cents(amount: Decimal) -> str:
    return str((amount * 100).quantize(Decimal("1")))


def parse_datetime(d: str) -> datetime:
    """
    A very naive Zulu time parser that returns a time zone aware datetime

    :param d: A datetime string in Zulu time with microseconds e.g.: "2019-04-15T13:40:19.151Z"
    """
    # TODO: Replace this datetime.fromisoformat when only Python 3.7 is supported
    return datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)


def format_datetime(d: datetime) -> str:
    """
    Converts a timezone aware datetime object into a UTC ISO 8601 (Zulu time) string
    """
    if not d.tzinfo:
        raise Exception("Naive datetime not supported")
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
