# these functions do not give correct output in edge cases, if those need to be handled they will be updated
# accordingly


def camel_to_snake(string):
    parts = []
    word = []

    for char in string:
        if char.isupper():
            _word = ''.join(word)
            parts.append(_word)
            word = [char.lower()]
        else:
            word.append(char)
    _word = ''.join(word)
    parts.append(_word)

    return '_'.join(parts[1:])


def snake_to_camel(string):
    parts = string.split('_')
    camelized = ''.join(f'{x[0].upper()}{x[1:]}' for x in parts)
    return f'{parts[0]}{camelized}'
