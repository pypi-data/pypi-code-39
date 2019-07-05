import os

from flask import Flask, request
from flask_resto import Api

from notify_server.events import EventSystem

app = Flask(__name__)
api = Api(app)
event_system = EventSystem(os.environ['NS_RUKO_HOST'], int(os.environ['NS_RUKO_PORT']))


def submit_event(event):
    data = request.get_data().decode()
    event_system.send(event, data)
    return {'event': event, 'data': data}


api.resources = {
    '/event/<event>': {
        'POST': submit_event
    }
}
