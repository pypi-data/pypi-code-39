# -*- coding: utf-8 -*-
"""The tgapp-calendarevents package"""
from calendarevents.lib.event_type import EventType


def plugme(app_config, options):
    # configurations for 2.3 and 2.4
    try:
        app_config['_calendarevents'] = options  # 2.3
    except TypeError as ex:
        app_config.update_blueprint({
            '_calendarevents': options  # 2.4
        })
    return dict(appid='calendarevents', global_helpers=False)

