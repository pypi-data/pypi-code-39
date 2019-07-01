
from collections import namedtuple


class PreHandleEventsSystem:
    ALL = 0
    _event_ids_and_handlers = []
    __max_event_id = 1

    @classmethod
    def define(cls, event_name: str, event_identifier_name: str, fields: list):
        event = namedtuple(event_name, fields)

        event.id = cls.__max_event_id

        event.add_handler = lambda handler: cls.add_handler(handler, event.id)

        event.on = lambda handler: cls.add_handler(handler, event.id)

        event.remove_handler = lambda handler: cls.remove_handler(
            handler, event.id)

        setattr(cls, event_name, event)
        setattr(cls, event_identifier_name, cls.__max_event_id)

        handlers = list()
        cls._event_ids_and_handlers.append((cls.__max_event_id, handlers))
        decorator = cls.call_handlers_on_event_creation(handlers)
        event.__new__ = decorator(event.__new__)

        cls.__max_event_id <<= 1
        cls.ALL = cls.__max_event_id - 1
        return event

    @staticmethod
    def call_handlers_on_event_creation(handlers_list):
        def decorator(event_creator):
            def wrapper(*args, **kwargs):
                event = event_creator(*args, **kwargs)
                for handler in handlers_list:
                    handler(event)
                return event
            return wrapper
        return decorator

    @classmethod
    def on(cls, event_types=-1):
        def decorator(handler):
            return cls.add_handler(handler, event_types)
        return decorator

    @classmethod
    def add_handler(cls, handler, event_types=-1):
        for event_id, handlers_list in cls._event_ids_and_handlers:
            if event_id & event_types:
                handlers_list.append(handler)
        return handler

    @classmethod
    def remove_handler(cls, handler, event_types=-1):
        for event_id, handlers_list in cls._event_ids_and_handlers:
            if event_id & event_types and handler in handlers_list:
                handlers_list.remove(handler)
