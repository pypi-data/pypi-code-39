import json


class Definition:

    def __init__(self, name, description, subscription_id):
        self.name = name
        self.role = {
            'Name': name,
            'Description': description,
            'Actions': [],
            'DataActions': [],
            'NotDataActions': [],
            'AssignableScopes': ["/subscriptions/{}".format(subscription_id)]
        }

    def add_action(self, action):
        self.role['Actions'].append(action)

    def add_data_action(self, action):
        self.role['DataActions'].append(action)

    def add_not_data_action(self, action):
        self.role['NotDataActions'].append(action)

    @property
    def json(self):
        return json.dumps(self.role)
