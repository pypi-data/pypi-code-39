import re
from decimal import Decimal

def get_operations(data):
    if data:
        if "cogs" in data:
            data["first_cost"] = data.pop('cogs')
        if "revenue" in data:
            data['transaction_amount'] = data.pop('revenue')
        return {field: str(data[field]).replace('{','').replace('}', '') for field in data if data[field]}
    return None


def calc(s):
    val = s.group()
    if not val.strip():
        return val
    return "%s" % eval(val.strip(), {'__builtins__': None})


def calculate(s):
    return re.sub(r"([0-9\ \.\+\*\-\/(\)]+)", calc, s)


def replacer(string: str, data:dict) -> str:
    for fname, fvalue in data.items():
        if fname in string:
            string = string.replace(fname, Decimal(fvalue).__str__())
    return string