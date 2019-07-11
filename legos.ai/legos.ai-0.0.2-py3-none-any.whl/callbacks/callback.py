from legos.utils import camel2snake


class Callback():
    order = 0

    def __init__(self):
        self.learner = None

    @property
    def name(self):
        """
        Get the callback name in snake_case format
        """
        name = camel2snake(self.__class__.__name__)
        return name.replace("_callback", "")

    def __repr__(self):
        return f'{self.name}'
