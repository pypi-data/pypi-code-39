def tag(name, content, singleton=False, **attribs):
    return f"<{name} {''.join([f'{attribute}={value!r} ' for attribute, value in attribs.items()])}>{content}{'</>' if not singleton else ''}"
