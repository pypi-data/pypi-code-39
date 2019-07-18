import math



sin_cache = {}
cos_cache = {}


def fast_sin(x):
    deg = int(math.degrees(x))

    if deg in sin_cache:
        return sin_cache[deg]

    else:
        res = math.sin(x)
        sin_cache[deg] = res

        return res

def fast_cos(x):
    deg = int(math.degrees(x))

    if deg in cos_cache:
        return cos_cache[deg]

    else:
        res = math.cos(x)
        cos_cache[deg] = res
        
        return res