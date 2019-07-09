class Timestep(object):
    def __init__(self, api_key=""):
        self.api_key = api_key

        self.name = None
        self.date = None
        self.value = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def elements(self):
        """Return a list of the elements which are not None"""

        elements = []

        for el in ct:
            if isinstance(el[1], meteocat_api.Element.Element):
                elements.append(el[1])

        return elements

