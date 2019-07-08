import abc
from datetime import datetime

import cerberus
import isodate


class InvalidAttributeError(ValueError):
    pass


class ElementValidator(cerberus.Validator):
    types_mapping = cerberus.Validator.types_mapping.copy()
    purge_unknown = True

    def _normalize_default_setter_utcnow(self, document):
        timestamp = datetime.utcnow()
        timestamp = timestamp.replace(microsecond=0)
        return timestamp

    def _normalize_coerce_string_to_datetime(self, value):
        if isinstance(value, str):
            try:
                return isodate.parse_datetime(value)
            except isodate.ISO8601Error:
                pass
        return value


class ABCElement(abc.ABC):
    def __init__(self, validate_normalize: bool = True, **kwargs):
        super().__init__()
        if validate_normalize:
            # Validate and Normalize attributes
            validator = ElementValidator(self.schema)
            valid = validator.validate(kwargs)
            if not valid:
                raise InvalidAttributeError(validator.errors)
            attributes = validator.document
        else:
            attributes = kwargs

        # Store attributes
        self.__attributes = attributes
        self.__attributes["type"] = type(self).__name__

    def __getattr__(self, attr):
        try:
            return self.__attributes[attr]
        except KeyError as e:
            raise AttributeError(e)

    def __getitem__(self, attr):
        return self.__attributes[attr]

    def asdict(self):
        return self.__attributes.copy()

    schema = {
        "created": {
            "type": "datetime",
            "required": True,
            "default_setter": "utcnow",
            "coerce": "string_to_datetime",
        },
        "deleted": {
            "type": "datetime",
            "required": False,
            "coerce": "string_to_datetime",
        },
        "changes": {
            "type": "list",
            "required": False,
            "schema": {
                "type": "dict",
                "schema": {
                    "path": {"type": "string", "required": True},
                    "old_value": {
                        "type": ["number", "boolean", "string", "dict", "list"],
                        "required": True,
                    },
                    "datetime": {
                        "type": "datetime",
                        "required": True,
                        "default_setter": "utcnow",
                        "coerce": "string_to_datetime",
                    },
                },
            },
        },
    }

    @staticmethod
    def location_schema(z_required):
        return {
            "x": {"type": "float", "required": True},
            "y": {"type": "float", "required": True},
            "z": {"type": "float", "required": z_required},
        }
