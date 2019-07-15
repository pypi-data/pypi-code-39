"""Exporters export an object to an external end point, e.g. a calendar or
meetup.
"""
from meetspace.util import load_schema


class APINotFound(Exception):
    pass


class ApiTranslation:

    def __init__(self, schema_from, schema_to):
        self.from_name = schema_from
        self.to_name = schema_to
        self.associations = {}

        try:
            self.from_schema = load_schema(self.from_name)
            self.to_scehma = load_schema(self.to_name)
        except Exception:
            raise APINotFound

        try:
            self.associations = load_schema('associations.json')
        except Exception:
            raise ValueError("Associations file not found")

        self.associate_schemas()

    def associate_schemas(self):
        """create a one-way map between the two object representations.
        associations are always one-way from meetthigns -> api end point.
        object (e.g. form) = [
            { meetspace.object.field:
                (target.object.field, target.object.field.translator) } ]
        """

        for form, fields in self.associations.items():
            mappings = [field[self.to_name]
                        for name, field in fields.items()]

    def translate_fields(self):
        # probably treat this like validators on the form_factory.
        pass


class Exporter:

    def __init__(self):
        pass
