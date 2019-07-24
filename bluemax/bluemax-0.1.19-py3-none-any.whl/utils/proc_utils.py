from importlib import import_module


def qname_to_class(qname):
    """ returns a class from module_name:class_name """
    _modules, _class = qname.split(":")
    return getattr(import_module(_modules), _class)
