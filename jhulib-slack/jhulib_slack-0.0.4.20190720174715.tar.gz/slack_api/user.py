import json


class User(object):
    """ A Python object representation of the Slack user JSON blob """
    def __init__(self, json_blob=None):
        for key in json_blob.keys():
            setattr(self, key, json_blob[key])

    def to_json(self):
        return json.dumps(vars(self))
