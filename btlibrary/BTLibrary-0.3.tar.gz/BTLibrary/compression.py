import zlib

import json, base64
import jsonpickle
ZIPJSON_KEY = 'base64(zip(o))'

def json_zip(j):

    j = {
        ZIPJSON_KEY: base64.b64encode(
            zlib.compress(
                jsonpickle.encode(j).encode('utf-8')
            )
        ).decode('ascii')
    }

    return j


def json_unzip(j, insist=True):
    try:
        assert (j[ZIPJSON_KEY])
        assert (set(j.keys()) == {ZIPJSON_KEY})
    except:
        if insist:
            raise RuntimeError("JSON not in the expected format {" + str(ZIPJSON_KEY) + ": zipstring}")
        else:
            return j

    try:
        j = zlib.decompress(base64.b64decode(j[ZIPJSON_KEY]))
    except:
        raise RuntimeError("Could not decode/unzip the contents")

    try:
        j = jsonpickle.decode(j)
    except:
        raise RuntimeError("Could interpret the unzipped contents")

    return j

    
if __name__=="__main__":
    json2 = {'atest':4}
    

    aa = json_zip(json2)
    bb = json_unzip(aa)
    
