import faker
import arrow

__all__ = [
    "pick_random_time_between",
]

def pick_random_time_between(faker:faker.Generator, start:arrow.Arrow, stop:arrow.Arrow) -> arrow.arrow:
    return arrow.get(faker.date_time_between(start.datetime, stop.datetime))