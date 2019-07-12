import inspect


class Factory:
    _objects = None

    def __init__(self):
        self._objects = [self]

    def inject(self, *objects):
        self._objects.extend(objects)

    def secure(self, class_, **kwargs):
        if self._is_saved(class_):
            return self._find(class_)

        obj = self.make(class_, **kwargs)

        self._save(obj)

        return obj

    def make(self, class_, **kwargs):
        deps = self._get_dependencies(class_, kwargs)

        return class_(**deps)

    def _get_dependencies(self, class_, kwargs):
        params = inspect.signature(class_.__init__).parameters.items()
        filtered_params = [param for param in params if not self._should_ignore(param)]
        deps = {param[0]: self._get_dependency(param, kwargs) for param in filtered_params}

        return deps

    def _get_dependency(self, param, kwargs):
        name = param[0]
        annotation = param[1].annotation

        if name in kwargs:
            return kwargs[name]

        if annotation is inspect._empty:
            return None

        return self.secure(annotation)

    @staticmethod
    def _should_ignore(param):
        return param[0] in ['self', 'args', 'kwargs']

    def _find(self, class_):
        if not self._is_saved(class_):
            return None

        return self._filter_saved_objects_by_type(class_)[0]

    def _is_saved(self, class_):
        return bool(self._filter_saved_objects_by_type(class_))

    def _filter_saved_objects_by_type(self, class_):
        return [object_ for object_ in self._objects if isinstance(object_, class_)]

    def _save(self, obj):
        self._objects.append(obj)
