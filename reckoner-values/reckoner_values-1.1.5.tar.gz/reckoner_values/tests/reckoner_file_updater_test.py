import os
import sys
import json

try:
    from collections.abc import OrderedDict
except ImportError:
    from collections import OrderedDict

from ..reckoner_file_updater import ReckonerFileUpdater

test_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = test_dir + "/data"

def test_load_yaml():
    source = "{data_dir}/autohelm.yaml".format(data_dir=data_dir)
    dest = "{data_dir}/autohelm_dest.yaml".format(data_dir = data_dir)
    rfu = ReckonerFileUpdater(source=source, dest=dest, region="us-east-1")
    rfu.load_yaml()
    assert type(rfu.data) is OrderedDict

def test_add_files():
    source = "{data_dir}/autohelm.yaml".format(data_dir=data_dir)
    dest = "{data_dir}/autohelm_dest.yaml".format(data_dir=data_dir)
    download_path = data_dir + "/olive-production-helm-values"
    rfu = ReckonerFileUpdater(source=source, dest=dest, region="us-east-1", download_path=download_path)

    rfu.load_yaml()
    rfu.add_files()
    for chart_index in rfu.data['charts']:
        if "files" in rfu.data['charts'][chart_index]:
            for file in rfu.data['charts'][chart_index]['files']:
                full_path = "{}/{}".format(download_path, file)
                assert os.path.isfile("{}/{}".format(download_path, file)) == True
