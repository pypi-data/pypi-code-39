import os
import sys



from ..git_values import GitValues

import os
import json

test_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = test_dir + "/data"

def test_get_required_files():
    gv = GitValues("prod-v3-croud", "croudtech-v3-service", "acl-api", region="eu-west-2", extra_files=["_system"])
    actual = gv.get_required_files()
    expected = [
        'prod/common.yaml',
        'prod/v3/common.yaml',
        'prod/v3/_croudtech-v3-service/common.yaml',
        'prod/v3/croud/common.yaml',
        'prod/v3/croud/croudtech-v3-service/common.yaml',
        'prod/v3/croud/croudtech-v3-service/_system.yaml',
        'prod/v3/croud/croudtech-v3-service/acl-api.yaml',
        'prod/v3/croud/croudtech-v3-service/acl-api/common.yaml',
        'prod/v3/croud/croudtech-v3-service/acl-api/_system.yaml',
        'prod/v3/croud/croudtech-v3-service/acl-api/acl-api.yaml',
        'eu-west-2/prod/common.yaml',
        'eu-west-2/prod/v3/common.yaml',
        'eu-west-2/prod/v3/_croudtech-v3-service/common.yaml',
        'eu-west-2/prod/v3/croud/common.yaml',
        'eu-west-2/prod/v3/croud/croudtech-v3-service/common.yaml',
        'eu-west-2/prod/v3/croud/croudtech-v3-service/_system.yaml',
        'eu-west-2/prod/v3/croud/croudtech-v3-service/acl-api.yaml',
        'eu-west-2/prod/v3/croud/croudtech-v3-service/acl-api/common.yaml',
        'eu-west-2/prod/v3/croud/croudtech-v3-service/acl-api/_system.yaml',
        'eu-west-2/prod/v3/croud/croudtech-v3-service/acl-api/acl-api.yaml'
    ]
    assert actual == expected

def test_get_existing_files():
    gv = GitValues("prod-v3-croud", "croudtech-v3-service", "acl-api", region="eu-west-2", extra_files=["_system"], download_path=data_dir + "/olive-production-helm-values")
    actual = gv.get_existing_files()
    expected = [
        'prod/v3/_croudtech-v3-service/common.yaml',
        'prod/v3/croud/croudtech-v3-service/_system.yaml',
        'prod/v3/croud/croudtech-v3-service/acl-api.yaml'
    ]
    assert actual == expected

def test_get_existing_files_regional():
    gv = GitValues("prod-v3-croud", "croudtech-v3-service", "acl-api", region="us-east-1", extra_files=["_system"], download_path=data_dir + "/olive-production-helm-values")
    actual = gv.get_existing_files()
    expected = [
        'prod/v3/_croudtech-v3-service/common.yaml',
        'prod/v3/croud/croudtech-v3-service/_system.yaml',
        'prod/v3/croud/croudtech-v3-service/acl-api.yaml',
        'us-east-1/prod/v3/_croudtech-v3-service/common.yaml',
    ]
    assert actual == expected

