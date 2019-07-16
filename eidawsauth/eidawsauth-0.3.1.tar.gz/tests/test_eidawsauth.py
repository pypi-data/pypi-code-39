import sys
sys.path.append('eidawsauth')

import os
import pytest
from eidawsauth import eidawsauth
from pprint import pprint
import gnupg

GPGHOMEDIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files/gpg_home',
    )

@pytest.fixture
def gpg(tmp_path):
    gpg = gnupg.GPG(gnupghome=GPGHOMEDIR)
    return gpg

@pytest.fixture
def client():
    client = eidawsauth.application.test_client()
    yield client

def test_auth_get(client):
    """
    Get method should return 405
    """
    rv = client.get('/')

    assert  rv.status_code == 405

def test_auth_post_empty(client):
    """
    Test a post with no data, should return 415
    """
    rv = client.post('/')
    assert  rv.status_code == 415

def test_auth_post_nodata(client):
    """
    Test to post random stuff, should return 415
    """
    rv = client.post('/',data="blablabla")
    assert rv.status_code == 415


def test_auth_post_old_token(client, gpg):
    """
    Test posting an expired token.
    Should return 415 and an error message containing the date.
    """
    # First generate a nice token
    content = '{"valid_until": "2010-03-19T09:07:10.096722Z", "cn": "Jonathan SCHAEFFER", "memberof": "/epos;/", "sn": "SCHAEFFER", "issued": "2019-03-18T09:07:10.096727Z", "mail": "jonathan.schaeffer@univ-grenoble-alpes.fr", "givenName": "Jonathan", "expiration": "1d"}'
    old_token = str(gpg.sign(content))
    rv = client.post('/',data=old_token)
    assert rv.status_code == 415

def test_auth_post_valid_token(client, gpg):
    if 'RUNMODE' in os.environ and os.environ['RUNMODE'] == 'development':
        content = '{"valid_until": "2020-03-19T09:07:10.096722Z", "cn": "Jonathan SCHAEFFER", "memberof": "/epos;/", "sn": "SCHAEFFER", "issued": "2019-03-18T09:07:10.096727Z", "mail": "jonathan.schaeffer@univ-grenoble-alpes.fr", "givenName": "Jonathan", "expiration": "1d"}'
        token = str(gpg.sign(content))
        rv = client.post('/',data=token)
        assert rv.status_code == 200

def test_cleanup(client):
    if 'RUNMODE' in os.environ and os.environ['RUNMODE'] == 'development':
        rv = client.get('/cleanup')
        assert rv.status_code == 200
