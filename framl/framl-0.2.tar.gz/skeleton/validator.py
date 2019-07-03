
class Validator:

    def __init__(self, schema: dict ):
        self.schema = schema

    def validate(self, row: dict ) -> bool:
        if self.schema and row:
            return True

        return False