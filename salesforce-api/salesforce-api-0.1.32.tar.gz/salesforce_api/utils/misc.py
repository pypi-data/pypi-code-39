import distutils.util
import requests
import hashlib


def parse_bool(input_value: str) -> bool:
    return distutils.util.strtobool(input_value)


def get_session(session: requests.Session = None):
    return session if isinstance(session, requests.Session) else requests.Session()

def hash_list(input_list):
    if not isinstance(input_list, list) or input_list is None:
        return None
    return hashlib.md5(str(input_list).encode())\
                  .hexdigest()
