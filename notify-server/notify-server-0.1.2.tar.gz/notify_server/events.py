from threading import Thread
from time import sleep
from uuid import uuid4

from ruko import RDict


class EventDb:
    def __init__(self, ruko_host, ruko_port, event_name):
        self.db = RDict.client(ruko_host, ruko_port)
        event = self.db['events'][event_name]
        self.events = event['items']
        self.last_id = event['last_id']
        self.last_uuid = event['last_uuid']
        self.first_uuid = event['first_uuid']


class EventProducer:
    def __init__(self, ruko_host, ruko_port):
        self.db_params = (ruko_host, ruko_port)

    def produce(self, event, data):
        es = EventDb(*self.db_params, event)
        event_uuid = str(uuid4())
        # TODO: Add locking mechanism to prevent race conditions
        if es.last_uuid.get():
            es.events[es.last_uuid()]['next'] = event_uuid
        es.events[event_uuid] = {'event': event, 'data': data, 'next': None}
        last_id = es.last_id.get(default=0)
        es.last_uuid[()] = event_uuid
        if last_id == 0:
            es.first_uuid[()] = event_uuid
        es.last_id[()] = last_id + 1


class EventSubscriber(EventDb):
    def __init__(self, ruko_host, ruko_port, event_name):
        super().__init__(ruko_host, ruko_port, event_name)
        self.last_seen_id = self.last_id.get(default=0)
        self.last_seen_uuid = self.last_uuid.get()
        self.quit = False

    def get_next_event(self):
        while self.last_seen_id == self.last_id.get(default=0):
            if self.quit:
                return None
            sleep(0.05)
        if self.last_seen_uuid:
            new_uuid = self.events[self.last_seen_uuid]['next']()
        else:
            new_uuid = self.first_uuid()
        self.last_seen_uuid = new_uuid
        self.last_seen_id += 1
        return self.events[new_uuid](fields=['event', 'data'])

    def close(self):
        self.quit = True


class EventSystem:
    def __init__(self, ruko_host, ruko_port):
        self.ruko_host = ruko_host
        self.ruko_port = ruko_port
        self.producer = EventProducer(ruko_host, ruko_port)
        self.callbacks = {}

    def send(self, event, data):
        self.producer.produce(event, data)

    def subscribe(self, event, callback):
        if event not in self.callbacks:
            subscriber = EventSubscriber(self.ruko_host, self.ruko_port, event)
            callbacks = self.callbacks[event] = []
            Thread(target=self._handle_subscriber, args=[subscriber, callbacks], daemon=True).start()
        self.callbacks[event].append(callback)

    def unsubscribe(self, event, callback):
        callbacks = self.callbacks[event]
        callbacks.remove(callback)
        if not callbacks:
            del self.callbacks[event]

    def _handle_subscriber(self, subscriber: EventSubscriber, callbacks: list):
        while True:
            event = subscriber.get_next_event()
            if not event:
                return
            for fn in callbacks:
                fn(event)
