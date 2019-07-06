import re


def _get_property_getter(attribute_name):
    def property_getter(self):
        return getattr(self, attribute_name)

    return property_getter


def _get_property_setter(attribute_name, notify_objects):

    def property_setter(self, value):
        if getattr(self, attribute_name) is not value:
            for notify_object in notify_objects:
                notify_object(
                    self,
                    id(self),
                    attribute_name.strip('__'),
                    getattr(self, attribute_name),
                    value
                )
            setattr(self, attribute_name, value)

    return property_setter


def _create_properties(instance, cls, notify_objects):
    attr_list = list(instance.__dict__.keys())
    new_attrs = {}

    for attr_name in filter(
            lambda x: re.match(instance.pattern, x), attr_list
    ):
        new_attr_name = '__' + attr_name
        value = instance.__dict__.pop(attr_name)
        new_attrs[new_attr_name] = value

        setattr(instance, new_attr_name, value)

        getter = property(_get_property_getter(new_attr_name))
        setattr(cls, attr_name, getter)

        setter = getter.setter(
            _get_property_setter(new_attr_name, notify_objects)
        )
        setattr(cls, attr_name, setter)

    setattr(cls, '__init__', _get_init_method(new_attrs, cls.__init__))

    return instance


def _get_init_method(attributes, original_init_method):

    def init(self, *args, **kwargs):
        for key in attributes:
            setattr(self, key, attributes[key])

        original_init_method(self, *args, **kwargs)

    return init


def _get_setattr_method(cls):

    def set_attr_method(self, key, value):
        print(key, value, self.pattern)
        if re.match(self.pattern, key):
            super(cls, self).__setattr__('__' + key, value)

        super(cls, self).__setattr__(key, value)

    return set_attr_method


class ObservablesFactory(type):
    _notify_methods = []
    _processed = set()

    def __call__(cls, *args, **kwargs):
        instance = super(ObservablesFactory, cls).__call__(*args, **kwargs)

        if issubclass(cls, Observable) and cls not in cls._processed:
            cls._processed.add(cls)
            instance = _create_properties(instance, cls,  cls._notify_methods)

        elif issubclass(cls, Observer):
            instance = super(ObservablesFactory, cls).__call__(*args, **kwargs)
            cls._notify_methods.append(instance.notify)

        return instance


class Observable(metaclass=ObservablesFactory):
    pattern = r'.*'


class Observer(metaclass=ObservablesFactory):

    def notify(self, class_name, object_id, attribute_name, old, new):
        pass

