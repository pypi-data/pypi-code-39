import json
from collections import OrderedDict
from django.contrib.postgres.fields.jsonb import JSONField, JsonAdapter


class JsonOrderedAdapter(JsonAdapter):

    def add_order(self, dictionary):
        dict_ordered = {}
        for i,v in enumerate(OrderedDict(dictionary).items()): 
            dict_ordered[v[0]]={"value":v[1], "order":i}
        return dict_ordered

    def dumps(self, obj):
        options = {'cls': self.encoder} if self.encoder else {}

        return json.dumps(self.add_order(obj), **options)


class JsonOrderedField(JSONField):

    def parser_json_ordered(self, dictionary):
        dictionary_sorted = sorted(dictionary.items(), key=lambda item: item[1].get('order'))
        dictionary_sorted = OrderedDict([(key, value.get('value')) for key,value in dictionary_sorted])
        return dict(dictionary_sorted)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.parser_json_ordered(value)

    def to_python(self, value):
        if isinstance(value, OrderedDict):
            return value

        if value is None:
            return value

        return self.parser_json_ordered(value)

    def get_prep_value(self, value):
        if value is not None:
            return JsonOrderedAdapter(value, encoder=self.encoder)
        return value