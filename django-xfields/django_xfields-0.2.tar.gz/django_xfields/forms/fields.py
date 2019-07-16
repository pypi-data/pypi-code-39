from django.forms import fields

__all__ = ['CommaSeparatedStringsField', ]

class CommaSeparatedStringsField(fields.CharField):
    def prepare_value(self, value):
        return ','.join(value)