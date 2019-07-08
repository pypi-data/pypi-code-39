from .element import ABCElement


class _Node(ABCElement):
    schema = {
        **ABCElement.schema,
        "uid": {"type": "string", "required": True, "regex": "^[a-zA-Z]\\w*$"},
        "display_name": {
            "type": "string",
            "required": False,
            "default_setter": lambda doc: doc["uid"],
        },
        "location": {
            "type": "dict",
            "required": True,
            "schema": ABCElement.location_schema(True),
        },
        "schematic_location": {
            "type": "dict",
            "required": False,
            "schema": ABCElement.location_schema(False),
            "default_setter": lambda doc: doc["location"],
        },
        "tags": {"type": "list", "required": False, "schema": {"type": "string"}},
    }


class Junction(_Node):
    pass


class LevelBoundary(_Node):
    pass


class FlowBoundary(_Node):
    pass


class Storage(_Node):
    schema = {
        **_Node.schema,
        "level_volume": {
            "type": "list",
            "required": True,
            "minlength": 2,
            "schema": {
                "type": "dict",
                "schema": {
                    "level": {"type": "float", "required": True},
                    "volume": {"type": "float", "required": True, "min": 0},
                },
            },
        },
    }
