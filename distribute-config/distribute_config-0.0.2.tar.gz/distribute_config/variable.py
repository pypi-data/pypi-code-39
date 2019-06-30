class Variable:
    """A config variable
    """

    def __init__(self, name, default, description, type, is_list=False):
        # Variable name, used as key in yaml, or to get variable via command line and env varaibles
        self.name = name

        # Description of the variable, used for --help
        self.description = description

        # Type of the variable, can be int, float, str
        self.type = type
        self.is_list = is_list

        # The value of the variable
        self._value = None
        self.set_value(default)

    def get_value(self):
        return self._value

    def set_value(self, value):
        """Check if the value match the type of the variable and set it

        Args:
            value: The new value of the variable, will be checked before updating the var 

        Raises:
            TypeError: if the type of value doesn't matche the type of the variable
        """

        if self.is_list:
            assert type(value) == list
            end_list = []
            for element in value:
                end_list.append(self._convert_type(element))
            self._value = end_list
        else:
            self._value = self._convert_type(value)

    def _convert_type(self, value):
        if self.type in [str, float]:
            return self.type(value)
        # Now self.type == int
        if type(value) == str:
            value = float(value)
        if type(value) == float:
            if int(value) == value:
                value = int(value)
            else:
                raise ValueError("value should have type {} but have type {}".format(self.type, type(value)))
        # now  type(value) == int
        return value
