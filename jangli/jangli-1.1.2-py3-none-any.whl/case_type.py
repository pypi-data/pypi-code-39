class CamelCase:
    def __init__(self, function):
        self.function = function
        self.obj = None

    def __call__(self, *args, **kwargs):
        try:
            self.obj = self.function(*args, **kwargs)
            func_dict = self.obj.__dict__
            class_var_value = {var: func_dict[var] for var in func_dict}
            for _var in class_var_value:
                self.obj.__setattr__(self.camel_type(_var), class_var_value[_var])
                self.obj.__delattr__(_var)

            return self.obj

        except Exception as e:
            print("Error while converting to camel case : {}".format(e))
            raise e

    def __instancecheck__(self, dec_class):
        return self.obj

    def camel_type(self, snake_str):
        try:
            return "".join(x.title() for x in snake_str.split("_"))
        except Exception as e:
            print("Error While converting to camel case : {}".format(e))
            raise e
