import re

def camel2snake(name):
    """
    Convert Camel Case to Snake Case. Source: https://stackoverflow.com/a/1176023
    Example:
    LoggerCallback -> logger_callback
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

