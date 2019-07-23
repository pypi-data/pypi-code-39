from re import sub


def replace_non_ascii(value: str, replace: str = '') -> str:
    if isinstance(value, str):
        return sub(r'[^\x00-\x7F]+', replace, value).strip() if len(value) else value
    elif value is None:
        return None
    else:
        raise Exception(f'Wrong type "{type(value)}" for replace_non_ascii. It must be a string.')
