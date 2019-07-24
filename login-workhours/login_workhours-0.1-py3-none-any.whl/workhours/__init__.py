from collections import defaultdict
from datetime import timedelta
from datetime import datetime

import operator
import functools

from tabulate import tabulate
import utmp

DATE_FORMAT = "%Y-%m-%d"
EVENTS = {
    6: 'login',
    8: 'logout'
}


def get_events_from_fs():
    """Return all events, do not filter them"""
    with open('/var/log/wtmp', 'rb') as fd:
        buf = fd.read()
        for entry in utmp.read(buf):
            yield entry


def compute_days_duration(events):
    groups = defaultdict(functools.partial(defaultdict, list))

    for event in events:
        # Read all events, filter logins and logouts.
        if event.type.value in EVENTS.keys():
            # We onsider each day to start at 4am and end at 3:59am.
            # in order to make long stand-up nights belong to the
            # previous day.
            # It's a big hack, because the values we now use in the
            # computations are not correct, but it's okay in order
            # to compute a delta between start and end of day.
            fake_date = event.time - timedelta(hours=4)
            formated_date = fake_date.strftime(DATE_FORMAT)
            event_type = EVENTS[event.type.value]

            groups[formated_date][event_type].append(fake_date)
            groups[formated_date][event_type].sort()

    # For each day, get the first login and the last logout
    # and compute the diff between the two.
    days = dict()
    for day, info in groups.items():
        try:
            first_login = info['login'][0]
        except IndexError:
            first_login = None
        try:
            last_logout = info['logout'][-1]
        except IndexError:
            last_logout = None

        if first_login and last_logout:
            days[day] = round((last_logout - first_login).seconds / 3600, 2)

    return days


def group_days_per_week(days):
    weeks = defaultdict(float)
    for day, duration in days.items():
        week_number = datetime.strptime(day, DATE_FORMAT).isocalendar()[1]
        weeks[week_number] += duration

    return weeks


def print_weekly_workload(weeks):
    ordered_weeks = [(key, value) for key, value in weeks.items()]
    ordered_weeks.sort(key=operator.itemgetter(0))
    print(tabulate(ordered_weeks, headers=('Week #', 'Duration (hours)')))


def main():
    events = get_events_from_fs()
    days = compute_days_duration(events)
    weeks = group_days_per_week(days)
    print_weekly_workload(weeks)


if __name__ == '__main__':
    main()
