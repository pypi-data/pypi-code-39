from tinynetrc import Netrc
from pathlib import Path
import os
import sys
import dong

def get_credential_or_exit(message="Can't find any credential information, please login first."):
    netrc = load_netrc()
    login = netrc[dong.SERVER_NAME]['login']
    password = netrc[dong.SERVER_NAME]['password']
    if login is None or password is None:
        print(message)
        sys.exit(1)

    return (login, password)


def load_netrc():
    file = os.path.join(os.path.expanduser('~'), '.netrc')
    try:
        Path(file).touch()
    except PermissionError: 
        pass
    return Netrc(file=file)
