from wtforms import ValidationError


class Length:
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            mesasge = u'Field must be between {} and {}'.format(min, max)

        self.message = message

    def __call__(self, form, field):
        length = field.data and len(field.data) or 0
        if length < self.min or self.max != -1 and length > self.max:
            raise ValidationError(self.message)


length = Length


class IsValidValue:
    def __init__(self, min=0, max=0, message=None):
        self.min = min
        self.max = max
        if not message:
            message = u'Field must be between {} and {}'.format(min, max)

        self.message = message

    def __call__(self, form, field):
        value = field.data
        if not (value <= self.max and value >= self.min):
            raise ValidationError(self.message)


isValidValue = IsValidValue
