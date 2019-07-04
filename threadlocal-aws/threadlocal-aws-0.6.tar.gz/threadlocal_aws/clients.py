import sys
from threadlocal_aws import _get_local_client, session, PY37
from threadlocal_aws.pep562 import Pep562

def __getattr__(name):
    return lambda **kwargs: _get_local_client(name, **kwargs)

if not PY37:
    Pep562(__name__)