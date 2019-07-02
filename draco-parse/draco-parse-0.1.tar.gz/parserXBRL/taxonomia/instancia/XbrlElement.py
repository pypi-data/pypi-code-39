class Element:

    def __init__(self, position=None, xml_line=None, name=None, decimals=None, id=None, context_ref=None, unit_ref=None,
                 value=None, label=None):
        if label is None:
            label = []
        self._position = position
        self._xml_line = xml_line
        self._name = name
        self._decimals = decimals
        self._id = id
        self._context_ref = context_ref
        self._unit_ref = unit_ref
        self._value = value
        self._label = label

    def __del__(self):
        pass
