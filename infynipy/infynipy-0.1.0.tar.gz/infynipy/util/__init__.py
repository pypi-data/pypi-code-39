"""Package imports for utilities"""
import json

def get_type(obj):
    return type(obj).__class__.__name__

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj.__class__.__name__ == 'Infynity':
            return None
        return json.JSONEncoder.default(self, obj)
