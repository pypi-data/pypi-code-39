from . import field_exists_checker
from . import field_value_checker
from . import field_has_value_checker

def getFieldExistsChecker(data, field_name):
    return field_exists_checker.FieldExistsChecker(data, field_name)

def getFieldValueChecker(data, field_name, dield_value):
    return field_value_checker.FieldValueChecker(data, field_name, dield_value)

def getFieldHasValueChecker(data, field_name):
    return field_has_value_checker.FieldHasValueChecker(data, field_name)
